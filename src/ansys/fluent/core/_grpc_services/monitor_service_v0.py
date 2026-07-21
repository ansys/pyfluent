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

"""Wrapper over the monitor gRPC service of Fluent (v0 proto API)."""

from google.protobuf.json_format import MessageToDict
import grpc

from ansys.api.fluent.v0 import monitor_pb2, monitor_pb2_grpc
from ansys.fluent.core._grpc_services.streaming_service import StreamingService
from ansys.fluent.core.services._protocols import ServiceProtocol
from ansys.fluent.core.services.interceptors import (
    BatchInterceptor,
    ErrorStateInterceptor,
    TracingInterceptor,
)


class MonitorService(
    StreamingService, ServiceProtocol
):  # pyright: ignore[reportUnsafeMultipleInheritance]
    """Class wrapping the monitor gRPC service of Fluent."""

    def __init__(self, channel: grpc.Channel, metadata, fluent_error_state):
        """__init__ method of MonitorService class."""
        intercept_channel = grpc.intercept_channel(
            channel,
            ErrorStateInterceptor(fluent_error_state),
            TracingInterceptor(),
            BatchInterceptor(),
        )
        self._stub = monitor_pb2_grpc.MonitorStub(intercept_channel)
        self._metadata = metadata
        super().__init__(
            stub=self._stub,
            metadata=self._metadata,
        )

    def get_monitors_info(self) -> dict:
        """Get monitors information.

        Parameters
        ----------
        None

        Returns
        -------
        dict
            Dictionary containing the monitors information.
        """
        monitors_info = {}
        request = monitor_pb2.GetMonitorsRequest()
        response = self._stub.GetMonitors(request, metadata=self._metadata)
        for monitor_set in response.monitorset:
            monitor_info = MessageToDict(monitor_set)
            monitors_info[monitor_set.name] = monitor_info
        return monitors_info

    def _process_streaming(self, id, stream_begin_method, started_evt, *args, **kwargs):
        """Processes events streaming."""
        request = monitor_pb2.StreamingRequest(*args, **kwargs)
        return self.begin_streaming(
            request, started_evt, id=id, stream_begin_method=stream_begin_method
        )

    def parse_streaming_response(self, response):
        """Parse v0 streaming response into canonical (x_index, y_data) form."""
        x_axis_index = response.xaxisdata.xaxisindex
        y_data = {y.name: y.value for y in response.yaxisvalues}
        return x_axis_index, y_data
