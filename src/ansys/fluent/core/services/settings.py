"""Wrapper to settings gRPC service of Fluent."""

import collections.abc
from functools import wraps
from typing import Any

import grpc

from ansys.api.fluent.v0 import settings_pb2 as SettingsModule
from ansys.api.fluent.v0 import settings_pb2_grpc as SettingsGrpcModule
from ansys.fluent.core.services.interceptors import (
    BatchInterceptor,
    ErrorStateInterceptor,
    GrpcErrorInterceptor,
    TracingInterceptor,
)


class _SettingsServiceImpl:
    def __init__(
        self, channel: grpc.Channel, metadata: list[tuple[str, str]], fluent_error_state
    ) -> None:
        intercept_channel = grpc.intercept_channel(
            channel,
            GrpcErrorInterceptor(),
            ErrorStateInterceptor(fluent_error_state),
            TracingInterceptor(),
            BatchInterceptor(),
        )
        self.__stub = SettingsGrpcModule.SettingsStub(intercept_channel)
        self.__metadata = metadata

    def set_var(
        self, request: SettingsModule.SetVarRequest
    ) -> SettingsModule.SetVarResponse:
        """Set a variable."""
        return self.__stub.SetVar(request, metadata=self.__metadata)

    def get_var(
        self, request: SettingsModule.GetVarRequest
    ) -> SettingsModule.GetVarResponse:
        """Get a variable."""
        return self.__stub.GetVar(request, metadata=self.__metadata)

    def rename(
        self, request: SettingsModule.RenameRequest
    ) -> SettingsModule.RenameResponse:
        """Rename an object."""
        return self.__stub.Rename(request, metadata=self.__metadata)

    def create(
        self, request: SettingsModule.CreateRequest
    ) -> SettingsModule.CreateResponse:
        """Create an object."""
        return self.__stub.Create(request, metadata=self.__metadata)

    def delete(
        self, request: SettingsModule.DeleteRequest
    ) -> SettingsModule.DeleteResponse:
        """Delete an object."""
        return self.__stub.Delete(request, metadata=self.__metadata)

    def get_object_names(
        self, request: SettingsModule.GetObjectNamesRequest
    ) -> SettingsModule.GetObjectNamesResponse:
        """Get object names."""
        return self.__stub.GetObjectNames(request, metadata=self.__metadata)

    def get_list_size(
        self, request: SettingsModule.GetListSizeRequest
    ) -> SettingsModule.GetListSizeResponse:
        """Get list size."""
        return self.__stub.GetListSize(request, metadata=self.__metadata)

    def resize_list_object(
        self, request: SettingsModule.ResizeListObjectRequest
    ) -> SettingsModule.ResizeListObjectResponse:
        """Resize list object."""
        return self.__stub.ResizeListObject(request, metadata=self.__metadata)

    def get_static_info(
        self, request: SettingsModule.GetStaticInfoRequest
    ) -> SettingsModule.GetStaticInfoResponse:
        """Get static info."""
        return self.__stub.GetStaticInfo(request, metadata=self.__metadata)

    def execute_cmd(
        self, request: SettingsModule.ExecuteCommandRequest
    ) -> SettingsModule.ExecuteCommandResponse:
        """Execute the command."""
        return self.__stub.ExecuteCommand(request, metadata=self.__metadata)

    def execute_query(
        self, request: SettingsModule.ExecuteQueryRequest
    ) -> SettingsModule.ExecuteQueryResponse:
        """Execute the query."""
        return self.__stub.ExecuteQuery(request, metadata=self.__metadata)

    def get_attrs(
        self, request: SettingsModule.GetAttrsRequest
    ) -> SettingsModule.GetAttrsResponse:
        """Get attributes."""
        return self.__stub.GetAttrs(request, metadata=self.__metadata)


trace: bool = False
_indent: int = 0


def _trace(fn):
    @wraps(fn)
    def _fn(self, *args, **kwds):
        global _indent
        if trace:
            print(f"{' '*_indent}fn={fn.__name__}, args={args} {{")
            try:
                _indent += 1
                ret = fn(self, *args, **kwds)
            finally:
                _indent -= 1
            print(f"{' '*_indent}fn = {fn.__name__}, ret={ret} }}")
            return ret
        else:
            return fn(self, *args, **kwds)

    return _fn


def _get_request_instance_for_path(request_class, path: str) -> Any:
    request = request_class()
    request.path_info.path = path
    request.path_info.root = "fluent"
    return request


