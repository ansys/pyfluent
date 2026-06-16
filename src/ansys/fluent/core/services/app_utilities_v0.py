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

"""gRPC service stub wrappers for the AppUtilities service (v0 proto API).

Business logic lives in :mod:`ansys.fluent.core.application_runtime`.
"""

import grpc

from ansys.api.fluent.v0 import app_utilities_pb2 as AppUtilitiesProtoModule
from ansys.api.fluent.v0 import app_utilities_pb2_grpc as AppUtilitiesGrpcModule
from ansys.fluent.core.services._protocols import ServiceProtocol
from ansys.fluent.core.services.interceptors import (
    BatchInterceptor,
    ErrorStateInterceptor,
    GrpcErrorInterceptor,
    TracingInterceptor,
)

__all__ = ("AppUtilitiesService",)


class AppUtilitiesService(ServiceProtocol):
    """AppUtilities gRPC service wrapper (v0 proto API)."""

    def __init__(  # pyright: ignore[reportMissingSuperCall]
        self, channel: grpc.Channel, metadata: list[tuple[str, str]], fluent_error_state
    ):
        """Initialize AppUtilitiesService."""
        intercept_channel = grpc.intercept_channel(
            channel,
            GrpcErrorInterceptor(),
            ErrorStateInterceptor(fluent_error_state),
            TracingInterceptor(),
            BatchInterceptor(),
        )
        self._stub = self._create_stub(intercept_channel)
        self._metadata = metadata

    def _create_stub(self, intercept_channel):
        """Create the gRPC stub. Override in subclasses to use a different proto version."""
        return AppUtilitiesGrpcModule.AppUtilitiesStub(intercept_channel)

    def get_product_version(
        self, request: AppUtilitiesProtoModule.GetProductVersionRequest
    ) -> AppUtilitiesProtoModule.GetProductVersionResponse:
        """GetProductVersion RPC."""
        return self._stub.GetProductVersion(request, metadata=self._metadata)

    def get_build_info(
        self, request: AppUtilitiesProtoModule.GetBuildInfoRequest
    ) -> AppUtilitiesProtoModule.GetBuildInfoResponse:
        """GetBuildInfo RPC."""
        return self._stub.GetBuildInfo(request, metadata=self._metadata)

    def get_controller_process_info(
        self, request: AppUtilitiesProtoModule.GetControllerProcessInfoRequest
    ) -> AppUtilitiesProtoModule.GetControllerProcessInfoResponse:
        """GetControllerProcessInfo RPC."""
        return self._stub.GetControllerProcessInfo(request, metadata=self._metadata)

    def get_solver_process_info(
        self, request: AppUtilitiesProtoModule.GetSolverProcessInfoRequest
    ) -> AppUtilitiesProtoModule.GetSolverProcessInfoResponse:
        """GetSolverProcessInfo RPC."""
        return self._stub.GetSolverProcessInfo(request, metadata=self._metadata)

    def get_app_mode(
        self, request: AppUtilitiesProtoModule.GetAppModeRequest
    ) -> AppUtilitiesProtoModule.GetAppModeResponse:
        """GetAppMode RPC."""
        return self._stub.GetAppMode(request, metadata=self._metadata)

    def start_python_journal(
        self, request: AppUtilitiesProtoModule.StartPythonJournalRequest
    ) -> AppUtilitiesProtoModule.StartPythonJournalResponse:
        """StartPythonJournal RPC."""
        return self._stub.StartPythonJournal(request, metadata=self._metadata)

    def stop_python_journal(
        self, request: AppUtilitiesProtoModule.StopPythonJournalRequest
    ) -> AppUtilitiesProtoModule.StopPythonJournalResponse:
        """StopPythonJournal RPC."""
        return self._stub.StopPythonJournal(request, metadata=self._metadata)

    def is_beta_enabled(
        self, request: AppUtilitiesProtoModule.IsBetaEnabledRequest
    ) -> AppUtilitiesProtoModule.IsBetaEnabledResponse:
        """IsBetaEnabled RPC."""
        return self._stub.IsBetaEnabled(request, metadata=self._metadata)

    def enable_beta(
        self, request: AppUtilitiesProtoModule.EnableBetaRequest
    ) -> AppUtilitiesProtoModule.EnableBetaResponse:
        """EnableBeta RPC."""
        return self._stub.EnableBeta(request, metadata=self._metadata)

    def is_wildcard(
        self, request: AppUtilitiesProtoModule.IsWildcardRequest
    ) -> AppUtilitiesProtoModule.IsWildcardResponse:
        """IsWildcard RPC."""
        return self._stub.IsWildcard(request, metadata=self._metadata)

    def is_solution_data_available(
        self, request: AppUtilitiesProtoModule.IsSolutionDataAvailableRequest
    ) -> AppUtilitiesProtoModule.IsSolutionDataAvailableResponse:
        """IsSolutionDataAvailable RPC."""
        return self._stub.IsSolutionDataAvailable(request, metadata=self._metadata)

    def register_pause_on_solution_events(
        self, request: AppUtilitiesProtoModule.RegisterPauseOnSolutionEventsRequest
    ) -> AppUtilitiesProtoModule.RegisterPauseOnSolutionEventsResponse:
        """RegisterPauseOnSolutionEvents RPC."""
        return self._stub.RegisterPauseOnSolutionEvents(
            request, metadata=self._metadata
        )

    def resume_on_solution_event(
        self, request: AppUtilitiesProtoModule.ResumeOnSolutionEventRequest
    ) -> AppUtilitiesProtoModule.ResumeOnSolutionEventResponse:
        """ResumeOnSolutionEvent RPC."""
        return self._stub.ResumeOnSolutionEvent(request, metadata=self._metadata)

    def unregister_pause_on_solution_events(
        self, request: AppUtilitiesProtoModule.UnregisterPauseOnSolutionEventsRequest
    ) -> AppUtilitiesProtoModule.UnregisterPauseOnSolutionEventsResponse:
        """UnregisterPauseOnSolutionEvents RPC."""
        return self._stub.UnregisterPauseOnSolutionEvents(
            request, metadata=self._metadata
        )

    def exit(
        self, request: AppUtilitiesProtoModule.ExitRequest
    ) -> AppUtilitiesProtoModule.ExitResponse:
        """Exit RPC."""
        return self._stub.Exit(request, metadata=self._metadata)

    def set_working_directory(
        self, request: AppUtilitiesProtoModule.SetWorkingDirectoryRequest
    ) -> AppUtilitiesProtoModule.SetWorkingDirectoryResponse:
        """SetWorkingDirectory RPC."""
        return self._stub.SetWorkingDirectory(request, metadata=self._metadata)
