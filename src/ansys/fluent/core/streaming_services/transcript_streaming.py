# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Provides a module for transcript streaming."""

import os
from pathlib import Path

from ansys.api.fluent.v0 import transcript_pb2 as TranscriptModule
from ansys.fluent.core.streaming_services.streaming import StreamingService


class AppendToFile:
    """Class representing append to file action."""

    def __init__(self, file_name: str):
        """__init__ method of AppendToFile class."""
        self.f = open(file_name, "a")

    def __call__(self, transcript):
        self.f.write(transcript)
        self.f.flush()

    def __del__(self):
        self.f.close()


class Transcript(StreamingService):
    """Encapsulates a Fluent Transcript streaming service."""

    def __init__(self, transcript_service):
        """__init__ method of Transcript class."""
        super().__init__(
            stream_begin_method="BeginStreaming",
            target=Transcript._process_streaming,
            streaming_service=transcript_service,
        )
        self.callback_ids = []
        self._writing_transcript_to_interpreter = False

    def start(
        self, file_name: str | None = None, write_to_stdout: bool = False
    ) -> None:
        """Start streaming of Fluent transcript.

         Parameters
        ----------
        file_name: str, optional
            File path to write the transcript stream.
        write_to_stdout: bool, optional
            Flag to print transcript on the screen or not
        """
        if file_name:
            if Path(file_name).exists():
                os.remove(file_name)
            append_to_file = AppendToFile(file_name)
            self.callback_ids.append(
                self.register_callback(append_to_file, keep_new_lines=True)
            )
            if write_to_stdout:
                self._write_to_stdout()
        else:
            self._write_to_stdout()
        super().start()

    def _write_to_stdout(self):
        """Write transcript to stdout."""
        if not self._writing_transcript_to_interpreter:
            self.callback_ids.append(self.register_callback(print))
            self._writing_transcript_to_interpreter = True

    def stop(self) -> None:
        """Stop streaming of Fluent transcript."""
        for callback_id in self.callback_ids:
            self.unregister_callback(callback_id)
        super().stop()

    def _process_streaming(self, id, stream_begin_method, started_evt, *args, **kwargs):
        """Performs processes on transcript depending on the callback functions."""
        request = TranscriptModule.TranscriptRequest(*args, **kwargs)
        responses = self._streaming_service.begin_streaming(
            request, started_evt, id=id, stream_begin_method=stream_begin_method
        )
        transcript = ""
        while True:
            try:
                response = next(responses)
                with self._lock:
                    self._streaming = True
                    transcript += response.transcript
                    if transcript and transcript[-1] == "\n":
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
