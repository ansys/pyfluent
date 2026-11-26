"""Optional gRPC streaming transport for externalized solver snapshots."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import json
from math import isfinite
from pathlib import Path
import queue
import threading
from time import perf_counter

import grpc
from google.protobuf.wrappers_pb2 import BytesValue

from .model import StepSnapshot
from .strategies import ExternalizationMetrics
from .store import SnapshotStore

_SERVICE = "fvm.externalization.v1.SnapshotService"
_METHOD = f"/{_SERVICE}/Publish"


class GrpcSnapshotServer:
    """Local or cloud-side gRPC endpoint that durably consumes snapshot streams."""

    def __init__(
        self,
        directory: str | Path,
        address: str = "127.0.0.1:0",
        max_message_bytes: int = 64 * 1024 * 1024,
    ) -> None:
        if (
            isinstance(max_message_bytes, bool)
            or not isinstance(max_message_bytes, int)
            or max_message_bytes <= 0
        ):
            raise ValueError("max_message_bytes must be a positive integer")
        self.store = SnapshotStore(directory)
        self.address = address
        self._server = grpc.server(
            ThreadPoolExecutor(max_workers=4),
            options=(("grpc.max_receive_message_length", max_message_bytes),),
        )
        handler = grpc.stream_unary_rpc_method_handler(
            self._publish,
            request_deserializer=BytesValue.FromString,
            response_serializer=BytesValue.SerializeToString,
        )
        self._server.add_generic_rpc_handlers(
            (grpc.method_handlers_generic_handler(_SERVICE, {"Publish": handler}),)
        )
        self._bound_port: int | None = None
        self._run_locks: dict[str, threading.Lock] = {}
        self._run_locks_guard = threading.Lock()

    @property
    def target(self) -> str:
        """Return the actual bound address after ``start``."""
        if self._bound_port is None:
            raise RuntimeError("gRPC server has not been started")
        host = self.address.rsplit(":", 1)[0]
        return f"{host}:{self._bound_port}"

    def start(self, credentials: grpc.ServerCredentials | None = None) -> str:
        if self._bound_port is not None:
            return self.target
        port = (
            self._server.add_secure_port(self.address, credentials)
            if credentials is not None
            else self._server.add_insecure_port(self.address)
        )
        if port == 0:
            raise OSError(f"could not bind gRPC server to {self.address}")
        self._bound_port = port
        self._server.start()
        return self.target

    def stop(self, grace_seconds: float = 1.0) -> None:
        if self._bound_port is not None:
            self._server.stop(grace_seconds).wait()
            self._bound_port = None

    def _publish(self, requests, context) -> BytesValue:
        count = 0
        externalize_seconds = 0.0
        run_id: str | None = None
        last_step = 0
        run_lock: threading.Lock | None = None
        lock_acquired = False
        try:
            for request in requests:
                snapshot = StepSnapshot.from_bytes(request.value)
                if run_id is None:
                    run_id = snapshot.run_id
                    with self._run_locks_guard:
                        run_lock = self._run_locks.setdefault(
                            run_id, threading.Lock()
                        )
                        lock_acquired = run_lock.acquire(blocking=False)
                    if not lock_acquired:
                        context.abort(
                            grpc.StatusCode.ABORTED,
                            f"another stream is publishing run_id {run_id}",
                        )
                    last_step = self.store.latest_step_for(run_id)
                elif snapshot.run_id != run_id:
                    context.abort(
                        grpc.StatusCode.INVALID_ARGUMENT,
                        "one gRPC stream may publish only one run_id",
                    )
                if snapshot.step <= last_step:
                    context.abort(
                        grpc.StatusCode.INVALID_ARGUMENT,
                        f"snapshot step {snapshot.step} is not after {last_step}",
                    )
                started = perf_counter()
                self.store.write(snapshot)
                externalize_seconds += perf_counter() - started
                last_step = snapshot.step
                count += 1
            return BytesValue(
                value=json.dumps(
                    {
                        "snapshots": count,
                        "externalize_seconds": externalize_seconds,
                    },
                    allow_nan=False,
                ).encode("utf-8")
            )
        finally:
            if run_id is not None and run_lock is not None and lock_acquired:
                with self._run_locks_guard:
                    run_lock.release()
                    if self._run_locks.get(run_id) is run_lock:
                        del self._run_locks[run_id]


class GrpcExternalizer:
    """Strategy 4: stream snapshots over a bounded asynchronous gRPC channel."""

    def __init__(
        self,
        target: str,
        queue_size: int = 16,
        timeout_seconds: float | None = None,
        max_message_bytes: int = 64 * 1024 * 1024,
        credentials: grpc.ChannelCredentials | None = None,
    ) -> None:
        if isinstance(queue_size, bool) or not isinstance(queue_size, int) or queue_size <= 0:
            raise ValueError("queue_size must be a positive integer")
        if timeout_seconds is not None and timeout_seconds <= 0.0:
            raise ValueError("timeout_seconds must be positive")
        if (
            isinstance(max_message_bytes, bool)
            or not isinstance(max_message_bytes, int)
            or max_message_bytes <= 0
        ):
            raise ValueError("max_message_bytes must be a positive integer")
        self.metrics = ExternalizationMetrics()
        self._queue: queue.Queue[bytes | None] = queue.Queue(queue_size)
        self._timeout_seconds = timeout_seconds
        options = (
            ("grpc.max_send_message_length", max_message_bytes),
            ("grpc.max_receive_message_length", max_message_bytes),
        )
        self._channel = (
            grpc.secure_channel(target, credentials, options=options)
            if credentials is not None
            else grpc.insecure_channel(target, options=options)
        )
        self._publish_call = self._channel.stream_unary(
            _METHOD,
            request_serializer=BytesValue.SerializeToString,
            response_deserializer=BytesValue.FromString,
        )
        self._error: Exception | None = None
        self._closed = False
        self._sent = 0
        self._worker = threading.Thread(
            target=self._stream, name="fvm-grpc-externalizer", daemon=True
        )
        self._worker.start()

    def publish(self, snapshot: StepSnapshot) -> None:
        if self._closed:
            raise RuntimeError("externalizer is closed")
        started = perf_counter()
        payload = snapshot.to_bytes()
        while True:
            self._raise_worker_error()
            try:
                self._queue.put(payload, timeout=0.1)
                self._sent += 1
                break
            except queue.Full:
                continue
        self.metrics.record_publish(len(payload), perf_counter() - started)

    def close(self) -> None:
        if self._closed:
            self._raise_worker_error()
            return
        self._closed = True
        worker_error: RuntimeError | None = None
        while self._worker.is_alive():
            try:
                self._raise_worker_error()
            except RuntimeError as error:
                worker_error = error
                break
            try:
                self._queue.put(None, timeout=0.1)
                break
            except queue.Full:
                continue
        self._worker.join(timeout=self._timeout_seconds)
        if self._timeout_seconds is not None and self._worker.is_alive():
            self._channel.close()
            raise TimeoutError("gRPC externalization did not finish before timeout")
        self._channel.close()
        if worker_error is not None:
            raise worker_error
        self._raise_worker_error()

    def _requests(self):
        while True:
            item = self._queue.get()
            try:
                if item is None:
                    return
                yield BytesValue(value=item)
            finally:
                self._queue.task_done()

    def _stream(self) -> None:
        try:
            response = self._publish_call(
                self._requests(), timeout=self._timeout_seconds
            )
            acknowledgement = json.loads(response.value.decode("utf-8"))
            acknowledged = acknowledgement["snapshots"]
            externalize_seconds = acknowledgement["externalize_seconds"]
            if (
                isinstance(acknowledged, bool)
                or not isinstance(acknowledged, int)
                or not isinstance(externalize_seconds, (int, float))
                or isinstance(externalize_seconds, bool)
                or not isfinite(externalize_seconds)
                or externalize_seconds < 0.0
            ):
                raise ValueError("gRPC server returned invalid metrics")
            if acknowledged != self._sent:
                raise RuntimeError(
                    f"gRPC acknowledged {acknowledged} snapshots; sent {self._sent}"
                )
            self.metrics.record_externalize_time(float(externalize_seconds))
        except Exception as error:
            self._error = error

    def _raise_worker_error(self) -> None:
        if self._error is not None:
            raise RuntimeError(f"gRPC externalization failed: {self._error}") from self._error
