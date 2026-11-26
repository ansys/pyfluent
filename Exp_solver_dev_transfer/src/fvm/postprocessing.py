"""Post-processing, Ghia benchmark comparison, plots, and result export.

The Re=100 reference profiles below are transcribed from Ghia, Ghia, and Shin,
Journal of Computational Physics 48 (1982), 387-411,
doi:10.1016/0021-9991(82)90058-4. Wall endpoints are retained in the source
tables but excluded from RMS comparisons because the lid velocity is
discontinuous at the two upper corners and boundary values are not interior
centerline samples.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass, fields
from math import isfinite
from numbers import Integral, Real
from pathlib import Path
from typing import Sequence

import numpy as np

from .boundary_conditions import BoundaryConditions, MovingWall, NoSlipWall
from .fields import ScalarField, VectorField
from .mesh import BOUNDARY_NAMES, CartesianMesh, FloatArray
from .simulation import SimulationResult, StepDiagnostics, TransientSolver

# Coordinates are normalized and sorted from the lower wall to the upper/right wall.
GHIA_RE100_U_PROFILE = (
    (0.0000, 0.00000),
    (0.0625, -0.04192),
    (0.0703, -0.04775),
    (0.1016, -0.06434),
    (0.1719, -0.10150),
    (0.2813, -0.15662),
    (0.4531, -0.21090),
    (0.5000, -0.20581),
    (0.6172, -0.13641),
    (0.7344, 0.00332),
    (0.8516, 0.23151),
    (0.9531, 0.68717),
    (0.9609, 0.73722),
    (0.9688, 0.78871),
    (0.9766, 0.84123),
    (1.0000, 1.00000),
)
GHIA_RE100_V_PROFILE = (
    (0.0000, 0.00000),
    (0.0625, 0.09233),
    (0.0703, 0.10091),
    (0.0781, 0.10890),
    (0.0938, 0.12317),
    (0.1563, 0.16077),
    (0.2266, 0.17507),
    (0.2344, 0.17527),
    (0.5000, 0.05454),
    (0.8047, -0.24533),
    (0.8594, -0.22445),
    (0.9063, -0.16914),
    (0.9453, -0.10313),
    (0.9531, -0.08864),
    (0.9609, -0.07391),
    (0.9688, -0.05906),
    (1.0000, 0.00000),
)


@dataclass(frozen=True, slots=True)
class CenterlineProfiles:
    """Physical centerline coordinates and velocities interpolated from MAC data."""

    u_y: FloatArray
    u: FloatArray
    v_x: FloatArray
    v: FloatArray


@dataclass(frozen=True, slots=True)
class GhiaComparison:
    """Interior-point Re=100 profile comparison in nondimensional coordinates."""

    u_coordinate: FloatArray
    u_reference: FloatArray
    u_computed: FloatArray
    v_coordinate: FloatArray
    v_reference: FloatArray
    v_computed: FloatArray
    u_rms_error: float
    v_rms_error: float
    simulation_converged: bool
    steady_solution: bool

    @property
    def benchmark_valid(self) -> bool:
        """Only a converged steady solution is eligible for benchmark acceptance."""
        return self.simulation_converged and self.steady_solution


@dataclass(frozen=True, slots=True)
class ComponentExtrema:
    """Minimum and maximum of one velocity component and their coordinates."""

    minimum: float
    minimum_location: tuple[float, float]
    maximum: float
    maximum_location: tuple[float, float]


@dataclass(frozen=True, slots=True)
class VelocityExtrema:
    """Component extrema plus maximum cell-centered speed."""

    u: ComponentExtrema
    v: ComponentExtrema
    maximum_speed: float
    maximum_speed_location: tuple[float, float]


@dataclass(frozen=True, slots=True)
class GridStudyRow:
    """One grid's Re=100 run status and centerline errors."""

    cells_per_side: int
    converged: bool
    steps: int
    final_time: float
    u_rms_error: float
    v_rms_error: float
    max_divergence: float
    global_mass_imbalance: float

    @property
    def benchmark_valid(self) -> bool:
        """A grid result is benchmark-valid only if its run converged."""
        return self.converged


