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

"""Wrapper to settings gRPC service of Fluent (v1 proto API).

All shared logic lives in settings.py (v0). This module keeps only
v1-specific proto and stub bindings required for compatibility.
"""

from ansys.api.fluent.v1 import settings_pb2 as SettingsModule
from ansys.api.fluent.v1 import settings_pb2_grpc as SettingsGrpcModule
from ansys.fluent.core.services.settings import (
    _SettingsServiceImpl as _SettingsServiceImplV0,
)
from ansys.fluent.core.services.settings import SettingsService as _SettingsServiceV0


class _SettingsServiceImpl(_SettingsServiceImplV0):
    """Internal settings gRPC impl using v1 proto API."""

    def _create_stub(self, intercept_channel):
        """Create the v1 gRPC stub."""
        return SettingsGrpcModule.SettingsServiceStub(intercept_channel)


class SettingsService(_SettingsServiceV0):
    """Service for accessing and modifying Fluent settings (v1 proto API)."""

    _list_field: str = "lsts"
    _settings_module = SettingsModule

    def _create_service_impl(self, channel, metadata, fluent_error_state):
        """Create the v1 settings service implementation."""
        return _SettingsServiceImpl(channel, metadata, fluent_error_state)
