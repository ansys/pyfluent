"""Visualization based only on the externalization snapshot contract."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np

from .model import StepSnapshot
from .store import SnapshotStore

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure
    from matplotlib.image import AxesImage
    from matplotlib.lines import Line2D
    from matplotlib.quiver import Quiver


class LiveSnapshotPlotter:
    """Update one interactive figure as externalized snapshots arrive."""

    def __init__(self) -> None:
        import matplotlib.pyplot as plt

        self.pyplot = plt
        self.pyplot.ion()
        self.figure, axes = plt.subplots(
            1, 4, figsize=(17, 4), layout="constrained"
        )
        self.figure: Figure
        self.speed_axis: Axes
        self.pressure_axis: Axes
        self.velocity_axis: Axes
        self.history_axis: Axes
        (
            self.speed_axis,
            self.pressure_axis,
            self.velocity_axis,
            self.history_axis,
        ) = axes
        self.speed_image: AxesImage | None = None
        self.pressure_image: AxesImage | None = None
        self.velocity_quiver: Quiver | None = None
        self.velocity_line: Line2D
        self.divergence_line: Line2D
        self.steps: list[int] = []
        self.velocity_changes: list[float] = []
        self.divergences: list[float] = []
        self._mesh: tuple[int, int, float, float] | None = None
        self._history_floor = np.finfo(np.float64).tiny

        self.speed_axis.set_title("Velocity magnitude")
        self.pressure_axis.set_title("Pressure")
        self.velocity_axis.set_title("Cell-centered velocity")
        self.history_axis.set_xlabel("Step")
        self.history_axis.set_ylabel("Change / residual")
        self.history_axis.set_title("Convergence history")
        self.velocity_line, = self.history_axis.semilogy(
            [], [], label="velocity change"
        )
        self.divergence_line, = self.history_axis.semilogy(
            [], [], label="max divergence"
        )
        self.history_axis.legend()
        self.pyplot.show(block=False)

    def update(self, snapshot: StepSnapshot) -> None:
        """Append one persisted step to the existing live figure."""
        mesh = snapshot.mesh
        mesh_key = (
            int(mesh["nx"]),
            int(mesh["ny"]),
            float(mesh["width"]),
            float(mesh["height"]),
        )
        if self._mesh is not None and mesh_key != self._mesh:
            raise ValueError("mesh dimensions changed during one live run")

        u_cell = 0.5 * (snapshot.u_faces[:, :-1] + snapshot.u_faces[:, 1:])
        v_cell = 0.5 * (snapshot.v_faces[:-1, :] + snapshot.v_faces[1:, :])
        speed = np.hypot(u_cell, v_cell)
        if self.speed_image is None:
            extent = (0.0, mesh_key[2], 0.0, mesh_key[3])
            self.speed_image = self.speed_axis.imshow(
                speed,
                origin="lower",
                extent=extent,
                interpolation="nearest",
                cmap="viridis",
                vmin=0.0,
                vmax=max(float(np.max(speed)), 1e-12),
            )
            self.figure.colorbar(
                self.speed_image, ax=self.speed_axis, label="Speed (m/s)"
            )
            self.pressure_image = self.pressure_axis.imshow(
                snapshot.pressure,
                origin="lower",
                extent=extent,
                interpolation="nearest",
                cmap="coolwarm",
            )
            self.figure.colorbar(
                self.pressure_image, ax=self.pressure_axis, label="Pressure (Pa)"
            )
            grid_x, grid_y = np.meshgrid(
                snapshot.x_cell_centers, snapshot.y_cell_centers
            )
            self.velocity_quiver = self.velocity_axis.quiver(
                grid_x, grid_y, u_cell, v_cell, speed, cmap="viridis"
            )
            for axis in (
                self.speed_axis,
                self.pressure_axis,
                self.velocity_axis,
            ):
                axis.set_xlim(0.0, mesh_key[2])
                axis.set_ylim(0.0, mesh_key[3])
                axis.set_xlabel("x (m)")
                axis.set_ylabel("y (m)")
                axis.set_aspect("equal")
            self._mesh = mesh_key
        else:
            self.speed_image.set_data(speed)
            self.speed_image.set_clim(
                vmin=0.0, vmax=max(float(np.max(speed)), 1e-12)
            )
            self.pressure_image.set_data(snapshot.pressure)
            self.velocity_quiver.set_UVC(u_cell, v_cell, speed)

        velocity_change = snapshot.diagnostics.get("velocity_change")
        max_divergence = snapshot.diagnostics.get("max_divergence_after")
        if velocity_change is None or max_divergence is None:
            raise ValueError(
                "live convergence plot requires velocity_change and "
                "max_divergence_after diagnostics"
            )
        self.steps.append(snapshot.step)
        self.velocity_changes.append(float(velocity_change))
        self.divergences.append(float(max_divergence))
        self.velocity_line.set_data(
            self.steps,
            np.maximum(self.velocity_changes, self._history_floor),
        )
        self.divergence_line.set_data(
            self.steps,
            np.maximum(self.divergences, self._history_floor),
        )
        self.history_axis.set_xlim(1, max(snapshot.step, 2))
        self.history_axis.relim()
        self.history_axis.autoscale_view(scalex=False)

        time_value = snapshot.diagnostics.get("time")
        state = (
            f"t={time_value:.5g} s"
            if time_value is not None
            else f"iteration {snapshot.step}"
        )
        self.figure.suptitle(
            f"Run {snapshot.run_id}, step {snapshot.step} ({state})"
        )
        self.figure.canvas.draw_idle()
        self.pyplot.pause(0.001)

    def finish(self) -> None:
        """Keep the final live view open until the user closes it."""
        self.pyplot.ioff()
        self.pyplot.show(block=True)

    def wait_for_events(self, interval_seconds: float) -> None:
        """Keep the plot responsive while waiting for another snapshot."""
        self.pyplot.pause(interval_seconds)

    def close(self) -> None:
        """Close the interactive figure."""
        self.pyplot.close(self.figure)


def plot_snapshot(
    snapshot: StepSnapshot, output_path: str | Path | None = None
) -> object:
    """Render a persisted solver step without importing solver result classes."""
    import matplotlib.pyplot as plt

    mesh = snapshot.mesh
    u_cell = 0.5 * (snapshot.u_faces[:, :-1] + snapshot.u_faces[:, 1:])
    v_cell = 0.5 * (snapshot.v_faces[:-1, :] + snapshot.v_faces[1:, :])
    speed = np.hypot(u_cell, v_cell)
    x, y = snapshot.x_cell_centers, snapshot.y_cell_centers
    figure, axes = plt.subplots(1, 3, figsize=(13, 4), layout="constrained")

    speed_image = axes[0].pcolormesh(x, y, speed, shading="nearest", cmap="viridis")
    figure.colorbar(speed_image, ax=axes[0], label="Speed (m/s)")
    axes[0].set_title("Velocity magnitude")

    pressure_image = axes[1].pcolormesh(
        x, y, snapshot.pressure, shading="nearest", cmap="coolwarm"
    )
    figure.colorbar(pressure_image, ax=axes[1], label="Pressure (Pa)")
    axes[1].set_title("Pressure")

    axes[2].quiver(x, y, u_cell, v_cell, speed, cmap="viridis")
    axes[2].set_title("Cell-centered velocity")
    for axis in axes:
        axis.set_xlabel("x (m)")
        axis.set_ylabel("y (m)")
        axis.set_xlim(0.0, float(mesh["width"]))
        axis.set_ylim(0.0, float(mesh["height"]))
        axis.set_aspect("equal")
    time_value = snapshot.diagnostics.get("time")
    state = (
        f"t={time_value:.5g} s"
        if time_value is not None
        else f"iteration {snapshot.step}"
    )
    figure.suptitle(f"Run {snapshot.run_id}, step {snapshot.step} ({state})")
    if output_path is not None:
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(output, dpi=160, bbox_inches="tight")
    return figure


def plot_latest_snapshot(
    store: SnapshotStore, output_path: str | Path | None = None
) -> object:
    """Load the newest committed step from a store and render it."""
    return plot_snapshot(store.latest_snapshot, output_path)