def _velocity_arrays(velocity: VectorField) -> tuple[FloatArray, FloatArray]:
    """Validate face-array shapes and values before post-processing."""
    if not isinstance(velocity, VectorField):
        raise TypeError("velocity must be a VectorField")
    mesh = velocity.mesh
    u = np.asarray(velocity.u.values, dtype=np.float64)
    v = np.asarray(velocity.v.values, dtype=np.float64)
    if u.shape != mesh.shape_for_location("x_face"):
        raise ValueError("u values have an invalid shape")
    if v.shape != mesh.shape_for_location("y_face"):
        raise ValueError("v values have an invalid shape")
    if not np.all(np.isfinite(u)) or not np.all(np.isfinite(v)):
        raise ValueError("velocity values must all be finite")
    return u, v


def centerline_profiles(velocity: VectorField) -> CenterlineProfiles:
    """Interpolate staggered components onto the geometric cavity centerlines.

    ``u`` is interpolated in x from vertical faces to `x=width/2`; ``v`` is
    interpolated in y from horizontal faces to `y=height/2`. The returned
    profile coordinates remain physical distances, not normalized values.
    """
    u_values, v_values = _velocity_arrays(velocity)
    mesh = velocity.mesh
    center_x = 0.5 * mesh.width
    center_y = 0.5 * mesh.height
    u_centerline = np.array(
        [np.interp(center_x, mesh.x_face_centers, row) for row in u_values],
        dtype=np.float64,
    )
    v_centerline = np.array(
        [np.interp(center_y, mesh.y_face_centers, v_values[:, column])
         for column in range(mesh.nx)],
        dtype=np.float64,
    )
    return CenterlineProfiles(
        u_y=mesh.y_cell_centers.copy(),
        u=u_centerline,
        v_x=mesh.x_cell_centers.copy(),
        v=v_centerline,
    )


def compare_ghia_re100(
    simulation: SimulationResult, lid_speed: float = 1.0
) -> GhiaComparison:
    """Compare a simulation's centerlines with Ghia's Re=100 tabulated profiles.

    Wall endpoints are deliberately omitted. The RMS errors use interpolated,
    dimensionless numerical velocities at the interior reference coordinates.
    Results from a run capped before convergence are returned for inspection,
    but ``benchmark_valid`` remains false.
    """
    if not isinstance(simulation, SimulationResult):
        raise TypeError("simulation must be a SimulationResult")
    if isinstance(lid_speed, bool) or not isinstance(lid_speed, Real):
        raise TypeError("lid_speed must be a finite positive number")
    if not isfinite(lid_speed) or lid_speed <= 0.0:
        raise ValueError("lid_speed must be a finite positive number")
    mesh = simulation.velocity.mesh
    if not np.isclose(mesh.width, mesh.height):
        raise ValueError("Ghia cavity comparison requires a square domain")
    viscosity = simulation.settings.viscosity
    reynolds_number = (
        simulation.settings.density * lid_speed * mesh.width / viscosity
        if viscosity > 0.0
        else 0.0
    )
    if not np.isclose(reynolds_number, 100.0, rtol=1e-8, atol=1e-10):
        raise ValueError(
            f"Ghia comparison requires Reynolds number 100, got {reynolds_number:.6g}"
        )

    profiles = centerline_profiles(simulation.velocity)
    u_reference = np.asarray(GHIA_RE100_U_PROFILE, dtype=np.float64)
    v_reference = np.asarray(GHIA_RE100_V_PROFILE, dtype=np.float64)
    u_interior = (u_reference[:, 0] > 0.0) & (u_reference[:, 0] < 1.0)
    v_interior = (v_reference[:, 0] > 0.0) & (v_reference[:, 0] < 1.0)
    u_coordinates = u_reference[u_interior, 0]
    v_coordinates = v_reference[v_interior, 0]

    # Wall values are used only to interpolate nearby interior reference points;
    # the wall endpoints themselves are not included in the RMS comparisons.
    u_grid = np.concatenate(([0.0], profiles.u_y / mesh.height, [1.0]))
    u_values = np.concatenate(([0.0], profiles.u / lid_speed, [1.0]))
    v_grid = np.concatenate(([0.0], profiles.v_x / mesh.width, [1.0]))
    v_values = np.concatenate(([0.0], profiles.v / lid_speed, [0.0]))
    if (
        u_coordinates[0] < u_grid[0]
        or u_coordinates[-1] > u_grid[-1]
        or v_coordinates[0] < v_grid[0]
        or v_coordinates[-1] > v_grid[-1]
    ):
        raise ValueError("mesh is too coarse to interpolate all interior Ghia points")

    u_reference_values = u_reference[u_interior, 1]
    v_reference_values = v_reference[v_interior, 1]
    u_computed = np.interp(u_coordinates, u_grid, u_values)
    v_computed = np.interp(v_coordinates, v_grid, v_values)
    return GhiaComparison(
        u_coordinate=u_coordinates,
        u_reference=u_reference_values,
        u_computed=u_computed,
        v_coordinate=v_coordinates,
        v_reference=v_reference_values,
        v_computed=v_computed,
        u_rms_error=float(np.sqrt(np.mean((u_computed - u_reference_values) ** 2))),
        v_rms_error=float(np.sqrt(np.mean((v_computed - v_reference_values) ** 2))),
        simulation_converged=simulation.converged,
        steady_solution=(
            not simulation.settings.transient or simulation.settings.end_time is None
        ),
    )


