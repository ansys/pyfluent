"""Module for monitors management."""

import threading
from typing import Dict, List, Tuple, Union

import numpy as np
import pandas as pd

from ansys.fluent.core.streaming_services.streaming import StreamingService
from ansys.api.fluent.v0 import field_data_pb2 as FieldDataProtoModule

class _FieldDataConstants:
    """Defines constants for Fluent field data."""

    # data mapping
    proto_field_type_to_np_data_type = {
        FieldDataProtoModule.FieldType.INT_ARRAY: np.int32,
        FieldDataProtoModule.FieldType.LONG_ARRAY: np.int64,
        FieldDataProtoModule.FieldType.FLOAT_ARRAY: np.float32,
        FieldDataProtoModule.FieldType.DOUBLE_ARRAY: np.float64,
    }
    chunk_size = 256 * 1024
    bytes_stream = True
    payloadTags = {
        FieldDataProtoModule.PayloadTag.OVERSET_MESH: 1,
        FieldDataProtoModule.PayloadTag.ELEMENT_LOCATION: 2,
        FieldDataProtoModule.PayloadTag.NODE_LOCATION: 4,
        FieldDataProtoModule.PayloadTag.BOUNDARY_VALUES: 8,
    }

def extract_fields(chunk_iterator, field_data_streaming):
    """Extracts field data via a server call."""
   
    def _get_tag_for_surface_request(surface_request):
        return (("type", "surface-data"),)
        
    def _extract_field(field_datatype, field_size, chunk_iterator):
        field_arr = np.empty(field_size, dtype=field_datatype)
        field_datatype_item_size = np.dtype(field_datatype).itemsize
        index = 0
        for chunk in chunk_iterator:
            if chunk.bytePayload:
                count = min(
                    len(chunk.bytePayload) // field_datatype_item_size,
                    field_size - index,
                )
                field_arr[index : index + count] = np.frombuffer(
                    chunk.bytePayload, field_datatype, count=count
                )
                index += count
                if index == field_size:
                    return field_arr
            else:
                payload = (
                    chunk.floatPayload.payload
                    or chunk.intPayload.payload
                    or chunk.doublePayload.payload
                    or chunk.longPayload.payload
                )
                count = len(payload)
                field_arr[index : index + count] = np.fromiter(
                    payload, dtype=field_datatype
                )
                index += count
                if index == field_size:
                    return field_arr

    fields_data = {}
    for chunk in chunk_iterator:
        payload_info = chunk.payloadInfo       

        surface_id = payload_info.surfaceId 
        field_request_info = payload_info.fieldRequestInfo
        request_type = field_request_info.WhichOneof("request")
        
        payload_tag_id = (
            _get_tag_for_surface_request(field_request_info.surfaceRequest)
            if request_type == "surfaceRequest"
            else _get_tag_for_scalar_field_request(
                field_request_info.scalarFieldRequest
            )
            if request_type == "scalarFieldRequest"
            else _get_tag_for_vector_field_request(
                field_request_info.vectorFieldRequest
            )
            if request_type == "vectorFieldRequest"
            else _get_tag_for_pathlines_field_request(
                field_request_info.pathlinesFieldRequest
            )
            if request_type == "pathlinesFieldRequest"
            else None
        )
        field = None 
        if payload_tag_id is not None:            
            field = _extract_field(
                _FieldDataConstants.proto_field_type_to_np_data_type[
                    payload_info.fieldType
                ],
                payload_info.fieldSize,
                chunk_iterator,
            )
        
        for callback_map in field_data_streaming._service_callbacks.values():
            callback, args, kwargs = callback_map
            callback(surface_id, payload_info.fieldName, field, *args, **kwargs)
                                

    
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
        extract_fields(self._streaming_service.begin_streaming(request, started_evt), self)
        
                

   
