# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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

"""Wrappers over FieldData gRPC service of Fluent."""

from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from enum import Enum
import logging
import time
import warnings
import weakref

import numpy as np

from ansys.api.fluent.v0 import field_data_pb2 as FieldDataProtoModule
from ansys.fluent.core.exceptions import DisallowedValuesError
from ansys.fluent.core.field_data_interfaces import (
    BaseFieldDataSource,
    BaseFieldInfo,
    FieldBatch,
    FieldDataSource,
    PathlinesFieldDataRequest,
    ScalarFieldDataRequest,
    SurfaceDataType,
    SurfaceFieldDataRequest,
    VectorFieldDataRequest,
    _AllowedScalarFieldNames,
    _AllowedSurfaceIDs,
    _AllowedSurfaceNames,
    _AllowedVectorFieldNames,
    _ReturnFieldData,
    _ScalarFields,
    _SurfaceIds,
    _SurfaceNames,
    _to_field_name_str,
    _VectorFields,
    get_surfaces_from_objects,
)
from ansys.fluent.core.pyfluent_warnings import PyFluentDeprecationWarning
from ansys.fluent.core.utils.deprecate import (
    deprecate_function,
)

logger = logging.getLogger("pyfluent.field_data")


def override_help_text(func, func_to_be_wrapped):
    """Override function help text."""
    if func_to_be_wrapped.__doc__:
        func.__doc__ = "\n" + func_to_be_wrapped.__doc__
    func.__name__ = func_to_be_wrapped.__qualname__
    return func


class _FieldInfo(BaseFieldInfo):
    def __init__(
        self,
        field_data,
    ):
        """__init__ method of FieldInfo class."""
        self._field_data = field_data

    def _get_scalar_field_range(
        self, field: str, node_value: bool = False, surface_ids: list[int] | None = None
    ) -> list[float]:
        return self._field_data.get_scalar_field_range(field, node_value, surface_ids)

    def _get_scalar_fields_info(self) -> dict[str, dict]:
        return self._field_data.get_scalar_fields_info()

    def _get_vector_fields_info(self) -> dict[str, dict]:
        return self._field_data.get_vector_fields_info()

    def _get_surfaces_info(self) -> dict[str, dict]:
        return self._field_data.get_surfaces_info()


class _FetchFieldData:
    @staticmethod
    def _surface_data(
        data_types: list[SurfaceDataType] | list[str],
        surface_ids: list[int],
        overset_mesh: bool | None = False,
    ):
        return [
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

    @staticmethod
    def _scalar_data(
        field_name: str,
        surface_ids: list[int],
        node_value: bool,
        boundary_value: bool,
    ):
        return [
            FieldDataProtoModule.ScalarFieldRequest(
                surfaceId=surface_id,
                scalarFieldName=field_name,
                dataLocation=(
                    FieldDataProtoModule.DataLocation.Nodes
                    if node_value
                    else FieldDataProtoModule.DataLocation.Elements
                ),
                provideBoundaryValues=boundary_value,
            )
            for surface_id in surface_ids
        ]

    @staticmethod
    def _vector_data(
        field_name: str,
        surface_ids: list[int],
    ):
        return [
            FieldDataProtoModule.VectorFieldRequest(
                surfaceId=surface_id, vectorFieldName=field_name
            )
            for surface_id in surface_ids
        ]

    @staticmethod
    def _pathlines_data(
        field_name: str,
        surface_ids: list[int],
        **kwargs,
    ):
        return [
            FieldDataProtoModule.PathlinesFieldRequest(
                surfaceId=surface_id,
                field=field_name,
                **kwargs,
            )
            for surface_id in surface_ids
        ]


class BaseFieldData:
    """The base field data interface."""

    def __init__(
        self,
        data: dict,
        field_info,
        allowed_surface_names,
        allowed_scalar_field_names,
    ):
        """__init__ method of BaseFieldData class."""
        self.data = data
        self._field_info = field_info
        self._allowed_surface_names = allowed_surface_names
        self._allowed_scalar_field_names = allowed_scalar_field_names
        self._returned_data = _ReturnFieldData()
        self._deprecated_flag = False

    def get_surface_ids(self, surfaces: list[str | int]) -> list[int]:
        """Get a list of surface ids based on surfaces provided as inputs."""
        return _get_surface_ids(
            field_info=self._field_info,
            allowed_surface_names=self._allowed_surface_names,
            surfaces=surfaces,
        )

    def _get_scalar_field_data(
        self,
        **kwargs,
    ) -> dict[int | str, np.ndarray]:
        scalar_field_data = self.data[
            (
                ("type", "scalar-field"),
                ("dataLocation", 1 if kwargs.get("node_value") else 0),
                ("boundaryValues", kwargs.get("boundary_value")),
            )
        ]
        return self._returned_data._scalar_data(
            _to_field_name_str(kwargs.get("field_name")),
            kwargs.get("surfaces"),
            self.get_surface_ids(kwargs.get("surfaces")),
            scalar_field_data,
        )

    def _get_surface_data(
        self,
        **kwargs,
    ) -> dict[int | str, dict[SurfaceDataType, np.ndarray | list[np.ndarray]]]:
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
    ) -> dict[int | str, np.ndarray]:
        vector_field_data = self.data[(("type", "vector-field"),)]
        return self._returned_data._vector_data(
            _to_field_name_str(kwargs.get("field_name")),
            kwargs.get("surfaces"),
            self.get_surface_ids(kwargs.get("surfaces")),
            vector_field_data,
        )

    def _get_pathlines_field_data(
        self,
        **kwargs,
    ) -> dict:
        field_name = _to_field_name_str(kwargs.get("field_name"))
        pathlines_data = self.data[(("type", "pathlines-field"), ("field", field_name))]
        return self._returned_data._pathlines_data(
            field_name,
            kwargs.get("surfaces"),
            self.get_surface_ids(kwargs.get("surfaces")),
            pathlines_data,
            flatten_connectivity=kwargs.get("flatten_connectivity"),
        )

    def get_field_data(
        self,
        obj: (
            SurfaceFieldDataRequest
            | ScalarFieldDataRequest
            | VectorFieldDataRequest
            | PathlinesFieldDataRequest
        ),
    ) -> dict[int | str, dict | np.ndarray]:
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


