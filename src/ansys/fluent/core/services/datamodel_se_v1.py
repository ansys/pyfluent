# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
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

"""Wrappers over StateEngine based datamodel gRPC service of Fluent (v1 proto API).

All shared logic lives in datamodel_se.py (v0). This module keeps only
v1-specific proto/stub/request differences.
"""

from typing import Any, Callable

from google.protobuf.json_format import MessageToDict, ParseDict
import grpc

from ansys.api.fluent.v1 import datamodel_se_pb2 as DataModelProtoModule
from ansys.api.fluent.v1 import datamodel_se_pb2_grpc as DataModelGrpcModule
from ansys.api.fluent.v1.variant_pb2 import Variant
from ansys.fluent.core.data_model_cache import DataModelCache
from ansys.fluent.core.module_config import config
from ansys.fluent.core.services import (
    datamodel_se as _v0,  # v0 base: shared logic is reused; only v1-specific proto/stub differences are overridden below
)
from ansys.fluent.core.services.interceptors import (
    BatchInterceptor,
    ErrorStateInterceptor,
    GrpcErrorInterceptor,
    TracingInterceptor,
)
from ansys.fluent.core.services.streaming import StreamingService

Path = _v0.Path
PyMenuT = _v0.PyMenuT
ValueT = _v0.ValueT
logger = _v0.logger

member_specs_oneof_fields = [
    x.name
    for x in DataModelProtoModule.MemberSpecs.DESCRIPTOR.oneofs_by_name["as"].fields
]

_get_value_from_message_dict = _v0._get_value_from_message_dict


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


DisallowedFilePurpose = _v0.DisallowedFilePurpose
InvalidNamedObject = _v0.InvalidNamedObject
SubscribeEventError = _v0.SubscribeEventError
UnsubscribeEventError = _v0.UnsubscribeEventError
ReadOnlyObjectError = _v0.ReadOnlyObjectError
Attribute = _v0.Attribute
_FilterDatamodelNames = _v0._FilterDatamodelNames
SubscriptionList = _v0.SubscriptionList


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


