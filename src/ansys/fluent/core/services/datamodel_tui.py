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

"""Wrappers over TUI-based datamodel gRPC service of Fluent.

This module contains the shared TUI runtime/menu logic reused by the v1
adapter module, which overrides only v1 proto/stub/request differences.
"""

import keyword
import logging
from typing import Any

from ansys.fluent.core.services.api_upgrade import ApiUpgradeAdvisor

Path = list[str]

logger: logging.Logger = logging.getLogger("pyfluent.tui")


class TextInterface:
    """Pure Python wrapper of text interface grpc service."""

    def __init__(
        self,
        service,
        application_runtime_service,
        scheme_interpreter_service,
    ) -> None:
        """__init__ method of DatamodelService class."""
        self.service = service
        self._app_utilities = application_runtime_service
        self._scheme_eval = scheme_interpreter_service

    def get_attribute_value(
        self, path: str, attribute: str, include_unavailable: bool
    ) -> Any:
        """Get attribute value at a path.

        Parameters
        ----------
        path : str
            Path to the menu.
        attribute : str
            Attribute name.
        include_unavailable : bool
            Whether to query over static TUI metadata.

        Returns
        -------
        Any
            Attribute value (any Python datatype)
        """
        return self.service.get_attribute_value(path, attribute, include_unavailable)

    def execute_command(self, path: str, *args, **kwargs) -> Any:
        """Execute a command at a path with positional or keyword arguments.

        Parameters
        ----------
        path : str
            Path to the menu.
        *args
            Positional arguments of the command.
        **kwargs
            Keyword arguments of the command.

        Returns
        -------
        Any
            Command result (any Python datatype)
        """
        return self.service.execute_command(path, *args, **kwargs)

    def execute_query(self, path: str, *args, **kwargs) -> Any:
        """Execute a query at a path with positional or keyword arguments.

        Parameters
        ----------
        path : str
            Path to the menu.
        *args
            Positional arguments of the query.
        **kwargs
            Keyword arguments of the query.

        Returns
        -------
        Any
            Query result (any Python datatype)
        """
        return self.service.execute_query(path, *args, **kwargs)

    def get_static_info(self, path: str):
        """Get static info at a path.

        Parameters
        ----------
        path : str
            Path to the menu.

        Returns
        -------
        dict[str, Any]
            Static info at the menu level.
        """
        return self.service.get_static_info(path)

    def get_child_names(
        self, path: str, include_unavailable: bool = False
    ) -> list[str]:
        """Get the names of child menus.

        Parameters
        ----------
        path : str
            Path to the menu.

        include_unavailable : bool, optional
            Whether to query over static TUI metadata. The default is ``False``.

        Returns
        -------
        List[str]
            Names of child menus.
        """
        return self.service.get_child_names(path, include_unavailable)

    def get_doc_string(self, path: str, include_unavailable: bool = False) -> str:
        """Get docstring for a menu.

        Parameters
        ----------
        path : str
            Path to the menu.

        include_unavailable : bool, optional
            Whether to query over static TUI metadata. The default is ``False``.

        Returns
        -------
        str
        """
        return self.service.get_doc_string(path, include_unavailable)


class PyMenu:
    """Pythonic wrapper of TUI-based DatamodelService class. Use this class instead of
    directly calling the DatamodelService's method.

    Methods
    -------
    get_child_names(include_unavailable):
        Get child menu names.
    execute(*args, **kwargs)
        Execute a command or query at a menu with positional or keyword
        arguments.
    get_doc_string(include_unavailable)
        Get docstring for a menu.
    """

    def __init__(self, service, version, mode, path: Path | str) -> None:
        """__init__ method of PyMenu class."""
        self._service = service
        self._version = version
        self._mode = mode
        self._path = path if isinstance(path, str) else convert_path_to_grpc_path(path)

    def get_child_names(self, include_unavailable: bool = False) -> list[str]:
        """Get the names of child menus.

        Parameters
        ----------
        include_unavailable : bool, optional
            Whether to query over static TUI metadata. The default is ``False``.

        Returns
        -------
        List[str]
            Names of child menus.
        """
        return self._service.get_child_names(self._path, include_unavailable)

    def execute(self, *args, **kwargs) -> Any:
        """Execute a command or query at a path with positional or keyword arguments.

        Parameters
        ----------
        *args
            Positional arguments of the command or qyery.
        **kwargs
            Keyword arguments of the command or query.

        Returns
        -------
        Any
            Query result (any Python datatype)
        """
        with ApiUpgradeAdvisor(
            self._service._app_utilities,
            self._version,
            self._mode,
        ):
            if self._path.startswith("/query/"):
                return self._service.execute_query(self._path, *args, **kwargs)
            else:
                return self._service.execute_command(self._path, *args, **kwargs)

    def get_doc_string(self, include_unavailable: bool = False) -> str:
        """Get docstring for a menu.

        Parameters
        ----------
        include_unavailable : bool, optional
            Whether to query over static TUI metadata. The default is ``False``.

        Returns
        -------
        str
        """
        return self._service.get_doc_string(self._path, include_unavailable)

    def get_static_info(self) -> dict[str, Any]:
        """Get static info at menu level.

        Returns
        -------
        DataModelProtoModule.StaticInfo
            static info
        """
        try:
            return self._service.get_static_info(self._path)
        except RuntimeError:
            return _get_static_info_at_level(self)


