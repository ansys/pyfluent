"""Sparse Neumann pressure-correction equation for the MAC projection method."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from numbers import Integral, Real

import numpy as np
from scipy.sparse import coo_matrix, csr_matrix, lil_matrix
from scipy.sparse.linalg import spsolve

from .fields import ScalarField, VectorField
from .mesh import CartesianMesh, FloatArray
from .operators import divergence


@dataclass(frozen=True, slots=True)
class PressureCorrectionAssembly:
    """Sparse positive-Neumann Poisson system with one pressure reference.

    The equation is `-laplacian(p') = -(rho/dt) * div(u*)`. The cell-centered
    finite-volume matrix omits normal-gradient contributions at domain walls.
    ``reference_cell`` is stored as `(row, column)` and has an identity row to
    remove the constant-pressure nullspace.
    """

    mesh: CartesianMesh
    matrix: csr_matrix
    rhs: FloatArray
    reference_cell: tuple[int, int]
    net_boundary_flux: float


@dataclass(frozen=True, slots=True)
class PressureCorrectionResult:
    """Cell-centered pressure correction and normalized sparse residual."""

    correction: ScalarField
    relative_residual: float
    net_boundary_flux: float


def _positive_parameter(name: str, value: float) -> float:
    """Validate a finite positive scalar used by the pressure equation."""
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a finite positive number")
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be a finite positive number")
    return float(value)


def _reference_index(
    reference_cell: tuple[int, int], mesh: CartesianMesh
) -> tuple[int, int, int]:
    """Validate a `(row, column)` gauge location and return its flat index."""
    if (
        not isinstance(reference_cell, tuple)
        or len(reference_cell) != 2
        or any(isinstance(index, bool) or not isinstance(index, Integral) for index in reference_cell)
    ):
        raise TypeError("reference_cell must be a (row, column) integer tuple")
    row, column = (int(index) for index in reference_cell)
    if not (0 <= row < mesh.ny and 0 <= column < mesh.nx):
        raise ValueError("reference_cell lies outside the mesh")
    return row, column, row * mesh.nx + column


def _net_boundary_flux(velocity: VectorField) -> tuple[float, float]:
    """Return outward flux and an absolute-flux scale for compatibility checks."""
    mesh = velocity.mesh
    u = np.asarray(velocity.u.values, dtype=np.float64)
    v = np.asarray(velocity.v.values, dtype=np.float64)
    if u.shape != mesh.shape_for_location("x_face"):
        raise ValueError("u values have an invalid shape")
    if v.shape != mesh.shape_for_location("y_face"):
        raise ValueError("v values have an invalid shape")
    if not np.all(np.isfinite(u)) or not np.all(np.isfinite(v)):
        raise ValueError("velocity values must all be finite")

    east_flux = float(np.sum(u[:, -1]) * mesh.u_face_area)
    west_flux = float(np.sum(u[:, 0]) * mesh.u_face_area)
    north_flux = float(np.sum(v[-1, :]) * mesh.v_face_area)
    south_flux = float(np.sum(v[0, :]) * mesh.v_face_area)
    net_flux = east_flux - west_flux + north_flux - south_flux
    flux_scale = abs(east_flux) + abs(west_flux) + abs(north_flux) + abs(south_flux)
    return net_flux, flux_scale


def _assemble_neumann_matrix(mesh: CartesianMesh, reference_index: int) -> csr_matrix:
    """Assemble `-laplacian` with zero normal flux on every outer face."""
    row_indices: list[int] = []
    column_indices: list[int] = []
    coefficients: list[float] = []
    inverse_dx_squared = 1.0 / mesh.dx**2
    inverse_dy_squared = 1.0 / mesh.dy**2

    for row in range(mesh.ny):
        for column in range(mesh.nx):
            cell_index = row * mesh.nx + column
            diagonal = 0.0
            neighbors = (
                (row, column - 1, inverse_dx_squared),
                (row, column + 1, inverse_dx_squared),
                (row - 1, column, inverse_dy_squared),
                (row + 1, column, inverse_dy_squared),
            )
            for neighbor_row, neighbor_column, coefficient in neighbors:
                if 0 <= neighbor_row < mesh.ny and 0 <= neighbor_column < mesh.nx:
                    neighbor_index = neighbor_row * mesh.nx + neighbor_column
                    row_indices.append(cell_index)
                    column_indices.append(neighbor_index)
                    coefficients.append(-coefficient)
                    diagonal += coefficient
            row_indices.append(cell_index)
            column_indices.append(cell_index)
            coefficients.append(diagonal)

    matrix = coo_matrix(
        (coefficients, (row_indices, column_indices)),
        shape=(mesh.nx * mesh.ny, mesh.nx * mesh.ny),
    ).tolil()

    # A pure-Neumann Poisson matrix has an arbitrary additive constant. Replace
    # one equation by p'(reference_cell) = 0 to choose a unique solution.
    matrix[reference_index, :] = 0.0
    matrix[reference_index, reference_index] = 1.0
    return matrix.tocsr()


class PressureCorrectionSolver:
    """Assemble and solve one homogeneous-Neumann pressure-correction system.

    The predicted velocity must have compatible net boundary flux. For a
    closed cavity the momentum predictor enforces zero normal wall velocity,
    so this condition is satisfied. A nonzero net flux cannot be removed by a
    homogeneous-Neumann correction without changing the boundary conditions,
    and is reported as an error instead of silently modifying the RHS.
    """

    def __init__(
        self,
        density: float,
        time_step: float,
        reference_cell: tuple[int, int] = (0, 0),
        compatibility_tolerance: float = 1e-10,
    ) -> None:
        """Create a solver with a pressure gauge and flux tolerance.

        ``reference_cell`` uses zero-based `(row, column)` indexing. Net flux is
        accepted when its magnitude is no greater than the tolerance times
        `max(total absolute boundary flux, 1)`.
        """
        self.density = _positive_parameter("density", density)
        self.time_step = _positive_parameter("time_step", time_step)
        self.compatibility_tolerance = _positive_parameter(
            "compatibility_tolerance", compatibility_tolerance
        )
        if (
            not isinstance(reference_cell, tuple)
            or len(reference_cell) != 2
            or any(
                isinstance(index, bool) or not isinstance(index, Integral)
                for index in reference_cell
            )
        ):
            raise TypeError("reference_cell must be a (row, column) integer tuple")
        self.reference_cell = tuple(int(index) for index in reference_cell)

    def assemble(self, predicted_velocity: VectorField) -> PressureCorrectionAssembly:
        """Build the pressure equation from predicted face-velocity divergence."""
        if not isinstance(predicted_velocity, VectorField):
            raise TypeError("predicted_velocity must be a VectorField")
        mesh = predicted_velocity.mesh
        row, column, reference_index = _reference_index(self.reference_cell, mesh)
        net_flux, flux_scale = _net_boundary_flux(predicted_velocity)
        if abs(net_flux) > self.compatibility_tolerance * max(flux_scale, 1.0):
            raise ValueError(
                "predicted velocity has incompatible net boundary flux "
                f"({net_flux:.6g}); homogeneous-Neumann correction requires zero net flux"
            )

        velocity_divergence = divergence(predicted_velocity)
        rhs = (-self.density / self.time_step * velocity_divergence).ravel().copy()
        matrix = _assemble_neumann_matrix(mesh, reference_index)
        rhs[reference_index] = 0.0
        return PressureCorrectionAssembly(
            mesh=mesh,
            matrix=matrix,
            rhs=rhs,
            reference_cell=(row, column),
            net_boundary_flux=net_flux,
        )

    def solve(self, assembly: PressureCorrectionAssembly) -> PressureCorrectionResult:
        """Solve the gauged sparse system and return a cell-centered correction."""
        if not isinstance(assembly, PressureCorrectionAssembly):
            raise TypeError("assembly must be a PressureCorrectionAssembly")
        solution = np.asarray(spsolve(assembly.matrix, assembly.rhs), dtype=np.float64)
        if not np.all(np.isfinite(solution)):
            raise RuntimeError("pressure-correction solve produced non-finite values")

        correction = ScalarField(assembly.mesh, name="pressure_correction")
        correction.set_values(solution.reshape((assembly.mesh.ny, assembly.mesh.nx)))
        residual = assembly.matrix @ solution - assembly.rhs
        relative_residual = float(
            np.linalg.norm(residual) / max(float(np.linalg.norm(assembly.rhs)), 1.0)
        )
        return PressureCorrectionResult(
            correction=correction,
            relative_residual=relative_residual,
            net_boundary_flux=assembly.net_boundary_flux,
        )

    def predict(self, predicted_velocity: VectorField) -> PressureCorrectionResult:
        """Assemble and solve one pressure correction in a single call."""
        return self.solve(self.assemble(predicted_velocity))