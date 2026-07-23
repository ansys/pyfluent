# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
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

"""Wrapper over the object model gRPC service of Fluent (v1 proto API)."""

from collections.abc import Callable, Sequence
import logging
from threading import RLock
from typing import Any

from google.protobuf.json_format import MessageToDict, ParseDict
import grpc

from ansys.api.fluent.v1 import object_model_pb2, object_model_pb2_grpc
from ansys.api.fluent.v1.variant_pb2 import Variant
from ansys.fluent.core.services._command_arguments_mixin import (
    CommandArgumentsCleanupMixin,
)
from ansys.fluent.core.services._protocols import ServiceProtocol
from ansys.fluent.core.services.object_model_utilities import (
    convert_path_to_se_path,
    convert_se_path_to_path,
)
from ansys.fluent.core.streaming_services.streaming import StreamingService

ValueT = None | bool | int | float | str | Sequence["ValueT"] | dict[str, "ValueT"]
logger: logging.Logger = logging.getLogger("pyfluent.object_model_v1")


class EventSubscription:
    """EventSubscription class for any datamodel event."""

    def __init__(
        self,
        service,
        path,
        request_dict: dict[str, Any],
    ) -> None:
        """Subscribe to a datamodel event.

        Raises
        ------
        SubscribeEventError
            If server fails to subscribe from event.
        """
        self.is_subscribed: bool = False
        self._service = service
        self.path: str = path
        response = service.subscribe_events(request_dict)
        response = response[0]
        if response["status"] != object_model_pb2.SUBSCRIPTION_STATUS_SUBSCRIBED:
            raise SubscribeEventError(request_dict)
        self.is_subscribed = True
        self.tag: str = response["tag"]
        self._service.subscriptions.add(self.tag, self)

    def unsubscribe(self) -> None:
        """Unsubscribe the datamodel event.

        Raises
        ------
        UnsubscribeEventError
            If server fails to unsubscribe from event.
        """
        if self.is_subscribed:
            self._service.event_streaming.unregister_callback(self.tag)
            response = self._service.unsubscribe_events([self.tag])[0]
            if response["status"] != object_model_pb2.SUBSCRIPTION_STATUS_UNSUBSCRIBED:
                raise UnsubscribeEventError(self.tag)
            self.is_subscribed = False
            self._service.subscriptions.remove(self.tag)


class SubscriptionList:
    """Stores subscription objects by tag."""

    def __init__(self):
        """Initialize SubscriptionList."""
        self._subscriptions = {}
        self._lock = RLock()

    def __contains__(self, tag: str) -> bool:
        with self._lock:
            return tag in self._subscriptions

    def add(self, tag: str, subscription: EventSubscription) -> None:
        """Add a subscription object.

        Parameters
        ----------
        tag : str
            Subscription tag.
        subscription : EventSubscription
            Subscription object.
        """
        with self._lock:
            self._subscriptions[tag] = subscription

    def remove(self, tag: str) -> None:
        """Remove a subscription object.

        Parameters
        ----------
        tag : str
            Subscription tag.
        """
        with self._lock:
            self._subscriptions.pop(tag, None)

    def unsubscribe_while_deleting(
        self, rules: str, path: str, deletion_stage: str
    ) -> None:
        """Unsubscribe corresponding subscription objects while the datamodel object is
        being deleted.

        Parameters
        ----------
        rules : str
            Datamodel object rules.
        path : str
            Datamodel object path.
        deletion_stage : {"before", "after"}
            All subscription objects except those of on-deleted type are unsubscribed
            before the datamodel object is deleted. On-deleted subscription objects are
            unsubscribed after the datamodel object is deleted.
        """
        with self._lock:
            delete_tag = f"/{rules}/deleted"
            after = deletion_stage == "after"
            keys_to_unsubscribe = []
            for k, v in self._subscriptions.items():
                if v.path.startswith(path) and not (
                    after ^ v.tag.startswith(delete_tag)
                ):
                    keys_to_unsubscribe.append(k)
            for k in reversed(keys_to_unsubscribe):
                self._subscriptions[k].unsubscribe()

    def unsubscribe_all(self) -> None:
        """Unsubscribe all subscription objects."""
        with self._lock:
            while self._subscriptions:
                v = next(reversed(self._subscriptions.values()))
                v.unsubscribe()


