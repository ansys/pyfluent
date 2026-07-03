# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
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

"""Abstract reduction wrapper."""

from abc import ABC, abstractmethod
from typing import Any

import numpy as np
import numpy.typing as npt

from ansys.fluent.core.field_data_interfaces import SurfaceDataType


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
        data_types: list[SurfaceDataType],
        surfaces: list[int | str],
        overset_mesh: bool | None = False,
    ) -> dict[int | str, dict[SurfaceDataType, np.ndarray | list[np.ndarray]]]:
        """Get surface data (vertices, faces connectivity, centroids, and normals)."""
        pass

    @abstractmethod
    def _add_surfaces_request(
        self,
        data_types: list[SurfaceDataType],
        surfaces: list[int | str],
        overset_mesh: bool | None = False,
    ) -> dict[int | str, dict[SurfaceDataType, np.ndarray | list[np.ndarray]]]:
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
