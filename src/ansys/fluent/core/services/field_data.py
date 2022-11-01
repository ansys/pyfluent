"""Wrappers over FieldData gRPC service of Fluent."""
from enum import IntEnum
from functools import reduce
from typing import Dict, List, Optional, Tuple, Union

import grpc
import numpy as np

from ansys.api.fluent.v0 import field_data_pb2 as FieldDataProtoModule
from ansys.api.fluent.v0 import field_data_pb2_grpc as FieldGrpcModule
from ansys.fluent.core.services.error_handler import catch_grpc_error
from ansys.fluent.core.services.interceptors import TracingInterceptor


class FieldDataService:
    def __init__(self, channel: grpc.Channel, metadata):
        tracing_interceptor = TracingInterceptor()
        intercept_channel = grpc.intercept_channel(channel, tracing_interceptor)
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
        return self.__stub.GetVectorFieldsInfo(request, metadata=self.__metadata)

    @catch_grpc_error
    def get_surfaces_info(self, request):
        return self.__stub.GetSurfacesInfo(request, metadata=self.__metadata)

    @catch_grpc_error
    def get_fields(self, request):
        return self.__stub.GetFields(request, metadata=self.__metadata)


class FieldInfo:
    """Provides access to Fluent field information.

    Methods
    -------
    get_range(field: str, node_value: bool, surface_ids: List[int])
    -> List[float]
        Get the range (minimum and maximum values) of the field.

    get_fields_info(self) -> dict
        Get fields information (field name, domain, and section).

    get_vector_fields_info(self) -> dict
        Get vector fields information (vector of and components).

    get_surfaces_info(self) -> dict
        Get surfaces information (surface name, ID, and type).
    """

    def __init__(self, service: FieldDataService):
        self._service = service

    def get_range(
        self, field: str, node_value: bool = False, surface_ids: List[int] = None
    ) -> List[float]:
        if not surface_ids:
            surface_ids = []
        request = FieldDataProtoModule.GetRangeRequest()
        request.fieldName = field
        request.nodeValue = node_value
        request.surfaceid.extend(
            [FieldDataProtoModule.SurfaceId(id=int(id)) for id in surface_ids]
        )
        response = self._service.get_range(request)
        return [response.minimum, response.maximum]

    def get_fields_info(self) -> dict:
        request = FieldDataProtoModule.GetFieldsInfoRequest()
        response = self._service.get_fields_info(request)
        return {
            field_info.solverName: {
                "display_name": field_info.displayName,
                "section": field_info.section,
                "domain": field_info.domain,
            }
            for field_info in response.fieldInfo
        }

    def get_vector_fields_info(self) -> dict:
        request = FieldDataProtoModule.GetVectorFieldsInfoRequest()
        response = self._service.get_vector_fields_info(request)
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
        response = self._service.get_surfaces_info(request)
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


class SurfaceDataType(IntEnum):
    """Provides surface data types."""

    Vertices = 1
    FacesConnectivity = 2
    FacesNormal = 3
    FacesCentroid = 4


