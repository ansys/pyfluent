# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
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

"""Wrapper over the transcript gRPC service of Fluent (v1 proto API).

All shared logic lives in transcript.py (v0). This module keeps only
v1-specific stub binding required for compatibility.
"""

import grpc

from ansys.api.fluent.v1 import transcript_pb2_grpc as TranscriptGrpcModule
from ansys.fluent.core.services.transcript import (
    TranscriptService as _TranscriptServiceV0,
)


class TranscriptService(_TranscriptServiceV0):
    """Class wrapping the transcript gRPC service of Fluent (v1 proto API)."""

    def _create_stub(self, channel: grpc.Channel):
        """Create the v1 gRPC stub."""
        return TranscriptGrpcModule.TranscriptStub(channel)
