"""Wrappers over StateEngine based datamodel gRPC service of Fluent."""
from enum import Enum
import itertools
from typing import Any, Dict, Iterator, List, Tuple
import warnings

import grpc

from ansys.api.fluent.v0 import datamodel_se_pb2 as DataModelProtoModule
from ansys.api.fluent.v0 import datamodel_se_pb2_grpc as DataModelGrpcModule
from ansys.api.fluent.v0.variant_pb2 import Variant
from ansys.fluent.core.services.error_handler import catch_grpc_error
from ansys.fluent.core.services.interceptors import TracingInterceptor

Path = List[Tuple[str, str]]


class Attribute(Enum):
    """Contains the standard names of data model attributes associated with the
    data model service."""

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
    """Wraps the StateEngine-based datamodel gRPC service of Fluent.

    Using the methods from the ``PyMenu`` class is recommended.
    """

    def __init__(self, channel: grpc.Channel, metadata: List[Tuple[str, str]]):
        tracing_interceptor = TracingInterceptor()
        intercept_channel = grpc.intercept_channel(channel, tracing_interceptor)
        self.__stub = DataModelGrpcModule.DataModelStub(intercept_channel)
        self.__metadata = metadata

    @catch_grpc_error
    def initialize_datamodel(
        self, request: DataModelProtoModule.InitDatamodelRequest
    ) -> DataModelProtoModule.InitDatamodelResponse:
        return self.__stub.initDatamodel(request, metadata=self.__metadata)

    @catch_grpc_error
    def get_attribute_value(
        self, request: DataModelProtoModule.GetAttributeValueRequest
    ) -> DataModelProtoModule.GetAttributeValueResponse:
        return self.__stub.getAttributeValue(request, metadata=self.__metadata)

    @catch_grpc_error
    def get_state(
        self, request: DataModelProtoModule.GetStateRequest
    ) -> DataModelProtoModule.GetStateResponse:
        return self.__stub.getState(request, metadata=self.__metadata)

    @catch_grpc_error
    def set_state(
        self, request: DataModelProtoModule.SetStateRequest
    ) -> DataModelProtoModule.SetStateResponse:
        return self.__stub.setState(request, metadata=self.__metadata)

    @catch_grpc_error
    def update_dict(
        self, request: DataModelProtoModule.UpdateDictRequest
    ) -> DataModelProtoModule.UpdateDictResponse:
        return self.__stub.updateDict(request, metadata=self.__metadata)

    @catch_grpc_error
    def delete_object(
        self, request: DataModelProtoModule.DeleteObjectRequest
    ) -> DataModelProtoModule.DeleteObjectResponse:
        return self.__stub.deleteObject(request, metadata=self.__metadata)

    @catch_grpc_error
    def execute_command(
        self, request: DataModelProtoModule.ExecuteCommandRequest
    ) -> DataModelProtoModule.ExecuteCommandResponse:
        return self.__stub.executeCommand(request, metadata=self.__metadata)

    @catch_grpc_error
    def create_command_arguments(
        self, request: DataModelProtoModule.CreateCommandArgumentsRequest
    ) -> DataModelProtoModule.CreateCommandArgumentsResponse:
        return self.__stub.createCommandArguments(request, metadata=self.__metadata)

    @catch_grpc_error
    def delete_command_arguments(
        self, request: DataModelProtoModule.DeleteCommandArgumentsRequest
    ) -> DataModelProtoModule.DeleteCommandArgumentsResponse:
        return self.__stub.deleteCommandArguments(request, metadata=self.__metadata)

    @catch_grpc_error
    def get_specs(
        self, request: DataModelProtoModule.GetSpecsRequest
    ) -> DataModelProtoModule.GetSpecsResponse:
        return self.__stub.getSpecs(request, metadata=self.__metadata)

    @catch_grpc_error
    def get_static_info(
        self, request: DataModelProtoModule.GetStaticInfoRequest
    ) -> DataModelProtoModule.GetStaticInfoResponse:
        return self.__stub.getStaticInfo(request, metadata=self.__metadata)


