"""Uniform Cartesian mesh geometry for a two-dimensional MAC grid."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from numbers import Integral, Real
from types import MappingProxyType
from typing import Mapping

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]
IndexArray = NDArray[np.intp]
BOUNDARY_NAMES = ("west", "east", "south", "north")


@dataclass(frozen=True, slots=True)
class CartesianMesh:
    """Uniform rectangular mesh with cell-centered pressure and MAC faces.

    Coordinates are exposed as one-dimensional axes and as `(x, y)` arrays.
    Array rows increase from south to north; columns increase from west to east.
    In two dimensions, ``cell_area`` is the cell volume per unit depth.
    """

    nx: int
    ny: int
    width: float = 1.0
    height: float = 1.0

    def __post_init__(self) -> None:
        for name in ("nx", "ny"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, Integral):
                raise TypeError(f"{name} must be a positive integer")
            if value <= 0:
                raise ValueError(f"{name} must be a positive integer")
            object.__setattr__(self, name, int(value))

        for name in ("width", "height"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, Real):
                raise TypeError(f"{name} must be a finite positive number")
            if not isfinite(value) or value <= 0:
                raise ValueError(f"{name} must be a finite positive number")
            object.__setattr__(self, name, float(value))

    @property
    def dx(self) -> float:
        """Uniform cell width."""
        return self.width / self.nx

    @property
    def dy(self) -> float:
        """Uniform cell height."""
        return self.height / self.ny

    @property
    def x_face_centers(self) -> FloatArray:
        """X coordinates of vertical faces, including both side walls."""
        return np.linspace(0.0, self.width, self.nx + 1, dtype=np.float64)

    @property
    def y_face_centers(self) -> FloatArray:
        """Y coordinates of horizontal faces, including both side walls."""
        return np.linspace(0.0, self.height, self.ny + 1, dtype=np.float64)

    @property
    def x_cell_centers(self) -> FloatArray:
        """X coordinates of cell centers."""
        return (np.arange(self.nx, dtype=np.float64) + 0.5) * self.dx

    @property
    def y_cell_centers(self) -> FloatArray:
        """Y coordinates of cell centers."""
        return (np.arange(self.ny, dtype=np.float64) + 0.5) * self.dy

    @property
    def cell_center_coordinates(self) -> tuple[FloatArray, FloatArray]:
        """Return `(x, y)` coordinate arrays, each with shape `(ny, nx)`."""
        return np.meshgrid(self.x_cell_centers, self.y_cell_centers, indexing="xy")

    @property
    def u_face_coordinates(self) -> tuple[FloatArray, FloatArray]:
        """Return `(x, y)` coordinates for u locations, shape `(ny, nx + 1)`."""
        return np.meshgrid(self.x_face_centers, self.y_cell_centers, indexing="xy")

    @property
    def v_face_coordinates(self) -> tuple[FloatArray, FloatArray]:
        """Return `(x, y)` coordinates for v locations, shape `(ny + 1, nx)`."""
        return np.meshgrid(self.x_cell_centers, self.y_face_centers, indexing="xy")

    @property
    def cell_area(self) -> float:
        """Area of one cell (volume per unit depth)."""
        return self.dx * self.dy

    @property
    def u_face_area(self) -> float:
        """Area per unit depth of a vertical face."""
        return self.dy

    @property
    def v_face_area(self) -> float:
        """Area per unit depth of a horizontal face."""
        return self.dx

    @property
    def cell_areas(self) -> FloatArray:
        """Cell areas as an array with shape `(ny, nx)`."""
        return np.full((self.ny, self.nx), self.cell_area, dtype=np.float64)

    @property
    def u_face_areas(self) -> FloatArray:
        """Vertical-face areas as an array with shape `(ny, nx + 1)`."""
        return np.full((self.ny, self.nx + 1), self.u_face_area, dtype=np.float64)

    @property
    def v_face_areas(self) -> FloatArray:
        """Horizontal-face areas as an array with shape `(ny + 1, nx)`."""
        return np.full((self.ny + 1, self.nx), self.v_face_area, dtype=np.float64)

    @property
    def boundary_face_indices(self) -> Mapping[str, tuple[IndexArray, IndexArray]]:
        """Return `(row_indices, column_indices)` for each boundary's normal faces.

        West/east indices address the u array; south/north indices address v.
        Each call returns new index arrays so callers cannot mutate mesh state.
        """
        rows = np.arange(self.ny, dtype=np.intp)
        columns = np.arange(self.nx, dtype=np.intp)
        return MappingProxyType(
            {
                "west": (rows.copy(), np.zeros(self.ny, dtype=np.intp)),
                "east": (rows.copy(), np.full(self.ny, self.nx, dtype=np.intp)),
                "south": (np.zeros(self.nx, dtype=np.intp), columns.copy()),
                "north": (np.full(self.nx, self.ny, dtype=np.intp), columns.copy()),
            }
        )

    @property
    def boundary_face_counts(self) -> Mapping[str, int]:
        """Number of geometric faces on each side of the mesh."""
        return MappingProxyType(
            {"west": self.ny, "east": self.ny, "south": self.nx, "north": self.nx}
        )

    @property
    def boundary_face_normals(self) -> Mapping[str, tuple[float, float]]:
        """Outward unit normals for west, east, south, and north boundaries."""
        return MappingProxyType(
            {
                "west": (-1.0, 0.0),
                "east": (1.0, 0.0),
                "south": (0.0, -1.0),
                "north": (0.0, 1.0),
            }
        )

    def shape_for_location(self, location: str) -> tuple[int, int]:
        """Return the array shape for a cell-center, x-face, or y-face field."""
        shapes = {
            "cell_center": (self.ny, self.nx),
            "x_face": (self.ny, self.nx + 1),
            "y_face": (self.ny + 1, self.nx),
        }
        try:
            return shapes[location]
        except KeyError as error:
            raise ValueError(
                "location must be 'cell_center', 'x_face', or 'y_face'"
            ) from error