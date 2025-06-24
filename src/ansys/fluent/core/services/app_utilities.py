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

"""Wrappers over AppUtilities gRPC service of Fluent."""

from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple

import grpc

from ansys.api.fluent.v0 import app_utilities_pb2 as AppUtilitiesProtoModule
from ansys.api.fluent.v0 import app_utilities_pb2_grpc as AppUtilitiesGrpcModule
from ansys.fluent.core.services.interceptors import (
    BatchInterceptor,
    ErrorStateInterceptor,
    GrpcErrorInterceptor,
    TracingInterceptor,
)
from ansys.fluent.core.streaming_services.events_streaming import SolverEvent


class AppUtilitiesService:
    """AppUtilities Service."""

    def __init__(
        self, channel: grpc.Channel, metadata: List[Tuple[str, str]], fluent_error_state
    ):
        """__init__ method of AppUtilities class."""
        intercept_channel = grpc.intercept_channel(
            channel,
            GrpcErrorInterceptor(),
            ErrorStateInterceptor(fluent_error_state),
            TracingInterceptor(),
            BatchInterceptor(),
        )
        self._stub = AppUtilitiesGrpcModule.AppUtilitiesStub(intercept_channel)
        self._metadata = metadata

    def get_product_version(
        self, request: AppUtilitiesProtoModule.GetProductVersionRequest
    ) -> AppUtilitiesProtoModule.GetProductVersionResponse:
        """Get product version RPC of AppUtilities service."""
        return self._stub.GetProductVersion(request, metadata=self._metadata)

    def get_build_info(
        self, request: AppUtilitiesProtoModule.GetBuildInfoRequest
    ) -> AppUtilitiesProtoModule.GetBuildInfoResponse:
        """Get build info RPC of AppUtilities service."""
        return self._stub.GetBuildInfo(request, metadata=self._metadata)

    def get_controller_process_info(
        self, request: AppUtilitiesProtoModule.GetControllerProcessInfoRequest
    ) -> AppUtilitiesProtoModule.GetControllerProcessInfoResponse:
        """Get controller process info RPC of AppUtilities service."""
        return self._stub.GetControllerProcessInfo(request, metadata=self._metadata)

    def get_solver_process_info(
        self, request: AppUtilitiesProtoModule.GetSolverProcessInfoRequest
    ) -> AppUtilitiesProtoModule.GetSolverProcessInfoResponse:
        """Get solver process info RPC of AppUtilities service."""
        return self._stub.GetSolverProcessInfo(request, metadata=self._metadata)

    def get_app_mode(
        self, request: AppUtilitiesProtoModule.GetAppModeRequest
    ) -> AppUtilitiesProtoModule.GetAppModeResponse:
        """Get app mode RPC of AppUtilities service."""
        return self._stub.GetAppMode(request, metadata=self._metadata)

    def start_python_journal(
        self, request: AppUtilitiesProtoModule.StartPythonJournalRequest
    ) -> AppUtilitiesProtoModule.StartPythonJournalResponse:
        """Start python journal RPC of AppUtilities service."""
        return self._stub.StartPythonJournal(request, metadata=self._metadata)

    def stop_python_journal(
        self, request: AppUtilitiesProtoModule.StopPythonJournalRequest
    ) -> AppUtilitiesProtoModule.StopPythonJournalResponse:
        """Stop python journal RPC of AppUtilities service."""
        return self._stub.StopPythonJournal(request, metadata=self._metadata)

    def is_beta_enabled(
        self, request: AppUtilitiesProtoModule.IsBetaEnabledRequest
    ) -> AppUtilitiesProtoModule.IsBetaEnabledResponse:
        """Is beta enabled RPC of AppUtilities service."""
        return self._stub.IsBetaEnabled(request, metadata=self._metadata)

    def enable_beta(
        self, request: AppUtilitiesProtoModule.EnableBetaRequest
    ) -> AppUtilitiesProtoModule.EnableBetaResponse:
        """Is beta enabled RPC of AppUtilities service."""
        return self._stub.EnableBeta(request, metadata=self._metadata)

    def is_wildcard(
        self, request: AppUtilitiesProtoModule.IsWildcardRequest
    ) -> AppUtilitiesProtoModule.IsWildcardResponse:
        """Is wildcard RPC of AppUtilities service."""
        return self._stub.IsWildcard(request, metadata=self._metadata)

    def is_solution_data_available(
        self, request: AppUtilitiesProtoModule.IsSolutionDataAvailableRequest
    ) -> AppUtilitiesProtoModule.IsSolutionDataAvailableResponse:
        """Is solution data available RPC of AppUtilities service."""
        return self._stub.IsSolutionDataAvailable(request, metadata=self._metadata)

    def register_pause_on_solution_events(
        self, request: AppUtilitiesProtoModule.RegisterPauseOnSolutionEventsRequest
    ) -> AppUtilitiesProtoModule.RegisterPauseOnSolutionEventsResponse:
        """Register on pause solution events RPC of AppUtilities service."""
        return self._stub.RegisterPauseOnSolutionEvents(
            request, metadata=self._metadata
        )

    def resume_on_solution_event(
        self, request: AppUtilitiesProtoModule.ResumeOnSolutionEventRequest
    ) -> AppUtilitiesProtoModule.ResumeOnSolutionEventResponse:
        """Resume on solution event RPC of AppUtilities service."""
        return self._stub.ResumeOnSolutionEvent(request, metadata=self._metadata)

    def unregister_pause_on_solution_events(
        self, request: AppUtilitiesProtoModule.UnregisterPauseOnSolutionEventsRequest
    ) -> AppUtilitiesProtoModule.UnregisterPauseOnSolutionEventsResponse:
        """Unregister on pause solution events RPC of AppUtilities service."""
        return self._stub.UnregisterPauseOnSolutionEvents(
            request, metadata=self._metadata
        )

    def exit(
        self, request: AppUtilitiesProtoModule.ExitRequest
    ) -> AppUtilitiesProtoModule.ExitResponse:
        """Exit RPC of AppUtilities service."""
        return self._stub.Exit(request, metadata=self._metadata)

    def set_working_directory(
        self, request: AppUtilitiesProtoModule.SetWorkingDirectoryRequest
    ) -> AppUtilitiesProtoModule.SetWorkingDirectoryResponse:
        """SetWorkingDirectory RPC of AppUtilities service."""
        return self._stub.SetWorkingDirectory(request, metadata=self._metadata)


