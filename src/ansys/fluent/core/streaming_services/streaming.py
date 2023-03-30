import itertools
import threading
from typing import Callable, Optional


class StreamingService:
    """Encapsulates a Fluent streaming service."""

    def __init__(self, target, streaming_service, stop_service=None):
        """__init__ method of StreamingService class."""
        self._lock: threading.RLock = threading.RLock()
        self._streaming: bool = False
        self._target = target
        self._streaming_service = streaming_service
        self._stream_thread: Optional[threading.Thread] = None
        self._stop_service = stop_service
        self._service_callback_id = itertools.count()
        self._service_callbacks: dict = {}

    @property
    def is_streaming(self):
        """Checks whether it is streaming."""
        with self._lock:
            return self._streaming

    def register_callback(self, call_back: Callable, *args, **kwargs) -> str:
        """Register the callback.

        Parameters
        ----------
        call_back : Callable
            Callback to register.

        Returns
        -------
        str
            Registered callback ID.
        """
        with self._lock:
            callback_id = f"{next(self._service_callback_id)}"
            self._service_callbacks[callback_id] = [call_back, args, kwargs]
            return callback_id

    def unregister_callback(self, callback_id: str):
        """Unregister the callback.

        Parameters
        ----------
        callback_id : str
            ID of the registered callback.
        """
        with self._lock:
            if callback_id in self._service_callbacks:
                del self._service_callbacks[callback_id]

    def start(self, *args, **kwargs) -> None:
        """Start streaming of Fluent transcript."""
        with self._lock:
            if not self.is_streaming:
                self._prepare()
                started_evt = threading.Event()
                self._stream_thread = threading.Thread(
                    target=self._target, args=(self, started_evt, *args), kwargs=kwargs
                )
                self._stream_thread.start()
                started_evt.wait()

    def stop(self) -> None:
        """Stop streaming of Fluent transcript."""
        if self.is_streaming:
            if self._stop_service is None:
                self._streaming_service.end_streaming()
            else:
                self._stop_service()
            self._stream_thread.join()
            self._streaming = False
            self._stream_thread = None

    def refresh(self, session_id, event_info) -> None:
        """Refresh stream.

        Parameters
        ----------
        session_id : str
            Name of the monitor set.
        event_info : object
            Event info object.

        Returns
        -------
        None
        """
        with self._lock_refresh:
            self.stop()
            self.start()

    def _prepare(self):
        pass  # Currently only used by monitor services.
