"""Sparse staggered-grid momentum prediction for a transient projection step."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from numbers import Real

import numpy as np
from scipy.sparse import coo_matrix, csr_matrix
from scipy.sparse.linalg import spsolve

from .boundary_conditions import (
    BoundaryConditions,
    FixedValue,
    MovingWall,
    NoSlipWall,
)
from .fields import ScalarField, VectorField
from .mesh import BOUNDARY_NAMES, CartesianMesh, FloatArray
from .operators import face_gradient

WallVelocities = dict[str, tuple[float, float]]


@dataclass(frozen=True, slots=True)
class MomentumAssembly:
    """Two sparse component systems and terms used to construct their RHS.

    Boundary-aligned normal velocity faces are stored in ``fixed_u`` and
    ``fixed_v``. The matrix unknowns are only the interior component values:
    ``u`` has shape `(ny, nx - 1)` and ``v`` has shape `(ny - 1, nx)`.
    Keeping the convection and pressure-gradient terms here makes each
    assembled equation inspectable in tests and during debugging.
    """

    mesh: CartesianMesh
    u_matrix: csr_matrix
    u_rhs: FloatArray
    v_matrix: csr_matrix
    v_rhs: FloatArray
    u_unknown_shape: tuple[int, int]
    v_unknown_shape: tuple[int, int]
    fixed_u: FloatArray
    fixed_v: FloatArray
    u_convection: FloatArray
    v_convection: FloatArray
    u_pressure_gradient: FloatArray
    v_pressure_gradient: FloatArray


@dataclass(frozen=True, slots=True)
class MomentumPrediction:
    """Predicted face velocities and normalized linear-system residuals."""

    velocity: VectorField
    u_relative_residual: float
    v_relative_residual: float


def _validate_positive_parameter(name: str, value: float, allow_zero: bool = False) -> float:
    """Validate and normalize a finite positive physical/solver parameter."""
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a finite number")
    if not isfinite(value) or value < 0.0 or (value == 0.0 and not allow_zero):
        qualifier = "non-negative" if allow_zero else "positive"
        raise ValueError(f"{name} must be finite and {qualifier}")
    return float(value)


def _wall_velocities(boundary_conditions: BoundaryConditions) -> WallVelocities:
    """Get a two-component prescribed velocity for every physical wall."""
    if not isinstance(boundary_conditions, BoundaryConditions):
        raise TypeError("boundary_conditions must be BoundaryConditions")

    wall_values: WallVelocities = {}
    for side in BOUNDARY_NAMES:
        try:
            condition = boundary_conditions.get("velocity", side)
        except KeyError as error:
            raise ValueError(f"missing velocity boundary condition for {side}") from error

        if isinstance(condition, (NoSlipWall, MovingWall)):
            wall_values[side] = condition.velocity
        elif isinstance(condition, FixedValue) and isinstance(condition.value, tuple):
            wall_values[side] = condition.value
        else:
            raise ValueError(
                f"velocity boundary {side} must prescribe both velocity components"
            )
    return wall_values


def _staggered_upwind_convection(
    u: FloatArray,
    v: FloatArray,
    walls: WallVelocities,
    mesh: CartesianMesh,
) -> tuple[FloatArray, FloatArray]:
    """Compute conservative upwind advection on u/v control volumes.

    Advecting velocities at the cross-component locations are linearly
    interpolated. The transported component uses first-order upwind values;
    tangential wall velocities supply its boundary-face values.
    """
    u_adv_x = 0.5 * (u[:, :-1] + u[:, 1:])
    u_at_x_faces = np.where(u_adv_x >= 0.0, u[:, :-1], u[:, 1:])
    u_flux_x = u_adv_x * u_at_x_faces

    v_adv_at_u_y_faces = 0.5 * (v[:, :-1] + v[:, 1:])
    u_at_y_faces = np.empty((mesh.ny + 1, mesh.nx - 1), dtype=np.float64)
    u_at_y_faces[1:-1, :] = np.where(
        v_adv_at_u_y_faces[1:-1, :] >= 0.0,
        u[:-1, 1:-1],
        u[1:, 1:-1],
    )
    u_at_y_faces[0, :] = np.where(
        v_adv_at_u_y_faces[0, :] >= 0.0, walls["south"][0], u[0, 1:-1]
    )
    u_at_y_faces[-1, :] = np.where(
        v_adv_at_u_y_faces[-1, :] >= 0.0, u[-1, 1:-1], walls["north"][0]
    )
    u_flux_y = v_adv_at_u_y_faces * u_at_y_faces
    u_convection = (
        (u_flux_x[:, 1:] - u_flux_x[:, :-1]) * mesh.u_face_area
        + (u_flux_y[1:, :] - u_flux_y[:-1, :]) * mesh.v_face_area
    ) / mesh.cell_area

    v_adv_y = 0.5 * (v[:-1, :] + v[1:, :])
    v_at_y_faces = np.where(v_adv_y >= 0.0, v[:-1, :], v[1:, :])
    v_flux_y = v_adv_y * v_at_y_faces

    u_adv_at_v_x_faces = 0.5 * (u[:-1, :] + u[1:, :])
    v_at_x_faces = np.empty((mesh.ny - 1, mesh.nx + 1), dtype=np.float64)
    v_at_x_faces[:, 1:-1] = np.where(
        u_adv_at_v_x_faces[:, 1:-1] >= 0.0,
        v[1:-1, :-1],
        v[1:-1, 1:],
    )
    v_at_x_faces[:, 0] = np.where(
        u_adv_at_v_x_faces[:, 0] >= 0.0, walls["west"][1], v[1:-1, 0]
    )
    v_at_x_faces[:, -1] = np.where(
        u_adv_at_v_x_faces[:, -1] >= 0.0, v[1:-1, -1], walls["east"][1]
    )
    v_flux_x = u_adv_at_v_x_faces * v_at_x_faces
    v_convection = (
        (v_flux_x[:, 1:] - v_flux_x[:, :-1]) * mesh.u_face_area
        + (v_flux_y[1:, :] - v_flux_y[:-1, :]) * mesh.v_face_area
    ) / mesh.cell_area
    return u_convection, v_convection


def _build_u_matrix(
    mesh: CartesianMesh,
    old_u: FloatArray,
    fixed_u: FloatArray,
    convection: FloatArray,
    pressure_gradient: FloatArray,
    walls: WallVelocities,
    density: float,
    viscosity: float,
    time_step: float,
) -> tuple[csr_matrix, FloatArray, tuple[int, int]]:
    """Assemble `rho/dt - mu*laplacian` for interior u control volumes."""
    unknown_shape = (mesh.ny, mesh.nx - 1)
    unknown_count = unknown_shape[0] * unknown_shape[1]
    storage = density / time_step
    x_diffusion = viscosity / mesh.dx**2
    y_diffusion = viscosity / mesh.dy**2
    rows: list[int] = []
    columns: list[int] = []
    coefficients: list[float] = []
    rhs = np.empty(unknown_count, dtype=np.float64)

    for row_index in range(mesh.ny):
        for face_index in range(1, mesh.nx):
            row = row_index * (mesh.nx - 1) + face_index - 1
            diagonal = storage
            rhs[row] = (
                storage * old_u[row_index, face_index]
                - density * convection[row_index, face_index - 1]
                - pressure_gradient[row_index, face_index - 1]
            )

            def connect(neighbor: int | None, weight: float, boundary_value: float = 0.0) -> None:
                nonlocal diagonal
                if weight == 0.0:
                    return
                diagonal += weight
                if neighbor is None:
                    rhs[row] += weight * boundary_value
                else:
                    rows.append(row)
                    columns.append(neighbor)
                    coefficients.append(-weight)

            west = (
                row_index * (mesh.nx - 1) + face_index - 2
                if face_index > 1
                else None
            )
            connect(west, x_diffusion, fixed_u[row_index, 0])
            east = (
                row_index * (mesh.nx - 1) + face_index
                if face_index < mesh.nx - 1
                else None
            )
            connect(east, x_diffusion, fixed_u[row_index, -1])

            south = (row_index - 1) * (mesh.nx - 1) + face_index - 1 if row_index > 0 else None
            connect(
                south,
                y_diffusion if row_index > 0 else 2.0 * y_diffusion,
                walls["south"][0],
            )
            north = (
                (row_index + 1) * (mesh.nx - 1) + face_index - 1
                if row_index < mesh.ny - 1
                else None
            )
            connect(
                north,
                y_diffusion if row_index < mesh.ny - 1 else 2.0 * y_diffusion,
                walls["north"][0],
            )
            rows.append(row)
            columns.append(row)
            coefficients.append(diagonal)

    matrix = coo_matrix(
        (coefficients, (rows, columns)), shape=(unknown_count, unknown_count)
    ).tocsr()
    return matrix, rhs, unknown_shape


def _build_v_matrix(
    mesh: CartesianMesh,
    old_v: FloatArray,
    fixed_v: FloatArray,
    convection: FloatArray,
    pressure_gradient: FloatArray,
    walls: WallVelocities,
    density: float,
    viscosity: float,
    time_step: float,
) -> tuple[csr_matrix, FloatArray, tuple[int, int]]:
    """Assemble `rho/dt - mu*laplacian` for interior v control volumes."""
    unknown_shape = (mesh.ny - 1, mesh.nx)
    unknown_count = unknown_shape[0] * unknown_shape[1]
    storage = density / time_step
    x_diffusion = viscosity / mesh.dx**2
    y_diffusion = viscosity / mesh.dy**2
    rows: list[int] = []
    columns: list[int] = []
    coefficients: list[float] = []
    rhs = np.empty(unknown_count, dtype=np.float64)

    for face_index in range(1, mesh.ny):
        for column_index in range(mesh.nx):
            row = (face_index - 1) * mesh.nx + column_index
            diagonal = storage
            rhs[row] = (
                storage * old_v[face_index, column_index]
                - density * convection[face_index - 1, column_index]
                - pressure_gradient[face_index - 1, column_index]
            )

            def connect(neighbor: int | None, weight: float, boundary_value: float = 0.0) -> None:
                nonlocal diagonal
                if weight == 0.0:
                    return
                diagonal += weight
                if neighbor is None:
                    rhs[row] += weight * boundary_value
                else:
                    rows.append(row)
                    columns.append(neighbor)
                    coefficients.append(-weight)

            west = row - 1 if column_index > 0 else None
            connect(west, x_diffusion if column_index > 0 else 2.0 * x_diffusion, walls["west"][1])
            east = row + 1 if column_index < mesh.nx - 1 else None
            connect(east, x_diffusion if column_index < mesh.nx - 1 else 2.0 * x_diffusion, walls["east"][1])

            south = row - mesh.nx if face_index > 1 else None
            connect(south, y_diffusion, fixed_v[0, column_index])
            north = row + mesh.nx if face_index < mesh.ny - 1 else None
            connect(north, y_diffusion, fixed_v[-1, column_index])
            rows.append(row)
            columns.append(row)
            coefficients.append(diagonal)

    matrix = coo_matrix(
        (coefficients, (rows, columns)), shape=(unknown_count, unknown_count)
    ).tocsr()
    return matrix, rhs, unknown_shape


class MomentumPredictor:
    """Assemble and solve one explicit-convection/implicit-diffusion step.

    The predicted components satisfy, on their respective staggered control
    volumes,

    `rho/dt * (u* - u_n) = -rho div(u_n u_n) - dp/dx + mu laplacian(u*)`,

    with the analogous equation for `v`. Convection is first-order upwind and
    explicit. Diffusion is implicit; prescribed wall values contribute to the
    matrix right-hand side. Pressure is the supplied cell-centered field (this
    milestone does not compute pressure correction).
    """

    def __init__(self, density: float, viscosity: float, time_step: float) -> None:
        """Create a predictor for one fluid and a fixed transient time step."""
        self.density = _validate_positive_parameter("density", density)
        self.viscosity = _validate_positive_parameter("viscosity", viscosity, allow_zero=True)
        self.time_step = _validate_positive_parameter("time_step", time_step)

    def assemble(
        self,
        velocity: VectorField,
        pressure: ScalarField,
        boundary_conditions: BoundaryConditions,
    ) -> MomentumAssembly:
        """Build sparse component systems without modifying input fields.

        Velocity boundary conditions must prescribe both components on each
        side. The boundary-aligned normal components are fixed directly; the
        tangential components enter diffusion and convection at the adjacent
        staggered control-volume faces.
        """
        if not isinstance(velocity, VectorField):
            raise TypeError("velocity must be a VectorField")
        if not isinstance(pressure, ScalarField):
            raise TypeError("pressure must be a ScalarField")
        mesh = velocity.mesh
        if pressure.mesh != mesh or pressure.location != "cell_center":
            raise ValueError("pressure must be cell-centered on the velocity mesh")
        if mesh.nx < 2 or mesh.ny < 2:
            raise ValueError("momentum prediction requires at least two cells per direction")

        walls = _wall_velocities(boundary_conditions)
        old_u = np.asarray(velocity.u.values, dtype=np.float64).copy()
        old_v = np.asarray(velocity.v.values, dtype=np.float64).copy()
        if old_u.shape != mesh.shape_for_location("x_face"):
            raise ValueError("u values have an invalid shape")
        if old_v.shape != mesh.shape_for_location("y_face"):
            raise ValueError("v values have an invalid shape")
        if not np.all(np.isfinite(old_u)) or not np.all(np.isfinite(old_v)):
            raise ValueError("velocity values must all be finite")
        fixed_u = old_u.copy()
        fixed_v = old_v.copy()

        # On a MAC grid, u is stored on the west/east walls and v on the
        # south/north walls. Tangential values are applied to adjacent CV faces.
        fixed_u[:, 0] = walls["west"][0]
        fixed_u[:, -1] = walls["east"][0]
        fixed_v[0, :] = walls["south"][1]
        fixed_v[-1, :] = walls["north"][1]

        pressure_gradient_x, pressure_gradient_y = face_gradient(pressure)
        u_convection, v_convection = _staggered_upwind_convection(
            fixed_u, fixed_v, walls, mesh
        )
        u_matrix, u_rhs, u_shape = _build_u_matrix(
            mesh,
            old_u,
            fixed_u,
            u_convection,
            pressure_gradient_x[:, 1:-1],
            walls,
            self.density,
            self.viscosity,
            self.time_step,
        )
        v_matrix, v_rhs, v_shape = _build_v_matrix(
            mesh,
            old_v,
            fixed_v,
            v_convection,
            pressure_gradient_y[1:-1, :],
            walls,
            self.density,
            self.viscosity,
            self.time_step,
        )
        return MomentumAssembly(
            mesh=mesh,
            u_matrix=u_matrix,
            u_rhs=u_rhs,
            v_matrix=v_matrix,
            v_rhs=v_rhs,
            u_unknown_shape=u_shape,
            v_unknown_shape=v_shape,
            fixed_u=fixed_u,
            fixed_v=fixed_v,
            u_convection=u_convection,
            v_convection=v_convection,
            u_pressure_gradient=pressure_gradient_x[:, 1:-1].copy(),
            v_pressure_gradient=pressure_gradient_y[1:-1, :].copy(),
        )

    def solve(self, assembly: MomentumAssembly) -> MomentumPrediction:
        """Solve both sparse systems and restore fixed boundary-face values."""
        if not isinstance(assembly, MomentumAssembly):
            raise TypeError("assembly must be a MomentumAssembly")
        u_unknowns = np.asarray(spsolve(assembly.u_matrix, assembly.u_rhs), dtype=np.float64)
        v_unknowns = np.asarray(spsolve(assembly.v_matrix, assembly.v_rhs), dtype=np.float64)
        if not np.all(np.isfinite(u_unknowns)) or not np.all(np.isfinite(v_unknowns)):
            raise RuntimeError("momentum linear solve produced non-finite values")

        predicted_u = assembly.fixed_u.copy()
        predicted_v = assembly.fixed_v.copy()
        predicted_u[:, 1:-1] = u_unknowns.reshape(assembly.u_unknown_shape)
        predicted_v[1:-1, :] = v_unknowns.reshape(assembly.v_unknown_shape)
        predicted_velocity = VectorField(assembly.mesh, name="predicted_velocity")
        predicted_velocity.set_values(predicted_u, predicted_v)

        return MomentumPrediction(
            velocity=predicted_velocity,
            u_relative_residual=_relative_residual(
                assembly.u_matrix, u_unknowns, assembly.u_rhs
            ),
            v_relative_residual=_relative_residual(
                assembly.v_matrix, v_unknowns, assembly.v_rhs
            ),
        )

    def predict(
        self,
        velocity: VectorField,
        pressure: ScalarField,
        boundary_conditions: BoundaryConditions,
    ) -> MomentumPrediction:
        """Assemble and solve one momentum-prediction step in a single call."""
        return self.solve(self.assemble(velocity, pressure, boundary_conditions))


def _relative_residual(matrix: csr_matrix, solution: FloatArray, rhs: FloatArray) -> float:
    """Return a stable normalized L2 residual for a solved sparse system."""
    residual = matrix @ solution - rhs
    return float(np.linalg.norm(residual) / max(float(np.linalg.norm(rhs)), 1.0))