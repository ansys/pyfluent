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

"""Implementation of AppUtilities gRPC service of Fluent."""

from dataclasses import dataclass
from enum import Enum
import os

from ansys.api.fluent.v0 import app_utilities_pb2 as AppUtilitiesProtoModuleV0
from ansys.api.fluent.v1 import app_utilities_pb2 as AppUtilitiesProtoModule
from ansys.fluent.core._types import PathType
from ansys.fluent.core.services import AppUtilitiesService, AppUtilitiesServiceV0
from ansys.fluent.core.streaming_services.events_streaming import (
    SolverEvent as SolverEventV0,
)
from ansys.fluent.core.streaming_services.events_streaming_v1 import SolverEvent


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

    def register_pause_on_solution_events(self, solution_event: SolverEventV0) -> int:
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
                    {"#t" if solution_event == SolverEventV0.TIMESTEP_ENDED else "#f"}
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

    def set_working_directory(self, path: PathType) -> None:
        """Change client cortex dir."""
        self.scheme.eval(f'(syncdir "{os.fspath(path)}")')


class AppUtilitiesV0:
    """AppUtilities."""

    def __init__(self, service: AppUtilitiesServiceV0):
        """__init__ method of AppUtilities class."""
        self.service = service

    def get_product_version(self) -> str:
        """Get product version."""
        request = AppUtilitiesProtoModuleV0.GetProductVersionRequest()
        response = self.service.get_product_version(request)
        return f"{response.major}.{response.minor}.{response.patch}"

    def get_build_info(self) -> dict:
        """Get build info."""
        request = AppUtilitiesProtoModuleV0.GetBuildInfoRequest()
        response = self.service.get_build_info(request)
        return BuildInfo(
            build_time=response.build_time,
            build_id=response.build_id,
            vcs_revision=response.vcs_revision,
            vcs_branch=response.vcs_branch,
        )

    def get_controller_process_info(self) -> dict:
        """Get controller process info."""
        request = AppUtilitiesProtoModuleV0.GetControllerProcessInfoRequest()
        response = self.service.get_controller_process_info(request)
        return ProcessInfo(
            process_id=response.process_id,
            hostname=response.hostname,
            working_directory=response.working_directory,
        )

    def get_solver_process_info(self) -> dict:
        """Get solver process info."""
        request = AppUtilitiesProtoModuleV0.GetSolverProcessInfoRequest()
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

        request = AppUtilitiesProtoModuleV0.GetAppModeRequest()
        response = self.service.get_app_mode(request)
        match response.app_mode:
            case AppUtilitiesProtoModuleV0.APP_MODE_UNKNOWN:
                raise ValueError("Unknown app mode.")
            case AppUtilitiesProtoModuleV0.APP_MODE_MESHING:
                return pyfluent.FluentMode.MESHING
            case AppUtilitiesProtoModuleV0.APP_MODE_SOLVER:
                return pyfluent.FluentMode.SOLVER
            case AppUtilitiesProtoModuleV0.APP_MODE_SOLVER_ICING:
                return pyfluent.FluentMode.SOLVER_ICING
            case AppUtilitiesProtoModuleV0.APP_MODE_SOLVER_AERO:
                return pyfluent.FluentMode.SOLVER_AERO

    def start_python_journal(self, journal_name: str | None = None) -> int:
        """Start python journal."""
        request = AppUtilitiesProtoModuleV0.StartPythonJournalRequest()
        if journal_name:
            request.journal_name = journal_name
        response = self.service.start_python_journal(request)
        return response.journal_id

    def stop_python_journal(self, journal_id: str | None = None) -> str:
        """Stop python journal."""
        request = AppUtilitiesProtoModuleV0.StopPythonJournalRequest()
        if journal_id:
            request.journal_id = journal_id
        response = self.service.stop_python_journal(request)
        return response.journal_str

    def is_beta_enabled(self) -> bool:
        """Is beta enabled."""
        request = AppUtilitiesProtoModuleV0.IsBetaEnabledRequest()
        response = self.service.is_beta_enabled(request)
        return response.is_beta_enabled

    def enable_beta(self) -> None:
        """Enable beta features."""
        request = AppUtilitiesProtoModuleV0.EnableBetaRequest()
        self.service.enable_beta(request)

    def is_wildcard(self, input: str | None = None) -> bool:
        """Is wildcard."""
        request = AppUtilitiesProtoModuleV0.IsWildcardRequest()
        request.input = input
        response = self.service.is_wildcard(request)
        return response.is_wildcard

    def is_solution_data_available(self) -> bool:
        """Is solution data available."""
        request = AppUtilitiesProtoModuleV0.IsSolutionDataAvailableRequest()
        response = self.service.is_solution_data_available(request)
        return response.is_solution_data_available

    def register_pause_on_solution_events(self, solution_event: SolverEventV0) -> int:
        """Register pause on solution events."""
        request = AppUtilitiesProtoModuleV0.RegisterPauseOnSolutionEventsRequest()
        request.solution_event = AppUtilitiesProtoModuleV0.SOLUTION_EVENT_UNKNOWN
        match solution_event:
            case SolverEventV0.ITERATION_ENDED:
                request.solution_event = (
                    AppUtilitiesProtoModuleV0.SOLUTION_EVENT_ITERATION
                )
            case SolverEventV0.TIMESTEP_ENDED:
                request.solution_event = (
                    AppUtilitiesProtoModuleV0.SOLUTION_EVENT_TIME_STEP
                )
        response = self.service.register_pause_on_solution_events(request)
        return response.registration_id

    def resume_on_solution_event(self, registration_id: int) -> None:
        """Resume on solution event."""
        request = AppUtilitiesProtoModuleV0.ResumeOnSolutionEventRequest()
        request.registration_id = registration_id
        self.service.resume_on_solution_event(request)

    def unregister_pause_on_solution_events(self, registration_id: int) -> None:
        """Unregister pause on solution events."""
        request = AppUtilitiesProtoModuleV0.UnregisterPauseOnSolutionEventsRequest()
        request.registration_id = registration_id
        self.service.unregister_pause_on_solution_events(request)

    def exit(self) -> None:
        """Exit."""
        request = AppUtilitiesProtoModuleV0.ExitRequest()
        self.service.exit(request)

    def set_working_directory(self, path: PathType) -> None:
        """Change client cortex dir."""
        request = AppUtilitiesProtoModuleV0.SetWorkingDirectoryRequest()
        request.path = os.fspath(path)
        self.service.set_working_directory(request)


