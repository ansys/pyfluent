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

"""Wrapper to settings gRPC service of Fluent."""

from functools import wraps
from typing import Any

from ansys.fluent.core.services.abstract_setting import AbstractSettings

trace: bool = False
_indent: int = 0


def _trace(fn):
    @wraps(fn)
    def _fn(self, *args, **kwds):
        global _indent
        if trace:
            print(f"{' ' * _indent}fn={fn.__name__}, args={args} {{")
            try:
                _indent += 1
                ret = fn(self, *args, **kwds)
            finally:
                _indent -= 1
            print(f"{' ' * _indent}fn = {fn.__name__}, ret={ret} }}")
            return ret
        else:
            return fn(self, *args, **kwds)

    return _fn


class SettingsV261(AbstractSettings):
    """Service for accessing and modifying Fluent settings before Fluent 27R1."""

    def __init__(
        self, service, application_runtime_service, scheme_interpreter_service
    ) -> None:
        """__init__ method of SettingsV261 class."""
        self.service = service
        self._application_runtime_service = application_runtime_service
        self._scheme_interpreter_service = scheme_interpreter_service

    @_trace
    def set_var(self, path: str, value: Any) -> None:
        """Set the value for the given path."""
        self.service.set_var(path, value)

    @_trace
    def get_var(self, path: str) -> Any:
        """Get the value for the given path."""
        return self.service.get_var(path)

    @_trace
    def rename(self, path: str, new: str, old: str) -> None:
        """Rename the object at the given path."""
        self.service.rename(path, new, old)

    @_trace
    def create(self, path: str, name: str) -> None:
        """Create a named object child for the given path."""
        self.service.create(path, name)

    @_trace
    def delete(self, path: str, name: str) -> None:
        """Delete the object with the given name at the given path."""
        self.service.delete(path, name)

    @_trace
    def get_object_names(self, path: str) -> list[str]:
        """Get a list of named objects."""
        return self.service.get_object_names(path)

    @_trace
    def get_list_size(self, path: str) -> int:
        """Get the number of elements in a list object."""
        return self.service.get_list_size(path)

    @_trace
    def resize_list_object(self, path: str, size: int) -> None:
        """Resize a list object."""
        self.service.resize_list_object(path, size)

    @_trace
    def get_static_info(self) -> dict[str, Any]:
        """Get static-info for settings.

        Raises
        ------
        RuntimeError
            If type is empty.
        """
        return self._extract_static_info(self.service.get_static_info())

    @_trace
    def execute_cmd(self, path: str, command: str, **kwds) -> Any:
        """Execute a given command with the provided keyword arguments."""
        return self.service.execute_cmd(path, command, kwds)

    @_trace
    def execute_query(self, path: str, query: str, **kwds) -> Any:
        """Execute a given query with the provided keyword arguments."""
        return self.service.execute_query(path, query, kwds)

    @_trace
    def get_attrs(self, path: str, attrs: list[str], recursive: bool = False) -> Any:
        """Return values of given attributes."""
        return self.service.get_attrs(path, attrs, recursive)

    @_trace
    def _scheme_interpreter_is_defined(self, symbol: str) -> bool:
        return not self._scheme_interpreter_service.eval(
            f"(lexical-unreferenceable? user-initial-environment '{symbol})", True
        )

    @_trace
    def is_wildcard(self, input: str | None = None) -> bool:
        """Check whether a name contains a wildcard pattern."""
        return self._application_runtime_service.is_wildcard(input)

    @_trace
    def has_wildcard(self, name: str) -> bool:
        """Checks whether a name has a wildcard pattern."""
        return self._scheme_interpreter_is_defined(
            "has-fnmatch-wild-card?"
        ) and self.is_wildcard(name)

    @_trace
    def is_interactive_mode(self) -> bool:
        """Checks whether commands can be executed interactively."""
        return False

    @_trace
    def _extract_static_info(self, info) -> dict[str, Any]:
        ret = {}
        ret["type"] = info.type
        for key, value in sorted(info.attrs.items()):
            ret[key] = self._get_state_from_value(value)
        if info.has_allowed_values:
            ret["has-allowed-values"] = info.has_allowed_values
        if info.children:
            ret["children"] = {
                child.name: self._extract_static_info(child.value)
                for child in info.children
            }
        if info.commands:
            ret["commands"] = {
                child.name: self._extract_static_info(child.value)
                for child in info.commands
            }
        if hasattr(info, "queries") and info.queries:
            ret["queries"] = {
                child.name: self._extract_static_info(child.value)
                for child in info.queries
            }
        if info.arguments:
            ret["arguments"] = {
                child.name: self._extract_static_info(child.value)
                for child in info.arguments
            }
        if info.HasField("object_type"):
            ret["object-type"] = self._extract_static_info(info.object_type)
        if info.help:
            ret["help"] = info.help
        try:
            if info.include_child_named_objects:
                ret["include_child_named_objects"] = info.include_child_named_objects
        except AttributeError:
            pass

        try:
            if info.list_size:
                ret["list_size"] = info.list_size
        except AttributeError:
            pass

        try:
            if info.user_creatable:
                ret["user_creatable"] = info.user_creatable
        except AttributeError:
            ret["user_creatable"] = True

        return ret


