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

"""High-level user-facing field-data API.

This module sits above a transport adapter that implements
:class:`~ansys.fluent.core.fields.abstract_field_data.AbstractFieldData`. The
adapter can use any kind of service, such as gRPC or REST. ``FieldDataBase`` and
its version-specific subclasses implement that transport contract by forwarding
operations to the selected service object and parsing returned data.

:class:`LiveFieldData` is the user-facing wrapper over that service layer. It
validates requests, resolves surfaces, exposes field metadata, and creates
:class:`Batch` objects through :meth:`LiveFieldData.new_batch`. ``Batch``
collects requests and returns a :class:`BatchFieldData`, which is a thin
read-only wrapper over the shared :class:`BaseFieldData` implementation.

This separation lets users build a custom transport by implementing
:class:`~ansys.fluent.core.fields.abstract_field_data.AbstractFieldData`, or a
custom user-facing layer by implementing
:class:`~ansys.fluent.core.fields.abstract_field_data.FieldDataSource`.

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

from __future__ import annotations

from collections.abc import Callable
import logging
import time
from typing import Any
import warnings
import weakref

import numpy as np
import numpy.typing as npt

from ansys.fluent.core._variable_strategies import (
    FluentFieldDataNamingStrategy as naming_strategy,
)
from ansys.fluent.core.fields.field_data._field_data_interfaces import (
    _AllowedScalarFieldNames,
    _AllowedSurfaceIDs,
    _AllowedSurfaceNames,
    _AllowedVectorFieldNames,
    _BaseFieldInfo,
    _get_surface_ids,
    _ScalarFields,
    _SurfaceIds,
    _SurfaceNames,
    _VectorFields,
)
from ansys.fluent.core.fields.field_data.abstract_field_data import (
    AbstractFieldData,
    BaseFieldDataSource,
    CellElementType,
    Element,
    Facet,
    FieldBatch,
    FieldDataSource,
    Mesh,
    Node,
    PathlinesData,
    PathlinesFieldDataRequest,
    ScalarFieldDataRequest,
    SurfaceData,
    SurfaceDataType,
    SurfaceFieldDataRequest,
    VectorFieldDataRequest,
    ZoneInfo,
    ZoneType,
    _ReturnFieldData,
)

_naming_strategy_instance = naming_strategy()
_to_field_name_str = _naming_strategy_instance.to_string

logger = logging.getLogger("pyfluent.field_data")


class _FieldInfo(_BaseFieldInfo):
    def __init__(
        self,
        field_data: AbstractFieldData,
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


class BaseFieldData(BaseFieldDataSource):
    """Shared implementation for live and batched field-data responses.

    This class implements the request dispatch and response extraction shared by
    :class:`LiveFieldData` and :class:`BatchFieldData`. It is not a transport
    adapter and is not intended to be instantiated directly.
    """

    def __init__(
        self,
        data: dict[Any, Any],
        field_info: _BaseFieldInfo,
        allowed_surface_names: _AllowedSurfaceNames,
        allowed_scalar_field_names: _AllowedScalarFieldNames,
    ) -> None:
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
    ) -> dict[int | str, SurfaceData | PathlinesData | np.ndarray]:
        """Retrieve field data for a surface, scalar, vector, or pathlines request.

        Dispatches the request to the appropriate internal handler based on the
        type of *obj* and returns field data keyed by surface ID or surface name.

        Parameters
        ----------
        obj : SurfaceFieldDataRequest | ScalarFieldDataRequest | VectorFieldDataRequest | PathlinesFieldDataRequest
            A request object describing the field type, field name, and target
            surfaces. Construct the appropriate request type from
            :mod:`ansys.fluent.core.fields.abstract_field_data`.

        Returns
        -------
        dict[int | str, SurfaceData | PathlinesData | np.ndarray]
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


