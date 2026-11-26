"""Finite-volume operators for cell scalars and MAC-staggered velocities."""

from __future__ import annotations

from collections.abc import Mapping
from numbers import Real
from typing import Literal, TypeAlias

import numpy as np
from numpy.typing import ArrayLike

from .fields import ScalarField, VectorField
from .mesh import BOUNDARY_NAMES, CartesianMesh, FloatArray

BoundaryValues: TypeAlias = Mapping[str, ArrayLike | float]
FaceArrays: TypeAlias = tuple[FloatArray, FloatArray]


def _cell_values(field: ScalarField) -> FloatArray:
    """Check that an operator received a finite cell-centered scalar field."""
    if not isinstance(field, ScalarField):
        raise TypeError("field must be a ScalarField")
    if field.location != "cell_center":
        raise ValueError("operator requires a cell-centered scalar field")
    expected_shape = field.mesh.shape_for_location("cell_center")
    values = np.asarray(field.values, dtype=np.float64)
    if values.shape != expected_shape:
        raise ValueError(f"field values must have shape {expected_shape}")
    if not np.all(np.isfinite(values)):
        raise ValueError("field values must all be finite")
    return values


def _velocity_values(velocity: VectorField, mesh: CartesianMesh) -> FaceArrays:
    """Check that velocity components belong to the same mesh and are finite."""
    if not isinstance(velocity, VectorField):
        raise TypeError("velocity must be a VectorField")
    if velocity.mesh != mesh:
        raise ValueError("scalar and velocity fields must use the same mesh")
    u_values = np.asarray(velocity.u.values, dtype=np.float64)
    v_values = np.asarray(velocity.v.values, dtype=np.float64)
    if u_values.shape != mesh.shape_for_location("x_face"):
        raise ValueError("u values have an invalid shape")
    if v_values.shape != mesh.shape_for_location("y_face"):
        raise ValueError("v values have an invalid shape")
    if not np.all(np.isfinite(u_values)) or not np.all(np.isfinite(v_values)):
        raise ValueError("velocity values must all be finite")
    return u_values, v_values


def _boundary_arrays(
    mesh: CartesianMesh, boundary_values: BoundaryValues | None
) -> dict[str, FloatArray]:
    """Expand scalar or side-array boundary values to one value per face."""
    if boundary_values is None:
        return {}
    if not isinstance(boundary_values, Mapping):
        raise TypeError("boundary_values must be a mapping of side names to values")
    unknown_sides = set(boundary_values) - set(BOUNDARY_NAMES)
    if unknown_sides:
        raise ValueError(f"unknown boundary names: {sorted(unknown_sides)}")

    boundary_lengths = {
        "west": mesh.ny,
        "east": mesh.ny,
        "south": mesh.nx,
        "north": mesh.nx,
    }
    normalized: dict[str, FloatArray] = {}
    for side, boundary_value in boundary_values.items():
        try:
            values = np.asarray(boundary_value, dtype=np.float64)
        except (TypeError, ValueError) as error:
            raise TypeError(f"{side} boundary values must be numeric") from error
        if values.ndim == 0:
            values = np.full(boundary_lengths[side], float(values), dtype=np.float64)
        elif values.shape != (boundary_lengths[side],):
            raise ValueError(
                f"{side} boundary values must be scalar or have shape "
                f"({boundary_lengths[side]},)"
            )
        if not np.all(np.isfinite(values)):
            raise ValueError(f"{side} boundary values must all be finite")
        normalized[side] = values.copy()
    return normalized


def _lower_boundary_gradient(
    boundary_value: FloatArray,
    first_cell: FloatArray,
    spacing: float,
    second_cell: FloatArray | None,
    third_cell: FloatArray | None,
) -> FloatArray:
    """Reconstruct the positive-axis gradient at a lower boundary face."""
    if second_cell is None:
        return (first_cell - boundary_value) / (0.5 * spacing)
    if third_cell is not None:
        # A cubic through the face value and three cell centers keeps the
        # boundary flux accurate enough for a second-order cell Laplacian.
        return (
            (-46.0 / 15.0) * boundary_value
            + (15.0 / 4.0) * first_cell
            - (5.0 / 6.0) * second_cell
            + (3.0 / 20.0) * third_cell
        ) / spacing
    return (-8.0 * boundary_value + 9.0 * first_cell - second_cell) / (3.0 * spacing)