def velocity_extrema(velocity: VectorField) -> VelocityExtrema:
    """Find component extrema and maximum speed after averaging to cell centers."""
    u_values, v_values = _velocity_arrays(velocity)
    mesh = velocity.mesh
    u_x, u_y = mesh.u_face_coordinates
    v_x, v_y = mesh.v_face_coordinates

    u_min_index = np.unravel_index(np.argmin(u_values), u_values.shape)
    u_max_index = np.unravel_index(np.argmax(u_values), u_values.shape)
    v_min_index = np.unravel_index(np.argmin(v_values), v_values.shape)
    v_max_index = np.unravel_index(np.argmax(v_values), v_values.shape)

    u_center = 0.5 * (u_values[:, :-1] + u_values[:, 1:])
    v_center = 0.5 * (v_values[:-1, :] + v_values[1:, :])
    speed = np.hypot(u_center, v_center)
    speed_index = np.unravel_index(np.argmax(speed), speed.shape)
    cell_x, cell_y = mesh.cell_center_coordinates

    return VelocityExtrema(
        u=ComponentExtrema(
            minimum=float(u_values[u_min_index]),
            minimum_location=(float(u_x[u_min_index]), float(u_y[u_min_index])),
            maximum=float(u_values[u_max_index]),
            maximum_location=(float(u_x[u_max_index]), float(u_y[u_max_index])),
        ),
        v=ComponentExtrema(
            minimum=float(v_values[v_min_index]),
            minimum_location=(float(v_x[v_min_index]), float(v_y[v_min_index])),
            maximum=float(v_values[v_max_index]),
            maximum_location=(float(v_x[v_max_index]), float(v_y[v_max_index])),
        ),
        maximum_speed=float(speed[speed_index]),
        maximum_speed_location=(
            float(cell_x[speed_index]),
            float(cell_y[speed_index]),
        ),
    )


