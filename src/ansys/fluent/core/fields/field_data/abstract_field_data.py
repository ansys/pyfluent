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

"""Transport contracts and request models for Fluent field data.

This module defines the service-layer boundary. A transport adapter for any
kind of service, such as gRPC or REST, implements :class:`AbstractFieldData`
and is responsible for making service calls and returning transport results. It
does not provide the user-facing convenience API or batching behavior.

:class:`FieldDataSource` is the contract for a user-facing source built on top
of an :class:`AbstractFieldData` implementation. :class:`FieldBatch` is the
corresponding contract for a batch request object.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
import dataclasses
from enum import Enum
from typing import Any, Iterable
import warnings

import numpy as np
import numpy.typing as npt

from ansys.fluent.core.fields.field_data._field_data_interfaces import (
    _get_surfaces_from_objects,
    _set_dataclass_field_docs,
    _transform_faces_connectivity_data,
    _validate_scalar_variable_descriptor,
    _validate_vector_variable_descriptor,
)
from ansys.units.variable_descriptor import (
    ScalarVariableDescriptor,
    VectorVariableDescriptor,
)

__all__ = (
    "AbstractFieldData",
    "BaseDataRequest",
    "BaseFieldDataSource",
    "FieldBatch",
    "FieldDataSource",
    "PathlinesFieldDataRequest",
    "ScalarFieldDataRequest",
    "SurfaceDataType",
    "SurfaceFieldDataRequest",
    "VectorFieldDataRequest",
)


class SurfaceDataType(Enum):
    """Provides surface data types."""

    Vertices = "vertices"
    FacesConnectivity = "faces"
    FacesNormal = "face-normal"
    FacesCentroid = "centroid"


@dataclasses.dataclass(frozen=True)
class BaseDataRequest:
    """Abstract base container for data requests sharing common fields and methods."""

    surfaces: list[int | str | object]

    def _asdict(self) -> dict:
        """Serialize dataclass fields dynamically."""
        return {field: getattr(self, field) for field in self.__dataclass_fields__}

    def _replace(self, **changes) -> "BaseDataRequest":
        """Replicate NamedTuple._replace behavior for frozen dataclasses."""
        return dataclasses.replace(self, **changes)

    def __post_init__(self):
        """Validate shared attributes."""
        if not isinstance(self.surfaces, Iterable) or isinstance(
            self.surfaces, (str, bytes)
        ):
            raise TypeError("surfaces must be iterable.")
        self._validate_inputs()

    def _validate_inputs(self) -> None:
        """Hook method for subclasses to implement specific input validations."""
        pass


@dataclasses.dataclass(frozen=True)
class SurfaceFieldDataRequest(BaseDataRequest):
    """Container storing parameters for surface data request."""

    data_types: list[SurfaceDataType] | list[str]
    overset_mesh: bool | None = False
    flatten_connectivity: bool = False

    def _validate_inputs(self) -> None:
        if not isinstance(self.data_types, Iterable) or isinstance(
            self.data_types, (str, bytes)
        ):
            raise TypeError("`data_types` must be iterable.")


@dataclasses.dataclass(frozen=True)
class ScalarFieldDataRequest(BaseDataRequest):
    """Container storing parameters for scalar field data request."""

    field_name: str | "ScalarVariableDescriptor"
    node_value: bool | None = True
    boundary_value: bool | None = True

    def _validate_inputs(self) -> None:
        if not isinstance(self.field_name, (str)):
            _validate_scalar_variable_descriptor(self.field_name)


@dataclasses.dataclass(frozen=True)
class VectorFieldDataRequest(BaseDataRequest):
    """Container storing parameters for vector field data request."""

    field_name: str | "VectorVariableDescriptor"

    def _validate_inputs(self) -> None:
        if not isinstance(self.field_name, (str)):
            _validate_vector_variable_descriptor(self.field_name)


@dataclasses.dataclass(frozen=True)
class PathlinesFieldDataRequest(BaseDataRequest):
    """Container storing parameters for path-lines field data request."""

    field_name: str | "ScalarVariableDescriptor"
    additional_field_name: str = ""
    provide_particle_time_field: bool | None = False
    node_value: bool | None = True
    steps: int | None = 500
    step_size: float | None = 500
    skip: int | None = 0
    reverse: bool | None = False
    accuracy_control_on: bool | None = False
    tolerance: float | None = 0.001
    coarsen: int | None = 1
    velocity_domain: str | None = "all-phases"
    zones: list | None = None
    flatten_connectivity: bool = False

    def _validate_inputs(self) -> None:
        if not isinstance(self.field_name, (str)):
            _validate_scalar_variable_descriptor(self.field_name)


class ZoneType(Enum):
    """Enumeration of zone types that classify mesh zones in the Fluent solver."""

    CELL = 1
    FACE = 2


@dataclasses.dataclass
class ZoneInfo:
    """Metadata describing a mesh zone in the Fluent solver.

    Attributes
    ----------
    _id : int
        Integer zone ID assigned by the Fluent solver.
    name : str
        Name of the zone as defined in the Fluent case.
    zone_type : ZoneType
        Whether the zone is a cell zone or a face zone.
    """

    _id: int
    name: str
    zone_type: ZoneType


@dataclasses.dataclass
class Node:
    """A single mesh node with its spatial coordinates.

    Attributes
    ----------
    _id : int
        Integer node ID assigned by the Fluent solver.
    x : float
        X-coordinate of the node in the solver's length unit.
    y : float
        Y-coordinate of the node in the solver's length unit.
    z : float
        Z-coordinate of the node in the solver's length unit.
    """

    _id: int
    x: float
    y: float
    z: float


class CellElementType(Enum):
    """Enumeration of cell element topologies supported by the Fluent mesh.

    Each member corresponds to a standard finite-volume cell shape. The number of
    nodes and faces for each type is noted in the member comments.
    """

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


@dataclasses.dataclass
class Facet:
    """A face of a polyhedral mesh element, defined by its node indices.

    Used only for :attr:`CellElementType.POLYHEDRON` elements; standard
    element types store connectivity directly on :class:`Element` via
    ``node_indices``.

    Attributes
    ----------
    node_indices : list[int]
        Zero-based indices into the :attr:`Mesh.nodes` array for the nodes
        that form this facet.
    """

    node_indices: list[int]


@dataclasses.dataclass
class Element:
    """A single mesh cell containing topology and connectivity information.

    For standard element types (e.g. hexahedron, tetrahedron), connectivity is
    stored in ``node_indices``. For polyhedral elements, connectivity is stored
    as a list of :class:`Facet` objects in ``facets``.

    Attributes
    ----------
    _id : int
        Integer element ID assigned by the Fluent solver.
    element_type : CellElementType
        Shape of the element; see :class:`CellElementType`.
    node_indices : list[int]
        Zero-based indices into :attr:`Mesh.nodes` for standard elements.
        Empty for polyhedral elements.
    facets : list[Facet]
        Faces of the element for :attr:`CellElementType.POLYHEDRON` elements.
        Empty for standard elements.
    """

    _id: int
    element_type: CellElementType
    node_indices: list[int] = dataclasses.field(default_factory=list)
    facets: list[Facet] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class Mesh:
    """Computational mesh for a Fluent zone, containing nodes and elements.

    Returned by :meth:`LiveFieldData.get_mesh`. The ``nodes`` array provides
    spatial coordinates indexed from 0, and the ``elements`` array stores
    connectivity referencing those node indices.

    Attributes
    ----------
    nodes : list[Node]
        Ordered list of :class:`Node` objects; element connectivity uses
        zero-based indices into this list.
    elements : list[Element]
        List of :class:`Element` objects describing cell topology and
        connectivity.
    """

    nodes: list[Node]
    elements: list[Element]


class BaseFieldDataSource(ABC):
    """Abstract contract for a user-facing field-data source.

    This contract belongs to the wrapper layer, not to a transport service. It
    describes how callers resolve surfaces and retrieve data after a transport
    specific :class:`AbstractFieldData` implementation has been connected.

    :class:`~ansys.fluent.core.fields.live_field_data.LiveFieldData` is the
    standard implementation.
    """

    @abstractmethod
    def get_surface_ids(self, surfaces: list[str | int | object]) -> list[int]:
        """Retrieve a list of surface IDs based on input surface names or numerical identifiers."""
        pass

    @abstractmethod
    def get_field_data(
        self,
        obj: (
            SurfaceFieldDataRequest
            | ScalarFieldDataRequest
            | VectorFieldDataRequest
            | PathlinesFieldDataRequest
        ),
    ) -> "dict[int | str, SurfaceData | PathlinesData | np.ndarray]":
        """
        Retrieve the field data for a given request.

        This method processes the specified request and returns the corresponding
        field data in a structured format.

        Returns
        -------
            Dict[int | str, SurfaceData | PathlinesData | np.ndarray]: A dictionary where keys represent surface
            IDs or names, and values contain the corresponding field data.
        """
        pass


class FieldDataSource(BaseFieldDataSource, ABC):
    """Abstract contract for a field-data source that supports batching.

    This extends :class:`BaseFieldDataSource` with the factory method needed to
    create a :class:`FieldBatch`. The concrete source uses that batch to collect
    requests and return a batched response.

    :class:`~ansys.fluent.core.fields.live_field_data.LiveFieldData` fulfills
    this contract and returns a
    :class:`~ansys.fluent.core.fields.live_field_data.Batch` from
    :meth:`~ansys.fluent.core.fields.live_field_data.LiveFieldData.new_batch`.
    """

    @abstractmethod
    def new_batch(self) -> FieldBatch:
        """Create a new field batch."""
        pass


class FieldBatch(ABC):
    """Abstract contract for collecting and executing field-data requests.

    A batch belongs to a :class:`FieldDataSource`. It accepts request models,
    sends them through the source's transport adapter, and returns a field-data
    source containing the response.

    :class:`~ansys.fluent.core.fields.live_field_data.Batch` is the standard
    implementation and
    :class:`~ansys.fluent.core.fields.live_field_data.BatchFieldData` is its
    response container.
    """

    @abstractmethod
    def get_surface_ids(self, surfaces: list[str | int | object]) -> list[int]:
        """Retrieve a list of surface IDs based on input surface names or numerical identifiers."""
        pass

    @abstractmethod
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
    ) -> FieldBatch:
        """
        Add field data requests for surfaces, scalars, vectors, or pathlines.

        This method allows users to specify multiple field data requests, which will
        later be processed when retrieving responses.
        """
        pass

    @abstractmethod
    def get_response(self) -> FieldDataSource:
        """
        Retrieve the response containing data for previously added field requests.

        This method processes all pending requests and returns the corresponding
        field data.
        """
        pass


class SurfaceData:
    """
    Class that enables object-style access to surface data structures.

    Attributes
    ----------
    vertices: npt.NDArray[np.float64] | None
    connectivity: list[npt.NDArray[np.float64]] | None
    face_centroids: npt.NDArray[np.float64] | None
    face_normals: npt.NDArray[np.float64] | None
    """

    def __init__(self, surf_data):
        """__init__ method of SurfaceData class."""
        self._surf_data = surf_data
        self.vertices: npt.NDArray[np.float64] | None = self._surf_data.get(
            SurfaceDataType.Vertices
        )
        self.connectivity: list[npt.NDArray[np.int32]] | None = self._surf_data.get(
            SurfaceDataType.FacesConnectivity
        )
        self.face_centroids: npt.NDArray[np.float64] | None = self._surf_data.get(
            SurfaceDataType.FacesCentroid
        )
        self.face_normals: npt.NDArray[np.float64] | None = self._surf_data.get(
            SurfaceDataType.FacesNormal
        )


class PathlinesData:
    """
    Class that enables object-style access to pathlines data structure.

    Attributes
    ----------
    scalar_field_name: str
    vertices: npt.NDArray[np.float64] | None
    lines: list[npt.NDArray[np.float64]] | None
    scalar_field: npt.NDArray[np.float64] | None
    pathlines_count: npt.NDArray[np.float64] | None
    particle_time: npt.NDArray[np.float64] | None
    """

    def __init__(self, pathlines_data_for_surface):
        """__init__ method of PathlinesData class."""
        self._pathlines_data_for_surface = pathlines_data_for_surface
        self.scalar_field_name: str = list(
            set(self._pathlines_data_for_surface.keys())
            - {"lines", "vertices", "pathlines-count", "particle-time"}
        )[0]
        self.vertices: npt.NDArray[np.float64] | None = (
            self._pathlines_data_for_surface.get("vertices")
        )
        self.lines: list[npt.NDArray[np.int32]] | None = (
            self._pathlines_data_for_surface.get("lines")
        )
        self.scalar_field: npt.NDArray[np.float64] | None = (
            self._pathlines_data_for_surface.get(self.scalar_field_name)
        )
        self.pathlines_count: npt.NDArray[np.float64] | None = (
            self._pathlines_data_for_surface.get("pathlines-count")
        )
        self.particle_time: npt.NDArray[np.float64] | None = (
            self._pathlines_data_for_surface.get("particle-time")
        )


class AbstractFieldData(ABC):
    """Abstract base class for the field data service."""

    @abstractmethod
    def get_scalar_field_range(
        self, field: str, node_value: bool = False, surface_ids: list[int] | None = None
    ) -> list[float]:
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
        pass

    @abstractmethod
    def get_scalar_fields_info(self) -> dict[str, dict]:
        """Get fields information (field name, domain, and section).

        Returns
        -------
        Dict
        """
        pass

    @abstractmethod
    def get_vector_fields_info(self) -> dict[str, dict]:
        """Get vector fields information (vector components).

        Returns
        -------
        Dict
        """
        pass

    @abstractmethod
    def get_surfaces_info(self) -> dict[str, dict]:
        """Get surfaces information (surface name, ID, and type).

        Returns
        -------
        Dict
        """
        pass

    @abstractmethod
    def get_solver_mesh_nodes_float(
        self, domain_id: int, thread_id: int
    ) -> list[float]:
        """Get mesh node -> floating point precision.

        Returns
        -------
        List[float]
        """
        pass

    @abstractmethod
    def get_solver_mesh_nodes_double(
        self, domain_id: int, thread_id: int
    ) -> list[float]:
        """Get mesh node -> double precision.

        Returns
        -------
        List[float]
        """
        pass

    @abstractmethod
    def get_solver_mesh_elements(self, domain_id: int, thread_id: int) -> list[float]:
        """Get mesh elements.

        Returns
        -------
        List[float]
        """
        pass

    @abstractmethod
    def _get_surface_data(
        self,
        data_types: list["SurfaceDataType"],
        surfaces: list[int | str],
        overset_mesh: bool | None = False,
    ) -> dict[int | str, dict["SurfaceDataType", np.ndarray | list[np.ndarray]]]:
        """Get surface data (vertices, faces connectivity, centroids, and normals)."""
        pass

    @abstractmethod
    def _add_surfaces_request(
        self,
        data_types: list["SurfaceDataType"],
        surfaces: list[int | str],
        overset_mesh: bool | None = False,
    ) -> dict[int | str, dict["SurfaceDataType", np.ndarray | list[np.ndarray]]]:
        """Get surface data (vertices, faces connectivity, centroids, and normals)."""
        pass

    @abstractmethod
    def _get_scalar_field_data(
        self,
        field_name: str,
        surfaces: list[int | str],
        node_value: bool | None = True,
        boundary_value: bool | None = True,
    ) -> dict[int | str, np.ndarray]:
        """Get scalar field data on a surface."""
        pass

    @abstractmethod
    def _add_scalar_fields_request(
        self,
        field_name: str,
        surfaces: list[int | str],
        node_value: bool | None = True,
        boundary_value: bool | None = True,
    ) -> None:
        """Add a scalar field request to the batched fields request."""
        pass

    @abstractmethod
    def _get_vector_field_data(
        self,
        field_name: str,
        surfaces: list[int | str],
    ) -> dict[int | str, np.ndarray]:
        """Get vector field data on a surface."""
        pass

    @abstractmethod
    def _add_vector_fields_request(self, field_name: str, surfaces: list[int | str]):
        """Add a vector field request to the batched fields request."""
        pass

    @abstractmethod
    def _get_pathlines_field_data(
        self,
        field_name: str,
        surfaces: list[int | str],
        additional_field_name: str = "",
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
    ) -> dict:
        """Get the pathlines field data on a surface."""
        pass

    @abstractmethod
    def _add_pathlines_fields_request(
        self,
        field_name: str,
        surfaces: list[int | str],
        additional_field_name: str = "",
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
    ) -> None:
        """Add a pathlines field request to the batched fields request."""
        pass

    @abstractmethod
    def extract_fields(self, chunk_iterator) -> dict[Any, dict[str, npt.NDArray[Any]]]:
        """Extract fields from the chunk iterator."""
        pass

    @abstractmethod
    def get_batched_fields(self) -> dict[Any, dict[str, npt.NDArray[Any]]]:
        """Get the batched fields from the service."""
        pass


_set_dataclass_field_docs(
    SurfaceFieldDataRequest,
    {
        "data_types": "Surface data entries to request: vertices, face connectivity, face normals, and face centroids.",
        "surfaces": "A sequence of valid Fluent surfaces, each identified by either an integer ID, a name string, or a settings API surface object (or any object with a name() -> str method).",
        "overset_mesh": "Whether overset mesh entities should be included when available.",
        "flatten_connectivity": "Whether face connectivity is returned in flattened format.",
    },
)

_set_dataclass_field_docs(
    ScalarFieldDataRequest,
    {
        "field_name": "Scalar field name to request.",
        "surfaces": "A sequence of valid Fluent surfaces, each identified by either an integer ID, a name string, or a settings API surface object (or any object with a name() -> str method).",
        "node_value": "Whether to request nodal values. If ``False``, element values are requested.",
        "boundary_value": "Whether to request boundary values when supported.",
    },
)

_set_dataclass_field_docs(
    VectorFieldDataRequest,
    {
        "field_name": "Vector field name to request.",
        "surfaces": "A sequence of valid Fluent surfaces, each identified by either an integer ID, a name string, or a settings API surface object (or any object with a name() -> str method).",
    },
)

_set_dataclass_field_docs(
    PathlinesFieldDataRequest,
    {
        "field_name": "Scalar field name to sample along computed pathlines.",
        "surfaces": "A sequence of valid Fluent surfaces, each identified by either an integer ID, a name string, or a settings API surface object (or any object with a name() -> str method).",
        "additional_field_name": "Optional additional scalar field to include in the response.",
        "provide_particle_time_field": "Whether to include a particle-time field in the output.",
        "node_value": "Whether to request nodal values.",
        "steps": "Maximum number of integration steps per pathline.",
        "step_size": "Integration step size.",
        "skip": "Number of sampled points to skip.",
        "reverse": "Whether to integrate pathlines in reverse direction.",
        "accuracy_control_on": "Whether adaptive accuracy control is enabled.",
        "tolerance": "Tolerance used when accuracy control is enabled.",
        "coarsen": "Coarsening factor applied to pathline output.",
        "velocity_domain": "Velocity domain used for pathline integration.",
        "zones": "Optional zones used to constrain pathline computation.",
        "flatten_connectivity": "Whether line connectivity is returned in flattened format.",
    },
)


class _ReturnFieldData:
    @staticmethod
    def _scalar_data(
        field_name: str,
        surfaces: list[int | str | object],
        surface_ids: list[int],
        scalar_field_data: np.ndarray,
    ) -> dict[int | str, np.ndarray]:
        surfaces = _get_surfaces_from_objects(surfaces)
        return {
            surface: scalar_field_data[surface_ids[count]][field_name]
            for count, surface in enumerate(surfaces)
        }

    @staticmethod
    def _surface_data(
        data_types: list[SurfaceDataType],
        surfaces: list[int | str | object],
        surface_ids: list[int],
        surface_data: np.ndarray | list[np.ndarray],
        deprecated_flag: bool | None = False,
        flatten_connectivity: bool = False,
    ) -> dict[int | str, dict[SurfaceDataType, np.ndarray | list[np.ndarray]]]:
        surfaces = _get_surfaces_from_objects(surfaces)
        ret_surf_data = {}
        for count, surface in enumerate(surfaces):
            ret_surf_data[surface] = {}
            for data_type in data_types:
                if data_type == SurfaceDataType.FacesConnectivity:
                    if flatten_connectivity:
                        ret_surf_data[surface][data_type] = surface_data[
                            surface_ids[count]
                        ][SurfaceDataType.FacesConnectivity.value]
                    else:
                        from ansys.fluent.core.exceptions import (
                            PyFluentDeprecationWarning,
                        )

                        warnings.warn(
                            "Structured face connectivity output is deprecated and will be replaced by the flat format "
                            "in a future release. In the current release, pass 'flatten_connectivity=True' argument while creating the "
                            "'SurfaceFieldDataRequest' to request data in the flat format.",
                            PyFluentDeprecationWarning,
                        )
                        ret_surf_data[surface][data_type] = (
                            _transform_faces_connectivity_data(
                                surface_data[surface_ids[count]][
                                    SurfaceDataType.FacesConnectivity.value
                                ]
                            )
                        )
                else:
                    ret_surf_data[surface][data_type] = surface_data[
                        surface_ids[count]
                    ][data_type.value].reshape(-1, 3)
            if deprecated_flag is False:
                ret_surf_data[surface] = SurfaceData(ret_surf_data[surface])
        return ret_surf_data

    @staticmethod
    def _vector_data(
        field_name: str,
        surfaces: list[int | str | object],
        surface_ids: list[int],
        vector_field_data: np.ndarray,
    ) -> dict[int | str, np.ndarray]:
        surfaces = _get_surfaces_from_objects(surfaces)
        return {
            surface: vector_field_data[surface_ids[count]][field_name].reshape(-1, 3)
            for count, surface in enumerate(surfaces)
        }

    @staticmethod
    def _pathlines_data(
        field_name: str,
        surfaces: list[int | str | object],
        surface_ids: list[int],
        pathlines_data: dict,
        deprecated_flag: bool | None = False,
        flatten_connectivity: bool = False,
    ) -> dict[int | str, dict[str, np.ndarray | list[np.ndarray]]]:
        surfaces = _get_surfaces_from_objects(surfaces)
        path_lines_dict = {}
        for count, surface in enumerate(surfaces):
            if flatten_connectivity:
                lines_data = pathlines_data[surface_ids[count]]["lines"]
            else:
                from ansys.fluent.core.exceptions import (
                    PyFluentDeprecationWarning,
                )

                warnings.warn(
                    "Structured face connectivity output is deprecated and will be replaced by the flat format "
                    "in a future release. In the current release, pass 'flatten_connectivity=True' argument while creating the "
                    "'PathlinesFieldDataRequest' to request data in the flat format.",
                    PyFluentDeprecationWarning,
                )
                lines_data = _transform_faces_connectivity_data(
                    pathlines_data[surface_ids[count]]["lines"]
                )
            temp_dict = {
                "vertices": pathlines_data[surface_ids[count]]["vertices"].reshape(
                    -1, 3
                ),
                "lines": lines_data,
                field_name: pathlines_data[surface_ids[count]][field_name],
                "pathlines-count": pathlines_data[surface_ids[count]][
                    "pathlines-count"
                ],
            }
            if "particle-time" in pathlines_data[surface_ids[count]]:
                temp_dict["particle-time"] = pathlines_data[surface_ids[count]][
                    "particle-time"
                ]
            if deprecated_flag is False:
                path_lines_dict[surface] = PathlinesData(temp_dict)
            else:
                path_lines_dict[surface] = temp_dict
        return path_lines_dict
