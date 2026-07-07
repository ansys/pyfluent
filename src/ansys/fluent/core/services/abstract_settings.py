# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
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

"""Abstract settings wrapper."""

from abc import ABC, abstractmethod
from typing import Any


class AbstractSettings(ABC):
    """Abstract base class for accessing and modifying Fluent settings."""

    @abstractmethod
    def set_var(self, path: str, value: Any) -> None:
        """Set the value for the given path."""
        pass

    @abstractmethod
    def get_var(self, path: str) -> Any:
        """Get the value for the given path."""
        pass

    @abstractmethod
    def rename(self, path: str, new: str, old: str) -> None:
        """Rename the object at the given path."""
        pass

    @abstractmethod
    def create(self, path: str, name: str) -> None:
        """Create a named object child for the given path."""
        pass

    @abstractmethod
    def delete(self, path: str, name: str) -> None:
        """Delete the object with the given name at the given path."""
        pass

    @abstractmethod
    def get_object_names(self, path: str) -> list[str]:
        """Get a list of named objects."""
        pass

    @abstractmethod
    def get_list_size(self, path: str) -> int:
        """Get the number of elements in a list object."""
        pass

    @abstractmethod
    def resize_list_object(self, path: str, size: int) -> None:
        """Resize a list object."""
        pass

    @abstractmethod
    def get_static_info(self) -> dict[str, Any]:
        """Get static-info for settings.

        Raises
        ------
        RuntimeError
            If type is empty.
        """
        pass

    @abstractmethod
    def execute_cmd(self, path: str, command: str, **kwds) -> Any:
        """Execute a given command with the provided keyword arguments."""
        pass

    @abstractmethod
    def execute_query(self, path: str, query: str, **kwds) -> Any:
        """Execute a given query with the provided keyword arguments."""
        pass

    @abstractmethod
    def get_attrs(self, path: str, attrs: list[str], recursive: bool = False) -> Any:
        """Return values of given attributes."""
        pass

    @abstractmethod
    def is_interactive_mode(self) -> bool:
        """Checks whether commands can be executed interactively."""
        pass

    @abstractmethod
    def is_wildcard(self, input: str | None = None) -> bool:
        """Check whether a name contains a wildcard pattern (v1: Settings.IsWildcard)."""
        pass

    @abstractmethod
    def has_wildcard(self, name: str) -> bool:
        """Check whether a name has a wildcard pattern (v1: uses Settings.IsWildcard directly)."""
        pass
