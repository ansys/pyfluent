"""Wrappers over TUI-based datamodel grpc service of Fluent."""

import keyword
from typing import Any, List, Tuple

import grpc

from ansys.api.fluent.v0 import datamodel_tui_pb2 as DataModelProtoModule
from ansys.api.fluent.v0 import datamodel_tui_pb2_grpc as DataModelGrpcModule
from ansys.fluent.core.async_execution import asynchronous
from ansys.fluent.services.error_handler import catch_grpc_error
from ansys.fluent.services.interceptors import TracingInterceptor

Path = List[Tuple[str, str]]


class DatamodelService:
    """
    Class wrapping the TUI-based datamodel grpc service of Fluent.
    It is suggested to use the methods from PyMenu class.
    """

    def __init__(self, channel: grpc.Channel, metadata):
        tracing_interceptor = TracingInterceptor()
        intercept_channel = grpc.intercept_channel(
            channel, tracing_interceptor
        )
        self.__stub = DataModelGrpcModule.DataModelStub(intercept_channel)
        self.__metadata = metadata

    @catch_grpc_error
    def get_attribute_value(self, request):
        return self.__stub.GetAttributeValue(request, metadata=self.__metadata)

    @catch_grpc_error
    def get_state(self, request):
        return self.__stub.GetState(request, metadata=self.__metadata)

    @catch_grpc_error
    def set_state(self, request):
        return self.__stub.SetState(request, metadata=self.__metadata)

    @catch_grpc_error
    def execute_command(self, request):
        return self.__stub.ExecuteCommand(request, metadata=self.__metadata)

    @catch_grpc_error
    def execute_query(self, request):
        return self.__stub.ExecuteQuery(request, metadata=self.__metadata)


def _convert_value_to_gvalue(val, gval):
    """
    Convert Python datatype to Value type of
    google/protobuf/struct.proto
    """
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