class AppUtilitiesV252(AppUtilitiesV0):
    """AppUtilitiesV252.
    This is for methods whose implementations are missing in the 25R2 server.
    """

    def __init__(self, service: AppUtilitiesServiceV0, scheme):
        super().__init__(service)
        self.scheme = scheme

    def enable_beta(self) -> None:
        """Enable beta features."""
        self.scheme.eval(
            '(fl-execute-cmd "file" "beta-settings" (list (cons "enable?" #t)))'
        )


class AppUtilities(AppUtilitiesV0):
    """AppUtilities (v1 proto API)."""

    def __init__(self, service: AppUtilitiesService):
        super().__init__(service=service)

    def get_app_mode(self):
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
            case AppUtilitiesProtoModule.APP_MODE_UNSPECIFIED:
                raise ValueError("Unknown app mode.")
            case AppUtilitiesProtoModule.APP_MODE_MESHING:
                return pyfluent.FluentMode.MESHING
            case AppUtilitiesProtoModule.APP_MODE_SOLVER:
                return pyfluent.FluentMode.SOLVER
            case AppUtilitiesProtoModule.APP_MODE_SOLVER_ICING:
                return pyfluent.FluentMode.SOLVER_ICING
            case AppUtilitiesProtoModule.APP_MODE_SOLVER_AERO:
                return pyfluent.FluentMode.SOLVER_AERO