class BatchFieldData(BaseFieldData):
    """Read-only response container returned by :class:`Batch`.

    The batch transport response is stored here and exposed through the shared
    :meth:`BaseFieldData.get_field_data` implementation. This class adds only
    response-container behavior; it does not issue service calls.

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
        data: dict[Any, Any],
        field_info: _BaseFieldInfo,
        allowed_surface_names: _AllowedSurfaceNames,
        allowed_scalar_field_names: _AllowedScalarFieldNames,
    ) -> None:
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

    def __len__(self) -> int:
        return len(self.data)

    def __call__(self) -> dict[Any, Any]:
        return self.data


class Batch(FieldBatch):
    """Collect field-data requests and retrieve them in one service call.

    Create this object with :meth:`LiveFieldData.new_batch`. It delegates the
    transport operation to the :class:`AbstractFieldData` implementation owned
    by the parent :class:`LiveFieldData`, then returns a
    :class:`BatchFieldData` from :meth:`get_response`.

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
        field_data: AbstractFieldData,
        field_info: _FieldInfo,
        allowed_surface_ids: _AllowedSurfaceIDs,
        allowed_surface_names: _AllowedSurfaceNames,
        allowed_scalar_field_names: _AllowedScalarFieldNames,
        allowed_vector_field_names: _AllowedVectorFieldNames,
    ) -> None:
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

    def get_surface_ids(self, surfaces: list[str | int | object]) -> list[int]:
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

    def __call__(self) -> None:
        self.get_response()


# Root domain id in Fluent.
ROOT_DOMAIN_ID = 1