def _convert_gvalue_to_value(gval):
    """
    Convert Value type of google/protobuf/struct.proto to Python
    datatype
    """
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
    """
    Pythonic wrapper of TUI-based DatamodelService class. Use this class
    instead of directly calling DatamodelService's method.

    Methods
    -------
    is_extended_tui(path, include_unavailable=False)
        Check if path is part of extended TUI
    is_container(path, include_unavailable=False)
        Check if path is of a container
    get_child_names(path, include_unavailable=False):
        Get child menu names
    get_state(path)
        Get state of the object at path
    set_state(path, value)
        Set state of the object at path
    execute(path, *args, **kwargs)
        Execute command/query at path with positional or keyword
        arguments
    get_doc_string(path: str, include_unavailable=False)
        Get docstring for path
    rename(path, new_name)
        Rename the object at path
    get_child_object_names(path)
        Get child object names of the container at path
    set_item(path, name, value)
        Create or set state of child object within contanier at path
    del_item(path)
        Delete the child object at path

    """

    def __init__(self, service: DatamodelService):
        self.__service = service

    def is_extended_tui(
        self, path: str, include_unavailable: bool = False
    ) -> bool:
        """Check if path is part of extended TUI

        Parameters
        ----------
        path : str
        include_unavailable : bool, optional
            When True, will query over static TUI metadata,
            by default False

        Returns
        -------
        bool
        """
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.path = path
        request.attribute = DataModelProtoModule.Attribute.CUSTOM
        request.args["is_extended_tui"] = 1
        if include_unavailable:
            request.args["include_unavailable"] = 1
        response = self.__service.get_attribute_value(request)
        return _convert_gvalue_to_value(response.value)

    def is_container(
        self, path: str, include_unavailable: bool = False
    ) -> bool:
        """Check if path is of a container

        Parameters
        ----------
        path : str
        include_unavailable : bool, optional
            When True, will query over static TUI metadata,
            by default False

        Returns
        -------
        bool
        """
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.path = path
        request.attribute = DataModelProtoModule.Attribute.DATA_TYPE
        if include_unavailable:
            request.args["include_unavailable"] = 1
        response = self.__service.get_attribute_value(request)
        return (
            _convert_gvalue_to_value(response.value) == "NamedObjectContainer"
        )

    def get_child_names(
        self, path: str, include_unavailable: bool = False
    ) -> bool:
        """Get child menu names

        Parameters
        ----------
        path : str
        include_unavailable : bool, optional
            When True, will query over static TUI metadata,
            by default False

        Returns
        -------
        bool
        """
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.path = path
        request.attribute = DataModelProtoModule.Attribute.CHILD_NAMES
        if include_unavailable:
            request.args["include_unavailable"] = 1
        response = self.__service.get_attribute_value(request)
        return _convert_gvalue_to_value(response.value)

    def get_state(self, path: str) -> Any:
        """Get state of the object at path

        Parameters
        ----------
        path : str

        Returns
        -------
        Any
            state
        """
        request = DataModelProtoModule.GetStateRequest()
        request.path = path
        response = self.__service.get_state(request)
        return _convert_gvalue_to_value(response.state)

    def set_state(self, path: str, value: Any):
        """Set state of the object at path

        Parameters
        ----------
        path : str
        value : Any
            state
        """
        request = DataModelProtoModule.SetStateRequest()
        request.path = path
        _convert_value_to_gvalue(value, request.state)
        self.__service.set_state(request)

    @asynchronous
    def execute(self, path: str, *args, **kwargs) -> Any:
        """Execute command/query at path with positional or keyword
        arguments

        Parameters
        ----------
        path : str

        Returns
        -------
        Any
            Query result (any Python datatype) or Future object
            wrapping TUI output of a command
        """
        request = DataModelProtoModule.ExecuteCommandRequest()
        request.path = path
        if kwargs:
            for k, v in kwargs.items():
                _convert_value_to_gvalue(v, request.args.fields[k])
        else:
            _convert_value_to_gvalue(args, request.args.fields["tui_args"])
        if path.startswith("/query/"):
            ret = self.__service.execute_query(request)
            return _convert_gvalue_to_value(ret.result)
        else:
            ret = self.__service.execute_command(request)
            return _convert_gvalue_to_value(ret.result)

    def get_doc_string(
        self, path: str, include_unavailable: bool = False
    ) -> str:
        """Get docstring for path

        Parameters
        ----------
        path : str
        include_unavailable : bool, optional
            When True, will query over static TUI metadata,
            by default False

        Returns
        -------
        str
        """
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.path = path
        request.attribute = DataModelProtoModule.Attribute.HELP_STRING
        if include_unavailable:
            request.args["include_unavailable"] = 1
        response = self.__service.get_attribute_value(request)
        return _convert_gvalue_to_value(response.value)

    def rename(self, path: str, new_name: str):
        """Rename the object at path

        Parameters
        ----------
        path : str
        new_name : str
        """
        request = DataModelProtoModule.SetStateRequest()
        request.path = path
        _convert_value_to_gvalue(
            new_name, request.state.struct_value.fields["name"]
        )
        self.__service.set_state(request)

    def get_child_object_names(self, path: str) -> List[str]:
        """Get child object names of the container at path

        Parameters
        ----------
        path : str

        Returns
        -------
        List[str]
        """
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.path = path
        request.attribute = DataModelProtoModule.Attribute.OBJECT_NAMES
        response = self.__service.get_attribute_value(request)
        return _convert_gvalue_to_value(response.value)

    def set_item(self, path: str, name: str, value: Any):
        """Create or set state of child object within contanier at path

        Parameters
        ----------
        path : str
        name : str
            child object name
        value : Any
            state
        """
        request = DataModelProtoModule.SetStateRequest()
        request.path = path
        _convert_value_to_gvalue(value, request.state)
        self.__service.set_state(request)

    def del_item(self, path: str):
        """Delete the child object at path

        Parameters
        ----------
        path : str
        """
        request = DataModelProtoModule.SetStateRequest()
        request.path = path
        self.__service.set_state(request)


def convert_func_name_to_tui_menu(func_name: str) -> str:
    """
    Convert Python function name to TUI menu string
    E.g. import_ -> import
    TODO convert underscore -> hyphen, question mark etc., currently
    those are done in server side

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
    """
    Convert TUI menu string to Python function name
    E.g. import -> import_
         type? -> type_flag
    TODO convert hyphen -> underscore, currently those are done in
    server side

    Parameters
    ----------
    menu : str

    Returns
    -------
    str
    """
    if keyword.iskeyword(menu):
        return menu + "_"
    if menu.endswith("?"):
        return menu[:-1] + "_flag"
    return menu


def convert_path_to_grpc_path(path: Path) -> str:
    """
    Convert path structure to a string which can be passed to
    datamodel grpc service

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
