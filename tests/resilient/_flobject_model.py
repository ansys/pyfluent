# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""A small server-side settings model driven by the real ``flobject`` tree.

It lets resilient mode be tested end to end through PyFluent's settings objects
(navigation, ``__setattr__``, commands with hyphenated names) without Fluent.
"""

from __future__ import annotations

import json
from pathlib import Path

from _resilient_fakes import FakeErrorState

from ansys.fluent.core.resilient.engine import (
    ActivationCandidate,
    ResilientAdapter,
)
from ansys.fluent.core.solver import flobject


class _Setting:
    attrs: dict = {}

    def __init__(self, parent):
        self.parent = parent

    def get_attrs(self, names):
        active = self.attrs.get("active?")
        if active is not None and not active(self):
            return {"active?": False}
        result = {}
        for name in names:
            if name in self.attrs:
                result[name] = self.attrs[name](self)
            else:
                result[name] = True if name == "active?" else None
        return result


class _Value(_Setting):
    objtype = "real"
    default = None

    def __init__(self, parent):
        super().__init__(parent)
        self.value = self.default

    def validate(self, value):
        pass

    def get_state(self):
        return self.value

    def set_state(self, value):
        self.validate(value)
        self.value = value

    @classmethod
    def get_static_info(cls):
        info = {"type": cls.objtype}
        if "allowed-values" in cls.attrs:
            info["has_allowed_values"] = True
        return info


class _Group(_Setting):
    objtype = "group"
    children: dict = {}
    commands: dict = {}

    def __init__(self, parent):
        super().__init__(parent)
        self.objs = {name: cls(self) for name, cls in self.children.items()}

    def get_state(self):
        return {
            name: obj.get_state()
            for name, obj in self.objs.items()
            if obj.get_attrs(["active?"]).get("active?", True)
        }

    def set_state(self, value):
        for name, state in value.items():
            self.objs[name].set_state(state)

    def get_child(self, name):
        return self.objs[name]

    def get_command(self, name):
        return self.commands[name](self)

    @classmethod
    def get_static_info(cls):
        info = {"type": cls.objtype}
        if cls.children:
            info["children"] = {n: c.get_static_info() for n, c in cls.children.items()}
        if cls.commands:
            info["commands"] = {n: c.get_static_info() for n, c in cls.commands.items()}
        return info


class _Command(_Setting):
    objtype = "command"
    arguments: dict = {}
    attrs = {
        "read-only?": lambda self: False,
        "arguments-aliases": lambda self: {},
    }

    def __call__(self, **kwds):
        return self.run(**kwds)

    def run(self, **kwds):
        raise NotImplementedError

    @classmethod
    def get_static_info(cls):
        info = {"type": cls.objtype}
        if cls.arguments:
            info["arguments"] = {n: {"type": t} for n, t in cls.arguments.items()}
        return info


def _root(obj):
    while obj.parent is not None:
        obj = obj.parent
    return obj


class Enabled(_Value):
    objtype = "boolean"
    default = False


class Energy(_Group):
    children = {"enabled": Enabled}


class Models(_Group):
    children = {"energy": Energy}


class Setup(_Group):
    children = {"models": Models}


class Intensity(_Value):
    default = 0.05
    attrs = {"min": lambda self: 0.0, "max": lambda self: 1.0}

    def validate(self, value):
        if not 0.0 <= value <= 1.0:
            raise RuntimeError("Value is not in range.")


SPECIFICATIONS = ["Intensity and Viscosity Ratio", "Intensity and Hydraulic Diameter"]


class Specification(_Value):
    objtype = "string/symbol"
    default = SPECIFICATIONS[0]
    attrs = {"allowed-values": lambda self: list(SPECIFICATIONS)}

    def validate(self, value):
        if value not in SPECIFICATIONS:
            raise RuntimeError(f"{value!r} is not an allowed value.")


class Temperature(_Value):
    default = 300.0

    def validate(self, value):
        if value > 5000:
            raise RuntimeError("Temperature is unphysical.")


def _energy_enabled(obj):
    return _root(obj).objs["setup"].objs["models"].objs["energy"].objs["enabled"].value


class Thermal(_Group):
    children = {"temperature": Temperature}
    attrs = {"active?": _energy_enabled}


class Inlet(_Group):
    children = {
        "intensity": Intensity,
        "specification": Specification,
        "thermal": Thermal,
    }


class BoundaryConditions(_Group):
    children = {"inlet": Inlet}


class WriteCase(_Command):
    arguments = {"file-name": "string"}

    def run(self, **kwds):
        root = _root(self.parent)
        Path(kwds["file-name"]).write_text(json.dumps(root.get_state()))


class ReadCase(_Command):
    arguments = {"file-name": "string"}

    def run(self, **kwds):
        root = _root(self.parent)
        root.set_state(json.loads(Path(kwds["file-name"]).read_text()))


class File(_Group):
    commands = {"write-case": WriteCase, "read-case": ReadCase}


class Iterate(_Command):
    arguments = {"iter-count": "integer"}

    def run(self, **kwds):
        root = _root(self.parent)
        root.iterations += kwds.get("iter-count", 1)
        inlet = root.objs["bc"].objs["inlet"]
        inlet.objs["intensity"].value = 0.9
        if root.diverge:
            raise RuntimeError("Divergence detected in AMG solver.")


class Root(_Group):
    children = {"setup": Setup, "bc": BoundaryConditions, "file": File}
    commands = {"iterate": Iterate}

    def __init__(self, parent=None):
        super().__init__(parent)
        self.iterations = 0
        self.diverge = False

    def get_state(self):
        state = super().get_state()
        state.pop("file", None)
        return state

    def set_state(self, value):
        super().set_state({k: v for k, v in value.items() if k != "file"})


class ModelService:
    """Server-side settings service of the model."""

    def __init__(self):
        self.root = Root()
        self.dead = False

    def __getattribute__(self, name):
        attribute = object.__getattribute__(self, name)
        if name.startswith("_") or not object.__getattribute__(self, "dead"):
            return attribute

        def unavailable(*args, **kwargs):
            raise ConnectionError("failed to connect to all addresses")

        return unavailable if callable(attribute) else attribute

    def _obj(self, path):
        obj = self.root
        for name in (p for p in path.split("/") if p):
            try:
                obj = obj.get_child(name)
            except KeyError:
                obj = obj.get_command(name)
        return obj

    def get_var(self, path):
        return self._obj(path).get_state()

    def set_var(self, path, value):
        self._obj(path).set_state(value)

    def execute_cmd(self, path, command, **kwds):
        return self._obj(path).get_command(command)(**kwds)

    def get_attrs(self, path, attrs, recursive=False):
        return self._obj(path).get_attrs(attrs)

    def get_static_info(self):
        return Root.get_static_info()

    def is_interactive_mode(self):
        return False

    def has_wildcard(self, name):
        return False


class ModelSession:
    """A session whose ``settings`` is a real ``flobject`` root."""

    def __init__(self):
        self.service = ModelService()
        self._settings_service = self.service
        self._settings = None
        self.error_state = FakeErrorState()
        self.serving = True
        self.exit_callbacks = []

    @property
    def settings(self):
        if self._settings is None:
            self._settings = flobject.get_root(self._settings_service, version="261")
        return self._settings

    @property
    def server(self):
        return self.service.root

    def crash(self):
        """Mimic a server process that died."""
        self.serving = False
        self.service.dead = True


class ModelAdapter(ResilientAdapter):
    """Adapter for :class:`ModelSession`."""

    product_name = "Model"
    scheme_name_attr = "fluent_name"
    irreversible_commands = frozenset({"iterate", "read_case"})
    interruptible_commands = frozenset({"iterate"})
    non_replayable_prefixes = ("write",)
    checkpoint_suffix = ".json"

    def invalidate_settings_cache(self, session):
        session._settings = None

    def is_fatal(self, session):
        return session.error_state.name == "fatal"

    def is_server_healthy(self, session):
        return session.serving

    def write_checkpoint(self, session, file_path, *, include_data):
        self.settings_root(session).file.write_case(file_name=file_path)
        return False

    def read_checkpoint(self, session, file_path, *, include_data):
        self.settings_root(session).file.read_case(file_name=file_path)

    def activation_candidates(self, session):
        return (ActivationCandidate("setup.models.energy.enabled", True),)
