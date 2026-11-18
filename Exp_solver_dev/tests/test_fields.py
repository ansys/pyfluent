import numpy as np
import pytest

from fvm import CartesianMesh, ScalarField, VectorField


def test_scalar_field_uses_requested_mesh_location() -> None:
    mesh = CartesianMesh(nx=3, ny=2)
    pressure = ScalarField(mesh, name="pressure", initial_value=4.5)
    x_face_scalar = ScalarField(mesh, name="face_data", location="x_face")
    y_face_scalar = ScalarField(mesh, name="face_data_y", location="y_face")

    assert pressure.values.shape == (2, 3)
    assert x_face_scalar.values.shape == (2, 4)
    assert y_face_scalar.values.shape == (3, 3)
    np.testing.assert_array_equal(pressure.values, np.full((2, 3), 4.5))


def test_scalar_field_replaces_values_with_a_copy() -> None:
    field = ScalarField(CartesianMesh(nx=2, ny=2), name="pressure")
    values = np.arange(4, dtype=np.float64).reshape(2, 2)

    field.set_values(values)
    values[0, 0] = 100.0

    assert field.values[0, 0] == 0.0
    np.testing.assert_array_equal(field.values, [[0.0, 1.0], [2.0, 3.0]])


def test_scalar_field_rejects_wrong_shape_and_non_finite_values() -> None:
    field = ScalarField(CartesianMesh(nx=2, ny=2), name="pressure")

    with pytest.raises(ValueError, match="shape"):
        field.set_values(np.zeros((4,)))
    with pytest.raises(ValueError, match="finite"):
        field.set_values(np.full((2, 2), np.nan))


def test_vector_field_has_mac_component_shapes_and_initial_values() -> None:
    velocity = VectorField(CartesianMesh(nx=3, ny=2), initial_value=(1.0, -2.0))

    assert velocity.u.values.shape == (2, 4)
    assert velocity.v.values.shape == (3, 3)
    np.testing.assert_array_equal(velocity.u.values, np.ones((2, 4)))
    np.testing.assert_array_equal(velocity.v.values, np.full((3, 3), -2.0))


def test_vector_field_updates_both_components_together() -> None:
    velocity = VectorField(CartesianMesh(nx=2, ny=2))
    u_values = np.full((2, 3), 1.0)
    v_values = np.full((3, 2), -1.0)

    velocity.set_values(u_values, v_values)
    np.testing.assert_array_equal(velocity.u.values, u_values)
    np.testing.assert_array_equal(velocity.v.values, v_values)

    previous_u = velocity.u.values.copy()
    with pytest.raises(ValueError, match="shape"):
        velocity.set_values(np.zeros((2, 3)), np.zeros((2, 2)))
    np.testing.assert_array_equal(velocity.u.values, previous_u)


def test_re100_cavity_mesh_and_initial_velocity() -> None:
    mesh = CartesianMesh(nx=64, ny=64, width=1.0, height=1.0)
    velocity = VectorField(mesh)

    assert mesh.cell_area * mesh.nx * mesh.ny == pytest.approx(1.0)
    assert velocity.u.values.shape == (64, 65)
    assert velocity.v.values.shape == (65, 64)
    assert np.count_nonzero(velocity.u.values) == 0
    assert np.count_nonzero(velocity.v.values) == 0