"""Wrappers over StateEngine based datamodel gRPC service of Fluent."""
from enum import Enum
import functools
import itertools
import logging
from typing import Any, Callable, Dict, Iterator, List, Tuple, Type
import warnings

import grpc

from ansys.api.fluent.v0 import datamodel_se_pb2 as DataModelProtoModule
from ansys.api.fluent.v0 import datamodel_se_pb2_grpc as DataModelGrpcModule
from ansys.api.fluent.v0.variant_pb2 import Variant
import ansys.fluent.core as pyfluent
from ansys.fluent.core.data_model_cache import DataModelCache
from ansys.fluent.core.services.error_handler import catch_grpc_error
from ansys.fluent.core.services.interceptors import BatchInterceptor, TracingInterceptor
from ansys.fluent.core.services.streaming import StreamingService

Path = List[Tuple[str, str]]

logger = logging.getLogger("ansys.fluent.services.datamodel")


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


class DatamodelService(StreamingService):
    """Wraps the StateEngine-based datamodel gRPC service of Fluent.

    Using the methods from the ``PyMenu`` class is recommended.
    """

    def __init__(self, channel: grpc.Channel, metadata: List[Tuple[str, str]]):
        """__init__ method of DatamodelService class."""
        intercept_channel = grpc.intercept_channel(
            channel, TracingInterceptor(), BatchInterceptor()
        )
        self._stub = DataModelGrpcModule.DataModelStub(intercept_channel)
        self._metadata = metadata
        super().__init__(
            stub=self._stub,
            request=DataModelProtoModule.EventRequest(),
            metadata=metadata,
        )
        self.event_streaming = None
        self.events = {}

    @catch_grpc_error
    def initialize_datamodel(
        self, request: DataModelProtoModule.InitDatamodelRequest
    ) -> DataModelProtoModule.InitDatamodelResponse:
        """initDatamodel rpc of DataModel service."""
        return self._stub.initDatamodel(request, metadata=self._metadata)

    @catch_grpc_error
    def get_attribute_value(
        self, request: DataModelProtoModule.GetAttributeValueRequest
    ) -> DataModelProtoModule.GetAttributeValueResponse:
        """getAttributeValue rpc of DataModel service."""
        return self._stub.getAttributeValue(request, metadata=self._metadata)

    @catch_grpc_error
    def get_state(
        self, request: DataModelProtoModule.GetStateRequest
    ) -> DataModelProtoModule.GetStateResponse:
        """getState rpc of DataModel service."""
        return self._stub.getState(request, metadata=self._metadata)

    @catch_grpc_error
    def set_state(
        self, request: DataModelProtoModule.SetStateRequest
    ) -> DataModelProtoModule.SetStateResponse:
        """setState rpc of DataModel service."""
        return self._stub.setState(request, metadata=self._metadata)

    @catch_grpc_error
    def update_dict(
        self, request: DataModelProtoModule.UpdateDictRequest
    ) -> DataModelProtoModule.UpdateDictResponse:
        """updateDict rpc of DataModel service."""
        return self._stub.updateDict(request, metadata=self._metadata)

    @catch_grpc_error
    def delete_object(
        self, request: DataModelProtoModule.DeleteObjectRequest
    ) -> DataModelProtoModule.DeleteObjectResponse:
        """deleteObject rpc of DataModel service."""
        return self._stub.deleteObject(request, metadata=self._metadata)

    @catch_grpc_error
    def execute_command(
        self, request: DataModelProtoModule.ExecuteCommandRequest
    ) -> DataModelProtoModule.ExecuteCommandResponse:
        """executeCommand rpc of DataModel service."""
        logger.debug(f"Command: {request.command}")
        return self._stub.executeCommand(request, metadata=self._metadata)

    @catch_grpc_error
    def create_command_arguments(
        self, request: DataModelProtoModule.CreateCommandArgumentsRequest
    ) -> DataModelProtoModule.CreateCommandArgumentsResponse:
        """createCommandArguments rpc of DataModel service."""
        return self._stub.createCommandArguments(request, metadata=self._metadata)

    @catch_grpc_error
    def delete_command_arguments(
        self, request: DataModelProtoModule.DeleteCommandArgumentsRequest
    ) -> DataModelProtoModule.DeleteCommandArgumentsResponse:
        """deleteCommandArguments rpc of DataModel service."""
        return self._stub.deleteCommandArguments(request, metadata=self._metadata)

    @catch_grpc_error
    def get_specs(
        self, request: DataModelProtoModule.GetSpecsRequest
    ) -> DataModelProtoModule.GetSpecsResponse:
        """getSpecs rpc of DataModel service."""
        return self._stub.getSpecs(request, metadata=self._metadata)

    @catch_grpc_error
    def get_static_info(
        self, request: DataModelProtoModule.GetStaticInfoRequest
    ) -> DataModelProtoModule.GetStaticInfoResponse:
        """getStaticInfo rpc of DataModel service."""
        return self._stub.getStaticInfo(request, metadata=self._metadata)

    @catch_grpc_error
    def subscribe_events(
        self, request: DataModelProtoModule.SubscribeEventsRequest
    ) -> DataModelProtoModule.SubscribeEventsResponse:
        """subscribeEvents rpc of DataModel service."""
        return self._stub.subscribeEvents(request, metadata=self._metadata)

    @catch_grpc_error
    def unsubscribe_events(
        self, request: DataModelProtoModule.UnsubscribeEventsRequest
    ) -> DataModelProtoModule.UnsubscribeEventsResponse:
        """unsubscribeEvents rpc of DataModel service."""
        return self._stub.unsubscribeEvents(request, metadata=self._metadata)

    def begin_event_streaming(self, started_evt):
        """Begin datamodel event streaming."""
        self._streams = self._stub.BeginEventStreaming(
            self.request, metadata=self._metadata
        )
        started_evt.set()
        while True:
            try:
                yield next(self._streams)
            except Exception:
                break

    def unsubscribe_all_events(self):
        """Unsubscribe all subscribed events."""
        for event in list(self.events.values()):
            event.unsubscribe()
        self.events.clear()


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


