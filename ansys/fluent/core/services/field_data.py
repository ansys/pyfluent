"""Wrappers over FieldData grpc service of Fluent."""

from typing import Dict, List, Optional

import grpc
import numpy as np

from ansys.api.fluent.v0 import field_data_pb2 as FieldDataProtoModule
from ansys.api.fluent.v0 import field_data_pb2_grpc as FieldGrpcModule
from ansys.fluent.core.services.error_handler import catch_grpc_error
from ansys.fluent.core.services.interceptors import TracingInterceptor


class FieldDataService:
    def __init__(self, channel: grpc.Channel, metadata):
        tracing_interceptor = TracingInterceptor()
        intercept_channel = grpc.intercept_channel(
            channel, tracing_interceptor
        )
        self.__stub = FieldGrpcModule.FieldDataStub(intercept_channel)
        self.__metadata = metadata

    @catch_grpc_error
    def get_range(self, request):
        return self.__stub.GetRange(request, metadata=self.__metadata)

    @catch_grpc_error
    def get_fields_info(self, request):
        return self.__stub.GetFieldsInfo(request, metadata=self.__metadata)

    @catch_grpc_error
    def get_vector_fields_info(self, request):
        return self.__stub.GetVectorFieldsInfo(
            request, metadata=self.__metadata
        )

    @catch_grpc_error
    def get_surfaces_info(self, request):
        return self.__stub.GetSurfacesInfo(request, metadata=self.__metadata)

    @catch_grpc_error
    def get_fields(self, request):
        return self.__stub.GetFields(request, metadata=self.__metadata)


class FieldInfo:
    """
    Provide field info.

    Methods
    -------
    get_range(field: str, node_value: bool, surface_ids: List[int])
    -> List[float]
        Get field range i.e. minimum and maximum value.

    get_fields_info(self) -> dict
        Get fields information i.e. field name, domain and  section.

    get_vector_fields_info(self) -> dict
        Get vector fields information i.e. vector of and components.

    get_surfaces_info(self) -> dict
        Get surfaces information i.e. surface name, id and type.

    """

    def __init__(self, service: FieldDataService):
        self.__service = service

    def get_range(
        self, field: str, node_value: bool = False, surface_ids: List[int] = []
    ) -> List[float]:
        request = FieldDataProtoModule.GetRangeRequest()
        request.fieldName = field
        request.nodeValue = node_value
        request.surfaceid.extend(
            [FieldDataProtoModule.SurfaceId(id=int(id)) for id in surface_ids]
        )
        response = self.__service.get_range(request)
        return [response.minimum, response.maximum]

    def get_fields_info(self) -> dict:
        request = FieldDataProtoModule.GetFieldsInfoRequest()
        response = self.__service.get_fields_info(request)
        return {
            field_info.displayName: {
                "solver_name": field_info.solverName,
                "section": field_info.section,
                "domain": field_info.domain,
            }
            for field_info in response.fieldInfo
        }

    def get_vector_fields_info(self) -> dict:
        request = FieldDataProtoModule.GetVectorFieldsInfoRequest()
        response = self.__service.get_vector_fields_info(request)
        return {
            vector_field_info.displayName: {
                "x-component": vector_field_info.xComponent,
                "y-component": vector_field_info.yComponent,
                "z-component": vector_field_info.zComponent,
            }
            for vector_field_info in response.vectorFieldInfo
        }

    def get_surfaces_info(self) -> dict:
        request = FieldDataProtoModule.GetSurfacesInfoResponse()
        response = self.__service.get_surfaces_info(request)
        info = {
            surface_info.surfaceName: {
                "surface_id": [surf.id for surf in surface_info.surfaceId],
                "zone_id": surface_info.zoneId.id,
                "zone_type": surface_info.zoneType,
                "type": surface_info.type,
            }
            for surface_info in response.surfaceInfo
        }
        return info


