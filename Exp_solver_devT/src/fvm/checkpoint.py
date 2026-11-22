"""Atomic persistence and validated restoration of solver checkpoints."""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from dataclasses import asdict
from pathlib import Path
from typing import Mapping

import numpy as np

from .fields import ScalarField, VectorField
from .mesh import CartesianMesh
from .simulation import SimulationState, StepDiagnostics

CHECKPOINT_FORMAT_VERSION = "1.0"
_CHECKPOINT_NAME = re.compile(r"^checkpoint_(\d+)(?:_(\d+))?\.npz$")


class CheckpointError(ValueError):
    """A checkpoint is unreadable, invalid, or incompatible with a case."""


class CheckpointManager:
    """Read and write solver checkpoints in a dedicated directory.

    Numeric fields are stored in compressed NumPy archives. Metadata and the
    complete run configuration are JSON-encoded inside the archive; `latest.json`
    is the atomically updated pointer to the most recently committed checkpoint.
    """

    def __init__(self, directory: str | Path, retain_last: int = 5) -> None:
        if isinstance(retain_last, bool) or not isinstance(retain_last, int):
            raise TypeError("retain_last must be a positive integer")
        if retain_last < 1:
            raise ValueError("retain_last must be a positive integer")
        self.directory = Path(directory)
        self.retain_last = retain_last

    def save(
        self, state: SimulationState, case_document: Mapping[str, object]
    ) -> Path:
        """Commit a complete state and then update the latest-checkpoint pointer."""
        self._validate_state(state)
        normalized_case = json.loads(json.dumps(case_document, sort_keys=True))
        if not isinstance(normalized_case, dict):
            raise TypeError("case_document must be a JSON-compatible object")
        self.directory.mkdir(parents=True, exist_ok=True)
        target = self._next_path(state.completed_steps)
        metadata = {
            "checkpoint_format_version": CHECKPOINT_FORMAT_VERSION,
            "solver_version": "0.1.0",
            "completed_steps": state.completed_steps,
            "elapsed_time": state.elapsed_time,
            "pseudo_time": state.pseudo_time,
            "steady_time_step": state.steady_time_step,
            "mesh": {
                "nx": state.velocity.mesh.nx,
                "ny": state.velocity.mesh.ny,
                "width": state.velocity.mesh.width,
                "height": state.velocity.mesh.height,
            },
            "case": normalized_case,
            "configuration_fingerprint": configuration_fingerprint(normalized_case),
            "history": [asdict(item) for item in state.history],
        }
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{target.name}.", suffix=".tmp", dir=self.directory
        )
        temporary_path = Path(temporary_name)
        try:
            with os.fdopen(descriptor, "wb") as checkpoint_file:
                np.savez_compressed(
                    checkpoint_file,
                    u=state.velocity.u.values,
                    v=state.velocity.v.values,
                    pressure=state.pressure.values,
                    metadata=np.asarray(json.dumps(metadata, sort_keys=True)),
                )
                checkpoint_file.flush()
                os.fsync(checkpoint_file.fileno())
            self._read_archive(temporary_path, state.velocity.mesh)
            os.replace(temporary_path, target)
            latest = {
                "checkpoint_format_version": CHECKPOINT_FORMAT_VERSION,
                "file": target.name,
                "sha256": self._sha256(target),
                "completed_steps": state.completed_steps,
            }
            self._write_json_atomically(self.directory / "latest.json", latest)
        except Exception:
            temporary_path.unlink(missing_ok=True)
            raise

        self._apply_retention(target)
        return target

    def load(
        self,
        source: str | Path,
        case_document: Mapping[str, object],
        mesh: CartesianMesh,
    ) -> SimulationState:
        """Load `latest` or a specific archive after compatibility checks."""
        path, expected_digest = self._resolve_source(source)
        if expected_digest is not None:
            try:
                if self._sha256(path) != expected_digest:
                    raise CheckpointError(
                        "latest checkpoint SHA-256 does not match its manifest"
                    )
            except OSError as error:
                raise CheckpointError(f"cannot read latest checkpoint file: {error}") from error
        try:
            with np.load(path, allow_pickle=False) as archive:
                stored_mesh = self._read_metadata(archive)
                if stored_mesh.get("checkpoint_format_version") != CHECKPOINT_FORMAT_VERSION:
                    raise CheckpointError("unsupported checkpoint format version")
                metadata = stored_mesh
                saved_case = metadata.get("case")
                if not isinstance(saved_case, Mapping):
                    raise CheckpointError("checkpoint is missing its case configuration")
                if metadata.get("configuration_fingerprint") != configuration_fingerprint(
                    saved_case
                ):
                    raise CheckpointError("checkpoint case configuration fingerprint is invalid")
                validate_case_compatibility(saved_case, case_document)
                self._validate_mesh_metadata(metadata, mesh)
                pressure_values = np.asarray(archive["pressure"], dtype=np.float64)
                u_values = np.asarray(archive["u"], dtype=np.float64)
                v_values = np.asarray(archive["v"], dtype=np.float64)
                if pressure_values.shape != mesh.shape_for_location("cell_center"):
                    raise CheckpointError("checkpoint pressure array has an invalid shape")
                if u_values.shape != mesh.shape_for_location("x_face"):
                    raise CheckpointError("checkpoint u array has an invalid shape")
                if v_values.shape != mesh.shape_for_location("y_face"):
                    raise CheckpointError("checkpoint v array has an invalid shape")
                if not all(np.all(np.isfinite(values)) for values in (pressure_values, u_values, v_values)):
                    raise CheckpointError("checkpoint fields must contain only finite values")
                history_data = metadata.get("history")
                if not isinstance(history_data, list):
                    raise CheckpointError("checkpoint history is missing or invalid")
                history = tuple(StepDiagnostics(**item) for item in history_data)
                completed_steps = metadata.get("completed_steps")
                if (
                    isinstance(completed_steps, bool)
                    or not isinstance(completed_steps, int)
                    or completed_steps != len(history)
                ):
                    raise CheckpointError("checkpoint step count does not match its history")
                velocity = VectorField(mesh, name="velocity")
                velocity.set_values(u_values, v_values)
                pressure = ScalarField(mesh, name="pressure")
                pressure.set_values(pressure_values)
                state = SimulationState(
                    velocity=velocity,
                    pressure=pressure,
                    completed_steps=completed_steps,
                    elapsed_time=float(metadata["elapsed_time"]),
                    pseudo_time=float(metadata["pseudo_time"]),
                    steady_time_step=(
                        None
                        if metadata.get("steady_time_step") is None
                        else float(metadata["steady_time_step"])
                    ),
                    history=history,
                )
        except CheckpointError:
            raise
        except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
            raise CheckpointError(f"cannot load checkpoint {path}: {error}") from error
        self._validate_state(state)
        return state

    def _resolve_source(self, source: str | Path) -> tuple[Path, str | None]:
        if str(source) == "latest":
            manifest_path = self.directory / "latest.json"
            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                filename = manifest["file"]
                digest = manifest["sha256"]
                if Path(filename).name != filename or not isinstance(digest, str):
                    raise ValueError("invalid latest manifest fields")
                return self.directory / filename, digest
            except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
                raise CheckpointError(f"cannot read latest checkpoint manifest: {error}") from error
        path = Path(source)
        if not path.is_absolute():
            path = self.directory / path
        if not path.is_file():
            raise CheckpointError(f"checkpoint file does not exist: {path}")
        return path, None

    def _next_path(self, completed_steps: int) -> Path:
        base = f"checkpoint_{completed_steps:08d}"
        candidate = self.directory / f"{base}.npz"
        suffix = 2
        while candidate.exists():
            candidate = self.directory / f"{base}_{suffix}.npz"
            suffix += 1
        return candidate

    def _apply_retention(self, latest_path: Path) -> None:
        checkpoints = []
        for path in self.directory.glob("checkpoint_*.npz"):
            match = _CHECKPOINT_NAME.match(path.name)
            if match:
                checkpoints.append((int(match.group(1)), path.stat().st_mtime_ns, path))
        checkpoints.sort(reverse=True)
        retained = {path for _, _, path in checkpoints[: self.retain_last]}
        retained.add(latest_path)
        for _, _, path in checkpoints:
            if path not in retained:
                try:
                    path.unlink()
                except OSError:
                    pass

    @staticmethod
    def _read_metadata(archive: np.lib.npyio.NpzFile) -> dict[str, object]:
        try:
            raw = archive["metadata"]
            if raw.shape != ():
                raise ValueError("metadata must be a scalar JSON value")
            metadata = json.loads(str(raw.item()))
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
            raise CheckpointError(f"invalid checkpoint metadata: {error}") from error
        if not isinstance(metadata, dict):
            raise CheckpointError("checkpoint metadata root must be a JSON object")
        return metadata

    @staticmethod
    def _read_archive(path: Path, mesh: CartesianMesh) -> None:
        try:
            with np.load(path, allow_pickle=False) as archive:
                metadata = CheckpointManager._read_metadata(archive)
                if metadata.get("checkpoint_format_version") != CHECKPOINT_FORMAT_VERSION:
                    raise CheckpointError("unsupported checkpoint format version")
                for name, location in (
                    ("pressure", "cell_center"),
                    ("u", "x_face"),
                    ("v", "y_face"),
                ):
                    values = np.asarray(archive[name])
                    if values.shape != mesh.shape_for_location(location):
                        raise CheckpointError(f"checkpoint {name} array has an invalid shape")
                    if not np.all(np.isfinite(values)):
                        raise CheckpointError(f"checkpoint {name} array is not finite")
        except CheckpointError:
            raise
        except (OSError, KeyError, TypeError, ValueError) as error:
            raise CheckpointError(f"checkpoint validation failed: {error}") from error

    @staticmethod
    def _validate_state(state: SimulationState) -> None:
        if not isinstance(state, SimulationState):
            raise TypeError("state must be a SimulationState")
        if state.completed_steps < 0 or len(state.history) != state.completed_steps:
            raise CheckpointError("state history must cover all completed steps")
        if state.history and state.history[-1].step != state.completed_steps:
            raise CheckpointError("state history step does not match completed_steps")
        for value in (state.elapsed_time, state.pseudo_time):
            if not np.isfinite(value) or value < 0.0:
                raise CheckpointError("state times must be finite and non-negative")
        if state.steady_time_step is not None and (
            not np.isfinite(state.steady_time_step) or state.steady_time_step <= 0.0
        ):
            raise CheckpointError("steady_time_step must be finite and positive")
        for values in (
            state.velocity.u.values,
            state.velocity.v.values,
            state.pressure.values,
        ):
            if not np.all(np.isfinite(values)):
                raise CheckpointError("state fields must contain only finite values")

    @staticmethod
    def _validate_mesh_metadata(
        metadata: Mapping[str, object], mesh: CartesianMesh
    ) -> None:
        stored = metadata.get("mesh")
        if not isinstance(stored, Mapping):
            raise CheckpointError("checkpoint mesh metadata is missing")
        expected = {
            "nx": mesh.nx,
            "ny": mesh.ny,
            "width": mesh.width,
            "height": mesh.height,
        }
        if any(stored.get(key) != value for key, value in expected.items()):
            raise CheckpointError("checkpoint mesh does not match the case mesh")

    @staticmethod
    def _sha256(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as checkpoint_file:
            for block in iter(lambda: checkpoint_file.read(1024 * 1024), b""):
                digest.update(block)
        return digest.hexdigest()

    @staticmethod
    def _write_json_atomically(path: Path, document: Mapping[str, object]) -> None:
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
        )
        temporary_path = Path(temporary_name)
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as output:
                json.dump(document, output, indent=2, sort_keys=True)
                output.write("\n")
                output.flush()
                os.fsync(output.fileno())
            os.replace(temporary_path, path)
        except Exception:
            temporary_path.unlink(missing_ok=True)
            raise


def configuration_fingerprint(case_document: Mapping[str, object]) -> str:
    """Hash numerical case inputs, excluding permitted continuation limits."""
    normalized = json.loads(json.dumps(case_document, sort_keys=True))
    solver = normalized.get("solver")
    if isinstance(solver, dict):
        solver.pop("max_steps", None)
        solver.pop("end_time_s", None)
    encoded = json.dumps(normalized, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def validate_case_compatibility(
    saved_case: Mapping[str, object], current_case: Mapping[str, object]
) -> None:
    """Allow only monotonic run-limit extensions during a checkpoint restart."""
    saved_solver = saved_case.get("solver")
    current_solver = current_case.get("solver")
    if not isinstance(saved_solver, Mapping) or not isinstance(current_solver, Mapping):
        raise CheckpointError("case configuration is missing solver settings")
    if configuration_fingerprint(saved_case) != configuration_fingerprint(current_case):
        raise CheckpointError(
            "case configuration is incompatible with this checkpoint; mesh, physics, "
            "boundaries, initial conditions, and numerical controls must match"
        )
    saved_steps = saved_solver.get("max_steps")
    current_steps = current_solver.get("max_steps")
    if (
        isinstance(saved_steps, int)
        and not isinstance(saved_steps, bool)
        and isinstance(current_steps, int)
        and not isinstance(current_steps, bool)
        and current_steps < saved_steps
    ):
        raise CheckpointError("max_steps may be increased on restart, but not reduced")
    saved_end_time = saved_solver.get("end_time_s")
    current_end_time = current_solver.get("end_time_s")
    if saved_end_time != current_end_time:
        if (
            isinstance(saved_end_time, (int, float))
            and not isinstance(saved_end_time, bool)
            and isinstance(current_end_time, (int, float))
            and not isinstance(current_end_time, bool)
            and current_end_time >= saved_end_time
        ):
            return
        raise CheckpointError("end_time_s may be increased on restart, but not removed or reduced")