def plot_mesh_and_boundaries(
    mesh: CartesianMesh,
    boundary_conditions: BoundaryConditions,
    output_path: str | Path | None = None,
) -> object:
    """Draw the rectangle, Cartesian grid, and prescribed wall directions."""
    import matplotlib.pyplot as plt

    if not isinstance(mesh, CartesianMesh):
        raise TypeError("mesh must be a CartesianMesh")
    if not isinstance(boundary_conditions, BoundaryConditions):
        raise TypeError("boundary_conditions must be BoundaryConditions")

    figure, axis = plt.subplots(figsize=(6, 6), layout="constrained")
    for x_coordinate in mesh.x_face_centers:
        axis.axvline(x_coordinate, color="#cbd5e1", linewidth=0.7, zorder=0)
    for y_coordinate in mesh.y_face_centers:
        axis.axhline(y_coordinate, color="#cbd5e1", linewidth=0.7, zorder=0)
    axis.plot(
        [0.0, mesh.width, mesh.width, 0.0, 0.0],
        [0.0, 0.0, mesh.height, mesh.height, 0.0],
        color="#1f2937",
        linewidth=2.0,
        zorder=2,
    )

    for side in BOUNDARY_NAMES:
        condition = boundary_conditions.get("velocity", side)
        if isinstance(condition, MovingWall):
            u_wall, v_wall = condition.velocity
            magnitude = float(np.hypot(u_wall, v_wall))
            if magnitude > 0.0:
                arrow_length = 0.22 * min(mesh.width, mesh.height)
                dx = arrow_length * u_wall / magnitude
                dy = arrow_length * v_wall / magnitude
                if side in ("west", "east"):
                    inset = 0.025 * min(mesh.width, mesh.height)
                    start_x = inset if side == "west" else mesh.width - inset
                    start_y = 0.5 * (mesh.height - dy)
                else:
                    start_x = 0.5 * (mesh.width - dx)
                    inset = 0.025 * min(mesh.width, mesh.height)
                    start_y = inset if side == "south" else mesh.height - inset
                axis.quiver(
                    start_x,
                    start_y,
                    dx,
                    dy,
                    angles="xy",
                    scale_units="xy",
                    scale=1.0,
                    color="#d1495b",
                    width=0.009,
                    zorder=3,
                    label=f"{side} moving wall ({magnitude:g} m/s)",
                )
        elif isinstance(condition, NoSlipWall):
            inset = 0.035 * min(mesh.width, mesh.height)
            label_locations = {
                "west": (inset, 0.5 * mesh.height, 90.0),
                "east": (mesh.width - inset, 0.5 * mesh.height, 90.0),
                "south": (0.5 * mesh.width, inset, 0.0),
                "north": (0.5 * mesh.width, mesh.height - inset, 0.0),
            }
            label_x, label_y, angle = label_locations[side]
            axis.text(
                label_x,
                label_y,
                "no-slip",
                rotation=angle,
                color="#475569",
                fontsize=8,
                ha="center",
                va="center",
                backgroundcolor="white",
                zorder=4,
            )
        else:
            raise ValueError(f"unsupported velocity boundary condition on {side}")

    axis.set_xlim(0.0, mesh.width)
    axis.set_ylim(0.0, mesh.height)
    axis.set_aspect("equal")
    axis.set_xlabel("x (m)")
    axis.set_ylabel("y (m)")
    axis.set_title(f"Domain and uniform Cartesian mesh ({mesh.nx} x {mesh.ny})")
    handles, labels = axis.get_legend_handles_labels()
    if handles:
        axis.legend(handles, labels, loc="lower right")
    return _finish_figure(figure, output_path)


def export_simulation_result(
    simulation: SimulationResult, output_directory: str | Path
) -> Path:
    """Write compressed fields, run metadata, and per-step history to a folder."""
    if not isinstance(simulation, SimulationResult):
        raise TypeError("simulation must be a SimulationResult")
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    mesh = simulation.velocity.mesh
    u_values, v_values = _velocity_arrays(simulation.velocity)
    cell_u = 0.5 * (u_values[:, :-1] + u_values[:, 1:])
    cell_v = 0.5 * (v_values[:-1, :] + v_values[1:, :])

    np.savez_compressed(
        output / "fields.npz",
        x_cell_centers=mesh.x_cell_centers,
        y_cell_centers=mesh.y_cell_centers,
        x_face_centers=mesh.x_face_centers,
        y_face_centers=mesh.y_face_centers,
        pressure=simulation.pressure.values,
        u_faces=u_values,
        v_faces=v_values,
        u_cell_centers=cell_u,
        v_cell_centers=cell_v,
    )

    metadata = {
        "format_version": 1,
        "mesh": {
            "nx": mesh.nx,
            "ny": mesh.ny,
            "width": mesh.width,
            "height": mesh.height,
        },
        "settings": asdict(simulation.settings),
        "converged": simulation.converged,
        "termination_reason": simulation.termination_reason,
        "steps": simulation.steps,
        "final_time": simulation.final_time,
        "final_pseudo_time": simulation.final_pseudo_time,
        "temporal_mode": "transient" if simulation.settings.transient else "steady",
        "velocity_extrema": asdict(velocity_extrema(simulation.velocity)),
    }
    with (output / "metadata.json").open("w", encoding="utf-8") as metadata_file:
        json.dump(metadata, metadata_file, indent=2)

    history_fields = [field.name for field in fields(StepDiagnostics)]
    with (output / "history.csv").open("w", newline="", encoding="utf-8") as history_file:
        writer = csv.DictWriter(history_file, fieldnames=history_fields)
        writer.writeheader()
        writer.writerows(asdict(item) for item in simulation.history)
    return output


