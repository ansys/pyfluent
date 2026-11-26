import numpy as np
import pytest

from fvm import (
    BoundaryConditions,
    CartesianMesh,
    MomentumPredictor,
    MovingWall,
    NoSlipWall,
    PressureCorrectionSolver,
    ProjectionCorrector,
    ScalarField,
    VectorField,
)


def _cavity_conditions(lid_speed: float = 0.0) -> BoundaryConditions:
    conditions = BoundaryConditions()
    for side in ("west", "east", "south", "north"):
        if side == "north" and lid_speed != 0.0:
            conditions.set("velocity", side, MovingWall((lid_speed, 0.0)))
        else:
            conditions.set("velocity", side, NoSlipWall())
    return conditions


def test_projection_recovers_zero_divergence_from_discrete_gradient() -> None:
    mesh = CartesianMesh(nx=5, ny=4, width=2.0, height=1.5)
    density = 1.7
    time_step = 0.025
    known_correction = np.arange(mesh.nx * mesh.ny, dtype=np.float64).reshape(
        mesh.ny, mesh.nx
    )
    predicted = VectorField(mesh)
    u_values = np.zeros(mesh.shape_for_location("x_face"))
    v_values = np.zeros(mesh.shape_for_location("y_face"))
    u_values[:, 1:-1] = (
        time_step / density * np.diff(known_correction, axis=1) / mesh.dx
    )
    v_values[1:-1, :] = (
        time_step / density * np.diff(known_correction, axis=0) / mesh.dy
    )
    predicted.set_values(u_values, v_values)
    initial_pressure = ScalarField(mesh, name="pressure", initial_value=3.0)
    old_u = predicted.u.values.copy()
    old_v = predicted.v.values.copy()
    old_pressure = initial_pressure.values.copy()
    pressure_solver = PressureCorrectionSolver(density, time_step, reference_cell=(1, 2))
    pressure_correction = pressure_solver.predict(predicted)
    corrector = ProjectionCorrector(density, time_step)

    result = corrector.project(predicted, initial_pressure, pressure_correction)

    np.testing.assert_allclose(result.velocity.u.values, 0.0, atol=1e-12)
    np.testing.assert_allclose(result.velocity.v.values, 0.0, atol=1e-12)
    np.testing.assert_allclose(
        result.pressure.values,
        old_pressure + known_correction - known_correction[1, 2],
        atol=1e-12,
    )
    assert result.max_divergence_before > 0.0
    assert result.max_divergence_after < 1e-12
    assert result.global_mass_imbalance == pytest.approx(0.0, abs=1e-12)
    assert result.pressure_solve_residual < 1e-12
    np.testing.assert_array_equal(predicted.u.values, old_u)
    np.testing.assert_array_equal(predicted.v.values, old_v)
    np.testing.assert_array_equal(initial_pressure.values, old_pressure)


def test_lid_cavity_projection_reduces_continuity_and_preserves_wall_fluxes() -> None:
    mesh = CartesianMesh(nx=12, ny=12)
    velocity = VectorField(mesh)
    pressure = ScalarField(mesh, name="pressure")
    density = 1.0
    time_step = 0.001
    predictor = MomentumPredictor(density, viscosity=0.01, time_step=time_step)
    predicted = predictor.predict(velocity, pressure, _cavity_conditions(lid_speed=1.0))
    predicted_u_walls = predicted.velocity.u.values[:, [0, -1]].copy()
    predicted_v_walls = predicted.velocity.v.values[[0, -1], :].copy()
    pressure_solver = PressureCorrectionSolver(density, time_step)
    pressure_correction = pressure_solver.predict(predicted.velocity)
    corrector = ProjectionCorrector(density, time_step)

    result = corrector.project(predicted.velocity, pressure, pressure_correction)

    assert result.max_divergence_before > 1e-3
    assert result.max_divergence_after < 1e-11
    assert abs(result.global_mass_imbalance) < 1e-12
    np.testing.assert_array_equal(result.velocity.u.values[:, [0, -1]], predicted_u_walls)
    np.testing.assert_array_equal(result.velocity.v.values[[0, -1], :], predicted_v_walls)
    np.testing.assert_allclose(
        result.pressure.values,
        pressure.values + pressure_correction.correction.values,
    )


def test_corrector_rejects_fields_on_different_meshes() -> None:
    corrector = ProjectionCorrector(density=1.0, time_step=0.1)
    velocity = VectorField(CartesianMesh(nx=3, ny=3))
    correction = ScalarField(CartesianMesh(nx=4, ny=3), name="correction")

    with pytest.raises(ValueError, match="same mesh"):
        corrector.correct_velocity(velocity, correction)
