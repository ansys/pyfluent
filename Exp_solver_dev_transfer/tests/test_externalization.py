from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace

import matplotlib
import numpy as np
import pytest

matplotlib.use("Agg")

from fvm.externalization import (
    AsyncFileExternalizer,
    GrpcExternalizer,
    GrpcSnapshotServer,
    SharedFolderExternalizer,
    SharedFolderPoller,
    SnapshotStore,
    StepSnapshot,
    create_step_observer,
    SynchronousFileExternalizer,
    plot_latest_snapshot,
)


def _snapshot(step: int, run_id: str = "externalization-test") -> StepSnapshot:
    return StepSnapshot(
        run_id=run_id,
        step=step,
        mesh={"nx": 2, "ny": 2, "width": 1.0, "height": 1.0},
        diagnostics={
            "step": step,
            "time": step * 0.1,
            "pseudo_time": None,
            "time_step": 0.1,
            "cfl_number": 0.1,
            "velocity_change": 0.01,
            "max_divergence_before": 0.1,
            "max_divergence_after": 0.0,
            "global_mass_imbalance": 0.0,
            "u_momentum_residual": 0.0,
            "v_momentum_residual": 0.0,
            "pressure_residual": 0.0,
            "inner_iterations": 1,
        },
        x_cell_centers=np.array([0.25, 0.75]),
        y_cell_centers=np.array([0.25, 0.75]),
        pressure=np.full((2, 2), step, dtype=float),
        u_faces=np.full((2, 3), step, dtype=float),
        v_faces=np.full((3, 2), -step, dtype=float),
    )


def test_snapshot_round_trip_is_validated_and_arrays_are_immutable() -> None:
    snapshot = _snapshot(1)

    decoded = StepSnapshot.from_bytes(snapshot.to_bytes())

    assert decoded.run_id == snapshot.run_id
    assert decoded.step == 1
    np.testing.assert_array_equal(decoded.pressure, snapshot.pressure)
    with pytest.raises(ValueError):
        decoded.pressure[0, 0] = 4.0
    with pytest.raises(ValueError):
        decoded.pressure.setflags(write=True)
    with pytest.raises(ValueError, match="pressure must have shape"):
        StepSnapshot(
            run_id="invalid",
            step=1,
            mesh={"nx": 2, "ny": 2, "width": 1.0, "height": 1.0},
            diagnostics={"step": 1},
            x_cell_centers=np.array([0.25, 0.75]),
            y_cell_centers=np.array([0.25, 0.75]),
            pressure=np.zeros((1, 2)),
            u_faces=np.zeros((2, 3)),
            v_faces=np.zeros((3, 2)),
        )


@dataclass(frozen=True)
class _Step:
    step: int


def _solver_fields():
    mesh = SimpleNamespace(
        nx=2,
        ny=2,
        width=1.0,
        height=1.0,
        x_cell_centers=np.array([0.25, 0.75]),
        y_cell_centers=np.array([0.25, 0.75]),
    )
    velocity = SimpleNamespace(
        mesh=mesh,
        u=SimpleNamespace(values=np.zeros((2, 3))),
        v=SimpleNamespace(values=np.zeros((3, 2))),
    )
    pressure = SimpleNamespace(values=np.zeros((2, 2)))
    return velocity, pressure


def test_step_observer_defaults_to_ten_steps_and_publishes_the_final_step() -> None:
    class Collector:
        def __init__(self) -> None:
            self.steps: list[int] = []

        def publish(self, snapshot: StepSnapshot) -> None:
            self.steps.append(snapshot.step)

    collector = Collector()
    observer = create_step_observer(collector, "sampled-run")
    velocity, pressure = _solver_fields()

    for step in range(1, 21):
        diagnostics = _Step(step)
        observer(diagnostics, velocity, pressure)
    assert observer.publish_final_step(_Step(20), velocity, pressure) is False

    assert collector.steps == [10, 20]


def test_step_observer_uses_configured_interval_and_final_step() -> None:
    class Collector:
        def __init__(self) -> None:
            self.steps: list[int] = []

        def publish(self, snapshot: StepSnapshot) -> None:
            self.steps.append(snapshot.step)

    collector = Collector()
    observer = create_step_observer(
        collector, "custom-interval-run", snapshot_every=3
    )
    velocity, pressure = _solver_fields()

    for step in range(1, 6):
        diagnostics = _Step(step)
        observer(diagnostics, velocity, pressure)
    observer.publish_final_step(_Step(5), velocity, pressure)

    assert collector.steps == [3, 5]


def test_synchronous_externalizer_writes_complete_readable_snapshots(
    tmp_path: Path,
) -> None:
    externalizer = SynchronousFileExternalizer(tmp_path / "sync")
    externalizer.publish(_snapshot(1))
    externalizer.close()
    store = SnapshotStore(tmp_path / "sync")

    assert store.latest_step == 1
    assert store.read(1).diagnostics["max_divergence_after"] == 0.0
    assert externalizer.metrics.snapshots == 1
    assert externalizer.metrics.bytes_written > 0