def convert_path_to_se_path(path: Path) -> str:
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


class EventSubscription:
    """EventSubscription class for any datamodel event."""

    def __init__(
        self,
        service: DatamodelService,
        request: DataModelProtoModule.SubscribeEventsRequest,
    ):
        """Subscribe to a datamodel event."""
        self._service = service
        response = service.subscribe_events(request)
        response = response.response[0]
        if response.status != DataModelProtoModule.STATUS_SUBSCRIBED:
            raise RuntimeError(f"Failed to subscribe event: {request}!")
        self.status = response.status
        self.tag = response.tag
        self._service.events[self.tag] = self

    def unsubscribe(self):
        """Unsubscribe the datamodel event."""
        if self.status == DataModelProtoModule.STATUS_SUBSCRIBED:
            self._service.event_streaming.unregister_callback(self.tag)
            request = DataModelProtoModule.UnsubscribeEventsRequest()
            request.tag.append(self.tag)
            response = self._service.unsubscribe_events(request)
            response = response.response[0]
            if response.status != DataModelProtoModule.STATUS_UNSUBSCRIBED:
                raise RuntimeError(f"Failed to unsubscribe event: {request}!")
            self.status = response.status
        self._service.events.pop(self.tag, None)

    def __del__(self):
        """Unsubscribe the datamodel event."""
        self.unsubscribe()


