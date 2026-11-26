from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pytest

from examples import run_externalized_case
from fvm.externalization import LiveSnapshotPlotter, SnapshotStore, StepSnapshot


def _snapshot(run_id: str, step: int) -> StepSnapshot:
    return StepSnapshot(
        run_id=run_id,
        step=step,
        mesh={"nx": 2, "ny": 2, "width": 1.0, "height": 1.0},
        diagnostics={
            "step": step,
            "time": step * 0.1,
            "velocity_change": 0.01 / step,
            "max_divergence_after": 0.001 / step,
        },
        x_cell_centers=np.array([0.25, 0.75]),
        y_cell_centers=np.array([0.25, 0.75]),
        pressure=np.full((2, 2), step, dtype=float),
        u_faces=np.full((2, 3), step, dtype=float),
        v_faces=np.full((3, 2), -step, dtype=float),
    )


def test_live_mode_displays_snapshots_from_externalized_store(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    run_id = "live-example-test"
    snapshot_directory = tmp_path / "sync" / run_id / "snapshots"
    snapshot = _snapshot(run_id, 1)
    run_result = SimpleNamespace(simulation=SimpleNamespace(steps=1))
    plotters = []

    class FakeLivePlotter:
        def __init__(self) -> None:
            self.updates: list[StepSnapshot] = []
            self.finished = False
            self.closed = False
            self.waits: list[float] = []
            plotters.append(self)

        def update(self, item: StepSnapshot) -> None:
            self.updates.append(item)

        def finish(self) -> None:
            self.finished = True

        def close(self) -> None:
            self.closed = True

        def wait_for_events(self, interval_seconds: float) -> None:
            self.waits.append(interval_seconds)

    def persist_snapshot(*args):
        current_run_id = args[6]
        store = SnapshotStore(snapshot_directory, run_id=current_run_id)
        store.write(snapshot)
        return run_result, snapshot_directory, current_run_id

    monkeypatch.setattr(run_externalized_case, "_run", persist_snapshot)
    monkeypatch.setattr(run_externalized_case, "LiveSnapshotPlotter", FakeLivePlotter)
    monkeypatch.setattr(matplotlib, "get_backend", lambda: "QtAgg")

    result, returned_directory, returned_run_id = run_externalized_case._run_live(
        {},
        tmp_path,
        "sync",
        queue_size=8,
        poll_interval=0.1,
        snapshot_every=10,
        run_id=run_id,
    )

    assert result is run_result
    assert returned_directory == snapshot_directory
    assert returned_run_id == run_id
    assert len(plotters) == 1
    assert [item.step for item in plotters[0].updates] == [1]
    np.testing.assert_array_equal(plotters[0].updates[0].pressure, snapshot.pressure)
    assert plotters[0].finished
    assert plotters[0].closed


def test_live_snapshot_plotter_updates_one_figure_for_multiple_steps(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(plt, "show", Mock())
    monkeypatch.setattr(plt, "pause", Mock())
    plotter = LiveSnapshotPlotter()
    figure = plotter.figure
    try:
        plotter.update(_snapshot("live-plotter-test", 1))
        plotter.update(_snapshot("live-plotter-test", 2))

        assert plotter.figure is figure
        assert plotter.steps == [1, 2]
        assert len(plotter.speed_axis.images) == 1
        assert len(plotter.pressure_axis.images) == 1
    finally:
        plotter.close()