class DatamodelServiceImpl:
    """Wraps the StateEngine-based datamodel gRPC service of Fluent (v1)."""

    def __init__(
        self,
        channel: grpc.Channel,
        metadata: list[tuple[str, str]],
        fluent_error_state,
        file_transfer_service: Any | None = None,
    ) -> None:
        """Initialize DatamodelServiceImpl."""
        intercept_channel = grpc.intercept_channel(
            channel,
            GrpcErrorInterceptor(),
            ErrorStateInterceptor(fluent_error_state),
            TracingInterceptor(),
            BatchInterceptor(),
        )
        self._stub = DataModelGrpcModule.DataModelServiceStub(intercept_channel)
        self._metadata = metadata
        self.file_transfer_service = file_transfer_service

    def initialize_datamodel(
        self, request: DataModelProtoModule.InitDatamodelRequest
    ) -> DataModelProtoModule.InitDatamodelResponse:
        """RPC InitDatamodel of DataModel service."""
        return self._stub.InitDatamodel(request, metadata=self._metadata)

    def get_attribute_value(
        self, request: DataModelProtoModule.GetAttributeValueRequest
    ) -> DataModelProtoModule.GetAttributeValueResponse:
        """RPC GetAttributeValue of DataModel service."""
        return self._stub.GetAttributeValue(request, metadata=self._metadata)

    def get_state(
        self, request: DataModelProtoModule.GetStateRequest
    ) -> DataModelProtoModule.GetStateResponse:
        """RPC GetState of DataModel service."""
        return self._stub.GetState(request, metadata=self._metadata)

    def rename(
        self, request: DataModelProtoModule.RenameRequest
    ) -> DataModelProtoModule.RenameResponse:
        """RPC Rename of DataModel service."""
        return self._stub.Rename(request, metadata=self._metadata)

    def get_object_names(
        self, request: DataModelProtoModule.GetObjectNamesRequest
    ) -> DataModelProtoModule.GetObjectNamesResponse:
        """RPC GetObjectNames of DataModel service."""
        return self._stub.GetObjectNames(request, metadata=self._metadata)

    def delete_child_objects(
        self, request: DataModelProtoModule.DeleteChildObjectsRequest
    ) -> DataModelProtoModule.DeleteChildObjectsResponse:
        """RPC DeleteChildObjects of DataModel service."""
        return self._stub.DeleteChildObjects(request, metadata=self._metadata)

    def set_state(
        self, request: DataModelProtoModule.SetStateRequest
    ) -> DataModelProtoModule.SetStateResponse:
        """RPC SetState of DataModel service."""
        return self._stub.SetState(request, metadata=self._metadata)

    def fix_state(
        self, request: DataModelProtoModule.FixStateRequest
    ) -> DataModelProtoModule.FixStateResponse:
        """RPC FixState of DataModel service."""
        return self._stub.FixState(request, metadata=self._metadata)

    def update_dict(
        self, request: DataModelProtoModule.UpdateDictRequest
    ) -> DataModelProtoModule.UpdateDictResponse:
        """RPC UpdateDict of DataModel service."""
        return self._stub.UpdateDict(request, metadata=self._metadata)

    def delete_object(
        self, request: DataModelProtoModule.DeleteObjectRequest
    ) -> DataModelProtoModule.DeleteObjectResponse:
        """RPC DeleteObject of DataModel service."""
        return self._stub.DeleteObject(request, metadata=self._metadata)

    def execute_command(
        self, request: DataModelProtoModule.ExecuteCommandRequest
    ) -> DataModelProtoModule.ExecuteCommandResponse:
        """RPC ExecuteCommand of DataModel service."""
        logger.debug(f"Command: {request.command}")
        return self._stub.ExecuteCommand(request, metadata=self._metadata)

    def execute_query(
        self, request: DataModelProtoModule.ExecuteQueryRequest
    ) -> DataModelProtoModule.ExecuteQueryResponse:
        """RPC ExecuteQuery of DataModel service."""
        logger.debug(f"Query: {request.query}")
        return self._stub.ExecuteQuery(request, metadata=self._metadata)

    def create_command_arguments(
        self, request: DataModelProtoModule.CreateCommandArgumentsRequest
    ) -> DataModelProtoModule.CreateCommandArgumentsResponse:
        """RPC CreateCommandArguments of DataModel service."""
        return self._stub.CreateCommandArguments(request, metadata=self._metadata)

    def delete_command_arguments(
        self, request: DataModelProtoModule.DeleteCommandArgumentsRequest
    ) -> DataModelProtoModule.DeleteCommandArgumentsResponse:
        """RPC DeleteCommandArguments of DataModel service.

        Raises
        ------
        RuntimeError
            If command instancing is not supported.
        """
        try:
            return self._stub.DeleteCommandArguments(request, metadata=self._metadata)
        except grpc.RpcError as ex:
            raise RuntimeError(
                f"The following exception was caught\n {ex.details()}\n "
                "while deleting a command instance. Command instancing is"
                "supported from Ansys 2023R2 onward."
            ) from None

    def get_specs(
        self, request: DataModelProtoModule.GetSpecsRequest
    ) -> DataModelProtoModule.GetSpecsResponse:
        """RPC GetSpecs of DataModel service."""
        return self._stub.GetSpecs(request, metadata=self._metadata)

    def get_static_info(
        self, request: DataModelProtoModule.GetStaticInfoRequest
    ) -> DataModelProtoModule.GetStaticInfoResponse:
        """RPC GetStaticInfo of DataModel service."""
        return self._stub.GetStaticInfo(request, metadata=self._metadata)

    def subscribe_events(
        self, request: DataModelProtoModule.SubscribeEventsRequest
    ) -> DataModelProtoModule.SubscribeEventsResponse:
        """RPC SubscribeEvents of DataModel service."""
        return self._stub.SubscribeEvents(request, metadata=self._metadata)

    def unsubscribe_events(
        self, request: DataModelProtoModule.UnsubscribeEventsRequest
    ) -> DataModelProtoModule.UnsubscribeEventsResponse:
        """RPC UnsubscribeEvents of DataModel service."""
        return self._stub.UnsubscribeEvents(request, metadata=self._metadata)


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
        self._service: DatamodelService = service
        self.path: str = path
        response = service.subscribe_events(request_dict)[0]
        if response["status"] != DataModelProtoModule.SUBSCRIPTION_STATUS_SUBSCRIBED:
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
            if (
                response["status"]
                != DataModelProtoModule.SUBSCRIPTION_STATUS_UNSUBSCRIBED
            ):
                raise UnsubscribeEventError(self.tag)
            self.is_subscribed = False
            self._service.subscriptions.remove(self.tag)