class PyStateContainer(PyCallableStateObject):
    """Object class using StateEngine based DatamodelService as backend. Use
    this class instead of directly calling DatamodelService's method.

    Methods
    -------
    get_attr(attrib)
        Get the attribute value of the current object.
    getAttribValue(attrib)
        Get the attribute value of the current object.
        (This method is the same as the get_attr(attrib)
        method.)
    get_state()
        Get the state of the current object.
    getState()
        Deprecated camel case alias of get_state.
    set_state()
        Set the state of the current object.
    setState()
        Deprecated camel case alias of set_state.
    __call__()
        Set the state of the current object if state is provided else get its state.
    """

    def __init__(self, service: DatamodelService, rules: str, path: Path = None):
        """__init__ method of PyStateContainer class."""
        super().__init__()
        self.service = service
        self.rules = rules
        if path is None:
            self.path = []
        else:
            self.path = path
        self.cached_attrs = {}

    docstring = None

    def get_remote_state(self) -> Any:
        """Get state of the current object."""
        request = DataModelProtoModule.GetStateRequest()
        request.rules = self.rules
        request.path = convert_path_to_se_path(self.path)
        response = self.service.get_state(request)
        return _convert_variant_to_value(response.state)

    def get_state(self) -> Any:
        state = DataModelCache.get_state(self.rules, self)
        if DataModelCache.is_unassigned(state):
            state = self.get_remote_state()
        return state

    getState = get_state

    def set_state(self, state: Any = None, **kwargs) -> None:
        """Set state of the current object."""
        request = DataModelProtoModule.SetStateRequest()
        request.rules = self.rules
        request.path = convert_path_to_se_path(self.path)
        _convert_value_to_variant(
            kwargs, request.state
        ) if kwargs else _convert_value_to_variant(state, request.state)
        self.service.set_state(request)

    setState = set_state

    def _get_remote_attr(self, attrib: str) -> Any:
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.rules = self.rules
        request.path = convert_path_to_se_path(self.path)
        request.attribute = attrib
        response = self.service.get_attribute_value(request)
        return _convert_variant_to_value(response.result)

    def _get_cached_attr(self, attrib: str) -> Any:
        cached_val = self.cached_attrs.get(attrib)
        if cached_val is None:
            cached_val = self._get_remote_attr(attrib)
            try:  # will fail for Fluent 23.1 or before
                self.add_on_attribute_changed(
                    attrib,
                    functools.partial(dict.__setitem__, self.cached_attrs, attrib),
                )
                self.cached_attrs[attrib] = cached_val
            except Exception:
                pass
        return cached_val

    def get_attr(self, attrib: str) -> Any:
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
        if pyfluent.DATAMODEL_USE_ATTR_CACHE:
            return self._get_cached_attr(attrib)
        return self._get_remote_attr(attrib)

    getAttribValue = get_attr

    def is_active(self):
        """Returns true if the object is active."""
        return true_if_none(self.get_attr(Attribute.IS_ACTIVE.value))

    def is_read_only(self):
        """Checks whether the object is read only."""
        return false_if_none(self.get_attr(Attribute.IS_READ_ONLY.value))

    def help(self) -> None:
        """Print help string."""
        request = DataModelProtoModule.GetSpecsRequest()
        request.rules = self.rules
        request.path = convert_path_to_se_path(self.path)
        response = self.service.get_specs(request)
        help_string = getattr(
            response.member, response.member.WhichOneof("as")
        ).common.helpstring
        print(help_string)

    def __call__(self, *args, **kwargs):
        if kwargs:
            self.set_state(kwargs)
        elif args:
            self.set_state(args)
        else:
            return self.get_state()

    docstring = None

    def add_on_attribute_changed(
        self, attribute: str, cb: Callable
    ) -> EventSubscription:
        """Register a callback for when an attribute is changed

        Parameters
        ----------
        attribute : str
            attribute name
        cb : Callable
            Callback function

        Returns
        -------
        EventSubscription
            EventSubscription instance which can be used to unregister the callback
        """
        request = DataModelProtoModule.SubscribeEventsRequest()
        e = request.eventrequest.add(rules=self.rules)
        e.attributeChangedEventRequest.path = convert_path_to_se_path(self.path)
        e.attributeChangedEventRequest.attribute = attribute
        subscription = EventSubscription(self.service, request)
        self.service.event_streaming.register_callback(subscription.tag, self, cb)
        return subscription

    def add_on_command_attribute_changed(
        self, command: str, attribute: str, cb: Callable
    ) -> EventSubscription:
        """Register a callback for when an attribute is changed

        Parameters
        ----------
        command : str
            command name
        attribute : str
            attribute name
        cb : Callable
            Callback function

        Returns
        -------
        EventSubscription
            EventSubscription instance which can be used to unregister the callback
        """
        request = DataModelProtoModule.SubscribeEventsRequest()
        e = request.eventrequest.add(rules=self.rules)
        e.commandAttributeChangedEventRequest.path = convert_path_to_se_path(self.path)
        e.commandAttributeChangedEventRequest.command = command
        e.commandAttributeChangedEventRequest.attribute = attribute
        subscription = EventSubscription(self.service, request)
        self.service.event_streaming.register_callback(subscription.tag, self, cb)
        return subscription