class BatchFieldData(BaseFieldData, BaseFieldDataSource):
    """Provides access to Fluent field data on surfaces collected via batches."""

    def __init__(
        self,
        data: dict,
        field_info,
        allowed_surface_names,
        allowed_scalar_field_names,
    ):
        """__init__ method of BatchFieldData class."""
        super().__init__(
            data, field_info, allowed_surface_names, allowed_scalar_field_names
        )

    def __len__(self):
        return len(self.data)

    def __call__(self):
        return self.data


class TransactionFieldData(BatchFieldData):
    """TransactionFieldData class - deprecated."""

    def __init__(self, *args, **kwargs):
        warnings.warn(
            "'TransactionFieldData' is deprecated, use 'BatchFieldData' instead.",
            PyFluentDeprecationWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)


class Batch(FieldBatch):
    """Populates Fluent field data on surfaces."""

    def __init__(
        self,
        field_data,
        field_info,
        allowed_surface_ids,
        allowed_surface_names,
        allowed_scalar_field_names,
        allowed_vector_field_names,
    ):
        """__init__ method of Batch class."""
        self._field_data = field_data
        self._field_info = field_info

        self._allowed_surface_names = allowed_surface_names
        self._allowed_scalar_field_names = allowed_scalar_field_names
        self._allowed_vector_field_names = allowed_vector_field_names

        self._fetched_data = _FetchFieldData()
        self._pathline_field_data = []
        self._cache_requests = []

    def get_surface_ids(self, surfaces: list[str | int]) -> list[int]:
        """Get a list of surface ids based on surfaces provided as inputs."""
        return _get_surface_ids(
            field_info=self._field_info,
            allowed_surface_names=self._allowed_surface_names,
            surfaces=surfaces,
        )

    def _add_surfaces_request(self, **kwargs) -> None:
        updated_data_types = []
        for d_type in kwargs.get("data_types"):
            if isinstance(d_type, str):
                updated_data_types.append(SurfaceDataType(d_type))
            else:
                updated_data_types.append(d_type)
        data_types = updated_data_types
        self._field_data._add_surfaces_request(
            data_types=data_types,
            surfaces=kwargs.get("surfaces"),
            overset_mesh=kwargs.get("overset_mesh"),
        )

    def _add_scalar_fields_request(self, **kwargs) -> None:
        self._field_data._add_scalar_fields_request(
            self._allowed_scalar_field_names.valid_name(kwargs.get("field_name")),
            surfaces=kwargs.get("surfaces"),
            node_value=kwargs.get("node_value"),
            boundary_value=kwargs.get("boundary_value"),
        )

    def _add_vector_fields_request(self, **kwargs) -> None:
        self._field_data._add_vector_fields_request(
            self._allowed_vector_field_names.valid_name(kwargs.get("field_name")),
            surfaces=kwargs.get("surfaces"),
        )

    def _add_pathlines_fields_request(
        self,
        **kwargs,
    ) -> None:
        zones = kwargs.get("zones", [])
        field_name = self._allowed_scalar_field_names.valid_name(
            kwargs.get("field_name")
        )
        if field_name in self._pathline_field_data:
            raise ValueError("For 'path-lines' `field_name` should be unique.")
        else:
            self._pathline_field_data.append(field_name)
        additional_field_name = kwargs.get("additional_field_name")
        if additional_field_name:
            additional_field_name = self._allowed_scalar_field_names.valid_name(
                additional_field_name
            )
        self._field_data._add_pathlines_fields_request(
            field_name,
            kwargs.get("surfaces"),
            additional_field_name=additional_field_name,
            provide_particle_time_field=kwargs.get("provide_particle_time_field"),
            node_value=kwargs.get("node_value"),
            steps=kwargs.get("steps"),
            step_size=kwargs.get("step_size"),
            skip=kwargs.get("skip"),
            reverse=kwargs.get("reverse"),
            accuracy_control_on=kwargs.get("accuracy_control_on"),
            tolerance=kwargs.get("tolerance"),
            coarsen=kwargs.get("coarsen"),
            velocity_domain=kwargs.get("velocity_domain"),
            zones=zones,
        )

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
        """
        Add field data requests for surfaces, scalars, vectors, or pathlines.

        This method allows users to specify multiple field data requests, which will
        later be processed when retrieving responses.
        """
        for req in (obj,) + args:
            req = req._replace(surfaces=self.get_surface_ids(req.surfaces))
            if req in self._cache_requests:
                warnings.warn(f"{req._asdict()} is duplicate and being ignored.")
                continue
            elif isinstance(req, SurfaceFieldDataRequest):
                self._add_surfaces_request(
                    data_types=req.data_types,
                    surfaces=req.surfaces,
                    overset_mesh=req.overset_mesh,
                )
            elif isinstance(req, ScalarFieldDataRequest):
                self._add_scalar_fields_request(
                    field_name=req.field_name,
                    surfaces=req.surfaces,
                    node_value=req.node_value,
                    boundary_value=req.boundary_value,
                )
            elif isinstance(req, VectorFieldDataRequest):
                self._add_vector_fields_request(
                    field_name=req.field_name,
                    surfaces=req.surfaces,
                )
            elif isinstance(req, PathlinesFieldDataRequest):
                self._add_pathlines_fields_request(
                    field_name=req.field_name,
                    surfaces=req.surfaces,
                    additional_field_name=req.additional_field_name,
                    provide_particle_time_field=req.provide_particle_time_field,
                    node_value=req.node_value,
                    steps=req.steps,
                    step_size=req.step_size,
                    skip=req.skip,
                    reverse=req.reverse,
                    accuracy_control_on=req.accuracy_control_on,
                    tolerance=req.tolerance,
                    coarsen=req.coarsen,
                    velocity_domain=req.velocity_domain,
                    zones=req.zones,
                )
            self._cache_requests.append(req)
        return self

    def get_response(self) -> BatchFieldData:
        """Get data for previously added requests.

        Returns
        -------
        Dict[int, Dict[int, Dict[str, npt.NDArray[Any]]]]
            Data is returned as dictionary of dictionaries in the following structure:
            tag int | Tuple-> surface_id [int] -> field_name [str] -> field_data[np.array]

            The tag is a tuple.
        """
        return BatchFieldData(
            self._field_data.extract_fields(self._field_data.get_batched_fields()),
            self._field_info,
            self._allowed_surface_names,
            self._allowed_scalar_field_names,
        )

    def __call__(self):
        self.get_response()


