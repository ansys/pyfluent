"""Wrappers over StateEngine based datamodel grpc service of Fluent."""

import itertools
from enum import Enum
from typing import Any, Iterator, List, Tuple

import grpc

from ansys.api.fluent.v0 import datamodel_se_pb2 as DataModelProtoModule
from ansys.api.fluent.v0 import datamodel_se_pb2_grpc as DataModelGrpcModule
from ansys.fluent.services.interceptors import TracingInterceptor

Path = List[Tuple[str, str]]


class Attribute(Enum):
    IS_ACTIVE = "isActive"
    EXPOSURE_LEVEL = "exposureLevel"
    IS_READ_ONLY = "isReadOnly"
    DEFAULT = "default"
    FORCE_DEFAULT = "forceDefault"
    MIN = "min"
    MAX = "max"
    ALLOWED_VALUES = "allowedValues"
    EXCLUDED_VALUES = "excludedValues"
    MIN_LENGTH = "minLength"
    MAX_LENGTH = "maxLength"
    ERROR_STATUS = "errorStatus"
    USER_ERROR_STATUS = "userErrorStatus"
    MEMBERS = "members"
    DISPLAY_TEXT = "displayText"
    NAMES = "__names__"
    INTERNAL_NAMES = "__ids__"
    PATHS = "__paths__"
    ROOT_ID = "__root__"
    NAME = "_name_"
    REFERENCE_PATH = "referencePath"
    ARGUMENTS = "arguments"
    TOOL_TIP = "toolTip"
    SHOW_AT_PARENT_NODE = "showAtParentNode"
    WIDGET_TYPE = "widgetType"
    ECHO_MODE = "echoMode"
    IS_TREE_NODE = "isTreeNode"
    MIGRATION = "migration"
    DEPRECATED_VERSION = "deprecatedVersion"


class DatamodelService:
    """
    Class wrapping the StateEngine based datamodel grpc service of
    Fluent. It is suggested to use the methods from PyMenu class.
    """

    def __init__(self, channel: grpc.Channel, metadata):
        tracing_interceptor = TracingInterceptor()
        intercept_channel = grpc.intercept_channel(
            channel, tracing_interceptor
        )
        self.__stub = DataModelGrpcModule.DataModelStub(intercept_channel)
        self.__metadata = metadata

    def initialize_datamodel(self, request):
        return self.__stub.initDatamodel(request, metadata=self.__metadata)

    def get_attribute_value(self, request):
        return self.__stub.getAttributeValue(request, metadata=self.__metadata)

    def get_state(self, request):
        return self.__stub.getState(request, metadata=self.__metadata)

    def set_state(self, request):
        return self.__stub.setState(request, metadata=self.__metadata)

    def delete_object(self, request):
        return self.__stub.deleteObject(request, metadata=self.__metadata)

    def execute_command(self, request):
        return self.__stub.executeCommand(request, metadata=self.__metadata)

    def get_specs(self, request):
        return self.__stub.getSpecs(request, metadata=self.__metadata)


def _convert_value_to_variant(val, var, convert_keys=True):
    """Convert Python datatype to Fluent's Variant type"""

    if isinstance(val, bool):
        var.bool_state = val
    elif isinstance(val, int):
        var.int64_state = val
    elif isinstance(val, float):
        var.double_state = val
    elif isinstance(val, str):
        var.string_state = val
    elif isinstance(val, list) or isinstance(val, tuple):
        # set the one_of to variant_vector_state
        var.variant_vector_state.item.add()
        var.variant_vector_state.item.pop()
        for item in val:
            item_var = var.variant_vector_state.item.add()
            _convert_value_to_variant(item, item_var, convert_keys)
    elif isinstance(val, dict):
        for k, v in val.items():
            if convert_keys:
                k = convert_python_name_to_se_name(k)
            _convert_value_to_variant(
                v, var.variant_map_state.item[k], convert_keys
            )