class PyMenu(PyStateContainer):
    """Object class using StateEngine based DatamodelService as backend. Use
    this class instead of directly calling DatamodelService's method.

    Methods
    -------
    __setattr__(name, value)
        Set state of the child object
    rename(new_name)
    name()
    create_command_arguments(command)
    """

    def __init__(self, service: DatamodelService, rules: str, path: Path = None):
        """__init__ method of PyMenu class."""
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
        if hasattr(self, name) and isinstance(getattr(self, name), PyStateContainer):
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

    def name(self):
        """Get the name of the named object."""
        try:
            return self._name_()
        except AttributeError:
            raise RuntimeError(
                f"{self.__class__.__name__} is not a named object class."
            )

    def _raise_method_not_yet_implemented_exception(self):
        raise AttributeError("This method is yet to be implemented in pyfluent.")

    def delete_child(self):
        self._raise_method_not_yet_implemented_exception()

    def delete_child_objects(self):
        self._raise_method_not_yet_implemented_exception()

    def delete_all_child_objects(self):
        self._raise_method_not_yet_implemented_exception()

    def fix_state(self):
        self._raise_method_not_yet_implemented_exception()

    def create_command_arguments(self, command: str) -> str:
        """Create command arguments.

        Parameters
        ----------
        command : str
            Command name

        Returns
        -------
        str
            Command id
        """
        request = DataModelProtoModule.CreateCommandArgumentsRequest()
        request.rules = self.rules
        request.path = convert_path_to_se_path(self.path)
        request.command = command
        response = self.service.create_command_arguments(request)
        return response.commandid

    def add_on_child_created(self, child_type: str, cb: Callable) -> EventSubscription:
        """Register a callback for when a child object is created.

        Parameters
        ----------
        child_type : str
            Type of the child object
        cb : Callable
            Callback function

        Returns
        -------
        EventSubscription
            EventSubscription instance which can be used to unregister the callback
        """
        request = DataModelProtoModule.SubscribeEventsRequest()
        e = request.eventrequest.add(rules=self.rules)
        e.createdEventRequest.parentpath = convert_path_to_se_path(self.path)
        e.createdEventRequest.childtype = child_type
        subscription = EventSubscription(self.service, request)
        self.service.event_streaming.register_callback(subscription.tag, self, cb)
        return subscription

    def add_on_deleted(self, cb: Callable) -> EventSubscription:
        """Register a callback for when the object is deleted.

        Parameters
        ----------
        cb : Callable
            Callback function

        Returns
        -------
        EventSubscription
            EventSubscription instance which can be used to unregister the callback
        """
        request = DataModelProtoModule.SubscribeEventsRequest()
        e = request.eventrequest.add(rules=self.rules)
        e.deletedEventRequest.path = convert_path_to_se_path(self.path)
        subscription = EventSubscription(self.service, request)
        self.service.event_streaming.register_callback(subscription.tag, self, cb)
        return subscription

    def add_on_changed(self, cb: Callable) -> EventSubscription:
        """Register a callback for when the object is modified.

        Parameters
        ----------
        cb : Callable
            Callback function

        Returns
        -------
        EventSubscription
            EventSubscription instance which can be used to unregister the callback
        """
        request = DataModelProtoModule.SubscribeEventsRequest()
        e = request.eventrequest.add(rules=self.rules)
        e.modifiedEventRequest.path = convert_path_to_se_path(self.path)
        subscription = EventSubscription(self.service, request)
        self.service.event_streaming.register_callback(subscription.tag, self, cb)
        return subscription

    def add_on_affected(self, cb: Callable) -> EventSubscription:
        """Register a callback for when the object is affected.

        Parameters
        ----------
        cb : Callable
            Callback function

        Returns
        -------
        EventSubscription
            EventSubscription instance which can be used to unregister the callback
        """
        request = DataModelProtoModule.SubscribeEventsRequest()
        e = request.eventrequest.add(rules=self.rules)
        e.affectedEventRequest.path = convert_path_to_se_path(self.path)
        subscription = EventSubscription(self.service, request)
        self.service.event_streaming.register_callback(subscription.tag, self, cb)
        return subscription

    def add_on_affected_at_type_path(
        self, child_type: str, cb: Callable
    ) -> EventSubscription:
        """Register a callback for when the object is affected at child type

        Parameters
        ----------
        child_type : str
            child type
        cb : Callable
            Callback function

        Returns
        -------
        EventSubscription
            EventSubscription instance which can be used to unregister the callback
        """
        request = DataModelProtoModule.SubscribeEventsRequest()
        e = request.eventrequest.add(rules=self.rules)
        e.affectedEventRequest.path = convert_path_to_se_path(self.path)
        e.affectedEventRequest.subtype = child_type
        subscription = EventSubscription(self.service, request)
        self.service.event_streaming.register_callback(subscription.tag, self, cb)
        return subscription

    def add_on_command_executed(self, command: str, cb: Callable) -> EventSubscription:
        """Register a callback for when a command is executed

        Parameters
        ----------
        command : str
            command name
        cb : Callable
            Callback function

        Returns
        -------
        EventSubscription
            EventSubscription instance which can be used to unregister the callback
        """
        request = DataModelProtoModule.SubscribeEventsRequest()
        e = request.eventrequest.add(rules=self.rules)
        e.commandExecutedEventRequest.path = convert_path_to_se_path(self.path)
        e.commandExecutedEventRequest.command = command
        subscription = EventSubscription(self.service, request)
        self.service.event_streaming.register_callback(subscription.tag, self, cb)
        return subscription


