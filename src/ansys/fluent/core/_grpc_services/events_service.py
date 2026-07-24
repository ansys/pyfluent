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

from google.protobuf.json_format import MessageToDict

from ansys.api.fluent.v1 import events_pb2, events_pb2_grpc
from ansys.fluent.core._grpc_services._streaming import StreamingService
from ansys.fluent.core.services._protocols import ServiceProtocol
from ansys.fluent.core.streaming_services.events_streaming import SolverEvent


class EventsService(StreamingService, ServiceProtocol):
    """Class wrapping the events gRPC service of Fluent (v1 proto API)."""

    def __init__(
        self,
        channel,
        metadata: list[tuple[str, str]],
    ):
        """__init__ method of EventsService class."""
        super().__init__(
            stub=events_pb2_grpc.EventsStub(channel),
            metadata=metadata,
        )

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

    def event_from_proto_field(self, field_name: str) -> str:
        """Convert a v1 proto oneof field name to canonical event enum value."""
        return _v1_reverse_events_map.get(field_name, field_name)

    def _construct_event_info(
        self,
        response: events_pb2.BeginStreamingResponse,
        event,
        event_info_cls,
    ):
        proto_field = _v1_all_events_map.get(event.value, event.value)
        event_info_msg = getattr(response, proto_field)
        # Note: MessageToDict's parameter names are different in different protobuf versions
        event_info_dict = MessageToDict(event_info_msg, True)
        # Some event-info classes intentionally have no fields. Instantiate them without payload.
        dataclass_fields = getattr(event_info_cls, "__dataclass_fields__", None)
        if dataclass_fields is None or len(dataclass_fields) == 0:
            return event_info_cls()
        # v1 servers can emit empty payloads for some events; keep fallback v1-only
        # to avoid changing backward-compatible v0 behavior.
        if not event_info_dict:
            return event_info_cls()
        # Key names can be different, but their order is the same
        return event_info_cls(*event_info_dict.values())

    def _process_streaming(self, id, stream_begin_method, started_evt, *args, **kwargs):
        """Processes events streaming."""
        request = events_pb2.BeginStreamingRequest(*args, **kwargs)
        return self.begin_streaming(
            request, started_evt, id=id, stream_begin_method=stream_begin_method
        )


solver_events_map = {
    "timestep_started": "timestep_started_event",
    "timestep_ended": "timestep_ended_event",
    "iteration_ended": "iteration_ended_event",
    "calculations_started": "calculations_started_event",
    "calculations_ended": "calculations_ended_event",
    "calculations_paused": "calculations_paused_event",
    "calculations_resumed": "calculations_resumed_event",
    "about_to_load_case": "pre_read_case_event",
    "case_loaded": "case_read_event",
    "about_to_load_data": "pre_read_data_event",
    "data_loaded": "data_read_event",
    "about_to_initialize_solution": "pre_initialize_event",
    "solution_initialized": "initialized_event",
    "report_definition_updated": "report_definition_changed_event",
    "report_plot_set_updated": "plot_set_changed_event",
    "residual_plot_updated": "residual_plot_changed_event",
    "settings_cleared": "clear_settings_done_event",
    "solution_paused": "auto_pause_event",
    "progress_updated": "progress_event",
    "solver_time_estimate_updated": "solver_time_estimate_event",
    "fatal_error": "error_event",
}

meshing_events_map = {
    "about_to_load_case": "pre_read_case_event",
    "case_loaded": "case_read_event",
    "settings_cleared": "clear_settings_done_event",
    "progress_updated": "progress_event",
    "fatal_error": "error_event",
}

_v1_all_events_map = {**solver_events_map, **meshing_events_map}
_v1_reverse_events_map = {v: k for k, v in _v1_all_events_map.items()}
