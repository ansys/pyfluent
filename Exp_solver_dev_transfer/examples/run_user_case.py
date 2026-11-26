"""Run a versioned FVM case, export results, and create validation plots.

Run from the repository root:
    python examples/run_user_case.py
    python examples/run_user_case.py --case path/to/setup-export.json --output results/my_case
    python examples/run_user_case.py --mode live
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from fvm import (
    CheckpointManager,
    PythonFVMBackend,
    compare_ghia_re100,
    export_ghia_comparison,
    load_case_file,
    plot_cavity_fields,
    plot_convergence_history,
    plot_ghia_comparison,
    plot_mesh_and_boundaries,
)


ROOT = Path(__file__).resolve().parents[1]


def _history_plot_values(history):
    """Return the complete step and convergence series for live plotting."""
    return (
        [item.step for item in history],
        [item.velocity_change for item in history],
        [item.max_divergence_after for item in history],
    )


class LiveStepPlotter:
    """Update domain fields and convergence metrics after every solver step."""

    def __init__(self, mesh, velocity, pressure, history=()) -> None:
        import matplotlib

        backend_name = matplotlib.get_backend().lower()
        if backend_name in {"agg", "pdf", "svg", "ps", "template"}:
            raise RuntimeError(
                "live mode needs an interactive Matplotlib backend; use "
                "--mode save to write static PNGs without windows"
            )

        import matplotlib.pyplot as plt

        self.pyplot = plt
        self.mesh = mesh
        plt.ion()
        self.figure, axes = plt.subplots(1, 3, figsize=(14, 4), layout="constrained")
        extent = (0.0, mesh.width, 0.0, mesh.height)
        self.speed_image = axes[0].imshow(
            np.zeros((mesh.ny, mesh.nx)),
            origin="lower",
            extent=extent,
            interpolation="nearest",
            cmap="viridis",
            vmin=0.0,
            vmax=1.0,
        )
        self.figure.colorbar(self.speed_image, ax=axes[0], label="Speed (m/s)")
        self.pressure_image = axes[1].imshow(
            np.zeros((mesh.ny, mesh.nx)),
            origin="lower",
            extent=extent,
            interpolation="nearest",
            cmap="coolwarm",
        )
        self.figure.colorbar(self.pressure_image, ax=axes[1], label="Pressure (Pa)")
        self.speed_axis, self.pressure_axis, self.history_axis = axes
        self.speed_axis.set_title("Velocity magnitude")
        self.pressure_axis.set_title("Pressure")
        for axis in (self.speed_axis, self.pressure_axis):
            axis.set_xlabel("x (m)")
            axis.set_ylabel("y (m)")
            axis.set_aspect("equal")

        self.velocity_line, = self.history_axis.semilogy([], [], label="velocity change")
        self.divergence_line, = self.history_axis.semilogy([], [], label="max divergence")
        self.history_axis.set_xlabel("Step")
        self.history_axis.set_ylabel("Change / residual")
        self.history_axis.set_title("Live convergence")
        self.history_axis.legend()
        (
            self.steps,
            self.velocity_changes,
            self.divergences,
        ) = _history_plot_values(history)
        self.history_floor = np.finfo(np.float64).tiny
        self._set_history()
        state_label = (
            self._state_label(history[-1]) if history else "initial state"
        )
        self._set_fields(velocity, pressure, state_label)

    def __call__(self, diagnostics, velocity, pressure) -> None:
        """Refresh the live plots with an immutable per-step field snapshot."""
        self._set_fields(velocity, pressure, self._state_label(diagnostics))
        self.steps.append(diagnostics.step)
        self.velocity_changes.append(diagnostics.velocity_change)
        self.divergences.append(diagnostics.max_divergence_after)
        self._set_history()
        self.figure.canvas.draw_idle()
        self.pyplot.pause(0.001)

    @staticmethod
    def _state_label(diagnostics) -> str:
        return (
            f"t={diagnostics.time:.4g} s"
            if diagnostics.time is not None
            else f"iteration {diagnostics.step}"
        )

    def _set_fields(self, velocity, pressure, state_label: str) -> None:
        u = velocity.u.values
        v = velocity.v.values
        u_cell = 0.5 * (u[:, :-1] + u[:, 1:])
        v_cell = 0.5 * (v[:-1, :] + v[1:, :])
        speed = np.hypot(u_cell, v_cell)
        self.speed_image.set_data(speed)
        self.speed_image.set_clim(vmin=0.0, vmax=max(float(np.max(speed)), 1e-12))
        self.pressure_image.set_data(pressure.values)
        self.speed_axis.set_title(f"Speed, {state_label}")

    def _set_history(self) -> None:
        self.velocity_line.set_data(
            self.steps, np.maximum(self.velocity_changes, self.history_floor)
        )
        self.divergence_line.set_data(
            self.steps, np.maximum(self.divergences, self.history_floor)
        )
        if self.steps:
            self.history_axis.set_xlim(1, max(self.steps[-1], 2))
            self.history_axis.relim()
            self.history_axis.autoscale_view(scalex=False)

    def finish(self) -> None:
        """Leave the final live view open until the user closes it."""
        self.pyplot.ioff()
        self.pyplot.show(block=True)


def build_argument_parser() -> argparse.ArgumentParser:
    """Define inputs used by solver users and setup-software integrations."""
    parser = argparse.ArgumentParser(
        description="Run a schema-v1 case through the independent FVM backend."
    )
    parser.add_argument(
        "--case",
        type=Path,
        default=ROOT / "cases" / "lid_driven_cavity_re100_steady.json",
        help="JSON problem definition (default: steady Re=100 cavity).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "results" / "user_guide_lid_driven_cavity",
        help="Directory for fields, reports, history, and plots.",
    )
    parser.add_argument(
        "--mode",
        choices=("save", "live"),
        default="save",
        help=(
            "save: write PNGs only (default); live: show geometry, update plots "
            "each step, and also save all outputs"
        ),
    )
    parser.add_argument(
        "--checkpoint-every",
        type=int,
        help="Save restart checkpoints every N completed steps; also save the final safe state.",
    )
    parser.add_argument(
        "--retain-checkpoints",
        type=int,
        default=5,
        help="Number of recent checkpoint files to retain (default: 5).",
    )
    parser.add_argument(
        "--restart",
        help="Resume from latest or a checkpoint filename in OUTPUT/checkpoints.",
    )
    parser.add_argument(
        "--live",
        dest="mode",
        action="store_const",
        const="live",
        default=argparse.SUPPRESS,
        help=argparse.SUPPRESS,
    )
    return parser


def main() -> int:
    """Execute a case and return a nonzero exit code if it did not converge."""
    arguments = build_argument_parser().parse_args()
    case_path = arguments.case if arguments.case.is_absolute() else Path.cwd() / arguments.case
    output_path = (
        arguments.output
        if arguments.output.is_absolute()
        else Path.cwd() / arguments.output
    )

    backend = PythonFVMBackend()
    case_definition = load_case_file(case_path)
    prepared_case = backend.prepare(case_definition)
    restart_state = (
        CheckpointManager(output_path / "checkpoints", arguments.retain_checkpoints).load(
            arguments.restart,
            case_definition.to_mapping(),
            prepared_case.mesh,
        )
        if arguments.restart is not None
        else None
    )
    plot_mesh_and_boundaries(
        prepared_case.mesh,
        prepared_case.boundary_conditions,
        output_path / "geometry.png",
    )
    if arguments.mode == "live":
        import matplotlib.pyplot as plt

        # Show the setup first; the live field/convergence window follows.
        plt.show(block=False)
        plt.pause(0.1)
    live_plotter = (
        LiveStepPlotter(
            prepared_case.mesh,
            restart_state.velocity if restart_state else prepared_case.initial_velocity,
            restart_state.pressure if restart_state else prepared_case.initial_pressure,
            restart_state.history if restart_state else (),
        )
        if arguments.mode == "live"
        else None
    )
    backend_run = backend.run(
        case_definition,
        output_directory=output_path,
        step_observer=live_plotter,
        checkpoint_every=arguments.checkpoint_every,
        restart=arguments.restart,
        retain_checkpoints=arguments.retain_checkpoints,
    )
    simulation = backend_run.simulation
    comparison = compare_ghia_re100(simulation)

    # Backend exports fields, run settings, and history. Add validation-specific
    # output and the corresponding visual summaries beside those artifacts.
    export_ghia_comparison(comparison, output_path / "ghia_re100.json")
    plot_cavity_fields(simulation, output_path / "cavity_fields.png")
    plot_ghia_comparison(comparison, output_path / "ghia_profiles.png")
    plot_convergence_history(simulation, output_path / "convergence_history.png")

    print(f"Case: {backend_run.case_id}")
    print(f"Status: {backend_run.summary['status']}")
    if simulation.settings.transient:
        print(
            f"Time steps: {simulation.steps}; physical time: "
            f"{simulation.final_time:.6g} s"
        )
    else:
        print(f"Iterations: {simulation.steps}; pseudo-time is not physical time")
    print(f"Reynolds number: {backend_run.summary['reynolds_number']:.6g}")
    print(f"Ghia profile RMS: u={comparison.u_rms_error:.6g}, v={comparison.v_rms_error:.6g}")
    print(f"Benchmark eligible: {comparison.benchmark_valid}")
    print(f"Results: {output_path}")
    if arguments.checkpoint_every is not None:
        print(f"Checkpoints: {output_path / 'checkpoints'}")
    if live_plotter is not None:
        live_plotter.finish()
    return 0 if simulation.converged else 2


if __name__ == "__main__":
    raise SystemExit(main())