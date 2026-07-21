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

"""Wrapper over the events gRPC service of Fluent (v0 proto API)."""

import logging

from google.protobuf.json_format import MessageToDict
import grpc

from ansys.api.fluent.v0 import events_pb2, events_pb2_grpc
from ansys.fluent.core._grpc_services.streaming_service import StreamingService
from ansys.fluent.core.services._protocols import ServiceProtocol

network_logger = logging.getLogger("pyfluent.networking")


class EventsService(
    StreamingService, ServiceProtocol
):  # pyright: ignore[reportUnsafeMultipleInheritance]
    """Class wrapping the events gRPC service of Fluent."""

    def __init__(
        self, channel: grpc.Channel, metadata: list[tuple[str, str]], fluent_error_state
    ):
        """__init__ method of EventsService class."""
        super().__init__(
            stub=events_pb2_grpc.EventsStub(channel),
            metadata=metadata,
        )
        del fluent_error_state  # unused in v0

    def event_from_proto_field(self, field_name: str) -> str:
        """Convert a v0 proto oneof field name to canonical event enum value."""
        return _v0_reverse_events_map.get(field_name, field_name)

    def _construct_event_info(
        self,
        response: events_pb2.BeginStreamingResponse,
        event,
        event_info_cls,
    ):
        proto_field = _v0_all_events_map.get(event.value, event.value).lower()
        event_info_msg = getattr(response, proto_field)
        # Note: MessageToDict's parameter names are different in different protobuf versions
        event_info_dict = MessageToDict(event_info_msg, True)
        # Some event-info classes intentionally have no fields. Instantiate them without payload.
        dataclass_fields = getattr(event_info_cls, "__dataclass_fields__", None)
        if dataclass_fields is None or len(dataclass_fields) == 0:
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
    "timestep_started": "TimestepStartedEvent",
    "timestep_ended": "TimestepEndedEvent",
    "iteration_ended": "IterationEndedEvent",
    "calculations_started": "CalculationsStartedEvent",
    "calculations_ended": "CalculationsEndedEvent",
    "calculations_paused": "CalculationsPausedEvent",
    "calculations_resumed": "CalculationsResumedEvent",
    "about_to_load_case": "AboutToReadCaseEvent",
    "case_loaded": "CaseReadEvent",
    "about_to_load_data": "AboutToReadDataEvent",
    "data_loaded": "DataReadEvent",
    "about_to_initialize_solution": "AboutToInitializeEvent",
    "solution_initialized": "InitializedEvent",
    "report_definition_updated": "ReportDefinitionChangedEvent",
    "report_plot_set_updated": "PlotSetChangedEvent",
    "residual_plot_updated": "ResidualPlotChangedEvent",
    "settings_cleared": "ClearSettingsDoneEvent",
    "solution_paused": "AutoPauseEvent",
    "progress_updated": "ProgressEvent",
    "solver_time_estimate_updated": "SolverTimeEstimateEvent",
    "fatal_error": "ErrorEvent",
}

meshing_events_map = {
    "about_to_load_case": "AboutToReadCaseEvent",
    "case_loaded": "CaseReadEvent",
    "settings_cleared": "ClearSettingsDoneEvent",
    "progress_updated": "ProgressEvent",
    "fatal_error": "ErrorEvent",
}

_v0_all_events_map = {**solver_events_map, **meshing_events_map}
_v0_reverse_events_map = {v.lower(): k for k, v in _v0_all_events_map.items()}
