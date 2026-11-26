"""Local externalization strategies and the solver-observer adapter."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import queue
import threading
from time import perf_counter
from numbers import Integral
from typing import Protocol

from .model import StepSnapshot, validate_run_id
from .store import SnapshotStore


class Externalizer(Protocol):
    """Minimal transport contract consumed by solver integrations."""

    def publish(self, snapshot: StepSnapshot) -> None: ...

    def close(self) -> None: ...


class StepSnapshotObserver:
    """Sample completed solver steps and allow an explicit final-step publish."""

    def __init__(
        self,
        externalizer: Externalizer,
        run_id: str,
        snapshot_every: int = 10,
    ) -> None:
        if (
            isinstance(snapshot_every, bool)
            or not isinstance(snapshot_every, Integral)
            or snapshot_every <= 0
        ):
            raise ValueError("snapshot_every must be a positive integer")
        self.externalizer = externalizer
        self.run_id = validate_run_id(run_id)
        self.snapshot_every = int(snapshot_every)
        self._last_published_step = 0

    def __call__(self, diagnostics: object, velocity: object, pressure: object) -> None:
        step = self._step_number(diagnostics)
        if step % self.snapshot_every == 0:
            self._publish(diagnostics, velocity, pressure)

    def publish_final_step(
        self, diagnostics: object, velocity: object, pressure: object
    ) -> bool:
        """Publish the final state unless that step was already sampled."""
        step = self._step_number(diagnostics)
        if step == self._last_published_step:
            return False
        if step < self._last_published_step:
            raise ValueError("final snapshot step precedes the last published step")
        self._publish(diagnostics, velocity, pressure)
        return True

    @staticmethod
    def _step_number(diagnostics: object) -> int:
        step = getattr(diagnostics, "step", None)
        if (
            isinstance(step, bool)
            or not isinstance(step, Integral)
            or step <= 0
        ):
            raise ValueError("step diagnostics must contain a positive integer step")
        return int(step)

    def _publish(self, diagnostics: object, velocity: object, pressure: object) -> None:
        snapshot = StepSnapshot.from_solver_step(
            self.run_id, diagnostics, velocity, pressure
        )
        if snapshot.step <= self._last_published_step:
            raise ValueError("snapshots must be published in increasing step order")
        self.externalizer.publish(snapshot)
        self._last_published_step = snapshot.step


@dataclass(slots=True)
class ExternalizationMetrics:
    """Timing and volume counters for an externalization session."""

    snapshots: int = 0
    bytes_written: int = 0
    publish_seconds: float = 0.0
    externalize_seconds: float = 0.0
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def record(
        self,
        byte_count: int,
        publish_seconds: float,
        externalize_seconds: float,
    ) -> None:
        with self._lock:
            self.snapshots += 1
            self.bytes_written += byte_count
            self.publish_seconds += publish_seconds
            self.externalize_seconds += externalize_seconds

    def record_publish(self, byte_count: int, elapsed: float) -> None:
        with self._lock:
            self.snapshots += 1
            self.bytes_written += byte_count
            self.publish_seconds += elapsed

    def record_publish_time(self, elapsed: float) -> None:
        with self._lock:
            self.publish_seconds += elapsed

    def record_externalize(self, byte_count: int, elapsed: float) -> None:
        with self._lock:
            self.snapshots += 1
            self.bytes_written += byte_count
            self.externalize_seconds += elapsed

    def record_externalize_time(self, elapsed: float) -> None:
        with self._lock:
            self.externalize_seconds += elapsed


class SynchronousFileExternalizer:
    """Strategy 1: synchronously persist each solver step before continuing."""

    def __init__(self, directory: str | Path) -> None:
        self.store = SnapshotStore(directory)
        self.metrics = ExternalizationMetrics()
        self._closed = False

    def publish(self, snapshot: StepSnapshot) -> None:
        self._ensure_open()
        started = perf_counter()
        byte_count = self.store.write(snapshot)
        elapsed = perf_counter() - started
        self.metrics.record(byte_count, elapsed, elapsed)

    def close(self) -> None:
        self._closed = True

    def _ensure_open(self) -> None:
        if self._closed:
            raise RuntimeError("externalizer is closed")


class SharedFolderExternalizer:
    """Strategy 2 producer: commit snapshots to a shared-folder spool."""

    def __init__(self, shared_directory: str | Path) -> None:
        self.store = SnapshotStore(shared_directory)
        self.metrics = ExternalizationMetrics()
        self._closed = False

    def publish(self, snapshot: StepSnapshot) -> None:
        if self._closed:
            raise RuntimeError("externalizer is closed")
        started = perf_counter()
        byte_count = self.store.write(snapshot)
        self.metrics.record_publish(byte_count, perf_counter() - started)

    def close(self) -> None:
        self._closed = True


class SharedFolderPoller:
    """Independent consumer that periodically drains committed shared snapshots."""

    def __init__(
        self, shared_directory: str | Path, external_directory: str | Path
    ) -> None:
        self.source = SnapshotStore(shared_directory)
        self.destination = SnapshotStore(external_directory)
        self.last_steps = {
            run_id: self.destination.latest_step_for(run_id)
            for run_id in self.destination.list_run_ids()
        }
        self.snapshots = 0
        self.bytes_written = 0
        self.externalize_seconds = 0.0

    def poll_once(self) -> int:
        """Copy every newly committed snapshot; return the number copied."""
        copied = 0
        for snapshot in self.source.iter_after_by_run(self.last_steps):
            started = perf_counter()
            byte_count = self.destination.write(snapshot)
            self.externalize_seconds += perf_counter() - started
            self.bytes_written += byte_count
            self.snapshots += 1
            self.last_steps[snapshot.run_id] = snapshot.step
            copied += 1
        return copied

    def run(
        self,
        interval_seconds: float,
        stop_event: threading.Event | None = None,
    ) -> None:
        """Poll until stopped; surface storage errors to the caller."""
        if interval_seconds <= 0.0:
            raise ValueError("interval_seconds must be positive")
        stop = stop_event or threading.Event()
        while not stop.is_set():
            self.poll_once()
            stop.wait(interval_seconds)
        self.poll_once()


class AsyncFileExternalizer:
    """Strategy 3: bounded in-process queue drained by a dedicated worker."""

    def __init__(self, directory: str | Path, queue_size: int = 16) -> None:
        if isinstance(queue_size, bool) or not isinstance(queue_size, int) or queue_size <= 0:
            raise ValueError("queue_size must be a positive integer")
        self.store = SnapshotStore(directory)
        self.metrics = ExternalizationMetrics()
        self._queue: queue.Queue[StepSnapshot | None] = queue.Queue(queue_size)
        self._error: Exception | None = None
        self._closed = False
        self._worker = threading.Thread(
            target=self._consume, name="fvm-externalizer", daemon=True
        )
        self._worker.start()

    def publish(self, snapshot: StepSnapshot) -> None:
        if self._closed:
            raise RuntimeError("externalizer is closed")
        started = perf_counter()
        while True:
            self._raise_worker_error()
            try:
                self._queue.put(snapshot, timeout=0.1)
                break
            except queue.Full:
                continue
        self.metrics.record_publish_time(perf_counter() - started)

    def close(self) -> None:
        if self._closed:
            self._raise_worker_error()
            return
        self._closed = True
        self._enqueue_stop()
        self._worker.join()
        self._raise_worker_error()

    def _enqueue_stop(self) -> None:
        while self._worker.is_alive():
            try:
                self._queue.put(None, timeout=0.1)
                return
            except queue.Full:
                continue

    def _consume(self) -> None:
        while True:
            item = self._queue.get()
            try:
                if item is None:
                    return
                started = perf_counter()
                try:
                    byte_count = self.store.write(item)
                except Exception as error:
                    if self._error is None:
                        self._error = error
                else:
                    self.metrics.record_externalize(
                        byte_count, perf_counter() - started
                    )
            finally:
                self._queue.task_done()

    def _raise_worker_error(self) -> None:
        if self._error is not None:
            raise RuntimeError(
                f"asynchronous externalization failed: {self._error}"
            ) from self._error


def create_step_observer(
    externalizer: Externalizer, run_id: str, snapshot_every: int = 10
) -> StepSnapshotObserver:
    """Sample solver callbacks every N steps; callers may force the final step."""
    return StepSnapshotObserver(externalizer, run_id, snapshot_every)