def _upper_boundary_gradient(
    boundary_value: FloatArray,
    last_cell: FloatArray,
    spacing: float,
    second_cell: FloatArray | None,
    third_cell: FloatArray | None,
) -> FloatArray:
    """Reconstruct the positive-axis gradient at an upper boundary face."""
    if second_cell is None:
        return (boundary_value - last_cell) / (0.5 * spacing)
    if third_cell is not None:
        return (
            (46.0 / 15.0) * boundary_value
            - (15.0 / 4.0) * last_cell
            + (5.0 / 6.0) * second_cell
            - (3.0 / 20.0) * third_cell
        ) / spacing
    return (8.0 * boundary_value - 9.0 * last_cell + second_cell) / (3.0 * spacing)


def _lower_adjacent_face_gradient(
    boundary_value: FloatArray,
    first_cell: FloatArray,
    second_cell: FloatArray,
    third_cell: FloatArray,
    spacing: float,
) -> FloatArray:
    """Reconstruct the gradient one cell inward from a lower boundary."""
    return (
        (2.0 / 15.0) * boundary_value
        - (5.0 / 4.0) * first_cell
        + (7.0 / 6.0) * second_cell
        - (1.0 / 20.0) * third_cell
    ) / spacing


def _upper_adjacent_face_gradient(
    boundary_value: FloatArray,
    last_cell: FloatArray,
    second_cell: FloatArray,
    third_cell: FloatArray,
    spacing: float,
) -> FloatArray:
    """Reconstruct the gradient one cell inward from an upper boundary."""
    return (
        (-2.0 / 15.0) * boundary_value
        + (5.0 / 4.0) * last_cell
        - (7.0 / 6.0) * second_cell
        + (1.0 / 20.0) * third_cell
    ) / spacing


def interpolate_to_faces(
    field: ScalarField, boundary_values: BoundaryValues | None = None
) -> FaceArrays:
    """Interpolate a cell scalar to x/y faces using central averaging.

    Internal face values are arithmetic averages of adjacent cell values.
    Boundary faces use the nearest cell value by default (zero-gradient
    extrapolation); optional side values replace that default.
    """
    cell_values = _cell_values(field)
    mesh = field.mesh
    boundaries = _boundary_arrays(mesh, boundary_values)
    x_faces = np.empty(mesh.shape_for_location("x_face"), dtype=np.float64)
    y_faces = np.empty(mesh.shape_for_location("y_face"), dtype=np.float64)

    x_faces[:, 1:-1] = 0.5 * (cell_values[:, :-1] + cell_values[:, 1:])
    x_faces[:, 0] = cell_values[:, 0]
    x_faces[:, -1] = cell_values[:, -1]
    y_faces[1:-1, :] = 0.5 * (cell_values[:-1, :] + cell_values[1:, :])
    y_faces[0, :] = cell_values[0, :]
    y_faces[-1, :] = cell_values[-1, :]

    if "west" in boundaries:
        x_faces[:, 0] = boundaries["west"]
    if "east" in boundaries:
        x_faces[:, -1] = boundaries["east"]
    if "south" in boundaries:
        y_faces[0, :] = boundaries["south"]
    if "north" in boundaries:
        y_faces[-1, :] = boundaries["north"]
    return x_faces, y_faces


