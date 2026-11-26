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


def test_steady_mode_uses_fixed_pseudo_time_and_reports_iterations() -> None:
    mesh = CartesianMesh(nx=5, ny=4)
    solver = TransientSolver(
        density=1.0,
        viscosity=0.01,
        max_time_step=0.025,
        max_steps=3,
        transient=False,
    )

    result = solver.run(
        VectorField(mesh), ScalarField(mesh, name="pressure"), _conditions()
    )

    assert result.converged
    assert result.final_time is None
    assert result.final_pseudo_time == pytest.approx(0.025)
    assert result.history[0].time is None
    assert result.history[0].pseudo_time == pytest.approx(0.025)
    assert result.history[0].time_step == pytest.approx(0.025)


def test_steady_mode_caps_fixed_step_once_to_a_safe_cfl_value() -> None:
    mesh = CartesianMesh(nx=8, ny=8)
    solver = TransientSolver(
        density=1.0,
        viscosity=0.01,
        max_time_step=0.1,
        max_steps=4,
        cfl_limit=0.5,
        velocity_tolerance=1e-14,
        transient=False,
    )

    result = solver.run(
        VectorField(mesh),
        ScalarField(mesh, name="pressure"),
        _conditions(lid_speed=1.0),
    )

    assert result.history[0].time_step < solver.max_time_step
    assert len(result.history) == 4
    assert all(
        item.time_step == pytest.approx(result.history[0].time_step)
        for item in result.history
    )
    assert all(item.cfl_number <= solver.cfl_limit for item in result.history)


def test_finite_transient_converges_each_time_step_before_advancing() -> None:
    mesh = CartesianMesh(nx=4, ny=4)
    solver = TransientSolver(
        density=1.0,
        viscosity=0.01,
        max_time_step=0.001,
        max_steps=3,
        cfl_limit=0.35,
        velocity_tolerance=1e-6,
        end_time=0.002,
        max_inner_iterations_per_time_step=50,
    )

    result = solver.run(
        VectorField(mesh), ScalarField(mesh, name="pressure"), _conditions(lid_speed=1.0)
    )

    assert result.converged
    assert result.termination_reason == "final_time_reached"
    assert result.final_time == pytest.approx(0.002)
    assert [item.time for item in result.history] == pytest.approx([0.001, 0.002])
    assert all(item.inner_iterations > 1 for item in result.history)
    assert all(item.cfl_number <= 0.35 + 1e-14 for item in result.history)


def test_finite_transient_stops_when_a_physical_step_cannot_converge() -> None:
    mesh = CartesianMesh(nx=4, ny=4)
    solver = TransientSolver(
        density=1.0,
        viscosity=0.01,
        max_time_step=0.001,
        max_steps=3,
        velocity_tolerance=1e-14,
        end_time=0.002,
        max_inner_iterations_per_time_step=1,
    )

    result = solver.run(
        VectorField(mesh), ScalarField(mesh, name="pressure"), _conditions(lid_speed=1.0)
    )

    assert not result.converged
    assert result.termination_reason == "time_step_not_converged"
    assert result.steps == 1


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


def test_restart_state_matches_uninterrupted_transient_run() -> None:
    mesh = CartesianMesh(nx=5, ny=5)
    conditions = _conditions(lid_speed=1.0)
    solver_options = {
        "density": 1.0,
        "viscosity": 0.01,
        "max_time_step": 0.001,
        "max_steps": 4,
        "velocity_tolerance": 1e-14,
    }
    uninterrupted = TransientSolver(**solver_options).run(
        VectorField(mesh), ScalarField(mesh, name="pressure"), conditions
    )
    saved_states = []
    TransientSolver(**{**solver_options, "max_steps": 2}).run(
        VectorField(mesh),
        ScalarField(mesh, name="pressure"),
        conditions,
        state_observer=saved_states.append,
    )

    resumed = TransientSolver(**solver_options).run(
        VectorField(mesh),
        ScalarField(mesh, name="pressure"),
        conditions,
        restart_state=saved_states[-1],
    )

    assert [item.step for item in resumed.history] == [1, 2, 3, 4]
    assert resumed.final_time == pytest.approx(uninterrupted.final_time)
    np.testing.assert_array_equal(resumed.velocity.u.values, uninterrupted.velocity.u.values)
    np.testing.assert_array_equal(resumed.velocity.v.values, uninterrupted.velocity.v.values)
    np.testing.assert_array_equal(resumed.pressure.values, uninterrupted.pressure.values)
    assert resumed.history == uninterrupted.history


