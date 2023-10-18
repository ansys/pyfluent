"""Wrappers over FieldData gRPC service of Fluent."""
from enum import IntEnum
from functools import reduce
from typing import Callable, Dict, List, Optional, Tuple, Union

import grpc
import numpy as np

from ansys.api.fluent.v0 import field_data_pb2 as FieldDataProtoModule
from ansys.api.fluent.v0 import field_data_pb2_grpc as FieldGrpcModule
from ansys.fluent.core.services.error_handler import catch_grpc_error
from ansys.fluent.core.services.interceptors import (
    BatchInterceptor,
    ErrorStateInterceptor,
    TracingInterceptor,
)
from ansys.fluent.core.services.streaming import StreamingService
from ansys.fluent.core.solver.error_message import allowed_name_error_message


def override_help_text(func, func_to_be_wrapped):
    """Override function help text."""
    func.__doc__ = "\n" + func_to_be_wrapped.__doc__
    func.__name__ = func_to_be_wrapped.__qualname__
    return func


# this can be switched to False in scenarios where the field_data request inputs are
# fed by results of field_info queries, which might be true in GUI code.
validate_inputs = True


class FieldDataService(StreamingService):
    """FieldData service of Fluent."""

    def __init__(
        self, channel: grpc.Channel, metadata: List[Tuple[str, str]], fluent_error_state
    ):
        """__init__ method of FieldDataService class."""
        intercept_channel = grpc.intercept_channel(
            channel,
            ErrorStateInterceptor(fluent_error_state),
            TracingInterceptor(),
            BatchInterceptor(),
        )
        super().__init__(
            stub=FieldGrpcModule.FieldDataStub(intercept_channel), metadata=metadata
        )

    @catch_grpc_error
    def get_scalar_field_range(self, request):
        """GetRange RPC of FieldData service."""
        return self._stub.GetRange(request, metadata=self._metadata)

    @catch_grpc_error
    def get_scalar_fields_info(self, request):
        """GetFieldsInfo RPC of FieldData service."""
        return self._stub.GetFieldsInfo(request, metadata=self._metadata)

    @catch_grpc_error
    def get_vector_fields_info(self, request):
        """GetVectorFieldsInfo RPC of FieldData service."""
        return self._stub.GetVectorFieldsInfo(request, metadata=self._metadata)

    @catch_grpc_error
    def get_surfaces_info(self, request):
        """GetSurfacesInfo RPC of FieldData service."""
        return self._stub.GetSurfacesInfo(request, metadata=self._metadata)

    # pylint: disable=missing-raises-doc
    @catch_grpc_error
    def get_fields(self, request):
        """GetFields RPC of FieldData service."""
        chunk_iterator = self._stub.GetFields(request, metadata=self._metadata)
        if not chunk_iterator.is_active():
            raise RuntimeError(
                "Unexpectedly encountered empty chunk during field extraction."
            )
        return chunk_iterator


class FieldInfo:
    """Provides access to Fluent field information.

    Methods
    -------
    get_scalar_field_range(field: str, node_value: bool, surface_ids: List[int])
    -> List[float]
        Get the range (minimum and maximum values) of the field.

    get_scalar_fields_info(self) -> dict
        Get fields information (field name, domain, and section).

    get_vector_fields_info(self) -> dict
        Get vector fields information.

    get_surfaces_info(self) -> dict
        Get surfaces information (surface name, ID, and type).
    """

    def __init__(
        self,
        service: FieldDataService,
        is_data_valid: Optional[Callable[[], bool]],
    ):
        """__init__ method of FieldInfo class."""
        self._service = service
        self._is_data_valid = is_data_valid

    def get_scalar_field_range(
        self, field: str, node_value: bool = False, surface_ids: List[int] = None
    ) -> List[float]:
        """Get the range (minimum and maximum values) of the field.

        Parameters
        ----------
        field: str
            Field name
        node_value: bool
        surface_ids : List[int], optional
            List of surface IDS for the surface data.

        Returns
        -------
        List[float]
        """
        if not surface_ids:
            surface_ids = []
        request = FieldDataProtoModule.GetRangeRequest()
        request.fieldName = field
        request.nodeValue = node_value
        request.surfaceid.extend(
            [FieldDataProtoModule.SurfaceId(id=int(id)) for id in surface_ids]
        )
        response = self._service.get_scalar_field_range(request)
        return [response.minimum, response.maximum]

    def get_scalar_fields_info(self) -> Dict[str, Dict]:
        """Get fields information (field name, domain, and section).

        Returns
        -------
        Dict
        """
        request = FieldDataProtoModule.GetFieldsInfoRequest()
        response = self._service.get_scalar_fields_info(request)
        return {
            field_info.solverName: {
                "display_name": field_info.displayName,
                "section": field_info.section,
                "domain": field_info.domain,
            }
            for field_info in response.fieldInfo
        }

    def get_vector_fields_info(self) -> Dict[str, Dict]:
        """Get vector fields information (vector components).

        Returns
        -------
        Dict
        """
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

    def get_surfaces_info(self) -> Dict[str, Dict]:
        """Get surfaces information (surface name, ID, and type).

        Returns
        -------
        Dict
        """
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

    def validate_scalar_fields(self, field_name: str):
        _AllowedScalarFieldNames(
            self._is_data_valid, info=self.get_scalar_fields_info()
        ).valid_name(field_name)

    def validate_vector_fields(self, field_name: str):
        _AllowedVectorFieldNames(
            self._is_data_valid, info=self.get_vector_fields_info()
        ).valid_name(field_name)

    def validate_surfaces(self, surfaces: List[str]):
        for surface in surfaces:
            _AllowedSurfaceNames(info=self.get_surfaces_info()).valid_name(surface)