def _finish_figure(figure: object, output_path: str | Path | None) -> object:
    """Save a Matplotlib figure when requested and return it for customization."""
    if output_path is not None:
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(output, dpi=160, bbox_inches="tight")
    return figure


def plot_cavity_fields(
    simulation: SimulationResult, output_path: str | Path | None = None
) -> object:
    """Plot cell-centered speed, pressure, and streamlines for a cavity result."""
    import matplotlib.pyplot as plt
    from matplotlib.colors import TwoSlopeNorm

    mesh = simulation.velocity.mesh
    u_values, v_values = _velocity_arrays(simulation.velocity)
    cell_u = 0.5 * (u_values[:, :-1] + u_values[:, 1:])
    cell_v = 0.5 * (v_values[:-1, :] + v_values[1:, :])
    speed = np.hypot(cell_u, cell_v)
    vorticity = np.gradient(cell_v, mesh.dx, axis=1) - np.gradient(
        cell_u, mesh.dy, axis=0
    )
    x, y = mesh.x_cell_centers, mesh.y_cell_centers
    figure, axes = plt.subplots(2, 2, figsize=(11, 8), layout="constrained")
    speed_axis, pressure_axis, streamline_axis, vorticity_axis = axes.flat

    speed_max = float(np.max(speed))
    if speed_max > 0.0:
        speed_plot = speed_axis.contourf(
            x,
            y,
            speed,
            levels=np.linspace(0.0, speed_max, 33),
            cmap="viridis",
        )
    else:
        speed_plot = speed_axis.pcolormesh(
            x, y, speed, shading="nearest", cmap="viridis", vmin=0.0, vmax=1.0
        )
    figure.colorbar(speed_plot, ax=speed_axis, label="Speed (m/s)")
    speed_axis.set_title("Velocity magnitude")

    pressure = simulation.pressure.values
    pressure_limit = float(np.max(np.abs(pressure)))
    pressure_limit = pressure_limit if pressure_limit > 0.0 else 1.0
    pressure_norm = TwoSlopeNorm(
        vmin=-pressure_limit, vcenter=0.0, vmax=pressure_limit
    )
    if float(np.ptp(pressure)) > 0.0:
        pressure_plot = pressure_axis.contourf(
            x,
            y,
            pressure,
            levels=np.linspace(-pressure_limit, pressure_limit, 33),
            cmap="coolwarm",
            norm=pressure_norm,
        )
    else:
        pressure_plot = pressure_axis.pcolormesh(
            x,
            y,
            pressure,
            shading="nearest",
            cmap="coolwarm",
            norm=pressure_norm,
        )
    figure.colorbar(pressure_plot, ax=pressure_axis, label="Pressure (Pa)")
    pressure_axis.set_title("Pressure")

    if float(np.max(speed)) > 0.0:
        streamline_axis.streamplot(
            x,
            y,
            cell_u,
            cell_v,
            color=speed,
            density=2.0,
            linewidth=0.8,
            arrowsize=0.8,
            cmap="viridis",
        )
    else:
        streamline_axis.text(0.5, 0.5, "Zero velocity", ha="center", va="center")
    streamline_axis.set_title("Streamlines")

    vorticity_limit = float(np.max(np.abs(vorticity)))
    vorticity_limit = vorticity_limit if vorticity_limit > 0.0 else 1.0
    vorticity_norm = TwoSlopeNorm(
        vmin=-vorticity_limit, vcenter=0.0, vmax=vorticity_limit
    )
    if float(np.ptp(vorticity)) > 0.0:
        vorticity_plot = vorticity_axis.contourf(
            x,
            y,
            vorticity,
            levels=np.linspace(-vorticity_limit, vorticity_limit, 33),
            cmap="coolwarm",
            norm=vorticity_norm,
        )
        if float(np.min(vorticity)) < 0.0 < float(np.max(vorticity)):
            vorticity_axis.contour(
                x, y, vorticity, levels=[0.0], colors="#202020", linewidths=0.6
            )
    else:
        vorticity_plot = vorticity_axis.pcolormesh(
            x,
            y,
            vorticity,
            shading="nearest",
            cmap="coolwarm",
            norm=vorticity_norm,
        )
    figure.colorbar(vorticity_plot, ax=vorticity_axis, label="Vorticity (1/s)")
    vorticity_axis.set_title("Vorticity")

    for axis in axes.flat:
        axis.set_xlabel("x (m)")
        axis.set_ylabel("y (m)")
        axis.set_aspect("equal")
    state = "converged" if simulation.converged else simulation.termination_reason
    if simulation.settings.transient:
        figure.suptitle(f"Cavity at t={simulation.final_time:.4g} s ({state})")
    else:
        figure.suptitle(f"Steady cavity after {simulation.steps} iterations ({state})")
    return _finish_figure(figure, output_path)


