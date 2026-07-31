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

"""REST settings service wrapper."""

from typing import Any

from ansys.fluent.core.rest.client import FluentRestClient
from ansys.fluent.core.services.abstract_settings import AbstractSettings
from ansys.fluent.core.services.settings import _trace


class RestSettings(AbstractSettings):
    """REST-based settings service wrapper.

    This class provides high-level settings operations by delegating to a
    FluentRestClient instance. It is used for accessing and modifying Fluent
    settings over HTTP/REST transport.

    Available from Fluent 27.1 onward (v1 proto API).

    Parameters
    ----------
    rest_client : FluentRestClient
        The REST client instance to use for all settings operations.
    """

    def __init__(self, rest_client: FluentRestClient) -> None:
        """Initialize the REST settings service.

        Parameters
        ----------
        rest_client : FluentRestClient
            The REST client instance.
        """
        self.service = rest_client

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
        return self.service.get_static_info()

    @_trace
    def execute_cmd(self, path: str, command: str, **kwds) -> Any:
        """Execute a given command with the provided keyword arguments."""
        return self.service.execute_cmd(path, command, **kwds)

    @_trace
    def execute_query(self, path: str, query: str, **kwds) -> Any:
        """Execute a given query with the provided keyword arguments."""
        return self.service.execute_query(path, query, **kwds)

    @_trace
    def get_attrs(self, path: str, attrs: list[str], recursive: bool = False) -> Any:
        """Return values of given attributes."""
        return self.service.get_attrs(path, attrs, recursive)

    @_trace
    def is_interactive_mode(self) -> bool:
        """Checks whether commands can be executed interactively.

        Raises
        ------
        NotImplementedError
            This method is not applicable to REST transport.
        """
        raise NotImplementedError(
            "Interactive mode is not supported for REST transport."
        )

    @_trace
    def is_wildcard(self, input: str | None = None) -> bool:
        """Check whether a name contains a wildcard pattern.

        Raises
        ------
        NotImplementedError
            This method is not applicable to REST transport.
        """
        raise NotImplementedError(
            "Wildcard checking is not supported for REST transport."
        )

    @_trace
    def has_wildcard(self, name: str) -> bool:
        """Check whether a name has a wildcard pattern.

        Raises
        ------
        NotImplementedError
            This method is not applicable to REST transport.
        """
        raise NotImplementedError(
            "Wildcard checking is not supported for REST transport."
        )
