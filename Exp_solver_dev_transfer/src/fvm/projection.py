"""Velocity and pressure correction for one staggered-grid projection step."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from numbers import Real

import numpy as np

from .fields import ScalarField, VectorField
from .mesh import FloatArray
from .operators import divergence
from .pressure_correction import PressureCorrectionResult


@dataclass(frozen=True, slots=True)
class ProjectionResult:
    """Corrected fields and continuity diagnostics from one projection step."""

    velocity: VectorField
    pressure: ScalarField
    pressure_correction: ScalarField
    divergence_before: FloatArray
    divergence_after: FloatArray
    global_mass_imbalance: float
    pressure_solve_residual: float

    @property
    def max_divergence_before(self) -> float:
        """Largest absolute cell divergence before velocity correction."""
        return float(np.max(np.abs(self.divergence_before)))

    @property
    def max_divergence_after(self) -> float:
        """Largest absolute cell divergence after velocity correction."""
        return float(np.max(np.abs(self.divergence_after)))


def _finite_cell_values(field: ScalarField, name: str) -> FloatArray:
    """Validate a cell-centered scalar field before updating its values."""
    if not isinstance(field, ScalarField):
        raise TypeError(f"{name} must be a ScalarField")
    if field.location != "cell_center":
        raise ValueError(f"{name} must be cell-centered")
    values = np.asarray(field.values, dtype=np.float64)
    if values.shape != field.mesh.shape_for_location("cell_center"):
        raise ValueError(f"{name} values have an invalid shape")
    if not np.all(np.isfinite(values)):
        raise ValueError(f"{name} values must all be finite")
    return values


class ProjectionCorrector:
    """Correct a predicted MAC velocity and update pressure for one time step.

    The correction uses the same two-point face gradient as the M4 five-point
    pressure matrix. Using a different gradient stencil here would make the
    pressure solve and continuity correction inconsistent.
    """

    def __init__(self, density: float, time_step: float) -> None:
        """Create a corrector using the density and time step of the predictor."""
        for name, value in (("density", density), ("time_step", time_step)):
            if isinstance(value, bool) or not isinstance(value, Real):
                raise TypeError(f"{name} must be a finite positive number")
            if not isfinite(value) or value <= 0.0:
                raise ValueError(f"{name} must be a finite positive number")
        self.density = float(density)
        self.time_step = float(time_step)

    def correct_velocity(
        self, predicted_velocity: VectorField, correction: ScalarField
    ) -> VectorField:
        """Return `u* - dt/rho grad(p')`, preserving normal wall velocities.

        Only internal faces are updated. The pressure matrix uses homogeneous
        Neumann conditions, so correction gradients at outer normal faces are
        zero and their predicted wall velocities remain unchanged.
        """
        if not isinstance(predicted_velocity, VectorField):
            raise TypeError("predicted_velocity must be a VectorField")
        correction_values = _finite_cell_values(correction, "correction")
        mesh = predicted_velocity.mesh
        if correction.mesh != mesh:
            raise ValueError("correction and velocity fields must use the same mesh")

        u_values = np.asarray(predicted_velocity.u.values, dtype=np.float64)
        v_values = np.asarray(predicted_velocity.v.values, dtype=np.float64)
        if u_values.shape != mesh.shape_for_location("x_face"):
            raise ValueError("u values have an invalid shape")
        if v_values.shape != mesh.shape_for_location("y_face"):
            raise ValueError("v values have an invalid shape")
        if not np.all(np.isfinite(u_values)) or not np.all(np.isfinite(v_values)):
            raise ValueError("predicted velocity values must all be finite")

        corrected_u = u_values.copy()
        corrected_v = v_values.copy()
        corrected_u[:, 1:-1] -= (
            self.time_step
            / self.density
            * (correction_values[:, 1:] - correction_values[:, :-1])
            / mesh.dx
        )
        corrected_v[1:-1, :] -= (
            self.time_step
            / self.density
            * (correction_values[1:, :] - correction_values[:-1, :])
            / mesh.dy
        )

        corrected_velocity = VectorField(mesh, name="corrected_velocity")
        corrected_velocity.set_values(corrected_u, corrected_v)
        return corrected_velocity

    def correct_pressure(self, pressure: ScalarField, correction: ScalarField) -> ScalarField:
        """Return updated pressure `p + p'` without modifying either input."""
        pressure_values = _finite_cell_values(pressure, "pressure")
        correction_values = _finite_cell_values(correction, "correction")
        if pressure.mesh != correction.mesh:
            raise ValueError("pressure and correction fields must use the same mesh")
        updated_pressure = ScalarField(pressure.mesh, name="corrected_pressure")
        updated_pressure.set_values(pressure_values + correction_values)
        return updated_pressure

    def project(
        self,
        predicted_velocity: VectorField,
        pressure: ScalarField,
        pressure_correction: PressureCorrectionResult,
    ) -> ProjectionResult:
        """Correct velocity/pressure and report cell and global conservation.

        The input fields remain unchanged. ``global_mass_imbalance`` is the
        domain integral of the corrected velocity divergence; for unit-depth
        2D meshes it equals the net boundary volume flux.
        """
        if not isinstance(pressure_correction, PressureCorrectionResult):
            raise TypeError("pressure_correction must be a PressureCorrectionResult")
        if predicted_velocity.mesh != pressure.mesh:
            raise ValueError("pressure and velocity fields must use the same mesh")
        if pressure_correction.correction.mesh != predicted_velocity.mesh:
            raise ValueError("pressure correction and velocity fields must use the same mesh")

        divergence_before = divergence(predicted_velocity)
        corrected_velocity = self.correct_velocity(
            predicted_velocity, pressure_correction.correction
        )
        corrected_pressure = self.correct_pressure(pressure, pressure_correction.correction)
        divergence_after = divergence(corrected_velocity)
        global_mass_imbalance = float(
            np.sum(divergence_after) * predicted_velocity.mesh.cell_area
        )
        return ProjectionResult(
            velocity=corrected_velocity,
            pressure=corrected_pressure,
            pressure_correction=pressure_correction.correction,
            divergence_before=divergence_before,
            divergence_after=divergence_after,
            global_mass_imbalance=global_mass_imbalance,
            pressure_solve_residual=pressure_correction.relative_residual,
        )