class PyParameter(PyStateContainer):
    """Object class using StateEngine based DatamodelService as backend.

    Use this class instead of directly calling DatamodelService's
    method.
    """

    def default_value(self):
        """Get default value of the parameter."""
        return self.get_attr(Attribute.DEFAULT.value)

    def add_on_changed(self, cb: Callable) -> EventSubscription:
        """Register a callback for when the object is modified.

        Parameters
        ----------
        cb : Callable
            Callback function

        Returns
        -------
        EventSubscription
            EventSubscription instance which can be used to unregister the callback
        """
        request = DataModelProtoModule.SubscribeEventsRequest()
        e = request.eventrequest.add(rules=self.rules)
        e.modifiedEventRequest.path = convert_path_to_se_path(self.path)
        subscription = EventSubscription(self.service, request)
        self.service.event_streaming.register_callback(subscription.tag, self, cb)
        return subscription


def _bool_value_if_none(val, default):
    if isinstance(val, bool) or val is None:
        return default if val is None else val
    raise TypeError(f"{val} should be a bool or None")


def true_if_none(val):
    """Returns true if 'val' is true or None, else returns false."""
    return _bool_value_if_none(val, default=True)


def false_if_none(val):
    """Returns true if 'val' is true or None, else returns false."""
    return _bool_value_if_none(val, default=False)


