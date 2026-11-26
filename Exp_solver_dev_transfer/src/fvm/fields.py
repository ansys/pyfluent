"""Scalar and vector field storage on the staggered Cartesian mesh."""

from __future__ import annotations

from dataclasses import dataclass, field
from math import isfinite
from numbers import Real

import numpy as np
from numpy.typing import ArrayLike

from .mesh import CartesianMesh, FloatArray


def _as_finite_array(values: ArrayLike, shape: tuple[int, int], name: str) -> FloatArray:
    """Copy numeric values into a finite float array of the requested shape."""
    try:
        array = np.asarray(values, dtype=np.float64)
    except (TypeError, ValueError) as error:
        raise TypeError(f"{name} values must be numeric") from error
    if array.shape != shape:
        raise ValueError(f"{name} values must have shape {shape}, got {array.shape}")
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} values must all be finite")
    return array.copy()


@dataclass(slots=True)
class ScalarField:
    """A named scalar array located at cell centers or one face orientation."""

    mesh: CartesianMesh
    name: str
    location: str = "cell_center"
    initial_value: float = 0.0
    values: FloatArray = field(init=False, repr=False)

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("field name must be a non-empty string")
        shape = self.mesh.shape_for_location(self.location)
        if isinstance(self.initial_value, bool) or not isinstance(self.initial_value, Real):
            raise TypeError("initial_value must be a finite number")
        if not isfinite(self.initial_value):
            raise ValueError("initial_value must be a finite number")
        self.initial_value = float(self.initial_value)
        self.values = np.full(shape, self.initial_value, dtype=np.float64)

    def set_values(self, values: ArrayLike) -> None:
        """Replace field contents after checking shape, numeric type, and finiteness."""
        self.values = _as_finite_array(values, self.values.shape, self.name)


@dataclass(slots=True)
class VectorField:
    """A 2D vector field with x/y components on their MAC face locations."""

    mesh: CartesianMesh
    name: str = "velocity"
    initial_value: tuple[float, float] = (0.0, 0.0)
    u: ScalarField = field(init=False)
    v: ScalarField = field(init=False)

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("field name must be a non-empty string")
        if len(self.initial_value) != 2:
            raise ValueError("initial_value must contain x and y components")
        components = tuple(self.initial_value)
        if any(
            isinstance(value, bool) or not isinstance(value, Real) or not isfinite(value)
            for value in components
        ):
            raise ValueError("initial velocity components must be finite numbers")
        self.initial_value = (float(components[0]), float(components[1]))
        self.u = ScalarField(self.mesh, f"{self.name}.u", "x_face", self.initial_value[0])
        self.v = ScalarField(self.mesh, f"{self.name}.v", "y_face", self.initial_value[1])

    def set_values(self, u_values: ArrayLike, v_values: ArrayLike) -> None:
        """Replace both components, validating both before changing either one."""
        new_u = _as_finite_array(u_values, self.u.values.shape, self.u.name)
        new_v = _as_finite_array(v_values, self.v.values.shape, self.v.name)
        self.u.values = new_u
        self.v.values = new_v