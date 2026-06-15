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

"""Wrapper over the events gRPC service of Fluent (v1 proto API).

All shared logic lives in events.py (v0). This module keeps only
v1-specific stub binding required for compatibility.
"""

import grpc

from ansys.api.fluent.v1 import events_pb2 as EventsProtoModule
from ansys.api.fluent.v1 import events_pb2_grpc as EventsGrpcModule
from ansys.fluent.core.services.events import EventsService as _EventsServiceV0
from ansys.fluent.core.streaming_services.events_streaming_v1 import SolverEvent


class EventsService(_EventsServiceV0):
    """Class wrapping the events gRPC service of Fluent (v1 proto API)."""

    def _create_stub(self, channel: grpc.Channel):
        """Create the v1 gRPC stub."""
        return EventsGrpcModule.EventsStub(channel)

    def pause_solve_for(
        self, request: EventsProtoModule.PauseSolveForRequest
    ) -> EventsProtoModule.PauseSolveForResponse:
        """PauseSolveFor RPC of Events service (v1)."""
        return self._events_stub.PauseSolveFor(request, metadata=self._metadata)

    def resume_solve(
        self, request: EventsProtoModule.ResumeSolveRequest
    ) -> EventsProtoModule.ResumeSolveResponse:
        """ResumeSolve RPC of Events service (v1)."""
        return self._events_stub.ResumeSolve(request, metadata=self._metadata)

    def cancel_pause_solve(
        self, request: EventsProtoModule.CancelPauseSolveRequest
    ) -> EventsProtoModule.CancelPauseSolveResponse:
        """CancelPauseSolve RPC of Events service (v1)."""
        return self._events_stub.CancelPauseSolve(request, metadata=self._metadata)


class Events:
    """Events."""

    def __init__(self, service: EventsService):
        self._service = service

    def register_pause_on_solution_events(self, solution_event: SolverEvent) -> int:
        """Register pause on solution events."""
        request = EventsProtoModule.PauseSolveForRequest()
        request.solution_event = EventsProtoModule.SOLUTION_EVENT_UNSPECIFIED
        match solution_event:
            case SolverEvent.ITERATION_ENDED:
                request.solution_event = EventsProtoModule.SOLUTION_EVENT_ITERATION
            case SolverEvent.TIMESTEP_ENDED:
                request.solution_event = EventsProtoModule.SOLUTION_EVENT_TIME_STEP
        response = self.service.pause_solve_for(request)
        return response.registration_id

    def resume_on_solution_event(self, registration_id: int) -> None:
        """Resume on solution event."""
        request = EventsProtoModule.ResumeSolveRequest()
        request.registration_id = registration_id
        self.service.resume_solve(request)

    def unregister_pause_on_solution_events(self, registration_id: int) -> None:
        """Unregister pause on solution events."""
        request = EventsProtoModule.CancelPauseSolveRequest()
        request.registration_id = registration_id
        self.service.cancel_pause_solve(request)
