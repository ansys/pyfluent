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

"""Interception of the settings service.

Every settings write and command of a product's settings tree goes through its
settings service (``set_var``, ``execute_cmd``, ``create``, ...).
:class:`ResilientSettingsService` wraps that service and routes the
state-changing calls through the :class:`ResilientController`. Every other call
(reads and queries) is delegated to the product service; if it fails because
the server died, the controller fails over and repeats the read.

The settings tree can also ask its service how to handle navigation into an
*inactive* object (``on_inactive_access``). When model activation is allowed,
the controller returns an :class:`InactiveTargetProxy`: activation is deferred
until something is *written* through the proxy, so reading never changes solver
state.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from .controller import ResilientController

#: Attribute names that read an inactive object. Accessing them through a proxy
#: raises the product's original inactive-object error.
_READ_ATTRIBUTES = frozenset(
    {
        "allowed_values",
        "as_quantity",
        "child_names",
        "command_names",
        "default_value",
        "get_attr",
        "get_attrs",
        "get_object_names",
        "get_state",
        "is_active",
        "is_read_only",
        "max",
        "min",
        "print_state",
        "query_names",
        "units",
    }
)


class ResilientSettingsService:
    """Resilience-enabled proxy of a product settings service.

    Parameters
    ----------
    inner :
        The product settings service.
    controller : ResilientController
        The controller that owns the resilient state of the session.
    """

    _OWN_ATTRIBUTES = frozenset({"_inner", "_controller"})

    def __init__(self, inner: Any, controller: ResilientController):
        object.__setattr__(self, "_inner", inner)
        object.__setattr__(self, "_controller", controller)

    @property
    def inner(self) -> Any:
        """Return the wrapped product settings service."""
        return self._inner

    def rebind_inner(self, inner: Any) -> None:
        """Wrap a different product settings service (after a failover)."""
        object.__setattr__(self, "_inner", inner)

    # -- state-changing calls ----------------------------------------------------

    def set_var(self, path: str, value: Any) -> None:
        """Set a value with recovery, journaling and failover."""
        self._controller.apply_set(path, value)

    def execute_cmd(self, path: str, command: str, **kwds: Any) -> Any:
        """Execute a command with checkpointing, rollback, journaling and failover."""
        return self._controller.apply_command(path, command, kwds)

    def create(self, path: str, name: str) -> None:
        """Create a named object (journaled)."""
        self._controller.apply_object_change("create", path, (name,))

    def delete(self, path: str, name: str) -> None:
        """Delete a named object (journaled)."""
        self._controller.apply_object_change("delete", path, (name,))

    def rename(self, path: str, new: str, old: str) -> None:
        """Rename a named object (journaled)."""
        self._controller.apply_object_change("rename", path, (new, old))

    def resize_list_object(self, path: str, size: int) -> None:
        """Resize a list object (journaled)."""
        self._controller.apply_object_change("resize_list_object", path, (size,))

    # -- settings-tree hook ------------------------------------------------------

    def on_inactive_access(self, obj: Any, name: str) -> Any:
        """Return a stand-in for child ``name`` of the inactive object ``obj``.

        Returns ``None`` to let the settings tree raise its usual error.
        """
        return self._controller.on_inactive_access(obj, name)

    # -- transparent delegation ----------------------------------------------------

    def __getattr__(self, name: str) -> Any:
        attribute = getattr(object.__getattribute__(self, "_inner"), name)
        if name.startswith("_") or not callable(attribute):
            return attribute
        controller = object.__getattribute__(self, "_controller")

        def query(*args: Any, **kwargs: Any) -> Any:
            return controller.apply_query(name, args, kwargs)

        query.__name__ = name
        query.__doc__ = getattr(attribute, "__doc__", None)
        return query

    def __setattr__(self, name: str, value: Any) -> None:
        if name in self._OWN_ATTRIBUTES:
            object.__setattr__(self, name, value)
        else:
            setattr(self._inner, name, value)

    def __repr__(self) -> str:
        return f"<ResilientSettingsService wrapping {self._inner!r}>"


class InactiveTargetProxy:
    """Stand-in for a settings object below an inactive object.

    Navigation through the proxy (attributes, ``[key]``) only records the path.
    The first *write* through it -- assigning an attribute or item, calling
    ``set_state``, or calling the object with arguments -- asks the controller to
    activate the inactive object, then performs the write on the real object.
    Reading through the proxy reads the real object, which raises the product's
    inactive-object error while the object is inactive. Reads therefore never
    change solver state.
    """

    __slots__ = ("_controller", "_inactive", "_chain", "_failed")

    def __init__(
        self,
        controller: ResilientController,
        inactive: Any,
        chain: tuple[tuple[str, Any], ...],
    ):
        object.__setattr__(self, "_controller", controller)
        object.__setattr__(self, "_inactive", inactive)
        object.__setattr__(self, "_chain", chain)
        object.__setattr__(self, "_failed", False)

    def _extend(self, kind: str, key: Any) -> InactiveTargetProxy:
        return InactiveTargetProxy(
            self._controller, self._inactive, self._chain + ((kind, key),)
        )

    def _real(self) -> Any:
        """Return the real object, or raise the product's inactive-object error."""
        return self._controller.navigate(self._inactive, self._chain)

    def _write(self, action: Callable[[Any], Any]) -> Any:
        try:
            return self._controller.write_inactive(self._inactive, self._chain, action)
        except Exception:
            # Settings code that handles the failure (for example a check for
            # ``allowed_values``) must see the original error, not a new
            # inactive-object error raised by introspecting this proxy.
            object.__setattr__(self, "_failed", True)
            raise

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            raise AttributeError(name)
        if name in _READ_ATTRIBUTES:
            if self._failed:
                raise AttributeError(name)
            return getattr(self._real(), name)
        if name == "set_state":
            return lambda *args, **kwargs: self._write(
                lambda target: target.set_state(*args, **kwargs)
            )
        return self._extend("attr", name)

    def __getitem__(self, key: Any) -> InactiveTargetProxy:
        return self._extend("item", key)

    def __setattr__(self, name: str, value: Any) -> None:
        self._write(lambda target: setattr(target, name, value))

    def __setitem__(self, key: Any, value: Any) -> None:
        self._write(lambda target: target.__setitem__(key, value))

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if not args and not kwargs:
            # Calling a settings object without arguments reads its state.
            return self._real()()
        return self._write(lambda target: target(*args, **kwargs))

    def __repr__(self) -> str:
        location = getattr(self._inactive, "python_path", None) or repr(self._inactive)
        below = ".".join(str(key) for _, key in self._chain)
        return f"<inactive settings object {location}.{below}>"
