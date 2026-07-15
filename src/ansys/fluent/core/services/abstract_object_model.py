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

"""Abstract object model wrapper."""

from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any

ValueT = None | bool | int | float | str | Sequence["ValueT"] | dict[str, "ValueT"]


class AbstractObjectModel(ABC):
    """Abstract base class for the object model."""

    @abstractmethod
    def get_attribute_value(self, rules: str, path: str, attribute: str) -> ValueT:
        """Get attribute value."""
        pass

    @abstractmethod
    def get_state(self, rules: str, path: str) -> ValueT:
        """Get state."""
        pass

    @abstractmethod
    def get_object_names(self, rules: str, path: str) -> list[str]:
        """Get object names."""
        pass

    @abstractmethod
    def create_object(self, rules: str, path: str, name: str) -> None:
        """Create an object."""
        pass

    @abstractmethod
    def rename(self, rules: str, path: str, new_name: str) -> None:
        """Rename an object."""
        pass

    @abstractmethod
    def delete_child_objects(
        self, rules: str, path: str, obj_type: str, child_names: list[str]
    ) -> None:
        """Delete child objects."""
        pass

    @abstractmethod
    def delete_all_child_objects(self, rules: str, path: str, obj_type: str) -> None:
        """Delete all child objects."""
        pass

    @abstractmethod
    def set_state(self, rules: str, path: str, state: ValueT) -> None:
        """Set state."""
        pass

    @abstractmethod
    def fix_state(self, rules: str, path: str) -> None:
        """Fix state."""
        pass

    @abstractmethod
    def update_dict(
        self,
        rules: str,
        path: str,
        dict_state: dict[str, ValueT],
        recursive=False,
    ) -> None:
        """Update the dict."""
        pass

    @abstractmethod
    def delete_object(self, rules: str, path: str) -> None:
        """Delete an object."""
        pass

    @abstractmethod
    def execute_command(
        self, rules: str, path: str, command: str, args: dict[str, ValueT]
    ) -> ValueT:
        """Execute the command."""
        pass

    @abstractmethod
    def execute_query(
        self, rules: str, path: str, query: str, args: dict[str, ValueT]
    ) -> ValueT:
        """Execute the query."""
        pass

    @abstractmethod
    def create_command_arguments(self, rules: str, path: str, command: str) -> str:
        """Create command arguments."""
        pass

    @abstractmethod
    def delete_command_arguments(
        self, rules: str, path: str, command: str, commandid: str
    ) -> None:
        """Delete command arguments."""
        pass

    @abstractmethod
    def register_command_arguments(
        self, rules: str, path: str, command: str, commandid: str
    ) -> None:
        """Register command arguments for explicit cleanup during shutdown."""
        pass

    @abstractmethod
    def release_command_arguments(
        self, rules: str, path: str, command: str, commandid: str
    ) -> None:
        """Release command arguments when their Python wrapper is deleted."""
        pass

    @abstractmethod
    def get_static_info(self, rules: str) -> dict[str, Any]:
        """Get static info."""
        pass
