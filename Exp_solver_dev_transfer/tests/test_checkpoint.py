import json

import numpy as np
import pytest

from fvm import BoundaryConditions, CartesianMesh, MovingWall, NoSlipWall, ScalarField, TransientSolver, VectorField
from fvm.checkpoint import (
    CheckpointError,
    CheckpointManager,
    validate_case_compatibility,
)


def _case_document(max_steps: int = 4) -> dict[str, object]:
    return {
        "case_id": "checkpoint_test",
        "mesh": {"nx": 5, "ny": 5, "width_m": 1.0, "height_m": 1.0},
        "material": {"density_kg_m3": 1.0, "dynamic_viscosity_pa_s": 0.01},
        "solver": {"max_steps": max_steps},
    }


def _saved_state(max_steps: int = 2):
    mesh = CartesianMesh(nx=5, ny=5)
    boundaries = BoundaryConditions()
    for side in ("west", "east", "south"):
        boundaries.set("velocity", side, NoSlipWall())
    boundaries.set("velocity", "north", MovingWall((1.0, 0.0)))
    states = []
    TransientSolver(
        density=1.0,
        viscosity=0.01,
        max_time_step=0.001,
        max_steps=max_steps,
        velocity_tolerance=1e-14,
    ).run(
        VectorField(mesh),
        ScalarField(mesh, name="pressure"),
        boundaries,
        state_observer=states.append,
    )
    return mesh, states[-1]


def test_checkpoint_round_trips_state_and_loads_latest_or_specific(tmp_path) -> None:
    mesh, state = _saved_state()
    manager = CheckpointManager(tmp_path / "checkpoints")
    checkpoint_path = manager.save(state, _case_document(max_steps=2))

    latest = manager.load("latest", _case_document(max_steps=4), mesh)
    specific = manager.load(checkpoint_path.name, _case_document(max_steps=2), mesh)

    for restored in (latest, specific):
        assert restored.completed_steps == state.completed_steps == 2
        assert restored.elapsed_time == state.elapsed_time
        assert restored.history == state.history
        np.testing.assert_array_equal(restored.velocity.u.values, state.velocity.u.values)
        np.testing.assert_array_equal(restored.velocity.v.values, state.velocity.v.values)
        np.testing.assert_array_equal(restored.pressure.values, state.pressure.values)
    manifest = json.loads((tmp_path / "checkpoints" / "latest.json").read_text())
    assert manifest["file"] == checkpoint_path.name


def test_checkpoint_rejects_numerically_incompatible_case(tmp_path) -> None:
    mesh, state = _saved_state()
    manager = CheckpointManager(tmp_path / "checkpoints")
    manager.save(state, _case_document())
    changed_case = _case_document()
    changed_case["material"] = {
        "density_kg_m3": 1.0,
        "dynamic_viscosity_pa_s": 0.02,
    }

    with pytest.raises(CheckpointError, match="incompatible"):
        manager.load("latest", changed_case, mesh)


def test_restart_compatibility_allows_only_increasing_run_limits() -> None:
    saved_case = _case_document(max_steps=100)
    saved_case["solver"]["end_time_s"] = 1.0
    extended_case = _case_document(max_steps=200)
    extended_case["solver"]["end_time_s"] = 2.0

    validate_case_compatibility(saved_case, extended_case)

    reduced_steps = _case_document(max_steps=99)
    reduced_steps["solver"]["end_time_s"] = 1.0
    with pytest.raises(CheckpointError, match="max_steps may be increased"):
        validate_case_compatibility(saved_case, reduced_steps)
    reduced_time = _case_document(max_steps=100)
    reduced_time["solver"]["end_time_s"] = 0.5
    with pytest.raises(CheckpointError, match="end_time_s may be increased"):
        validate_case_compatibility(saved_case, reduced_time)


def test_checkpoint_latest_detects_modified_archive(tmp_path) -> None:
    mesh, state = _saved_state()
    manager = CheckpointManager(tmp_path / "checkpoints")
    checkpoint_path = manager.save(state, _case_document())
    checkpoint_path.write_bytes(checkpoint_path.read_bytes() + b"corrupt")

    with pytest.raises(CheckpointError, match="SHA-256"):
        manager.load("latest", _case_document(), mesh)


def test_checkpoint_retention_keeps_latest_and_newest_steps(tmp_path) -> None:
    mesh = CartesianMesh(nx=5, ny=5)
    boundaries = BoundaryConditions()
    for side in ("west", "east", "south"):
        boundaries.set("velocity", side, NoSlipWall())
    boundaries.set("velocity", "north", MovingWall((1.0, 0.0)))
    states = []
    TransientSolver(
        density=1.0,
        viscosity=0.01,
        max_time_step=0.001,
        max_steps=4,
        velocity_tolerance=1e-14,
    ).run(
        VectorField(mesh),
        ScalarField(mesh, name="pressure"),
        boundaries,
        state_observer=states.append,
    )
    manager = CheckpointManager(tmp_path / "checkpoints", retain_last=2)

    for state in states:
        manager.save(state, _case_document())

    retained = list((tmp_path / "checkpoints").glob("checkpoint_*.npz"))
    assert len(retained) == 2
    assert manager.load("latest", _case_document(), mesh).completed_steps == 4


def test_failed_checkpoint_write_preserves_previous_latest(tmp_path, monkeypatch) -> None:
    mesh, first_state = _saved_state(max_steps=1)
    _, next_state = _saved_state(max_steps=2)
    manager = CheckpointManager(tmp_path / "checkpoints")
    manager.save(first_state, _case_document())
    latest_before = (tmp_path / "checkpoints" / "latest.json").read_text()

    def fail_write(*args, **kwargs):
        raise OSError("simulated disk failure")

    monkeypatch.setattr("fvm.checkpoint.np.savez_compressed", fail_write)
    with pytest.raises(OSError, match="simulated disk failure"):
        manager.save(next_state, _case_document())

    assert (tmp_path / "checkpoints" / "latest.json").read_text() == latest_before
    restored = manager.load("latest", _case_document(), mesh)
    assert restored.completed_steps == 1