class LiveFieldData(BaseFieldData, FieldDataSource):
    """Primary user-facing wrapper over an :class:`AbstractFieldData` service.

    The ``field_data`` argument is the transport-specific service adapter. It
    implements :class:`~ansys.fluent.core.fields.abstract_field_data.AbstractFieldData`
    and can be backed by any kind of service, such as gRPC or REST. This wrapper
    adds validation, surface resolution, field metadata helpers, and conversion
    of transport results into user-facing objects.

    Use :meth:`new_batch` to create a :class:`Batch` for multiple requests. The
    batch returns a :class:`BatchFieldData` response while
    :class:`BaseFieldData` supplies the shared response extraction logic.

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
        field_data: AbstractFieldData,
        field_info: _FieldInfo,
        scheme_interpreter: Any,
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

    def new_batch(self) -> Batch:
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


class FieldDataBase(AbstractFieldData):
    """Shared transport adapter for Fluent field-data service versions.

    This class implements
    :class:`~ansys.fluent.core.fields.abstract_field_data.AbstractFieldData` by
    forwarding calls to ``service`` and parsing responses with ``chunk_parser``.
    :class:`FieldData`, :class:`FieldDataV251`, and :class:`FieldDataV261`
    provide version-specific service details while preserving the same contract
    for :class:`LiveFieldData`.
    """

    def __init__(
        self,
        service,
        chunk_parser,
    ):
        """__init__ method of FieldData class."""
        self._service = service
        self._chunk_parser = chunk_parser

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
        return self._service.get_scalar_field_range(field, node_value, surface_ids)

    def get_scalar_fields_info(self) -> dict[str, dict]:
        """Get fields information (field name, domain, and section).

        Returns
        -------
        Dict
        """
        return self._service.get_scalar_fields_info()

    def get_vector_fields_info(self) -> dict[str, dict]:
        """Get vector fields information (vector components).

        Returns
        -------
        Dict
        """
        return self._service.get_vector_fields_info()

    def get_surfaces_info(self) -> dict[str, dict]:
        """Get surfaces information (surface name, ID, and type).

        Returns
        -------
        Dict
        """
        return self._service.get_surfaces_info()

    def get_solver_mesh_nodes_float(
        self, domain_id: int, thread_id: int
    ) -> list[float]:
        """Get mesh node -> floating point precision.

        Returns
        -------
        List[float]
        """
        return self._service.get_solver_mesh_nodes_float(domain_id, thread_id)

    def get_solver_mesh_nodes_double(
        self, domain_id: int, thread_id: int
    ) -> list[float]:
        """Get mesh node -> double precision.

        Returns
        -------
        List[float]
        """
        return self._service.get_solver_mesh_nodes_double(domain_id, thread_id)

    def get_solver_mesh_elements(self, domain_id: int, thread_id: int) -> list[float]:
        """Get mesh elements.

        Returns
        -------
        List[float]
        """
        return self._service.get_solver_mesh_elements(domain_id, thread_id)

    def _get_surface_data(
        self,
        data_types: list[SurfaceDataType],
        surfaces: list[int | str],
        overset_mesh: bool | None = False,
    ) -> dict[int | str, dict[SurfaceDataType, np.ndarray | list[np.ndarray]]]:
        """Get surface data (vertices, faces connectivity, centroids, and normals)."""
        return self._service._get_surface_data(
            [dt.value if isinstance(dt, SurfaceDataType) else dt for dt in data_types],
            surfaces,
            overset_mesh,
        )

    def _add_surfaces_request(
        self,
        data_types: list[SurfaceDataType],
        surfaces: list[int | str],
        overset_mesh: bool | None = False,
    ) -> dict[int | str, dict[SurfaceDataType, np.ndarray | list[np.ndarray]]]:
        """Get surface data (vertices, faces connectivity, centroids, and normals)."""
        return self._service._add_surfaces_request(
            data_types=[
                dt.value if isinstance(dt, SurfaceDataType) else dt for dt in data_types
            ],
            surfaces=surfaces,
            overset_mesh=overset_mesh,
        )

    def _get_scalar_field_data(
        self,
        field_name: str,
        surfaces: list[int | str],
        node_value: bool | None = True,
        boundary_value: bool | None = True,
    ) -> dict[int | str, np.ndarray]:
        """Get scalar field data on a surface."""
        return self._service._get_scalar_field_data(
            field_name=field_name,
            surface_ids=surfaces,
            node_value=node_value,
            boundary_value=boundary_value,
        )

    def _add_scalar_fields_request(
        self,
        field_name: str,
        surfaces: list[int | str],
        node_value: bool | None = True,
        boundary_value: bool | None = True,
    ) -> None:
        """Add a scalar field request to the batched fields request."""
        return self._service._add_scalar_fields_request(
            field_name=field_name,
            surfaces=surfaces,
            node_value=node_value,
            boundary_value=boundary_value,
        )

    def _get_vector_field_data(
        self,
        field_name: str,
        surfaces: list[int | str],
    ) -> dict[int | str, np.ndarray]:
        """Get vector field data on a surface."""
        return self._service._get_vector_field_data(
            field_name=field_name,
            surface_ids=surfaces,
        )

    def _add_vector_fields_request(
        self, field_name: str, surfaces: list[int | str]
    ) -> None:
        """Add a vector field request to the batched fields request."""
        return self._service._add_vector_fields_request(
            field_name=field_name,
            surfaces=surfaces,
        )

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
    ) -> dict[Any, Any]:
        """Get the pathlines field data on a surface."""
        return self._service._get_pathlines_field_data(
            field_name=field_name,
            surfaces=surfaces,
            additional_field_name=additional_field_name,
            provide_particle_time_field=provide_particle_time_field,
            node_value=node_value,
            steps=steps,
            step_size=step_size,
            skip=skip,
            reverse=reverse,
            accuracy_control_on=accuracy_control_on,
            tolerance=tolerance,
            coarsen=coarsen,
            velocity_domain=velocity_domain,
            zones=zones,
        )

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
        return self._service._add_pathlines_fields_request(
            field_name=field_name,
            surfaces=surfaces,
            additional_field_name=additional_field_name,
            provide_particle_time_field=provide_particle_time_field,
            node_value=node_value,
            steps=steps,
            step_size=step_size,
            skip=skip,
            reverse=reverse,
            accuracy_control_on=accuracy_control_on,
            tolerance=tolerance,
            coarsen=coarsen,
            velocity_domain=velocity_domain,
            zones=zones,
        )

    def extract_fields(self, chunk_iterator) -> dict[Any, dict[str, npt.NDArray[Any]]]:
        """Extract fields from the chunk iterator."""
        return self._chunk_parser.extract_fields(chunk_iterator)

    def get_batched_fields(self) -> dict[Any, dict[str, npt.NDArray[Any]]]:
        """Get the batched fields from the service."""
        result = self._service.get_fields(self._service._batched_fields_request)
        self._service.reset_batched_fields_request()
        return result


class FieldDataV261(FieldDataBase):
    """Field-data transport adapter for Fluent 26.1 and later."""

    def __init__(
        self,
        service,
        chunk_parser,
        application_runtime_service,
    ):
        """__init__ method of FieldDataV261 class."""
        super().__init__(service, chunk_parser)
        self._application_runtime_service = application_runtime_service
        self.is_data_valid = (
            self._application_runtime_service.is_solution_data_available
        )


class FieldDataV251(FieldDataBase):
    """Field-data transport adapter for Fluent 25.1."""

    def __init__(
        self,
        service,
        chunk_parser,
        scheme_interpreter_service,
    ):
        """__init__ method of FieldDataV251 class."""
        super().__init__(service, chunk_parser)
        self._scheme_interpreter_service = scheme_interpreter_service

    def is_data_valid(self):
        """Check if the solution data is valid."""
        return self._scheme_interpreter_service.eval("(data-valid?)")


class FieldData(FieldDataBase):
    """Default field-data transport adapter for the base Fluent service API."""

    def __init__(
        self,
        service,
        chunk_parser,
    ):
        """__init__ method of FieldData class."""
        super().__init__(service, chunk_parser)
        self.is_data_valid = self._service.is_solution_data_available
