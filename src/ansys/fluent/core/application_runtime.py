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

"""High-level application runtime wrappers.

This module owns the business-logic layer on top of the AppUtilities gRPC
service.  The raw service stubs live in:

* ``ansys.fluent.core.services.app_utilities_v0`` (v0 proto API)
* ``ansys.fluent.core.services.app_utilities_v1`` (v1 proto API)

Class hierarchy
---------------
``ApplicationRuntimeOld``
    Scheme-based fallback used for Fluent versions before 25R2.

``ApplicationRuntime``
    gRPC-based implementation (v0 proto API).

``ApplicationRuntimeV1(ApplicationRuntime)``
    Thin v1 subclass – overrides only ``get_app_mode`` because the enum
    constants differ between the two proto versions.

``ApplicationRuntimeV252(ApplicationRuntime)``
    Fallback for Fluent 25R2 servers where ``EnableBeta`` is not yet
    implemented; delegates to Scheme instead.
"""

from dataclasses import dataclass
from enum import Enum
import os

from ansys.fluent.core._types import PathType
from ansys.fluent.core.streaming_services.events_streaming import SolverEvent

# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class ProcessInfo:
    """Hold process information."""

    process_id: int
    hostname: str
    working_directory: str


@dataclass
class BuildInfo:
    """Hold build information."""

    build_time: str
    build_id: str
    vcs_revision: str
    vcs_branch: str


# ---------------------------------------------------------------------------
# Scheme-based fallback (pre-gRPC, Fluent < 25R2)
# ---------------------------------------------------------------------------