class DatamodelService(StreamingService):
    """Pure Python wrapper of DatamodelServiceImpl (v1)."""

    def __init__(
        self,
        channel: grpc.Channel,
        metadata: list[tuple[str, str]],
        version: _v0.FluentVersion,
        fluent_error_state,
        file_transfer_service: Any | None = None,
    ) -> None:
        """Initialize DatamodelService."""
        self._impl = DatamodelServiceImpl(channel, metadata, fluent_error_state)
        super().__init__(
            stub=self._impl._stub,
            metadata=metadata,
        )
        self.event_streaming = None
        self.subscriptions = SubscriptionList()
        self.file_transfer_service = file_transfer_service
        self.cache = DataModelCache() if config.datamodel_use_state_cache else None
        self.version = version

    def get_attribute_value(self, rules: str, path: str, attribute: str) -> ValueT:
        """Get attribute value."""
        request = DataModelProtoModule.GetAttributeValueRequest(
            rules=rules, path=path, attribute=attribute
        )
        response = self._impl.get_attribute_value(request)
        return _convert_variant_to_value(response.result)

    def get_state(self, rules: str, path: str) -> ValueT:
        """Get state."""
        request = DataModelProtoModule.GetStateRequest(rules=rules, path=path)
        response = self._impl.get_state(request)
        return _convert_variant_to_value(response.state)

    def get_object_names(self, rules: str, path: str) -> list[str]:
        """Get object names."""
        request = DataModelProtoModule.GetObjectNamesRequest(rules=rules, path=path)
        response = self._impl.get_object_names(request)
        return response.names

    def rename(self, rules: str, path: str, new_name: str) -> None:
        """Rename an object."""
        request = DataModelProtoModule.RenameRequest(
            rules=rules, path=path, new_name=new_name, wait=True
        )
        response = self._impl.rename(request)
        if self.cache is not None:
            self.cache.update_cache(
                rules,
                response.state,
                response.deleted_paths,
                version=self.version,
            )

    def delete_child_objects(
        self, rules: str, path: str, obj_type: str, child_names: list[str]
    ) -> None:
        """Delete child objects."""
        request = DataModelProtoModule.DeleteChildObjectsRequest(
            rules=rules, path=path + "/" + obj_type, wait=True
        )
        request.child_names.names[:] = child_names
        response = self._impl.delete_child_objects(request)
        if self.cache is not None:
            self.cache.update_cache(
                rules,
                response.state,
                response.deleted_paths,
                version=self.version,
            )

    def delete_all_child_objects(self, rules: str, path: str, obj_type: str) -> None:
        """Delete all child objects."""
        request = DataModelProtoModule.DeleteChildObjectsRequest(
            rules=rules, path=path + "/" + obj_type, delete_all=True, wait=True
        )
        response = self._impl.delete_child_objects(request)
        if self.cache is not None:
            self.cache.update_cache(
                rules,
                response.state,
                response.deleted_paths,
                version=self.version,
            )

    def set_state(self, rules: str, path: str, state: ValueT) -> None:
        """Set state."""
        request = DataModelProtoModule.SetStateRequest(
            rules=rules, path=path, wait=True
        )
        _convert_value_to_variant(state, request.state)
        response = self._impl.set_state(request)
        if self.cache is not None:
            self.cache.update_cache(
                rules,
                response.state,
                response.deleted_paths,
                version=self.version,
            )

    def fix_state(self, rules, path) -> None:
        """Fix state."""
        request = DataModelProtoModule.FixStateRequest(
            rules=rules,
            path=convert_path_to_se_path(path),
        )
        response = self._impl.fix_state(request)
        if self.cache is not None:
            self.cache.update_cache(
                rules,
                response.state,
                response.deleted_paths,
                version=self.version,
            )

    def update_dict(
        self,
        rules: str,
        path: str,
        dict_state: dict[str, ValueT],
        recursive=False,
    ) -> None:
        """Update the dict."""
        request = DataModelProtoModule.UpdateDictRequest(
            rules=rules, path=path, wait=True, recursive=recursive
        )
        _convert_value_to_variant(dict_state, request.merge_dict)
        response = self._impl.update_dict(request)
        if self.cache is not None:
            self.cache.update_cache(
                rules,
                response.state,
                response.deleted_paths,
                version=self.version,
            )

    def delete_object(self, rules: str, path: str) -> None:
        """Delete an object."""
        request = DataModelProtoModule.DeleteObjectRequest(
            rules=rules, path=path, wait=True
        )
        response = self._impl.delete_object(request)
        if self.cache is not None:
            self.cache.update_cache(
                rules,
                response.state,
                response.deleted_paths,
                version=self.version,
            )

    def execute_command(
        self, rules: str, path: str, command: str, args: dict[str, ValueT]
    ) -> ValueT:
        """Execute the command."""
        request = DataModelProtoModule.ExecuteCommandRequest(
            rules=rules, path=path, command=command, wait=True
        )
        _convert_value_to_variant(args, request.args)
        response = self._impl.execute_command(request)
        if self.cache is not None:
            self.cache.update_cache(
                rules,
                response.state,
                response.deleted_paths,
                version=self.version,
            )
        return _convert_variant_to_value(response.result)

    def execute_query(
        self, rules: str, path: str, query: str, args: dict[str, ValueT]
    ) -> ValueT:
        """Execute the query."""
        request = DataModelProtoModule.ExecuteQueryRequest(
            rules=rules, path=path, query=query
        )
        _convert_value_to_variant(args, request.args)
        response = self._impl.execute_query(request)
        return _convert_variant_to_value(response.result)

    def create_command_arguments(self, rules: str, path: str, command: str) -> str:
        """Create command arguments."""
        request = DataModelProtoModule.CreateCommandArgumentsRequest(
            rules=rules, path=path, command=command
        )
        response = self._impl.create_command_arguments(request)
        return response.command_id

    def delete_command_arguments(
        self, rules: str, path: str, command: str, commandid: str
    ) -> None:
        """Delete command arguments."""
        request = DataModelProtoModule.DeleteCommandArgumentsRequest(
            rules=rules, path=path, command=command, command_id=commandid
        )
        self._impl.delete_command_arguments(request)

    def get_specs(
        self,
        rules: str,
        path: str,
    ) -> dict[str, Any]:
        """Get specifications."""
        request = DataModelProtoModule.GetSpecsRequest(
            rules=rules,
            path=path,
        )
        return _normalize_v1_datamodel_dict_keys(
            MessageToDict(
                self._impl.get_specs(request).member, use_integers_for_enums=True
            )
        )

    def get_static_info(self, rules: str) -> dict[str, Any]:
        """Get static info."""
        request = DataModelProtoModule.GetStaticInfoRequest(rules=rules)
        return _normalize_v1_datamodel_dict_keys(
            MessageToDict(
                self._impl.get_static_info(request).info, use_integers_for_enums=True
            )
        )

    def subscribe_events(self, request_dict: dict[str, Any]) -> list[dict[str, Any]]:
        """Subscribe events."""
        request = DataModelProtoModule.SubscribeEventsRequest()
        ParseDict(_normalize_v1_event_request_dict(request_dict), request)
        return [
            MessageToDict(x, use_integers_for_enums=True)
            for x in self._impl.subscribe_events(request).responses
        ]

    def unsubscribe_events(self, tags: list[str]) -> list[dict[str, Any]]:
        """Unsubscribe events."""
        request = DataModelProtoModule.UnsubscribeEventsRequest()
        request.tags[:] = tags
        return [
            MessageToDict(x, use_integers_for_enums=True)
            for x in self._impl.unsubscribe_events(request).responses
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


convert_path_to_se_path = _v0.convert_path_to_se_path
convert_se_path_to_path = _v0.convert_se_path_to_path

PyCallableStateObject = _v0.PyCallableStateObject
PyStateContainer = _v0.PyStateContainer
PyMenu = _v0.PyMenu
PyParameter = _v0.PyParameter
PyTextual = _v0.PyTextual
PyNumerical = _v0.PyNumerical
PyDictionary = _v0.PyDictionary
PyNamedObjectContainer = _v0.PyNamedObjectContainer
PyAction = _v0.PyAction
PyQuery = _v0.PyQuery
PyCommand = _v0.PyCommand
PyArgumentsSubItem = _v0.PyArgumentsSubItem
PyArguments = _v0.PyArguments
PyArgumentsTextualSubItem = _v0.PyArgumentsTextualSubItem
PyArgumentsNumericalSubItem = _v0.PyArgumentsNumericalSubItem
PyArgumentsDictionarySubItem = _v0.PyArgumentsDictionarySubItem
PyArgumentsParameterSubItem = _v0.PyArgumentsParameterSubItem
PyArgumentsSingletonSubItem = _v0.PyArgumentsSingletonSubItem
arg_class_by_type = _v0.arg_class_by_type
PyMenuGeneric = _v0.PyMenuGeneric
PySimpleMenuGeneric = _v0.PySimpleMenuGeneric
PyNamedObjectContainerGeneric = _v0.PyNamedObjectContainerGeneric

_bool_value_if_none = _v0._bool_value_if_none
true_if_none = _v0.true_if_none
false_if_none = _v0.false_if_none