class Transaction(Batch):
    """Transaction class - deprecated."""

    def __init__(self, *args, **kwargs):
        warnings.warn(
            "'Transaction' is deprecated, use 'Batch' instead.",
            PyFluentDeprecationWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)


def _get_surface_ids(
    field_info: _FieldInfo,
    allowed_surface_names,
    surfaces: list[int | str | object],
) -> list[int]:
    """Get surface IDs based on surface names or IDs.

    Parameters
    ----------
    surfaces : List[int] | List[str]
        List of surface IDs or surface names.

    Returns
    -------
    List[int]
    """
    surface_ids = []
    updated_surfaces = get_surfaces_from_objects(surfaces)
    for surf in updated_surfaces:
        if isinstance(surf, str):
            surface_ids.extend(
                field_info._get_surfaces_info()[allowed_surface_names.valid_name(surf)][
                    "surface_id"
                ]
            )
        else:
            allowed_surf_ids = _AllowedSurfaceIDs(field_info)()
            if surf in allowed_surf_ids:
                surface_ids.append(surf)
            elif isinstance(surf, Iterable) and not isinstance(surf, (str, bytes)):
                raise DisallowedValuesError("surface", surf, list(surf))
            else:
                raise DisallowedValuesError("surface", surf, allowed_surf_ids)
    return surface_ids


