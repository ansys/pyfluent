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

"""Wrapper over the health check gRPC service of Fluent (v1 proto API).

All shared logic lives in health_check.py (grpc-health API). This module keeps
only v1-specific proto construction.
"""

from ansys.api.fluent.v1 import health_pb2 as HealthCheckModule
from ansys.api.fluent.v1 import health_pb2_grpc as HealthCheckGrpcModule
from ansys.fluent.core.services.health_check import HealthCheckService as _HealthCheckV0


class HealthCheckService(_HealthCheckV0):
    """Class wrapping the health check gRPC service of Fluent (v1 proto API)."""

    def _create_stub(self, intercept_channel):
        """Create the v1 gRPC stub."""
        return HealthCheckGrpcModule.HealthStub(intercept_channel)

    def _create_health_check_request(self):
        """Create a v1 health-check request."""
        return HealthCheckModule.HealthCheckRequest()