def face_gradient(
    field: ScalarField, boundary_values: BoundaryValues | None = None
) -> FaceArrays:
    """Compute `(dphi/dx, dphi/dy)` at vertical and horizontal faces.

    Internal gradients use a four-cell stencil where available, with
    boundary-aware one-sided stencils near specified Dirichlet sides. Unless a
    boundary value is supplied, the boundary-normal gradient is zero. With only
    one or two cells along an axis, lower-order stencils are used as available.
    """
    cell_values = _cell_values(field)
    mesh = field.mesh
    boundaries = _boundary_arrays(mesh, boundary_values)
    gradient_x = np.zeros(mesh.shape_for_location("x_face"), dtype=np.float64)
    gradient_y = np.zeros(mesh.shape_for_location("y_face"), dtype=np.float64)

    gradient_x[:, 1:-1] = (cell_values[:, 1:] - cell_values[:, :-1]) / mesh.dx
    gradient_y[1:-1, :] = (cell_values[1:, :] - cell_values[:-1, :]) / mesh.dy

    if mesh.nx >= 4:
        # A symmetric four-cell stencil gives face gradients with smaller
        # errors; the following boundary reconstructions supply matching
        # accuracy for the first and last interior faces.
        gradient_x[:, 2:-2] = (
            27.0 * (cell_values[:, 2:-1] - cell_values[:, 1:-2])
            - (cell_values[:, 3:] - cell_values[:, :-3])
        ) / (24.0 * mesh.dx)
    if mesh.ny >= 4:
        gradient_y[2:-2, :] = (
            27.0 * (cell_values[2:-1, :] - cell_values[1:-2, :])
            - (cell_values[3:, :] - cell_values[:-3, :])
        ) / (24.0 * mesh.dy)

    if "west" in boundaries and mesh.nx >= 3:
        gradient_x[:, 1] = _lower_adjacent_face_gradient(
            boundaries["west"],
            cell_values[:, 0],
            cell_values[:, 1],
            cell_values[:, 2],
            mesh.dx,
        )
    if "east" in boundaries and mesh.nx >= 3:
        gradient_x[:, -2] = _upper_adjacent_face_gradient(
            boundaries["east"],
            cell_values[:, -1],
            cell_values[:, -2],
            cell_values[:, -3],
            mesh.dx,
        )
    if "south" in boundaries and mesh.ny >= 3:
        gradient_y[1, :] = _lower_adjacent_face_gradient(
            boundaries["south"],
            cell_values[0, :],
            cell_values[1, :],
            cell_values[2, :],
            mesh.dy,
        )
    if "north" in boundaries and mesh.ny >= 3:
        gradient_y[-2, :] = _upper_adjacent_face_gradient(
            boundaries["north"],
            cell_values[-1, :],
            cell_values[-2, :],
            cell_values[-3, :],
            mesh.dy,
        )

    if "west" in boundaries:
        second_cell = cell_values[:, 1] if mesh.nx > 1 else None
        third_cell = cell_values[:, 2] if mesh.nx > 2 else None
        gradient_x[:, 0] = _lower_boundary_gradient(
            boundaries["west"], cell_values[:, 0], mesh.dx, second_cell, third_cell
        )
    if "east" in boundaries:
        second_cell = cell_values[:, -2] if mesh.nx > 1 else None
        third_cell = cell_values[:, -3] if mesh.nx > 2 else None
        gradient_x[:, -1] = _upper_boundary_gradient(
            boundaries["east"], cell_values[:, -1], mesh.dx, second_cell, third_cell
        )
    if "south" in boundaries:
        second_cell = cell_values[1, :] if mesh.ny > 1 else None
        third_cell = cell_values[2, :] if mesh.ny > 2 else None
        gradient_y[0, :] = _lower_boundary_gradient(
            boundaries["south"], cell_values[0, :], mesh.dy, second_cell, third_cell
        )
    if "north" in boundaries:
        second_cell = cell_values[-2, :] if mesh.ny > 1 else None
        third_cell = cell_values[-3, :] if mesh.ny > 2 else None
        gradient_y[-1, :] = _upper_boundary_gradient(
            boundaries["north"], cell_values[-1, :], mesh.dy, second_cell, third_cell
        )
    return gradient_x, gradient_y


def divergence(velocity: VectorField) -> FloatArray:
    """Return the finite-volume divergence of face velocity in each cell.

    The face-normal velocity is multiplied by its face area, and the net
    outward flux is divided by cell area. This is the discrete continuity
    operator used by the later projection step.
    """
    if not isinstance(velocity, VectorField):
        raise TypeError("velocity must be a VectorField")
    mesh = velocity.mesh
    u_values, v_values = _velocity_values(velocity, mesh)
    net_outward_flux = (
        (u_values[:, 1:] - u_values[:, :-1]) * mesh.u_face_area
        + (v_values[1:, :] - v_values[:-1, :]) * mesh.v_face_area
    )
    return net_outward_flux / mesh.cell_area


def _divergence_of_face_fluxes(
    mesh: CartesianMesh, flux_x: FloatArray, flux_y: FloatArray
) -> FloatArray:
    """Convert positive-coordinate face fluxes to cell-centered divergence."""
    net_outward_flux = (
        (flux_x[:, 1:] - flux_x[:, :-1]) * mesh.u_face_area
        + (flux_y[1:, :] - flux_y[:-1, :]) * mesh.v_face_area
    )
    return net_outward_flux / mesh.cell_area


