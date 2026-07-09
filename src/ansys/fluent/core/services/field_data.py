# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
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

"""High-level field data wrappers.

This module owns the business-logic layer on top of the FieldData gRPC
service. The grpc service implementation lives in:

* ``ansys.fluent.core._grpc_services.field_data_service`` (v1 proto API)
* ``ansys.fluent.core._grpc_services.field_data_service_v0`` (v0 proto API)

Class hierarchy
---------------
``FieldDataBase``
    Shared implementation for all versions. Delegates the core field-data
    operations (scalar/vector/surface/pathlines retrieval, batching, etc.)
    to the underlying gRPC service.

``FieldDataV251(FieldDataBase)``
    Used for Fluent 24R2 and 25R1 (v0 proto API). ``is_data_valid``
    is evaluated eagerly via the Scheme interpreter
    (``(data-valid?)``), because the ``IsSolutionDataAvailable`` RPC
    was not yet available in the AppUtilities service for these versions.

``FieldDataV261(FieldDataBase)``
    Used for Fluent 25R2 and 26R1 (v0 proto API). ``is_data_valid``
    is a callable bound to ``ApplicationRuntimeServiceV0.is_solution_data_available``,
    which became available from 25R2 onward.

``FieldData(FieldDataBase)``
    Used from Fluent 27R1 onward (v1 proto API). ``is_data_valid``
    is a callable bound to the v1 field-data service's
    ``is_solution_data_available``.
"""

from typing import Any

import numpy as np
import numpy.typing as npt

from ansys.fluent.core.field_data_interfaces import SurfaceDataType
from ansys.fluent.core.services.abstract_field_data import AbstractFieldData


class FieldDataBase(AbstractFieldData):
    """Shared base class for FieldData and FieldDataV261 classes."""

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
        return self._service._get_surface_data(data_types, surfaces, overset_mesh)

    def _add_surfaces_request(
        self,
        data_types: list[SurfaceDataType],
        surfaces: list[int | str],
        overset_mesh: bool | None = False,
    ) -> dict[int | str, dict[SurfaceDataType, np.ndarray | list[np.ndarray]]]:
        """Get surface data (vertices, faces connectivity, centroids, and normals)."""
        return self._service._add_surfaces_request(
            data_types=data_types, surfaces=surfaces, overset_mesh=overset_mesh
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

    def _add_vector_fields_request(self, field_name: str, surfaces: list[int | str]):
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
    ) -> dict:
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
        return self._service.get_fields(self._service._batched_fields_request)


class FieldDataV261(FieldDataBase):
    """Class for FieldDataV261 service."""

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
    """Class for FieldDataV251 service."""

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
    """Class for FieldData service."""

    def __init__(
        self,
        service,
        chunk_parser,
    ):
        """__init__ method of FieldData class."""
        super().__init__(service, chunk_parser)
        self.is_data_valid = self._service.is_solution_data_available