class ApplicationRuntimeOld:
    """Application runtime backed by Scheme evaluation (Fluent < 25R2)."""

    def __init__(self, scheme_eval):
        """Initialize ApplicationRuntimeOld."""
        self.scheme = scheme_eval

    def get_product_version(self) -> str:
        """Get product version."""
        return self.scheme.version

    def get_build_info(self) -> BuildInfo:
        """Get build info."""
        return BuildInfo(
            build_time=self.scheme.eval("(inquire-build-time)"),
            build_id=self.scheme.eval("(inquire-build-id)"),
            vcs_revision=self.scheme.eval("(inquire-src-vcs-id)"),
            vcs_branch=self.scheme.eval("(inquire-src-vcs-branch)"),
        )

    def get_controller_process_info(self) -> ProcessInfo:
        """Get controller process info."""
        return ProcessInfo(
            process_id=self.scheme.eval("(cx-cortex-id)"),
            hostname=self.scheme.eval("(cx-cortex-host)"),
            working_directory=self.scheme.eval("(cortex-pwd)"),
        )

    def get_solver_process_info(self) -> ProcessInfo:
        """Get solver process info."""
        return ProcessInfo(
            process_id=self.scheme.eval("(cx-client-id)"),
            hostname=self.scheme.eval("(cx-client-host)"),
            working_directory=self.scheme.eval("(cx-send '(cx-client-pwd))"),
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
        """Return whether beta features are enabled."""
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
        """Return whether *input* contains a wildcard pattern."""
        return self.scheme.eval(f'(has-fnmatch-wild-card? "{input}")')

    def is_solution_data_available(self) -> bool:
        """Return whether solution data is currently available."""
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
                    {"#t" if solution_event == SolverEvent.TIMESTEP_ENDED else "#f"}
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
        """Exit the server."""
        self.scheme.exec(("(exit-server)",))

    def set_working_directory(self, path: PathType) -> None:
        """Change the client cortex working directory."""
        self.scheme.eval(f'(syncdir "{os.fspath(path)}")')


# ---------------------------------------------------------------------------
# gRPC-based implementation (v0 proto API)
# ---------------------------------------------------------------------------


class ApplicationRuntime:
    """Application runtime backed by the AppUtilities gRPC service (v0 proto API)."""

    def __init__(self, service):
        """Initialize ApplicationRuntime."""
        self.service = service

    def get_product_version(self) -> str:
        """Get product version."""
        from ansys.api.fluent.v0 import app_utilities_pb2 as _proto

        request = _proto.GetProductVersionRequest()
        response = self.service.get_product_version(request)
        return f"{response.major}.{response.minor}.{response.patch}"

    def get_build_info(self) -> BuildInfo:
        """Get build info."""
        from ansys.api.fluent.v0 import app_utilities_pb2 as _proto

        request = _proto.GetBuildInfoRequest()
        response = self.service.get_build_info(request)
        return BuildInfo(
            build_time=response.build_time,
            build_id=response.build_id,
            vcs_revision=response.vcs_revision,
            vcs_branch=response.vcs_branch,
        )

    def get_controller_process_info(self) -> ProcessInfo:
        """Get controller process info."""
        from ansys.api.fluent.v0 import app_utilities_pb2 as _proto

        request = _proto.GetControllerProcessInfoRequest()
        response = self.service.get_controller_process_info(request)
        return ProcessInfo(
            process_id=response.process_id,
            hostname=response.hostname,
            working_directory=response.working_directory,
        )

    def get_solver_process_info(self) -> ProcessInfo:
        """Get solver process info."""
        from ansys.api.fluent.v0 import app_utilities_pb2 as _proto

        request = _proto.GetSolverProcessInfoRequest()
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
        from ansys.api.fluent.v0 import app_utilities_pb2 as _proto
        import ansys.fluent.core as pyfluent

        request = _proto.GetAppModeRequest()
        response = self.service.get_app_mode(request)
        match response.app_mode:
            case _proto.APP_MODE_UNKNOWN:
                raise ValueError("Unknown app mode.")
            case _proto.APP_MODE_MESHING:
                return pyfluent.FluentMode.MESHING
            case _proto.APP_MODE_SOLVER:
                return pyfluent.FluentMode.SOLVER
            case _proto.APP_MODE_SOLVER_ICING:
                return pyfluent.FluentMode.SOLVER_ICING
            case _proto.APP_MODE_SOLVER_AERO:
                return pyfluent.FluentMode.SOLVER_AERO

    def start_python_journal(self, journal_name: str | None = None) -> int:
        """Start python journal."""
        from ansys.api.fluent.v0 import app_utilities_pb2 as _proto

        request = _proto.StartPythonJournalRequest()
        if journal_name:
            request.journal_name = journal_name
        response = self.service.start_python_journal(request)
        return response.journal_id

    def stop_python_journal(self, journal_id: str | None = None) -> str:
        """Stop python journal."""
        from ansys.api.fluent.v0 import app_utilities_pb2 as _proto

        request = _proto.StopPythonJournalRequest()
        if journal_id:
            request.journal_id = journal_id
        response = self.service.stop_python_journal(request)
        return response.journal_str

    def is_beta_enabled(self) -> bool:
        """Return whether beta features are enabled."""
        from ansys.api.fluent.v0 import app_utilities_pb2 as _proto

        request = _proto.IsBetaEnabledRequest()
        response = self.service.is_beta_enabled(request)
        return response.is_beta_enabled

    def enable_beta(self) -> None:
        """Enable beta features."""
        from ansys.api.fluent.v0 import app_utilities_pb2 as _proto

        request = _proto.EnableBetaRequest()
        self.service.enable_beta(request)

    def is_wildcard(self, input: str | None = None) -> bool:
        """Return whether *input* contains a wildcard pattern."""
        from ansys.api.fluent.v0 import app_utilities_pb2 as _proto

        request = _proto.IsWildcardRequest()
        request.input = input
        response = self.service.is_wildcard(request)
        return response.is_wildcard

    def is_solution_data_available(self) -> bool:
        """Return whether solution data is currently available."""
        from ansys.api.fluent.v0 import app_utilities_pb2 as _proto

        request = _proto.IsSolutionDataAvailableRequest()
        response = self.service.is_solution_data_available(request)
        return response.is_solution_data_available

    def register_pause_on_solution_events(self, solution_event: SolverEvent) -> int:
        """Register pause on solution events."""
        from ansys.api.fluent.v0 import app_utilities_pb2 as _proto

        request = _proto.RegisterPauseOnSolutionEventsRequest()
        request.solution_event = _proto.SOLUTION_EVENT_UNKNOWN
        match solution_event:
            case SolverEvent.ITERATION_ENDED:
                request.solution_event = _proto.SOLUTION_EVENT_ITERATION
            case SolverEvent.TIMESTEP_ENDED:
                request.solution_event = _proto.SOLUTION_EVENT_TIME_STEP
        response = self.service.register_pause_on_solution_events(request)
        return response.registration_id

    def resume_on_solution_event(self, registration_id: int) -> None:
        """Resume on solution event."""
        from ansys.api.fluent.v0 import app_utilities_pb2 as _proto

        request = _proto.ResumeOnSolutionEventRequest()
        request.registration_id = registration_id
        self.service.resume_on_solution_event(request)

    def unregister_pause_on_solution_events(self, registration_id: int) -> None:
        """Unregister pause on solution events."""
        from ansys.api.fluent.v0 import app_utilities_pb2 as _proto

        request = _proto.UnregisterPauseOnSolutionEventsRequest()
        request.registration_id = registration_id
        self.service.unregister_pause_on_solution_events(request)

    def exit(self) -> None:
        """Exit the server."""
        from ansys.api.fluent.v0 import app_utilities_pb2 as _proto

        request = _proto.ExitRequest()
        self.service.exit(request)

    def set_working_directory(self, path: PathType) -> None:
        """Change the client cortex working directory."""
        from ansys.api.fluent.v0 import app_utilities_pb2 as _proto

        request = _proto.SetWorkingDirectoryRequest()
        request.path = os.fspath(path)
        self.service.set_working_directory(request)


# ---------------------------------------------------------------------------
# v1 proto override – only get_app_mode differs (different enum constants)
# ---------------------------------------------------------------------------


class ApplicationRuntimeV1(ApplicationRuntime):
    """Application runtime for the v1 proto API.

    Identical to :class:`ApplicationRuntime` except for ``get_app_mode``,
    which uses the v1 proto enum constants (``APP_MODE_UNSPECIFIED`` instead
    of ``APP_MODE_UNKNOWN``).
    """

    def get_app_mode(self) -> Enum:
        """Get app mode.

        Raises
        ------
        ValueError
            If app mode is unknown.
        """
        from ansys.api.fluent.v1 import application_runtime_pb2 as _proto
        import ansys.fluent.core as pyfluent

        request = _proto.GetAppModeRequest()
        response = self.service.get_app_mode(request)
        match response.app_mode:
            case _proto.APP_MODE_UNSPECIFIED:
                raise ValueError("Unknown app mode.")
            case _proto.APP_MODE_MESHING:
                return pyfluent.FluentMode.MESHING
            case _proto.APP_MODE_SOLVER:
                return pyfluent.FluentMode.SOLVER
            case _proto.APP_MODE_SOLVER_ICING:
                return pyfluent.FluentMode.SOLVER_ICING
            case _proto.APP_MODE_SOLVER_AERO:
                return pyfluent.FluentMode.SOLVER_AERO


# ---------------------------------------------------------------------------
# Fluent 25R2 variant – EnableBeta not yet on the server
# ---------------------------------------------------------------------------


class ApplicationRuntimeV252(ApplicationRuntime):
    """Application runtime for Fluent 25R2.

    ``enable_beta`` is not implemented on the 25R2 server so it falls
    back to a Scheme call.  Accepts either a v0 or v1 service.
    """

    def __init__(self, service, scheme):
        """Initialize ApplicationRuntimeV252."""
        super().__init__(service)
        self.scheme = scheme

    def enable_beta(self) -> None:
        """Enable beta features via Scheme (25R2 fallback)."""
        self.scheme.eval(
            '(fl-execute-cmd "file" "beta-settings" (list (cons "enable?" #t)))'
        )


class ApplicationRuntimeV252V1(ApplicationRuntimeV1):
    """Application runtime for Fluent 25R2 (v1 proto API).

    Like :class:`ApplicationRuntimeV252` but inherits the v1
    ``get_app_mode`` override from :class:`ApplicationRuntimeV1`.
    """

    def __init__(self, service, scheme):
        """Initialize ApplicationRuntimeV252V1."""
        super().__init__(service)
        self.scheme = scheme

    def enable_beta(self) -> None:
        """Enable beta features via Scheme (25R2 fallback)."""
        self.scheme.eval(
            '(fl-execute-cmd "file" "beta-settings" (list (cons "enable?" #t)))'
        )
