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
from ansys.fluent.core.services.settings import (
    _get_request_instance_for_path,
)
from ansys.fluent.core.services.settings import (
    _trace,
)
from ansys.fluent.core.services.settings import SettingsService as _SettingsServiceV0


class _SettingsServiceImpl(_SettingsServiceImplV0):
    """Internal settings gRPC impl using v1 proto API."""

    def _create_stub(self, intercept_channel):
        """Create the v1 gRPC stub."""
        return SettingsGrpcModule.SettingsStub(intercept_channel)

    def get_var(self, request):
        """Get a variable (v1: GetState)."""
        return self._stub.GetState(request, metadata=self._metadata)

    def set_var(self, request):
        """Set a variable (v1: SetState)."""
        return self._stub.SetState(request, metadata=self._metadata)

    def create(self, request):
        """Create an object (v1: CreateObject)."""
        return self._stub.CreateObject(request, metadata=self._metadata)

    def delete(self, request):
        """Delete an object (v1: DeleteObject)."""
        return self._stub.DeleteObject(request, metadata=self._metadata)

    def get_static_info(self, request):
        """Get static info (v1: GetSchema)."""
        return self._stub.GetSchema(request, metadata=self._metadata)

    def is_wildcard(self, request):
        """IsWildcard RPC of Settings service (v1)."""
        return self._stub.IsWildcard(request, metadata=self._metadata)


class SettingsService(_SettingsServiceV0):
    """Service for accessing and modifying Fluent settings (v1 proto API)."""

    _list_field: str = "lsts"
    _settings_module = SettingsModule

    def __init__(self, channel, metadata, scheme_eval, fluent_error_state) -> None:
        """__init__ method of SettingsService class."""
        super().__init__(channel, metadata, None, scheme_eval, fluent_error_state)

    def _create_service_impl(self, channel, metadata, fluent_error_state):
        """Create the v1 settings service implementation."""
        return _SettingsServiceImpl(channel, metadata, fluent_error_state)

    @_trace
    def set_var(self, path: str, value) -> None:
        """Set the value for the given path (v1: SetState)."""
        request = _get_request_instance_for_path(SettingsModule.SetStateRequest, path)
        self._set_state_from_value(request.value, value)
        self._service_impl.set_var(request)

    @_trace
    def get_var(self, path: str):
        """Get the value for the given path (v1: GetState)."""
        request = _get_request_instance_for_path(SettingsModule.GetStateRequest, path)
        response = self._service_impl.get_var(request)
        return self._get_state_from_value(response.value)

    @_trace
    def create(self, path: str, name: str) -> None:
        """Create a named object child for the given path (v1: CreateObject)."""
        request = _get_request_instance_for_path(
            SettingsModule.CreateObjectRequest, path
        )
        request.name = name
        self._service_impl.create(request)

    @_trace
    def delete(self, path: str, name: str) -> None:
        """Delete the object with the given name at the given path (v1: DeleteObject)."""
        request = _get_request_instance_for_path(
            SettingsModule.DeleteObjectRequest, path
        )
        request.name = name
        self._service_impl.delete(request)

    @_trace
    def get_static_info(self) -> dict:
        """Get static-info for settings (v1: GetSchema).

        Raises
        ------
        RuntimeError
            If type is empty.
        """
        request = SettingsModule.GetSchemaRequest()
        request.root = "fluent"
        request.optional_attrs.extend(["allowed-values", "has-migration-adapter?"])
        response = self._service_impl.get_static_info(request)
        if not response.info.type:
            raise RuntimeError
        return self._extract_static_info(response.info)

    @_trace
    def is_wildcard(self, input: str | None = None) -> bool:
        """Check whether a name contains a wildcard pattern (v1: Settings.IsWildcard)."""
        request = SettingsModule.IsWildcardRequest()
        if input is not None:
            request.input = input
        response = self._service_impl.is_wildcard(request)
        return response.is_wildcard

    @_trace
    def has_wildcard(self, name: str) -> bool:
        """Check whether a name has a wildcard pattern (v1: uses Settings.IsWildcard directly)."""
        return self.is_wildcard(name)
