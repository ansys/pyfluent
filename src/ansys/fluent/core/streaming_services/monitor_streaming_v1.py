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

"""Module for monitors management (v1 proto API).

All shared DataFrame/callback/refresh logic lives in monitor_streaming.py (v0).
This module keeps only the v1-specific proto field name differences in the
streaming response:

- v0: ``response.xaxisdata.xaxisindex``, ``response.yaxisvalues``
- v1: ``response.x_axis_data.x_axis_index``, ``response.y_axis_values``
"""

from ansys.api.fluent.v1 import monitor_pb2 as MonitorModuleV1
import ansys.fluent.core.streaming_services.monitor_streaming as _v0  # v0 base: shared logic is reused; only v1-specific proto field name differences are overridden below


class MonitorsManager(_v0.MonitorsManager):
    """Manages Fluent monitors (v1 proto API).

    Inherits all DataFrame/callback/refresh logic from the v0 base class.
    Only the proto field names in the streaming response differ between
    protocol versions:

    - v0: ``response.xaxisdata.xaxisindex``, ``response.yaxisvalues``
    - v1: ``response.x_axis_data.x_axis_index``, ``response.y_axis_values``
    """

    def __init__(self, session_id: str, service):
        """Initialize MonitorsManager (v1)."""
        super().__init__(session_id, service)
        # Replace the v0 _process_streaming target set by the base __init__
        # with this class's v1 override so the streaming thread uses v1 field names.
        self._target = MonitorsManager._process_streaming

    def _process_streaming(self, id, stream_begin_method, started_evt, *args, **kwargs):
        """Begin monitors streaming (v1 proto field names).

        Overrides v0 to use the renamed streaming-response fields:
        - ``x_axis_data.x_axis_index`` instead of ``xaxisdata.xaxisindex``
        - ``y_axis_values`` instead of ``yaxisvalues``
        """
        request = MonitorModuleV1.StreamingRequest(*args, **kwargs)
        responses = self._streaming_service.begin_streaming(
            request, started_evt, id=id, stream_begin_method=stream_begin_method
        )

        while True:
            try:
                data_received = {}
                response = next(responses)
                # v1 renames: x_axis_data / x_axis_index (v0: xaxisdata / xaxisindex)
                x_axis_index = response.x_axis_data.x_axis_index
                data_received["xvalues"] = x_axis_index
                # v1 renames: y_axis_values (v0: yaxisvalues)
                for y_axis_value in response.y_axis_values:
                    data_received[y_axis_value.name] = y_axis_value.value
                with self._lock:
                    self._streaming = True
                    self._populate_dataframes(data_received, *args, **kwargs)

            except StopIteration:
                break
