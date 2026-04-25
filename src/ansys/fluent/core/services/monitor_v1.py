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

"""Wrapper over the monitor gRPC service of Fluent (v1 proto API).

All shared logic lives in monitor.py (v0). This module keeps only v1-specific
proto/stub/response-field differences.
"""

from google.protobuf.json_format import MessageToDict

from ansys.api.fluent.v1 import monitor_pb2 as MonitorModuleV1
from ansys.api.fluent.v1 import monitor_pb2_grpc as MonitorGrpcModuleV1
import ansys.fluent.core.services.monitor as _v0

# v1 MessageToDict produces camelCase keys for the renamed snake_case fields
# (x_label → xLabel, y_label → yLabel, unit_info → unitInfo). Callers of
# get_monitors_info() still expect the v0 legacy lowercase spellings, so
# this map translates them back.
_KEY_MAP_V1_TO_LEGACY = {
    "xLabel": "xlabel",
    "yLabel": "ylabel",
    "unitInfo": "unitinfo",
}


def _normalize_monitor_set_dict_keys(data: dict) -> dict:
    """Translate v1 camelCase dict keys back to v0 legacy names expected by callers.

    The v1 proto uses snake_case field names (``x_label``, ``y_label``,
    ``unit_info``), which ``MessageToDict`` serialises as camelCase
    (``xLabel``, ``yLabel``, ``unitInfo``).  All consumers of
    ``get_monitors_info()`` still expect the legacy lowercase spellings
    produced by v0's ``MessageToDict`` (``xlabel``, ``ylabel``,
    ``unitinfo``), so this normaliser translates them back so that higher
    layers remain version-agnostic.
    """
    if isinstance(data, dict):
        return {
            _KEY_MAP_V1_TO_LEGACY.get(k, k): _normalize_monitor_set_dict_keys(v)
            for k, v in data.items()
        }
    return data


class MonitorsService(_v0.MonitorsService):
    """Monitors gRPC service wrapper (v1 proto API).

    Inherits the interceptor setup and ``_create_stub`` hook from the v0
    base class.  Only the stub factory and the response-field access in
    ``get_monitors_info`` differ between protocol versions.
    """

    def _create_stub(self, intercept_channel):
        """Create the v1 Monitor gRPC stub."""
        return MonitorGrpcModuleV1.MonitorStub(intercept_channel)

    def get_monitors_info(self) -> dict:
        """Get monitors information (v1 proto).

        Overrides v0 to use the renamed ``monitor_sets`` response field
        (v0: ``monitorset``) and normalises the camelCase dict keys produced
        by ``MessageToDict`` back to the v0 legacy spellings so that all
        consumers remain version-agnostic.
        """
        monitors_info = {}
        request = MonitorModuleV1.GetMonitorsRequest()
        response = self._stub.GetMonitors(request, metadata=self._metadata)
        for monitor_set in response.monitor_sets:  # v1: monitor_sets (v0: monitorset)
            monitor_info = _normalize_monitor_set_dict_keys(MessageToDict(monitor_set))
            monitors_info[monitor_set.name] = monitor_info
        return monitors_info
