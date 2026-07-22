# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
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

"""Wrapper over the transcript gRPC service of Fluent (v0 proto API)."""

import grpc

from ansys.api.fluent.v0 import transcript_pb2, transcript_pb2_grpc
from ansys.fluent.core._grpc_services.streaming_service import StreamingService
from ansys.fluent.core.services._protocols import ServiceProtocol


class TranscriptService(
    StreamingService, ServiceProtocol
):  # pyright: ignore[reportUnsafeMultipleInheritance]
    """Class wrapping the transcript gRPC service of Fluent."""

    def __init__(
        self,
        channel: grpc.Channel,
        metadata: list[tuple[str, str]],
    ) -> None:
        """__init__ method of TranscriptService class."""
        super().__init__(
            stub=transcript_pb2_grpc.TranscriptStub(channel),
            metadata=metadata,
        )

    def _process_streaming(self, id, stream_begin_method, started_evt, *args, **kwargs):
        """Processes events streaming."""
        request = transcript_pb2.TranscriptRequest(*args, **kwargs)
        return self.begin_streaming(
            request, started_evt, id=id, stream_begin_method=stream_begin_method
        )