def _convert_value_to_variant(val: Any, var: Variant):
    """Convert a Python data type to Fluent's variant type."""

    if isinstance(val, bool):
        var.bool_state = val
    elif isinstance(val, int):
        var.int64_state = val
    elif isinstance(val, float):
        var.double_state = val
    elif isinstance(val, str):
        var.string_state = val
    elif isinstance(val, (list, tuple)):
        # set the one_of to variant_vector_state
        var.variant_vector_state.item.add()
        var.variant_vector_state.item.pop()
        for item in val:
            item_var = var.variant_vector_state.item.add()
            _convert_value_to_variant(item, item_var)
    elif isinstance(val, dict):
        for k, v in val.items():
            _convert_value_to_variant(v, var.variant_map_state.item[k])


def _convert_variant_to_value(var: Variant):
    """Convert Fluent's variant type to a Python data type."""

    if var.HasField("bool_state"):
        return var.bool_state
    elif var.HasField("int64_state"):
        return var.int64_state
    elif var.HasField("double_state"):
        return var.double_state
    elif var.HasField("string_state"):
        return var.string_state
    elif var.HasField("bool_vector_state"):
        return var.bool_vector_state.item
    elif var.HasField("int64_vector_state"):
        return var.int64_vector_state.item
    elif var.HasField("double_vector_state"):
        return var.double_vector_state.item
    elif var.HasField("string_vector_state"):
        return var.string_vector_state.item
    elif var.HasField("variant_vector_state"):
        val = []
        for item in var.variant_vector_state.item:
            val.append(_convert_variant_to_value(item))
        return val
    elif var.HasField("variant_map_state"):
        val = {}
        for k, v in var.variant_map_state.item.items():
            val[k] = _convert_variant_to_value(v)
        return val


