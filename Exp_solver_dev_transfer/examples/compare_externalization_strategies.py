"""Compare local solver-step externalization strategies on the same case.

Run from the repository root:
    python examples/compare_externalization_strategies.py --steps 4
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import threading
from time import perf_counter
from uuid import uuid4

from fvm import PythonFVMBackend, load_case_file
from fvm.externalization import (
    AsyncFileExternalizer,
    GrpcExternalizer,
    GrpcSnapshotServer,
    SharedFolderExternalizer,
    SharedFolderPoller,
    SnapshotStore,
    SynchronousFileExternalizer,
    create_step_observer,
    plot_latest_snapshot,
)


ROOT = Path(__file__).resolve().parents[1]
STRATEGIES = ("sync", "shared", "async", "grpc")


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Measure solver and local externalization timings."
    )
    parser.add_argument(
        "--case",
        type=Path,
        default=ROOT / "cases" / "lid_driven_cavity_re100_steady.json",
        help="Case JSON to run for every strategy.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "results" / "externalization_poc",
        help="Directory for strategy output, plots, and benchmark.csv.",
    )
    parser.add_argument(
        "--strategy",
        choices=(*STRATEGIES, "all"),
        default="all",
        help="Run one strategy or all four (default: all).",
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=4,
        help="Maximum solver steps per strategy (default: 4).",
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
        help="Bounded in-memory queue size for async and gRPC strategies.",
    )
    parser.add_argument(
        "--poll-interval",
        type=float,
        default=0.1,
        help="Independent shared-folder poll interval in seconds.",
    )
    return parser


def _run_strategy(
    strategy: str,
    case_document: dict[str, object],
    output: Path,
    queue_size: int,
    poll_interval: float,
    snapshot_every: int,
) -> dict[str, object]:
    run_id = f"{case_document['case_id']}-{uuid4().hex[:8]}"
    strategy_output = output / strategy / run_id
    store_directory = strategy_output / "snapshots"
    poller: SharedFolderPoller | None = None
    poller_thread: threading.Thread | None = None
    poller_stop: threading.Event | None = None
    poller_errors: list[Exception] = []
    grpc_server: GrpcSnapshotServer | None = None

    if strategy == "sync":
        externalizer = SynchronousFileExternalizer(store_directory)
    elif strategy == "shared":
        shared_directory = strategy_output / "shared"
        poller = SharedFolderPoller(shared_directory, store_directory)
        poller_stop = threading.Event()

        def poll_until_stopped() -> None:
            try:
                poller.run(poll_interval, poller_stop)
            except Exception as error:
                poller_errors.append(error)

        poller_thread = threading.Thread(
            target=poll_until_stopped,
            name=f"snapshot-poller-{strategy}",
            daemon=True,
        )
        poller_thread.start()
        externalizer = SharedFolderExternalizer(shared_directory)
    elif strategy == "async":
        externalizer = AsyncFileExternalizer(store_directory, queue_size=queue_size)
    else:
        grpc_server = GrpcSnapshotServer(store_directory)
        externalizer = GrpcExternalizer(
            grpc_server.start(), queue_size=queue_size
        )

    started = perf_counter()
    try:
        observer = create_step_observer(
            externalizer, run_id, snapshot_every=snapshot_every
        )
        run = PythonFVMBackend().run(
            case_document,
            step_observer=observer,
        )
        if run.simulation.history:
            observer.publish_final_step(
                run.simulation.history[-1],
                run.simulation.velocity,
                run.simulation.pressure,
            )
        solver_seconds = perf_counter() - started
    finally:
        try:
            externalizer.close()
        finally:
            if poller_stop is not None and poller_thread is not None:
                poller_stop.set()
                poller_thread.join()
                if poller_errors:
                    raise RuntimeError("shared-folder polling failed") from poller_errors[0]
            if grpc_server is not None:
                grpc_server.stop()
    total_seconds = perf_counter() - started

    if poller is not None:
        snapshot_count = poller.snapshots
        externalize_seconds = poller.externalize_seconds
        bytes_written = poller.bytes_written
    else:
        snapshot_count = externalizer.metrics.snapshots
        externalize_seconds = externalizer.metrics.externalize_seconds
        bytes_written = externalizer.metrics.bytes_written
    expected_snapshot_count = run.simulation.steps // snapshot_every
    if run.simulation.steps % snapshot_every:
        expected_snapshot_count += 1
    if snapshot_count != expected_snapshot_count:
        raise RuntimeError(
            f"{strategy} externalized {snapshot_count} snapshots for "
            f"{run.simulation.steps} completed steps at interval {snapshot_every}"
        )

    plot_latest_snapshot(
        SnapshotStore(store_directory), strategy_output / "final_snapshot.png"
    )
    return {
        "strategy": strategy,
        "steps": run.simulation.steps,
        "snapshot_every": snapshot_every,
        "converged": run.simulation.converged,
        "solver_seconds": solver_seconds,
        "total_seconds": total_seconds,
        "publish_seconds": externalizer.metrics.publish_seconds,
        "externalize_seconds": externalize_seconds,
        "bytes_written": bytes_written,
        "snapshot_count": snapshot_count,
        "seconds_per_step": (
            total_seconds / run.simulation.steps if run.simulation.steps else 0.0
        ),
    }


def main() -> int:
    arguments = build_argument_parser().parse_args()
    if arguments.steps <= 0:
        raise SystemExit("--steps must be positive")
    if arguments.queue_size <= 0:
        raise SystemExit("--queue-size must be positive")
    if arguments.poll_interval <= 0.0:
        raise SystemExit("--poll-interval must be positive")
    if arguments.snapshot_every <= 0:
        raise SystemExit("--snapshot-every must be positive")

    case_document = load_case_file(arguments.case).to_mapping()
    solver_config = case_document["solver"]
    solver_config["max_steps"] = min(solver_config["max_steps"], arguments.steps)
    strategies = STRATEGIES if arguments.strategy == "all" else (arguments.strategy,)
    arguments.output.mkdir(parents=True, exist_ok=True)
    rows = [
        _run_strategy(
            strategy,
            case_document,
            arguments.output,
            arguments.queue_size,
            arguments.poll_interval,
            arguments.snapshot_every,
        )
        for strategy in strategies
    ]

    report_path = arguments.output / "benchmark.csv"
    with report_path.open("w", newline="", encoding="utf-8") as report_file:
        writer = csv.DictWriter(report_file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (arguments.output / "benchmark.json").write_text(
        json.dumps(rows, indent=2), encoding="utf-8"
    )
    print("strategy     steps  snapshots  solver(s)  total(s)  externalize(s)  bytes")
    for row in rows:
        print(
            f"{row['strategy']:<12} {row['steps']:>5}  "
            f"{row['snapshot_count']:>9}  "
            f"{row['solver_seconds']:>9.4f}  {row['total_seconds']:>8.4f}  "
            f"{row['externalize_seconds']:>14.4f}  {row['bytes_written']}"
        )
    print(f"Benchmark report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