@dataclass
class ProcessInfo:
    """ProcessInfo dataclass to hold process information."""

    process_id: int
    hostname: str
    working_directory: str


@dataclass
class BuildInfo:
    """BuildInfo dataclass to hold build information."""

    build_time: str
    build_id: str
    vcs_revision: str
    vcs_branch: str


class AppUtilitiesOld:
    """AppUtilitiesOld."""

    def __init__(self, scheme_eval):
        """__init__ method of AppUtilitiesOld class."""
        self.scheme = scheme_eval

    def get_product_version(self) -> str:
        """Get product version."""
        return self.scheme.version

    def get_build_info(self) -> dict:
        """Get build info."""
        build_time = self.scheme.eval("(inquire-build-time)")
        build_id = self.scheme.eval("(inquire-build-id)")
        vcs_revision = self.scheme.eval("(inquire-src-vcs-id)")
        vcs_branch = self.scheme.eval("(inquire-src-vcs-branch)")
        return BuildInfo(
            build_time=build_time,
            build_id=build_id,
            vcs_revision=vcs_revision,
            vcs_branch=vcs_branch,
        )

    def get_controller_process_info(self) -> dict:
        """Get controller process info."""
        cortex_host = self.scheme.eval("(cx-cortex-host)")
        cortex_pid = self.scheme.eval("(cx-cortex-id)")
        cortex_pwd = self.scheme.eval("(cortex-pwd)")
        return ProcessInfo(
            process_id=cortex_pid,
            hostname=cortex_host,
            working_directory=cortex_pwd,
        )

    def get_solver_process_info(self) -> dict:
        """Get solver process info."""
        fluent_host = self.scheme.eval("(cx-client-host)")
        fluent_pid = self.scheme.eval("(cx-client-id)")
        fluent_pwd = self.scheme.eval("(cx-send '(cx-client-pwd))")
        return ProcessInfo(
            process_id=fluent_pid,
            hostname=fluent_host,
            working_directory=fluent_pwd,
        )

    def get_app_mode(self) -> Enum:
        """Get app mode."""
        from ansys.fluent.core import FluentMode

        if self.scheme.eval("(cx-solver-mode?)"):
            mode_str = self.scheme.eval('(getenv "PRJAPP_APP")')
            if mode_str == "flaero_server":
                return FluentMode.SOLVER_AERO
            elif mode_str == "flicing":
                return FluentMode.SOLVER_ICING
            else:
                return FluentMode.SOLVER
        else:
            return FluentMode.MESHING

    def start_python_journal(self, journal_name: str | None = None) -> int:
        """Start python journal."""
        if journal_name:
            self.scheme.exec([f'(api-start-python-journal "{journal_name}")'])
        else:
            self.scheme.eval("(define pyfluent-journal-str-port (open-output-string))")
            self.scheme.eval("(api-echo-python-port pyfluent-journal-str-port)")
            return "1"

    def stop_python_journal(self, journal_id: str | None = None) -> str:
        """Stop python journal."""
        if journal_id:
            self.scheme.eval("(api-unecho-python-port pyfluent-journal-str-port)")
            journal_str = self.scheme.eval(
                "(close-output-port pyfluent-journal-str-port)"
            )
            return journal_str
        else:
            self.scheme.exec(["(api-stop-python-journal)"])

    def is_beta_enabled(self) -> bool:
        """Is beta enabled."""
        return self.scheme.eval("(is-beta-feature-available?)")

    def enable_beta(self):
        """Enable beta features.

        Raises
        ------
        RuntimeError
            Not supported before Fluent 2025 R2.
        """
        raise RuntimeError(
            "Enabling beta is not supported by PyFluent for Fluent versions before 2025 R2."
        )

    def is_wildcard(self, input: str | None = None) -> bool:
        """Is wildcard."""
        return self.scheme.eval(f'(has-fnmatch-wild-card? "{input}")')

    def is_solution_data_available(self) -> bool:
        """Is solution data available."""
        return self.scheme.eval("(data-valid?)")

    def register_pause_on_solution_events(self, solution_event: SolverEvent) -> int:
        """Register pause on solution events."""
        unique_id: int = self.scheme.eval(
            f"""
            (let
                ((ids
                    (let loop ((i 1))
                        (define next-id (string->symbol (format #f "pyfluent-~d" i)))
                        (if (check-monitor-existence next-id)
                            (loop (1+ i))
                            (list i next-id)
                            )
                        )
                    ))
                (register-solution-monitor
                    (cadr ids)
                    (lambda (niter time)
                        (if (integer? niter)
                            (begin
                                (events/transmit 'auto-pause (cons (car ids) niter))
                                (grpcserver/auto-pause (is-server-running?) (cadr ids))
                                )
                            )
                        ()
                        )
                    {'#t' if solution_event == SolverEvent.TIMESTEP_ENDED else '#f'}
                    )
                (car ids)
                )
        """
        )
        return unique_id

    def resume_on_solution_event(self, registration_id: int) -> None:
        """Resume on solution event."""
        self.scheme.eval(
            f"(grpcserver/auto-resume (is-server-running?) 'pyfluent-{registration_id})"
        )

    def unregister_pause_on_solution_events(self, registration_id: int) -> None:
        """Unregister pause on solution events."""
        self.scheme.eval(f"(cancel-solution-monitor 'pyfluent-{registration_id})")

    def exit(self) -> None:
        """Exit."""
        self.scheme.exec(("(exit-server)",))

    def set_working_directory(self, path: str) -> None:
        """Change client cortex dir."""
        self.scheme.eval(f'(syncdir "{path}")')