def diffusive_fluxes(
    field: ScalarField,
    diffusivity: float = 1.0,
    boundary_values: BoundaryValues | None = None,
) -> FaceArrays:
    """Return face fluxes `diffusivity * grad(field)` on the MAC mesh.

    Diffusivity is constant over the domain. Missing boundary values imply
    zero normal diffusive flux, which is the homogeneous Neumann condition.
    """
    if isinstance(diffusivity, bool) or not isinstance(diffusivity, Real):
        raise TypeError("diffusivity must be a finite non-negative number")
    if not np.isfinite(diffusivity) or diffusivity < 0.0:
        raise ValueError("diffusivity must be a finite non-negative number")
    gradient_x, gradient_y = face_gradient(field, boundary_values)
    return diffusivity * gradient_x, diffusivity * gradient_y


def diffusion_operator(
    field: ScalarField,
    diffusivity: float = 1.0,
    boundary_values: BoundaryValues | None = None,
) -> FloatArray:
    """Return the conservative cell-centered `div(diffusivity * grad(phi))`.

    ``boundary_values`` supplies Dirichlet values on any specified side;
    unspecified sides have zero normal diffusive flux.
    """
    flux_x, flux_y = diffusive_fluxes(field, diffusivity, boundary_values)
    return _divergence_of_face_fluxes(field.mesh, flux_x, flux_y)


def convective_fluxes(
    field: ScalarField,
    velocity: VectorField,
    scheme: Literal["central", "upwind"] = "upwind",
    boundary_values: BoundaryValues | None = None,
) -> FaceArrays:
    """Return conservative face fluxes `velocity * field`.

    ``central`` uses arithmetic interpolation on internal faces. ``upwind``
    selects the upstream cell value based on face-normal velocity. At an
    inflow boundary, a supplied boundary value is used; otherwise the nearest
    cell value is extrapolated. The latter is a convenience default, not a
    replacement for a physically specified inflow condition.
    """
    cell_values = _cell_values(field)
    u_values, v_values = _velocity_values(velocity, field.mesh)
    mesh = field.mesh
    boundaries = _boundary_arrays(mesh, boundary_values)

    if scheme == "central":
        face_values_x, face_values_y = interpolate_to_faces(field, boundaries)
    elif scheme == "upwind":
        face_values_x = np.empty(mesh.shape_for_location("x_face"), dtype=np.float64)
        face_values_y = np.empty(mesh.shape_for_location("y_face"), dtype=np.float64)

        # Positive x/y velocity enters an internal face from its lower-index cell.
        face_values_x[:, 1:-1] = np.where(
            u_values[:, 1:-1] >= 0.0, cell_values[:, :-1], cell_values[:, 1:]
        )
        face_values_y[1:-1, :] = np.where(
            v_values[1:-1, :] >= 0.0, cell_values[:-1, :], cell_values[1:, :]
        )

        face_values_x[:, 0] = cell_values[:, 0]
        face_values_x[:, -1] = cell_values[:, -1]
        face_values_y[0, :] = cell_values[0, :]
        face_values_y[-1, :] = cell_values[-1, :]

        # At west/south boundaries inward flow points in the positive axis direction.
        if "west" in boundaries:
            inflow = u_values[:, 0] > 0.0
            face_values_x[inflow, 0] = boundaries["west"][inflow]
        if "east" in boundaries:
            inflow = u_values[:, -1] < 0.0
            face_values_x[inflow, -1] = boundaries["east"][inflow]
        if "south" in boundaries:
            inflow = v_values[0, :] > 0.0
            face_values_y[0, inflow] = boundaries["south"][inflow]
        if "north" in boundaries:
            inflow = v_values[-1, :] < 0.0
            face_values_y[-1, inflow] = boundaries["north"][inflow]
    else:
        raise ValueError("scheme must be 'central' or 'upwind'")

    return u_values * face_values_x, v_values * face_values_y


def convection_operator(
    field: ScalarField,
    velocity: VectorField,
    scheme: Literal["central", "upwind"] = "upwind",
    boundary_values: BoundaryValues | None = None,
) -> FloatArray:
    """Return conservative cell-centered `div(velocity * field)`.

    Face fluxes are multiplied by face areas and differenced before division
    by cell area, so the sum over cells telescopes to the domain-boundary flux.
    """
    flux_x, flux_y = convective_fluxes(field, velocity, scheme, boundary_values)
    return _divergence_of_face_fluxes(field.mesh, flux_x, flux_y)