def plot_ghia_comparison(
    comparison: GhiaComparison, output_path: str | Path | None = None
) -> object:
    """Plot both dimensionless centerline profiles against Ghia reference points."""
    import matplotlib.pyplot as plt

    figure, axes = plt.subplots(1, 2, figsize=(10, 4), layout="constrained")
    axes[0].plot(comparison.u_computed, comparison.u_coordinate, label="FVM")
    axes[0].scatter(comparison.u_reference, comparison.u_coordinate, marker="x", label="Ghia Re=100")
    axes[0].set_xlabel("u / lid speed")
    axes[0].set_ylabel("y / height")
    axes[0].set_title(f"Vertical centerline, RMS={comparison.u_rms_error:.3e}")
    axes[0].legend()

    axes[1].plot(comparison.v_coordinate, comparison.v_computed, label="FVM")
    axes[1].scatter(comparison.v_coordinate, comparison.v_reference, marker="x", label="Ghia Re=100")
    axes[1].set_xlabel("x / width")
    axes[1].set_ylabel("v / lid speed")
    axes[1].set_title(f"Horizontal centerline, RMS={comparison.v_rms_error:.3e}")
    axes[1].legend()
    if not comparison.benchmark_valid:
        figure.suptitle("Diagnostic comparison only: simulation has not converged")
    return _finish_figure(figure, output_path)


def plot_convergence_history(
    simulation: SimulationResult, output_path: str | Path | None = None
) -> object:
    """Plot velocity change, continuity, and pressure residual versus time."""
    import matplotlib.pyplot as plt

    if not simulation.history:
        raise ValueError("simulation has no time-step history to plot")
    transient = simulation.settings.transient
    x_values = np.array(
        [item.time if transient else item.step for item in simulation.history],
        dtype=np.float64,
    )
    series = {
        "max velocity change": [item.velocity_change for item in simulation.history],
        "max post-projection divergence": [
            item.max_divergence_after for item in simulation.history
        ],
        "pressure residual": [item.pressure_residual for item in simulation.history],
    }
    figure, axis = plt.subplots(figsize=(7, 4), layout="constrained")
    floor = np.finfo(np.float64).tiny
    for label, values in series.items():
        axis.semilogy(x_values, np.maximum(values, floor), label=label)
    axis.set_xlabel("Time (s)" if transient else "Iteration")
    axis.set_ylabel("Residual / change")
    axis.set_title("Transient convergence history" if transient else "Steady convergence history")
    axis.legend()
    axis.grid(True, which="both", alpha=0.25)
    return _finish_figure(figure, output_path)


