import numpy as np
import pytest

from fvm import (
    CartesianMesh,
    ScalarField,
    VectorField,
    convection_operator,
    convective_fluxes,
    diffusion_operator,
    diffusive_fluxes,
    divergence,
    face_gradient,
    interpolate_to_faces,
)


def _linear_boundary_values(mesh: CartesianMesh) -> dict[str, np.ndarray]:
    return {
        "west": 3.0 * mesh.y_cell_centers,
        "east": 2.0 * mesh.width + 3.0 * mesh.y_cell_centers,
        "south": 2.0 * mesh.x_cell_centers,
        "north": 2.0 * mesh.x_cell_centers + 3.0 * mesh.height,
    }


def _quadratic_boundary_values(mesh: CartesianMesh) -> dict[str, np.ndarray]:
    x = mesh.x_cell_centers
    y = mesh.y_cell_centers
    return {
        "west": y**2,
        "east": mesh.width**2 + y**2,
        "south": x**2,
        "north": x**2 + mesh.height**2,
    }


def test_interpolation_is_exact_for_a_linear_field_with_face_values() -> None:
    mesh = CartesianMesh(nx=5, ny=3, width=2.0, height=1.5)
    x, y = mesh.cell_center_coordinates
    field = ScalarField(mesh, name="linear")
    field.set_values(2.0 * x + 3.0 * y)

    face_x, face_y = interpolate_to_faces(field, _linear_boundary_values(mesh))
    u_x, u_y = mesh.u_face_coordinates
    v_x, v_y = mesh.v_face_coordinates

    np.testing.assert_allclose(face_x, 2.0 * u_x + 3.0 * u_y)
    np.testing.assert_allclose(face_y, 2.0 * v_x + 3.0 * v_y)


def test_interpolation_defaults_to_nearest_cell_at_boundaries() -> None:
    field = ScalarField(CartesianMesh(nx=2, ny=2), name="field")
    field.set_values([[1.0, 3.0], [5.0, 7.0]])

    face_x, face_y = interpolate_to_faces(field)

    np.testing.assert_allclose(face_x[:, 0], [1.0, 5.0])
    np.testing.assert_allclose(face_x[:, -1], [3.0, 7.0])
    np.testing.assert_allclose(face_x[:, 1], [2.0, 6.0])
    np.testing.assert_allclose(face_y[0, :], [1.0, 3.0])
    np.testing.assert_allclose(face_y[-1, :], [5.0, 7.0])


def test_face_gradient_matches_linear_field_and_zero_gradient_defaults() -> None:
    mesh = CartesianMesh(nx=4, ny=3, width=2.0, height=1.5)
    x, y = mesh.cell_center_coordinates
    field = ScalarField(mesh, name="linear")
    field.set_values(2.0 * x + 3.0 * y)

    gradient_x, gradient_y = face_gradient(field, _linear_boundary_values(mesh))
    np.testing.assert_allclose(gradient_x, 2.0)
    np.testing.assert_allclose(gradient_y, 3.0)

    neumann_x, neumann_y = face_gradient(field)
    assert np.all(neumann_x[:, 0] == 0.0)
    assert np.all(neumann_x[:, -1] == 0.0)
    assert np.all(neumann_y[0, :] == 0.0)
    assert np.all(neumann_y[-1, :] == 0.0)


def test_velocity_divergence_is_exact_for_linear_face_velocity() -> None:
    mesh = CartesianMesh(nx=5, ny=3, width=2.0, height=1.5)
    velocity = VectorField(mesh)
    u_x, _ = mesh.u_face_coordinates
    _, v_y = mesh.v_face_coordinates
    velocity.set_values(u_x, v_y)

    np.testing.assert_allclose(divergence(velocity), 2.0)


def test_quadratic_diffusion_operator_returns_analytic_laplacian() -> None:
    mesh = CartesianMesh(nx=7, ny=4, width=2.0, height=1.5)
    x, y = mesh.cell_center_coordinates
    field = ScalarField(mesh, name="quadratic")
    field.set_values(x**2 + y**2)

    actual = diffusion_operator(field, boundary_values=_quadratic_boundary_values(mesh))

    np.testing.assert_allclose(actual, 4.0, atol=1e-12)