def unavailable_field_error_message(context: str, field_name: str) -> str:
    """Error message for unavailable fields."""
    return f"{field_name} is not a currently available {context}."


class FieldNameError(ValueError):
    """Exception class for errors in field name."""

    pass


class ScalarFieldNameError(FieldNameError):
    """Exception class for errors in scalar field name."""

    def __init__(self, field_name: str, allowed_values: List[str]):
        """__init__ method of ScalarFieldNameError class."""
        self.field_name = field_name
        super().__init__(
            allowed_name_error_message("scalar field", field_name, allowed_values)
        )


class VectorFieldNameError(FieldNameError):
    """Exception class for errors in vector field name."""

    def __init__(self, field_name: str, allowed_values: List[str]):
        """__init__ method of VectorFieldNameError class."""
        self.field_name = field_name
        super().__init__(
            allowed_name_error_message("vector field", field_name, allowed_values)
        )


class FieldUnavailable(RuntimeError):
    """Exception class for when field is unavailable."""

    pass


class ScalarFieldUnavailable(FieldUnavailable):
    """Exception class for when scalar field is unavailable."""

    def __init__(self, field_name: str):
        """__init__ method of ScalarFieldUnavailable class."""
        self.field_name = field_name
        super().__init__(unavailable_field_error_message("scalar field", field_name))


class VectorFieldUnavailable(FieldUnavailable):
    """Exception class for when vector field is unavailable."""

    def __init__(self, field_name: str):
        """__init__ method of VectorFieldUnavailable class."""
        self.field_name = field_name
        super().__init__(unavailable_field_error_message("vector field", field_name))


class SurfaceNameError(ValueError):
    """Exception class for errors in surface name."""

    def __init__(self, surface_name: str, allowed_values: List[str]):
        """__init__ method of SurfaceNameError class."""
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
    def __init__(
        self, field_info: Optional[FieldInfo] = None, info: Optional[Dict] = None
    ):
        self._field_info = field_info
        self._info = info

    def is_valid(self, name, respect_data_valid=True):
        """Checks validity."""
        return name in self(respect_data_valid)


class _AllowedFieldNames(_AllowedNames):
    def __init__(
        self,
        is_data_valid: Callable[[], bool],
        field_info: Optional[FieldInfo] = None,
        info: Optional[Dict] = None,
    ):
        super().__init__(field_info=field_info, info=info)
        self._is_data_valid = is_data_valid

    def valid_name(self, field_name):
        """Returns valid names."""
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
        return self._info if self._info else self._field_info.get_surfaces_info()

    # pylint: disable=missing-raises-doc
    def valid_name(self, surface_name: str) -> str:
        """Returns valid names."""
        if validate_inputs and not self.is_valid(surface_name):
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
        field_dict = (
            self._info if self._info else self._field_info.get_scalar_fields_info()
        )
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
            self._info
            if self._info
            else self._field_info.get_vector_fields_info()
            if (not respect_data_valid or self._is_data_valid())
            else []
        )

    def is_valid(self, name, respect_data_valid=True):
        """Checks validity."""
        return name in self(respect_data_valid)


