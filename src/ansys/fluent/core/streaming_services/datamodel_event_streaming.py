import threading
from typing import Callable

from ansys.api.fluent.v0 import datamodel_se_pb2 as DataModelProtoModule
from ansys.fluent.core.services.datamodel_se import _convert_variant_to_value
from ansys.fluent.core.streaming_services.streaming import StreamingService


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

    def register_callback(self, tag: str, obj, cb: Callable):
        """Register a callback."""
        with self._lock:
            self._cbs[tag] = obj, cb

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
                with self._lock:
                    self._streaming = True
                    for tag, cb in self._cbs.items():
                        if tag == response.tag:
                            if response.HasField("createdEventResponse"):
                                childtype = response.createdEventResponse.childtype
                                childname = response.createdEventResponse.childname
                                child = getattr(cb[0], childtype)[childname]
                                cb[1](child)
                            elif (
                                response.HasField("modifiedEventResponse")
                                or response.HasField("deletedEventResponse")
                                or response.HasField("affectedEventResponse")
                                or response.HasField("attributeChangedEventResponse")
                                or response.HasField(
                                    "commandAttributeChangedEventResponse"
                                )
                            ):
                                cb[1](cb[0])
                            elif response.HasField("commandExecutedEventResponse"):
                                command = response.commandExecutedEventResponse.command
                                args = _convert_variant_to_value(
                                    response.commandExecutedEventResponse.args
                                )
                                cb[1](cb[0], command, args)
            except StopIteration:
                break