def test_shared_folder_poller_copies_only_committed_new_steps(
    tmp_path: Path,
) -> None:
    shared = SharedFolderExternalizer(tmp_path / "shared")
    poller = SharedFolderPoller(tmp_path / "shared", tmp_path / "externalized")
    shared.publish(_snapshot(1))
    shared.publish(_snapshot(1, "other-run"))
    shared.publish(_snapshot(2))

    assert poller.poll_once() == 3
    assert poller.poll_once() == 0
    assert SnapshotStore(tmp_path / "externalized").latest_step == 2
    assert poller.snapshots == 3


def test_async_externalizer_drains_bounded_queue_before_close(tmp_path: Path) -> None:
    externalizer = AsyncFileExternalizer(tmp_path / "async", queue_size=1)
    externalizer.publish(_snapshot(1))
    externalizer.publish(_snapshot(2))
    externalizer.close()

    assert SnapshotStore(tmp_path / "async").latest_step == 2
    assert externalizer.metrics.snapshots == 2
    assert externalizer.metrics.externalize_seconds >= 0.0


def test_async_externalizer_surfaces_background_write_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    externalizer = AsyncFileExternalizer(tmp_path / "failed", queue_size=1)

    def fail_write(snapshot: StepSnapshot) -> int:
        raise OSError(f"disk unavailable for step {snapshot.step}")

    monkeypatch.setattr(externalizer.store, "write", fail_write)
    externalizer.publish(_snapshot(1))

    with pytest.raises(RuntimeError, match="asynchronous externalization failed"):
        externalizer.close()


def test_grpc_externalizer_streams_snapshots_to_local_server(tmp_path: Path) -> None:
    server = GrpcSnapshotServer(tmp_path / "grpc")
    client = GrpcExternalizer(server.start(), queue_size=1)
    try:
        client.publish(_snapshot(1))
        client.publish(_snapshot(2))
        client.close()
    finally:
        server.stop()

    store = SnapshotStore(tmp_path / "grpc")
    assert store.latest_step == 2
    assert store.read(1).run_id == "externalization-test"
    assert client.metrics.snapshots == 2


def test_grpc_server_accepts_independent_runs_in_separate_streams(
    tmp_path: Path,
) -> None:
    server = GrpcSnapshotServer(tmp_path / "grpc-multi-run")
    target = server.start()
    try:
        for run_id in ("run-one", "run-two"):
            client = GrpcExternalizer(target)
            client.publish(_snapshot(1, run_id))
            client.close()
    finally:
        server.stop()

    store = SnapshotStore(tmp_path / "grpc-multi-run")
    assert store.list_run_ids() == ("run-one", "run-two")
    assert store.read(1, run_id="run-two").run_id == "run-two"


def test_snapshot_visualization_reads_externalized_data(tmp_path: Path) -> None:
    store = SnapshotStore(tmp_path / "visualization")
    store.write(_snapshot(1))

    figure = plot_latest_snapshot(store, tmp_path / "snapshot.png")

    assert len(figure.axes) >= 3
    assert (tmp_path / "snapshot.png").stat().st_size > 1000


def test_snapshot_store_writes_valid_metadata_without_pickle(tmp_path: Path) -> None:
    store = SnapshotStore(tmp_path / "metadata")
    store.write(_snapshot(1))

    with np.load(
        tmp_path / "metadata" / "externalization-test" / "step_00000001.npz",
        allow_pickle=False,
    ) as archive:
        metadata = json.loads(str(archive["metadata"].item()))

    assert metadata["format_version"] == 1
    assert metadata["run_id"] == "externalization-test"


def test_snapshot_store_isolates_runs_and_requires_run_id_for_ambiguous_reads(
    tmp_path: Path,
) -> None:
    store = SnapshotStore(tmp_path / "multi-run")
    store.write(_snapshot(1, "run-one"))
    store.write(_snapshot(1, "run-two"))

    assert store.list_run_ids() == ("run-one", "run-two")
    with pytest.raises(ValueError, match="run_id is required"):
        store.read(1)
    assert store.read(1, run_id="run-two").run_id == "run-two"
    assert store.latest_snapshot.run_id in {"run-one", "run-two"}


def test_snapshot_store_supports_sparse_steps_and_rejects_out_of_order_writes(
    tmp_path: Path,
) -> None:
    store = SnapshotStore(tmp_path / "resumed")
    store.write(_snapshot(20, "restarted-run"))
    store.write(_snapshot(22, "restarted-run"))

    assert [item.step for item in store.iter_after_by_run({})] == [20, 22]
    with pytest.raises(ValueError, match="in increasing order"):
        store.write(_snapshot(21, "restarted-run"))
    assert store.latest_step_for("restarted-run") == 22


def test_snapshot_rejects_path_like_run_ids() -> None:
    with pytest.raises(ValueError, match="run_id"):
        _snapshot(1, "../outside")