class _FieldMethod:
    class _Arg:
        def __init__(self, accessor):
            self._accessor = accessor

        def allowed_values(self):
            """Returns set of allowed values."""
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
        """__init__ method of FieldTransaction class."""
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
        self.add_scalar_fields_request = override_help_text(
            _FieldMethod(
                field_data_accessor=self.add_scalar_fields_request,
                args_allowed_values_accessors=scalar_field_args,
            ),
            self.add_scalar_fields_request,
        )
        self.add_vector_fields_request = override_help_text(
            _FieldMethod(
                field_data_accessor=self.add_vector_fields_request,
                args_allowed_values_accessors={
                    **dict(field_name=self._allowed_vector_field_names),
                    **surface_args,
                },
            ),
            self.add_vector_fields_request,
        )
        self.add_surfaces_request = override_help_text(
            _FieldMethod(
                field_data_accessor=self.add_surfaces_request,
                args_allowed_values_accessors=surface_args,
            ),
            self.add_surfaces_request,
        )
        self.add_pathlines_fields_request = override_help_text(
            _FieldMethod(
                field_data_accessor=self.add_pathlines_fields_request,
                args_allowed_values_accessors=scalar_field_args,
            ),
            self.add_pathlines_fields_request,
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
        """Add request to get surface data (vertices, face connectivity, centroids, and
        normals).

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
        return ChunkParser().extract_fields(
            self._service.get_fields(self._fields_request)
        )

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
    np_data_type_to_proto_field_type = {
        np.int32: FieldDataProtoModule.FieldType.INT_ARRAY,
        np.int64: FieldDataProtoModule.FieldType.LONG_ARRAY,
        np.float32: FieldDataProtoModule.FieldType.FLOAT_ARRAY,
        np.float64: FieldDataProtoModule.FieldType.DOUBLE_ARRAY,
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
    """Get surface IDs based on surface names or IDs.

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
        raise RuntimeError("Please provide either surface names or surface IDs.")
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
            raise RuntimeError("Please provide either surface names or surface IDs.")
    return surface_ids


def get_fields_request():
    """Populates a new field request."""
    return FieldDataProtoModule.GetFieldsRequest(
        provideBytesStream=_FieldDataConstants.bytes_stream,
        chunkSize=_FieldDataConstants.chunk_size,
    )


class ChunkParser:
    """Class for parsing field data stream received from Fluent.

    Parameters
    ----------
    callbacks_provider : object
    The object which can register and unregister callbacks.
    It provides callbacks, which are triggered with following arguments:
        zone_id : int
        field_name : str
        field : numpy array
    """

    def __init__(self, callbacks_provider: object = None):
        """__init__ method of ChunkParser class."""
        self._callbacks_provider = callbacks_provider

    def extract_fields(self, chunk_iterator) -> Dict[int, Dict[str, np.array]]:
        """Extracts field data received from Fluent.

        if callbacks_provider is set then callbacks are triggered with extracted data.
        """

        def _get_tag_for_surface_request():
            return (("type", "surface-data"),)

        def _get_tag_for_vector_field_request():
            return (("type", "vector-field"),)

        def _get_tag_for_scalar_field_request(scalar_field_request):
            return (
                ("type", "scalar-field"),
                ("dataLocation", scalar_field_request.dataLocation),
                ("boundaryValues", scalar_field_request.provideBoundaryValues),
            )

        def _get_tag_for_pathlines_field_request(pathlines_field_request):
            return (
                ("type", "pathlines-field"),
                ("field", pathlines_field_request.field),
            )

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
            if request_type is not None:
                payload_tag_id = (
                    _get_tag_for_surface_request()
                    if request_type == "surfaceRequest"
                    else _get_tag_for_scalar_field_request(
                        field_request_info.scalarFieldRequest
                    )
                    if request_type == "scalarFieldRequest"
                    else _get_tag_for_vector_field_request()
                    if request_type == "vectorFieldRequest"
                    else _get_tag_for_pathlines_field_request(
                        field_request_info.pathlinesFieldRequest
                    )
                    if request_type == "pathlinesFieldRequest"
                    else None
                )
            else:
                if self._callbacks_provider is None:
                    payload_tag_id = reduce(
                        lambda x, y: x | y,
                        [
                            _FieldDataConstants.payloadTags[tag]
                            for tag in payload_info.payloadTag
                        ]
                        or [0],
                    )
                else:
                    payload_tag_id = None
            field = None
            if payload_tag_id is not None:
                field = _extract_field(
                    _FieldDataConstants.proto_field_type_to_np_data_type[
                        payload_info.fieldType
                    ],
                    payload_info.fieldSize,
                    chunk_iterator,
                )

            if self._callbacks_provider is not None:
                for callback_data in self._callbacks_provider.callbacks():
                    callback, args, kwargs = callback_data
                    # print('cb', surface_id, payload_info.fieldName)
                    callback(surface_id, payload_info.fieldName, field, *args, **kwargs)
            else:
                payload_data = fields_data.get(payload_tag_id)
                if not payload_data:
                    payload_data = fields_data[payload_tag_id] = {}
                surface_data = payload_data.get(surface_id)
                if surface_data:
                    if payload_info.fieldName in surface_data:
                        surface_data.update(
                            {
                                payload_info.fieldName: np.concatenate(
                                    (surface_data[payload_info.fieldName], field)
                                )
                            }
                        )
                    else:
                        surface_data.update({payload_info.fieldName: field})
                else:
                    payload_data[surface_id] = {payload_info.fieldName: field}
        return fields_data


class BaseFieldData:
    """Contains common properties required by all field data types."""

    def __init__(self, i_d, data):
        """__init__ method of BaseFieldData class."""
        self._data = data
        self._id = i_d

    @property
    def data(self):
        """Returns data."""
        return self._data

    @property
    def surface_id(self):
        """Returns surface ID."""
        return self._id

    @property
    def size(self):
        """Returns size of data."""
        return len(self._data)

    def __getitem__(self, item):
        return self._data[item]


class ScalarFieldData(BaseFieldData):
    """Contains scalar field data."""

    class ScalarData:
        """Stores and provides the data as a scalar."""

        def __init__(self, data):
            """__init__ method of ScalarData class."""
            self.scalar_data = data

    def __init__(self, i_d, data):
        """__init__ method of ScalarFieldData class."""
        super().__init__(i_d, [ScalarFieldData.ScalarData(_data) for _data in data])


class Vector:
    """Stores the data as a vector ``(x, y, z)``."""

    def __init__(self, x, y, z):
        """__init__ method of Vector class."""
        self._x = x
        self._y = y
        self._z = z

    @property
    def x(self) -> float:
        """Returns vector point x."""
        return self._x

    @property
    def y(self) -> float:
        """Returns vector point y."""
        return self._y

    @property
    def z(self) -> float:
        """Returns vector point z."""
        return self._z


def _resolve_into_array_of_vectors(data):
    if data.size % 3:
        raise ValueError(
            "Dataset must be resolved as a set of vectors."
            "The length of the dataset should always be in multiples of 3."
        )
    data.shape = data.size // 3, 3


class VectorFieldData(BaseFieldData):
    """Provides a container for vector field data."""

    class VectorData(Vector):
        """Stores and provides the data as a vector."""

        def __init__(self, x, y, z):
            """__init__ method of VectorData class."""
            super().__init__(x, y, z)

    def __init__(self, i_d, data, scale):
        """__init__ method of VectorFieldData class."""
        _resolve_into_array_of_vectors(data)
        self._scale = scale
        super().__init__(i_d, [VectorFieldData.VectorData(x, y, z) for x, y, z in data])

    @property
    def scale(self) -> float:
        """Returns scale of the vector field."""
        return self._scale


class Vertices(BaseFieldData):
    """Provides a container for the vertex data."""

    class Vertex(Vector):
        """Stores and provides the data as a vector of a vertex."""

        def __init__(self, x, y, z):
            """__init__ method of Vertex class."""
            super().__init__(x, y, z)

    def __init__(self, i_d, data):
        """__init__ method of Vertices class."""
        _resolve_into_array_of_vectors(data)
        super().__init__(i_d, [(Vertices.Vertex(x, y, z)) for x, y, z in data])


class FacesCentroid(BaseFieldData):
    """Provides the container for the face centroid data."""

    class Centroid(Vector):
        """Stores and provides the face centroid data as a vector."""

        def __init__(self, x, y, z):
            """__init__ method of Centroid class."""
            super().__init__(x, y, z)

    def __init__(self, i_d, data):
        """__init__ method of FacesCentroid class."""
        _resolve_into_array_of_vectors(data)
        super().__init__(i_d, [(FacesCentroid.Centroid(x, y, z)) for x, y, z in data])


class FacesConnectivity(BaseFieldData):
    """Provides the container for the face connectivity data."""

    class Faces:
        """Stores and provides the face connectivity data as an array."""

        def __init__(self, node_count, node_indices):
            """__init__ method of Faces class."""
            self.node_count = node_count
            self.node_indices = node_indices

    def __init__(self, i_d, data):
        """__init__ method of FacesConnectivity class."""
        faces_data = []
        i = 0

        while i < len(data):
            end = i + 1 + data[i]
            faces_data.append(FacesConnectivity.Faces(data[i], data[i + 1 : end]))
            i = end

        super().__init__(i_d, faces_data)


class FacesNormal(BaseFieldData):
    """Provides the container for the face normal data."""

    class Normal(Vector):
        """Stores and provides the face normal data as a vector."""

        def __init__(self, x, y, z):
            """__init__ method of Normal class."""
            super().__init__(x, y, z)

    def __init__(self, i_d, data):
        """__init__ method of FacesNormal class."""
        _resolve_into_array_of_vectors(data)
        super().__init__(i_d, [FacesNormal.Normal(x, y, z) for x, y, z in data])


class FieldData:
    """Provides access to Fluent field data on surfaces."""

    def __init__(
        self,
        service: FieldDataService,
        field_info: FieldInfo,
        is_data_valid: Callable[[], bool],
        scheme_eval: Optional = None,
    ):
        """__init__ method of FieldData class."""
        self._service = service
        self._field_info = field_info
        self.is_data_valid = is_data_valid
        self.scheme_eval = scheme_eval

        self._allowed_surface_names = _AllowedSurfaceNames(field_info)

        self._allowed_surface_ids = _AllowedSurfaceIDs(field_info)

        self._allowed_scalar_field_names = _AllowedScalarFieldNames(
            is_data_valid, field_info
        )

        self._allowed_vector_field_names = _AllowedVectorFieldNames(
            is_data_valid, field_info
        )

        surface_args = dict(
            surface_ids=self._allowed_surface_ids,
            surface_name=self._allowed_surface_names,
        )
        scalar_field_args = {
            **dict(field_name=self._allowed_scalar_field_names),
            **surface_args,
        }
        self.get_scalar_field_data = override_help_text(
            _FieldMethod(
                field_data_accessor=self.get_scalar_field_data,
                args_allowed_values_accessors=scalar_field_args,
            ),
            self.get_scalar_field_data,
        )
        self.get_vector_field_data = override_help_text(
            _FieldMethod(
                field_data_accessor=self.get_vector_field_data,
                args_allowed_values_accessors={
                    **dict(field_name=self._allowed_vector_field_names),
                    **surface_args,
                },
            ),
            self.get_vector_field_data,
        )
        self.get_surface_data = override_help_text(
            _FieldMethod(
                field_data_accessor=self.get_surface_data,
                args_allowed_values_accessors=surface_args,
            ),
            self.get_surface_data,
        )
        self.get_pathlines_field_data = override_help_text(
            _FieldMethod(
                field_data_accessor=self.get_pathlines_field_data,
                args_allowed_values_accessors=scalar_field_args,
            ),
            self.get_pathlines_field_data,
        )

    def new_transaction(self):
        """Create a new field transaction."""
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
    ) -> Union[ScalarFieldData, Dict[int, ScalarFieldData]]:
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
        Union[ScalarFieldData, Dict[int, ScalarFieldData]]
            If a surface name is provided as input, scalar field data is returned. If surface
            IDs are provided as input, a dictionary containing a map of surface IDs to scalar
            field data.
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

        fields = ChunkParser().extract_fields(self._service.get_fields(fields_request))
        scalar_field_data = next(iter(fields.values()))

        if surface_name:
            return ScalarFieldData(
                surface_ids[0], scalar_field_data[surface_ids[0]][field_name]
            )
        else:
            return {
                surface_id: ScalarFieldData(
                    surface_id, scalar_field_data[surface_id][field_name]
                )
                for surface_id in surface_ids
            }

    def get_surface_data(
        self,
        data_type: SurfaceDataType,
        surface_ids: Optional[List[int]] = None,
        surface_name: Optional[str] = None,
        overset_mesh: Optional[bool] = False,
    ) -> Union[
        Union[Vertices, FacesConnectivity, FacesNormal, FacesCentroid],
        Dict[int, Union[Vertices, FacesConnectivity, FacesNormal, FacesCentroid]],
    ]:
        """Get surface data (vertices, faces connectivity, centroids, and normals).

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
        Union[Vertices, FacesConnectivity, FacesNormal, FacesCentroid,
        Dict[int, Union[Vertices, FacesConnectivity, FacesNormal, FacesCentroid]]]
             If a surface name is provided as input, face vertices, connectivity data, and normal or centroid data are returned.
             If surface IDs are provided as input, a dictionary containing a map of surface IDs to face
             vertices, connectivity data, and normal or centroid data is returned.
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
        fields = ChunkParser().extract_fields(self._service.get_fields(fields_request))
        surface_data = next(iter(fields.values()))

        def _get_surfaces_data(parent_class, surf_id, _data_type):
            return parent_class(
                surf_id,
                surface_data[surf_id][enum_to_field_name[_data_type]],
            )

        if data_type == SurfaceDataType.Vertices:
            if surface_name:
                return _get_surfaces_data(Vertices, surface_ids[0], data_type)
            else:
                return {
                    surface_id: _get_surfaces_data(Vertices, surface_id, data_type)
                    for surface_id in surface_ids
                }

        if data_type == SurfaceDataType.FacesCentroid:
            if surface_name:
                return _get_surfaces_data(FacesCentroid, surface_ids[0], data_type)
            else:
                return {
                    surface_id: _get_surfaces_data(FacesCentroid, surface_id, data_type)
                    for surface_id in surface_ids
                }

        if data_type == SurfaceDataType.FacesConnectivity:
            if surface_name:
                return _get_surfaces_data(FacesConnectivity, surface_ids[0], data_type)
            else:
                return {
                    surface_id: _get_surfaces_data(
                        FacesConnectivity, surface_id, data_type
                    )
                    for surface_id in surface_ids
                }

        if data_type == SurfaceDataType.FacesNormal:
            if surface_name:
                return _get_surfaces_data(FacesNormal, surface_ids[0], data_type)
            else:
                return {
                    surface_id: _get_surfaces_data(FacesNormal, surface_id, data_type)
                    for surface_id in surface_ids
                }

    def get_vector_field_data(
        self,
        field_name: str,
        surface_ids: Optional[List[int]] = None,
        surface_name: Optional[str] = None,
    ) -> Union[VectorFieldData, Dict[int, VectorFieldData]]:
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
        Union[VectorFieldData, Dict[int, VectorFieldData]]
            If a surface name is provided as input, vector field data is returned.
            If surface IDs are provided as input, a dictionary containing a map of
            surface IDs to vector field data is returned.
        """
        if surface_name:
            self.scheme_eval.string_eval(
                f"(surface? (thread-name->id '{surface_name}))"
            )
        elif surface_ids:
            for surface_id in surface_ids:
                self.scheme_eval.string_eval(f"(surface? {surface_id})")
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
        fields = ChunkParser().extract_fields(self._service.get_fields(fields_request))
        vector_field_data = next(iter(fields.values()))

        if surface_name:
            return VectorFieldData(
                surface_ids[0],
                vector_field_data[surface_ids[0]][field_name],
                vector_field_data[surface_ids[0]]["vector-scale"][0],
            )
        else:
            return {
                surface_id: VectorFieldData(
                    surface_id,
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
    ) -> Dict:
        """Get the pathlines field data on a surface.

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
        Dict
            Dictionary containing a map of surface IDs to the pathline data.
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
        fields = ChunkParser().extract_fields(self._service.get_fields(fields_request))
        pathlines_data = next(iter(fields.values()))

        def _get_surfaces_data(parent_class, surf_id, _data_type):
            return parent_class(
                surf_id,
                pathlines_data[surf_id][_data_type],
            )

        if surface_name:
            vertices_data = _get_surfaces_data(Vertices, surface_ids[0], "vertices")
            lines_data = _get_surfaces_data(FacesConnectivity, surface_ids[0], "lines")
            field_data = ScalarFieldData(
                surface_ids[0], pathlines_data[surface_ids[0]][field_name]
            )
            return {
                "vertices": vertices_data,
                "lines": lines_data,
                field_name: field_data,
            }
        else:
            path_lines_dict = {}
            for surface_id in surface_ids:
                path_lines_dict[surface_id] = {
                    "vertices": _get_surfaces_data(Vertices, surface_id, "vertices"),
                    "lines": _get_surfaces_data(FacesConnectivity, surface_id, "lines"),
                    field_name: ScalarFieldData(
                        surface_id, pathlines_data[surface_id][field_name]
                    ),
                }
            return path_lines_dict