class FieldData:
    """
    Provide the field data.

    Methods
    -------
    get_surfaces(surface_ids: List[int], overset_mesh: bool) -> Dict[int, Dict]
        Get surfaces data i.e. coordinates and connectivity.

    get_scalar_field(
        surface_ids: List[int],
        scalar_field: str,
        node_value: Optional[bool] = True,
        boundary_value: Optional[bool] = False,
    ) -> Dict[int, Dict]:
        Get scalar field data i.e. surface data and associated
        scalar field values.

    get_vector_field(
        surface_ids: List[int],
        vector_field: Optional[str] = "velocity",
        scalar_field: Optional[str] = "",
        node_value: Optional[bool] = False,
    ) -> Dict[int, Dict]:
        Get vector field data i.e. surface data and associated
        scalar and vector field values.

    """

    # data mapping
    _proto_field_type_to_np_data_type = {
        FieldDataProtoModule.FieldType.INT_ARRAY: np.int32,
        FieldDataProtoModule.FieldType.LONG_ARRAY: np.int64,
        FieldDataProtoModule.FieldType.FLOAT_ARRAY: np.float32,
        FieldDataProtoModule.FieldType.DOUBLE_ARRAY: np.float64,
    }
    _chunk_size = 256 * 1024
    _bytes_stream = True

    def __init__(self, service: FieldDataService):
        self.__service = service

    def _extract_fields(self, chunk_iterator):
        def _extract_field(field_datatype, field_size, chunk_iterator):
            if not chunk_iterator.is_active():
                raise RuntimeError("Chunk is Empty.")
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
        # added this but it still gets bypassed 
        # even when is_active() == False 
        if not chunk_iterator.is_active(): 
            raise RuntimeError("Chunk is Empty.")
        fields_data = {}
        for chunk in chunk_iterator:
            payload_info = chunk.payloadInfo
            surface_id = payload_info.surfaceId
            surface_data = fields_data.get(surface_id)
            field = _extract_field(
                self._proto_field_type_to_np_data_type[payload_info.fieldType],
                payload_info.fieldSize,
                chunk_iterator,
            )
            if surface_data:
                surface_data.update({payload_info.fieldName: field})
            else:
                fields_data[surface_id] = {payload_info.fieldName: field}
        return fields_data

    def get_surfaces(
        self, surface_ids: List[int], overset_mesh: bool = False
    ) -> Dict[int, Dict]:
        request = FieldDataProtoModule.GetFieldsRequest(
            provideBytesStream=self._bytes_stream, chunkSize=self._chunk_size
        )
        request.surfaceRequest.extend(
            [
                FieldDataProtoModule.SurfaceRequest(
                    surfaceId=surface_id,
                    oversetMesh=overset_mesh,
                    provideFaces=True,
                )
                for surface_id in surface_ids
            ]
        )
        return self._extract_fields(self.__service.get_fields(request))

    def get_scalar_field(
        self,
        surface_ids: List[int],
        field_name: str,
        node_value: Optional[bool] = True,
        boundary_value: Optional[bool] = False,
    ) -> Dict[int, Dict]:
        request = FieldDataProtoModule.GetFieldsRequest(
            provideBytesStream=self._bytes_stream, chunkSize=self._chunk_size
        )
        request.surfaceRequest.extend(
            [
                FieldDataProtoModule.SurfaceRequest(
                    surfaceId=surface_id,
                    oversetMesh=False,
                    provideFaces=True,
                )
                for surface_id in surface_ids
            ]
        )
        request.scalarFieldRequest.extend(
            [
                FieldDataProtoModule.ScalarFieldRequest(
                    surfaceId=surface_id,
                    scalarFieldName=field_name,
                    dataLocation=FieldDataProtoModule.DataLocation.Nodes
                    if node_value
                    else FieldDataProtoModule.DataLocation.Elements,
                    provideBoundaryValues=boundary_value,
                )
                for surface_id in surface_ids
            ]
        )
        return self._extract_fields(self.__service.get_fields(request))

    def get_vector_field(
        self,
        surface_ids: List[int],
        vector_field: Optional[str] = "velocity",
        field_name: Optional[str] = "",
        node_value: Optional[bool] = False,
    ) -> Dict[int, Dict]:
        request = FieldDataProtoModule.GetFieldsRequest(
            provideBytesStream=self._bytes_stream, chunkSize=self._chunk_size
        )
        request.surfaceRequest.extend(
            [
                FieldDataProtoModule.SurfaceRequest(
                    surfaceId=surface_id,
                    oversetMesh=False,
                    provideFaces=True,
                )
                for surface_id in surface_ids
            ]
        )
        if field_name:
            request.scalarFieldRequest.extend(
                [
                    FieldDataProtoModule.ScalarFieldRequest(
                        surfaceId=surface_id,
                        scalarFieldName=field_name,
                        dataLocation=FieldDataProtoModule.DataLocation.Nodes
                        if node_value
                        else FieldDataProtoModule.DataLocation.Elements,
                        provideBoundaryValues=boundary_value,
                    )
                    for surface_id in surface_ids
                ]
            )
        request.vectorFieldRequest.extend(
            [
                FieldDataProtoModule.VectorFieldRequest(
                    surfaceId=surface_id,
                    vectorFieldName=vector_field,
                    provideFacesCentroid=False,
                    provideFacesAreaNormal=False,
                )
                for surface_id in surface_ids
            ]
        )
        return self._extract_fields(self.__service.get_fields(request))