def _convert_path_to_se_path(path: Path) -> str:
    """Convert a path structure to a StateEngine path.

    Parameters
    ----------
    path : Path
        Path structure.

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


class PyCallableStateObject:
    """Any object which can be called to get its state.

    Methods
    -------
    __call__()
        Get the state of the current object.
    """

    def __call__(self, *args, **kwds) -> Any:
        return self.get_state()


class PyBasicStateContainer(PyCallableStateObject):
    """Object class using StateEngine based DatamodelService as backend. Use
    this class instead of directly calling DatamodelService's method.

    Methods
    -------
    get_attrib_value(attrib)
        Get the attribute value of the current object.
    getAttribValue(attrib)
        Get the attribute value of the current object.
        (This method is the same as the get_attrib_value(attrib)
        method.)
    get_state()
        Get the state of the current object. (This method is the
        same as the __call__() method.)
    getState()
        Get the state of the current object. (This method is the
        same as the __call__() method.)
    set_state(state)
        Set the state of the current object.
    setState(state)
        Set state of the current object (same as set_state(state))
    """

    def __init__(self, service: DatamodelService, rules: str, path: Path = None):
        super().__init__()
        self.service = service
        self.rules = rules
        if path is None:
            self.path = []
        else:
            self.path = path

    docstring = None

    def get_state(self) -> Any:
        request = DataModelProtoModule.GetStateRequest()
        request.rules = self.rules
        request.path = _convert_path_to_se_path(self.path)
        response = self.service.get_state(request)
        return _convert_variant_to_value(response.state)

    getState = get_state

    def set_state(self, state: Any) -> None:
        request = DataModelProtoModule.SetStateRequest()
        request.rules = self.rules
        request.path = _convert_path_to_se_path(self.path)
        _convert_value_to_variant(state, request.state)
        self.service.set_state(request)

    setState = set_state

    def get_attrib_value(self, attrib: str) -> Any:
        """Get attribute value of the current object.

        Parameters
        ----------
        attrib : str
            Name of the attribute.

        Returns
        -------
        Any
            Value of the attribute.
        """
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.rules = self.rules
        request.path = _convert_path_to_se_path(self.path)
        request.attribute = attrib
        response = self.service.get_attribute_value(request)
        return _convert_variant_to_value(response.result)

    getAttribValue = get_attrib_value

    def is_active(self):
        """Returns true if the parameter is active."""
        return true_if_none(self.get_attrib_value(Attribute.IS_ACTIVE.value))

    def help(self) -> None:
        """Print help string."""
        request = DataModelProtoModule.GetSpecsRequest()
        request.rules = self.rules
        request.path = _convert_path_to_se_path(self.path)
        response = self.service.get_specs(request)
        help_string = getattr(
            response.member, response.member.WhichOneof("as")
        ).common.helpstring
        print(help_string)


class PyMenu(PyBasicStateContainer):
    """Object class using StateEngine based DatamodelService as backend. Use
    this class instead of directly calling DatamodelService's method.

    Methods
    -------
    __setattr__(name, value)
        Set state of the child object
    create_command_arguments(command)
    """

    def __init__(self, service: DatamodelService, rules: str, path: Path = None):
        super().__init__(service, rules, path)

    def __setattr__(self, name: str, value: Any):
        """Set state of the child object.

        Parameters
        ----------
        name : str
            child object name
        value : Any
            state
        """
        if hasattr(self, name) and isinstance(
            getattr(self, name), PyBasicStateContainer
        ):
            getattr(self, name).set_state(value)
        else:
            super().__setattr__(name, value)

    def rename(self, new_name: str) -> None:
        """Rename the named object.

        Parameters
        ----------
        new_name : str
            New name for the object.
        """
        try:
            self._name_.set_state(new_name)
        except AttributeError:
            raise RuntimeError(
                f"{self.__class__.__name__} is not a named object class."
            )

    def create_command_arguments(self, command):
        request = DataModelProtoModule.CreateCommandArgumentsRequest()
        request.rules = self.rules
        request.path = _convert_path_to_se_path(self.path)
        request.command = command
        response = self.service.create_command_arguments(request)
        return response.commandid


class PyParameter(PyBasicStateContainer):
    """Object class using StateEngine based DatamodelService as backend.

    Use this class instead of directly calling DatamodelService's
    method.
    """

    def default_value(self):
        """Get default value of the parameter."""
        return self.get_attrib_value(Attribute.DEFAULT.value)

    def is_read_only(self):
        return true_if_none(self.get_attrib_value(Attribute.IS_READ_ONLY.value))


def true_if_none(val):
    """Returns true if 'val' is true or None, else returns false."""
    if val in [True, False, None]:
        return True if val is None else val
    else:
        raise RuntimeError(f"In-correct value passed")


class PyTextual(PyParameter):
    """Provides interface for textual parameters."""

    def allowed_values(self):
        return self.get_attrib_value(Attribute.ALLOWED_VALUES.value)


class PyNumerical(PyParameter):
    """Provides interface for numerical parameters."""

    def min(self):
        return self.get_attrib_value(Attribute.MIN.value)

    def max(self):
        return self.get_attrib_value(Attribute.MAX.value)


class PyDictionary(PyParameter):
    """Provides interface for dictionaries.
    Methods
        -------
        update_dict(dict_state)
            Update the state of the current object if the current object
            is a Dict in the data model, else throws RuntimeError
            (currently not showing up in Python). Update is executed according
            to dict.update semantics
        updateDict(dict_state)
            Update the state of the current object if the current object
            is a Dict in the data model, else throws RuntimeError
            (currently not showing up in Python). Update is executed according
            to dict.update semantics (same as update_dict(dict_state))
    """

    def update_dict(self, dict_state: Dict[str, Any]) -> None:
        request = DataModelProtoModule.UpdateDictRequest()
        request.rules = self.rules
        request.path = _convert_path_to_se_path(self.path)
        _convert_value_to_variant(dict_state, request.dicttomerge)
        self.service.update_dict(request)

    updateDict = update_dict


class PyNamedObjectContainer:
    """Container class using the StateEngine-based DatamodelService as the
    backend. Use this class instead of directly calling the DatamodelService's
    method.

    Methods
    -------
    __len__()
        Return a count of the child objects.
    __iter__()
        Return the next child object.
    __getitem__(key)
        Return the child object by key.
    __setitem__(key, value)
        Set the state of the child object by name.
    __delitem__(key)
        Delete the child object by name.
    """

    def __init__(self, service: DatamodelService, rules: str, path: Path = None):
        self.service = service
        self.rules = rules
        if path is None:
            self.path = []
        else:
            self.path = path

    def _get_child_object_names(self):
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
                        child_object_names.append(member[len(child_type_suffix) :])
        return child_object_names

    def _get_child_object_display_names(self):
        child_object_display_names = []
        for name in self._get_child_object_names():
            name_path = self.path[0:-1]
            name_path.append((self.path[-1][0], name))
            name_path.append(("_name_", ""))
            child_object_display_names.append(
                PyMenu(self.service, self.rules, name_path).get_state()
            )
        return child_object_display_names

    def __len__(self) -> int:
        """Return a count of child objects.

        Returns
        -------
        int
            Count of child objects.
        """
        return len(self._get_child_object_display_names())

    def __iter__(self) -> Iterator[PyMenu]:
        """Return the next child object.

        Yields
        -------
        Iterator[PyMenu]
            Iterator of child objects.
        """
        for name in self._get_child_object_display_names():
            child_path = self.path[:-1]
            child_path.append((self.path[-1][0], name))
            yield getattr(self.__class__, f"_{self.__class__.__name__}")(
                self.service, self.rules, child_path
            )

    def _get_item(self, key: str):
        if key in self._get_child_object_display_names():
            child_path = self.path[:-1]
            child_path.append((self.path[-1][0], key))
            return getattr(self.__class__, f"_{self.__class__.__name__}")(
                self.service, self.rules, child_path
            )
        else:
            raise LookupError(
                f"{key} is not found at path " f"{_convert_path_to_se_path(self.path)}"
            )

    def _del_item(self, key: str):
        if key in self._get_child_object_display_names():
            child_path = self.path[:-1]
            child_path.append((self.path[-1][0], key))
            request = DataModelProtoModule.DeleteObjectRequest()
            request.rules = self.rules
            request.path = _convert_path_to_se_path(child_path)
            self.service.delete_object(request)
        else:
            raise LookupError(
                f"{key} is not found at path " f"{_convert_path_to_se_path(self.path)}"
            )

    def __getitem__(self, key: str) -> PyMenu:
        """Return the child object by key.

        Parameters
        ----------
        key : str
            Name of the child object.

        Returns
        -------
        PyMenu
            Child object.
        """
        return self._get_item(key)

    def __setitem__(self, key: str, value: Any):
        """Set state of the child object by name.

        Parameters
        ----------
        key : str
            Name of the child object.
        value : Any
            State of the child object.
        """
        if isinstance(value, dict) and not value:
            value["_name_"] = key
        parent_state = {f"{self.__class__.__name__}:{key}": value}
        PyMenu(self.service, self.rules, self.path[:-1]).set_state(parent_state)

    def __delitem__(self, key: str):
        """Delete the child object by name.

        Parameters
        ----------
        key : str
            Name of the child object.
        """
        self._del_item(key)


class PyCommand:
    """Command class using the StateEngine-based DatamodelService as the
    backend. Use this class instead of directly calling the DatamodelService's
    method.

    Methods
    -------
    __call__()
        Execute the command.
    help()
        Print the command help string.
    """

    docstring = None

    def __init__(
        self, service: DatamodelService, rules: str, command: str, path: Path = None
    ):
        self.service = service
        self.rules = rules
        self.command = command
        if path is None:
            self.path = []
        else:
            self.path = path

    def __call__(self, *args, **kwds) -> Any:
        """Execute the command.

        Returns
        -------
        Any
            Return value.
        """
        request = DataModelProtoModule.ExecuteCommandRequest()
        request.rules = self.rules
        request.path = _convert_path_to_se_path(self.path)
        request.command = self.command
        request.wait = True
        _convert_value_to_variant(kwds, request.args)
        response = self.service.execute_command(request)
        return _convert_variant_to_value(response.result)

    def help(self) -> None:
        """Prints help string."""
        request = DataModelProtoModule.GetSpecsRequest()
        request.rules = self.rules
        request.path = _convert_path_to_se_path(self.path)
        response = self.service.get_specs(request)
        help_string = getattr(
            response.member, response.member.WhichOneof("as")
        ).common.helpstring
        print(help_string)

    def _create_command_arguments(self):
        request = DataModelProtoModule.CreateCommandArgumentsRequest()
        request.rules = self.rules
        request.path = _convert_path_to_se_path(self.path)
        request.command = self.command
        response = self.service.create_command_arguments(request)
        return response.commandid

    def new(self):
        try:
            id = self._create_command_arguments()
            return PyCommandArguments(
                self.service, self.rules, self.command, self.path.copy(), id
            )
        except RuntimeError:
            warnings.warn(
                "Create command arguments object is available from 23.1 onwards"
            )
            pass


class PyCommandArgumentsSubItem(PyCallableStateObject):
    def __init__(self, parent, name: str):
        self.parent = parent
        self.name = name

    def __getattr__(self, attr):
        return PyCommandArgumentsSubItem(self, attr)

    def get_state(self) -> Any:
        parent_state = self.parent.get_state()
        try:
            return parent_state[self.name]
        except KeyError:
            pass

    getState = get_state

    def set_state(self, state: Any) -> None:
        self.parent.set_state({self.name: state})

    setState = set_state

    def get_attrib_value(self, attrib: str) -> Any:
        attrib_path = f"{self.name}/{attrib}"
        return self.parent.get_attrib_value(attrib_path)

    getAttribValue = get_attrib_value

    def help(self) -> None:
        pass


class PyCommandArguments(PyBasicStateContainer):
    def __init__(
        self, service: DatamodelService, rules: str, command: str, path: Path, id: str
    ):
        super().__init__(service, rules, path)
        self.path.append((command, id))

    def __del__(self):
        request = DataModelProtoModule.DeleteCommandArgumentsRequest()
        request.rules = self.rules
        request.path = _convert_path_to_se_path(self.path[:-1])
        request.command = self.path[-1][0]
        request.commandid = self.path[-1][1]
        try:
            self.service.delete_command_arguments(request)
        except ValueError:
            # "Cannot invoke RPC on closed channel!"
            pass

    def __getattr__(self, attr):
        return PyCommandArgumentsSubItem(self, attr)


class PyMenuGeneric(PyMenu):
    attrs = ("service", "rules", "path")

    def _get_child_names(self):
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
                        singleton_names.append(member)
                creatable_type_names = struct_field.creatabletypes
                command_names = [x.name for x in struct_field.commands]
        return singleton_names, creatable_type_names, command_names

    def _get_child(self, name: str):
        singletons, creatable_types, commands = self._get_child_names()
        if name in singletons:
            child_path = self.path + [(name, "")]
            return PyMenuGeneric(self.service, self.rules, child_path)
        elif name in creatable_types:
            child_path = self.path + [(name, "")]
            return PyNamedObjectContainerGeneric(self.service, self.rules, child_path)
        elif name in commands:
            return PyCommand(self.service, self.rules, name, self.path)
        else:
            raise LookupError(
                f"{name} is not found at path " f"{_convert_path_to_se_path(self.path)}"
            )

    def __dir__(self):
        return list(itertools.chain(*self._get_child_names()))

    def __getattr__(self, name: str):
        if name in PyMenuGeneric.attrs:
            return super().__getattr__(name)
        else:
            return self._get_child(name)


class PyNamedObjectContainerGeneric(PyNamedObjectContainer):
    def __iter__(self):
        for name in self._get_child_object_display_names():
            child_path = self.path[:-1]
            child_path.append((self.path[-1][0], name))
            yield PyMenuGeneric(self.service, self.rules, child_path)

    def _get_item(self, key: str):
        if key in self._get_child_object_display_names():
            child_path = self.path[:-1]
            child_path.append((self.path[-1][0], key))
            return PyMenuGeneric(self.service, self.rules, child_path)
        else:
            raise LookupError(
                f"{key} is not found at path " f"{_convert_path_to_se_path(self.path)}"
            )
