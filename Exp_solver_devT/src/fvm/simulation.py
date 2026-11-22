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
StateObserver = Callable[["SimulationState"], None]
BoundaryConditionsAtTime = Callable[[float], BoundaryConditions]
BoundaryConditionsOverInterval = Callable[[float, float], BoundaryConditions]


@dataclass(frozen=True, slots=True)
class StepDiagnostics:
    """Quantities recorded after each completed projection time step."""

    step: int
    time: float | None
    pseudo_time: float | None
    time_step: float
    cfl_number: float
    velocity_change: float
    max_divergence_before: float
    max_divergence_after: float
    global_mass_imbalance: float
    u_momentum_residual: float
    v_momentum_residual: float
    pressure_residual: float
    inner_iterations: int = 1


@dataclass(frozen=True, slots=True)
class SimulationState:
    """Complete solver state at a completed step boundary."""

    velocity: VectorField
    pressure: ScalarField
    completed_steps: int
    elapsed_time: float
    pseudo_time: float
    steady_time_step: float | None
    history: tuple[StepDiagnostics, ...]


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
    transient: bool
    end_time: float | None
    max_inner_iterations_per_time_step: int


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
    def final_time(self) -> float | None:
        """Physical time reached by the final completed step."""
        return self.history[-1].time if self.history else 0.0

    @property
    def final_pseudo_time(self) -> float | None:
        """Pseudo-time accumulated by a steady-state run."""
        return self.history[-1].pseudo_time if self.history else 0.0


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
        transient: bool = True,
        end_time: float | None = None,
        max_inner_iterations_per_time_step: int = 100,
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
        if not isinstance(transient, bool):
            raise TypeError("transient must be a boolean")
        self.transient = transient
        self.end_time = (
            None if end_time is None else _positive_number("end_time", end_time)
        )
        if self.end_time is not None and not self.transient:
            raise ValueError("end_time is only valid for transient simulations")
        if (
            isinstance(max_inner_iterations_per_time_step, bool)
            or not isinstance(max_inner_iterations_per_time_step, Integral)
            or max_inner_iterations_per_time_step <= 0
        ):
            raise ValueError("max_inner_iterations_per_time_step must be a positive integer")
        self.max_inner_iterations_per_time_step = int(
            max_inner_iterations_per_time_step
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
            transient=self.transient,
            end_time=self.end_time,
            max_inner_iterations_per_time_step=(
                self.max_inner_iterations_per_time_step
            ),
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
        state_observer: StateObserver | None = None,
        state_observer_interval: int = 1,
        restart_state: SimulationState | None = None,
        boundary_conditions_at_time: BoundaryConditionsAtTime | None = None,
        boundary_conditions_over_interval: BoundaryConditionsOverInterval | None = None,
    ) -> SimulationResult:
        """Advance steady iterations or transient physical steps.

        Steady runs use a fixed pseudo-time step. Finite transient runs keep the
        previous physical-time state fixed while iterating the nonlinear
        predictor/projection system to tolerance at each physical time step.
        Transient runs without ``end_time`` retain the legacy march-to-steady
        behavior for existing case files.

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
        if (
            isinstance(state_observer_interval, bool)
            or not isinstance(state_observer_interval, Integral)
            or state_observer_interval <= 0
        ):
            raise ValueError("state_observer_interval must be a positive integer")
        walls = _wall_velocities(boundary_conditions)

        if restart_state is None:
            velocity = initial_velocity
            pressure = initial_pressure
            elapsed_time = 0.0
            pseudo_time = 0.0
            history: list[StepDiagnostics] = []
            completed_steps = 0
            restored_steady_time_step = None
        else:
            self._validate_restart_state(restart_state, initial_velocity)
            velocity = self._copy_velocity(restart_state.velocity)
            pressure = self._copy_pressure(restart_state.pressure)
            elapsed_time = restart_state.elapsed_time
            pseudo_time = restart_state.pseudo_time
            history = list(restart_state.history)
            completed_steps = restart_state.completed_steps
            restored_steady_time_step = restart_state.steady_time_step
        finite_transient = self.transient and self.end_time is not None
        steady_time_step = restored_steady_time_step or self.max_time_step
        if (
            finite_transient
            and elapsed_time >= self.end_time - 1e-14 * max(1.0, self.end_time)
        ):
            return SimulationResult(
                velocity=velocity,
                pressure=pressure,
                history=tuple(history),
                settings=self.settings,
                converged=True,
                termination_reason="final_time_reached",
            )
        if not self.transient:
            if restored_steady_time_step is None:
                initial_rate = _advective_rate(velocity, walls)
                if initial_rate > 0.0:
                    steady_time_step = min(
                        self.max_time_step,
                        self.cfl_limit / (4.0 * initial_rate),
                    )
            if steady_time_step < self.minimum_time_step:
                raise RuntimeError(
                    f"safe steady pseudo-time step {steady_time_step:.6g} is below "
                    f"minimum_time_step {self.minimum_time_step:.6g}"
                )

        for step in range(completed_steps + 1, self.max_steps + 1):
            if finite_transient:
                remaining_time = self.end_time - elapsed_time
                if remaining_time <= 0.0:
                    break
                time_step, interval_conditions = self._transient_step_size(
                    velocity,
                    elapsed_time,
                    remaining_time,
                    boundary_conditions,
                    boundary_conditions_at_time,
                    boundary_conditions_over_interval,
                )
                step_time = elapsed_time + time_step
                step_conditions = (
                    boundary_conditions_at_time(step_time)
                    if boundary_conditions_at_time is not None
                    else boundary_conditions
                )
                temporal_velocity = velocity
                iterate_velocity = velocity
                iterate_pressure = pressure
                diagnostics: StepDiagnostics | None = None
                for inner_iteration in range(1, self.max_inner_iterations_per_time_step + 1):
                    momentum, projection = self._project(
                        iterate_velocity,
                        iterate_pressure,
                        step_conditions,
                        time_step,
                        temporal_velocity=temporal_velocity,
                    )
                    velocity_change = self._velocity_change(
                        projection.velocity, iterate_velocity
                    )
                    advective_rate = _advective_rate(
                        iterate_velocity,
                        _wall_velocities(interval_conditions),
                    )
                    diagnostics = StepDiagnostics(
                        step=step,
                        time=step_time,
                        pseudo_time=None,
                        time_step=time_step,
                        cfl_number=time_step * advective_rate,
                        velocity_change=velocity_change,
                        max_divergence_before=projection.max_divergence_before,
                        max_divergence_after=projection.max_divergence_after,
                        global_mass_imbalance=projection.global_mass_imbalance,
                        u_momentum_residual=momentum.u_relative_residual,
                        v_momentum_residual=momentum.v_relative_residual,
                        pressure_residual=projection.pressure_solve_residual,
                        inner_iterations=inner_iteration,
                    )
                    iterate_velocity = projection.velocity
                    iterate_pressure = projection.pressure
                    if self._has_converged(diagnostics):
                        break

                assert diagnostics is not None
                history.append(diagnostics)
                velocity = iterate_velocity
                pressure = iterate_pressure
                elapsed_time = step_time
                step_converged = self._has_converged(diagnostics)
            else:
                step_conditions = (
                    boundary_conditions_at_time(elapsed_time)
                    if boundary_conditions_at_time is not None
                    else boundary_conditions
                )
                advective_rate = _advective_rate(
                    velocity, _wall_velocities(step_conditions)
                )
                if self.transient:
                    time_step = self.estimate_time_step(velocity, step_conditions)
                    step_conditions = (
                        boundary_conditions_at_time(elapsed_time + time_step)
                        if boundary_conditions_at_time is not None
                        else boundary_conditions
                    )
                    advective_rate = _advective_rate(
                        velocity, _wall_velocities(step_conditions)
                    )
                else:
                    time_step = steady_time_step
                cfl_number = time_step * advective_rate
                momentum, projection = self._project(
                    velocity, pressure, step_conditions, time_step
                )
                velocity_change = self._velocity_change(
                    projection.velocity, velocity
                )
                if self.transient:
                    elapsed_time += time_step
                    physical_time: float | None = elapsed_time
                    step_pseudo_time: float | None = None
                else:
                    pseudo_time += time_step
                    physical_time = None
                    step_pseudo_time = pseudo_time
                diagnostics = StepDiagnostics(
                    step=step,
                    time=physical_time,
                    pseudo_time=step_pseudo_time,
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
                step_converged = self._has_converged(diagnostics)

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
            if (
                state_observer is not None
                and step % state_observer_interval == 0
                and (not finite_transient or step_converged)
            ):
                state_observer(
                    SimulationState(
                        velocity=self._copy_velocity(velocity),
                        pressure=self._copy_pressure(pressure),
                        completed_steps=step,
                        elapsed_time=elapsed_time,
                        pseudo_time=pseudo_time,
                        steady_time_step=(
                            steady_time_step if not self.transient else None
                        ),
                        history=tuple(history),
                    )
                )
            if finite_transient:
                if not step_converged:
                    return SimulationResult(
                        velocity=velocity,
                        pressure=pressure,
                        history=tuple(history),
                        settings=self.settings,
                        converged=False,
                        termination_reason="time_step_not_converged",
                    )
                if elapsed_time >= self.end_time - 1e-14 * max(1.0, self.end_time):
                    return SimulationResult(
                        velocity=velocity,
                        pressure=pressure,
                        history=tuple(history),
                        settings=self.settings,
                        converged=True,
                        termination_reason="final_time_reached",
                    )
            elif step_converged:
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

    @staticmethod
    def _copy_velocity(velocity: VectorField) -> VectorField:
        """Make an independent copy of staggered velocity fields."""
        copied = VectorField(velocity.mesh, name=velocity.name)
        copied.set_values(velocity.u.values, velocity.v.values)
        return copied

    @staticmethod
    def _copy_pressure(pressure: ScalarField) -> ScalarField:
        """Make an independent copy of a cell-centered pressure field."""
        copied = ScalarField(pressure.mesh, name=pressure.name)
        copied.set_values(pressure.values)
        return copied

    @staticmethod
    def _validate_restart_state(
        state: SimulationState, initial_velocity: VectorField
    ) -> None:
        """Reject inconsistent or incompatible restored solver state."""
        if not isinstance(state, SimulationState):
            raise TypeError("restart_state must be a SimulationState")
        if state.velocity.mesh != initial_velocity.mesh:
            raise ValueError("restart state and initial velocity must use the same mesh")
        if state.pressure.mesh != initial_velocity.mesh:
            raise ValueError("restart state pressure must use the same mesh")
        if state.pressure.location != "cell_center":
            raise ValueError("restart state pressure must be cell-centered")
        if (
            isinstance(state.completed_steps, bool)
            or not isinstance(state.completed_steps, Integral)
            or state.completed_steps < 0
        ):
            raise ValueError("restart state completed_steps must be a non-negative integer")
        for name, value in (
            ("elapsed_time", state.elapsed_time),
            ("pseudo_time", state.pseudo_time),
        ):
            if not isfinite(value) or value < 0.0:
                raise ValueError(f"restart state {name} must be finite and non-negative")
        if state.steady_time_step is not None and (
            not isfinite(state.steady_time_step) or state.steady_time_step <= 0.0
        ):
            raise ValueError("restart state steady_time_step must be finite and positive")
        if len(state.history) != state.completed_steps:
            raise ValueError("restart state history must cover all completed steps")
        if state.history and state.history[-1].step != state.completed_steps:
            raise ValueError("restart state history step does not match completed_steps")

    def _project(
        self,
        velocity: VectorField,
        pressure: ScalarField,
        boundary_conditions: BoundaryConditions,
        time_step: float,
        *,
        temporal_velocity: VectorField | None = None,
    ):
        """Run one momentum, pressure-correction, and projection operation."""
        momentum = MomentumPredictor(
            self.density, self.viscosity, time_step
        ).predict(
            velocity,
            pressure,
            boundary_conditions,
            temporal_velocity=temporal_velocity,
        )
        pressure_correction = PressureCorrectionSolver(
            self.density, time_step
        ).predict(momentum.velocity)
        projection = ProjectionCorrector(self.density, time_step).project(
            momentum.velocity, pressure, pressure_correction
        )
        return momentum, projection

    @staticmethod
    def _velocity_change(current: VectorField, previous: VectorField) -> float:
        """Return the maximum staggered-face velocity difference."""
        return max(
            float(np.max(np.abs(current.u.values - previous.u.values))),
            float(np.max(np.abs(current.v.values - previous.v.values))),
        )

    def _transient_step_size(
        self,
        velocity: VectorField,
        current_time: float,
        remaining_time: float,
        boundary_conditions: BoundaryConditions,
        boundary_conditions_at_time: BoundaryConditionsAtTime | None,
        boundary_conditions_over_interval: BoundaryConditionsOverInterval | None,
    ) -> tuple[float, BoundaryConditions]:
        """Choose a CFL-safe step using wall speeds over its full interval."""
        candidate = min(self.max_time_step, remaining_time)
        interval_conditions = boundary_conditions
        for _ in range(8):
            end_time = current_time + candidate
            interval_conditions = (
                boundary_conditions_over_interval(current_time, end_time)
                if boundary_conditions_over_interval is not None
                else (
                    boundary_conditions_at_time(end_time)
                    if boundary_conditions_at_time is not None
                    else boundary_conditions
                )
            )
            rate = _advective_rate(velocity, _wall_velocities(interval_conditions))
            allowed = self.max_time_step if rate == 0.0 else self.cfl_limit / rate
            updated = min(candidate, allowed)
            if abs(updated - candidate) <= 1e-14 * max(1.0, candidate):
                break
            candidate = updated
        if candidate < self.minimum_time_step and remaining_time > self.minimum_time_step:
            raise RuntimeError(
                f"stable time step {candidate:.6g} is below minimum_time_step "
                f"{self.minimum_time_step:.6g}"
            )
        return candidate, interval_conditions

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