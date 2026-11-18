import numpy as np
import pytest

from fvm import (
    BoundaryConditions,
    CartesianMesh,
    MovingWall,
    NoSlipWall,
    ScalarField,
    TransientSolver,
    VectorField,
)


def _conditions(lid_speed: float = 0.0) -> BoundaryConditions:
    conditions = BoundaryConditions()
    for side in ("west", "east", "south", "north"):
        if side == "north" and lid_speed != 0.0:
            conditions.set("velocity", side, MovingWall((lid_speed, 0.0)))
        else:
            conditions.set("velocity", side, NoSlipWall())
    return conditions


def test_stationary_cavity_converges_and_stays_at_rest() -> None:
    mesh = CartesianMesh(nx=5, ny=4)
    velocity = VectorField(mesh)
    pressure = ScalarField(mesh, name="pressure")
    solver = TransientSolver(
        density=1.0,
        viscosity=0.01,
        max_time_step=0.1,
        max_steps=5,
    )

    result = solver.run(velocity, pressure, _conditions())

    assert result.converged
    assert result.termination_reason == "converged"
    assert result.steps == 1
    assert result.history[0].velocity_change == 0.0
    assert result.history[0].max_divergence_after == 0.0
    assert result.history[0].time_step == pytest.approx(0.1)
    assert np.count_nonzero(result.velocity.u.values) == 0
    assert np.count_nonzero(result.velocity.v.values) == 0
    assert np.count_nonzero(velocity.u.values) == 0
    assert np.count_nonzero(pressure.values) == 0


def test_time_step_estimate_includes_moving_wall_and_cfl_limit() -> None:
    mesh = CartesianMesh(nx=10, ny=5, width=2.0, height=1.0)
    solver = TransientSolver(
        density=1.0,
        viscosity=0.01,
        max_time_step=1.0,
        cfl_limit=0.4,
    )

    time_step = solver.estimate_time_step(VectorField(mesh), _conditions(lid_speed=1.0))

    assert time_step == pytest.approx(0.08)


def test_lid_cavity_runs_to_step_limit_with_cfl_and_continuity_monitored() -> None:
    mesh = CartesianMesh(nx=8, ny=8)
    velocity = VectorField(mesh)
    pressure = ScalarField(mesh, name="pressure")
    solver = TransientSolver(
        density=1.0,
        viscosity=0.01,
        max_time_step=0.01,
        max_steps=3,
        cfl_limit=0.35,
        velocity_tolerance=1e-14,
    )

    result = solver.run(velocity, pressure, _conditions(lid_speed=1.0))

    assert not result.converged
    assert result.termination_reason == "maximum_steps_reached"
    assert result.steps == 3
    assert result.final_time == pytest.approx(sum(item.time_step for item in result.history))
    assert all(item.cfl_number <= 0.35 + 1e-14 for item in result.history)
    assert all(item.max_divergence_after < 1e-10 for item in result.history)
    assert all(abs(item.global_mass_imbalance) < 1e-12 for item in result.history)
    assert all(item.pressure_residual < 1e-10 for item in result.history)
    assert any(item.velocity_change > 0.0 for item in result.history)


def test_solver_reports_time_step_underflow_instead_of_using_unstable_step() -> None:
    mesh = CartesianMesh(nx=10, ny=10)
    velocity = VectorField(mesh)
    velocity.u.values.fill(100.0)
    solver = TransientSolver(
        density=1.0,
        viscosity=0.01,
        max_time_step=1.0,
        cfl_limit=0.5,
        minimum_time_step=0.1,
    )

    with pytest.raises(RuntimeError, match="below minimum_time_step"):
        solver.estimate_time_step(velocity, _conditions())


def test_solver_validates_iteration_and_cfl_configuration() -> None:
    with pytest.raises(ValueError, match="max_steps"):
        TransientSolver(1.0, 0.01, 0.1, max_steps=0)
    with pytest.raises(ValueError, match="cfl_limit"):
        TransientSolver(1.0, 0.01, 0.1, cfl_limit=1.1)
    with pytest.raises(ValueError, match="minimum_time_step"):
        TransientSolver(1.0, 0.01, 0.1, minimum_time_step=0.2)


def test_step_observer_receives_each_step_without_mutating_solver_state() -> None:
    mesh = CartesianMesh(nx=5, ny=5)
    solver = TransientSolver(
        density=1.0,
        viscosity=0.01,
        max_time_step=0.001,
        max_steps=2,
        velocity_tolerance=1e-14,
    )
    observed_steps: list[int] = []

    def observe(diagnostics, velocity_snapshot, pressure_snapshot) -> None:
        observed_steps.append(diagnostics.step)
        velocity_snapshot.u.values.fill(999.0)
        pressure_snapshot.values.fill(999.0)

    result = solver.run(
        VectorField(mesh),
        ScalarField(mesh, name="pressure"),
        _conditions(lid_speed=1.0),
        step_observer=observe,
    )

    assert observed_steps == [1, 2]
    assert np.max(result.velocity.u.values) < 999.0
    assert np.max(result.pressure.values) < 999.0
