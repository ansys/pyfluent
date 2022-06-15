"""Wrappers over TUI-based datamodel grpc service of Fluent."""

import keyword
import types
from typing import Any, Iterable, List, Tuple, Union

import grpc

from ansys.api.fluent.v0 import datamodel_tui_pb2 as DataModelProtoModule
from ansys.api.fluent.v0 import datamodel_tui_pb2_grpc as DataModelGrpcModule
from ansys.api.fluent.v0.variant_pb2 import Variant
from ansys.fluent.core.services.error_handler import catch_grpc_error
from ansys.fluent.core.services.interceptors import TracingInterceptor

Path = List[str]


class DatamodelService:
    """Class wrapping the TUI-based datamodel grpc service of Fluent.

    It is suggested to use the methods from PyMenu class.
    """

    def __init__(self, channel: grpc.Channel, metadata: List[Tuple[str, str]]):
        tracing_interceptor = TracingInterceptor()
        intercept_channel = grpc.intercept_channel(channel, tracing_interceptor)
        self.__stub = DataModelGrpcModule.DataModelStub(intercept_channel)
        self.__metadata = metadata

    @catch_grpc_error
    def get_attribute_value(
        self, request: DataModelProtoModule.GetAttributeValueRequest
    ) -> DataModelProtoModule.GetAttributeValueResponse:
        return self.__stub.GetAttributeValue(request, metadata=self.__metadata)

    @catch_grpc_error
    def get_state(
        self, request: DataModelProtoModule.GetStateRequest
    ) -> DataModelProtoModule.GetStateResponse:
        return self.__stub.GetState(request, metadata=self.__metadata)

    @catch_grpc_error
    def set_state(
        self, request: DataModelProtoModule.SetStateRequest
    ) -> DataModelProtoModule.SetStateResponse:
        return self.__stub.SetState(request, metadata=self.__metadata)

    @catch_grpc_error
    def execute_command(
        self, request: DataModelProtoModule.ExecuteCommandRequest
    ) -> DataModelProtoModule.ExecuteCommandResponse:
        return self.__stub.ExecuteCommand(request, metadata=self.__metadata)

    @catch_grpc_error
    def execute_query(
        self, request: DataModelProtoModule.ExecuteQueryRequest
    ) -> DataModelProtoModule.ExecuteQueryResponse:
        return self.__stub.ExecuteQuery(request, metadata=self.__metadata)


def _convert_value_to_gvalue(val: Any, gval: Variant):
    """Convert Python datatype to Value type of
    google/protobuf/struct.proto."""
    if isinstance(val, bool):
        gval.bool_value = val
    elif isinstance(val, int) or isinstance(val, float):
        gval.number_value = val
    elif isinstance(val, str):
        gval.string_value = val
    elif isinstance(val, list) or isinstance(val, tuple):
        # set the one_of to list_value
        gval.list_value.values.add()
        gval.list_value.values.pop()
        for item in val:
            item_gval = gval.list_value.values.add()
            _convert_value_to_gvalue(item, item_gval)
    elif isinstance(val, dict):
        for k, v in val.items():
            _convert_value_to_gvalue(v, gval.struct_value.fields[k])


def _convert_gvalue_to_value(gval: Variant):
    """Convert Value type of google/protobuf/struct.proto to Python
    datatype."""
    if gval.HasField("bool_value"):
        return gval.bool_value
    elif gval.HasField("number_value"):
        return gval.number_value
    elif gval.HasField("string_value"):
        return gval.string_value
    elif gval.HasField("list_value"):
        val = []
        for item in gval.list_value.values:
            val.append(_convert_gvalue_to_value(item))
        return val
    elif gval.HasField("struct_value"):
        val = {}
        for k, v in gval.struct_value.fields.items():
            val[k] = _convert_gvalue_to_value(v)
        return val


