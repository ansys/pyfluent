"""Module for monitors management."""

import threading
from typing import Dict, List, Tuple, Union

import numpy as np
import pandas as pd

from ansys.fluent.core.streaming_services.streaming import StreamingService
from ansys.api.fluent.v0 import field_data_pb2 as FieldDataProtoModule
from ansys.fluent.core.services.field_data import ChunkParser
                               
class FieldDataStreaming(StreamingService):
    """Manages monitors (Fluent residuals and report definitions monitors).

    Parameters
    ----------
    session_id : str
        Session ID.
    service : MonitorsService
        Monitors streaming service.
    """

    def __init__(self, session_id: str, service):
        super().__init__(
            target=FieldDataStreaming._process_streaming,
            streaming_service=service,
        )
        self._session_id: str = session_id
        self._lock_refresh: threading.Lock = threading.Lock()


    def _process_streaming(self, started_evt, *args, **kwargs):
        """Performs processes on transcript depending on the callback
        functions."""
        request=FieldDataProtoModule.BeginFieldsStreamingRequest(*args, **kwargs)
        ChunkParser(self).extract_fields(self._streaming_service.begin_streaming(request, started_evt))
        
                

   