def run_lid_driven_grid_study(
    grid_sizes: Sequence[int] = (16, 32, 64, 128),
    *,
    max_time_step: float = 1e-3,
    max_steps: int = 1000,
    cfl_limit: float = 0.5,
    velocity_tolerance: float = 1e-6,
) -> tuple[GridStudyRow, ...]:
    """Run Re=100 cavity cases on requested square grids and compare profiles.

    The default grid series is the planned 16/32/64/128 study. Each row keeps
    the convergence flag: profile RMS errors from a run that reaches its step
    cap are diagnostics, not accepted benchmark results.
    """
    if not grid_sizes:
        raise ValueError("grid_sizes must contain at least one resolution")
    normalized_sizes: list[int] = []
    for size in grid_sizes:
        if isinstance(size, bool) or not isinstance(size, Integral):
            raise TypeError("grid sizes must be integers")
        if size < 16:
            raise ValueError("Ghia grid study resolutions must be at least 16 per side")
        normalized_sizes.append(int(size))
    if normalized_sizes != sorted(set(normalized_sizes)):
        raise ValueError("grid_sizes must be unique and strictly increasing")

    rows: list[GridStudyRow] = []
    for cells in normalized_sizes:
        mesh = CartesianMesh(nx=cells, ny=cells)
        velocity = VectorField(mesh)
        pressure = ScalarField(mesh, name="pressure")
        conditions = BoundaryConditions()
        for side in BOUNDARY_NAMES:
            if side == "north":
                conditions.set("velocity", side, MovingWall((1.0, 0.0)))
            else:
                conditions.set("velocity", side, NoSlipWall())
        solver = TransientSolver(
            density=1.0,
            viscosity=0.01,
            max_time_step=max_time_step,
            max_steps=max_steps,
            cfl_limit=cfl_limit,
            velocity_tolerance=velocity_tolerance,
        )
        simulation = solver.run(velocity, pressure, conditions)
        comparison = compare_ghia_re100(simulation)
        last_step = simulation.history[-1]
        rows.append(
            GridStudyRow(
                cells_per_side=cells,
                converged=simulation.converged,
                steps=simulation.steps,
                final_time=simulation.final_time,
                u_rms_error=comparison.u_rms_error,
                v_rms_error=comparison.v_rms_error,
                max_divergence=last_step.max_divergence_after,
                global_mass_imbalance=last_step.global_mass_imbalance,
            )
        )
    return tuple(rows)


def write_grid_study_csv(rows: Sequence[GridStudyRow], output_path: str | Path) -> Path:
    """Write grid-study metrics to a CSV file."""
    if not rows:
        raise ValueError("rows must contain at least one grid result")
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    field_names = [field.name for field in fields(GridStudyRow)]
    with output.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)
    return output


def export_ghia_comparison(
    comparison: GhiaComparison, output_path: str | Path
) -> Path:
    """Write profile samples, RMS errors, and convergence eligibility as JSON."""
    if not isinstance(comparison, GhiaComparison):
        raise TypeError("comparison must be a GhiaComparison")
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "benchmark": "Ghia et al. lid-driven cavity Re=100",
        "simulation_converged": comparison.simulation_converged,
        "benchmark_valid": comparison.benchmark_valid,
        "u_rms_error": comparison.u_rms_error,
        "v_rms_error": comparison.v_rms_error,
        "u_profile": [
            {
                "coordinate": float(coordinate),
                "reference": float(reference),
                "computed": float(computed),
            }
            for coordinate, reference, computed in zip(
                comparison.u_coordinate,
                comparison.u_reference,
                comparison.u_computed,
            )
        ],
        "v_profile": [
            {
                "coordinate": float(coordinate),
                "reference": float(reference),
                "computed": float(computed),
            }
            for coordinate, reference, computed in zip(
                comparison.v_coordinate,
                comparison.v_reference,
                comparison.v_computed,
            )
        ],
    }
    with output.open("w", encoding="utf-8") as output_file:
        json.dump(payload, output_file, indent=2)
    return output