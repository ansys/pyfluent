import numpy as np
import pytest

from fvm import (
    BoundaryConditions,
    CartesianMesh,
    MomentumPredictor,
    MovingWall,
    NoSlipWall,
    ScalarField,
    VectorField,
)


def _wall_conditions(lid_speed: float = 0.0) -> BoundaryConditions:
    conditions = BoundaryConditions()
    for side in ("west", "east", "south", "north"):
        if side == "north" and lid_speed != 0.0:
            conditions.set("velocity", side, MovingWall((lid_speed, 0.0)))
        else:
            conditions.set("velocity", side, NoSlipWall())
    return conditions


def test_sparse_component_matrices_have_expected_stencil_coefficients() -> None:
    mesh = CartesianMesh(nx=3, ny=2, width=3.0, height=2.0)
    velocity = VectorField(mesh)
    pressure = ScalarField(mesh, name="pressure")
    predictor = MomentumPredictor(density=2.0, viscosity=1.0, time_step=0.5)

    assembly = predictor.assemble(velocity, pressure, _wall_conditions())

    assert assembly.u_unknown_shape == (2, 2)
    assert assembly.v_unknown_shape == (1, 3)
    assert assembly.u_matrix.shape == (4, 4)
    assert assembly.v_matrix.shape == (3, 3)
    assert assembly.u_matrix[0, 0] == pytest.approx(9.0)
    assert assembly.u_matrix[0, 1] == pytest.approx(-1.0)
    assert assembly.u_matrix[0, 2] == pytest.approx(-1.0)
    assert assembly.v_matrix[0, 0] == pytest.approx(9.0)
    assert assembly.v_matrix[0, 1] == pytest.approx(-1.0)
    assert np.all(assembly.u_rhs == 0.0)
    assert np.all(assembly.v_rhs == 0.0)


def test_stationary_cavity_predictor_preserves_zero_flow() -> None:
    mesh = CartesianMesh(nx=4, ny=3)
    velocity = VectorField(mesh)
    pressure = ScalarField(mesh, name="pressure")
    predictor = MomentumPredictor(density=1.0, viscosity=0.01, time_step=0.1)

    prediction = predictor.predict(velocity, pressure, _wall_conditions())

    assert np.count_nonzero(prediction.velocity.u.values) == 0
    assert np.count_nonzero(prediction.velocity.v.values) == 0
    assert prediction.u_relative_residual < 1e-14
    assert prediction.v_relative_residual < 1e-14


def test_pressure_gradient_is_an_explicit_momentum_source() -> None:
    mesh = CartesianMesh(nx=4, ny=3)
    velocity = VectorField(mesh)
    pressure = ScalarField(mesh, name="pressure")
    x, _ = mesh.cell_center_coordinates
    pressure.set_values(x)
    density = 2.0
    time_step = 0.1
    predictor = MomentumPredictor(density, viscosity=0.0, time_step=time_step)

    assembly = predictor.assemble(velocity, pressure, _wall_conditions())
    prediction = predictor.solve(assembly)

    np.testing.assert_allclose(assembly.u_pressure_gradient, 1.0)
    np.testing.assert_allclose(assembly.u_rhs, -1.0)
    np.testing.assert_allclose(
        prediction.velocity.u.values[:, 1:-1], -time_step / density
    )
    assert np.count_nonzero(prediction.velocity.v.values) == 0


