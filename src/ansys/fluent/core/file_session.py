# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Provides a module for file session."""

from typing import Dict, List
import warnings

from deprecated.sphinx import deprecated
import numpy as np

from ansys.api.fluent.v0.field_data_pb2 import DataLocation
from ansys.fluent.core import PyFluentDeprecationWarning
from ansys.fluent.core.field_data_interfaces import (
    BaseFieldInfo,
    FieldBatch,
    FieldDataSource,
    PathlinesFieldDataRequest,
    ScalarFieldDataRequest,
    SurfaceDataType,
    SurfaceFieldDataRequest,
    VectorFieldDataRequest,
    _AllowedScalarFieldNames,
    _AllowedSurfaceNames,
    _ReturnFieldData,
    _ScalarFields,
    _SurfaceIds,
    _SurfaceNames,
    _transform_faces_connectivity_data,
    _VectorFields,
)
from ansys.fluent.core.filereader.case_file import CaseFile
from ansys.fluent.core.filereader.data_file import (
    DataFile,
    _to_scalar_field_name,
    _to_vector_field_name,
)
from ansys.fluent.core.utils.deprecate import all_deprecators


class InvalidMultiPhaseFieldName(ValueError):
    """Raised when multi-phase field name is inappropriate."""

    def __init__(self):
        """Initialize InvalidMultiPhaseFieldName."""
        super().__init__("Multi-phase field name should start with 'phase-'.")


class InvalidFieldName(ValueError):
    """Raised when a field name is inappropriate."""

    def __init__(self):
        """Initialize InvalidFieldName."""
        super().__init__("The only allowed field is 'velocity'.")


def _data_type_convertor(args_dict):
    d_type_list = []
    d_type_map = {
        "provide_vertices": SurfaceDataType.Vertices,
        "provide_faces": SurfaceDataType.FacesConnectivity,
    }
    for key, val in d_type_map.items():
        if args_dict.get(key):
            d_type_list.append(val)
        args_dict.pop(key, None)
    args_dict["data_types"] = d_type_list
    return args_dict


class BatchFieldData:
    """Provides access to Fluent field data on surfaces collected via batches."""

    def __init__(
        self,
        data: Dict,
        field_info,
        allowed_surface_names,
        allowed_scalar_field_names,
    ):
        """__init__ method of BatchFieldData class."""
        self.data = data
        self._field_info = field_info
        self._allowed_surface_names = allowed_surface_names
        self._allowed_scalar_field_names = allowed_scalar_field_names
        self._returned_data = _ReturnFieldData()

    def get_surface_ids(self, surfaces: List[str | int]) -> List[int]:
        """Get a list of surface ids based on surfaces provided as inputs."""
        return _get_surface_ids(
            field_info=self._field_info,
            surfaces=surfaces,
        )

    def _get_scalar_field_data(
        self,
        **kwargs,
    ) -> Dict[int | str, np.array]:
        scalar_field_data = self.data[
            (
                ("type", "scalar-field"),
                ("dataLocation", 0 if kwargs.get("node_value") else 1),
                ("boundaryValues", kwargs.get("boundary_value")),
            )
        ]
        return self._returned_data._scalar_data(
            _to_scalar_field_name(kwargs.get("field_name")),
            kwargs.get("surfaces"),
            self.get_surface_ids(kwargs.get("surfaces")),
            scalar_field_data,
        )

    def _get_surface_data(
        self,
        **kwargs,
    ) -> Dict[int | str, Dict[SurfaceDataType, np.array | List[np.array]]]:
        surface_data = self.data[(("type", "surface-data"),)]
        return self._returned_data._surface_data(
            kwargs.get("data_types"),
            kwargs.get("surfaces"),
            self.get_surface_ids(kwargs.get("surfaces")),
            surface_data,
            flatten_connectivity=kwargs.get("flatten_connectivity"),
        )

    def _get_vector_field_data(
        self,
        **kwargs,
    ) -> Dict[int | str, np.array]:
        vector_field_data = self.data[(("type", "vector-field"),)]
        return self._returned_data._vector_data(
            _to_vector_field_name(kwargs.get("field_name")),
            kwargs.get("surfaces"),
            self.get_surface_ids(kwargs.get("surfaces")),
            vector_field_data,
        )

    def _get_pathlines_field_data(
        self,
        **kwargs,
    ) -> Dict:
        if kwargs.get("zones") is None:
            zones = []
        del zones
        pathlines_data = self.data[
            (
                ("type", "pathlines-field"),
                (
                    "field",
                    _to_scalar_field_name(kwargs.get("field_name")),
                ),
            )
        ]
        return self._returned_data._pathlines_data(
            _to_scalar_field_name(kwargs.get("field_name")),
            kwargs.get("surfaces"),
            self.get_surface_ids(kwargs.get("surfaces")),
            pathlines_data,
        )

    def get_field_data(
        self,
        obj: (
            SurfaceFieldDataRequest
            | ScalarFieldDataRequest
            | VectorFieldDataRequest
            | PathlinesFieldDataRequest
        ),
    ) -> Dict[int | str, Dict | np.array]:
        """Get the surface, scalar, vector or path-lines field data on a surface.

        Returns
        -------
        Dict[int | str, Dict | np.array]
            Field data for the requested surface. If field data is unavailable for the surface,
            an empty array is returned and a warning is issued. Users should always check
            the array size before using the data.

            Example:
                data = get_field_data(field_data_request)[surface_id]
                if data.size == 0:
                    # Handle missing data
        """
        if isinstance(obj, SurfaceFieldDataRequest):
            return self._get_surface_data(**obj._asdict())
        elif isinstance(obj, ScalarFieldDataRequest):
            return self._get_scalar_field_data(**obj._asdict())
        elif isinstance(obj, VectorFieldDataRequest):
            return self._get_vector_field_data(**obj._asdict())
        elif isinstance(obj, PathlinesFieldDataRequest):
            return self._get_pathlines_field_data(**obj._asdict())

    def __len__(self):
        return len(self.data)

    def __call__(self):
        return self.data


