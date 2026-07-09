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

"""Wrapper over the settings gRPC service of Fluent (v1 proto API)."""

import collections.abc
from typing import Any

import grpc

from ansys.api.fluent.v1 import settings_pb2, settings_pb2_grpc
from ansys.fluent.core.services._protocols import ServiceProtocol
from ansys.fluent.core.services.interceptors import (
    BatchInterceptor,
    ErrorStateInterceptor,
    GrpcErrorInterceptor,
    TracingInterceptor,
)


def _get_request_instance_for_path(request_class, path: str) -> Any:
    request = request_class()
    request.path_info.path = path
    request.path_info.root = "fluent"
    return request


class SettingsService(ServiceProtocol):
    """Settings gRPC service wrapper (v1 proto API)."""

    def __init__(
        self, channel: grpc.Channel, metadata: list[tuple[str, str]], fluent_error_state
    ) -> None:
        """Initialize SettingsService."""
        intercept_channel = grpc.intercept_channel(
            channel,
            GrpcErrorInterceptor(),
            ErrorStateInterceptor(fluent_error_state),
            TracingInterceptor(),
            BatchInterceptor(),
        )
        self._stub = settings_pb2_grpc.SettingsStub(intercept_channel)
        self._metadata = metadata

    def _set_state_from_value(self, state: settings_pb2.Value, value: Any):
        if value is None:
            return
        if isinstance(value, bool):
            state.boolean = value
        elif isinstance(value, int):
            state.integer = value
        elif isinstance(value, float):
            state.real = value
        elif isinstance(value, str):
            state.string = value
        elif isinstance(value, collections.abc.Mapping):
            for k, v in value.items():
                self._set_state_from_value(state.value_map.m[k], v)
        elif isinstance(value, collections.abc.Iterable):
            for v in value:
                self._set_state_from_value(getattr(state.value_list, "lsts").add(), v)
        else:  # fall back to string (for example, pathlib.Path)
            state.string = str(value)

    def _get_state_from_value(self, state: settings_pb2.Value) -> Any:
        t = state.WhichOneof("value")
        if t == "boolean":
            return state.boolean
        elif t == "integer":
            return state.integer
        elif t == "real":
            return state.real
        elif t == "string":
            return state.string
        elif t == "value_list":
            return [
                self._get_state_from_value(v) for v in getattr(state.value_list, "lsts")
            ]
        elif t == "value_map":
            return {
                k: self._get_state_from_value(v)
                for k, v in sorted(state.value_map.m.items())
            }
        else:
            return None

    def set_var(self, path: str, value: Any) -> None:
        """Set the value for the given path."""
        request = _get_request_instance_for_path(settings_pb2.SetStateRequest, path)
        self._set_state_from_value(request.value, value)
        self._stub.SetState(request, metadata=self._metadata)

    def get_var(self, path: str) -> Any:
        """Get the value for the given path."""
        request = _get_request_instance_for_path(settings_pb2.GetStateRequest, path)
        response = self._stub.GetState(request, metadata=self._metadata)
        return self._get_state_from_value(response.value)

    def rename(self, path: str, new: str, old: str) -> None:
        """Rename the object at the given path."""
        request = _get_request_instance_for_path(settings_pb2.RenameRequest, path)
        request.old_name = old
        request.new_name = new
        self._stub.Rename(request, metadata=self._metadata)

    def create(self, path: str, name: str) -> None:
        """Create a named object child for the given path."""
        request = _get_request_instance_for_path(settings_pb2.CreateObjectRequest, path)
        request.name = name
        self._stub.CreateObject(request, metadata=self._metadata)

    def delete(self, path: str, name: str) -> None:
        """Delete the object with the given name at the given path."""
        request = _get_request_instance_for_path(settings_pb2.DeleteObjectRequest, path)
        request.name = name
        self._stub.DeleteObject(request, metadata=self._metadata)

    def get_object_names(self, path: str) -> list[str]:
        """Get a list of named objects."""
        request = _get_request_instance_for_path(
            settings_pb2.GetObjectNamesRequest, path
        )
        return self._stub.GetObjectNames(request, metadata=self._metadata).names

    def get_list_size(self, path: str) -> int:
        """Get the number of elements in a list object."""
        request = _get_request_instance_for_path(settings_pb2.GetListSizeRequest, path)
        return self._stub.GetListSize(request, metadata=self._metadata).size

    def resize_list_object(self, path: str, size: int) -> None:
        """Resize a list object."""
        request = _get_request_instance_for_path(
            settings_pb2.ResizeListObjectRequest, path
        )
        request.size = size
        self._stub.ResizeListObject(request, metadata=self._metadata)

    def get_static_info(self) -> dict[str, Any]:
        """Get static-info for settings.

        Raises
        ------
        RuntimeError
            If type is empty.
        """
        request = settings_pb2.GetSchemaRequest()
        request.root = "fluent"
        request.optional_attrs.extend(["allowed-values", "has-migration-adapter?"])
        response = self._stub.GetSchema(request, metadata=self._metadata)
        # The RPC calls no longer raise an exception. Force an exception if
        # type is empty
        if not response.info.type:
            raise RuntimeError
        return self._extract_static_info(response.info)

    def execute_cmd(self, path: str, command: str, **kwds) -> Any:
        """Execute a given command with the provided keyword arguments."""
        request = _get_request_instance_for_path(
            settings_pb2.ExecuteCommandRequest, path
        )
        request.command = command
        self._set_state_from_value(request.args, kwds)

        response = self._stub.ExecuteCommand(request, metadata=self._metadata)
        return self._get_state_from_value(response.reply)

    def execute_query(self, path: str, query: str, **kwds) -> Any:
        """Execute a given query with the provided keyword arguments."""
        request = _get_request_instance_for_path(settings_pb2.ExecuteQueryRequest, path)
        request.query = query
        self._set_state_from_value(request.args, kwds)

        response = self._stub.ExecuteQuery(request, metadata=self._metadata)
        return self._get_state_from_value(response.reply)

    def _parse_attrs(self, response: settings_pb2.GetAttrsResponse) -> dict[str, Any]:
        ret = {}
        ret["attrs"] = self._get_state_from_value(response.values)
        if response.group_children:
            ret["group_children"] = {
                child.name: self._parse_attrs(child.value)
                for child in response.group_children
            }
        return ret

    def get_attrs(self, path: str, attrs: list[str], recursive: bool = False) -> Any:
        """Return values of given attributes."""
        request = _get_request_instance_for_path(settings_pb2.GetAttrsRequest, path)
        request.attrs[:] = attrs
        request.recursive = recursive

        response = self._stub.GetAttrs(request, metadata=self._metadata)
        if recursive:
            return self._parse_attrs(response)
        return self._get_state_from_value(response.values)

    def is_wildcard(self, input: str | None = None) -> bool:
        """Check whether a name contains a wildcard pattern (v1: Settings.IsWildcard)."""
        request = settings_pb2.IsWildcardRequest()
        if input is not None:
            request.input = input
        response = self._stub.IsWildcard(request, metadata=self._metadata)
        return response.is_wildcard

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