def test_explicit_upwind_convection_is_included_in_each_rhs() -> None:
    mesh = CartesianMesh(nx=4, ny=3)
    velocity = VectorField(mesh)
    u_values = np.zeros(mesh.shape_for_location("x_face"))
    v_values = np.zeros(mesh.shape_for_location("y_face"))
    u_values[:, 1:-1] = [
        [0.2, -0.1, 0.3],
        [0.1, 0.4, -0.2],
        [-0.3, 0.2, 0.1],
    ]
    v_values[1:-1, :] = [[0.2, -0.1, 0.3, 0.1], [-0.2, 0.3, 0.1, -0.1]]
    velocity.set_values(u_values, v_values)
    pressure = ScalarField(mesh, name="pressure")
    density = 1.5
    time_step = 0.2
    predictor = MomentumPredictor(density, viscosity=0.0, time_step=time_step)

    assembly = predictor.assemble(velocity, pressure, _wall_conditions())

    assert np.any(assembly.u_convection != 0.0)
    assert np.any(assembly.v_convection != 0.0)
    np.testing.assert_allclose(
        assembly.u_rhs.reshape(assembly.u_unknown_shape),
        density / time_step * u_values[:, 1:-1]
        - density * assembly.u_convection,
    )
    np.testing.assert_allclose(
        assembly.v_rhs.reshape(assembly.v_unknown_shape),
        density / time_step * v_values[1:-1, :]
        - density * assembly.v_convection,
    )


def test_transient_storage_uses_fixed_time_level_during_nonlinear_iteration() -> None:
    mesh = CartesianMesh(nx=4, ny=3)
    iterate_velocity = VectorField(mesh)
    iterate_velocity.u.values[:, 1:-1] = 0.25
    time_level_velocity = VectorField(mesh)
    time_level_velocity.u.values[:, 1:-1] = 0.1
    pressure = ScalarField(mesh, name="pressure")
    density = 1.5
    time_step = 0.2
    predictor = MomentumPredictor(density, viscosity=0.0, time_step=time_step)

    assembly = predictor.assemble(
        iterate_velocity,
        pressure,
        _wall_conditions(),
        temporal_velocity=time_level_velocity,
    )

    np.testing.assert_allclose(
        assembly.u_rhs.reshape(assembly.u_unknown_shape)
        + density * assembly.u_convection,
        density / time_step * time_level_velocity.u.values[:, 1:-1],
    )


def test_moving_lid_enters_implicit_diffusion_without_mutating_inputs() -> None:
    mesh = CartesianMesh(nx=4, ny=4)
    velocity = VectorField(mesh)
    pressure = ScalarField(mesh, name="pressure")
    initial_u = velocity.u.values.copy()
    initial_v = velocity.v.values.copy()
    predictor = MomentumPredictor(density=1.0, viscosity=0.1, time_step=0.1)

    prediction = predictor.predict(velocity, pressure, _wall_conditions(lid_speed=1.0))

    np.testing.assert_array_equal(velocity.u.values, initial_u)
    np.testing.assert_array_equal(velocity.v.values, initial_v)
    np.testing.assert_array_equal(prediction.velocity.u.values[:, [0, -1]], 0.0)
    np.testing.assert_array_equal(prediction.velocity.v.values[[0, -1], :], 0.0)
    assert np.all(prediction.velocity.u.values[:, 1:-1] > 0.0)
    assert (
        np.mean(prediction.velocity.u.values[-1, 1:-1])
        > np.mean(prediction.velocity.u.values[0, 1:-1])
    )


def test_predictor_rejects_missing_boundaries_and_invalid_properties() -> None:
    mesh = CartesianMesh(nx=3, ny=3)
    predictor = MomentumPredictor(density=1.0, viscosity=0.0, time_step=0.1)

    with pytest.raises(ValueError, match="missing velocity boundary"):
        predictor.assemble(
            VectorField(mesh), ScalarField(mesh, name="pressure"), BoundaryConditions()
        )
    with pytest.raises(ValueError, match="density"):
        MomentumPredictor(density=0.0, viscosity=0.01, time_step=0.1)
    with pytest.raises(ValueError, match="viscosity"):
        MomentumPredictor(density=1.0, viscosity=-0.01, time_step=0.1)
    with pytest.raises(ValueError, match="time_step"):
        MomentumPredictor(density=1.0, viscosity=0.01, time_step=0.0)
