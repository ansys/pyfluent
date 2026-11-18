"""Transient execution and convergence monitoring for the projection solver."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from numbers import Integral, Real
from collections.abc import Callable

import numpy as np

from .boundary_conditions import (
    BoundaryConditions,
    FixedValue,
    MovingWall,
    NoSlipWall,
)
from .fields import ScalarField, VectorField
from .mesh import BOUNDARY_NAMES, FloatArray
from .momentum import MomentumPredictor
from .pressure_correction import PressureCorrectionSolver
from .projection import ProjectionCorrector

StepObserver = Callable[["StepDiagnostics", VectorField, ScalarField], None]


@dataclass(frozen=True, slots=True)
class StepDiagnostics:
    """Quantities recorded after each completed projection time step."""

    step: int
    time: float
    time_step: float
    cfl_number: float
    velocity_change: float
    max_divergence_before: float
    max_divergence_after: float
    global_mass_imbalance: float
    u_momentum_residual: float
    v_momentum_residual: float
    pressure_residual: float


@dataclass(frozen=True, slots=True)
class SimulationSettings:
    """Immutable input settings retained for reproducible output export."""

    density: float
    viscosity: float
    max_time_step: float
    max_steps: int
    cfl_limit: float
    velocity_tolerance: float
    continuity_tolerance: float
    mass_tolerance: float
    momentum_residual_tolerance: float
    pressure_residual_tolerance: float
    minimum_time_step: float


@dataclass(frozen=True, slots=True)
class SimulationResult:
    """Final fields, convergence state, and immutable step history."""

    velocity: VectorField
    pressure: ScalarField
    history: tuple[StepDiagnostics, ...]
    settings: SimulationSettings
    converged: bool
    termination_reason: str

    @property
    def steps(self) -> int:
        """Number of projection steps completed."""
        return len(self.history)

    @property
    def final_time(self) -> float:
        """Physical time reached by the final completed step."""
        return self.history[-1].time if self.history else 0.0


def _positive_number(name: str, value: float) -> float:
    """Validate a finite positive scalar simulation setting."""
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a finite positive number")
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be a finite positive number")
    return float(value)


def _wall_velocities(boundary_conditions: BoundaryConditions) -> dict[str, tuple[float, float]]:
    """Read the vector velocity prescribed at every physical wall."""
    if not isinstance(boundary_conditions, BoundaryConditions):
        raise TypeError("boundary_conditions must be BoundaryConditions")
    wall_values: dict[str, tuple[float, float]] = {}
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


def _advective_rate(
    velocity: VectorField, wall_velocities: dict[str, tuple[float, float]]
) -> float:
    """Estimate the global explicit-convection rate including moving walls."""
    mesh = velocity.mesh
    u_values = np.asarray(velocity.u.values, dtype=np.float64)
    v_values = np.asarray(velocity.v.values, dtype=np.float64)
    if u_values.shape != mesh.shape_for_location("x_face"):
        raise ValueError("u values have an invalid shape")
    if v_values.shape != mesh.shape_for_location("y_face"):
        raise ValueError("v values have an invalid shape")
    if not np.all(np.isfinite(u_values)) or not np.all(np.isfinite(v_values)):
        raise ValueError("velocity values must all be finite")

    max_u = float(np.max(np.abs(u_values)))
    max_v = float(np.max(np.abs(v_values)))
    max_u = max(max_u, *(abs(wall[0]) for wall in wall_velocities.values()))
    max_v = max(max_v, *(abs(wall[1]) for wall in wall_velocities.values()))
    return max_u / mesh.dx + max_v / mesh.dy


class TransientSolver:
    """Run repeated momentum-predictor, pressure-solve, and projection steps.

    ``max_time_step`` is a cap. Each step is reduced as needed to satisfy
    `dt * (max|u|/dx + max|v|/dy) <= cfl_limit`; moving-wall speeds are included
    in those maxima. Diffusion is implicit in M3, so only explicit convection
    contributes to this CFL restriction.

    Steady state is reported only when velocity change, continuity, global
    mass balance, momentum residuals, and pressure residual all meet their
    configured tolerances. Reaching ``max_steps`` instead returns a result
    with ``converged=False`` and an explicit termination reason.
    """

    def __init__(
        self,
        density: float,
        viscosity: float,
        max_time_step: float,
        max_steps: int = 1000,
        cfl_limit: float = 0.5,
        velocity_tolerance: float = 1e-6,
        continuity_tolerance: float = 1e-8,
        mass_tolerance: float = 1e-10,
        momentum_residual_tolerance: float = 1e-10,
        pressure_residual_tolerance: float = 1e-10,
        minimum_time_step: float = 1e-12,
    ) -> None:
        """Configure material properties, time-step limits, and stop criteria."""
        self.density = _positive_number("density", density)
        if isinstance(viscosity, bool) or not isinstance(viscosity, Real):
            raise TypeError("viscosity must be a finite non-negative number")
        if not isfinite(viscosity) or viscosity < 0.0:
            raise ValueError("viscosity must be a finite non-negative number")
        self.viscosity = float(viscosity)
        self.max_time_step = _positive_number("max_time_step", max_time_step)
        self.minimum_time_step = _positive_number("minimum_time_step", minimum_time_step)
        if self.minimum_time_step > self.max_time_step:
            raise ValueError("minimum_time_step must not exceed max_time_step")
        if isinstance(max_steps, bool) or not isinstance(max_steps, Integral):
            raise TypeError("max_steps must be a positive integer")
        if max_steps <= 0:
            raise ValueError("max_steps must be a positive integer")
        self.max_steps = int(max_steps)
        self.cfl_limit = _positive_number("cfl_limit", cfl_limit)
        if self.cfl_limit > 1.0:
            raise ValueError("cfl_limit must not exceed 1 for explicit upwind convection")
        self.velocity_tolerance = _positive_number("velocity_tolerance", velocity_tolerance)
        self.continuity_tolerance = _positive_number(
            "continuity_tolerance", continuity_tolerance
        )
        self.mass_tolerance = _positive_number("mass_tolerance", mass_tolerance)
        self.momentum_residual_tolerance = _positive_number(
            "momentum_residual_tolerance", momentum_residual_tolerance
        )
        self.pressure_residual_tolerance = _positive_number(
            "pressure_residual_tolerance", pressure_residual_tolerance
        )
        self.settings = SimulationSettings(
            density=self.density,
            viscosity=self.viscosity,
            max_time_step=self.max_time_step,
            max_steps=self.max_steps,
            cfl_limit=self.cfl_limit,
            velocity_tolerance=self.velocity_tolerance,
            continuity_tolerance=self.continuity_tolerance,
            mass_tolerance=self.mass_tolerance,
            momentum_residual_tolerance=self.momentum_residual_tolerance,
            pressure_residual_tolerance=self.pressure_residual_tolerance,
            minimum_time_step=self.minimum_time_step,
        )

    def estimate_time_step(
        self, velocity: VectorField, boundary_conditions: BoundaryConditions
    ) -> float:
        """Return the maximum time step allowed by the current convective CFL."""
        if not isinstance(velocity, VectorField):
            raise TypeError("velocity must be a VectorField")
        walls = _wall_velocities(boundary_conditions)
        rate = _advective_rate(velocity, walls)
        if rate == 0.0:
            return self.max_time_step
        time_step = min(self.max_time_step, self.cfl_limit / rate)
        if time_step < self.minimum_time_step:
            raise RuntimeError(
                f"stable time step {time_step:.6g} is below minimum_time_step "
                f"{self.minimum_time_step:.6g}"
            )
        return time_step

    def run(
        self,
        initial_velocity: VectorField,
        initial_pressure: ScalarField,
        boundary_conditions: BoundaryConditions,
        *,
        step_observer: StepObserver | None = None,
    ) -> SimulationResult:
        """Advance the supplied case until steady, or until ``max_steps``.

        Input fields are never mutated. Each recorded step follows this order:
        choose a CFL-limited step, predict momentum, solve pressure correction,
        correct velocity and pressure, measure conservation, then test all stop
        criteria.

        When ``step_observer`` is supplied, it is called after each completed
        projection with that step's diagnostics and defensive copies of the
        velocity and pressure fields. Observers can visualize or export state
        without being able to mutate the running simulation.
        """
        if not isinstance(initial_velocity, VectorField):
            raise TypeError("initial_velocity must be a VectorField")
        if not isinstance(initial_pressure, ScalarField):
            raise TypeError("initial_pressure must be a ScalarField")
        if initial_pressure.mesh != initial_velocity.mesh:
            raise ValueError("initial pressure and velocity must use the same mesh")
        if initial_pressure.location != "cell_center":
            raise ValueError("initial pressure must be cell-centered")
        walls = _wall_velocities(boundary_conditions)

        velocity = initial_velocity
        pressure = initial_pressure
        elapsed_time = 0.0
        history: list[StepDiagnostics] = []

        for step in range(1, self.max_steps + 1):
            advective_rate = _advective_rate(velocity, walls)
            time_step = self.estimate_time_step(velocity, boundary_conditions)
            cfl_number = time_step * advective_rate

            momentum_predictor = MomentumPredictor(
                self.density, self.viscosity, time_step
            )
            momentum = momentum_predictor.predict(velocity, pressure, boundary_conditions)

            pressure_solver = PressureCorrectionSolver(self.density, time_step)
            pressure_correction = pressure_solver.predict(momentum.velocity)

            corrector = ProjectionCorrector(self.density, time_step)
            projection = corrector.project(
                momentum.velocity, pressure, pressure_correction
            )

            velocity_change = max(
                float(np.max(np.abs(projection.velocity.u.values - velocity.u.values))),
                float(np.max(np.abs(projection.velocity.v.values - velocity.v.values))),
            )
            elapsed_time += time_step
            diagnostics = StepDiagnostics(
                step=step,
                time=elapsed_time,
                time_step=time_step,
                cfl_number=cfl_number,
                velocity_change=velocity_change,
                max_divergence_before=projection.max_divergence_before,
                max_divergence_after=projection.max_divergence_after,
                global_mass_imbalance=projection.global_mass_imbalance,
                u_momentum_residual=momentum.u_relative_residual,
                v_momentum_residual=momentum.v_relative_residual,
                pressure_residual=projection.pressure_solve_residual,
            )
            history.append(diagnostics)

            velocity = projection.velocity
            pressure = projection.pressure
            if step_observer is not None:
                # Observers receive copies so visualization code cannot alter
                # the state that will be advanced on the next time step.
                velocity_snapshot = VectorField(velocity.mesh, name="observer_velocity")
                velocity_snapshot.set_values(velocity.u.values, velocity.v.values)
                pressure_snapshot = ScalarField(
                    pressure.mesh, name="observer_pressure"
                )
                pressure_snapshot.set_values(pressure.values)
                step_observer(diagnostics, velocity_snapshot, pressure_snapshot)
            if self._has_converged(diagnostics):
                return SimulationResult(
                    velocity=velocity,
                    pressure=pressure,
                    history=tuple(history),
                    settings=self.settings,
                    converged=True,
                    termination_reason="converged",
                )

        return SimulationResult(
            velocity=velocity,
            pressure=pressure,
            history=tuple(history),
            settings=self.settings,
            converged=False,
            termination_reason="maximum_steps_reached",
        )

    def _has_converged(self, diagnostics: StepDiagnostics) -> bool:
        """Require steady velocity, continuity, mass, and solver tolerances."""
        return (
            diagnostics.velocity_change <= self.velocity_tolerance
            and diagnostics.max_divergence_after <= self.continuity_tolerance
            and abs(diagnostics.global_mass_imbalance) <= self.mass_tolerance
            and diagnostics.u_momentum_residual <= self.momentum_residual_tolerance
            and diagnostics.v_momentum_residual <= self.momentum_residual_tolerance
            and diagnostics.pressure_residual <= self.pressure_residual_tolerance
        )