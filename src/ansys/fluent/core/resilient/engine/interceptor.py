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
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .controller import ResilientController


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
        """Set a value with journaling and failover."""
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