class PyMenu:
    """Pythonic wrapper of TUI-based DatamodelService class. Use this class
    instead of directly calling DatamodelService's method.

    Methods
    -------
    get_child_names(include_unavailable):
        Get child menu names
    execute(*args, **kwargs)
        Execute command/query at menu with positional or keyword
        arguments
    get_doc_string(include_unavailable)
        Get docstring for menu
    """

    def __init__(self, service: DatamodelService, path: Union[Path, str]):
        self._service = service
        self._path = path if isinstance(path, str) else convert_path_to_grpc_path(path)

    def get_child_names(self, include_unavailable: bool = False) -> List[str]:
        """Get child menu names.

        Parameters
        ----------
        include_unavailable : bool, optional
            When True, will query over static TUI metadata,
            by default False

        Returns
        -------
        List[str]
        """
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.path = self._path
        request.attribute = DataModelProtoModule.Attribute.CHILD_NAMES
        if include_unavailable:
            request.args["include_unavailable"] = 1
        response = self._service.get_attribute_value(request)
        return _convert_gvalue_to_value(response.value)

    def _execute_command(
        self, request: DataModelProtoModule.ExecuteCommandRequest
    ) -> Any:
        ret = self._service.execute_command(request)
        return _convert_gvalue_to_value(ret.result)

    def _execute_query(
        self, request: DataModelProtoModule.ExecuteCommandRequest
    ) -> Any:
        ret = self._service.execute_query(request)
        return _convert_gvalue_to_value(ret.result)

    def execute(self, *args, **kwargs) -> Any:
        """Execute command/query at path with positional or keyword arguments.

        Parameters
        ----------

        Returns
        -------
        Any
            Query result (any Python datatype) or Future object
            wrapping TUI output of a command
        """
        request = DataModelProtoModule.ExecuteCommandRequest()
        request.path = self._path
        if kwargs:
            for k, v in kwargs.items():
                _convert_value_to_gvalue(v, request.args.fields[k])
        else:
            _convert_value_to_gvalue(args, request.args.fields["tui_args"])
        if self._path.startswith("/query/"):
            return self._execute_query(request)
        else:
            return self._execute_command(request)

    def get_doc_string(self, include_unavailable: bool = False) -> str:
        """Get docstring for menu.

        Parameters
        ----------
        include_unavailable : bool, optional
            When True, will query over static TUI metadata,
            by default False

        Returns
        -------
        str
        """
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.path = self._path
        request.attribute = DataModelProtoModule.Attribute.HELP_STRING
        if include_unavailable:
            request.args["include_unavailable"] = 1
        response = self._service.get_attribute_value(request)
        return _convert_gvalue_to_value(response.value)


class TUIMenu:
    """Base class for the generated menu classes."""

    def __init__(self, path, service):
        self.path = path
        self.service = service

    def __dir__(self) -> Iterable[str]:
        return [
            convert_tui_menu_to_func_name(x)
            for x in PyMenu(self.service, self.path).get_child_names()
        ]

    def __getattribute__(self, name):
        attr = super().__getattribute__(name)
        if type(attr) == types.MethodType:
            path = self.path + [name]
            # if menus are inserted at runtime in Fluent
            if PyMenu(self.service, path).get_child_names():
                return TUIMenuGeneric(path, self.service)
        return attr


class TUIMenuGeneric(TUIMenu):
    """Generic menu class for when the explicit menu classes aren't
    available."""

    def __getattribute__(self, name):
        if name in ["path", "service"]:
            return super().__getattribute__(name)
        name = convert_func_name_to_tui_menu(name)
        path = self.path + [name]
        if PyMenu(self.service, path).get_child_names():
            return TUIMenuGeneric(path, self.service)
        else:
            return TUICommandGeneric(path, self.service)


class TUICommandGeneric(TUIMenu):
    """Generic command class for when the explicit menu classes aren't
    available."""

    def __call__(self, *args, **kwargs):
        return PyMenu(self.service, self.path).execute(*args, **kwargs)


def convert_func_name_to_tui_menu(func_name: str) -> str:
    """Convert Python function name to TUI menu string.

    Parameters
    ----------
    func_name : str

    Returns
    -------
    str
    """
    if func_name.endswith("_") and keyword.iskeyword(func_name[:-1]):
        return func_name[:-1]
    return func_name


def convert_tui_menu_to_func_name(menu: str) -> str:
    """Convert TUI menu string to Python function name.

    Parameters
    ----------
    menu : str

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
    """Convert path structure to a string which can be passed to datamodel grpc
    service.

    Parameters
    ----------
    path : Path
        Path structure

    Returns
    -------
    str
        grpc path
    """
    return "/" + "/".join(convert_func_name_to_tui_menu(x) for x in path)
