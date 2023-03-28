"""Module for monitors management."""

import threading

from ansys.api.fluent.v0 import field_data_pb2 as FieldDataProtoModule
from ansys.fluent.core.services.field_data import ChunkParser
from ansys.fluent.core.streaming_services.streaming import StreamingService
from typing import Callable, List

class FieldDataStreaming(StreamingService):
    """Class wrapping the Field gRPC streaming service of Fluent.

    Parameters
    ----------
    session_id : str
        Session ID.
    service : FieldDataService
        FieldData streaming service.
    """

    def __init__(self, session_id: str, service):
        super().__init__(
            target=FieldDataStreaming._process_streaming,
            streaming_service=service,
        )
        self._session_id: str = session_id
        self._lock_refresh: threading.Lock = threading.Lock()
       
    def _process_streaming(self, started_evt, *args, **kwargs):
        """Processes on field data streaming."""
        request = FieldDataProtoModule.BeginFieldsStreamingRequest(*args, **kwargs)
        ChunkParser(self).extract_fields(
            self._streaming_service.begin_streaming(request, started_evt)
        )
        
    def callbacks(self) -> List[List[Callable,[],{}]]:
        """Provides list of callbacks along with arguments and keyword arguments"""
        return self._service_callbacks.values()    
