import itertools
import threading
from typing import Callable, Optional

from ansys.fluent.core.services.transcript import TranscriptService


class Transcript:
    """Encapsulates a Fluent Transcript streaming service."""

    def __init__(self, channel, metadata):
        self._channel = channel
        self._metadata = metadata
        self._transcript_service = TranscriptService(self._channel, self._metadata)
        self._transcript_thread: Optional[threading.Thread] = None
        self._transcript_callbacks = {}
        self._transcript_callback_id = itertools.count()
        self._lock = threading.Lock()

    def add_transcript_callback(self, callback_fn: Callable, keep_new_lines=False):
        """Initiates a fluent transcript streaming depending on the
        callback_fn.

        For eg.: add_transcript_callback(print) prints the transcript on
        the interpreter screen.
        """
        with self._lock:
            callback_id = next(self._transcript_callback_id)
            self._transcript_callbacks[callback_id] = (
                callback_fn,
                keep_new_lines,
            )
            start_thread = len(self._transcript_callbacks) == 1
        if start_thread:
            self.start()
        return callback_id

    def remove_transcript_callback(self, callback_id):
        """Stops each transcript streaming based on the callback_id."""
        with self._lock:
            del self._transcript_callbacks[callback_id]
            stop_thread = len(self._transcript_callbacks) == 0
        if stop_thread:
            self.stop()

    def _process_transcript(self, started_evt):
        """Performs processes on transcript depending on the callback
        functions."""
        responses = self._transcript_service.begin_streaming(started_evt)
        transcript = ""
        while True:
            try:
                response = next(responses)
                with self._lock:
                    self._streaming = True
                    transcript += response.transcript
                    if transcript[-1] == "\n":
                        for (
                            callback_function,
                            keep_new_lines,
                        ) in self._transcript_callbacks.values():
                            if keep_new_lines:
                                callback_function(transcript)
                            else:
                                callback_function(transcript[0:-1])
                        transcript = ""
            except StopIteration:
                break

    @property
    def is_streaming(self):
        with self._lock:
            return self._streaming

    def start(self) -> None:
        """Start streaming of Fluent transcript."""
        with self._lock:
            if self._transcript_thread is None:
                started_evt = threading.Event()
                self._transcript_thread = threading.Thread(
                    target=Transcript._process_transcript, args=(self, started_evt)
                )
                self._transcript_thread.start()
                started_evt.wait()

    def stop(self) -> None:
        """Stop streaming of Fluent transcript."""
        self._transcript_service.end_streaming()
        self._transcript_thread.join()
        self._streaming = False
        self._transcript_thread = None
