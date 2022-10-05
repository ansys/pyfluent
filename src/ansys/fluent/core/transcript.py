import itertools
import threading
from typing import Callable, Optional

from ansys.fluent.core.services.transcript import TranscriptService


class Transcript:
    """Encapsulates a Fluent Transcript streaming service."""

    def __init__(self, channel, metadata):
        self._channel = channel
        self._metadata = metadata
        self.transcript_service = TranscriptService(self._channel, self._metadata)
        self._transcript_thread: Optional[threading.Thread] = None
        self._transcript_callbacks = {}
        self._transcript_callback_id = itertools.count()
        self.lock = threading.Lock()

    def add_transcript_callback(self, callback_fn: Callable, keep_new_lines=False):
        """Initiates a fluent transcript streaming depending on the
        callback_fn.

        For eg.: add_transcript_callback(print) prints the transcript on
        the interpreter screen.
        """
        with self.lock:
            callback_id = next(self._transcript_callback_id)
            self._transcript_callbacks[callback_id] = (
                callback_fn,
                keep_new_lines,
            )
            start_thread = len(self._transcript_callbacks) == 1
        if start_thread:
            self._transcript_thread = threading.Thread(
                target=self._process_transcript,
                args=(self.transcript_service,),
            )
            self._transcript_thread.start()
        return callback_id

    def remove_transcript_callback(self, callback_id):
        """Stops each transcript streaming based on the callback_id."""
        with self.lock:
            del self._transcript_callbacks[callback_id]
            stop_thread = len(self._transcript_callbacks) == 0
        if stop_thread:
            self.transcript_service.end_streaming()
            self._transcript_thread.join()

    def _process_transcript(self, transcript_service):
        """Performs processes on transcript depending on the callback
        functions."""
        responses = transcript_service.begin_streaming()
        transcript = ""
        while True:
            try:
                response = next(responses)
                transcript += response.transcript
                if transcript[-1] == "\n":
                    with self.lock:
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