# Root domain id in Fluent.
ROOT_DOMAIN_ID = 1


class ZoneType(Enum):
    """Zone types for mesh."""

    CELL = 1
    FACE = 2


@dataclass
class ZoneInfo:
    """Zone information for mesh.

    Attributes
    ----------
    _id : int
        Zone ID.
    name : str
        Name of the zone.
    zone_type : ZoneType
        Type of the zone for mesh.
    """

    _id: int
    name: str
    zone_type: ZoneType


@dataclass
class Node:
    """Node class for mesh.

    Attributes
    ----------
    x : float
        x-coordinate of the node.
    y : float
        y-coordinate of the node.
    z : float
        z-coordinate of the node.
    """

    _id: int
    x: float
    y: float
    z: float


class CellElementType(Enum):
    """Element types for a cell element."""

    # 3 nodes, 3 faces
    TRIANGLE = 1
    # 4 nodes, 4 faces
    TETRAHEDRON = 2
    # 4 nodes, 4 faces
    QUADRILATERAL = 3
    # 8 nodes, 6 faces
    HEXAHEDRON = 4
    # 5 nodes, 5 faces
    PYRAMID = 5
    # 6 nodes, 5 faces
    WEDGE = 6
    # Arbitrary number of nodes and faces
    POLYHEDRON = 7
    # 2 nodes, 1 face (only in 2D)
    GHOST = 8
    # 10 nodes, 4 faces
    QUADRATIC_TETRAHEDRON = 9
    # 20 nodes, 6 faces
    QUADRATIC_HEXAHEDRON = 10
    # 13 nodes, 5 faces
    QUADRATIC_PYRAMID = 11
    # 15 nodes, 5 faces
    QUADRATIC_WEDGE = 12


@dataclass
class Facet:
    """Facet class within a mesh element.

    Attributes
    ----------
    node_indices : list[int]
        0-based node indices of the facet.
    """

    node_indices: list[int]


@dataclass
class Element:
    """Element class for mesh.

    Attributes
    ----------
    element_type : CellElementType
        Element type of the element.
    node_indices : list[int]
        0-based node indices of the element. Populated for standard elements.
    facets : list[Facet]
        List of facets of the element. Populated for polyhedral elements.
    """

    _id: int
    element_type: CellElementType
    node_indices: list[int] = field(default_factory=list)
    facets: list[Facet] = field(default_factory=list)


@dataclass
class Mesh:
    """Mesh class for Fluent field data.

    Attributes
    ----------
    nodes : list[Node]
        List of nodes in the mesh.
    elements : list[Element]
        List of elements in the mesh.
    """

    nodes: list[Node]
    elements: list[Element]


