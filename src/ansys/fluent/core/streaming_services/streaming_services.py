import threading
from typing import Optional


class StreamingService:
    """Encapsulates a Fluent streaming service."""

    def __init__(self, target, streaming_service):
        self._lock: threading.Lock = threading.Lock()
        self._streaming: bool = False
        self._target = target
        self._streaming_service = streaming_service
        self._stream_thread: Optional[threading.Thread] = None

    @property
    def is_streaming(self):
        with self._lock:
            return self._streaming

    def start(self) -> None:
        """Start streaming of Fluent transcript."""
        with self._lock:
            if self._stream_thread is None:
                started_evt = threading.Event()
                self._stream_thread = threading.Thread(
                    target=self._target, args=(self, started_evt)
                )
                self._stream_thread.start()
                started_evt.wait()

    def stop(self) -> None:
        """Stop streaming of Fluent transcript."""
        if self.is_streaming:
            self._streaming_service.end_streaming()
            self._stream_thread.join()
            self._streaming = False
            self._stream_thread = None