class SettingsService:
    """Service for accessing and modifying Fluent settings."""

    def __init__(
        self, channel, metadata, app_utilities, scheme_eval, fluent_error_state
    ) -> None:
        """__init__ method of SettingsService class."""
        self._service_impl = _SettingsServiceImpl(channel, metadata, fluent_error_state)
        self._app_utilities = app_utilities
        self._scheme_eval = scheme_eval

    @_trace
    def _set_state_from_value(self, state: SettingsModule.Value, value: Any):
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
                self._set_state_from_value(state.value_list.lst.add(), v)
        else:  # fall back to string (for example, pathlib.Path)
            state.string = str(value)

    @_trace
    def _get_state_from_value(self, state: SettingsModule.Value) -> Any:
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
            return [self._get_state_from_value(v) for v in state.value_list.lst]
        elif t == "value_map":
            return {
                k: self._get_state_from_value(v)
                for k, v in sorted(state.value_map.m.items())
            }
        else:
            return None

    @_trace
    def set_var(self, path: str, value: Any) -> None:
        """Set the value for the given path."""
        request = _get_request_instance_for_path(SettingsModule.SetVarRequest, path)
        self._set_state_from_value(request.value, value)
        self._service_impl.set_var(request)

    @_trace
    def get_var(self, path: str) -> Any:
        """Get the value for the given path."""
        request = _get_request_instance_for_path(SettingsModule.GetVarRequest, path)
        response = self._service_impl.get_var(request)
        return self._get_state_from_value(response.value)

    @_trace
    def rename(self, path: str, new: str, old: str) -> None:
        """Rename the object at the given path."""
        request = _get_request_instance_for_path(SettingsModule.RenameRequest, path)
        request.old_name = old
        request.new_name = new

        self._service_impl.rename(request)

    @_trace
    def create(self, path: str, name: str) -> None:
        """Create a named object child for the given path."""
        request = _get_request_instance_for_path(SettingsModule.CreateRequest, path)
        request.name = name

        self._service_impl.create(request)

    @_trace
    def delete(self, path: str, name: str) -> None:
        """Delete the object with the given name at the given path."""
        request = _get_request_instance_for_path(SettingsModule.DeleteRequest, path)
        request.name = name

        self._service_impl.delete(request)

    @_trace
    def get_object_names(self, path: str) -> list[str]:
        """Get a list of named objects."""
        request = _get_request_instance_for_path(
            SettingsModule.GetObjectNamesRequest, path
        )
        return self._service_impl.get_object_names(request).names

    @_trace
    def get_list_size(self, path: str) -> int:
        """Get the number of elements in a list object."""
        request = _get_request_instance_for_path(
            SettingsModule.GetListSizeRequest, path
        )
        return self._service_impl.get_list_size(request).size

    @_trace
    def resize_list_object(self, path: str, size: int) -> None:
        """Resize a list object."""
        request = _get_request_instance_for_path(
            SettingsModule.ResizeListObjectRequest, path
        )
        request.size = size
        return self._service_impl.resize_list_object(request)

    @_trace
    def _extract_static_info(self, info: SettingsModule.StaticInfo) -> dict[str, Any]:
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
    def get_static_info(self) -> dict[str, Any]:
        """Get static-info for settings.

        Raises
        ------
        RuntimeError
            If type is empty.
        """
        request = SettingsModule.GetStaticInfoRequest()
        request.root = "fluent"
        response = self._service_impl.get_static_info(request)
        # The RPC calls no longer raise an exception. Force an exception if
        # type is empty
        if not response.info.type:
            raise RuntimeError
        return self._extract_static_info(response.info)

    @_trace
    def execute_cmd(self, path: str, command: str, **kwds) -> Any:
        """Execute a given command with the provided keyword arguments."""
        request = _get_request_instance_for_path(
            SettingsModule.ExecuteCommandRequest, path
        )
        request.command = command
        self._set_state_from_value(request.args, kwds)

        response = self._service_impl.execute_cmd(request)
        return self._get_state_from_value(response.reply)

    @_trace
    def execute_query(self, path: str, query: str, **kwds) -> Any:
        """Execute a given query with the provided keyword arguments."""
        request = _get_request_instance_for_path(
            SettingsModule.ExecuteQueryRequest, path
        )
        request.query = query
        self._set_state_from_value(request.args, kwds)

        response = self._service_impl.execute_query(request)
        return self._get_state_from_value(response.reply)

    @_trace
    def _parse_attrs(self, response: SettingsModule.GetAttrsResponse) -> dict[str, Any]:
        ret = {}
        ret["attrs"] = self._get_state_from_value(response.values)
        if response.group_children:
            ret["group_children"] = {
                child.name: self._parse_attrs(child.value)
                for child in response.group_children
            }
        return ret

    @_trace
    def get_attrs(self, path: str, attrs: list[str], recursive: bool = False) -> Any:
        """Return values of given attributes."""
        request = _get_request_instance_for_path(SettingsModule.GetAttrsRequest, path)
        request.attrs[:] = attrs
        request.recursive = recursive

        response = self._service_impl.get_attrs(request)
        if recursive:
            return self._parse_attrs(response)
        return self._get_state_from_value(response.values)

    @_trace
    def has_wildcard(self, name: str) -> bool:
        """Checks whether a name has a wildcard pattern."""
        return self._scheme_eval.is_defined(
            "has-fnmatch-wild-card?"
        ) and self._app_utilities.is_wildcard(name)

    @_trace
    def is_interactive_mode(self) -> bool:
        """Checks whether commands can be executed interactively."""
        return False