def _convert_variant_to_value(var, convert_keys=True):
    """Convert Fluent's Variant to Python datatype"""

    if var.HasField("bool_state"):
        return var.bool_state
    elif var.HasField("int64_state"):
        return var.int64_state
    elif var.HasField("double_state"):
        return var.double_state
    elif var.HasField("string_state"):
        return var.string_state
    elif var.HasField("bool_vector_state"):
        return var.bool_vector_state
    elif var.HasField("int64_vector_state"):
        return var.int64_vector_state
    elif var.HasField("double_vector_state"):
        return var.double_vector_state
    elif var.HasField("string_vector_state"):
        return var.string_vector_state
    elif var.HasField("variant_vector_state"):
        val = []
        for item in var.variant_vector_state.item:
            val.append(_convert_variant_to_value(item, convert_keys))
        return val
    elif var.HasField("variant_map_state"):
        val = {}
        for k, v in var.variant_map_state.item.items():
            if convert_keys:
                k = convert_se_name_to_python_name(k)
            val[k] = _convert_variant_to_value(v, convert_keys)
        return val


def convert_python_name_to_se_name(python_name: str) -> str:
    """
    Convert Python name to StateEngine name
    E.g. save_image -> SaveImage

    Parameters
    ----------
    python_name : str

    Returns
    -------
    str
    """
    return "".join([x[0].upper() + x[1:] for x in python_name.split("_")])


def convert_se_name_to_python_name(se_name: str) -> str:
    """
    Convert StateEngine name to Python name
    E.g. SaveImage -> save_image

    Parameters
    ----------
    se_name : str

    Returns
    -------
    str
    """
    return "".join(
        ["_" + c.lower() if c.isupper() else c for c in se_name]
    ).lstrip("_")


def _convert_path_to_se_path(path: Path) -> str:
    """
    Convert path structure to a StateEngine path

    Parameters
    ----------
    path : Path
        Path structure

    Returns
    -------
    str
        stateengine path
    """
    se_path = ""
    for comp in path:
        se_path += "/" + comp[0]
        if comp[1]:
            se_path += ":" + comp[1]
    return se_path


