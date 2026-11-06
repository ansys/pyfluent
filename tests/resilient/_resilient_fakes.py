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

"""Product-free fakes for unit testing the resilient engine.

The fake session exposes a settings tree and a settings service that resolves
dotted paths on that tree. Writes made through the service are what the engine
intercepts, so tests drive the engine with ``session._settings_service`` calls.
"""

from __future__ import annotations

import json
from pathlib import Path

from ansys.fluent.core.resilient.engine import (
    ActivationCandidate,
    ResilientAdapter,
    paths,
)


class FakeLeaf:
    """A settings value with optional bounds, allowed values and activity."""

    def __init__(
        self,
        value=None,
        *,
        allowed=None,
        minimum=None,
        maximum=None,
        active=True,
        reject=None,
    ):
        self.value = value
        self.allowed = allowed
        self.minimum = minimum
        self.maximum = maximum
        self.active = active
        #: Optional callable(value) that raises to mimic a server rejection.
        self.reject = reject

    def get_state(self):
        return self.value

    def set_state(self, value):
        if callable(self.active):
            active = self.active()
        else:
            active = self.active
        if not active:
            raise RuntimeError("The object is not allowed to be set.")
        if self.reject is not None:
            self.reject(value)
        self.value = value

    def is_active(self):
        return self.active() if callable(self.active) else self.active

    def allowed_values(self):
        return list(self.allowed) if self.allowed is not None else None

    def min(self):
        return self.minimum

    def max(self):
        return self.maximum


class FakeGroup:
    """A group of named children."""

    def __init__(self, **children):
        self.__dict__.update(children)

    def _children(self):
        return {
            name: child
            for name, child in vars(self).items()
            if hasattr(child, "get_state") and not name.startswith("_")
        }

    @staticmethod
    def _active(child):
        is_active = getattr(child, "is_active", None)
        return is_active() if callable(is_active) else True

    def get_state(self):
        return {
            name: child.get_state()
            for name, child in self._children().items()
            if self._active(child)
        }

    def set_state(self, state):
        for name, value in (state or {}).items():
            child = getattr(self, name)
            if self._active(child):
                child.set_state(value)


class FakeFileGroup:
    """``settings.file``: writes and reads the settings state as JSON."""

    def __init__(self, root):
        self._root = root
        self.writes = []
        self.reads = []

    def write(self, file_name):
        self.writes.append(file_name)
        Path(file_name).write_text(json.dumps(self._root.get_state()))

    def read(self, file_name):
        self.reads.append(file_name)
        self._root.set_state(json.loads(Path(file_name).read_text()))


class FakeSettings(FakeGroup):
    """A settings root with a ``file`` group and any number of commands."""

    def __init__(self, **children):
        super().__init__(**children)
        self._file = FakeFileGroup(self)
        self.commands = {}

    @property
    def file(self):
        return self._file

    def __getattr__(self, name):
        commands = self.__dict__.get("commands", {})
        if name in commands:
            return commands[name]
        raise AttributeError(name)


class FakeSettingsService:
    """A settings service over a :class:`FakeSettings` tree (dotted paths)."""

    def __init__(self, settings):
        self.settings = settings
        self.dead = False
        self.calls = []

    def _check(self):
        if self.dead:
            raise ConnectionError("failed to connect to all addresses; Socket closed")

    def _resolve(self, path):
        return paths.resolve(self.settings, path) if path else self.settings

    def set_var(self, path, value):
        self._check()
        self.calls.append(("set_var", path, value))
        self._resolve(path).set_state(value)

    def get_var(self, path):
        self._check()
        return self._resolve(path).get_state()

    def get_attrs(self, path, attrs, recursive=False):
        self._check()
        self._resolve(path)
        return {"attrs": dict.fromkeys(attrs, True)}

    def execute_cmd(self, path, command, **kwds):
        self._check()
        self.calls.append(("execute_cmd", path, command, kwds))
        return getattr(self._resolve(path), command)(**kwds)

    def create(self, path, name):
        self._check()
        self.calls.append(("create", path, name))
        setattr(self._resolve(path), name, FakeLeaf(None))

    def get_static_info(self):
        return {}


class FakeErrorState:
    """Mimics a product connection's error state."""

    def __init__(self):
        self.name = ""
        self.details = ""

    def set(self, name, details=""):
        self.name = name
        self.details = details


def default_tree():
    """Return a settings tree used by most tests."""
    energy = FakeLeaf(False)
    return FakeSettings(
        setup=FakeGroup(
            energy=energy,
            intensity=FakeLeaf(
                0.05,
                minimum=0.0,
                maximum=1.0,
                reject=_reject_out_of_range(0.0, 1.0),
            ),
            model=FakeLeaf(
                "k-epsilon",
                allowed=["laminar", "k-epsilon", "k-omega"],
                reject=_reject_disallowed(["laminar", "k-epsilon", "k-omega"]),
            ),
            temperature=FakeLeaf(300.0, active=lambda: energy.value is True),
            radiation=FakeLeaf(False),
        ),
    )


def _reject_out_of_range(low, high):
    def reject(value):
        if isinstance(value, (int, float)) and not low <= value <= high:
            raise RuntimeError("Value is not in range.")

    return reject


def _reject_disallowed(allowed):
    def reject(value):
        if value not in allowed:
            raise RuntimeError(f"{value!r} is not an allowed value.")

    return reject


class FakeSession:
    """A product-like session."""

    def __init__(self, settings=None):
        self.settings = settings if settings is not None else default_tree()
        self._settings_service = FakeSettingsService(self.settings)
        self.error_state = FakeErrorState()
        self.serving = True
        self.exited = False
        self.exit_callbacks = []
        self.cache_invalidations = 0
        self.has_case = True

    def exit(self):
        if self.exited:
            return
        self.exited = True
        for callback in list(self.exit_callbacks):
            callback()

    def crash(self):
        """Mimic a server process that died."""
        self.serving = False
        self._service().dead = True

    def _service(self):
        service = self._settings_service
        return getattr(service, "inner", service)


class FakeAdapter(ResilientAdapter):
    """Adapter for :class:`FakeSession`."""

    product_name = "Fake"
    path_prefixes = ("settings.",)
    irreversible_commands = frozenset({"iterate", "read_case"})
    interruptible_commands = frozenset({"iterate"})
    non_replayable_prefixes = ("write",)
    checkpoint_suffix = ".json"

    def __init__(self, factory=None, candidates=()):
        self.factory = factory
        self.candidates = tuple(candidates)
        self.launched = []

    def invalidate_settings_cache(self, session):
        session.cache_invalidations += 1

    def is_fatal(self, session):
        return session.error_state.name == "fatal"

    def fatal_details(self, session):
        return session.error_state.details or None

    def is_server_healthy(self, session):
        return session.serving

    def launch(self, **kwargs):
        session = self.factory(**kwargs)
        self.launched.append(session)
        return session

    def standby_launcher(self, session):
        if self.factory is None:
            return None
        return lambda: self.launch()

    def register_exit_callback(self, session, callback):
        session.exit_callbacks.append(callback)
        return True

    def can_checkpoint(self, session):
        return session.has_case

    def write_checkpoint(self, session, file_path, *, include_data):
        session.settings.file.write(file_path)
        return False

    def read_checkpoint(self, session, file_path, *, include_data):
        session.settings.file.read(file_path)

    def activation_candidates(self, session):
        return tuple(
            ActivationCandidate(path, value) for path, value in self.candidates
        )


def service_of(session):
    """Return the product (unwrapped) settings service of a fake session."""
    service = session._settings_service
    return getattr(service, "inner", service)