class LiveFieldData(BaseFieldData, FieldDataSource):
    """Provides access to Fluent field data on surfaces."""

    def __init__(
        self,
        field_data,
        field_info,
        scheme_interpreter,
        get_zones_info: weakref.WeakMethod[Callable[[], list[ZoneInfo]]] | None = None,
    ):
        """__init__ method of FieldData class."""
        self._field_data = field_data
        self._field_info = field_info
        self.is_data_valid = field_data.is_data_valid
        self.scheme = scheme_interpreter

        self.get_zones_info = lambda: get_zones_info()()

        self._allowed_surface_names = _AllowedSurfaceNames(field_info)

        self._allowed_surface_ids = _AllowedSurfaceIDs(field_info)

        self._allowed_scalar_field_names = _AllowedScalarFieldNames(
            self.is_data_valid, field_info
        )

        self._allowed_vector_field_names = _AllowedVectorFieldNames(
            self.is_data_valid, field_info
        )
        super().__init__(
            {},
            self._field_info,
            self._allowed_surface_names,
            self._allowed_scalar_field_names,
        )
        self.surfaces = _SurfaceNames(allowed_surface_names=self._allowed_surface_names)
        self.surface_ids = _SurfaceIds(allowed_surface_ids=self._allowed_surface_ids)
        self.scalar_fields = _ScalarFields(
            available_field_names=self._allowed_scalar_field_names,
            field_info=self._field_info,
        )
        self.vector_fields = _VectorFields(
            available_field_names=self._allowed_vector_field_names
        )
        self._returned_data = _ReturnFieldData()

    def new_batch(self):
        """Create a new field batch."""
        return Batch(
            self._field_data,
            self._field_info,
            self._allowed_surface_ids,
            self._allowed_surface_names,
            self._allowed_scalar_field_names,
            self._allowed_vector_field_names,
        )

    @deprecate_function(version="v0.34.0", new_func="new_batch")
    def new_transaction(self):
        """Create a new field transaction."""
        return self.new_batch()

    def _get_scalar_field_data(self, **kwargs):
        surfaces = kwargs.get("surfaces")
        surface_ids = self.get_surface_ids(surfaces)
        field_name = self._allowed_scalar_field_names.valid_name(
            kwargs.get("field_name")
        )
        fields = self._field_data.extract_fields(
            self._field_data._get_scalar_field_data(
                field_name,
                surface_ids,
                kwargs.get("node_value"),
                kwargs.get("boundary_value"),
            )
        )
        scalar_field_data = next(iter(fields.values()))
        return self._returned_data._scalar_data(
            field_name, surfaces, surface_ids, scalar_field_data
        )

    def _get_surface_data(
        self,
        **kwargs,
    ) -> dict[int | str, dict[SurfaceDataType, np.ndarray | list[np.ndarray]]]:
        surface_ids = self.get_surface_ids(kwargs.get("surfaces"))
        fields = self._field_data.extract_fields(
            self._field_data._get_surface_data(
                kwargs.get("data_types"), surface_ids, kwargs.get("overset_mesh")
            )
        )
        surface_data = next(iter(fields.values()))
        if self._deprecated_flag:
            self._deprecated_flag = False
            return self._returned_data._surface_data(
                kwargs.get("data_types"),
                kwargs.get("surfaces"),
                surface_ids,
                surface_data,
                deprecated_flag=True,
                flatten_connectivity=kwargs.get("flatten_connectivity"),
            )

        return self._returned_data._surface_data(
            kwargs.get("data_types"),
            kwargs.get("surfaces"),
            surface_ids,
            surface_data,
            flatten_connectivity=kwargs.get("flatten_connectivity"),
        )

    def _get_vector_field_data(
        self,
        **kwargs,
    ) -> dict[int | str, np.ndarray]:
        surface_ids = self.get_surface_ids(kwargs.get("surfaces"))
        field_name = self._allowed_vector_field_names.valid_name(
            kwargs.get("field_name")
        )
        for surface_id in surface_ids:
            self.scheme.string_eval(f"(surface? {surface_id})")
        fields = self._field_data.extract_fields(
            self._field_data._get_vector_field_data(field_name, surface_ids)
        )
        vector_field_data = next(iter(fields.values()))

        return self._returned_data._vector_data(
            field_name,
            kwargs.get("surfaces"),
            surface_ids,
            vector_field_data,
        )

    def _get_pathlines_field_data(
        self,
        **kwargs,
    ) -> dict:
        zones = kwargs.get("zones", [])
        surface_ids = self.get_surface_ids(kwargs.get("surfaces"))
        field_name = self._allowed_scalar_field_names.valid_name(
            kwargs.get("field_name")
        )
        additional_field_name = kwargs.get("additional_field_name")
        if additional_field_name:
            additional_field_name = self._allowed_scalar_field_names.valid_name(
                additional_field_name
            )
        fields = self._field_data.extract_fields(
            self._field_data._get_pathlines_field_data(
                field_name=field_name,
                surfaces=surface_ids,
                additional_field_name=additional_field_name,
                provide_particle_time_field=kwargs.get("provide_particle_time_field"),
                node_value=kwargs.get("node_value"),
                steps=kwargs.get("steps"),
                step_size=kwargs.get("step_size"),
                skip=kwargs.get("skip"),
                reverse=kwargs.get("reverse"),
                accuracy_control_on=kwargs.get("accuracy_control_on"),
                tolerance=kwargs.get("tolerance"),
                coarsen=kwargs.get("coarsen"),
                velocity_domain=kwargs.get("velocity_domain"),
                zones=zones,
            )
        )
        pathlines_data = next(iter(fields.values()))

        if self._deprecated_flag:
            self._deprecated_flag = False
            return self._returned_data._pathlines_data(
                field_name,
                kwargs.get("surfaces"),
                surface_ids,
                pathlines_data,
                deprecated_flag=True,
                flatten_connectivity=kwargs.get("flatten_connectivity"),
            )

        return self._returned_data._pathlines_data(
            field_name,
            kwargs.get("surfaces"),
            surface_ids,
            pathlines_data,
            flatten_connectivity=kwargs.get("flatten_connectivity"),
        )

    def get_mesh(self, zone: str | int) -> Mesh:
        """Get mesh for a zone.

        Parameters
        ----------
        zone : str | int
            Zone name or id. Currently, only cell zones are supported.

        Returns
        -------
        Mesh
            Mesh object containing nodes and elements.

        Raises
        ------
        ValueError
            If the zone is not found.
        NotImplementedError
            If a face zone is provided.
        """
        zone_info = None
        for zone_info in self.get_zones_info():
            if zone_info.name == zone or zone_info._id == zone:
                break
        if zone_info is None:
            raise ValueError(f"Zone {zone} not found.")
        if zone_info.zone_type == ZoneType.FACE:
            raise NotImplementedError("Face zone mesh is not supported.")

        # Mesh data is retrieved from the root domain in Fluent
        logger.info(f"Getting nodes data for zone {zone_info._id}")
        start_time = time.time()
        # TODO: Add precision query in AppUtilities service
        is_double_precision = self.scheme.eval("(rp-double?)")
        if is_double_precision:
            nested_nodes = self._field_data.get_solver_mesh_nodes_double(
                domain_id=ROOT_DOMAIN_ID, thread_id=zone_info._id
            )
        else:
            nested_nodes = self._field_data.get_solver_mesh_nodes_float(
                domain_id=ROOT_DOMAIN_ID, thread_id=zone_info._id
            )
        logger.info(f"Nodes data received in {time.time() - start_time} seconds")
        logger.info(f"Getting elements for zone {zone_info._id}")
        start_time = time.time()
        elementss_pb = self._field_data.get_solver_mesh_elements(
            domain_id=ROOT_DOMAIN_ID, thread_id=zone_info._id
        )
        logger.info(f"Elements data received in {time.time() - start_time} seconds")
        logger.info("Constructing nodes structure in PyFluent")
        start_time = time.time()
        node_count = sum(len(nodes) for nodes in nested_nodes)
        nodes = np.empty(node_count, dtype=Node)
        node_index_by_id = {}
        i = 0
        for nodes_pb in nested_nodes:
            for node_pb in nodes_pb:
                nodes[i] = Node(_id=node_pb.id, x=node_pb.x, y=node_pb.y, z=node_pb.z)
                node_index_by_id[node_pb.id] = i
                i += 1
        logger.info(
            f"Nodes structure constructed in {time.time() - start_time} seconds"
        )
        logger.info("Constructing elements structure in PyFluent")
        start_time = time.time()
        element_count = sum(len(elements) for elements in elementss_pb)
        elements = np.empty(element_count, dtype=Element)
        i = 0
        for elements_pb in elementss_pb:
            for element_pb in elements_pb:
                element_type = CellElementType(element_pb.element_type)
                if element_type == CellElementType.POLYHEDRON:
                    facets = []
                    for facet_pb in element_pb.facets:
                        facet = Facet(
                            node_indices=[
                                node_index_by_id[id]
                                for id in getattr(
                                    facet_pb,
                                    "nodes",
                                    getattr(facet_pb, "node", []),
                                )
                            ]
                        )
                        facets.append(facet)
                    element = Element(
                        _id=element_pb.id,
                        element_type=element_type,
                        facets=facets,
                    )
                else:
                    element = Element(
                        _id=element_pb.id,
                        element_type=element_type,
                        node_indices=[
                            node_index_by_id[id] for id in element_pb.node_ids
                        ],
                    )
                elements[i] = element
                i += 1
        logger.info(
            f"Elements structure constructed in {time.time() - start_time} seconds"
        )
        logger.info("Returning mesh")
        return Mesh(nodes=nodes, elements=elements)