def test_finite_transient_restart_preserves_elapsed_time() -> None:
    mesh = CartesianMesh(nx=4, ny=4)
    conditions = _conditions(lid_speed=1.0)
    options = {
        "density": 1.0,
        "viscosity": 0.01,
        "max_time_step": 0.001,
        "max_steps": 4,
        "end_time": 0.004,
        "max_inner_iterations_per_time_step": 50,
    }
    uninterrupted = TransientSolver(**options).run(
        VectorField(mesh), ScalarField(mesh, name="pressure"), conditions
    )
    saved_states = []
    TransientSolver(**{**options, "max_steps": 2}).run(
        VectorField(mesh),
        ScalarField(mesh, name="pressure"),
        conditions,
        state_observer=saved_states.append,
    )

    resumed = TransientSolver(**options).run(
        VectorField(mesh),
        ScalarField(mesh, name="pressure"),
        conditions,
        restart_state=saved_states[-1],
    )

    assert saved_states[-1].elapsed_time == pytest.approx(0.002)
    assert resumed.final_time == pytest.approx(0.004)
    assert resumed.history == uninterrupted.history
    np.testing.assert_array_equal(resumed.velocity.u.values, uninterrupted.velocity.u.values)
    np.testing.assert_array_equal(resumed.velocity.v.values, uninterrupted.velocity.v.values)
    np.testing.assert_array_equal(resumed.pressure.values, uninterrupted.pressure.values)


def test_restart_at_finite_transient_end_time_reports_completion() -> None:
    mesh = CartesianMesh(nx=4, ny=4)
    conditions = _conditions(lid_speed=1.0)
    options = {
        "density": 1.0,
        "viscosity": 0.01,
        "max_time_step": 0.001,
        "max_steps": 4,
        "end_time": 0.002,
        "max_inner_iterations_per_time_step": 50,
    }
    saved_states = []
    original = TransientSolver(**options).run(
        VectorField(mesh),
        ScalarField(mesh, name="pressure"),
        conditions,
        state_observer=saved_states.append,
    )

    restarted = TransientSolver(**options).run(
        VectorField(mesh),
        ScalarField(mesh, name="pressure"),
        conditions,
        restart_state=saved_states[-1],
    )

    assert original.converged
    assert restarted.converged
    assert restarted.termination_reason == "final_time_reached"
    assert restarted.history == original.history


def test_steady_restart_reuses_selected_pseudo_time_step() -> None:
    mesh = CartesianMesh(nx=5, ny=5)
    conditions = _conditions(lid_speed=1.0)
    options = {
        "density": 1.0,
        "viscosity": 0.01,
        "max_time_step": 0.1,
        "max_steps": 4,
        "velocity_tolerance": 1e-14,
        "transient": False,
    }
    uninterrupted = TransientSolver(**options).run(
        VectorField(mesh), ScalarField(mesh, name="pressure"), conditions
    )
    saved_states = []
    TransientSolver(**{**options, "max_steps": 2}).run(
        VectorField(mesh),
        ScalarField(mesh, name="pressure"),
        conditions,
        state_observer=saved_states.append,
    )

    resumed = TransientSolver(**options).run(
        VectorField(mesh),
        ScalarField(mesh, name="pressure"),
        conditions,
        restart_state=saved_states[-1],
    )

    assert saved_states[-1].steady_time_step == pytest.approx(
        uninterrupted.history[0].time_step
    )
    assert resumed.history == uninterrupted.history
    np.testing.assert_array_equal(resumed.velocity.u.values, uninterrupted.velocity.u.values)
    np.testing.assert_array_equal(resumed.pressure.values, uninterrupted.pressure.values)
