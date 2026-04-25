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

"""Provides a module for datamodel event streaming."""

import logging
import threading
from typing import Callable

from google.protobuf.json_format import MessageToDict

from ansys.api.fluent.v0 import datamodel_se_pb2 as DataModelProtoModule
from ansys.fluent.core.services.datamodel_se import _convert_variant_to_value
from ansys.fluent.core.streaming_services.streaming import StreamingService

network_logger: logging.Logger = logging.getLogger("pyfluent.networking")


class _BaseDatamodelEvents(StreamingService):
    """Shared datamodel event streaming implementation."""

    _streaming_rpc_path = "/grpcRemoting.DataModel/BeginEventStreaming"

    def __init__(self, service):
        """Initialize DatamodelEvents."""
        super().__init__(
            stream_begin_method="BeginEventStreaming",
            target=type(self)._process_streaming,
            streaming_service=service,
        )
        self._cbs = {}
        service.event_streaming = self
        self._lock = threading.RLock()

    def register_callback(self, tag: str, cb: Callable):
        """Register a callback."""
        with self._lock:
            self._cbs[tag] = cb

    def unregister_callback(self, tag: str):
        """Unregister a callback."""
        with self._lock:
            self._cbs.pop(tag, None)

    def _make_request(self, *args, **kwargs):
        raise NotImplementedError()

    def _get_response_callback(self, response):
        return self._cbs.get(response.tag, None)

    def _dispatch_response(self, cb: Callable, response) -> None:
        if self._has_created_event_response(response):
            cb(
                self._get_created_event_child_type(response),
                self._get_created_event_child_name(response),
            )
        elif self._has_attribute_changed_event_response(response):
            cb(
                self._convert_variant_to_value(
                    self._get_attribute_changed_value(response)
                )
            )
        elif self._has_command_attribute_changed_event_response(response):
            cb(
                self._convert_variant_to_value(
                    self._get_command_attribute_changed_value(response)
                )
            )
        elif self._has_modified_event_response(response):
            cb(self._convert_variant_to_value(self._get_modified_event_value(response)))
        elif self._has_affected_event_response(response):
            cb()
        elif self._has_deleted_event_response(response):
            cb()
        elif self._has_command_executed_event_response(response):
            cb(
                self._get_command_executed_command(response),
                self._convert_variant_to_value(
                    self._get_command_executed_args(response)
                ),
            )

    def _process_streaming(self, id, stream_begin_method, started_evt, *args, **kwargs):
        """Processes datamodel events."""
        from ansys.fluent.core.module_config import config

        request = self._make_request(*args, **kwargs)
        responses = self._streaming_service.begin_streaming(
            request, started_evt, id=id, stream_begin_method=stream_begin_method
        )
        while True:
            try:
                response = next(responses)
                if not config.hide_log_secrets:
                    network_logger.debug(
                        f"GRPC_TRACE: RPC = {self._streaming_rpc_path}, response = {MessageToDict(response)}"
                    )
                with self._lock:
                    self._streaming = True
                    cb = self._get_response_callback(response)
                    if cb:
                        self._dispatch_response(cb, response)
            except StopIteration:
                break

    def _has_created_event_response(self, response) -> bool:
        raise NotImplementedError()

    def _get_created_event_child_type(self, response) -> str:
        raise NotImplementedError()

    def _get_created_event_child_name(self, response) -> str:
        raise NotImplementedError()

    def _has_attribute_changed_event_response(self, response) -> bool:
        raise NotImplementedError()

    def _get_attribute_changed_value(self, response):
        raise NotImplementedError()

    def _has_command_attribute_changed_event_response(self, response) -> bool:
        raise NotImplementedError()

    def _get_command_attribute_changed_value(self, response):
        raise NotImplementedError()

    def _has_modified_event_response(self, response) -> bool:
        raise NotImplementedError()

    def _get_modified_event_value(self, response):
        raise NotImplementedError()

    def _has_affected_event_response(self, response) -> bool:
        raise NotImplementedError()

    def _has_deleted_event_response(self, response) -> bool:
        raise NotImplementedError()

    def _has_command_executed_event_response(self, response) -> bool:
        raise NotImplementedError()

    def _get_command_executed_command(self, response) -> str:
        raise NotImplementedError()

    def _get_command_executed_args(self, response):
        raise NotImplementedError()

    def _convert_variant_to_value(self, value):
        raise NotImplementedError()


class DatamodelEvents(_BaseDatamodelEvents):
    """Encapsulates a datamodel events streaming service."""

    def __init__(self, service):
        """Initialize DatamodelEvents."""
        super().__init__(service)

    def _make_request(self, *args, **kwargs):
        return DataModelProtoModule.EventRequest(*args, **kwargs)

    def _has_created_event_response(self, response) -> bool:
        return response.HasField("createdEventResponse")

    def _get_created_event_child_type(self, response) -> str:
        return response.createdEventResponse.childtype

    def _get_created_event_child_name(self, response) -> str:
        return response.createdEventResponse.childname

    def _has_attribute_changed_event_response(self, response) -> bool:
        return response.HasField("attributeChangedEventResponse")

    def _get_attribute_changed_value(self, response):
        return response.attributeChangedEventResponse.value

    def _has_command_attribute_changed_event_response(self, response) -> bool:
        return response.HasField("commandAttributeChangedEventResponse")

    def _get_command_attribute_changed_value(self, response):
        return response.commandAttributeChangedEventResponse.value

    def _has_modified_event_response(self, response) -> bool:
        return response.HasField("modifiedEventResponse")

    def _get_modified_event_value(self, response):
        return response.modifiedEventResponse.value

    def _has_affected_event_response(self, response) -> bool:
        return response.HasField("affectedEventResponse")

    def _has_deleted_event_response(self, response) -> bool:
        return response.HasField("deletedEventResponse")

    def _has_command_executed_event_response(self, response) -> bool:
        return response.HasField("commandExecutedEventResponse")

    def _get_command_executed_command(self, response) -> str:
        return response.commandExecutedEventResponse.command

    def _get_command_executed_args(self, response):
        return response.commandExecutedEventResponse.args

    def _convert_variant_to_value(self, value):
        return _convert_variant_to_value(value)
