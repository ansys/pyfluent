"""Wrappers over FieldData gRPC service of Fluent."""

from enum import Enum
from functools import reduce
from typing import Callable, Dict, List, Tuple

import grpc
import numpy as np

from ansys.api.fluent.v0 import field_data_pb2 as FieldDataProtoModule
from ansys.api.fluent.v0 import field_data_pb2_grpc as FieldGrpcModule
from ansys.fluent.core.exceptions import DisallowedValuesError
from ansys.fluent.core.services.interceptors import (
    BatchInterceptor,
    ErrorStateInterceptor,
    GrpcErrorInterceptor,
    TracingInterceptor,
)
from ansys.fluent.core.services.streaming import StreamingService
from ansys.fluent.core.utils.deprecate import deprecate_argument, deprecate_arguments


def override_help_text(func, func_to_be_wrapped):
    """Override function help text."""
    if func_to_be_wrapped.__doc__:
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
            GrpcErrorInterceptor(),
            ErrorStateInterceptor(fluent_error_state),
            TracingInterceptor(),
            BatchInterceptor(),
        )
        super().__init__(
            stub=FieldGrpcModule.FieldDataStub(intercept_channel), metadata=metadata
        )

    def get_scalar_field_range(self, request):
        """GetRange RPC of FieldData service."""
        return self._stub.GetRange(request, metadata=self._metadata)

    def get_scalar_fields_info(self, request):
        """GetFieldsInfo RPC of FieldData service."""
        return self._stub.GetFieldsInfo(request, metadata=self._metadata)

    def get_vector_fields_info(self, request):
        """GetVectorFieldsInfo RPC of FieldData service."""
        return self._stub.GetVectorFieldsInfo(request, metadata=self._metadata)

    def get_surfaces_info(self, request):
        """GetSurfacesInfo RPC of FieldData service."""
        return self._stub.GetSurfacesInfo(request, metadata=self._metadata)

    def get_fields(self, request):
        """GetFields RPC of FieldData service.

        Raises
        ------
        RuntimeError
            If an empty chunk encountered during field extraction.
        """
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
        is_data_valid: Callable[[], bool],
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
        """Validate scalar fields."""
        _AllowedScalarFieldNames(
            self._is_data_valid, info=self.get_scalar_fields_info()
        ).valid_name(field_name)

    def validate_vector_fields(self, field_name: str):
        """Validate vector fields."""
        _AllowedVectorFieldNames(
            self._is_data_valid, info=self.get_vector_fields_info()
        ).valid_name(field_name)

    def validate_surfaces(self, surfaces: List[str]):
        """Validate surfaces."""
        for surface in surfaces:
            _AllowedSurfaceNames(info=self.get_surfaces_info()).valid_name(surface)


class FieldUnavailable(RuntimeError):
    """Raised when field is unavailable."""

    pass


class SurfaceDataType(Enum):
    """Provides surface data types."""

    Vertices = "vertices"
    FacesConnectivity = "faces"
    FacesNormal = "face-normal"
    FacesCentroid = "centroid"


class _AllowedNames:
    def __init__(self, field_info: FieldInfo | None = None, info: dict | None = None):
        self._field_info = field_info
        self._info = info

    def is_valid(self, name, respect_data_valid=True):
        """Checks validity."""
        return name in self(respect_data_valid)


class _AllowedFieldNames(_AllowedNames):
    def __init__(
        self,
        is_data_valid: Callable[[], bool],
        field_info: FieldInfo | None = None,
        info: dict | None = None,
    ):
        super().__init__(field_info=field_info, info=info)
        self._is_data_valid = is_data_valid

    def valid_name(self, field_name):
        """Returns valid names."""
        if validate_inputs:
            names = self
            if not names.is_valid(field_name, respect_data_valid=False):
                raise self._field_name_error(
                    context="field",
                    name=field_name,
                    allowed_values=list(names(respect_data_valid=False).keys()),
                )
            if not names.is_valid(field_name, respect_data_valid=True):
                raise self._field_unavailable_error(
                    f"{field_name} is not a currently available field."
                )
        return field_name


