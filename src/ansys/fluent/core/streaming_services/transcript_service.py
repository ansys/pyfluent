import itertools
from typing import Callable

from ansys.fluent.core.services.transcript import TranscriptService
from ansys.fluent.core.streaming_services.streaming_services import StreamingService


class Transcript(StreamingService):
    """Encapsulates a Fluent Transcript streaming service."""

    def __init__(self, channel, metadata):
        super().__init__(
            target=Transcript._process_transcript,
            streaming_service=TranscriptService(channel, metadata),
        )
        self._transcript_callbacks = {}
        self._transcript_callback_id = itertools.count()

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
        responses = self._streaming_service.begin_streaming(started_evt)
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
