# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
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

"""Wrapper over the events gRPC service of Fluent (v1 proto API)."""

import grpc

from ansys.api.fluent.v1 import events_pb2, events_pb2_grpc
from ansys.fluent.core._grpc_services.streaming_service import StreamingService
from ansys.fluent.core.services._protocols import ServiceProtocol
from ansys.fluent.core.streaming_services.events_streaming_v1 import SolverEvent


class EventsService(StreamingService, ServiceProtocol):
    """Class wrapping the events gRPC service of Fluent (v1 proto API)."""

    def __init__(
        self, channel: grpc.Channel, metadata: list[tuple[str, str]], fluent_error_state
    ):
        """__init__ method of EventsService class."""
        super().__init__(
            stub=events_pb2_grpc.EventsStub(channel),
            metadata=metadata,
        )
        del fluent_error_state  # unused in v1

    def register_pause_on_solution_events(self, solution_event: SolverEvent) -> int:
        """Register pause on solution events."""
        request = events_pb2.PauseSolveForRequest()
        request.solution_event = events_pb2.SOLUTION_EVENT_UNSPECIFIED
        match solution_event:
            case SolverEvent.ITERATION_ENDED:
                request.solution_event = events_pb2.SOLUTION_EVENT_ITERATION
            case SolverEvent.TIMESTEP_ENDED:
                request.solution_event = events_pb2.SOLUTION_EVENT_TIME_STEP
        response = self._stub.PauseSolveFor(request, metadata=self._metadata)
        return response.registration_id

    def resume_on_solution_event(self, registration_id: int) -> None:
        """Resume on solution event."""
        request = events_pb2.ResumeSolveRequest()
        request.registration_id = registration_id
        self._stub.ResumeSolve(request, metadata=self._metadata)

    def unregister_pause_on_solution_events(self, registration_id: int) -> None:
        """Unregister pause on solution events."""
        request = events_pb2.CancelPauseSolveRequest()
        request.registration_id = registration_id
        self._stub.CancelPauseSolve(request, metadata=self._metadata)