def _get_static_info_at_level(menu: PyMenu) -> dict[str, Any]:
    info = {}
    info["help"] = menu.get_doc_string(include_unavailable=True)
    info["menus"] = {}
    info["commands"] = {}
    child_names = menu.get_child_names(include_unavailable=True)
    if child_names:
        for child_name in child_names:
            if child_name:
                child_menu = PyMenu(
                    menu._service,
                    menu._version,
                    menu._mode,
                    menu._path + ("" if menu._path.endswith("/") else "/") + child_name,
                )
                child_info = _get_static_info_at_level(child_menu)
                if child_info.pop("is_command", False):
                    info["commands"][child_name] = child_info
                else:
                    info["menus"][child_name] = child_info
    else:
        info["is_command"] = True
    return info


class TUIMethod:
    """Base class for the generated menu methods.

    Methods like ___repr__ are inserted at PyConsole side.
    """

    def __init__(self, service, version, mode, path):
        """Initialize TUIMethod."""
        self._service = service
        self._version = version
        self._mode = mode
        self._path = path

    def __call__(self, *args, **kwargs):
        return PyMenu(self._service, self._version, self._mode, self._path).execute(
            *args, **kwargs
        )


class TUIMenu:
    """Base class for the generated menu classes."""

    def __init__(self, service, version, mode, path) -> None:
        """__init__ method of TUIMenu class."""
        self._service = service
        self._version = version
        self._mode = mode
        self._path = path

    def __dir__(self) -> list[str]:
        return [
            convert_tui_menu_to_func_name(x)
            for x in PyMenu(
                self._service, self._version, self._mode, self._path
            ).get_child_names()
            if x not in ["exit", "switch_to_meshing_mode"]
        ]

    def __getattribute__(self, name) -> Any:
        if name in ["exit"] and not self._path:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
            )
        try:
            attr = super().__getattribute__(name)
            if isinstance(attr, TUIMethod):
                # some runtime submenus are generated as methods during codegen
                path = self._path + [name]
                if PyMenu(
                    self._service, self._version, self._mode, path
                ).get_child_names():
                    return TUIMenu(self._service, self._version, self._mode, path)
            return attr
        except AttributeError as ex:
            if name in dir(self):
                # for runtime submenus and commands which are not available during codegen
                path = self._path + [name]
                if PyMenu(
                    self._service, self._version, self._mode, path
                ).get_child_names():
                    return TUIMenu(self._service, self._version, self._mode, path)
                else:
                    return TUICommand(self._service, self._version, self._mode, path)
            else:
                raise ex


class TUICommand(TUIMenu):
    """Generic command class for when the explicit menu classes aren't available."""

    def __call__(self, *args, **kwargs) -> Any:
        return PyMenu(self._service, self._version, self._mode, self._path).execute(
            *args, **kwargs
        )


def convert_tui_menu_to_func_name(menu: str) -> str:
    """Convert a TUI menu string to a Python function name.

    Parameters
    ----------
    menu : str
       TUI menu string.

    Returns
    -------
    str
    """
    if keyword.iskeyword(menu):
        return menu + "_"
    if menu.endswith("[beta]"):
        menu = menu[:-6]
    menu = menu.rstrip("?")
    return menu


def convert_path_to_grpc_path(path: Path) -> str:
    """Convert a path structure to a string that can be passed to the data model gRPC
    service.

    Parameters
    ----------
    path : Path
        Path structure.

    Returns
    -------
    str
        gRPC path.
    """
    return "/" + "/".join(x for x in path)