class AppUtilities:
    """AppUtilities."""

    def __init__(self, service: AppUtilitiesService):
        """__init__ method of AppUtilities class."""
        self.service = service

    def get_product_version(self) -> str:
        """Get product version."""
        request = AppUtilitiesProtoModule.GetProductVersionRequest()
        response = self.service.get_product_version(request)
        return f"{response.major}.{response.minor}.{response.patch}"

    def get_build_info(self) -> dict:
        """Get build info."""
        request = AppUtilitiesProtoModule.GetBuildInfoRequest()
        response = self.service.get_build_info(request)
        return BuildInfo(
            build_time=response.build_time,
            build_id=response.build_id,
            vcs_revision=response.vcs_revision,
            vcs_branch=response.vcs_branch,
        )

    def get_controller_process_info(self) -> dict:
        """Get controller process info."""
        request = AppUtilitiesProtoModule.GetControllerProcessInfoRequest()
        response = self.service.get_controller_process_info(request)
        return ProcessInfo(
            process_id=response.process_id,
            hostname=response.hostname,
            working_directory=response.working_directory,
        )

    def get_solver_process_info(self) -> dict:
        """Get solver process info."""
        request = AppUtilitiesProtoModule.GetSolverProcessInfoRequest()
        response = self.service.get_solver_process_info(request)
        return ProcessInfo(
            process_id=response.process_id,
            hostname=response.hostname,
            working_directory=response.working_directory,
        )

    def get_app_mode(self) -> Enum:
        """Get app mode.

        Raises
        ------
        ValueError
            If app mode is unknown.
        """
        import ansys.fluent.core as pyfluent

        request = AppUtilitiesProtoModule.GetAppModeRequest()
        response = self.service.get_app_mode(request)
        match response.app_mode:
            case AppUtilitiesProtoModule.APP_MODE_UNKNOWN:
                raise ValueError("Unknown app mode.")
            case AppUtilitiesProtoModule.APP_MODE_MESHING:
                return pyfluent.FluentMode.MESHING
            case AppUtilitiesProtoModule.APP_MODE_SOLVER:
                return pyfluent.FluentMode.SOLVER
            case AppUtilitiesProtoModule.APP_MODE_SOLVER_ICING:
                return pyfluent.FluentMode.SOLVER_ICING
            case AppUtilitiesProtoModule.APP_MODE_SOLVER_AERO:
                return pyfluent.FluentMode.SOLVER_AERO

    def start_python_journal(self, journal_name: str | None = None) -> int:
        """Start python journal."""
        request = AppUtilitiesProtoModule.StartPythonJournalRequest()
        if journal_name:
            request.journal_name = journal_name
        response = self.service.start_python_journal(request)
        return response.journal_id

    def stop_python_journal(self, journal_id: str | None = None) -> str:
        """Stop python journal."""
        request = AppUtilitiesProtoModule.StopPythonJournalRequest()
        if journal_id:
            request.journal_id = journal_id
        response = self.service.stop_python_journal(request)
        return response.journal_str

    def is_beta_enabled(self) -> bool:
        """Is beta enabled."""
        request = AppUtilitiesProtoModule.IsBetaEnabledRequest()
        response = self.service.is_beta_enabled(request)
        return response.is_beta_enabled

    def enable_beta(self) -> None:
        """Enable beta features."""
        request = AppUtilitiesProtoModule.EnableBetaRequest()
        self.service.enable_beta(request)

    def is_wildcard(self, input: str | None = None) -> bool:
        """Is wildcard."""
        request = AppUtilitiesProtoModule.IsWildcardRequest()
        request.input = input
        response = self.service.is_wildcard(request)
        return response.is_wildcard

    def is_solution_data_available(self) -> bool:
        """Is solution data available."""
        request = AppUtilitiesProtoModule.IsSolutionDataAvailableRequest()
        response = self.service.is_solution_data_available(request)
        return response.is_solution_data_available

    def register_pause_on_solution_events(self, solution_event: SolverEvent) -> int:
        """Register pause on solution events."""
        request = AppUtilitiesProtoModule.RegisterPauseOnSolutionEventsRequest()
        request.solution_event = AppUtilitiesProtoModule.SOLUTION_EVENT_UNKNOWN
        match solution_event:
            case SolverEvent.ITERATION_ENDED:
                request.solution_event = (
                    AppUtilitiesProtoModule.SOLUTION_EVENT_ITERATION
                )
            case SolverEvent.TIMESTEP_ENDED:
                request.solution_event = (
                    AppUtilitiesProtoModule.SOLUTION_EVENT_TIME_STEP
                )
        response = self.service.register_pause_on_solution_events(request)
        return response.registration_id

    def resume_on_solution_event(self, registration_id: int) -> None:
        """Resume on solution event."""
        request = AppUtilitiesProtoModule.ResumeOnSolutionEventRequest()
        request.registration_id = registration_id
        self.service.resume_on_solution_event(request)

    def unregister_pause_on_solution_events(self, registration_id: int) -> None:
        """Unregister pause on solution events."""
        request = AppUtilitiesProtoModule.UnregisterPauseOnSolutionEventsRequest()
        request.registration_id = registration_id
        self.service.unregister_pause_on_solution_events(request)

    def exit(self) -> None:
        """Exit."""
        request = AppUtilitiesProtoModule.ExitRequest()
        self.service.exit(request)

    def set_working_directory(self, path: str) -> None:
        """Change client cortex dir."""
        request = AppUtilitiesProtoModule.SetWorkingDirectoryRequest()
        request.path = path
        self.service.set_working_directory(request)


class AppUtilitiesV252(AppUtilities):
    """AppUtilitiesV252.
    This is for methods whose implementations are missing in the 25R2 server.
    """

    def __init__(self, service: AppUtilitiesService, scheme):
        super().__init__(service)
        self.scheme = scheme

    def enable_beta(self) -> None:
        """Enable beta features."""
        self.scheme.eval(
            '(fl-execute-cmd "file" "beta-settings" (list (cons "enable?" #t)))'
        )