class SubscribeEventError(RuntimeError):
    """Raised when server fails to subscribe from event."""

    def __init__(self, request):
        """Initialize SubscribeEventError."""
        super().__init__(f"Failed to subscribe event: {request}!")


class UnsubscribeEventError(RuntimeError):
    """Raised when server fails to unsubscribe from event."""

    def __init__(self, request):
        """Initialize UnsubscribeEventError."""
        super().__init__(f"Failed to unsubscribe event: {request}!")


class ObjectModelService(  # pyright: ignore[reportUnsafeMultipleInheritance]
    CommandArgumentsCleanupMixin, StreamingService, ServiceProtocol
):
    """Class wrapping the object model gRPC service of Fluent (v1 proto API)."""

    def __init__(
        self,
        intercept_channel,
        metadata: list[tuple[str, str]],
    ) -> None:
        """__init__ method of ObjectModelService class."""
        super().__init__(
            stub=object_model_pb2_grpc.ObjectModelStub(intercept_channel),
            metadata=metadata,
        )
        self.subscriptions = SubscriptionList()
        self.event_streaming = None

    def _delete_command_arguments_rpc(
        self, rules: str, path: str, command: str, commandid: str
    ) -> None:
        """Issue RPC to delete command arguments."""
        self._delete_command_arguments(rules, path, command, commandid)

    def _delete_command_arguments(
        self, rules: str, path: str, command: str, commandid: str
    ) -> None:
        """RPC deleteCommandArguments of ObjectModel service.

        Raises
        ------
        RuntimeError
            If command instancing is not supported.
        """
        try:
            request = object_model_pb2.DeleteCommandArgumentsRequest(
                rules=rules, path=path, command=command, command_id=commandid
            )
            return self._stub.DeleteCommandArguments(request, metadata=self._metadata)
        except grpc.RpcError as ex:
            raise RuntimeError(
                f"The following exception was caught\n {ex.details()}\n "
                "while deleting a command instance. Command instancing is"
                "supported from Ansys 2023R2 onward."
            ) from None

    def get_attribute_value(self, rules: str, path: str, attribute: str) -> ValueT:
        """Get attribute value."""
        request = object_model_pb2.GetAttributeValueRequest(
            rules=rules, path=path, attribute=attribute
        )
        response = self._stub.GetAttributeValue(request, metadata=self._metadata)
        return _convert_variant_to_value(response.result)

    def get_state(self, rules: str, path: str) -> ValueT:
        """Get state."""
        request = object_model_pb2.GetStateRequest(rules=rules, path=path)
        response = self._stub.GetState(request, metadata=self._metadata)
        return _convert_variant_to_value(response.state)

    def get_object_names(self, rules: str, path: str) -> list[str]:
        """Get object names."""
        request = object_model_pb2.GetObjectNamesRequest(rules=rules, path=path)
        response = self._stub.GetObjectNames(request, metadata=self._metadata)
        return response.names

    def rename(self, rules: str, path: str, new_name: str) -> None:
        """Rename an object."""
        request = object_model_pb2.RenameRequest(
            rules=rules, path=path, new_name=new_name, wait=True
        )
        response = self._stub.Rename(request, metadata=self._metadata)
        return response.state, response.deleted_paths

    def delete_child_objects(
        self, rules: str, path: str, obj_type: str, child_names: list[str]
    ) -> None:
        """Delete child objects."""
        request = object_model_pb2.DeleteChildObjectsRequest(
            rules=rules, path=path + "/" + obj_type, wait=True
        )
        request.child_names.names[:] = child_names
        response = self._stub.DeleteChildObjects(request, metadata=self._metadata)
        return response.state, response.deleted_paths

    def delete_all_child_objects(self, rules: str, path: str, obj_type: str) -> None:
        """Delete all child objects."""
        request = object_model_pb2.DeleteChildObjectsRequest(
            rules=rules, path=path + "/" + obj_type, delete_all=True, wait=True
        )
        response = self._stub.DeleteChildObjects(request, metadata=self._metadata)
        return response.state, response.deleted_paths

    def set_state(self, rules: str, path: str, state: ValueT) -> None:
        """Set state."""
        request = object_model_pb2.SetStateRequest(rules=rules, path=path, wait=True)
        _convert_value_to_variant(state, request.state)
        response = self._stub.SetState(request, metadata=self._metadata)
        return response.state, response.deleted_paths

    def fix_state(self, rules, path) -> None:
        """Fix state."""
        request = object_model_pb2.FixStateRequest(
            rules=rules,
            path=convert_path_to_se_path(path),
        )
        response = self._stub.FixState(request, metadata=self._metadata)
        return response.state, response.deleted_paths

    def update_dict(
        self,
        rules: str,
        path: str,
        dict_state: dict[str, ValueT],
        recursive=False,
    ) -> None:
        """Update the dict."""
        request = object_model_pb2.UpdateDictRequest(
            rules=rules, path=path, wait=True, recursive=recursive
        )
        _convert_value_to_variant(dict_state, request.merge_dict)
        response = self._stub.UpdateDict(request, metadata=self._metadata)
        return response.state, response.deleted_paths

    def create_object(self, rules: str, path: str, name: str) -> None:
        """Create a named object."""
        request = object_model_pb2.CreateObjectRequest(
            rules=rules, path=path, name=name, wait=True
        )
        response = self._stub.CreateObject(request, metadata=self._metadata)
        return response.state, response.deleted_paths

    def delete_object(self, rules: str, path: str) -> None:
        """Delete an object."""
        request = object_model_pb2.DeleteObjectRequest(
            rules=rules, path=path, wait=True
        )
        response = self._stub.DeleteObject(request, metadata=self._metadata)
        return response.state, response.deleted_paths

    def execute_command(
        self, rules: str, path: str, command: str, args: dict[str, ValueT]
    ) -> ValueT:
        """Execute the command."""
        request = object_model_pb2.ExecuteCommandRequest(
            rules=rules, path=path, command=command, wait=True
        )
        _convert_value_to_variant(args, request.args)
        response = self._stub.ExecuteCommand(request, metadata=self._metadata)
        return (
            _convert_variant_to_value(response.result),
            response.state,
            response.deleted_paths,
        )

    def execute_query(
        self, rules: str, path: str, query: str, args: dict[str, ValueT]
    ) -> ValueT:
        """Execute the query."""
        request = object_model_pb2.ExecuteQueryRequest(
            rules=rules, path=path, query=query
        )
        _convert_value_to_variant(args, request.args)
        response = self._stub.ExecuteQuery(request, metadata=self._metadata)
        return _convert_variant_to_value(response.result)

    def create_command_arguments(self, rules: str, path: str, command: str) -> str:
        """Create command arguments."""
        request = object_model_pb2.CreateCommandArgumentsRequest(
            rules=rules, path=path, command=command
        )
        response = self._stub.CreateCommandArguments(request, metadata=self._metadata)
        return response.command_id

    def delete_command_arguments(
        self, rules: str, path: str, command: str, commandid: str
    ) -> None:
        """Delete command arguments."""
        return super().delete_command_arguments(rules, path, command, commandid)

    def get_static_info(self, rules: str) -> dict[str, Any]:
        """Get static info."""
        request = object_model_pb2.GetSchemaRequest(rules=rules)
        return _normalize_v1_datamodel_dict_keys(
            MessageToDict(
                self._stub.GetSchema(request, metadata=self._metadata).info,
                use_integers_for_enums=True,
            )
        )

    def subscribe_events(self, request_dict: dict[str, Any]) -> list[dict[str, Any]]:
        """Subscribe events."""
        request = object_model_pb2.SubscribeEventsRequest()
        ParseDict(_normalize_v1_event_request_dict(request_dict), request)
        return [
            MessageToDict(x, use_integers_for_enums=True)
            for x in self._stub.SubscribeEvents(
                request, metadata=self._metadata
            ).responses
        ]

    def unsubscribe_events(self, tags: list[str]) -> list[dict[str, Any]]:
        """Unsubscribe events."""
        request = object_model_pb2.UnsubscribeEventsRequest()
        request.tags[:] = tags
        return [
            MessageToDict(x, use_integers_for_enums=True)
            for x in self._stub.UnsubscribeEvents(
                request, metadata=self._metadata
            ).responses
        ]

    def unsubscribe_all_events(self) -> None:
        """Unsubscribe all subscribed events."""
        self.subscriptions.unsubscribe_all()

    def add_on_child_created(
        self, rules: str, path: str, child_type: str, cb: Callable[[str], None]
    ) -> EventSubscription:
        """Add on child created."""
        request_dict = {
            "eventrequest": [
                {
                    "rules": rules,
                    "createdEventRequest": {
                        "parentpath": path,
                        "childtype": child_type,
                    },
                }
            ]
        }
        subscription = EventSubscription(self, path, request_dict)

        def cb_grpc(child_type: str, child_name: str):
            ppath = convert_se_path_to_path(path)
            ppath.append((child_type, child_name))
            child_path = convert_path_to_se_path(ppath)
            cb(child_path)

        self.event_streaming.register_callback(subscription.tag, cb_grpc)
        return subscription

    def add_on_deleted(
        self, rules: str, path: str, cb: Callable[[], None]
    ) -> EventSubscription:
        """Add on deleted."""
        request_dict = {
            "eventrequest": [
                {
                    "rules": rules,
                    "deletedEventRequest": {"path": path},
                }
            ]
        }
        subscription = EventSubscription(self, path, request_dict)
        self.event_streaming.register_callback(subscription.tag, cb)
        return subscription

    def add_on_changed(
        self, rules: str, path: str, cb: Callable[[ValueT], None]
    ) -> EventSubscription:
        """Add on changed."""
        request_dict = {
            "eventrequest": [
                {
                    "rules": rules,
                    "modifiedEventRequest": {"path": path},
                }
            ]
        }
        subscription = EventSubscription(self, path, request_dict)
        self.event_streaming.register_callback(subscription.tag, cb)
        return subscription

    def add_on_affected(
        self, rules: str, path: str, cb: Callable[[], None]
    ) -> EventSubscription:
        """Add on affected."""
        request_dict = {
            "eventrequest": [
                {
                    "rules": rules,
                    "affectedEventRequest": {"path": path},
                }
            ]
        }
        subscription = EventSubscription(self, path, request_dict)
        self.event_streaming.register_callback(subscription.tag, cb)
        return subscription

    def add_on_affected_at_type_path(
        self, rules: str, path: str, child_type: str, cb: Callable[[], None]
    ) -> EventSubscription:
        """Add on affected at type path."""
        request_dict = {
            "eventrequest": [
                {
                    "rules": rules,
                    "affectedEventRequest": {
                        "path": path,
                        "subtype": child_type,
                    },
                }
            ]
        }
        subscription = EventSubscription(self, path, request_dict)
        self.event_streaming.register_callback(subscription.tag, cb)
        return subscription

    def add_on_command_executed_old(
        self,
        rules: str,
        path: str,
        command: str,
        obj,
        cb: Callable[[str, ValueT], None],
    ) -> EventSubscription:
        """Add on command executed."""
        request_dict = {
            "eventrequest": [
                {
                    "rules": rules,
                    "commandExecutedEventRequest": {
                        "path": path,
                        "command": command,
                    },
                }
            ]
        }
        subscription = EventSubscription(self, path, request_dict)
        self.event_streaming.register_callback(subscription.tag, cb)
        return subscription

    def add_on_command_executed(
        self, rules: str, path: str, cb: Callable[[str, ValueT], None]
    ) -> EventSubscription:
        """Add on command executed."""
        request_dict = {
            "eventrequest": [
                {
                    "rules": rules,
                    "commandExecutedEventRequest": {
                        "path": path,
                    },
                }
            ]
        }
        subscription = EventSubscription(self, path, request_dict)
        self.event_streaming.register_callback(subscription.tag, cb)
        return subscription

    def add_on_attribute_changed(
        self, rules: str, path: str, attribute: str, cb: Callable[[ValueT], None]
    ) -> EventSubscription:
        """Add on attribute changed."""
        request_dict = {
            "eventrequest": [
                {
                    "rules": rules,
                    "attributeChangedEventRequest": {
                        "path": path,
                        "attribute": attribute,
                    },
                }
            ]
        }
        subscription = EventSubscription(self, path, request_dict)
        self.event_streaming.register_callback(subscription.tag, cb)
        return subscription

    def add_on_command_attribute_changed(
        self,
        rules: str,
        path: str,
        command: str,
        attribute: str,
        cb: Callable[[ValueT], None],
    ) -> EventSubscription:
        """Add on command attribute changed."""
        request_dict = {
            "eventrequest": [
                {
                    "rules": rules,
                    "commandAttributeChangedEventRequest": {
                        "path": path,
                        "command": command,
                        "attribute": attribute,
                    },
                }
            ]
        }
        subscription = EventSubscription(self, path, request_dict)
        self.event_streaming.register_callback(subscription.tag, cb)
        return subscription

    def _process_streaming(
        self,
        id,
        stream_begin_method,
        started_evt,
        rules,
        datamodel_return_state_changes,
        no_commands_diff_state,
        *args,
        **kwargs,
    ):
        """Processes events streaming."""
        data_model_request = object_model_pb2.StreamStateChangesRequest(*args, **kwargs)
        data_model_request.rules = rules
        data_model_request.return_state_changes = datamodel_return_state_changes
        if no_commands_diff_state:
            data_model_request.diff_state = object_model_pb2.DIFF_STATE_NOCOMMANDS
        return self.begin_streaming(
            data_model_request,
            started_evt,
            id=id,
            stream_begin_method=stream_begin_method,
        )

    def parse_streaming_response(self, response):
        """Parse v1 streaming response into canonical (state, deleted_paths) form."""
        return response.state, response.deleted_paths

    _stream_begin_method = "StreamStateChanges"
    _streaming_rpc_path = (
        "/ansys.api.fluent.v1.object_model.ObjectModel/StreamStateChanges"
    )

    _event_stream_begin_method = "StreamEvents"
    _event_streaming_rpc_path = (
        "/ansys.api.fluent.v1.datamodel_se.DataModel/StreamEvents"
    )

    def _process_event_streaming(self, id, started_evt, *args, **kwargs):
        """Begin v1 event streaming."""
        request = object_model_pb2.StreamEventsRequest()
        return self.begin_streaming(
            request,
            started_evt,
            id=id,
            stream_begin_method=self._event_stream_begin_method,
        )

    def parse_event_response(self, response):
        """Parse a v1 event streaming response into (event_type, cb_args) form."""
        if response.HasField("created_event_response"):
            return "created", (
                response.created_event_response.child_type,
                response.created_event_response.child_name,
            )
        elif response.HasField("attribute_changed_event_response"):
            return "attribute_changed", (
                _convert_variant_to_value(
                    response.attribute_changed_event_response.value
                ),
            )
        elif response.HasField("command_attribute_changed_event_response"):
            return "command_attribute_changed", (
                _convert_variant_to_value(
                    response.command_attribute_changed_event_response.value
                ),
            )
        elif response.HasField("modified_event_response"):
            return "modified", (
                _convert_variant_to_value(response.modified_event_response.value),
            )
        elif response.HasField("affected_event_response"):
            return "affected", ()
        elif response.HasField("deleted_event_response"):
            return "deleted", ()
        elif response.HasField("command_executed_event_response"):
            return "command_executed", (
                response.command_executed_event_response.command,
                _convert_variant_to_value(
                    response.command_executed_event_response.args
                ),
            )
        return None, ()