class FieldTransaction:
    """Populates Fluent field data on surfaces."""

    def __init__(self, service: FieldDataService, field_info: FieldInfo):
        self._service = service
        self._field_info = field_info
        self._fields_request = get_fields_request()

    def add_surfaces_request(
        self,
        surface_ids: Optional[List[int]] = None,
        surface_names: Optional[List[str]] = None,
        overset_mesh: Optional[bool] = False,
        provide_vertices: Optional[bool] = True,
        provide_faces: Optional[bool] = True,
        provide_faces_centroid: Optional[bool] = False,
        provide_faces_normal: Optional[bool] = False,
    ) -> None:
        """Add request to get surface data (vertices, face connectivity,
        centroids, and normals).

        Parameters
        ----------
        surface_ids : List[int], optional
            List of surface IDS for the surface data.
        surface_names: List[str], optional
            List of surface names for the surface data.
        overset_mesh : bool, optional
            Whether to get the overset met. The default is ``False``.
        provide_vertices : bool, optional
            Whether to get node coordinates. The default is ``True``.
        provide_faces : bool, optional
            Whether to get face connectivity. The default is ``True``.
        provide_faces_centroid : bool, optional
            Whether to get face centroids. The default is ``False``.
        provide_faces_normal : bool, optional
            Whether to get faces normal. The default is ``False``

        Returns
        -------
        None
        """
        surface_ids = _get_surface_ids(
            field_info=self._field_info,
            surface_ids=surface_ids,
            surface_names=surface_names,
        )
        self._fields_request.surfaceRequest.extend(
            [
                FieldDataProtoModule.SurfaceRequest(
                    surfaceId=surface_id,
                    oversetMesh=overset_mesh,
                    provideFaces=provide_faces,
                    provideVertices=provide_vertices,
                    provideFacesCentroid=provide_faces_centroid,
                    provideFacesNormal=provide_faces_normal,
                )
                for surface_id in surface_ids
            ]
        )

    def add_scalar_fields_request(
        self,
        field_name: str,
        surface_ids: Optional[List[int]] = None,
        surface_names: Optional[List[str]] = None,
        node_value: Optional[bool] = True,
        boundary_value: Optional[bool] = False,
    ) -> None:
        """Add request to get scalar field data on surfaces.

        Parameters
        ----------
        field_name : str
            Name of the scalar field.
        surface_ids : List[int], optional
            List of surface IDs for scalar field data.
        surface_names: List[str], optional
            List of surface names for scalar field data.
        node_value : bool, optional
            Whether to provide the nodal location. The default is ``True``. If
            ``False``, the element location is provided.
        boundary_value : bool, optional
            Whether to provide the slip velocity at the wall boundaries. The default
            is ``False``. When ``True``, no slip velocity is provided.

        Returns
        -------
        None
        """
        surface_ids = _get_surface_ids(
            field_info=self._field_info,
            surface_ids=surface_ids,
            surface_names=surface_names,
        )
        self._fields_request.scalarFieldRequest.extend(
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

    def add_vector_fields_request(
        self,
        field_name: str,
        surface_ids: Optional[List[int]] = None,
        surface_names: Optional[List[str]] = None,
    ) -> None:
        """Add request to get vector field data on surfaces.

        Parameters
        ----------
        field_name : str
            Name of the vector field.
        surface_ids : List[int], optional
            List of surface IDs for vector field data.
        surface_names: List[str], optional
            List of surface names for vector field data.

        Returns
        -------
        None
        """
        surface_ids = _get_surface_ids(
            field_info=self._field_info,
            surface_ids=surface_ids,
            surface_names=surface_names,
        )
        self._fields_request.vectorFieldRequest.extend(
            [
                FieldDataProtoModule.VectorFieldRequest(
                    surfaceId=surface_id,
                    vectorFieldName=field_name,
                )
                for surface_id in surface_ids
            ]
        )

    def add_pathlines_fields_request(
        self,
        field_name: str,
        surface_ids: Optional[List[int]] = None,
        surface_names: Optional[List[str]] = None,
        additional_field_name: Optional[str] = "",
        provide_particle_time_field: Optional[bool] = False,
        node_value: Optional[bool] = True,
        steps: Optional[int] = 500,
        step_size: Optional[float] = 0.01,
        skip: Optional[int] = 0,
        reverse: Optional[bool] = False,
        accuracy_control_on: Optional[bool] = False,
        tolerance: Optional[float] = 0.001,
        coarsen: Optional[int] = 1,
        velocity_domain: Optional[str] = "all-phases",
        zones: Optional[list] = [],
    ) -> None:
        """Add request to get pathlines field on surfaces.

        Parameters
        ----------
        field_name : str
            Name of the scalar field to color pathlines.
        surface_ids : List[int], optional
            List of surface IDs for pathlines field data.
        surface_names : List[str], optional
            List of surface names for pathlines field data.
        additional_field_name : str, optional
            Additional field if required.
        provide_particle_time_field: bool, optional
            Whether to provide the particle time. The default is ``False``.
        node_value : bool, optional
                    Whether to provide the nodal values. The default is ``True``. If
                    ``False``, element values are provided.
        steps: int, optional
            Pathlines steps. The default is ``500``
        step_size: float, optional
            Pathlines step size. The default is ``0.01``.
        skip: int, optional
            Pathlines to skip. The default is ``0``.
        reverse: bool, optional
            Whether to draw pathlines in reverse direction. The default is ``False``.
        tolerance: float, optional
            Pathlines tolerance. The default is ``0.001``.
        coarsen: int, optional
            Pathlines coarsen. The default is ``1``.
        velocity_domain: str, optional
            Domain for pathlines. The default is ``"all-phases"``.
        zones: list, optional
            Zones for pathlines. The default is ``[]``.
        Returns
        -------
        None
        """
        surface_ids = _get_surface_ids(
            field_info=self._field_info,
            surface_ids=surface_ids,
            surface_names=surface_names,
        )
        self._fields_request.pathlinesFieldRequest.extend(
            [
                FieldDataProtoModule.PathlinesFieldRequest(
                    surfaceId=surface_id,
                    field=field_name,
                    additionalField=additional_field_name,
                    provideParticleTimeField=provide_particle_time_field,
                    dataLocation=FieldDataProtoModule.DataLocation.Nodes
                    if node_value
                    else FieldDataProtoModule.DataLocation.Elements,
                    steps=steps,
                    stepSize=step_size,
                    skip=skip,
                    reverse=reverse,
                    accuracyControlOn=accuracy_control_on,
                    tolerance=tolerance,
                    coarsen=coarsen,
                    velocityDomain=velocity_domain,
                    zones=zones,
                )
                for surface_id in surface_ids
            ]
        )

    def get_fields(self) -> Dict[Union[int, Tuple], Dict[int, Dict[str, np.array]]]:
        """Get data for previously added requests and then clear all requests.

        Returns
        -------
        Dict[int, Dict[int, Dict[str, np.array]]]
            Data is returned as dictionary of dictionaries in the following structure:
            tag Union[int, Tuple]-> surface_id [int] -> field_name [str] -> field_data[np.array]

            The tag is a tuple for Fluent 2023 R1 or later.
        """
        return extract_fields(self._service.get_fields(self._fields_request))

    def __call__(self):
        self.get_fields()


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


def _get_surface_ids(
    field_info: FieldInfo,
    surface_ids: Optional[List[int]] = None,
    surface_names: Optional[List[str]] = None,
    surface_name: Optional[str] = None,
) -> List[int]:
    """Get surface ids' based on surface names or ids'.

    Parameters
    ----------
    surface_ids : List[int], optional
        List of surface IDs.
    surface_names: List[str], optional
        List of surface names.
    surface_name: str, optional
        List of surface name.

    Returns
    -------
    List[int]
    """
    if surface_ids and (surface_name or surface_names):
        raise RuntimeError("Please provide either surface names or surface ids.")
    if not surface_ids:
        surface_ids = []
        if surface_names:
            for surface_name in surface_names:
                surface_ids.append(
                    field_info.get_surfaces_info()[surface_name]["surface_id"]
                )
        elif surface_name:
            surface_ids = field_info.get_surfaces_info()[surface_name]["surface_id"]
        else:
            raise RuntimeError("Please provide either surface names or surface ids.")
    return surface_ids


def get_fields_request():
    """Populates a new field request."""
    return FieldDataProtoModule.GetFieldsRequest(
        provideBytesStream=_FieldDataConstants.bytes_stream,
        chunkSize=_FieldDataConstants.chunk_size,
    )


def merge_pathlines_data(pathlines_data, field):
    """Merge multiple pathlines for a surface to create a single mesh
    object."""

    data = {}
    for surface_id, data_for_surface in pathlines_data.items():
        if "pathlines-count" in data_for_surface:
            pathlines_count = data_for_surface["pathlines-count"][0]
            pathline_count = 0
            pathline_connectivity = None
            pathline_positions = None
            pathline_field = None
            while pathline_count < pathlines_count:
                line_id = f"pathline-{pathline_count}-line-data"
                position_id = f"pathline-{pathline_count}-position-data"
                field_id = f"pathline-{pathline_count}-field-data"

                pathline_positions = (
                    data_for_surface[position_id]
                    if pathline_positions is None
                    else np.concatenate(
                        (pathline_positions, data_for_surface[position_id])
                    )
                )
                pathline_connectivity = (
                    data_for_surface[line_id]
                    if pathline_connectivity is None
                    else np.concatenate(
                        (pathline_connectivity, data_for_surface[line_id])
                    )
                )
                pathline_field = (
                    data_for_surface[field_id]
                    if pathline_field is None
                    else np.concatenate((pathline_field, data_for_surface[field_id]))
                )
                pathline_count = pathline_count + 1

            data[surface_id] = {
                "faces": pathline_connectivity,
                "vertices": pathline_positions,
                field: pathline_field,
            }
    return data


def extract_fields(chunk_iterator):
    """Extracts field data via a server call."""

    def _get_tag_for_surface_request(surface_request):
        return (("type", "surface-data"),)

    def _get_tag_for_vector_field_request(vector_field_request):
        return (("type", "vector-field"),)

    def _get_tag_for_scalar_field_request(scalar_field_request):
        return (
            ("type", "scalar-field"),
            ("dataLocation", scalar_field_request.dataLocation),
            ("boundaryValues", scalar_field_request.provideBoundaryValues),
        )

    def _get_tag_for_pathlines_field_request(pathlines_field_request):
        return (("type", "pathlines-field"), ("field", pathlines_field_request.field))

    def _extract_field(field_datatype, field_size, chunk_iterator):
        if not chunk_iterator.is_active():
            raise RuntimeError(
                "Unexpectedly encountered empty chunk during field extraction."
            )
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
        field = _extract_field(
            _FieldDataConstants.proto_field_type_to_np_data_type[
                payload_info.fieldType
            ],
            payload_info.fieldSize,
            chunk_iterator,
        )

        surface_id = payload_info.surfaceId

        field_request_info = payload_info.fieldRequestInfo
        request_type = field_request_info.WhichOneof("request")
        if request_type is not None:
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
        else:
            payload_tag_id = reduce(
                lambda x, y: x | y,
                [self._payloadTags[tag] for tag in payload_info.payloadTag] or [0],
            )
        payload_data = fields_data.get(payload_tag_id)
        if not payload_data:
            payload_data = fields_data[payload_tag_id] = {}
        surface_data = payload_data.get(surface_id)
        if surface_data:
            surface_data.update({payload_info.fieldName: field})
        else:
            payload_data[surface_id] = {payload_info.fieldName: field}
    return fields_data


class FieldData:
    """Provides access to Fluent field data on surfaces."""

    def __init__(self, service: FieldDataService, field_info: FieldInfo):
        self._service = service
        self._field_info = field_info

    def new_transaction(self):
        return FieldTransaction(self._service, self._field_info)

    def get_surface_data(
        self,
        data_type: SurfaceDataType,
        surface_ids: Optional[List[int]] = None,
        surface_name: Optional[str] = None,
        overset_mesh: Optional[bool] = False,
    ) -> Dict[int, np.array]:
        """Get surface data (vertices, faces connectivity, centroids, and
        normals).

        Parameters
        ----------
        data_type : SurfaceDataType
            SurfaceDataType Enum member.
        surface_ids : List[int], optional
            List of surface IDs for the surface data.
        surface_name : str, optional
            Surface name for the surface data.
        overset_mesh : bool, optional
            Whether to provide the overset method. The default is ``False``.

        Returns
        -------
        Dict[int, np.array]
            Dictionary containing a map of surface IDs to surface data.
        """
        surface_ids = _get_surface_ids(
            field_info=self._field_info,
            surface_ids=surface_ids,
            surface_name=surface_name,
        )
        fields_request = get_fields_request()
        fields_request.surfaceRequest.extend(
            [
                FieldDataProtoModule.SurfaceRequest(
                    surfaceId=surface_id,
                    oversetMesh=overset_mesh,
                    provideFaces=data_type == SurfaceDataType.FacesConnectivity,
                    provideVertices=data_type == SurfaceDataType.Vertices,
                    provideFacesCentroid=data_type == SurfaceDataType.FacesCentroid,
                    provideFacesNormal=data_type == SurfaceDataType.FacesNormal,
                )
                for surface_id in surface_ids
            ]
        )
        enum_to_field_name = {
            SurfaceDataType.FacesConnectivity: "faces",
            SurfaceDataType.Vertices: "vertices",
            SurfaceDataType.FacesCentroid: "centroid",
            SurfaceDataType.FacesNormal: "face-normal",
        }
        fields = extract_fields(self._service.get_fields(fields_request))
        surface_data = next(iter(fields.values()))
        return {
            surface_id: surface_data[surface_id][enum_to_field_name[data_type]]
            for surface_id in surface_ids
        }

    def get_scalar_field_data(
        self,
        field_name: str,
        surface_ids: Optional[List[int]] = None,
        surface_name: Optional[str] = None,
        node_value: Optional[bool] = True,
        boundary_value: Optional[bool] = False,
    ) -> Dict[int, np.array]:
        """Get scalar field data on a surface.

        Parameters
        ----------
        field_name : str
            Name of the scalar field.
        surface_ids : List[int], optional
            List of surface IDs for scalar field data.
        surface_name: str, optional
            Surface Name for scalar field data.
        node_value : bool, optional
            Whether to provide data for the nodal location. The default is ``True``.
            When ``False``, data is provided for the element location.
        boundary_value : bool, optional
            Whether to provide slip velocity at the wall boundaries. The default is
            ``False``. When ``True``, no slip velocity is provided.

        Returns
        -------
        Dict[int, np.array]
            Dictionary containing a map of surface IDs to the scalar field.
        """
        surface_ids = _get_surface_ids(
            field_info=self._field_info,
            surface_ids=surface_ids,
            surface_name=surface_name,
        )
        fields_request = get_fields_request()
        fields_request.scalarFieldRequest.extend(
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

        fields = extract_fields(self._service.get_fields(fields_request))
        scalar_field_data = next(iter(fields.values()))
        return {
            surface_id: scalar_field_data[surface_id][field_name]
            for surface_id in surface_ids
        }

    def get_vector_field_data(
        self,
        field_name: str,
        surface_ids: Optional[List[int]] = None,
        surface_name: Optional[str] = None,
    ) -> Dict[int, Tuple[np.array, float]]:
        """Get vector field data on a surface.

        Parameters
        ----------
        field_name : str
            Name of the vector field.
        surface_ids : List[int], optional
            List of surface IDs for vector field data.
        surface_name: str, optional
            Surface Name for vector field data.

        Returns
        -------
        Dict[int, Tuple[np.array, float]]
            Dictionary containing a map of surface IDs to a tuple of vector field and vector scale.
        """
        surface_ids = _get_surface_ids(
            field_info=self._field_info,
            surface_ids=surface_ids,
            surface_name=surface_name,
        )
        fields_request = get_fields_request()
        fields_request.vectorFieldRequest.extend(
            [
                FieldDataProtoModule.VectorFieldRequest(
                    surfaceId=surface_id,
                    vectorFieldName=field_name,
                )
                for surface_id in surface_ids
            ]
        )
        fields = extract_fields(self._service.get_fields(fields_request))
        vector_field_data = next(iter(fields.values()))
        return {
            surface_id: (
                vector_field_data[surface_id][field_name],
                vector_field_data[surface_id]["vector-scale"][0],
            )
            for surface_id in surface_ids
        }

    def get_pathlines_field_data(
        self,
        field_name: str,
        surface_ids: Optional[List[int]] = None,
        surface_name: Optional[str] = None,
        additional_field_name: Optional[str] = "",
        provide_particle_time_field: Optional[bool] = False,
        node_value: Optional[bool] = True,
        steps: Optional[int] = 500,
        step_size: Optional[float] = 0.01,
        skip: Optional[int] = 0,
        reverse: Optional[bool] = False,
        accuracy_control_on: Optional[bool] = False,
        tolerance: Optional[float] = 0.001,
        coarsen: Optional[int] = 1,
        velocity_domain: Optional[str] = "all-phases",
        zones: Optional[list] = [],
    ) -> Dict[int, Dict[str, np.array]]:
        """Get pathlines field data on a surface.

        Parameters
        ----------
        field_name : str
            Name of the scalar field to color pathlines.
        surface_ids : List[int], optional
            List of surface IDs for pathlines field data.
        surface_name : str, optional
            Surface name for pathlines field data.
        additional_field_name : str, optional
            Additional field if required.
        provide_particle_time_field: bool, optional
            Whether to provide the particle time. The default is ``False``.
        node_value : bool, optional
                    Whether to provide the nodal values. The default is ``True``. If
                    ``False``, element values are provided.
        steps: int, optional
            Pathlines steps. The default is ``500``
        step_size: float, optional
            Pathlines step size. The default is ``0.01``.
        skip: int, optional
            Pathlines to skip. The default is ``0``.
        reverse: bool, optional
            Whether to draw pathlines in reverse direction. The default is ``False``.
        tolerance: float, optional
            Pathlines tolerance. The default is ``0.001``.
        coarsen: int, optional
            Pathlines coarsen. The default is ``1``.
        velocity_domain: str, optional
            Domain for pathlines. The default is ``"all-phases"``.
        zones: list, optional
            Zones for pathlines. The default is ``[]``.

        Returns
        -------
        Dict[int, Dict[str, np.array]]
            Dictionary containing a map of surface IDs to the pathline data
            For example, pathlines connectivity, vertices, and field.
        """
        surface_ids = _get_surface_ids(
            field_info=self._field_info,
            surface_ids=surface_ids,
            surface_name=surface_name,
        )
        fields_request = get_fields_request()
        fields_request.pathlinesFieldRequest.extend(
            [
                FieldDataProtoModule.PathlinesFieldRequest(
                    surfaceId=surface_id,
                    field=field_name,
                    additionalField=additional_field_name,
                    provideParticleTimeField=provide_particle_time_field,
                    dataLocation=FieldDataProtoModule.DataLocation.Nodes
                    if node_value
                    else FieldDataProtoModule.DataLocation.Elements,
                    steps=steps,
                    stepSize=step_size,
                    skip=skip,
                    reverse=reverse,
                    accuracyControlOn=accuracy_control_on,
                    tolerance=tolerance,
                    coarsen=coarsen,
                    velocityDomain=velocity_domain,
                    zones=zones,
                )
                for surface_id in surface_ids
            ]
        )
        fields = extract_fields(self._service.get_fields(fields_request))
        vector_field_data = next(iter(fields.values()))
        pathlines_data = next(iter(fields.values()))
        return merge_pathlines_data(pathlines_data, field_name)
