"""Wrappers over FieldData gRPC service of Fluent."""
import difflib
from enum import IntEnum
from functools import partial, reduce
from typing import Callable, Dict, List, Optional, Tuple, Union

import grpc
import numpy as np

from ansys.api.fluent.v0 import field_data_pb2 as FieldDataProtoModule
from ansys.api.fluent.v0 import field_data_pb2_grpc as FieldGrpcModule
from ansys.fluent.core.services.error_handler import catch_grpc_error
from ansys.fluent.core.services.interceptors import TracingInterceptor

# this can be switched to False in scenarios where the field_data request inputs are
# fed by results of field_info queries, which might be true in GUI code.
validate_inputs = True


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


def closest_allowed_names(trial_name: str, allowed_names: str) -> List[str]:
    f = partial(difflib.get_close_matches, trial_name, allowed_names)
    return f(cutoff=0.6, n=5) or f(cutoff=0.3, n=1)


def allowed_name_error_message(
    context: str, trial_name: str, allowed_values: List[str]
) -> str:
    message = f"{trial_name} is not an allowed {context} name.\n"
    matches = closest_allowed_names(trial_name, allowed_values)
    if matches:
        message += f"The most similar names are: {', '.join(matches)}."
    return message


def unavailable_field_error_message(context: str, field_name: str) -> str:
    return f"{field_name} is not a currently available {context}."


class FieldNameError(ValueError):
    pass


class ScalarFieldNameError(FieldNameError):
    def __init__(self, field_name: str, allowed_values: List[str]):
        self.field_name = field_name
        super().__init__(
            allowed_name_error_message("scalar field", field_name, allowed_values)
        )


class VectorFieldNameError(FieldNameError):
    def __init__(self, field_name: str, allowed_values: List[str]):
        self.field_name = field_name
        super().__init__(
            allowed_name_error_message("vector field", field_name, allowed_values)
        )


class FieldUnavailable(RuntimeError):
    pass


class ScalarFieldUnavailable(FieldUnavailable):
    def __init__(self, field_name: str):
        self.field_name = field_name
        super().__init__(unavailable_field_error_message("scalar field", field_name))


class VectorFieldUnavailable(FieldUnavailable):
    def __init__(self, field_name: str):
        self.field_name = field_name
        super().__init__(unavailable_field_error_message("vector field", field_name))


class SurfaceNameError(ValueError):
    def __init__(self, surface_name: str, allowed_values: List[str]):
        self.surface_name = surface_name
        super().__init__(
            allowed_name_error_message("surface", surface_name, allowed_values)
        )


class SurfaceDataType(IntEnum):
    """Provides surface data types."""

    Vertices = 1
    FacesConnectivity = 2
    FacesNormal = 3
    FacesCentroid = 4


class _AllowedNames:
    def __init__(self, field_info: FieldInfo):
        self._field_info = field_info

    def is_valid(self, name, respect_data_valid=True):
        return name in self(respect_data_valid)


class _AllowedFieldNames(_AllowedNames):
    def __init__(self, field_info: FieldInfo, is_data_valid: Callable[[], bool]):
        super().__init__(field_info=field_info)
        self._is_data_valid = is_data_valid

    def valid_name(self, field_name):
        if validate_inputs:
            names = self
            if not names.is_valid(field_name, respect_data_valid=False):
                raise self._field_name_error(
                    field_name=field_name,
                    allowed_values=names(respect_data_valid=False),
                )
            if not names.is_valid(field_name, respect_data_valid=True):
                raise self._field_unavailable_error(field_name)
        return field_name


class _AllowedSurfaceNames(_AllowedNames):
    def __call__(self, respect_data_valid: bool = True) -> List[str]:
        return self._field_info.get_surfaces_info()

    def valid_name(self, surface_name: str) -> str:
        if validate_inputs:
            if not self.is_valid(surface_name):
                raise SurfaceNameError(
                    surface_name=surface_name,
                    allowed_values=self(),
                )
        return surface_name


class _AllowedSurfaceIDs(_AllowedNames):
    def __call__(self, respect_data_valid: bool = True) -> List[int]:
        try:
            return [
                info["surface_id"][0]
                for _, info in self._field_info.get_surfaces_info().items()
            ]
        except (KeyError, IndexError):
            pass


