import os
from pathlib import Path

from ansys.fluent.core.services.transcript import TranscriptService
from ansys.fluent.core.streaming_services.streaming import StreamingService


class AppendToFile:
    def __init__(self, file_path: str):
        self.f = open(file_path, "a")

    def __call__(self, transcript):
        self.f.write(transcript)

    def __del__(self):
        self.f.close()


class Transcript(StreamingService):
    """Encapsulates a Fluent Transcript streaming service."""

    _writing_transcript_to_interpreter = False

    def __init__(self, channel, metadata):
        super().__init__(
            target=Transcript._process_streaming,
            streaming_service=TranscriptService(channel, metadata),
        )
        self.callback_ids = []

    def start(self, file_path: str = None, write_to_interpreter: bool = True) -> None:
        """Start streaming of Fluent transcript.

         Parameters
        ----------
        file_path: str, optional
            File path to write the transcript stream.
        write_to_interpreter: bool, optional
            Flag to print transcript on the screen or not
        """
        if not Transcript._writing_transcript_to_interpreter:
            if write_to_interpreter:
                self.callback_ids.append(self.register_callback(print))
                Transcript._writing_transcript_to_interpreter = True
        if file_path:
            if Path(file_path).exists():
                os.remove(file_path)
            append_to_file = AppendToFile(file_path)
            self.callback_ids.append(
                self.register_callback(append_to_file, keep_new_lines=True)
            )
        super().start()

    def stop(self) -> None:
        """Stop streaming of Fluent transcript."""
        for callback_id in self.callback_ids:
            self.unregister_callback(callback_id)
        super().stop()

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
