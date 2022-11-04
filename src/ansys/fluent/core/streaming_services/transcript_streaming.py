from ansys.fluent.core.services.transcript import TranscriptService
from ansys.fluent.core.streaming_services.streaming import StreamingService


class Transcript(StreamingService):
    """Encapsulates a Fluent Transcript streaming service."""

    def __init__(self, channel, metadata):
        super().__init__(
            target=Transcript._process_streaming,
            streaming_service=TranscriptService(channel, metadata),
        )

    def _process_streaming(self, started_evt):
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
                        for callback_map in self._service_callbacks.values():
                            if "keep_new_lines" in callback_map[-1].keys():
                                if callback_map[-1]["keep_new_lines"]:
                                    callback_map[0](transcript)
                                else:
                                    callback_map[0](transcript[0:-1])
                            else:
                                callback_map[0](transcript[0:-1])
                        transcript = ""
            except StopIteration:
                break
