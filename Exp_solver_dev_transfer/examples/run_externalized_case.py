"""Run one case with a selected externalization strategy and plot its snapshots.

Run from the repository root:
    python examples/run_externalized_case.py --case path/to/case.json
    python examples/run_externalized_case.py --case path/to/case.json --strategy grpc
    python examples/run_externalized_case.py --case path/to/case.json --mode live
"""

from __future__ import annotations

import argparse
from pathlib import Path
import threading
from uuid import uuid4

from fvm import BackendRun, PythonFVMBackend, load_case_file
from fvm.externalization import (
    AsyncFileExternalizer,
    GrpcExternalizer,
    GrpcSnapshotServer,
    LiveSnapshotPlotter,
    SharedFolderExternalizer,
    SharedFolderPoller,
    SnapshotStore,
    SynchronousFileExternalizer,
    create_step_observer,
    plot_snapshot,
)


ROOT = Path(__file__).resolve().parents[1]
STRATEGIES = ("sync", "shared", "async", "grpc")


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run a case, externalize selected steps, and plot the "
            "persisted snapshots."
        )
    )
    parser.add_argument(
        "--case",
        type=Path,
        default=ROOT / "cases" / "lid_driven_cavity_re100_steady.json",
        help="Case JSON to run (default: steady Re=100 cavity).",
    )
    parser.add_argument(
        "--strategy",
        choices=STRATEGIES,
        default="sync",
        help="Snapshot delivery strategy (default: sync).",
    )
    parser.add_argument(
        "--mode",
        choices=("save", "live"),
        default="save",
        help=(
            "save: write per-step PNGs after the run (default); live: display "
            "snapshots as they appear in the externalized store"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "results" / "externalized_case",
        help="Directory for snapshots and plots.",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        help="Optional step cap for a shorter demo; case settings are used otherwise.",
    )
    parser.add_argument(
        "--snapshot-every",
        type=int,
        default=10,
        help="Externalize every N completed steps and always the final step (default: 10).",
    )
    parser.add_argument(
        "--queue-size",
        type=int,
        default=8,
        help="Bounded queue size for async and gRPC (default: 8).",
    )
    parser.add_argument(
        "--poll-interval",
        type=float,
        default=0.1,
        help="Shared-folder poll interval in seconds (default: 0.1).",
    )
    return parser


def _run(
    case_document: dict[str, object],
    output_path: Path,
    strategy: str,
    queue_size: int,
    poll_interval: float,
    snapshot_every: int,
    run_id: str,
) -> tuple[BackendRun, Path, str]:
    strategy_output = output_path / strategy / run_id
    snapshot_directory = strategy_output / "snapshots"

    poller: SharedFolderPoller | None = None
    poller_thread: threading.Thread | None = None
    poller_stop: threading.Event | None = None
    poller_errors: list[Exception] = []
    grpc_server: GrpcSnapshotServer | None = None

    if strategy == "sync":
        externalizer = SynchronousFileExternalizer(snapshot_directory)
    elif strategy == "shared":
        shared_directory = strategy_output / "shared"
        poller = SharedFolderPoller(shared_directory, snapshot_directory)
        poller_stop = threading.Event()

        def poll_until_stopped() -> None:
            try:
                poller.run(poll_interval, poller_stop)
            except Exception as error:
                poller_errors.append(error)

        externalizer = SharedFolderExternalizer(shared_directory)
        poller_thread = threading.Thread(
            target=poll_until_stopped,
            name="externalized-case-poller",
            daemon=True,
        )
        poller_thread.start()
    elif strategy == "async":
        externalizer = AsyncFileExternalizer(snapshot_directory, queue_size=queue_size)
    else:
        grpc_server = GrpcSnapshotServer(snapshot_directory)
        externalizer = GrpcExternalizer(
            grpc_server.start(), queue_size=queue_size
        )

    try:
        observer = create_step_observer(
            externalizer, run_id, snapshot_every=snapshot_every
        )
        backend_run = PythonFVMBackend().run(
            case_document,
            step_observer=observer,
        )
        if backend_run.simulation.history:
            observer.publish_final_step(
                backend_run.simulation.history[-1],
                backend_run.simulation.velocity,
                backend_run.simulation.pressure,
            )
    finally:
        try:
            externalizer.close()
        finally:
            try:
                if poller_stop is not None and poller_thread is not None:
                    poller_stop.set()
                    poller_thread.join()
            finally:
                if grpc_server is not None:
                    grpc_server.stop()

    if poller_errors:
        raise RuntimeError("shared-folder polling failed") from poller_errors[0]
    return backend_run, snapshot_directory, run_id


def _run_live(
    case_document: dict[str, object],
    output_path: Path,
    strategy: str,
    queue_size: int,
    poll_interval: float,
    snapshot_every: int,
    run_id: str,
) -> tuple[BackendRun, Path, str]:
    """Run off the GUI thread and display only committed externalized snapshots."""
    import matplotlib

    if matplotlib.get_backend().lower() in {"agg", "pdf", "svg", "ps", "template"}:
        raise RuntimeError(
            "live mode needs an interactive Matplotlib backend; use "
            "--mode save to write static PNGs without windows"
        )

    snapshot_directory = output_path / strategy / run_id / "snapshots"
    store = SnapshotStore(snapshot_directory, run_id=run_id)
    worker_result: list[tuple[BackendRun, Path, str]] = []
    worker_errors: list[Exception] = []

    def run_solver() -> None:
        try:
            worker_result.append(
                _run(
                    case_document,
                    output_path,
                    strategy,
                    queue_size,
                    poll_interval,
                    snapshot_every,
                    run_id,
                )
            )
        except Exception as error:
            worker_errors.append(error)

    worker = threading.Thread(
        target=run_solver,
        name="externalized-case-solver",
        daemon=False,
    )
    plotter = LiveSnapshotPlotter()
    last_step = 0
    worker.start()
    try:
        while worker.is_alive() or store.latest_step_for(run_id) > last_step:
            found_snapshot = False
            for snapshot in store.iter_after(last_step, run_id):
                found_snapshot = True
                plotter.update(snapshot)
                last_step = snapshot.step
            if not found_snapshot:
                plotter.wait_for_events(0.05)
        worker.join()
        if worker_errors:
            raise RuntimeError(
                f"solver or externalization failed in live mode: {worker_errors[0]}"
            ) from worker_errors[0]
        if not worker_result:
            raise RuntimeError("live solver worker completed without a result")
        plotter.finish()
    finally:
        if worker.is_alive():
            worker.join()
        plotter.close()

    return worker_result[0]


def _save_snapshot_plots(
    store: SnapshotStore,
    simulation_steps: int,
    snapshot_every: int,
    plots_directory: Path,
    final_plot: Path,
) -> int:
    import matplotlib.pyplot as plt

    plots_directory.mkdir(parents=True, exist_ok=True)
    snapshot_count = 0
    final_snapshot = None
    for snapshot in store.iter_after():
        plot_snapshot(
            snapshot,
            plots_directory / f"step_{snapshot.step:08d}.png",
        )
        plt.close()
        final_snapshot = snapshot
        snapshot_count += 1

    expected_snapshot_count = simulation_steps // snapshot_every
    if simulation_steps % snapshot_every:
        expected_snapshot_count += 1
    if snapshot_count != expected_snapshot_count:
        raise RuntimeError(
            f"externalized {snapshot_count} snapshots for "
            f"{simulation_steps} completed steps at interval {snapshot_every}"
        )
    if final_snapshot is None:
        raise RuntimeError("the solver completed without externalizing any snapshots")

    plot_snapshot(final_snapshot, final_plot)
    plt.close()
    return snapshot_count


def main() -> int:
    arguments = build_argument_parser().parse_args()
    if arguments.max_steps is not None and arguments.max_steps <= 0:
        raise SystemExit("--max-steps must be positive")
    if arguments.queue_size <= 0:
        raise SystemExit("--queue-size must be positive")
    if arguments.poll_interval <= 0.0:
        raise SystemExit("--poll-interval must be positive")
    if arguments.snapshot_every <= 0:
        raise SystemExit("--snapshot-every must be positive")

    case_path = (
        arguments.case
        if arguments.case.is_absolute()
        else Path.cwd() / arguments.case
    )
    output_path = (
        arguments.output
        if arguments.output.is_absolute()
        else Path.cwd() / arguments.output
    )
    case_document = load_case_file(case_path).to_mapping()
    if arguments.max_steps is not None:
        solver_config = case_document["solver"]
        solver_config["max_steps"] = min(
            solver_config["max_steps"], arguments.max_steps
        )

    # Pass the validated mapping so an optional demo step cap does not require
    # modifying the user's case file on disk.
    run_id = f"run-{uuid4().hex}"
    runner = _run_live if arguments.mode == "live" else _run
    backend_run, snapshot_directory, run_id = runner(
        case_document,
        output_path,
        arguments.strategy,
        arguments.queue_size,
        arguments.poll_interval,
        arguments.snapshot_every,
        run_id,
    )
    store = SnapshotStore(snapshot_directory, run_id=run_id)
    strategy_output = output_path / arguments.strategy / run_id
    plots_directory = strategy_output / "step_plots"
    final_plot = output_path / arguments.strategy / run_id / "final_result.png"
    snapshot_count = _save_snapshot_plots(
        store,
        backend_run.simulation.steps,
        arguments.snapshot_every,
        plots_directory,
        final_plot,
    )

    print(f"Case: {backend_run.case_id}")
    print(f"Strategy: {arguments.strategy}")
    print(f"Mode: {arguments.mode}")
    print(f"Snapshots plotted: {snapshot_count}")
    print(f"Snapshot interval: every {arguments.snapshot_every} steps plus final")
    print(f"Snapshot store: {snapshot_directory}")
    print(f"Per-step plots: {plots_directory}")
    print(f"Final result plot: {final_plot}")
    print(f"Converged: {backend_run.simulation.converged}")
    return 0 if backend_run.simulation.converged else 2


if __name__ == "__main__":
    raise SystemExit(main())
