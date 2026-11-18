import json

import matplotlib
import numpy as np
import pytest

matplotlib.use("Agg")

from fvm import (
    BoundaryConditions,
    CartesianMesh,
    MovingWall,
    NoSlipWall,
    ScalarField,
    TransientSolver,
    VectorField,
    centerline_profiles,
    compare_ghia_re100,
    export_ghia_comparison,
    export_simulation_result,
    plot_cavity_fields,
    plot_convergence_history,
    plot_ghia_comparison,
    plot_mesh_and_boundaries,
    run_lid_driven_grid_study,
    velocity_extrema,
    write_grid_study_csv,
)


def _conditions(lid_speed: float = 1.0) -> BoundaryConditions:
    conditions = BoundaryConditions()
    for side in ("west", "east", "south", "north"):
        if side == "north":
            conditions.set("velocity", side, MovingWall((lid_speed, 0.0)))
        else:
            conditions.set("velocity", side, NoSlipWall())
    return conditions


def _run_cavity(cells: int, max_steps: int = 2):
    mesh = CartesianMesh(nx=cells, ny=cells)
    solver = TransientSolver(
        density=1.0,
        viscosity=0.01,
        max_time_step=0.001,
        max_steps=max_steps,
        velocity_tolerance=1e-14,
    )
    return solver.run(
        VectorField(mesh),
        ScalarField(mesh, name="pressure"),
        _conditions(),
    )


def test_centerline_extraction_interpolates_mac_fields_to_exact_lines() -> None:
    mesh = CartesianMesh(nx=6, ny=4, width=2.0, height=1.0)
    velocity = VectorField(mesh)
    u_values = np.broadcast_to(3.0 * mesh.y_cell_centers[:, None], (mesh.ny, mesh.nx + 1))
    v_values = np.broadcast_to(2.0 * mesh.x_cell_centers[None, :], (mesh.ny + 1, mesh.nx))
    velocity.set_values(u_values, v_values)

    profiles = centerline_profiles(velocity)

    np.testing.assert_allclose(profiles.u_y, mesh.y_cell_centers)
    np.testing.assert_allclose(profiles.u, 3.0 * mesh.y_cell_centers)
    np.testing.assert_allclose(profiles.v_x, mesh.x_cell_centers)
    np.testing.assert_allclose(profiles.v, 2.0 * mesh.x_cell_centers)


def test_ghia_comparison_excludes_wall_endpoints_and_marks_uncapped_status() -> None:
    simulation = _run_cavity(cells=16, max_steps=1)

    comparison = compare_ghia_re100(simulation)

    assert not comparison.benchmark_valid
    assert len(comparison.u_coordinate) == 14
    assert len(comparison.v_coordinate) == 15
    assert np.all((comparison.u_coordinate > 0.0) & (comparison.u_coordinate < 1.0))
    assert np.all((comparison.v_coordinate > 0.0) & (comparison.v_coordinate < 1.0))
    assert np.isfinite(comparison.u_rms_error)
    assert np.isfinite(comparison.v_rms_error)


def test_velocity_extrema_include_component_and_speed_locations() -> None:
    mesh = CartesianMesh(nx=3, ny=2, width=2.0, height=1.0)
    velocity = VectorField(mesh)
    u_values = np.zeros(mesh.shape_for_location("x_face"))
    v_values = np.zeros(mesh.shape_for_location("y_face"))
    u_values[0, 0] = -2.0
    u_values[-1, -1] = 3.0
    v_values[0, 0] = -4.0
    v_values[-1, -1] = 5.0
    velocity.set_values(u_values, v_values)

    extrema = velocity_extrema(velocity)

    assert extrema.u.minimum == -2.0
    assert extrema.u.maximum == 3.0
    assert extrema.v.minimum == -4.0
    assert extrema.v.maximum == 5.0
    assert extrema.maximum_speed > 0.0
    assert len(extrema.maximum_speed_location) == 2


def test_simulation_export_contains_fields_settings_and_history(tmp_path) -> None:
    simulation = _run_cavity(cells=4, max_steps=1)

    output = export_simulation_result(simulation, tmp_path / "run")

    with np.load(output / "fields.npz") as fields:
        assert fields["pressure"].shape == (4, 4)
        assert fields["u_faces"].shape == (4, 5)
        assert fields["v_faces"].shape == (5, 4)
    metadata = json.loads((output / "metadata.json").read_text(encoding="utf-8"))
    assert metadata["settings"]["density"] == 1.0
    assert metadata["steps"] == 1
    assert (output / "history.csv").read_text(encoding="utf-8").count("\n") == 2


def test_matplotlib_plots_save_field_profile_and_history_figures(tmp_path) -> None:
    simulation = _run_cavity(cells=16, max_steps=1)
    comparison = compare_ghia_re100(simulation)

    field_figure = plot_cavity_fields(simulation, tmp_path / "fields.png")
    profile_figure = plot_ghia_comparison(comparison, tmp_path / "profiles.png")
    history_figure = plot_convergence_history(simulation, tmp_path / "history.png")

    assert len(field_figure.axes) >= 3
    assert len(profile_figure.axes) == 2
    assert len(history_figure.axes) == 1
    assert all((tmp_path / name).stat().st_size > 1000 for name in (
        "fields.png", "profiles.png", "history.png"
    ))


def test_geometry_plot_shows_mesh_and_moving_wall(tmp_path) -> None:
    mesh = CartesianMesh(nx=4, ny=4)

    figure = plot_mesh_and_boundaries(
        mesh,
        _conditions(),
        tmp_path / "geometry.png",
    )

    assert len(figure.axes) == 1
    assert (tmp_path / "geometry.png").stat().st_size > 1000


def test_grid_study_records_nonconvergence_and_writes_csv(tmp_path) -> None:
    rows = run_lid_driven_grid_study(
        grid_sizes=(16,),
        max_steps=1,
        velocity_tolerance=1e-14,
    )

    assert len(rows) == 1
    assert rows[0].cells_per_side == 16
    assert not rows[0].benchmark_valid
    assert np.isfinite(rows[0].u_rms_error)
    output = write_grid_study_csv(rows, tmp_path / "study.csv")
    assert "cells_per_side" in output.read_text(encoding="utf-8")


def test_ghia_comparison_rejects_non_square_domain() -> None:
    mesh = CartesianMesh(nx=16, ny=16, width=2.0, height=1.0)
    solver = TransientSolver(1.0, 0.01, max_time_step=0.001, max_steps=1)
    result = solver.run(VectorField(mesh), ScalarField(mesh, "pressure"), _conditions())

    with pytest.raises(ValueError, match="square domain"):
        compare_ghia_re100(result)


def test_ghia_comparison_rejects_a_non_re100_run() -> None:
    mesh = CartesianMesh(nx=16, ny=16)
    solver = TransientSolver(1.0, 0.02, max_time_step=0.001, max_steps=1)
    result = solver.run(VectorField(mesh), ScalarField(mesh, "pressure"), _conditions())

    with pytest.raises(ValueError, match="requires Reynolds number 100"):
        compare_ghia_re100(result)


def test_ghia_report_exports_comparison_eligibility(tmp_path) -> None:
    comparison = compare_ghia_re100(_run_cavity(cells=16, max_steps=1))

    report_path = export_ghia_comparison(comparison, tmp_path / "ghia.json")

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["benchmark"] == "Ghia et al. lid-driven cavity Re=100"
    assert report["benchmark_valid"] is False
    assert len(report["u_profile"]) == 14