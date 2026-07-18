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

"""Abstract text interface wrapper."""

from abc import ABC, abstractmethod
from typing import Any


class AbstractTextInterface(ABC):
    """Abstract base class for the text interface."""

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass
