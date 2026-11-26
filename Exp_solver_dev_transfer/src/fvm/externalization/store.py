"""Atomic, replayable local snapshot storage used by every transport strategy."""

from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
from collections.abc import Iterator
from numbers import Integral
from time import sleep

from .model import StepSnapshot, validate_run_id


class SnapshotStore:
    """Persist snapshots as atomically committed, independently readable files."""

    def __init__(self, directory: str | Path, run_id: str | None = None) -> None:
        self.directory = Path(directory)
        self.run_id = None if run_id is None else validate_run_id(run_id)

    def write(self, snapshot: StepSnapshot) -> int:
        """Atomically write a snapshot and return the committed byte count."""
        if not isinstance(snapshot, StepSnapshot):
            raise TypeError("snapshot must be a StepSnapshot")
        if self.run_id is not None and snapshot.run_id != self.run_id:
            raise ValueError("snapshot run_id does not match this store")
        run_directory = self.directory / snapshot.run_id
        run_directory.mkdir(parents=True, exist_ok=True)
        target = run_directory / f"step_{snapshot.step:08d}.npz"
        manifest_path = run_directory / "latest.json"
        previous_manifest = self._read_manifest(snapshot.run_id)
        previous_latest = (
            previous_manifest["latest_step"]
            if previous_manifest is not None
            else snapshot.step
        )
        if previous_manifest is not None and snapshot.step < previous_latest:
            raise ValueError("snapshot steps must be written in increasing order")
        payload = snapshot.to_bytes()
        self._atomic_write(target, payload)
        manifest = {
            "format_version": 1,
            "run_id": snapshot.run_id,
            "first_step": min(
                snapshot.step,
                previous_manifest["first_step"]
                if previous_manifest is not None
                else snapshot.step,
            ),
            "latest_step": max(snapshot.step, previous_latest),
        }
        self._atomic_write(
            manifest_path,
            json.dumps(manifest, allow_nan=False).encode("utf-8"),
        )
        return len(payload)

    @staticmethod
    def _atomic_write(target: Path, payload: bytes) -> None:
        file_descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{target.name}.", suffix=".tmp", dir=target.parent
        )
        try:
            with os.fdopen(file_descriptor, "wb") as temporary_file:
                temporary_file.write(payload)
                temporary_file.flush()
                os.fsync(temporary_file.fileno())
            os.replace(temporary_name, target)
        except OSError:
            try:
                os.unlink(temporary_name)
            except FileNotFoundError:
                pass
            raise

    def read(self, step: int, run_id: str | None = None) -> StepSnapshot:
        """Read one complete committed step."""
        if isinstance(step, bool) or not isinstance(step, Integral) or step <= 0:
            raise ValueError("step must be a positive integer")
        step = int(step)
        selected_run = self.run_id if run_id is None else run_id
        if selected_run is None:
            matches = [
                candidate
                for candidate_run in self.list_run_ids()
                for candidate in (
                    self.directory / candidate_run / f"step_{step:08d}.npz",
                )
                if candidate.exists()
            ]
            if len(matches) > 1:
                raise ValueError("run_id is required when multiple runs contain this step")
            if not matches:
                raise FileNotFoundError(
                    self.directory / f"*/step_{step:08d}.npz"
                )
            path = matches[0]
        else:
            validate_run_id(selected_run)
            path = self.directory / selected_run / f"step_{step:08d}.npz"
        return StepSnapshot.from_bytes(path.read_bytes())

    def iter_after(
        self, step: int = 0, run_id: str | None = None
    ) -> Iterator[StepSnapshot]:
        """Yield committed snapshots in ascending step order."""
        if isinstance(step, bool) or not isinstance(step, Integral) or step < 0:
            raise ValueError("step must be a non-negative integer")
        step = int(step)
        selected_run = self.run_id if run_id is None else run_id
        if selected_run is not None:
            validate_run_id(selected_run)
        run_ids = (selected_run,) if selected_run is not None else self.list_run_ids()
        for current_run in run_ids:
            latest = self.latest_step_for(current_run)
            first = self.first_step_for(current_run)
            run_directory = self.directory / current_run
            step_numbers = sorted(
                int(path.stem[5:])
                for path in run_directory.glob("step_*.npz")
                if path.stem[5:].isdecimal()
            )
            for current_step in step_numbers:
                if current_step < max(step + 1, first) or current_step > latest:
                    continue
                yield self.read(current_step, current_run)

    def iter_after_by_run(
        self, last_steps: dict[str, int]
    ) -> Iterator[StepSnapshot]:
        """Yield new snapshots using an independent cursor for every run."""
        for run_id in self.list_run_ids():
            yield from self.iter_after(last_steps.get(run_id, 0), run_id)

    @property
    def latest_step(self) -> int:
        """Return the largest committed step, or zero when the store is empty."""
        if self.run_id is not None:
            return self.latest_step_for(self.run_id)
        return max(
            (self.latest_step_for(run_id) for run_id in self.list_run_ids()),
            default=0,
        )

    def latest_step_for(self, run_id: str) -> int:
        """Return the latest step for one run."""
        manifest = self._read_manifest(run_id)
        return 0 if manifest is None else manifest["latest_step"]

    def first_step_for(self, run_id: str) -> int:
        """Return the earliest committed step for one run."""
        manifest = self._read_manifest(run_id)
        return 0 if manifest is None else manifest["first_step"]

    def _read_manifest(self, run_id: str) -> dict[str, int | str] | None:
        validate_run_id(run_id)
        manifest_path = self.directory / run_id / "latest.json"
        if not manifest_path.exists():
            return None
        for attempt in range(3):
            try:
                manifest_text = manifest_path.read_text(encoding="utf-8")
                break
            except PermissionError:
                if attempt == 2:
                    raise
                sleep(0.01)
        manifest = json.loads(manifest_text)
        if not isinstance(manifest, dict):
            raise ValueError(f"invalid latest snapshot manifest: {manifest_path}")
        first_step = manifest.get("first_step")
        latest_step = manifest.get("latest_step")
        version = manifest.get("format_version")
        if (
            isinstance(version, bool)
            or not isinstance(version, int)
            or version != 1
            or manifest.get("run_id") != run_id
            or isinstance(first_step, bool)
            or not isinstance(first_step, int)
            or first_step <= 0
            or isinstance(latest_step, bool)
            or not isinstance(latest_step, int)
            or latest_step < first_step
        ):
            raise ValueError(f"invalid latest snapshot manifest: {manifest_path}")
        return manifest

    def list_run_ids(self) -> tuple[str, ...]:
        """List run directories that contain at least one committed snapshot."""
        if not self.directory.exists():
            return ()
        return tuple(
            sorted(
                path.name
                for path in self.directory.iterdir()
                if path.is_dir() and (path / "latest.json").is_file()
            )
        )

    @property
    def latest_snapshot(self) -> StepSnapshot:
        """Read the most recently committed snapshot across this store."""
        run_ids = (self.run_id,) if self.run_id is not None else self.list_run_ids()
        candidates = [
            self.directory / run_id / "latest.json"
            for run_id in run_ids
            if (self.directory / run_id / "latest.json").is_file()
        ]
        if not candidates:
            raise FileNotFoundError(f"snapshot store is empty: {self.directory}")
        latest_manifest = max(candidates, key=lambda path: path.stat().st_mtime_ns)
        run_id = latest_manifest.parent.name
        return self.read(self.latest_step_for(run_id), run_id=run_id)
