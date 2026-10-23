# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
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

"""Lightweight fakes mimicking the settings-object protocol.

These let the resilient runtime be unit-tested with no live Fluent session. They
implement exactly the surface the runtime relies on: ``get_state`` /
``set_state`` / ``is_active`` / ``is_read_only`` / ``allowed_values`` / ``min`` /
``max``, named-object indexing, group attribute access, and a ``file`` command
group recording ``write_case_data`` / ``read_case_data`` calls.
"""

from __future__ import annotations


class FakeErrorState:
    """Mimics ``connectivity.fluent_connection.ErrorState``."""

    def __init__(self, name: str = "", details: str = ""):
        self._name = name
        self._details = details

    @property
    def name(self):
        return self._name

    @property
    def details(self):
        return self._details

    def set(self, name, details=""):
        self._name = name
        self._details = details

    def clear(self):
        self._name = ""
        self._details = ""


class FakeConnection:
    def __init__(self, error_state: FakeErrorState):
        self._error_state = error_state


class FakeLeaf:
    """A settable leaf that mimics a settings parameter."""

    def __init__(
        self,
        value=None,
        allowed=None,
        active=True,
        read_only=False,
        minimum=None,
        maximum=None,
        set_raises=None,
    ):
        self._value = value
        self._allowed = allowed
        self._active = active
        self._read_only = read_only
        self._min = minimum
        self._max = maximum
        #: Optional callable(value) -> raises or returns None, to simulate a
        #: Fluent-side rejection (e.g. out-of-range).
        self._set_raises = set_raises

    def get_state(self):
        return self._value

    def set_state(self, value):
        if self._set_raises is not None:
            self._set_raises(value)
        self._value = value

    def is_active(self):
        return self._active

    def is_read_only(self):
        return self._read_only

    def allowed_values(self):
        return list(self._allowed) if self._allowed is not None else None

    def min(self):
        return self._min

    def max(self):
        return self._max


class FakeGroup:
    """A group whose children are attributes."""

    def __init__(self, **children):
        self.__dict__.update(children)

    def get_state(self):
        return {
            name: child.get_state()
            for name, child in self.__dict__.items()
            if hasattr(child, "get_state")
        }

    def set_state(self, state):
        for name, value in (state or {}).items():
            child = getattr(self, name, None)
            if child is not None and hasattr(child, "set_state"):
                child.set_state(value)


class FakeNamedObject:
    """A named-object collection addressable by key."""

    def __init__(self, **instances):
        self._instances = dict(instances)

    def __getitem__(self, key):
        return self._instances[key]

    def get_object_names(self):
        return list(self._instances)

    def get_state(self):
        return {k: v.get_state() for k, v in self._instances.items()}

    def set_state(self, state):
        for key, value in (state or {}).items():
            if key in self._instances:
                self._instances[key].set_state(value)


class FakeCommand:
    """A callable command that records its invocations."""

    def __init__(self, result=None, raises=None, log=None, name=""):
        self._result = result
        self._raises = raises
        self._log = log if log is not None else []
        self._name = name

    def __call__(self, **kwargs):
        self._log.append((self._name, kwargs))
        if self._raises is not None:
            raise self._raises
        return self._result


class FakeFileGroup:
    """Mimics ``settings.file`` with case/data checkpoint commands.

    Writes real (non-empty) placeholder files on disk -- including the ``.dat.h5``
    companion for a case+data write -- so that the file-checkpoint pre-flight
    checks (which verify an artifact exists and is non-empty before a read) see a
    realistic artifact, just as a real Fluent write would produce.
    """

    def __init__(self):
        self.calls = []

    @staticmethod
    def _touch(file_name, *, with_data_companion):
        try:
            with open(file_name, "wb") as handle:
                handle.write(b"fake-case")
            if with_data_companion and str(file_name).endswith(".cas.h5"):
                companion = str(file_name)[: -len(".cas.h5")] + ".dat.h5"
                with open(companion, "wb") as handle:
                    handle.write(b"fake-data")
        except OSError:
            # Some tests point at non-existent directories on purpose.
            pass

    def write_case_data(self, file_name):
        self.calls.append(("write_case_data", file_name))
        self._touch(file_name, with_data_companion=True)

    def write_case(self, file_name):
        self.calls.append(("write_case", file_name))
        self._touch(file_name, with_data_companion=False)

    def read_case_data(self, file_name):
        self.calls.append(("read_case_data", file_name))

    def read_case(self, file_name):
        self.calls.append(("read_case", file_name))


class FakeEvents:
    """Mimics ``session.events`` callback registration."""

    def __init__(self):
        self._callbacks = {}
        self._next = 0

    def register_callback(self, event_types, callback, *args, **kwargs):
        cb_id = f"cb-{self._next}"
        self._next += 1
        self._callbacks[cb_id] = (event_types, callback)
        return cb_id

    def unregister_callback(self, callback_id):
        self._callbacks.pop(callback_id, None)

    def fire(self, event_info=None):
        for _event_types, callback in list(self._callbacks.values()):
            callback(self, event_info)


class FakeSettings(FakeGroup):
    """A settings root that also carries a ``file`` command group."""

    def __init__(self, file_group=None, **children):
        super().__init__(**children)
        self.file = file_group if file_group is not None else FakeFileGroup()


class FakeSettingsService:
    """Mimics ``services.settings.BaseSettings`` (set_var / execute_cmd / get_var).

    Operates on a live :class:`FakeSettings` tree so that an interceptor wrapped
    around it exercises the real resilient path. ``set_var`` / ``execute_cmd``
    resolve the dotted path to the fake object and call its protocol methods.
    """

    def __init__(self, settings):
        self.settings = settings
        self.calls = []

    def _resolve(self, path):
        from ansys.fluent.core.resilient import _compat

        return _compat.resolve(self.settings, path) if path else self.settings

    def set_var(self, path, value):
        self.calls.append(("set_var", path, value))
        self._resolve(path).set_state(value)

    def get_var(self, path):
        return self._resolve(path).get_state()

    def execute_cmd(self, path, command, **kwds):
        self.calls.append(("execute_cmd", path, command, kwds))
        parent = self._resolve(path)
        method = getattr(parent, command)
        return method(**kwds) if kwds else method()

    # A version-specific method to prove transparent delegation works.
    def is_wildcard(self, path):
        return False


class FakeSession:
    """A session exposing ``settings``, ``events`` and an error state."""

    def __init__(self, settings=None, error_state=None, serving=True):
        self.settings = settings if settings is not None else FakeSettings()
        self.events = FakeEvents()
        self._error_state = error_state or FakeErrorState()
        self._fluent_connection = FakeConnection(self._error_state)
        self._serving = serving
        self.exited = False
        # Settings-service plumbing so enable_resilient_mode can wrap it.
        self._settings_service = FakeSettingsService(self.settings)
        self._settings = self.settings

    def _is_server_healthy(self):
        return self._serving

    def go_fatal(self, details="boom"):
        self._error_state.set("fatal", details)

    def exit(self):
        self.exited = True
