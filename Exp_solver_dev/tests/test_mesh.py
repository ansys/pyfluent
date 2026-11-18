import numpy as np
import pytest

from fvm import BOUNDARY_NAMES, CartesianMesh


def test_mesh_dimensions_coordinates_and_areas() -> None:
    mesh = CartesianMesh(nx=4, ny=2, width=2.0, height=1.0)

    assert mesh.dx == pytest.approx(0.5)
    assert mesh.dy == pytest.approx(0.5)
    np.testing.assert_allclose(mesh.x_cell_centers, [0.25, 0.75, 1.25, 1.75])
    np.testing.assert_allclose(mesh.y_cell_centers, [0.25, 0.75])
    np.testing.assert_allclose(mesh.x_face_centers, [0.0, 0.5, 1.0, 1.5, 2.0])
    np.testing.assert_allclose(mesh.y_face_centers, [0.0, 0.5, 1.0])

    cell_x, cell_y = mesh.cell_center_coordinates
    u_x, u_y = mesh.u_face_coordinates
    v_x, v_y = mesh.v_face_coordinates
    assert cell_x.shape == cell_y.shape == (2, 4)
    assert u_x.shape == u_y.shape == (2, 5)
    assert v_x.shape == v_y.shape == (3, 4)
    assert mesh.cell_area * mesh.nx * mesh.ny == pytest.approx(2.0)
    assert mesh.u_face_area == pytest.approx(0.5)
    assert mesh.v_face_area == pytest.approx(0.5)
    assert mesh.cell_areas.shape == (2, 4)
    assert mesh.u_face_areas.shape == (2, 5)
    assert mesh.v_face_areas.shape == (3, 4)


def test_boundary_face_indices_and_normals() -> None:
    mesh = CartesianMesh(nx=3, ny=2)
    faces = mesh.boundary_face_indices

    np.testing.assert_array_equal(faces["west"][0], [0, 1])
    np.testing.assert_array_equal(faces["west"][1], [0, 0])
    np.testing.assert_array_equal(faces["east"][1], [3, 3])
    np.testing.assert_array_equal(faces["south"][0], [0, 0, 0])
    np.testing.assert_array_equal(faces["north"][0], [2, 2, 2])
    assert dict(mesh.boundary_face_counts) == {
        "west": 2,
        "east": 2,
        "south": 3,
        "north": 3,
    }
    assert set(mesh.boundary_face_normals) == set(BOUNDARY_NAMES)
    assert mesh.boundary_face_normals["north"] == (0.0, 1.0)


@pytest.mark.parametrize("nx, ny", [(0, 2), (2, 0), (-1, 2)])
def test_mesh_rejects_non_positive_cell_counts(nx: int, ny: int) -> None:
    with pytest.raises(ValueError):
        CartesianMesh(nx=nx, ny=ny)


@pytest.mark.parametrize("width, height", [(0.0, 1.0), (1.0, -1.0), (float("inf"), 1.0)])
def test_mesh_rejects_invalid_domain_size(width: float, height: float) -> None:
    with pytest.raises(ValueError):
        CartesianMesh(nx=2, ny=2, width=width, height=height)


def test_mesh_rejects_non_integer_cell_count() -> None:
    with pytest.raises(TypeError):
        CartesianMesh(nx=2.5, ny=2)  # type: ignore[arg-type]