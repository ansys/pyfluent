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

"""High-level user-facing API for retrieving field data from Fluent surfaces.

This module provides the primary interface for querying scalar fields, vector fields,
surface data, and pathlines from Ansys Fluent simulations. It wraps the low-level
FieldData gRPC service and exposes intuitive classes for both real-time and batched
field data retrieval.

Key classes:
    - :class:`LiveFieldData`: Primary entry point for accessing field data live from
      a running Fluent session. Supports individual queries and batch operations.
    - :class:`Batch`: Accumulates multiple field data requests and retrieves them
      efficiently in a single server round-trip via :meth:`Batch.get_response`.
    - :class:`BatchFieldData`: Read-only container for field data returned from a
      batch request.
    - :class:`Mesh`: Represents the computational mesh (nodes and elements) for a
      Fluent zone, returned by :meth:`LiveFieldData.get_mesh`.
"""

from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from enum import Enum
import logging
import time
import warnings
import weakref

import numpy as np

from ansys.fluent.core.exceptions import DisallowedValuesError
from ansys.fluent.core.fields.field_data_interfaces import (
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
    _VectorFields,
    get_surfaces_from_objects,
)
from ansys.fluent.core.pyfluent_warnings import PyFluentDeprecationWarning
from ansys.fluent.core.variable_strategies import (
    FluentFieldDataNamingStrategy as naming_strategy,
)

_naming_strategy_instance = naming_strategy()
_to_field_name_str = _naming_strategy_instance.to_string

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
        return self._field_data.get_scalar_field_range(
            _to_field_name_str(field), node_value, surface_ids
        )

    def _get_scalar_fields_info(self) -> dict[str, dict]:
        return self._field_data.get_scalar_fields_info()

    def _get_vector_fields_info(self) -> dict[str, dict]:
        return self._field_data.get_vector_fields_info()

    def _get_surfaces_info(self) -> dict[str, dict]:
        return self._field_data.get_surfaces_info()