class PyMenu:
    """
    Object class using StateEngine based DatamodelService as backend.
    Use this class instead of directly calling DatamodelService's
    method.

    Methods
    -------
    __dir__()
        Returns list of child object names
    __getattr__(name)
        Returns the child object
    __setattr__(name, value)
        Set state of the child object
    __call__()
        Get state of the current object
    get_attrib_value(attrib)
        Get attribute value of the current object

    """

    __slots__ = ("service", "rules", "path")
    docstring = None

    def __init__(
        self, service: DatamodelService, rules: str, path: Path = None
    ):
        self.service = service
        self.rules = rules
        if path is None:
            self.path = []
        else:
            self.path = path

    def __get_child_names(self) -> Tuple[List[str], List[str]]:
        request = DataModelProtoModule.GetSpecsRequest()
        request.rules = self.rules
        request.path = _convert_path_to_se_path(self.path)
        response = self.service.get_specs(request)
        singleton_names = []
        creatable_type_names = []
        command_names = []
        for struct_type in ("singleton", "namedobject"):
            if response.member.HasField(struct_type):
                struct_field = getattr(response.member, struct_type)
                for member in struct_field.members:
                    if ":" not in member:
                        singleton_names.append(
                            convert_se_name_to_python_name(member)
                        )
                creatable_type_names = [
                    convert_se_name_to_python_name(x)
                    for x in struct_field.creatabletypes
                ]
                for command in struct_field.commands:
                    command_names.append(
                        convert_se_name_to_python_name(command.name)
                    )
        return singleton_names, creatable_type_names, command_names

    def __get_child(self, name: str):
        se_name = convert_python_name_to_se_name(name)
        singletons, creatable_types, commands = self.__get_child_names()
        if name in singletons:
            child_path = self.path + [(se_name, "")]
            return PyMenu(self.service, self.rules, child_path)
        elif name in creatable_types:
            child_path = self.path + [(se_name, "")]
            return PyNamedObjectContainer(self.service, self.rules, child_path)
        elif name in commands:
            return PyCommand(self.service, self.rules, se_name, self.path)
        else:
            raise LookupError(
                f"{name} is not found at path "
                f"{_convert_path_to_se_path(self.path_)}"
            )

    def get_state(self):
        request = DataModelProtoModule.GetStateRequest()
        request.rules = self.rules
        request.path = _convert_path_to_se_path(self.path)
        response = self.service.get_state(request)
        return _convert_variant_to_value(response.state)

    def set_state(self, state):
        request = DataModelProtoModule.SetStateRequest()
        request.rules = self.rules
        request.path = _convert_path_to_se_path(self.path)
        _convert_value_to_variant(state, request.state)
        self.service.set_state(request)

    def __dir__(self) -> List[str]:
        """Returns list of child object names

        Returns
        -------
        List[str]
            child object names
        """
        return list(itertools.chain(*self.__get_child_names()))

    def __getattr__(self, name: str) -> Any:
        """Returns the child object

        Parameters
        ----------
        name : str
            child object name

        Returns
        -------
        Any
            child object
        """
        if name in PyMenu.__slots__:
            return super().__getattr__(name)
        else:
            return self.__get_child(name)

    def __setattr__(self, name: str, value: Any):
        """Set state of the child object

        Parameters
        ----------
        name : str
            child object name
        value : Any
            state
        """
        if name in PyMenu.__slots__:
            super().__setattr__(name, value)
        else:
            self.__get_child(name).set_state(value)

    def __call__(self, *args, **kwds) -> Any:
        """Get state of the current object

        Returns
        -------
        Any
            state
        """
        return self.get_state()

    def get_attrib_value(self, attrib: str) -> Any:
        """Get attribute value of the current object

        Parameters
        ----------
        attrib : str
            attribute name

        Returns
        -------
        Any
            attribute value
        """
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.rules = self.rules
        request.path = _convert_path_to_se_path(self.path)
        request.attribute = attrib
        response = self.service.get_attribute_value(request)
        return _convert_variant_to_value(response.result, False)

    def get_docstring(self):
        if self.__class__.docstring is None:
            request = DataModelProtoModule.GetSpecsRequest()
            request.rules = self.rules
            request.path = _convert_path_to_se_path(self.path)
            response = self.service.get_specs(request)
            self.__class__.docstring = getattr(
                response.member, response.member.WhichOneof("as")
            ).common.helpstring
        return self.__class__.docstring

    def help(self):
        """Prints command help string"""
        print(self.get_docstring())


