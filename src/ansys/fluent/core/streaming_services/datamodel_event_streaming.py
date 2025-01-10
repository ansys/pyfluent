"""Provides a module for datamodel event streaming."""

import logging
import os
import threading
from typing import Callable

from google.protobuf.json_format import MessageToDict

from ansys.api.fluent.v0 import datamodel_se_pb2 as DataModelProtoModule
from ansys.fluent.core.services.datamodel_se import _convert_variant_to_value
from ansys.fluent.core.streaming_services.streaming import StreamingService

network_logger: logging.Logger = logging.getLogger("pyfluent.networking")


class DatamodelEvents(StreamingService):
    """Encapsulates a datamodel events streaming service."""

    def __init__(self, service):
        """Initialize DatamodelEvents."""
        super().__init__(
            stream_begin_method="BeginEventStreaming",
            target=DatamodelEvents._process_streaming,
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

    def _process_streaming(self, id, stream_begin_method, started_evt, *args, **kwargs):
        """Processes datamodel events."""
        request = DataModelProtoModule.EventRequest(*args, **kwargs)
        responses = self._streaming_service.begin_streaming(
            request, started_evt, id=id, stream_begin_method=stream_begin_method
        )
        while True:
            try:
                response: DataModelProtoModule.EventResponse = next(responses)
                if os.getenv("PYFLUENT_HIDE_LOG_SECRETS") != "1":
                    network_logger.debug(
                        f"GRPC_TRACE: RPC = /grpcRemoting.DataModel/BeginEventStreaming, response = {MessageToDict(response)}"
                    )
                with self._lock:
                    self._streaming = True
                    cb = self._cbs.get(response.tag, None)
                    if cb:
                        if response.HasField("createdEventResponse"):
                            childtype = response.createdEventResponse.childtype
                            childname = response.createdEventResponse.childname
                            cb(childtype, childname)
                        elif response.HasField("attributeChangedEventResponse"):
                            value = response.attributeChangedEventResponse.value
                            cb(_convert_variant_to_value(value))
                        elif response.HasField("commandAttributeChangedEventResponse"):
                            value = response.commandAttributeChangedEventResponse.value
                            cb(_convert_variant_to_value(value))
                        elif response.HasField("modifiedEventResponse"):
                            value = response.modifiedEventResponse.value
                            cb(_convert_variant_to_value(value))
                        elif response.HasField("affectedEventResponse"):
                            cb()
                        elif response.HasField("deletedEventResponse"):
                            cb()
                        elif response.HasField("commandExecutedEventResponse"):
                            command = response.commandExecutedEventResponse.command
                            args = _convert_variant_to_value(
                                response.commandExecutedEventResponse.args
                            )
                            cb(command, args)
            except StopIteration:
                break
