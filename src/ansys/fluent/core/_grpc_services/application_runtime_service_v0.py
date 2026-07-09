# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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

"""Wrapper over the application runtime gRPC service of Fluent (v0 proto API)."""

import os

import grpc

from ansys.api.fluent.v0 import app_utilities_pb2, app_utilities_pb2_grpc
from ansys.fluent.core._types import PathType
from ansys.fluent.core.services._protocols import ServiceProtocol
from ansys.fluent.core.services.interceptors import (
    BatchInterceptor,
    ErrorStateInterceptor,
    GrpcErrorInterceptor,
    TracingInterceptor,
)
from ansys.fluent.core.streaming_services.events_streaming import SolverEvent


class ApplicationRuntimeService(ServiceProtocol):
    """AppUtilities gRPC service wrapper (v0 proto API)."""

    def __init__(  # pyright: ignore[reportMissingSuperCall]
        self, channel: grpc.Channel, metadata: list[tuple[str, str]], fluent_error_state
    ):
        """Initialize ApplicationRuntimeService."""
        intercept_channel = grpc.intercept_channel(
            channel,
            GrpcErrorInterceptor(),
            ErrorStateInterceptor(fluent_error_state),
            TracingInterceptor(),
            BatchInterceptor(),
        )
        self._stub = app_utilities_pb2_grpc.AppUtilitiesStub(intercept_channel)
        self._metadata = metadata

    def get_product_version(self) -> str:
        """GetProductVersion RPC."""
        request = app_utilities_pb2.GetProductVersionRequest()
        response = self._stub.GetProductVersion(request, metadata=self._metadata)
        return f"{response.major}.{response.minor}.{response.patch}"

    def get_build_info(self) -> tuple[str, str, str, str]:
        """GetBuildInfo RPC."""
        request = app_utilities_pb2.GetBuildInfoRequest()
        response = self._stub.GetBuildInfo(request, metadata=self._metadata)
        return (
            response.build_time,
            response.build_id,
            response.vcs_revision,
            response.vcs_branch,
        )

    def get_controller_process_info(self) -> tuple[int, str, str]:
        """GetControllerProcessInfo RPC."""
        request = app_utilities_pb2.GetControllerProcessInfoRequest()
        response = self._stub.GetControllerProcessInfo(request, metadata=self._metadata)
        return (
            response.process_id,
            response.hostname,
            response.working_directory,
        )

    def get_solver_process_info(self) -> tuple[int, str, str]:
        """GetSolverProcessInfo RPC."""
        request = app_utilities_pb2.GetSolverProcessInfoRequest()
        response = self._stub.GetSolverProcessInfo(request, metadata=self._metadata)
        return (
            response.process_id,
            response.hostname,
            response.working_directory,
        )

    def get_app_mode(self) -> str:
        """GetAppMode RPC.

        Raises
        ------
        ValueError
            If app mode is unknown.
        """
        request = app_utilities_pb2.GetAppModeRequest()
        response = self._stub.GetAppMode(request, metadata=self._metadata)
        match response.app_mode:
            case app_utilities_pb2.APP_MODE_UNKNOWN:
                raise ValueError("Unknown app mode.")
            case app_utilities_pb2.APP_MODE_MESHING:
                return "meshing"
            case app_utilities_pb2.APP_MODE_SOLVER:
                return "solver"
            case app_utilities_pb2.APP_MODE_SOLVER_ICING:
                return "solver_icing"
            case app_utilities_pb2.APP_MODE_SOLVER_AERO:
                return "solver_aero"

    def start_python_journal(self, journal_name: str | None = None) -> int:
        """StartPythonJournal RPC."""
        request = app_utilities_pb2.StartPythonJournalRequest()
        if journal_name:
            request.journal_name = journal_name
        response = self._stub.StartPythonJournal(request, metadata=self._metadata)
        return response.journal_id

    def stop_python_journal(self, journal_id: str | None = None) -> str:
        """StopPythonJournal RPC."""
        request = app_utilities_pb2.StopPythonJournalRequest()
        if journal_id:
            request.journal_id = journal_id
        response = self._stub.StopPythonJournal(request, metadata=self._metadata)
        return response.journal_str

    def is_beta_enabled(self) -> bool:
        """IsBetaEnabled RPC."""
        request = app_utilities_pb2.IsBetaEnabledRequest()
        response = self._stub.IsBetaEnabled(request, metadata=self._metadata)
        return response.is_beta_enabled

    def enable_beta(self) -> None:
        """EnableBeta RPC."""
        request = app_utilities_pb2.EnableBetaRequest()
        self._stub.EnableBeta(request, metadata=self._metadata)

    def exit(self) -> None:
        """Exit RPC."""
        request = app_utilities_pb2.ExitRequest()
        self._stub.Exit(request, metadata=self._metadata)

    def set_working_directory(self, path: PathType) -> None:
        """SetWorkingDirectory RPC."""
        request = app_utilities_pb2.SetWorkingDirectoryRequest()
        request.path = os.fspath(path)
        self._stub.SetWorkingDirectory(request, metadata=self._metadata)

    def is_wildcard(self, input: str | None = None) -> bool:
        """IsWildcard RPC."""
        request = app_utilities_pb2.IsWildcardRequest()
        request.input = input
        response = self._stub.IsWildcard(request, metadata=self._metadata)
        return response.is_wildcard

    def is_solution_data_available(self) -> bool:
        """IsSolutionDataAvailable RPC."""
        request = app_utilities_pb2.IsSolutionDataAvailableRequest()
        response = self._stub.IsSolutionDataAvailable(request, metadata=self._metadata)
        return response.is_solution_data_available

    def register_pause_on_solution_events(self, solution_event: SolverEvent) -> int:
        """RegisterPauseOnSolutionEvents RPC."""
        request = app_utilities_pb2.RegisterPauseOnSolutionEventsRequest()
        request.solution_event = app_utilities_pb2.SOLUTION_EVENT_UNKNOWN
        match solution_event:
            case SolverEvent.ITERATION_ENDED:
                request.solution_event = app_utilities_pb2.SOLUTION_EVENT_ITERATION
            case SolverEvent.TIMESTEP_ENDED:
                request.solution_event = app_utilities_pb2.SOLUTION_EVENT_TIME_STEP
        response = self._stub.RegisterPauseOnSolutionEvents(
            request, metadata=self._metadata
        )
        return response.registration_id

    def resume_on_solution_event(self, registration_id: int) -> None:
        """ResumeOnSolutionEvent RPC."""
        request = app_utilities_pb2.ResumeOnSolutionEventRequest()
        request.registration_id = registration_id
        self._stub.ResumeOnSolutionEvent(request, metadata=self._metadata)

    def unregister_pause_on_solution_events(self, registration_id: int) -> None:
        """UnregisterPauseOnSolutionEvents RPC."""
        request = app_utilities_pb2.UnregisterPauseOnSolutionEventsRequest()
        request.registration_id = registration_id
        self._stub.UnregisterPauseOnSolutionEvents(request, metadata=self._metadata)
