# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
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

"""Formal ``typing.Protocol`` for the settings proxy (flproxy) contract.

The 14 methods listed here are the complete duck-typed interface that
:func:`~ansys.fluent.core.solver.flobject.get_root` and the settings tree
objects call on the *flproxy* they receive.  Both
:class:`~ansys.fluent.core.services.settings.SettingsService` (gRPC) and
:class:`~ansys.fluent.core.rest.client.FluentRestClient` (REST) satisfy this
protocol.

This module introduces **no** runtime behaviour — it exists purely for static
type-checking and documentation.
"""

from typing import Any, Protocol, runtime_checkable

__all__ = ["SettingsProxy"]


@runtime_checkable
class SettingsProxy(Protocol):
    """Protocol formalising the *flproxy* contract consumed by ``flobject``.

    Any object whose public methods match the signatures below can be passed as
    the *flproxy* argument to
    :func:`~ansys.fluent.core.solver.flobject.get_root`.

    The 14 methods are grouped into four categories:

    **Introspection**
        ``get_static_info``, ``get_attrs``, ``has_wildcard``,
        ``is_interactive_mode``

    **Value access**
        ``get_var``, ``set_var``

    **Named-object / list-object management**
        ``get_object_names``, ``create``, ``delete``, ``rename``,
        ``get_list_size``, ``resize_list_object``

    **Command / query execution**
        ``execute_cmd``, ``execute_query``
    """

    # -- Introspection ---------------------------------------------------

    def get_static_info(self) -> dict[str, Any]:
        """Return the full static-info tree for all solver settings.

        Returns
        -------
        dict[str, Any]
            Nested dict with keys such as ``type``, ``children``,
            ``commands``, ``queries``, ``object-type``, ``allowed-values``,
            etc.
        """
        ...

    def get_attrs(self, path: str, attrs: list[str], recursive: bool = False) -> Any:
        """Return the requested attributes for the setting at *path*.

        Parameters
        ----------
        path : str
            Slash-delimited settings path.
        attrs : list[str]
            Attribute names to retrieve, e.g.
            ``["allowed-values", "active?"]``.
        recursive : bool, optional
            When ``True``, also return attributes for all descendants.

        Returns
        -------
        Any
            Attribute values.  Shape depends on *recursive*.
        """
        ...

    def has_wildcard(self, name: str) -> bool:
        """Return ``True`` if *name* contains an ``fnmatch``-style wildcard.

        Parameters
        ----------
        name : str
            Object name to check.
        """
        ...

    def is_interactive_mode(self) -> bool:
        """Return whether commands can be executed interactively."""
        ...

    # -- Value access ----------------------------------------------------

    def get_var(self, path: str) -> Any:
        """Return the current value of the setting at *path*.

        Parameters
        ----------
        path : str
            Slash-delimited settings path.
        """
        ...

    def set_var(self, path: str, value: Any) -> None:
        """Set the value of the setting at *path*.

        Parameters
        ----------
        path : str
            Slash-delimited settings path.
        value : Any
            New value (bool, int, float, str, list, dict, or ``None``).
        """
        ...

    # -- Named-object / list-object management ---------------------------

    def get_object_names(self, path: str) -> list[str]:
        """Return the child named-object names at *path*.

        Parameters
        ----------
        path : str
            Slash-delimited settings path of a named-object container.
        """
        ...

    def create(self, path: str, name: str) -> None:
        """Create a named child object at *path*.

        Parameters
        ----------
        path : str
            Slash-delimited settings path.
        name : str
            Name of the new child.
        """
        ...

    def delete(self, path: str, name: str) -> None:
        """Delete the named child object at *path*.

        Parameters
        ----------
        path : str
            Slash-delimited settings path.
        name : str
            Name of the child to delete.
        """
        ...

    def rename(self, path: str, new: str, old: str) -> None:
        """Rename a child object at *path* from *old* to *new*.

        Parameters
        ----------
        path : str
            Slash-delimited settings path.
        new : str
            New name.
        old : str
            Current name.
        """
        ...

    def get_list_size(self, path: str) -> int:
        """Return the number of elements in the list-object at *path*.

        Parameters
        ----------
        path : str
            Slash-delimited settings path of a list-object.
        """
        ...

    def resize_list_object(self, path: str, size: int) -> None:
        """Resize the list-object at *path*.

        Parameters
        ----------
        path : str
            Slash-delimited settings path of a list-object.
        size : int
            New number of elements.
        """
        ...

    # -- Command / query execution ---------------------------------------

    def execute_cmd(self, path: str, command: str, **kwds: Any) -> Any:
        """Execute *command* at *path* with keyword arguments.

        Parameters
        ----------
        path : str
            Slash-delimited settings path.
        command : str
            Command name.
        **kwds
            Keyword arguments forwarded to the command.
        """
        ...

    def execute_query(self, path: str, query: str, **kwds: Any) -> Any:
        """Execute *query* at *path* with keyword arguments.

        Parameters
        ----------
        path : str
            Slash-delimited settings path.
        query : str
            Query name.
        **kwds
            Keyword arguments forwarded to the query.
        """
        ...