class Settings(AbstractSettings):
    """Service for accessing and modifying Fluent settings since Fluent 27R1."""

    def __init__(self, service) -> None:
        """__init__ method of SettingsV261 class."""
        self.service = service

    @_trace
    def set_var(self, path: str, value: Any) -> None:
        """Set the value for the given path."""
        self.service.set_var(path, value)

    @_trace
    def get_var(self, path: str) -> Any:
        """Get the value for the given path."""
        return self.service.get_var(path)

    @_trace
    def rename(self, path: str, new: str, old: str) -> None:
        """Rename the object at the given path."""
        self.service.rename(path, new, old)

    @_trace
    def create(self, path: str, name: str) -> None:
        """Create a named object child for the given path."""
        self.service.create(path, name)

    @_trace
    def delete(self, path: str, name: str) -> None:
        """Delete the object with the given name at the given path."""
        self.service.delete(path, name)

    @_trace
    def get_object_names(self, path: str) -> list[str]:
        """Get a list of named objects."""
        return self.service.get_object_names(path)

    @_trace
    def get_list_size(self, path: str) -> int:
        """Get the number of elements in a list object."""
        return self.service.get_list_size(path)

    @_trace
    def resize_list_object(self, path: str, size: int) -> None:
        """Resize a list object."""
        self.service.resize_list_object(path, size)

    @_trace
    def get_static_info(self) -> dict[str, Any]:
        """Get static-info for settings.

        Raises
        ------
        RuntimeError
            If type is empty.
        """
        return self._extract_static_info(self.service.get_static_info())

    @_trace
    def execute_cmd(self, path: str, command: str, **kwds) -> Any:
        """Execute a given command with the provided keyword arguments."""
        return self.service.execute_cmd(path, command, kwds)

    @_trace
    def execute_query(self, path: str, query: str, **kwds) -> Any:
        """Execute a given query with the provided keyword arguments."""
        return self.service.execute_query(path, query, kwds)

    @_trace
    def get_attrs(self, path: str, attrs: list[str], recursive: bool = False) -> Any:
        """Return values of given attributes."""
        return self.service.get_attrs(path, attrs, recursive)

    @_trace
    def is_interactive_mode(self) -> bool:
        """Checks whether commands can be executed interactively."""
        return False

    @_trace
    def _extract_static_info(self, info) -> dict[str, Any]:
        ret = {}
        ret["type"] = info.type
        for key, value in sorted(info.attrs.items()):
            ret[key] = self._get_state_from_value(value)
        if info.has_allowed_values:
            ret["has-allowed-values"] = info.has_allowed_values
        if info.children:
            ret["children"] = {
                child.name: self._extract_static_info(child.value)
                for child in info.children
            }
        if info.commands:
            ret["commands"] = {
                child.name: self._extract_static_info(child.value)
                for child in info.commands
            }
        if hasattr(info, "queries") and info.queries:
            ret["queries"] = {
                child.name: self._extract_static_info(child.value)
                for child in info.queries
            }
        if info.arguments:
            ret["arguments"] = {
                child.name: self._extract_static_info(child.value)
                for child in info.arguments
            }
        if info.HasField("object_type"):
            ret["object-type"] = self._extract_static_info(info.object_type)
        if info.help:
            ret["help"] = info.help
        try:
            if info.include_child_named_objects:
                ret["include_child_named_objects"] = info.include_child_named_objects
        except AttributeError:
            pass

        try:
            if info.list_size:
                ret["list_size"] = info.list_size
        except AttributeError:
            pass

        try:
            if info.user_creatable:
                ret["user_creatable"] = info.user_creatable
        except AttributeError:
            ret["user_creatable"] = True

        return ret

    @_trace
    def is_wildcard(self, input: str | None = None) -> bool:
        """Check whether a name contains a wildcard pattern (v1: Settings.IsWildcard)."""
        return self.service.is_wildcard(input)

    @_trace
    def has_wildcard(self, name: str) -> bool:
        """Check whether a name has a wildcard pattern (v1: uses Settings.IsWildcard directly)."""
        return self.is_wildcard(name)