class Batch(FieldBatch):
    """Populates field data on surfaces."""

    class _SurfaceTransaction:
        def __init__(self, surface_id, provide_vertices, provide_faces):
            self.surface_id = surface_id
            self.provide_vertices = provide_vertices
            self.provide_faces = provide_faces

    class _ScalarFieldTransaction:
        def __init__(self, field_name, surface_ids, phase="phase-1"):
            self.phase_name = phase
            self.field_name = field_name
            self.surface_ids = surface_ids

    class _VectorFieldTransaction:
        def __init__(self, field_name, surface_ids, phase="phase-1"):
            self.phase_name = phase
            self.field_name = field_name
            self.surface_ids = surface_ids

    def __init__(self, file_session, field_info):
        """__init__ method of Batch class."""
        self._surface_batches = []
        self._scalar_field_batches = []
        self._vector_field_batches = []
        self._file_session = file_session
        self._field_info = field_info
        self._cache_requests = []

    def get_surface_ids(self, surfaces: List[str | int]) -> List[int]:
        """Get a list of surface ids based on surfaces provided as inputs."""
        return _get_surface_ids(
            field_info=self._field_info,
            surfaces=surfaces,
        )

    @all_deprecators(
        deprecate_arg_mappings=[
            {
                "old_arg": "surface_names",
                "new_arg": "surfaces",
                "converter": lambda old_arg_val: old_arg_val,
            },
            {
                "old_arg": "surface_ids",
                "new_arg": "surfaces",
                "converter": lambda old_arg_val: old_arg_val,
            },
        ],
        data_type_converter=_data_type_convertor,
        deprecated_version="v0.25.0",
        deprecated_reason="Old arguments 'surface_ids' and 'surface_names' are deprecated. Use 'surfaces' instead.",
        warn_message="'add_surfaces_request' is deprecated, use 'add_requests' instead.",
    )
    def add_surfaces_request(
        self,
        data_types: List[SurfaceDataType] | List[str],
        surfaces: List[int | str],
    ) -> None:
        """Add request to get surface data (vertices, face connectivity, centroids, and
        normals).

        Parameters
        ----------
        data_types : List[SurfaceDataType] | List[str],
            SurfaceDataType Enum members.
        surfaces : List[int | str]
            List of surface IDS or surface names for the surface data.

        Returns
        -------
        None
        """
        self._add_surfaces_request(data_types=data_types, surfaces=surfaces)

    def _add_surfaces_request(
        self,
        data_types: List[SurfaceDataType] | List[str],
        surfaces: List[int | str],
    ) -> None:
        updated_types = []
        for d_type in data_types:
            if isinstance(d_type, str):
                updated_types.append(SurfaceDataType(d_type))
            else:
                updated_types.append(d_type)
        data_types = updated_types
        provide_vertices = SurfaceDataType.Vertices in data_types
        provide_faces = SurfaceDataType.FacesConnectivity in data_types
        for surface_id in self.get_surface_ids(surfaces):
            self._surface_batches.append(
                Batch._SurfaceTransaction(surface_id, provide_vertices, provide_faces)
            )

    @all_deprecators(
        deprecate_arg_mappings=[
            {
                "old_arg": "surface_names",
                "new_arg": "surfaces",
                "converter": lambda old_arg_val: old_arg_val,
            },
            {
                "old_arg": "surface_ids",
                "new_arg": "surfaces",
                "converter": lambda old_arg_val: old_arg_val,
            },
        ],
        data_type_converter=None,
        deprecated_version="v0.25.0",
        deprecated_reason="Old arguments 'surface_ids' and 'surface_names' are deprecated. Use 'surfaces' instead.",
        warn_message="'add_scalar_fields_request' is deprecated, use 'add_requests' instead.",
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

        Raises
        ------
        InvalidMultiPhaseFieldName
            If field name does not have prefix ``phase-`` for multi-phase cases.
        """
        self._add_scalar_fields_request(
            field_name=field_name,
            surfaces=surfaces,
            node_value=node_value,
            boundary_value=boundary_value,
        )

    def _add_scalar_fields_request(
        self,
        field_name: str,
        surfaces: List[int | str],
        node_value: bool | None = True,
        boundary_value: bool | None = True,
    ) -> None:
        surface_ids = self.get_surface_ids(surfaces)
        if len(self._file_session._data_file.get_phases()) > 1:
            if not field_name.startswith("phase-"):
                raise InvalidMultiPhaseFieldName()
            self._scalar_field_batches.append(
                Batch._ScalarFieldTransaction(
                    field_name, surface_ids, field_name.split(":")[0]
                )
            )
        else:
            self._scalar_field_batches.append(
                Batch._ScalarFieldTransaction(field_name, surface_ids)
            )

    @all_deprecators(
        deprecate_arg_mappings=[
            {
                "old_arg": "surface_names",
                "new_arg": "surfaces",
                "converter": lambda old_arg_val: old_arg_val,
            },
            {
                "old_arg": "surface_ids",
                "new_arg": "surfaces",
                "converter": lambda old_arg_val: old_arg_val,
            },
        ],
        data_type_converter=None,
        deprecated_version="v0.25.0",
        deprecated_reason="Old arguments 'surface_ids' and 'surface_names' are deprecated. Use 'surfaces' instead.",
        warn_message="'add_vector_fields_request' is deprecated, use 'add_requests' instead.",
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

        Raises
        ------
        InvalidMultiPhaseFieldName
            If field name does not have prefix ``phase-`` for multi-phase cases.
        """
        self._add_vector_fields_request(field_name=field_name, surfaces=surfaces)

    def _add_vector_fields_request(
        self,
        field_name: str,
        surfaces: List[int | str],
    ) -> None:
        surface_ids = self.get_surface_ids(surfaces)
        if len(self._file_session._data_file.get_phases()) > 1:
            if not field_name.startswith("phase-"):
                raise InvalidMultiPhaseFieldName()
            self._vector_field_batches.append(
                Batch._VectorFieldTransaction(
                    field_name, surface_ids, field_name.split(":")[0]
                )
            )
        else:
            self._vector_field_batches.append(
                Batch._VectorFieldTransaction(field_name, surface_ids)
            )

    @all_deprecators(
        deprecate_arg_mappings=[
            {
                "old_arg": "surface_names",
                "new_arg": "surfaces",
                "converter": lambda old_arg_val: old_arg_val,
            },
            {
                "old_arg": "surface_ids",
                "new_arg": "surfaces",
                "converter": lambda old_arg_val: old_arg_val,
            },
        ],
        data_type_converter=None,
        deprecated_version="v0.25.0",
        deprecated_reason="Old arguments 'surface_ids' and 'surface_names' are deprecated. Use 'surfaces' instead.",
        warn_message="Pathlines are not supported.",
    )
    def add_pathlines_fields_request(
        self,
        field_name: str,
        surfaces: List[int | str],
    ):
        """Add request to get pathlines field on surfaces.

        Parameters
        ----------
        field_name : str
            Name of the scalar field to color pathlines.
        surfaces : List[int | str]
            List of surface IDS or surface names for the surface data.

        Returns
        -------
        None
        """
        raise NotImplementedError("Pathlines are not supported.")

    def _add_pathlines_fields_request(
        self,
        field_name: str,
        surfaces: List[int | str],
    ):
        raise NotImplementedError("Pathlines are not supported.")

    def add_requests(
        self,
        obj: (
            SurfaceFieldDataRequest
            | ScalarFieldDataRequest
            | VectorFieldDataRequest
            | PathlinesFieldDataRequest
        ),
        *args: SurfaceFieldDataRequest
        | ScalarFieldDataRequest
        | VectorFieldDataRequest
        | PathlinesFieldDataRequest,
    ):
        """Add request to get surface, scalar, vector or path-lines field on surfaces."""
        for req in (obj,) + args:
            req = req._replace(surfaces=self.get_surface_ids(req.surfaces))
            if req in self._cache_requests:
                warnings.warn(f"{req._asdict()} is duplicate and being ignored.")
                continue
            elif isinstance(req, SurfaceFieldDataRequest):
                self._add_surfaces_request(
                    data_types=req.data_types,
                    surfaces=req.surfaces,
                )
            elif isinstance(req, ScalarFieldDataRequest):
                self._add_scalar_fields_request(
                    field_name=_to_scalar_field_name(req.field_name),
                    surfaces=req.surfaces,
                    node_value=req.node_value,
                    boundary_value=req.boundary_value,
                )
            elif isinstance(req, VectorFieldDataRequest):
                self._add_vector_fields_request(
                    field_name=_to_vector_field_name(req.field_name),
                    surfaces=req.surfaces,
                )
            elif isinstance(req, PathlinesFieldDataRequest):
                self._add_pathlines_fields_request(
                    field_name=req.field_name,
                    surfaces=req.surfaces,
                )
            self._cache_requests.append(req)
        return self

    def get_fields(self):
        """Get data for previously added requests."""
        warnings.warn(
            "'get_fields' is deprecated, use 'get_response' instead",
            PyFluentDeprecationWarning,
        )
        return self.get_response()

    def get_response(self):
        """Get data for previously added requests.

        Returns
        -------
        Dict[int, Dict[int, Dict[str, np.array]]]
            Data is returned as dictionary of dictionaries in the following structure:
            tag int | Tuple-> surface_id [int] -> field_name [str] -> field_data[np.array]

        Raises
        ------
        InvalidFieldName
            If any field other than ``"velocity"`` is provided.
        """
        mesh = self._file_session._case_file.get_mesh()
        field_data = {}

        scalar_field_tag = (
            ("type", "scalar-field"),
            (
                "dataLocation",
                DataLocation.Elements,
            ),
            ("boundaryValues", False),
        )

        for batch in self._scalar_field_batches:
            if scalar_field_tag not in field_data:
                field_data[scalar_field_tag] = {}
            field_data_surface = field_data[scalar_field_tag]
            for surface_id in batch.surface_ids:
                field_data_surface[surface_id] = {}
                field_data_surface[surface_id][batch.field_name] = (
                    self._file_session._data_file.get_face_scalar_field_data(
                        batch.phase_name, batch.field_name, surface_id
                    )
                )

        vector_field_tag = (("type", "vector-field"),)

        for batch in self._vector_field_batches:
            if "velocity" not in batch.field_name:
                raise InvalidFieldName()
            if vector_field_tag not in field_data:
                field_data[vector_field_tag] = {}
            field_data_surface = field_data[vector_field_tag]
            for surface_id in batch.surface_ids:
                field_data_surface[surface_id] = {}
                field_data_surface[surface_id][batch.field_name] = (
                    self._file_session._data_file.get_face_vector_field_data(
                        batch.phase_name, surface_id
                    )
                )
                field_data_surface[surface_id]["vector-scale"] = np.array([0.1])

        for batch in self._surface_batches:
            if (("type", "surface-data"),) not in field_data:
                field_data[(("type", "surface-data"),)] = {}
            field_data_surface = field_data[(("type", "surface-data"),)]
            field_data_surface[batch.surface_id] = {}
            field_data_surface[batch.surface_id]["faces"] = mesh.get_connectivity(
                batch.surface_id
            )
            field_data_surface[batch.surface_id]["vertices"] = mesh.get_vertices(
                batch.surface_id
            )
        return BatchFieldData(
            field_data,
            self._field_info,
            _AllowedSurfaceNames(self._field_info),
            _AllowedScalarFieldNames(True, self._field_info),
        )


class FileFieldData(FieldDataSource):
    """File field data."""

    def __init__(self, file_session, field_info):
        """Initialize FileFieldData."""
        self._file_session = file_session
        self._field_info = field_info
        self.scalar_fields = _ScalarFields(
            self._field_info._get_scalar_fields_info, self._field_info
        )
        self.vector_fields = _VectorFields(self._field_info._get_vector_fields_info)
        self.surfaces = _SurfaceNames(self._field_info._get_surfaces_info)

    @property
    def surface_ids(self):
        """Get the surface ids."""
        return _SurfaceIds(
            _get_surface_ids(
                self._field_info, list(self._field_info._get_surfaces_info())
            )
        )

    def new_batch(self):
        """Create a new field batch."""
        return Batch(self._file_session, self._field_info)

    @deprecated(version="0.34", reason="Use `new_batch` instead.")
    def new_transaction(self):
        """Create a new field transaction."""
        return self.new_batch()

    def get_surface_ids(self, surfaces: List[str | int]) -> List[int]:
        """Get a list of surface ids based on surfaces provided as inputs."""
        return _get_surface_ids(
            field_info=self._field_info,
            surfaces=surfaces,
        )

    @all_deprecators(
        deprecate_arg_mappings=[
            {
                "old_arg": "surface_names",
                "new_arg": "surfaces",
                "converter": lambda old_arg_val: [old_arg_val],
            },
            {
                "old_arg": "surface_ids",
                "new_arg": "surfaces",
                "converter": lambda old_arg_val: old_arg_val,
            },
            {
                "old_arg": "data_type",
                "new_arg": "data_types",
                "converter": lambda old_arg_val: [old_arg_val] if old_arg_val else None,
            },
        ],
        data_type_converter=None,
        deprecated_version="v0.25.0",
        deprecated_reason="Old arguments 'surface_ids', 'surface_names' and 'data_type' are deprecated. Use 'surfaces' and 'data_types' instead.",
        warn_message="'get_surface_data' is deprecated, use 'get_field_data' instead.",
    )
    def get_surface_data(
        self,
        data_types: List[SurfaceDataType] | List[str],
        surfaces: List[int | str],
        overset_mesh: bool | None = False,
        flatten_connectivity: bool = False,
    ):
        """Get surface data (vertices and faces connectivity).

        Parameters
        ----------
        data_types : List[SurfaceDataType] | List[str],
            SurfaceDataType Enum members.
        surfaces : List[int | str]
            List of surface IDS or surface names for the surface data.
        overset_mesh : bool, optional
            Whether to provide the overset method. The default is ``False``.
        flatten_connectivity: bool, optional
            Whether to provide faces connectivity data in flattened format.

        Returns
        -------
        Vertices | FacesConnectivity | Dict[int, Vertices | FacesConnectivity]
             If a surface name is provided as input, face vertices, connectivity data, and normal or centroid data are returned.
             If surface IDs are provided as input, a dictionary containing a map of surface IDs to face
             vertices, connectivity data, and normal or centroid data is returned.
        """
        return self._get_surface_data(
            data_types=data_types,
            surfaces=surfaces,
            overset_mesh=overset_mesh,
            flatten_connectivity=flatten_connectivity,
        )

    def _get_surface_data(
        self,
        data_types: List[SurfaceDataType] | List[str],
        surfaces: List[int | str],
        overset_mesh: bool | None = False,
        flatten_connectivity: bool = False,
    ):
        for d_type in data_types:
            if isinstance(d_type, str):
                data_types.remove(d_type)
                data_types.append(SurfaceDataType(d_type))

        surface_ids = self.get_surface_ids(surfaces=surfaces)

        if SurfaceDataType.Vertices in data_types:
            return {
                surface: self._file_session._case_file.get_mesh()
                .get_vertices(surface_ids[count])
                .reshape(-1, 3)
                for count, surface in enumerate(surfaces)
            }

        if SurfaceDataType.FacesConnectivity in data_types:
            if flatten_connectivity:
                return {
                    surface: self._file_session._case_file.get_mesh().get_connectivity(
                        surface_ids[count]
                    )
                    for count, surface in enumerate(surfaces)
                }
            else:
                warnings.warn(
                    "Structured face connectivity output is deprecated and will be replaced by the flat format "
                    "in a future release. In the current release, pass 'flatten_connectivity=True' argument while creating the "
                    "'SurfaceFieldDataRequest' to request data in the flat format.",
                    PyFluentDeprecationWarning,
                )
                return {
                    surface: _transform_faces_connectivity_data(
                        self._file_session._case_file.get_mesh().get_connectivity(
                            surface_ids[count]
                        )
                    )
                    for count, surface in enumerate(surfaces)
                }

    @all_deprecators(
        deprecate_arg_mappings=[
            {
                "old_arg": "surface_names",
                "new_arg": "surfaces",
                "converter": lambda old_arg_val: [old_arg_val],
            },
            {
                "old_arg": "surface_ids",
                "new_arg": "surfaces",
                "converter": lambda old_arg_val: old_arg_val,
            },
        ],
        data_type_converter=None,
        deprecated_version="v0.25.0",
        deprecated_reason="Old arguments 'surface_ids' and 'surface_names' are deprecated. Use 'surfaces' instead.",
        warn_message="'get_scalar_field_data' is deprecated, use 'get_field_data' instead.",
    )
    def get_scalar_field_data(
        self,
        field_name: str,
        surfaces: List[int | str],
        node_value: bool | None = True,
        boundary_value: bool | None = True,
    ):
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

        Raises
        ------
        InvalidMultiPhaseFieldName
            If field name does not have prefix ``phase-`` for multi-phase cases.
        """
        return self._get_scalar_field_data(
            field_name=field_name,
            surfaces=surfaces,
            node_value=node_value,
            boundary_value=boundary_value,
        )

    def _get_scalar_field_data(
        self,
        field_name: str,
        surfaces: List[int | str],
        node_value: bool | None = True,
        boundary_value: bool | None = True,
    ):
        surface_ids = self.get_surface_ids(surfaces=surfaces)
        if len(self._file_session._data_file.get_phases()) > 1:
            if not field_name.startswith("phase-"):
                raise InvalidMultiPhaseFieldName()
            return {
                surface: self._file_session._data_file.get_face_scalar_field_data(
                    field_name.split(":")[0],
                    field_name.split(":")[1],
                    surface_ids[count],
                )
                for count, surface in enumerate(surfaces)
            }
        else:
            return {
                surface: self._file_session._data_file.get_face_scalar_field_data(
                    "phase-1", field_name, surface_ids[count]
                )
                for count, surface in enumerate(surfaces)
            }

    @all_deprecators(
        deprecate_arg_mappings=[
            {
                "old_arg": "surface_names",
                "new_arg": "surfaces",
                "converter": lambda old_arg_val: [old_arg_val],
            },
            {
                "old_arg": "surface_ids",
                "new_arg": "surfaces",
                "converter": lambda old_arg_val: old_arg_val,
            },
        ],
        data_type_converter=None,
        deprecated_version="v0.25.0",
        deprecated_reason="Old arguments 'surface_ids' and 'surface_names' are deprecated. Use 'surfaces' instead.",
        warn_message="'get_vector_field_data' is deprecated, use 'get_field_data' instead.",
    )
    def get_vector_field_data(
        self,
        field_name: str,
        surfaces: List[int | str],
    ):
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

        Raises
        ------
        InvalidFieldName
            If any field other than ``"velocity"`` is provided.
        InvalidMultiPhaseFieldName
            If field name does not have prefix ``phase-`` for multi-phase cases.
        """
        return self._get_vector_field_data(
            field_name=field_name,
            surfaces=surfaces,
        )

    def _get_vector_field_data(
        self,
        field_name: str,
        surfaces: List[int | str],
    ):
        field_name = _to_vector_field_name(field_name)
        surface_ids = self.get_surface_ids(surfaces=surfaces)
        if (
            field_name.lower() != "velocity"
            and field_name.split(":")[1].lower() != "velocity"
        ):
            raise InvalidFieldName()

        if len(self._file_session._data_file.get_phases()) > 1:
            if not field_name.startswith("phase-"):
                raise InvalidMultiPhaseFieldName()
            return {
                surface: self._file_session._data_file.get_face_vector_field_data(
                    field_name.split(":")[0], surface_ids[count]
                ).reshape(-1, 3)
                for count, surface in enumerate(surfaces)
            }
        else:
            return {
                surface: self._file_session._data_file.get_face_vector_field_data(
                    "phase-1", surface_ids[count]
                ).reshape(-1, 3)
                for count, surface in enumerate(surfaces)
            }

    @all_deprecators(
        deprecate_arg_mappings=[
            {
                "old_arg": "surface_names",
                "new_arg": "surfaces",
                "converter": lambda old_arg_val: [old_arg_val],
            },
            {
                "old_arg": "surface_ids",
                "new_arg": "surfaces",
                "converter": lambda old_arg_val: old_arg_val,
            },
        ],
        data_type_converter=None,
        deprecated_version="v0.25.0",
        deprecated_reason="Old arguments 'surface_ids' and 'surface_names' are deprecated. Use 'surfaces' instead.",
        warn_message="Pathlines are not supported.",
    )
    def get_pathlines_field_data(
        self,
        field_name: str,
        surfaces: List[int | str],
    ):
        """Get the pathlines field data on a surface.

        Parameters
        ----------
        field_name : str
            Name of the scalar field to color pathlines.
        surfaces : List[int | str]
            List of surface IDS or surface names for the surface data.

        Returns
        -------
        Dict
            Dictionary containing a map of surface IDs to the pathline data.
            For example, pathlines connectivity, vertices, and field.
        """
        raise NotImplementedError("Pathlines are not supported.")

    def _get_pathlines_field_data(
        self,
        field_name: str,
        surfaces: List[int | str],
        **kwargs,
    ):
        raise NotImplementedError("Pathlines are not supported.")

    def get_field_data(
        self,
        obj: (
            SurfaceFieldDataRequest
            | ScalarFieldDataRequest
            | VectorFieldDataRequest
            | PathlinesFieldDataRequest
        ),
    ) -> Dict[int | str, Dict | np.array]:
        """Get the surface, scalar, vector or path-lines field data on a surface.

        Returns
        -------
        Dict[int | str, Dict | np.array]
            Field data for the requested surface. If field data is unavailable for the surface,
            an empty array is returned and a warning is issued. Users should always check
            the array size before using the data.

            Example:
                data = get_field_data(field_data_request)[surface_id]
                if data.size == 0:
                    # Handle missing data
        """
        if isinstance(obj, SurfaceFieldDataRequest):
            return self._get_surface_data(**obj._asdict())
        elif isinstance(obj, ScalarFieldDataRequest):
            return self._get_scalar_field_data(**obj._asdict())
        elif isinstance(obj, VectorFieldDataRequest):
            return self._get_vector_field_data(**obj._asdict())
        elif isinstance(obj, PathlinesFieldDataRequest):
            return self._get_pathlines_field_data(**obj._asdict())


class _FileFieldInfo(BaseFieldInfo):
    """File field info."""

    def __init__(self, file_session):
        """Initialize _FileFieldInfo."""
        self._file_session = file_session

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
        warnings.warn(
            "This usage is deprecated and will be removed in a future release. "
            f"Please use 'field_data.scalar_fields.range({field}, {node_value}, {surface_ids})' instead",
            PyFluentDeprecationWarning,
        )
        return self._get_scalar_field_range(field, node_value, surface_ids)

    def _get_scalar_field_range(
        self, field: str, node_value: bool = False, surface_ids: List[int] = None
    ) -> List[float]:
        minimum = None
        maximum = None
        if not surface_ids:
            surface_ids = self._file_session._case_file.get_mesh().get_surface_ids()
        for surface_id in surface_ids:
            data = self._file_session._data_file.get_face_scalar_field_data(
                "phase-1", field, surface_id
            )
            if len(data) == 0:
                continue
            minimum = min(data) if minimum is None else min(minimum, min(data))
            maximum = max(data) if maximum is None else max(maximum, max(data))

        return [minimum, maximum]

    def get_scalar_fields_info(self):
        """Get fields information (field name, domain, and section).

        Returns
        -------
        Dict
        """
        warnings.warn(
            "This usage is deprecated and will be removed in a future release. "
            "Please use 'field_data.scalar_fields()' instead",
            PyFluentDeprecationWarning,
        )
        return self._get_scalar_fields_info()

    def _get_scalar_fields_info(self):
        phases = self._file_session._data_file.get_phases()

        scalar_field_info = {}

        if len(phases) > 1:
            for phase in phases:
                for face_variable in self._file_session._data_file.get_face_variables(
                    phase
                ):
                    if face_variable:
                        scalar_field_info[phase + ":" + face_variable] = {
                            "display_name": face_variable,
                            "section": "field-data",
                            "domain": phase,
                        }
        else:
            for face_variable in self._file_session._data_file.get_face_variables(
                phases[0]
            ):
                if face_variable:
                    scalar_field_info[face_variable] = {
                        "display_name": face_variable,
                        "section": "field-data",
                        "domain": phases[0],
                    }

        return scalar_field_info

    def get_vector_fields_info(self):
        """Get vector fields information (vector components).

        Returns
        -------
        Dict
        """
        warnings.warn(
            "This usage is deprecated and will be removed in a future release. "
            "Please use 'field_data.vector_fields()' instead",
            PyFluentDeprecationWarning,
        )
        return self._get_vector_fields_info()

    def _get_vector_fields_info(self):
        phases = self._file_session._data_file.get_phases()

        if len(phases) > 1:
            return {
                phase
                + ":"
                + "velocity": {
                    "x-component": f"{phase}: SV_U",
                    "y-component": f"{phase}: SV_V",
                    "z-component": f"{phase}: SV_W",
                }
                for phase in phases
            }
        else:
            return {
                "velocity": {
                    "x-component": "SV_U",
                    "y-component": "SV_V",
                    "z-component": "SV_W",
                }
            }

    def get_surfaces_info(self):
        """Get surfaces information (surface name, ID, and type).

        Returns
        -------
        Dict
        """
        warnings.warn(
            "This usage is deprecated and will be removed in a future release. "
            "Please use 'field_data.surfaces()' instead",
            PyFluentDeprecationWarning,
        )
        return self._get_surfaces_info()

    def _get_surfaces_info(self):
        mesh = self._file_session._case_file.get_mesh()
        surface_names = mesh.get_surface_names()
        surface_ids = mesh.get_surface_ids()
        info = {
            name: {
                "surface_id": [surface_id],
                "zone_id": -1,
                "zone_type": "wall",
                "type": "plane",
            }
            for name, surface_id in zip(surface_names, surface_ids)
        }
        return info


class FileFieldInfo(_FileFieldInfo):
    """File field info."""

    def __init__(self, file_session):
        """Initialize FileFieldInfo"""
        warnings.warn(
            "'FieldInfo' is deprecated and will be removed in a future release. "
            "Please use relevant methods from 'FieldData' instead",
            PyFluentDeprecationWarning,
        )
        super().__init__(file_session)


class FileSession:
    """File session to read case and data file."""

    def __init__(self, case_file_name=None, data_file_name=None):
        """__init__ method of FileSession class."""
        self._case_file = CaseFile(case_file_name) if case_file_name else None
        self._data_file = (
            DataFile(data_file_name, case_file_handle=self._case_file)
            if case_file_name and data_file_name
            else None
        )

        self.monitors = None
        self.session_id = 1
        self.fields = Fields(self)

    def read_case(self, case_file_name):
        """Read Case file."""
        if self._case_file:
            warnings.warn("Case already read during initialization. Over-writing...")
        self._case_file = CaseFile(case_file_name)

    def read_data(self, data_file_name):
        """Read Data file."""
        if self._data_file:
            warnings.warn("Data already read during initialization. Over-writing...")
        self._data_file = DataFile(data_file_name, case_file_handle=self._case_file)

    @property
    def field_info(self):
        """Provides access to Fluent field information."""
        warnings.warn(
            "field_info is deprecated. Use fields.field_info instead.",
            PyFluentDeprecationWarning,
        )
        return self.fields.field_info

    @property
    def field_data(self):
        """Fluent field data on surfaces."""
        warnings.warn(
            "field_data is deprecated. Use fields.field_data instead.",
            PyFluentDeprecationWarning,
        )
        return self.fields.field_data


def _get_surface_ids(
    field_info: FileFieldInfo,
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
            surface_ids.extend(field_info._get_surfaces_info()[surf]["surface_id"])
        else:
            surface_ids.append(surf)
    return surface_ids


class Fields:
    """Container for field and solution variables."""

    def __init__(self, _session: FileSession):
        """Initialize Fields."""
        self.field_info = _FileFieldInfo(_session)
        self.field_data = FileFieldData(_session, self.field_info)
