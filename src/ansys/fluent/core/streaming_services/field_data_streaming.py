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

"""Module for Field data streaming."""

from typing import Callable, Dict, List

from ansys.api.fluent.v0 import field_data_pb2 as FieldDataProtoModule
from ansys.fluent.core.services.field_data import ChunkParser
from ansys.fluent.core.streaming_services.streaming import StreamingService


class FieldDataStreaming(StreamingService):
    """Class wrapping the Field gRPC streaming service of Fluent.

    Parameters
    ----------
    session_id : str
        Session ID.
    service : FieldDataService
        FieldData streaming service.
    """

    def __init__(self, session_id: str, service):
        """Initialize FieldDataStreaming."""
        super().__init__(
            stream_begin_method="BeginFieldsStreaming",
            target=FieldDataStreaming._process_streaming,
            streaming_service=service,
        )
        self._session_id: str = session_id

    def _process_streaming(self, id, stream_begin_method, started_evt, *args, **kwargs):
        """Processes field data streaming."""
        request = FieldDataProtoModule.BeginFieldsStreamingRequest(*args, **kwargs)
        ChunkParser(self).extract_fields(
            self._streaming_service.begin_streaming(
                request, started_evt, id=id, stream_begin_method=stream_begin_method
            )
        )

    def callbacks(self) -> List[List[Callable | List | Dict]]:
        """Get list of callbacks along with arguments and keyword arguments."""
        return self._service_callbacks.values()
