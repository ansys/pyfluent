import numpy as np
import pytest

from fvm import (
    CartesianMesh,
    PressureCorrectionSolver,
    VectorField,
)


def test_neumann_matrix_has_expected_coefficients_and_reference_row() -> None:
    mesh = CartesianMesh(nx=3, ny=2, width=2.0, height=1.0)
    velocity = VectorField(mesh)
    solver = PressureCorrectionSolver(density=1.0, time_step=0.1)

    assembly = solver.assemble(velocity)

    assert assembly.matrix.shape == (6, 6)
    assert assembly.matrix[0, 0] == pytest.approx(1.0)
    assert np.count_nonzero(assembly.matrix.getrow(0).toarray()) == 1
    assert assembly.matrix[1, 1] == pytest.approx(8.5)
    assert assembly.matrix[1, 0] == pytest.approx(-2.25)
    assert assembly.matrix[1, 2] == pytest.approx(-2.25)
    assert assembly.matrix[1, 4] == pytest.approx(-4.0)
    assert np.all(assembly.rhs == 0.0)


def test_solver_recovers_known_discrete_pressure_correction() -> None:
    mesh = CartesianMesh(nx=5, ny=4, width=2.0, height=1.5)
    density = 1.7
    time_step = 0.025
    known = np.arange(mesh.nx * mesh.ny, dtype=np.float64).reshape(mesh.ny, mesh.nx)
    velocity = VectorField(mesh)
    u_values = np.zeros(mesh.shape_for_location("x_face"))
    v_values = np.zeros(mesh.shape_for_location("y_face"))
    u_values[:, 1:-1] = (
        time_step / density * np.diff(known, axis=1) / mesh.dx
    )
    v_values[1:-1, :] = (
        time_step / density * np.diff(known, axis=0) / mesh.dy
    )
    velocity.set_values(u_values, v_values)
    solver = PressureCorrectionSolver(
        density=density,
        time_step=time_step,
        reference_cell=(1, 2),
    )

    result = solver.predict(velocity)

    np.testing.assert_allclose(
        result.correction.values,
        known - known[1, 2],
        atol=1e-12,
    )
    assert result.correction.values[1, 2] == 0.0
    assert result.net_boundary_flux == pytest.approx(0.0)
    assert result.relative_residual < 1e-12


def test_solver_rejects_nonzero_net_boundary_flux() -> None:
    mesh = CartesianMesh(nx=3, ny=2)
    velocity = VectorField(mesh)
    u_values = np.zeros(mesh.shape_for_location("x_face"))
    u_values[:, -1] = 1.0
    velocity.set_values(u_values, np.zeros(mesh.shape_for_location("y_face")))
    solver = PressureCorrectionSolver(density=1.0, time_step=0.1)

    with pytest.raises(ValueError, match="incompatible net boundary flux"):
        solver.assemble(velocity)


def test_solver_does_not_modify_predicted_velocity() -> None:
    mesh = CartesianMesh(nx=3, ny=3)
    velocity = VectorField(mesh)
    u_values = np.zeros(mesh.shape_for_location("x_face"))
    v_values = np.zeros(mesh.shape_for_location("y_face"))
    u_values[1, 1] = 0.5
    u_values[1, 2] = 0.5
    v_values[1, 1] = 0.25
    v_values[2, 1] = 0.25
    velocity.set_values(u_values, v_values)
    before_u = velocity.u.values.copy()
    before_v = velocity.v.values.copy()
    solver = PressureCorrectionSolver(density=1.0, time_step=0.1)

    solver.predict(velocity)

    np.testing.assert_array_equal(velocity.u.values, before_u)
    np.testing.assert_array_equal(velocity.v.values, before_v)


@pytest.mark.parametrize("reference_cell", [(-1, 0), (0, 3)])
def test_solver_rejects_reference_outside_mesh(reference_cell: tuple[int, int]) -> None:
    velocity = VectorField(CartesianMesh(nx=3, ny=2))
    solver = PressureCorrectionSolver(
        density=1.0, time_step=0.1, reference_cell=reference_cell
    )

    with pytest.raises(ValueError, match="outside the mesh"):
        solver.assemble(velocity)