class _AllowedScalarFieldNames(_AllowedFieldNames):
    _field_name_error = ScalarFieldNameError
    _field_unavailable_error = ScalarFieldUnavailable

    def __call__(self, respect_data_valid: bool = True) -> List[str]:
        field_dict = self._field_info.get_fields_info()
        return (
            field_dict
            if (not respect_data_valid or self._is_data_valid())
            else [
                name
                for name, info in field_dict.items()
                if info["section"] in ("Mesh...", "Cell Info...")
            ]
        )


class _AllowedVectorFieldNames(_AllowedFieldNames):
    _field_name_error = VectorFieldNameError
    _field_unavailable_error = VectorFieldUnavailable

    def __call__(self, respect_data_valid: bool = True) -> List[str]:
        return (
            self._field_info.get_vector_fields_info()
            if (not respect_data_valid or self._is_data_valid())
            else []
        )

    def is_valid(self, name, respect_data_valid=True):
        return name in self(respect_data_valid)


class _FieldMethod:
    class _Arg:
        def __init__(self, accessor):
            self._accessor = accessor

        def allowed_values(self):
            return sorted(self._accessor())

    def __init__(self, field_data_accessor, args_allowed_values_accessors):
        self._field_data_accessor = field_data_accessor
        for arg_name, accessor in args_allowed_values_accessors.items():
            setattr(self, arg_name, _FieldMethod._Arg(accessor))

    def __call__(self, *args, **kwargs):
        return self._field_data_accessor(*args, **kwargs)