def _convert_value_to_variant(val: ValueT, var: Variant) -> None:
    """Convert a Python data type to Fluent's variant type (v1 proto)."""
    if isinstance(val, bool):
        var.bool_state = val
    elif isinstance(val, int):
        var.int64_state = val
    elif isinstance(val, float):
        var.double_state = val
    elif isinstance(val, str):
        var.string_state = val
    elif isinstance(val, (list, tuple)):
        var.variant_vector_state.SetInParent()
        for item in val:
            item_var = var.variant_vector_state.items.add()
            _convert_value_to_variant(item, item_var)
    elif isinstance(val, dict):
        var.variant_map_state.SetInParent()
        for k, v in val.items():
            _convert_value_to_variant(v, var.variant_map_state.item[k])


def _convert_variant_to_value(var: Variant) -> ValueT:
    """Convert Fluent's variant type to a Python data type (v1 proto)."""
    if var.HasField("bool_state"):
        return var.bool_state
    elif var.HasField("int64_state"):
        return var.int64_state
    elif var.HasField("double_state"):
        return var.double_state
    elif var.HasField("string_state"):
        return var.string_state
    elif var.HasField("bool_vector_state"):
        return var.bool_vector_state.items
    elif var.HasField("int64_vector_state"):
        return var.int64_vector_state.items
    elif var.HasField("double_vector_state"):
        return var.double_vector_state.items
    elif var.HasField("string_vector_state"):
        return var.string_vector_state.items
    elif var.HasField("variant_vector_state"):
        val = []
        for item in var.variant_vector_state.items:
            val.append(_convert_variant_to_value(item))
        return val
    elif var.HasField("variant_map_state"):
        val = {}
        for k, v in var.variant_map_state.item.items():
            val[k] = _convert_variant_to_value(v)
        return val


