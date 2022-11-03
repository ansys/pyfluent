from functools import partial
import itertools
import threading
from typing import Callable, Optional


class StreamingService:
    """Encapsulates a Fluent streaming service."""

    def __init__(self, target, streaming_service):
        self._lock: threading.Lock = threading.Lock()
        self._streaming: bool = False
        self._target = target
        self._streaming_service = streaming_service
        self._stream_thread: Optional[threading.Thread] = None

        self._service_callback_id = itertools.count()
        self._service_callbacks: dict = {}

    @property
    def is_streaming(self):
        with self._lock:
            return self._streaming

    def register_callback(
        self, service_name: str, call_back: Callable, *args, **kwargs
    ) -> str:
        with self._lock:
            service_name = service_name.lower()
            callback_id = f"{service_name}-{next(self._service_callback_id)}"
            callbacks_map = self._service_callbacks.get(service_name)
            if callbacks_map:
                callbacks_map.update({callback_id: partial(call_back, *args, **kwargs)})
            else:
                self._service_callbacks[service_name] = {
                    callback_id: partial(call_back, *args, **kwargs)
                }
            return callback_id

    def unregister_callback(self, callback_id: str):
        """Unregister the callback.

        Parameters
        ----------
        callback_id : str
            ID of the registered callback.
        """
        with self._lock:
            for callbacks_map in self._service_callbacks.values():
                if callback_id in callbacks_map:
                    del callbacks_map[callback_id]

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