class BaseFieldData:
    """Base class providing shared field data retrieval logic.

    Provides common functionality for extracting scalar fields, surface geometry,
    vector fields, and pathlines from pre-fetched Fluent field data. This class is
    not intended to be used directly; use :class:`LiveFieldData` for live session
    access or :class:`BatchFieldData` for data returned from a batch request.
    """

    def __init__(
        self,
        data: dict,
        field_info,
        allowed_surface_names,
        allowed_scalar_field_names,
    ):
        """Initialize the field data container.

        Parameters
        ----------
        data : dict
            Raw field data keyed by request descriptor tuples.
        field_info : _FieldInfo
            Object used to query metadata about available fields and surfaces.
        allowed_surface_names : _AllowedSurfaceNames
            Validator for surface name inputs.
        allowed_scalar_field_names : _AllowedScalarFieldNames
            Validator for scalar field name inputs.
        """
        self.data = data
        self._field_info = field_info
        self._allowed_surface_names = allowed_surface_names
        self._allowed_scalar_field_names = allowed_scalar_field_names
        self._returned_data = _ReturnFieldData()
        self._deprecated_flag = False

    def get_surface_ids(self, surfaces: list[str | int]) -> list[int]:
        """Resolve surface names or IDs to a list of integer surface IDs.

        Parameters
        ----------
        surfaces : list[str | int]
            Surface names (str) or surface IDs (int) to resolve.

        Returns
        -------
        list[int]
            Corresponding list of integer surface IDs recognized by Fluent.

        Raises
        ------
        DisallowedValuesError
            If a surface name or ID is not found among the allowed surfaces.
        """
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
        """Retrieve field data for a surface, scalar, vector, or pathlines request.

        Dispatches the request to the appropriate internal handler based on the
        type of *obj* and returns field data keyed by surface ID or surface name.

        Parameters
        ----------
        obj : SurfaceFieldDataRequest | ScalarFieldDataRequest | VectorFieldDataRequest | PathlinesFieldDataRequest
            A request object describing the field type, field name, and target
            surfaces. Construct the appropriate request type from
            :mod:`ansys.fluent.core.fields.field_data_interfaces`.

        Returns
        -------
        dict[int | str, dict | np.ndarray]
            Field data keyed by surface ID (int) or surface name (str), depending
            on how surfaces were specified in the request. If field data is
            unavailable for a surface, an empty array is returned and a warning is
            issued. Always check the array size before using the data.

        Examples
        --------
        >>> data = field_data.get_field_data(
        ...     ScalarFieldDataRequest(field_name="pressure", surfaces=["wall"])
        ... )
        >>> pressure_array = data["wall"]
        >>> if pressure_array.size == 0:
        ...     # Handle missing data
        ...     pass
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
    """Read-only container for Fluent field data retrieved via a batch request.

    Returned by :meth:`Batch.get_response`, this object holds all field data
    collected during a batch session. Use :meth:`get_field_data` (inherited from
    :class:`BaseFieldData`) to extract individual field arrays keyed by surface.

    Examples
    --------
    >>> batch = field_data.new_batch()
    >>> batch.add_requests(
    ...     ScalarFieldDataRequest(field_name="pressure", surfaces=["wall"])
    ... )
    >>> result: BatchFieldData = batch.get_response()
    >>> pressure = result.get_field_data(
    ...     ScalarFieldDataRequest(field_name="pressure", surfaces=["wall"])
    ... )
    """

    def __init__(
        self,
        data: dict,
        field_info,
        allowed_surface_names,
        allowed_scalar_field_names,
    ):
        """Initialize a BatchFieldData container.

        Parameters
        ----------
        data : dict
            Extracted field data keyed by request descriptor tuples.
        field_info : _FieldInfo
            Object used to query metadata about available fields and surfaces.
        allowed_surface_names : _AllowedSurfaceNames
            Validator for surface name inputs.
        allowed_scalar_field_names : _AllowedScalarFieldNames
            Validator for scalar field name inputs.
        """
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
    """Accumulates field data requests and retrieves them in a single batch call.

    Use this class to efficiently request multiple field quantities simultaneously,
    reducing the number of server round-trips. Create an instance through
    :meth:`LiveFieldData.new_batch`, add requests with :meth:`add_requests`, then
    call :meth:`get_response` to retrieve all data at once.

    Examples
    --------
    >>> batch = field_data.new_batch()
    >>> batch.add_requests(
    ...     ScalarFieldDataRequest(field_name="pressure", surfaces=["wall"]),
    ...     VectorFieldDataRequest(field_name="velocity", surfaces=["wall"]),
    ... )
    >>> result = batch.get_response()
    """

    def __init__(
        self,
        field_data,
        field_info,
        allowed_surface_ids,
        allowed_surface_names,
        allowed_scalar_field_names,
        allowed_vector_field_names,
    ):
        """Initialize a Batch instance.

        Parameters
        ----------
        field_data : object
            Low-level field data service proxy connected to a running Fluent session.
        field_info : _FieldInfo
            Object used to query metadata about available fields and surfaces.
        allowed_surface_ids : _AllowedSurfaceIDs
            Validator for surface ID inputs.
        allowed_surface_names : _AllowedSurfaceNames
            Validator for surface name inputs.
        allowed_scalar_field_names : _AllowedScalarFieldNames
            Validator for scalar field name inputs.
        allowed_vector_field_names : _AllowedVectorFieldNames
            Validator for vector field name inputs.
        """
        self._field_data = field_data
        self._field_info = field_info

        self._allowed_surface_names = allowed_surface_names
        self._allowed_scalar_field_names = allowed_scalar_field_names
        self._allowed_vector_field_names = allowed_vector_field_names

        self._pathline_field_data = []
        self._cache_requests = []

    def get_surface_ids(self, surfaces: list[str | int]) -> list[int]:
        """Resolve surface names or IDs to a list of integer surface IDs.

        Parameters
        ----------
        surfaces : list[str | int]
            Surface names (str) or surface IDs (int) to resolve.

        Returns
        -------
        list[int]
            Corresponding list of integer surface IDs recognized by Fluent.

        Raises
        ------
        DisallowedValuesError
            If a surface name or ID is not found among the allowed surfaces.
        """
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
            self._allowed_scalar_field_names.valid_name(
                _to_field_name_str(kwargs.get("field_name"))
            ),
            surfaces=kwargs.get("surfaces"),
            node_value=kwargs.get("node_value"),
            boundary_value=kwargs.get("boundary_value"),
        )

    def _add_vector_fields_request(self, **kwargs) -> None:
        self._field_data._add_vector_fields_request(
            self._allowed_vector_field_names.valid_name(
                _to_field_name_str(kwargs.get("field_name"))
            ),
            surfaces=kwargs.get("surfaces"),
        )

    def _add_pathlines_fields_request(
        self,
        **kwargs,
    ) -> None:
        zones = kwargs.get("zones", [])
        field_name = self._allowed_scalar_field_names.valid_name(
            _to_field_name_str(kwargs.get("field_name"))
        )
        if field_name in self._pathline_field_data:
            raise ValueError("For 'path-lines' `field_name` should be unique.")
        else:
            self._pathline_field_data.append(field_name)
        additional_field_name = kwargs.get("additional_field_name")
        if additional_field_name:
            additional_field_name = self._allowed_scalar_field_names.valid_name(
                _to_field_name_str(additional_field_name)
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
        """Add one or more field data requests to the batch queue.

        Accepts requests for surface geometry, scalar fields, vector fields, or
        pathlines. All requested surfaces are resolved to integer IDs. Duplicate
        requests are ignored with a warning. This method returns ``self`` to
        support method chaining.

        Parameters
        ----------
        obj : SurfaceFieldDataRequest | ScalarFieldDataRequest | VectorFieldDataRequest | PathlinesFieldDataRequest
            The first (required) field data request.
        *args : SurfaceFieldDataRequest | ScalarFieldDataRequest | VectorFieldDataRequest | PathlinesFieldDataRequest
            Additional optional field data requests.

        Returns
        -------
        Batch
            Returns ``self`` to allow method chaining with :meth:`get_response`.

        Raises
        ------
        ValueError
            If two pathlines requests share the same ``field_name``.

        Examples
        --------
        >>> result = (
        ...     field_data.new_batch()
        ...     .add_requests(
        ...         ScalarFieldDataRequest(field_name="pressure", surfaces=["wall"]),
        ...         VectorFieldDataRequest(field_name="velocity", surfaces=["wall"]),
        ...     )
        ...     .get_response()
        ... )
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
        """Send all queued requests to Fluent and return the retrieved field data.

        Executes all requests added via :meth:`add_requests` in a single server
        call. Returns a :class:`BatchFieldData` object; use its
        :meth:`~BatchFieldData.get_field_data` method to access individual field
        arrays by surface.

        Returns
        -------
        BatchFieldData
            Container holding the retrieved field data for all requested surfaces
            and field types.

        Examples
        --------
        >>> batch = field_data.new_batch()
        >>> batch.add_requests(
        ...     ScalarFieldDataRequest(field_name="pressure", surfaces=["wall"])
        ... )
        >>> result = batch.get_response()
        >>> pressure = result.get_field_data(
        ...     ScalarFieldDataRequest(field_name="pressure", surfaces=["wall"])
        ... )
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
    """Enumeration of zone types that classify mesh zones in the Fluent solver."""

    CELL = 1
    FACE = 2


@dataclass
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


@dataclass
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


@dataclass
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


@dataclass
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
    node_indices: list[int] = field(default_factory=list)
    facets: list[Facet] = field(default_factory=list)


@dataclass
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


class LiveFieldData(BaseFieldData, FieldDataSource):
    """Primary high-level interface for accessing field data from a live Fluent session.

    This is the main user-facing entry point for querying field quantities from a
    running Fluent solver. It supports retrieving scalar fields, vector fields,
    surface geometry data, and pathlines for one or more surfaces. Mesh topology
    for cell zones is accessible via :meth:`get_mesh`.

    For retrieving multiple field quantities at once, use :meth:`new_batch` to
    create a :class:`Batch` that collects all requests and sends them to Fluent
    in a single round-trip.

    Attributes
    ----------
    surfaces : _SurfaceNames
        Lists all surface names available in the current Fluent session.
    surface_ids : _SurfaceIds
        Lists all surface IDs available in the current Fluent session.
    scalar_fields : _ScalarFields
        Lists available scalar field names (e.g., ``"pressure"``,
        ``"temperature"``).
    vector_fields : _VectorFields
        Lists available vector field names (e.g., ``"velocity"``).

    Examples
    --------
    >>> field_data = solver.fields.field_data
    >>> pressure = field_data.get_field_data(
    ...     ScalarFieldDataRequest(field_name="pressure", surfaces=["wall"])
    ... )
    """

    def __init__(
        self,
        field_data,
        field_info,
        scheme_interpreter,
        get_zones_info: weakref.WeakMethod[Callable[[], list[ZoneInfo]]] | None = None,
    ):
        """Initialize a LiveFieldData instance.

        Parameters
        ----------
        field_data : object
            Low-level field data service proxy connected to a running Fluent session.
        field_info : object
            Low-level field info service proxy for querying available fields and
            surfaces.
        scheme_interpreter : object
            Interface to the Fluent Scheme interpreter, used for evaluating
            expressions such as precision queries.
        get_zones_info : weakref.WeakMethod, optional
            Weak reference to a callable that returns a list of :class:`ZoneInfo`
            objects. Required for mesh retrieval via :meth:`get_mesh`.
        """
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
        """Create a new :class:`Batch` for queuing multiple field data requests.

        Use a batch to accumulate several field data requests (scalar, vector,
        surface geometry, or pathlines) and retrieve them all from Fluent in a
        single efficient server call via :meth:`Batch.get_response`.

        Returns
        -------
        Batch
            A new :class:`Batch` instance bound to this session.

        Examples
        --------
        >>> batch = field_data.new_batch()
        >>> batch.add_requests(
        ...     ScalarFieldDataRequest(field_name="pressure", surfaces=["wall"]),
        ...     VectorFieldDataRequest(field_name="velocity", surfaces=["wall"]),
        ... )
        >>> result = batch.get_response()
        """
        return Batch(
            self._field_data,
            self._field_info,
            self._allowed_surface_ids,
            self._allowed_surface_names,
            self._allowed_scalar_field_names,
            self._allowed_vector_field_names,
        )

    def _get_scalar_field_data(self, **kwargs):
        surfaces = kwargs.get("surfaces")
        surface_ids = self.get_surface_ids(surfaces)
        field_name = self._allowed_scalar_field_names.valid_name(
            _to_field_name_str(kwargs.get("field_name"))
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
            _to_field_name_str(kwargs.get("field_name"))
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
            _to_field_name_str(kwargs.get("field_name"))
        )
        additional_field_name = kwargs.get("additional_field_name")
        if additional_field_name:
            additional_field_name = self._allowed_scalar_field_names.valid_name(
                _to_field_name_str(additional_field_name)
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
        """Retrieve the computational mesh for a Fluent cell zone.

        Fetches node coordinates and element connectivity from the Fluent solver
        for the specified zone and returns them as a :class:`Mesh` object. Only
        cell zones are currently supported; face zones raise
        :exc:`NotImplementedError`.

        Parameters
        ----------
        zone : str | int
            Name or integer ID of the zone to retrieve. Must be a cell zone.

        Returns
        -------
        Mesh
            :class:`Mesh` containing all :class:`Node` coordinates and
            :class:`Element` connectivity for the zone.

        Raises
        ------
        ValueError
            If *zone* does not match any known zone name or ID.
        NotImplementedError
            If *zone* refers to a face zone.

        Examples
        --------
        >>> mesh = field_data.get_mesh("fluid")
        >>> print(f"Nodes: {len(mesh.nodes)}, Elements: {len(mesh.elements)}")
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