class FieldTransaction:
    """Populates Fluent field data on surfaces."""

    def __init__(
        self,
        service: FieldDataService,
        field_info: FieldInfo,
        allowed_surface_ids,
        allowed_surface_names,
        allowed_scalar_field_names,
        allowed_vector_field_names,
    ):
        self._service = service
        self._field_info = field_info
        self._fields_request = get_fields_request()

        self._allowed_surface_names = allowed_surface_names
        self._allowed_scalar_field_names = allowed_scalar_field_names
        self._allowed_vector_field_names = allowed_vector_field_names

        surface_args = dict(
            surface_ids=allowed_surface_ids,
            surface_names=self._allowed_surface_names,
        )
        scalar_field_args = {
            **dict(field_name=self._allowed_scalar_field_names),
            **surface_args,
        }
        self.add_scalar_fields_request = _FieldMethod(
            field_data_accessor=self.add_scalar_fields_request,
            args_allowed_values_accessors=scalar_field_args,
        )
        self.add_vector_fields_request = _FieldMethod(
            field_data_accessor=self.add_vector_fields_request,
            args_allowed_values_accessors={
                **dict(field_name=self._allowed_vector_field_names),
                **surface_args,
            },
        )
        self.add_surfaces_request = _FieldMethod(
            field_data_accessor=self.add_surfaces_request,
            args_allowed_values_accessors=surface_args,
        )
        self.add_pathlines_fields_request = _FieldMethod(
            field_data_accessor=self.add_pathlines_fields_request,
            args_allowed_values_accessors=scalar_field_args,
        )

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
            allowed_surface_names=self._allowed_surface_names,
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
            allowed_surface_names=self._allowed_surface_names,
            surface_ids=surface_ids,
            surface_names=surface_names,
        )
        self._fields_request.scalarFieldRequest.extend(
            [
                FieldDataProtoModule.ScalarFieldRequest(
                    surfaceId=surface_id,
                    scalarFieldName=self._allowed_scalar_field_names.valid_name(
                        field_name
                    ),
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
            allowed_surface_names=self._allowed_surface_names,
            surface_ids=surface_ids,
            surface_names=surface_names,
        )
        self._fields_request.vectorFieldRequest.extend(
            [
                FieldDataProtoModule.VectorFieldRequest(
                    surfaceId=surface_id,
                    vectorFieldName=self._allowed_vector_field_names.valid_name(
                        field_name,
                    ),
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
            allowed_surface_names=self._allowed_surface_names,
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
    allowed_surface_names,
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
                surface_ids.extend(
                    field_info.get_surfaces_info()[surface_name]["surface_id"]
                )
        elif surface_name:
            surface_ids = field_info.get_surfaces_info()[
                allowed_surface_names.valid_name(surface_name)
            ]["surface_id"]
        else:
            raise RuntimeError("Please provide either surface names or surface ids.")
    return surface_ids


def get_fields_request():
    """Populates a new field request."""
    return FieldDataProtoModule.GetFieldsRequest(
        provideBytesStream=_FieldDataConstants.bytes_stream,
        chunkSize=_FieldDataConstants.chunk_size,
    )

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
                [
                    _FieldDataConstants.payloadTags[tag]
                    for tag in payload_info.payloadTag
                ]
                or [0],
            )
        payload_data = fields_data.get(payload_tag_id)
        if not payload_data:
            payload_data = fields_data[payload_tag_id] = {}
        surface_data = payload_data.get(surface_id)
        if surface_data:
            if payload_info.fieldName in surface_data:
                surface_data.update({payload_info.fieldName: np.concatenate((surface_data[payload_info.fieldName], field))})
            else:
                surface_data.update({payload_info.fieldName: field})
        else:
            payload_data[surface_id] = {payload_info.fieldName: field}
    return fields_data


class FieldData:
    """Provides access to Fluent field data on surfaces."""

    def __init__(
        self,
        service: FieldDataService,
        field_info: FieldInfo,
        is_data_valid: Callable[[], bool],
    ):
        self._service = service
        self._field_info = field_info
        self.is_data_valid = is_data_valid

        self._allowed_surface_names = _AllowedSurfaceNames(field_info)

        self._allowed_surface_ids = _AllowedSurfaceIDs(field_info)

        self._allowed_scalar_field_names = _AllowedScalarFieldNames(
            field_info, is_data_valid
        )

        self._allowed_vector_field_names = _AllowedVectorFieldNames(
            field_info, is_data_valid
        )

        surface_args = dict(
            surface_ids=self._allowed_surface_ids,
            surface_name=self._allowed_surface_names,
        )
        scalar_field_args = {
            **dict(field_name=self._allowed_scalar_field_names),
            **surface_args,
        }
        self.get_scalar_field_data = _FieldMethod(
            field_data_accessor=self.get_scalar_field_data,
            args_allowed_values_accessors=scalar_field_args,
        )
        self.get_vector_field_data = _FieldMethod(
            field_data_accessor=self.get_vector_field_data,
            args_allowed_values_accessors={
                **dict(field_name=self._allowed_vector_field_names),
                **surface_args,
            },
        )
        self.get_surface_data = _FieldMethod(
            field_data_accessor=self.get_surface_data,
            args_allowed_values_accessors=surface_args,
        )
        self.get_pathlines_field_data = _FieldMethod(
            field_data_accessor=self.get_pathlines_field_data,
            args_allowed_values_accessors=scalar_field_args,
        )

    def new_transaction(self):
        return FieldTransaction(
            self._service,
            self._field_info,
            self._allowed_surface_ids,
            self._allowed_surface_names,
            self._allowed_scalar_field_names,
            self._allowed_vector_field_names,
        )

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
            allowed_surface_names=self._allowed_surface_names,
            surface_ids=surface_ids,
            surface_name=surface_name,
        )
        fields_request = get_fields_request()
        fields_request.scalarFieldRequest.extend(
            [
                FieldDataProtoModule.ScalarFieldRequest(
                    surfaceId=surface_id,
                    scalarFieldName=self._allowed_scalar_field_names.valid_name(
                        field_name
                    ),
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
            allowed_surface_names=self._allowed_surface_names,
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
            allowed_surface_names=self._allowed_surface_names,
            surface_ids=surface_ids,
            surface_name=surface_name,
        )
        fields_request = get_fields_request()
        fields_request.vectorFieldRequest.extend(
            [
                FieldDataProtoModule.VectorFieldRequest(
                    surfaceId=surface_id,
                    vectorFieldName=self._allowed_vector_field_names.valid_name(
                        field_name
                    ),
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
            allowed_surface_names=self._allowed_surface_names,
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
        return pathlines_data
