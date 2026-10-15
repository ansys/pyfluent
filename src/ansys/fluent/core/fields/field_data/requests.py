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

"""Public request models for Fluent surface and field-data queries."""

from __future__ import annotations

import dataclasses
from enum import Enum
from typing import Iterable

from ansys.fluent.core.fields.field_data._field_data_interfaces import (
    _set_dataclass_field_docs,
    _validate_scalar_variable_descriptor,
    _validate_vector_variable_descriptor,
)
from ansys.units.variable_descriptor import (
    ScalarVariableDescriptor,
    VectorVariableDescriptor,
)

__all__ = (
    "BaseDataRequest",
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
