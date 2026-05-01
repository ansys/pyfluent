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

"""Wrappers over AppUtilities gRPC service of Fluent (v1 proto API).

All shared logic lives in app_utilities.py (v0). This module subclasses only
the parts that differ due to renamed protobuf messages and RPC methods in v1.
"""

from ansys.api.fluent.v1 import app_utilities_pb2 as AppUtilitiesProtoModule
from ansys.api.fluent.v1 import app_utilities_pb2_grpc as AppUtilitiesGrpcModule
from ansys.fluent.core.services.app_utilities import (
    AppUtilitiesService as _AppUtilitiesServiceV0,
)
from ansys.fluent.core.services.app_utilities import (  # noqa: F401 – re-exported for consumers
    AppUtilitiesOld,
)
from ansys.fluent.core.services.app_utilities import AppUtilities as _AppUtilitiesV0
from ansys.fluent.core.services.app_utilities import BuildInfo  # noqa: F401
from ansys.fluent.core.services.app_utilities import ProcessInfo  # noqa: F401
from ansys.fluent.core.streaming_services.events_streaming_v1 import SolverEvent


class AppUtilitiesService(_AppUtilitiesServiceV0):
    """AppUtilities Service (v1 proto API)."""

    def _create_stub(self, intercept_channel):
        """Create the v1 gRPC stub."""
        return AppUtilitiesGrpcModule.AppUtilitiesStub(intercept_channel)

    def register_pause_on_solution_events(
        self, request: AppUtilitiesProtoModule.RegisterSolutionEventsPauseRequest
    ) -> AppUtilitiesProtoModule.RegisterSolutionEventsPauseResponse:
        """Register on pause solution events RPC of AppUtilities service."""
        return self._stub.RegisterSolutionEventsPause(request, metadata=self._metadata)

    def resume_on_solution_event(
        self, request: AppUtilitiesProtoModule.ResumeSolutionEventRequest
    ) -> AppUtilitiesProtoModule.ResumeSolutionEventResponse:
        """Resume on solution event RPC of AppUtilities service."""
        return self._stub.ResumeSolutionEvent(request, metadata=self._metadata)

    def unregister_pause_on_solution_events(
        self, request: AppUtilitiesProtoModule.UnregisterSolutionEventsPauseRequest
    ) -> AppUtilitiesProtoModule.UnregisterSolutionEventsPauseResponse:
        """Unregister on pause solution events RPC of AppUtilities service."""
        return self._stub.UnregisterSolutionEventsPause(
            request, metadata=self._metadata
        )


class AppUtilities(_AppUtilitiesV0):
    """AppUtilities (v1 proto API)."""

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

    def register_pause_on_solution_events(self, solution_event: SolverEvent) -> int:
        """Register pause on solution events."""
        request = AppUtilitiesProtoModule.RegisterSolutionEventsPauseRequest()
        request.solution_event = AppUtilitiesProtoModule.SOLUTION_EVENT_UNSPECIFIED
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
        request = AppUtilitiesProtoModule.ResumeSolutionEventRequest()
        request.registration_id = registration_id
        self.service.resume_on_solution_event(request)

    def unregister_pause_on_solution_events(self, registration_id: int) -> None:
        """Unregister pause on solution events."""
        request = AppUtilitiesProtoModule.UnregisterSolutionEventsPauseRequest()
        request.registration_id = registration_id
        self.service.unregister_pause_on_solution_events(request)


class AppUtilitiesV252(AppUtilities):
    """AppUtilitiesV252 (v1 proto API).

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
