"""Deprecated wrappers over FieldData gRPC service of Fluent."""

from typing import Callable, Dict, List
import warnings

from ansys.api.fluent.v0 import field_data_pb2 as FieldDataProtoModule
from ansys.fluent.core.services.field_data import (
    ChunkParser,
    FieldDataService,
    FieldInfo,
    FieldTransaction,
    SurfaceDataType,
    _AllowedScalarFieldNames,
    _AllowedSurfaceIDs,
    _AllowedSurfaceNames,
    _AllowedVectorFieldNames,
    _FieldMethod,
    _get_surface_ids,
    get_fields_request,
    override_help_text,
)
from ansys.fluent.core.utils.deprecate import deprecate_argument
from ansys.fluent.core.warnings import PyFluentDeprecationWarning

DEPRECATION_MSG = "'field_data_old' is deprecated. Use 'field_data' instead."


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


class DeprecatedFieldData:
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
        warnings.warn(DEPRECATION_MSG, PyFluentDeprecationWarning)
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
        warnings.warn(DEPRECATION_MSG, PyFluentDeprecationWarning)
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
        warnings.warn(DEPRECATION_MSG, PyFluentDeprecationWarning)
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
        warnings.warn(DEPRECATION_MSG, PyFluentDeprecationWarning)
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
        zones: list | None = None,
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
        if zones is None:
            zones = []
        warnings.warn(DEPRECATION_MSG, PyFluentDeprecationWarning)
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