class PyTextual(PyParameter):
    """Provides interface for textual parameters."""

    def allowed_values(self):
        return self.get_attr(Attribute.ALLOWED_VALUES.value)


class PyNumerical(PyParameter):
    """Provides interface for numerical parameters."""

    def min(self):
        """Minimum value of the numerical parameter."""
        return self.get_attr(Attribute.MIN.value)

    def max(self):
        """Maximum value of the numerical parameter."""
        return self.get_attr(Attribute.MAX.value)


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
        to dict.update semantics (same as update_dict(dict_state))]
    """

    def update_dict(self, dict_state: Dict[str, Any]) -> None:
        """Update the state of the current object if the current object
        is a Dict in the data model, else throws RuntimeError
        (currently not showing up in Python). Update is executed according
        to dict.update semantics.

        Parameters
        ----------
        dict_state : Dict[str, Any]
            Incoming dict state
        """
        request = DataModelProtoModule.UpdateDictRequest()
        request.rules = self.rules
        request.path = convert_path_to_se_path(self.path)
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
        """__init__ method of PyNamedObjectContainer class."""
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
        request.path = convert_path_to_se_path(parent_path)
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

    def get_object_names(self):
        return self._get_child_object_display_names()

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
                f"{key} is not found at path " f"{convert_path_to_se_path(self.path)}"
            )

    def _del_item(self, key: str):
        if key in self._get_child_object_display_names():
            child_path = self.path[:-1]
            child_path.append((self.path[-1][0], key))
            request = DataModelProtoModule.DeleteObjectRequest()
            request.rules = self.rules
            request.path = convert_path_to_se_path(child_path)
            self.service.delete_object(request)
        else:
            raise LookupError(
                f"{key} is not found at path " f"{convert_path_to_se_path(self.path)}"
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
    _stored_static_info = {}

    def __init__(
        self, service: DatamodelService, rules: str, command: str, path: Path = None
    ):
        """__init__ method of PyCommand class."""
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
        request.path = convert_path_to_se_path(self.path)
        request.command = self.command
        request.wait = True
        _convert_value_to_variant(kwds, request.args)
        response = self.service.execute_command(request)
        return _convert_variant_to_value(response.result)

    def help(self) -> None:
        """Prints help string."""
        request = DataModelProtoModule.GetSpecsRequest()
        request.rules = self.rules
        request.path = convert_path_to_se_path(self.path)
        response = self.service.get_specs(request)
        help_string = getattr(
            response.member, response.member.WhichOneof("as")
        ).common.helpstring
        print(help_string)

    def _create_command_arguments(self):
        request = DataModelProtoModule.CreateCommandArgumentsRequest()
        request.rules = self.rules
        request.path = convert_path_to_se_path(self.path)
        request.command = self.command
        response = self.service.create_command_arguments(request)
        return response.commandid

    def _get_static_info(self):
        if self.rules not in PyCommand._stored_static_info.keys():
            # Populate the static info with respect to a rules only if the
            # same info has not been obtained in another context already.
            # If the information is available, we can use it without additional remote calls.
            request = DataModelProtoModule.GetStaticInfoRequest()
            request.rules = self.rules
            response = self.service.get_static_info(request)
            PyCommand._stored_static_info[self.rules] = response.info
        return PyCommand._stored_static_info[self.rules]

    def create_instance(self):
        """Create a command instance."""
        try:
            static_info = self._get_static_info()
            id = self._create_command_arguments()
            return PyCommandArguments(
                self.service,
                self.rules,
                self.command,
                self.path.copy(),
                id,
                static_info,
            )
        except RuntimeError:
            warnings.warn(
                "Create command arguments object is available from 23.1 onwards"
            )
            pass


class PyCommandArgumentsSubItem(PyCallableStateObject):
    """Class representing command argument in datamodel."""

    def __init__(
        self,
        parent,
        name: str,
        service: DatamodelService,
        rules: str,
        path: Path,
        parent_arg,
    ):
        """__init__ method of PyCommandArgumentsSubItem class."""
        self.parent = parent
        self.name = name

        self.service = service
        self.rules = rules
        self.path = path
        self.parent_arg = parent_arg

    def get_state(self) -> Any:
        """Get state of the command argument."""
        parent_state = self.parent.get_state()
        try:
            return parent_state[self.name]
        except KeyError:
            pass

    getState = get_state

    def get_attr(self, attrib: str) -> Any:
        """Get attribute value of the command argument.

        Parameters
        ----------
        attrib : str
            attribute name

        Returns
        -------
        Any
            attribute value
        """
        attrib_path = f"{self.name}/{attrib}"
        return self.parent.get_attr(attrib_path)

    getAttribValue = get_attr

    def help(self) -> None:
        pass


class PyCommandArguments(PyStateContainer):
    """Class representing command arguments in datamodel."""

    def __init__(
        self,
        service: DatamodelService,
        rules: str,
        command: str,
        path: Path,
        id: str,
        static_info,
    ):
        """__init__ method of PyCommandArguments class."""
        self.static_info = static_info
        super().__init__(service, rules, path)
        self.path.append((command, id))
        self.command = command
        self.id = id

    def __del__(self):
        request = DataModelProtoModule.DeleteCommandArgumentsRequest()
        request.rules = self.rules
        request.path = convert_path_to_se_path(self.path[:-1])
        request.command = self.path[-1][0]
        request.commandid = self.path[-1][1]
        try:
            self.service.delete_command_arguments(request)
        except ValueError:
            # "Cannot invoke RPC on closed channel!"
            pass

    def __getattr__(self, attr):
        for arg in self.static_info.commands[self.command].commandinfo.args:
            if arg.name == attr:
                mode = DataModelType.get_mode(arg.type)
                py_class = mode.value[1]
                return py_class(self, attr, self.service, self.rules, self.path, arg)

    def get_attr(self, attrib: str) -> Any:
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
        return self._get_remote_attr(attrib)


class PyTextualCommandArgumentsSubItem(PyCommandArgumentsSubItem, PyTextual):
    """Class representing textual command argument in datamodel."""

    def __init__(
        self,
        parent,
        attr,
        service: DatamodelService,
        rules: str,
        path: Path,
        arg,
    ):
        """__init__ method of PyTextualCommandArgumentsSubItem class."""
        PyCommandArgumentsSubItem.__init__(
            self, parent, attr, service, rules, path, arg
        )
        PyTextual.__init__(self, service, rules, path)


class PyNumericalCommandArgumentsSubItem(PyCommandArgumentsSubItem, PyNumerical):
    """Class representing numerical command argument in datamodel."""

    def __init__(
        self,
        parent,
        attr,
        service: DatamodelService,
        rules: str,
        path: Path,
        arg,
    ):
        """__init__ method of PyNumericalCommandArgumentsSubItem class."""
        PyCommandArgumentsSubItem.__init__(
            self, parent, attr, service, rules, path, arg
        )
        PyNumerical.__init__(self, service, rules, path)


class PyDictionaryCommandArgumentsSubItem(PyCommandArgumentsSubItem, PyDictionary):
    """Class representing dictionary-like command argument in datamodel."""

    def __init__(
        self,
        parent,
        attr,
        service: DatamodelService,
        rules: str,
        path: Path,
        arg,
    ):
        """__init__ method of PyDictionaryCommandArgumentsSubItem class."""
        PyCommandArgumentsSubItem.__init__(
            self, parent, attr, service, rules, path, arg
        )
        PyDictionary.__init__(self, service, rules, path)


class PyParameterCommandArgumentsSubItem(PyCommandArgumentsSubItem, PyParameter):
    """Class representing generic parameter-like command argument in datamodel."""

    def __init__(
        self,
        parent,
        attr,
        service: DatamodelService,
        rules: str,
        path: Path,
        arg,
    ):
        """__init__ method of PyParameterCommandArgumentsSubItem class."""
        PyCommandArgumentsSubItem.__init__(
            self, parent, attr, service, rules, path, arg
        )
        PyParameter.__init__(self, service, rules, path)


class PySingletonCommandArgumentsSubItem(PyCommandArgumentsSubItem):
    """Class representing singleton-like command argument in datamodel."""

    def __init__(
        self,
        parent,
        attr,
        service: DatamodelService,
        rules: str,
        path: Path,
        arg,
    ):
        """__init__ method of PySingletonCommandArgumentsSubItem class."""
        PyCommandArgumentsSubItem.__init__(
            self, parent, attr, service, rules, path, arg
        )

    def __getattr__(self, attr):
        arg = self.parent_arg.info.parameters[attr]

        mode = DataModelType.get_mode(arg.type)
        py_class = mode.value[1]
        return py_class(self, attr, self.service, self.rules, self.path, arg)


class DataModelType(Enum):
    """An enumeration over datamodel types."""

    # Really???

    # Tuple:   Name, Solver object type, Meshing flag, Launcher options
    # Really???
    TEXT = (["String", "ListString", "String List"], PyTextualCommandArgumentsSubItem)
    NUMBER = (
        ["Real", "Int", "ListReal", "Real List", "Integer"],
        PyNumericalCommandArgumentsSubItem,
    )
    DICTIONARY = (["Dict"], PyDictionaryCommandArgumentsSubItem)
    PARAMETER = (
        ["Bool", "Logical", "Logical List"],
        PyParameterCommandArgumentsSubItem,
    )
    MODELOBJECT = (["ModelObject"], PySingletonCommandArgumentsSubItem)

    @staticmethod
    def get_mode(mode: str) -> Type[PyCommandArgumentsSubItem]:
        """Returns the datamodel type."""
        for m in DataModelType:
            if mode in m.value[0]:
                return m
        else:
            raise TypeError(f"The specified mode: {mode} was not found.")


class PyMenuGeneric(PyMenu):
    """Generic PyMenu class for when generated API code is not available."""

    attrs = ("service", "rules", "path")

    def _get_child_names(self):
        request = DataModelProtoModule.GetSpecsRequest()
        request.rules = self.rules
        request.path = convert_path_to_se_path(self.path)
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
                f"{name} is not found at path " f"{convert_path_to_se_path(self.path)}"
            )

    def __dir__(self):
        return list(itertools.chain(*self._get_child_names()))

    def __getattr__(self, name: str):
        if name in PyMenuGeneric.attrs:
            return super().__getattr__(name)
        else:
            return self._get_child(name)


class PySimpleMenuGeneric(PyMenu, PyDictionary):
    """A simple implementation of PyMenuGeneric applicable only for SINGLETONS.

    This is required for the stand-alone datamodel server to avoid the
    usage of 'service.get_specs'
    """

    attrs = ("service", "rules", "path")

    def _get_child(self, name: str):
        child_path = self.path + [(name, "")]
        return PySimpleMenuGeneric(self.service, self.rules, child_path)

    def __getattr__(self, name: str):
        if name in PySimpleMenuGeneric.attrs:
            return super().__getattr__(name)
        else:
            return self._get_child(name)


class PyNamedObjectContainerGeneric(PyNamedObjectContainer):
    """Generic PyNamedObjectContainer class for when generated API code is not available."""

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
                f"{key} is not found at path " f"{convert_path_to_se_path(self.path)}"
            )