_DATAMODEL_KEY_MAP_V1_TO_LEGACY = {
    "namedObjects": "namedobjects",
    "creatableTypes": "creatabletypes",
    "commandInfo": "commandinfo",
    "queryInfo": "queryinfo",
    "returnType": "returntype",
    "helpString": "helpstring",
    "apiHelpText": "api_help_text",
}


def _normalize_v1_datamodel_dict_keys(data):
    """Normalize v1 camelCase datamodel keys to legacy keys expected by callers."""
    if isinstance(data, dict):
        return {
            _DATAMODEL_KEY_MAP_V1_TO_LEGACY.get(
                key, key
            ): _normalize_v1_datamodel_dict_keys(value)
            for key, value in data.items()
        }
    if isinstance(data, list):
        return [_normalize_v1_datamodel_dict_keys(item) for item in data]
    return data


def _normalize_v1_event_request_dict(data):
    """Normalize legacy event-request payload keys to v1 proto keys."""
    if isinstance(data, list):
        return [_normalize_v1_event_request_dict(x) for x in data]
    if isinstance(data, dict):
        key_map = {
            "eventrequest": "event_requests",
            "createdEventRequest": "created_event_request",
            "modifiedEventRequest": "modified_event_request",
            "deletedEventRequest": "deleted_event_request",
            "affectedEventRequest": "affected_event_request",
            "attributeChangedEventRequest": "attribute_changed_event_request",
            "commandAttributeChangedEventRequest": "command_attribute_changed_event_request",
            "commandExecutedEventRequest": "command_executed_event_request",
            "parentpath": "parent_path",
            "childtype": "child_type",
        }
        return {
            key_map.get(k, k): _normalize_v1_event_request_dict(v)
            for k, v in data.items()
        }
    return data