class _AllowedSurfaceNames(_AllowedNames):
    def __call__(self, respect_data_valid: bool = True) -> List[str]:
        return self._info if self._info else self._field_info.get_surfaces_info()

    def valid_name(self, surface_name: str) -> str:
        """Returns valid names.

        Raises
        ------
        DisallowedValuesError
            If surface name is invalid.
        """
        if validate_inputs and not self.is_valid(surface_name):
            raise DisallowedValuesError("surface", surface_name, self())
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
    _field_name_error = DisallowedValuesError
    _field_unavailable_error = FieldUnavailable

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
    _field_name_error = DisallowedValuesError
    _field_unavailable_error = FieldUnavailable

    def __call__(self, respect_data_valid: bool = True) -> List[str]:
        return (
            self._info
            if self._info
            else (
                self._field_info.get_vector_fields_info()
                if (not respect_data_valid or self._is_data_valid())
                else []
            )
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


def _data_type_convertor(args_dict):
    d_type_list = []
    d_type_map = {
        "provide_vertices": SurfaceDataType.Vertices,
        "provide_faces": SurfaceDataType.FacesConnectivity,
        "provide_faces_centroid": SurfaceDataType.FacesCentroid,
        "provide_faces_normal": SurfaceDataType.FacesNormal,
    }
    for key, val in d_type_map.items():
        if args_dict.get(key):
            d_type_list.append(val)
        args_dict.pop(key, None)
    if args_dict.get("data_types") is None:
        args_dict["data_types"] = d_type_list
    return args_dict


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

    @deprecate_argument(
        old_arg="surface_names",
        new_arg="surfaces",
        converter=lambda old_arg_val: old_arg_val or [],
    )
    @deprecate_argument(
        old_arg="surface_ids",
        new_arg="surfaces",
        converter=lambda old_arg_val: old_arg_val or [],
    )
    @deprecate_arguments(converter=_data_type_convertor)
    def add_surfaces_request(
        self,
        data_types: List[SurfaceDataType] | List[str],
        surfaces: List[int | str],
        overset_mesh: bool | None = False,
    ) -> None:
        """Add request to get surface data (vertices, face connectivity, centroids, and
        normals).

        Parameters
        ----------
        data_types : List[SurfaceDataType] | List[str],
            SurfaceDataType Enum members.
        surfaces : List[int | str]
            List of surface IDS or surface names for the surface data.
        overset_mesh : bool, optional
            Whether to get the overset met. The default is ``False``.

        Returns
        -------
        None
        """
        surface_ids = _get_surface_ids(
            field_info=self._field_info,
            allowed_surface_names=self._allowed_surface_names,
            surfaces=surfaces,
        )
        updated_data_types = []
        for d_type in data_types:
            if isinstance(d_type, str):
                updated_data_types.append(SurfaceDataType(d_type))
            else:
                updated_data_types.append(d_type)
        data_types = updated_data_types
        self._fields_request.surfaceRequest.extend(
            [
                FieldDataProtoModule.SurfaceRequest(
                    surfaceId=surface_id,
                    oversetMesh=overset_mesh,
                    provideFaces=SurfaceDataType.FacesConnectivity in data_types,
                    provideVertices=SurfaceDataType.Vertices in data_types,
                    provideFacesCentroid=SurfaceDataType.FacesCentroid in data_types,
                    provideFacesNormal=SurfaceDataType.FacesNormal in data_types,
                )
                for surface_id in surface_ids
            ]
        )

    @deprecate_argument(
        old_arg="surface_names",
        new_arg="surfaces",
        converter=lambda old_arg_val: old_arg_val or [],
    )
    @deprecate_argument(
        old_arg="surface_ids",
        new_arg="surfaces",
        converter=lambda old_arg_val: old_arg_val or [],
    )
    def add_scalar_fields_request(
        self,
        field_name: str,
        surfaces: List[int | str],
        node_value: bool | None = True,
        boundary_value: bool | None = True,
    ) -> None:
        """Add request to get scalar field data on surfaces.

        Parameters
        ----------
        field_name : str
            Name of the scalar field.
        surfaces : List[int | str]
            List of surface IDS or surface names for the surface data.
        node_value : bool, optional
            Whether to provide the nodal location. The default is ``True``. If
            ``False``, the element location is provided.
        boundary_value : bool, optional
            Whether to provide the slip velocity at the wall boundaries. The default
            is ``True``. When ``True``, no slip velocity is provided.

        Returns
        -------
        None
        """
        surface_ids = _get_surface_ids(
            field_info=self._field_info,
            allowed_surface_names=self._allowed_surface_names,
            surfaces=surfaces,
        )
        self._fields_request.scalarFieldRequest.extend(
            [
                FieldDataProtoModule.ScalarFieldRequest(
                    surfaceId=surface_id,
                    scalarFieldName=self._allowed_scalar_field_names.valid_name(
                        field_name
                    ),
                    dataLocation=(
                        FieldDataProtoModule.DataLocation.Nodes
                        if node_value
                        else FieldDataProtoModule.DataLocation.Elements
                    ),
                    provideBoundaryValues=boundary_value,
                )
                for surface_id in surface_ids
            ]
        )

    @deprecate_argument(
        old_arg="surface_names",
        new_arg="surfaces",
        converter=lambda old_arg_val: old_arg_val or [],
    )
    @deprecate_argument(
        old_arg="surface_ids",
        new_arg="surfaces",
        converter=lambda old_arg_val: old_arg_val or [],
    )
    def add_vector_fields_request(
        self,
        field_name: str,
        surfaces: List[int | str],
    ) -> None:
        """Add request to get vector field data on surfaces.

        Parameters
        ----------
        field_name : str
            Name of the vector field.
        surfaces : List[int | str]
            List of surface IDS or surface names for the surface data.

        Returns
        -------
        None
        """
        surface_ids = _get_surface_ids(
            field_info=self._field_info,
            allowed_surface_names=self._allowed_surface_names,
            surfaces=surfaces,
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

    @deprecate_argument(
        old_arg="surface_names",
        new_arg="surfaces",
        converter=lambda old_arg_val: old_arg_val or [],
    )
    @deprecate_argument(
        old_arg="surface_ids",
        new_arg="surfaces",
        converter=lambda old_arg_val: old_arg_val or [],
    )
    def add_pathlines_fields_request(
        self,
        field_name: str,
        surfaces: List[int | str],
        additional_field_name: str | None = "",
        provide_particle_time_field: bool | None = False,
        node_value: bool | None = True,
        steps: int | None = 500,
        step_size: float | None = 500,
        skip: int | None = 0,
        reverse: bool | None = False,
        accuracy_control_on: bool | None = False,
        tolerance: float | None = 0.001,
        coarsen: int | None = 1,
        velocity_domain: str | None = "all-phases",
        zones: list = [],
    ) -> None:
        """Add request to get pathlines field on surfaces.

        Parameters
        ----------
        field_name : str
            Name of the scalar field to color pathlines.
        surfaces : List[int | str]
            List of surface IDS or surface names for the surface data.
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
            Whether to draw pathlines in a reverse direction. The default is ``False``.
        accuracy_control_on: bool, optional
            Whether to control accuracy. The default is ``False``.
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
            surfaces=surfaces,
        )
        self._fields_request.pathlinesFieldRequest.extend(
            [
                FieldDataProtoModule.PathlinesFieldRequest(
                    surfaceId=surface_id,
                    field=field_name,
                    additionalField=additional_field_name,
                    provideParticleTimeField=provide_particle_time_field,
                    dataLocation=(
                        FieldDataProtoModule.DataLocation.Nodes
                        if node_value
                        else FieldDataProtoModule.DataLocation.Elements
                    ),
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

    def get_fields(self) -> Dict[int | Tuple, Dict[int, Dict[str, np.array]]]:
        """Get data for previously added requests and then clear all requests.

        Returns
        -------
        Dict[int, Dict[int, Dict[str, np.array]]]
            Data is returned as dictionary of dictionaries in the following structure:
            tag int | Tuple-> surface_id [int] -> field_name [str] -> field_data[np.array]

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
    surfaces: List[int | str],
) -> List[int]:
    """Get surface IDs based on surface names or IDs.

    Parameters
    ----------
    surfaces : List[int], | List[str]
        List of surface IDs or surface names.

    Returns
    -------
    List[int]
    """
    surface_ids = []
    for surf in surfaces:
        if isinstance(surf, str):
            surface_ids.extend(
                field_info.get_surfaces_info()[allowed_surface_names.valid_name(surf)][
                    "surface_id"
                ]
            )
        else:
            surface_ids.append(surf)
    return list(set(surface_ids))


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
                    else (
                        _get_tag_for_scalar_field_request(
                            field_request_info.scalarFieldRequest
                        )
                        if request_type == "scalarFieldRequest"
                        else (
                            _get_tag_for_vector_field_request()
                            if request_type == "vectorFieldRequest"
                            else (
                                _get_tag_for_pathlines_field_request(
                                    field_request_info.pathlinesFieldRequest
                                )
                                if request_type == "pathlinesFieldRequest"
                                else None
                            )
                        )
                    )
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
        scheme_eval=None,
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

    @deprecate_argument(
        old_arg="surface_name",
        new_arg="surfaces",
        converter=lambda old_arg_val: [old_arg_val] if old_arg_val else [],
    )
    @deprecate_argument(
        old_arg="surface_ids",
        new_arg="surfaces",
        converter=lambda old_arg_val: old_arg_val or [],
    )
    def get_scalar_field_data(
        self,
        field_name: str,
        surfaces: List[int | str],
        node_value: bool | None = True,
        boundary_value: bool | None = True,
    ) -> ScalarFieldData | Dict[int, ScalarFieldData]:
        """Get scalar field data on a surface.

        Parameters
        ----------
        field_name : str
            Name of the scalar field.
        surfaces : List[int | str]
            List of surface IDS or surface names for the surface data.
        node_value : bool, optional
            Whether to provide data for the nodal location. The default is ``True``.
            When ``False``, data is provided for the element location.
        boundary_value : bool, optional
            Whether to provide slip velocity at the wall boundaries. The default is
            ``True``. When ``True``, no slip velocity is provided.

        Returns
        -------
        ScalarFieldData | Dict[int, ScalarFieldData]
            If a surface name is provided as input, scalar field data is returned. If surface
            IDs are provided as input, a dictionary containing a map of surface IDs to scalar
            field data.
        """
        surface_ids = _get_surface_ids(
            field_info=self._field_info,
            allowed_surface_names=self._allowed_surface_names,
            surfaces=surfaces,
        )
        fields_request = get_fields_request()
        fields_request.scalarFieldRequest.extend(
            [
                FieldDataProtoModule.ScalarFieldRequest(
                    surfaceId=surface_id,
                    scalarFieldName=self._allowed_scalar_field_names.valid_name(
                        field_name
                    ),
                    dataLocation=(
                        FieldDataProtoModule.DataLocation.Nodes
                        if node_value
                        else FieldDataProtoModule.DataLocation.Elements
                    ),
                    provideBoundaryValues=boundary_value,
                )
                for surface_id in surface_ids
            ]
        )

        fields = ChunkParser().extract_fields(self._service.get_fields(fields_request))
        scalar_field_data = next(iter(fields.values()))

        if len(surfaces) == 1 and isinstance(surfaces[0], str):
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

    @deprecate_argument(
        old_arg="surface_name",
        new_arg="surfaces",
        converter=lambda old_arg_val: [old_arg_val] if old_arg_val else [],
    )
    @deprecate_argument(
        old_arg="surface_ids",
        new_arg="surfaces",
        converter=lambda old_arg_val: old_arg_val or [],
    )
    @deprecate_argument(
        old_arg="data_type",
        new_arg="data_types",
        converter=lambda old_arg_val: [old_arg_val] if old_arg_val else [],
    )
    def get_surface_data(
        self,
        data_types: List[SurfaceDataType] | List[str],
        surfaces: List[int | str],
        overset_mesh: bool | None = False,
    ) -> (
        Vertices
        | FacesConnectivity
        | FacesNormal
        | FacesCentroid
        | Dict[int, Vertices | FacesConnectivity | FacesNormal | FacesCentroid]
    ):
        """Get surface data (vertices, faces connectivity, centroids, and normals).

        Parameters
        ----------
        data_types : List[SurfaceDataType] | List[str],
            SurfaceDataType Enum members.
        surfaces : List[int | str]
            List of surface IDS or surface names for the surface data.
        overset_mesh : bool, optional
            Whether to provide the overset method. The default is ``False``.

        Returns
        -------
        Vertices, FacesConnectivity, FacesNormal, FacesCentroid | Dict[int, Vertices | FacesConnectivity | FacesNormal | FacesCentroid]
             If a surface name is provided as input, face vertices, connectivity data, and normal or centroid data are returned.
             If surface IDs are provided as input, a dictionary containing a map of surface IDs to face
             vertices, connectivity data, and normal or centroid data is returned.
        """
        surface_ids = _get_surface_ids(
            field_info=self._field_info,
            allowed_surface_names=self._allowed_surface_names,
            surfaces=surfaces,
        )
        updated_data = []
        for d_type in data_types:
            if isinstance(d_type, str):
                updated_data.append(SurfaceDataType(d_type))
            else:
                updated_data.append(d_type)
        data_types = updated_data
        fields_request = get_fields_request()
        fields_request.surfaceRequest.extend(
            [
                FieldDataProtoModule.SurfaceRequest(
                    surfaceId=surface_id,
                    oversetMesh=overset_mesh,
                    provideFaces=SurfaceDataType.FacesConnectivity in data_types,
                    provideVertices=SurfaceDataType.Vertices in data_types,
                    provideFacesCentroid=SurfaceDataType.FacesCentroid in data_types,
                    provideFacesNormal=SurfaceDataType.FacesNormal in data_types,
                )
                for surface_id in surface_ids
            ]
        )
        fields = ChunkParser().extract_fields(self._service.get_fields(fields_request))
        surface_data = next(iter(fields.values()))

        def _get_surfaces_data(parent_class, surf_id, _data_type):
            return parent_class(
                surf_id,
                surface_data[surf_id][SurfaceDataType(_data_type).value],
            )

        if SurfaceDataType.Vertices in data_types:
            if len(surfaces) == 1 and isinstance(surfaces[0], str):
                return _get_surfaces_data(
                    Vertices, surface_ids[0], SurfaceDataType.Vertices
                )
            else:
                return {
                    surface_id: _get_surfaces_data(
                        Vertices, surface_id, SurfaceDataType.Vertices
                    )
                    for surface_id in surface_ids
                }

        if SurfaceDataType.FacesCentroid in data_types:
            if len(surfaces) == 1 and isinstance(surfaces[0], str):
                return _get_surfaces_data(
                    FacesCentroid, surface_ids[0], SurfaceDataType.FacesCentroid
                )
            else:
                return {
                    surface_id: _get_surfaces_data(
                        FacesCentroid, surface_id, SurfaceDataType.FacesCentroid
                    )
                    for surface_id in surface_ids
                }

        if SurfaceDataType.FacesConnectivity in data_types:
            if len(surfaces) == 1 and isinstance(surfaces[0], str):
                return _get_surfaces_data(
                    FacesConnectivity, surface_ids[0], SurfaceDataType.FacesConnectivity
                )
            else:
                return {
                    surface_id: _get_surfaces_data(
                        FacesConnectivity, surface_id, SurfaceDataType.FacesConnectivity
                    )
                    for surface_id in surface_ids
                }

        if SurfaceDataType.FacesNormal in data_types:
            if len(surfaces) == 1 and isinstance(surfaces[0], str):
                return _get_surfaces_data(
                    FacesNormal, surface_ids[0], SurfaceDataType.FacesNormal
                )
            else:
                return {
                    surface_id: _get_surfaces_data(
                        FacesNormal, surface_id, SurfaceDataType.FacesNormal
                    )
                    for surface_id in surface_ids
                }

    @deprecate_argument(
        old_arg="surface_name",
        new_arg="surfaces",
        converter=lambda old_arg_val: [old_arg_val] if old_arg_val else [],
    )
    @deprecate_argument(
        old_arg="surface_ids",
        new_arg="surfaces",
        converter=lambda old_arg_val: old_arg_val or [],
    )
    def get_vector_field_data(
        self,
        field_name: str,
        surfaces: List[int | str],
    ) -> VectorFieldData | Dict[int, VectorFieldData]:
        """Get vector field data on a surface.

        Parameters
        ----------
        field_name : str
            Name of the vector field.
        surfaces : List[int | str]
            List of surface IDS or surface names for the surface data.

        Returns
        -------
        VectorFieldData | Dict[int, VectorFieldData]
            If a surface name is provided as input, vector field data is returned.
            If surface IDs are provided as input, a dictionary containing a map of
            surface IDs to vector field data is returned.
        """
        surface_ids = _get_surface_ids(
            field_info=self._field_info,
            allowed_surface_names=self._allowed_surface_names,
            surfaces=surfaces,
        )
        for surface_id in surface_ids:
            self.scheme_eval.string_eval(f"(surface? {surface_id})")
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

        if len(surfaces) == 1 and isinstance(surfaces[0], str):
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

    @deprecate_argument(
        old_arg="surface_name",
        new_arg="surfaces",
        converter=lambda old_arg_val: [old_arg_val] if old_arg_val else [],
    )
    @deprecate_argument(
        old_arg="surface_ids",
        new_arg="surfaces",
        converter=lambda old_arg_val: old_arg_val or [],
    )
    def get_pathlines_field_data(
        self,
        field_name: str,
        surfaces: List[int | str],
        additional_field_name: str | None = "",
        provide_particle_time_field: bool | None = False,
        node_value: bool | None = True,
        steps: int | None = 500,
        step_size: float | None = 500,
        skip: int | None = 0,
        reverse: bool | None = False,
        accuracy_control_on: bool | None = False,
        tolerance: float | None = 0.001,
        coarsen: int | None = 1,
        velocity_domain: str | None = "all-phases",
        zones: list = [],
    ) -> Dict:
        """Get the pathlines field data on a surface.

        Parameters
        ----------
        field_name : str
            Name of the scalar field to color pathlines.
        surfaces : List[int | str]
            List of surface IDS or surface names for the surface data.
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
        accuracy_control_on: bool, optional
            Whether to control accuracy. The default is ``False``.
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
            surfaces=surfaces,
        )
        fields_request = get_fields_request()
        fields_request.pathlinesFieldRequest.extend(
            [
                FieldDataProtoModule.PathlinesFieldRequest(
                    surfaceId=surface_id,
                    field=field_name,
                    additionalField=additional_field_name,
                    provideParticleTimeField=provide_particle_time_field,
                    dataLocation=(
                        FieldDataProtoModule.DataLocation.Nodes
                        if node_value
                        else FieldDataProtoModule.DataLocation.Elements
                    ),
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

        if len(surfaces) == 1 and isinstance(surfaces[0], str):
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
