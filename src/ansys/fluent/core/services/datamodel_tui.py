"""Wrappers over TUI-based datamodel grpc service of Fluent."""

import keyword
from typing import Any, List, Tuple, Union

import grpc

from ansys.api.fluent.v0 import datamodel_tui_pb2 as DataModelProtoModule
from ansys.api.fluent.v0 import datamodel_tui_pb2_grpc as DataModelGrpcModule
from ansys.api.fluent.v0.variant_pb2 import Variant
from ansys.fluent.core.services.error_handler import catch_grpc_error
from ansys.fluent.core.services.interceptors import TracingInterceptor

Path = List[Tuple[str, str]]


class DatamodelService:
    """Class wrapping the TUI-based datamodel grpc service of Fluent.

    It is suggested to use the methods from PyMenu class.
    """

    def __init__(self, channel: grpc.Channel, metadata: List[Tuple[str, str]]):
        tracing_interceptor = TracingInterceptor()
        intercept_channel = grpc.intercept_channel(
            channel, tracing_interceptor
        )
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
    is_extended_tui(include_unavailable)
        Check if menu is in extended TUI
    is_container(include_unavailable)
        Check if menu is a container
    get_child_names(include_unavailable):
        Get child menu names
    get_state()
        Get state of the object at menu
    set_state(value)
        Set state of the object at menu
    execute(*args, **kwargs)
        Execute command/query at menu with positional or keyword
        arguments
    get_doc_string(include_unavailable)
        Get docstring for menu
    rename(new_name)
        Rename the object at menu
    get_child_object_names()
        Get child object names of the container at menu
    set_item(name, value)
        Create or set state of child object within contanier at menu
    del_item()
        Delete the child object at menu
    """

    def __init__(self, service: DatamodelService, path: Union[Path, str]):
        self._service = service
        self._path = (
            path if isinstance(path, str) else convert_path_to_grpc_path(path)
        )

    def is_extended_tui(self, include_unavailable: bool = False) -> bool:
        """Check if menu is in extended TUI.

        Parameters
        ----------
        include_unavailable : bool, optional
            When True, will query over static TUI metadata,
            by default False

        Returns
        -------
        bool
        """
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.path = self._path
        request.attribute = DataModelProtoModule.Attribute.CUSTOM
        request.args["is_extended_tui"] = 1
        if include_unavailable:
            request.args["include_unavailable"] = 1
        response = self._service.get_attribute_value(request)
        return _convert_gvalue_to_value(response.value)

    def is_container(self, include_unavailable: bool = False) -> bool:
        """Check if menu is a container.

        Parameters
        ----------
        include_unavailable : bool, optional
            When True, will query over static TUI metadata,
            by default False

        Returns
        -------
        bool
        """
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.path = self._path
        request.attribute = DataModelProtoModule.Attribute.DATA_TYPE
        if include_unavailable:
            request.args["include_unavailable"] = 1
        response = self._service.get_attribute_value(request)
        return (
            _convert_gvalue_to_value(response.value) == "NamedObjectContainer"
        )

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

    def get_state(self) -> Any:
        """Get state of the object at menu.

        Returns
        -------
        Any
            state
        """
        request = DataModelProtoModule.GetStateRequest()
        request.path = self._path
        response = self._service.get_state(request)
        return _convert_gvalue_to_value(response.state)

    def set_state(self, value: Any) -> None:
        """Set state of the object at menu.

        Parameters
        ----------
        value : Any
            state
        """
        request = DataModelProtoModule.SetStateRequest()
        request.path = self._path
        _convert_value_to_gvalue(value, request.state)
        self._service.set_state(request)

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

    def rename(self, new_name: str) -> None:
        """Rename the object at menu.

        Parameters
        ----------
        new_name : str
        """
        request = DataModelProtoModule.SetStateRequest()
        request.path = self._path
        _convert_value_to_gvalue(
            new_name, request.state.struct_value.fields["name"]
        )
        self._service.set_state(request)

    def get_child_object_names(self) -> List[str]:
        """Get child object names of the container at menu.

        Returns
        -------
        List[str]
        """
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.path = self._path
        request.attribute = DataModelProtoModule.Attribute.OBJECT_NAMES
        response = self._service.get_attribute_value(request)
        return _convert_gvalue_to_value(response.value)

    def set_item(self, name: str, value: Any) -> None:
        """Create or set state of child object within contanier at menu.

        Parameters
        ----------
        name : str
            child object name
        value : Any
            state
        """
        request = DataModelProtoModule.SetStateRequest()
        request.path = self._path
        _convert_value_to_gvalue(value, request.state)
        self._service.set_state(request)

    def del_item(self) -> None:
        """Delete the child object at path."""
        request = DataModelProtoModule.SetStateRequest()
        request.path = self._path
        self._service.set_state(request)


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
    grpc_path = ""
    for comp in path:
        grpc_path += "/" + convert_func_name_to_tui_menu(comp[0])
        if comp[1]:
            grpc_path += ":" + comp[1]
    return grpc_path