def test_diffusive_fluxes_apply_diffusivity_and_zero_flux_boundaries() -> None:
    mesh = CartesianMesh(nx=3, ny=2)
    x, y = mesh.cell_center_coordinates
    field = ScalarField(mesh, name="linear")
    field.set_values(2.0 * x + 3.0 * y)

    flux_x, flux_y = diffusive_fluxes(field, diffusivity=0.5)

    np.testing.assert_allclose(flux_x[:, 1:-1], 1.0)
    np.testing.assert_allclose(flux_y[1:-1, :], 1.5)
    assert np.all(flux_x[:, (0, -1)] == 0.0)
    assert np.all(flux_y[(0, -1), :] == 0.0)


def test_diffusion_operator_is_second_order_under_grid_refinement() -> None:
    def rms_error(cells: int) -> float:
        mesh = CartesianMesh(nx=cells, ny=cells)
        x, y = mesh.cell_center_coordinates
        field = ScalarField(mesh, name="manufactured")
        exact = np.sin(np.pi * x) * np.sin(np.pi * y)
        field.set_values(exact)
        numerical = diffusion_operator(
            field,
            boundary_values={side: 0.0 for side in ("west", "east", "south", "north")},
        )
        analytical = -2.0 * np.pi**2 * exact
        return float(np.sqrt(np.mean((numerical - analytical) ** 2)))

    coarse_error = rms_error(32)
    fine_error = rms_error(64)

    assert coarse_error / fine_error > 3.5


@pytest.mark.parametrize("scheme", ["central", "upwind"])
def test_constant_scalar_convection_matches_scalar_times_divergence(scheme: str) -> None:
    mesh = CartesianMesh(nx=4, ny=3, width=2.0, height=1.5)
    scalar = ScalarField(mesh, name="constant", initial_value=2.0)
    velocity = VectorField(mesh)
    u_x, _ = mesh.u_face_coordinates
    _, v_y = mesh.v_face_coordinates
    velocity.set_values(u_x, v_y)
    boundary_values = {side: 2.0 for side in ("west", "east", "south", "north")}

    actual = convection_operator(scalar, velocity, scheme, boundary_values)

    np.testing.assert_allclose(actual, 2.0 * divergence(velocity))


def test_upwind_flux_uses_upstream_cell_and_inflow_boundary_value() -> None:
    mesh = CartesianMesh(nx=2, ny=1)
    scalar = ScalarField(mesh, name="scalar")
    scalar.set_values([[1.0, 3.0]])
    velocity = VectorField(mesh)
    velocity.set_values([[2.0, 2.0, 2.0]], [[0.0, 0.0], [0.0, 0.0]])

    flux_x, _ = convective_fluxes(
        scalar,
        velocity,
        scheme="upwind",
        boundary_values={"west": 5.0},
    )

    np.testing.assert_allclose(flux_x, [[10.0, 2.0, 6.0]])


def test_operators_reject_invalid_meshes_boundaries_and_schemes() -> None:
    mesh = CartesianMesh(nx=2, ny=2)
    field = ScalarField(mesh, name="scalar")
    velocity = VectorField(mesh)

    with pytest.raises(ValueError, match="same mesh"):
        convection_operator(field, VectorField(CartesianMesh(nx=3, ny=2)))
    with pytest.raises(ValueError, match="boundary values must be scalar or have shape"):
        interpolate_to_faces(field, {"west": [1.0, 2.0, 3.0]})
    with pytest.raises(ValueError, match="unknown boundary"):
        face_gradient(field, {"top": 0.0})
    with pytest.raises(ValueError, match="scheme"):
        convective_fluxes(field, velocity, scheme="central-upwind")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="diffusivity"):
        diffusion_operator(field, diffusivity=-1.0)