class PyNamedObjectContainer:
    """
    Container class using StateEngine based DatamodelService as backend.
    Use this class instead of directly calling DatamodelService's
    method.

    Methods
    -------
    __len__()
        Returns count of child objects
    __iter__()
        Returns the next child object
    __getitem__(key)
        Returns the child object by key
    __setitem__(key, value)
        Set state of the child object by name
    __delitem__(key)
        Deletes the child object by name

    """

    def __init__(
        self, service: DatamodelService, rules: str, path: Path = None
    ):
        self.service = service
        self.rules = rules
        if path is None:
            self.path = []
        else:
            self.path = path

    def __get_child_object_names(self):
        request = DataModelProtoModule.GetSpecsRequest()
        request.rules = self.rules
        parent_path = self.path[0:-1]
        child_type_suffix = self.path[-1][0] + ":"
        request.path = _convert_path_to_se_path(parent_path)
        response = self.service.get_specs(request)
        child_object_names = []
        for struct_type in ("singleton", "namedobject"):
            if response.member.HasField(struct_type):
                struct_field = getattr(response.member, struct_type)
                for member in struct_field.members:
                    if member.startswith(child_type_suffix):
                        child_object_names.append(
                            member[len(child_type_suffix) :]
                        )
        return child_object_names

    def __get_child_object_display_names(self):
        child_object_display_names = []
        for name in self.__get_child_object_names():
            name_path = self.path[0:-1]
            name_path.append((self.path[-1][0], name))
            name_path.append(("_name_", ""))
            child_object_display_names.append(
                PyMenu(self.service, self.rules, name_path).get_state()
            )
        return child_object_display_names

    def __len__(self) -> int:
        """Returns count of child objects

        Returns
        -------
        int
            count
        """
        return len(self.__get_child_object_display_names())

    def __iter__(self) -> Iterator[PyMenu]:
        """Returns the next child object

        Yields
        -------
        Iterator[PyMenu]
            iterator of child objects
        """
        for name in self.__get_child_object_display_names():
            child_path = self.path[0:-1]
            child_path.append((self.path[-1][0], name))
            yield PyMenu(self.service, self.rules, child_path)

    def __get_item(self, key: str):
        if key in self.__get_child_object_display_names():
            child_path = self.path[0:-1]
            child_path.append((self.path[-1][0], key))
            return PyMenu(self.service, self.rules, child_path)
        else:
            raise LookupError(
                f"{key} is not found at path "
                f"{_convert_path_to_se_path(self.path)}"
            )

    def __del_item(self, key: str):
        if key in self.__get_child_object_display_names():
            child_path = self.path[0:-1]
            child_path.append((self.path[-1][0], key))
            request = DataModelProtoModule.DeleteObjectRequest()
            request.rules = self.rules
            request.path = _convert_path_to_se_path(child_path)
            self.service.delete_object(request)
        else:
            raise LookupError(
                f"{key} is not found at path "
                f"{_convert_path_to_se_path(self.path)}"
            )

    def __getitem__(self, key: str) -> PyMenu:
        """Returns the child object by key

        Parameters
        ----------
        key : str
            child name

        Returns
        -------
        PyMenu
            child object
        """
        return self.__get_item(key)

    def __setitem__(self, key: str, value: Any):
        """Set state of the child object by name

        Parameters
        ----------
        key : str
            child name
        value : Any
            state
        """
        self.__get_item(key).set_state(value)

    def __delitem__(self, key: str):
        """Deletes the child object by name

        Parameters
        ----------
        key : str
            child name
        """
        self.__del_item(key)


class PyCommand:
    """
    Command class using StateEngine based DatamodelService as backend.
    Use this class instead of directly calling DatamodelService's
    method.

    Methods
    -------
    __call__()
        Executes the command
    help()
        Prints command help string

    """

    docstring = None

    def __init__(
        self,
        service: DatamodelService,
        rules: str,
        command: str,
        path: Path = None,
    ):
        self.service = service
        self.rules = rules
        self.command = command
        if path is None:
            self.path = []
        else:
            self.path = path

    def __call__(self, *args, **kwds) -> Any:
        """Executes the command

        Returns
        -------
        Any
            return value
        """
        request = DataModelProtoModule.ExecuteCommandRequest()
        request.rules = self.rules
        request.path = _convert_path_to_se_path(self.path)
        request.command = self.command
        _convert_value_to_variant(kwds, request.args)
        response = self.service.execute_command(request)
        return _convert_variant_to_value(response.result)

    def get_docstring(self):
        if self.__class__.docstring is None:
            request = DataModelProtoModule.GetSpecsRequest()
            request.rules = self.rules
            request.path = _convert_path_to_se_path(self.path)
            response = self.service.get_specs(request)
            self.__class__.docstring = getattr(
                response.member, response.member.WhichOneof("as")
            ).common.helpstring
        return self.__class__.docstring

    def help(self):
        """Prints command help string"""
        print(self.get_docstring())
