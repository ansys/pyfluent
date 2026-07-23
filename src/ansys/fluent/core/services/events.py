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

"""High level events wrapper."""

from ansys.fluent.core.services.abstract_events import AbstractEvents
from ansys.fluent.core.streaming_services.events_streaming import SolverEvent


class Events(AbstractEvents):
    """Events backed by the Events gRPC service."""

    def __init__(self, service):
        """Initialize Events."""
        self.service = service

    def register_pause_on_solution_events(self, solution_event: SolverEvent) -> int:
        """Register pause on solution events."""
        return self.service.register_pause_on_solution_events(solution_event)

    def resume_on_solution_event(self, registration_id: int) -> None:
        """Resume on solution event."""
        self.service.resume_on_solution_event(registration_id)

    def unregister_pause_on_solution_events(self, registration_id: int) -> None:
        """Unregister pause on solution events."""
        self.service.unregister_pause_on_solution_events(registration_id)

    def event_from_proto_field(self, field_name: str) -> str:
        """Convert a proto oneof field name to canonical event enum value."""
        return self.service.event_from_proto_field(field_name)

    def _construct_event_info(self, response, event, event_info_cls):
        return self.service._construct_event_info(response, event, event_info_cls)

    def _process_streaming(self, id, stream_begin_method, started_evt, *args, **kwargs):
        """Delegate streaming request creation to the gRPC service."""
        return self.service._process_streaming(
            *args,
            id=id,
            stream_begin_method=stream_begin_method,
            started_evt=started_evt,
            **kwargs,
        )

    def begin_streaming(self, request, started_evt, id, stream_begin_method):
        """Begin streaming from Fluent."""
        return self.service.begin_streaming(
            request, started_evt, id=id, stream_begin_method=stream_begin_method
        )

    def end_streaming(self, id, stream_begin_method) -> None:
        """End streaming from Fluent."""
        self.service.end_streaming(id, stream_begin_method)


class EventsV261(AbstractEvents):
    """Events backed by the Events gRPC service."""

    def __init__(self, service, application_runtime_service):
        """Initialize ApplicationRuntime."""
        self.service = service
        self.application_runtime_service = application_runtime_service

    def register_pause_on_solution_events(self, solution_event: SolverEvent) -> int:
        """Register pause on solution events."""
        return self.application_runtime_service.register_pause_on_solution_events(
            solution_event
        )

    def resume_on_solution_event(self, registration_id: int) -> None:
        """Resume on solution event."""
        self.application_runtime_service.resume_on_solution_event(registration_id)

    def unregister_pause_on_solution_events(self, registration_id: int) -> None:
        """Unregister pause on solution events."""
        self.application_runtime_service.unregister_pause_on_solution_events(
            registration_id
        )

    def _construct_event_info(self, response, event, event_info_cls):
        return self.service._construct_event_info(response, event, event_info_cls)

    def event_from_proto_field(self, field_name: str) -> str:
        """Convert a proto oneof field name to canonical event enum value."""
        return self.service.event_from_proto_field(field_name)

    def _process_streaming(self, id, stream_begin_method, started_evt, *args, **kwargs):
        """Delegate streaming request creation to the gRPC service."""
        return self.service._process_streaming(
            *args,
            id=id,
            stream_begin_method=stream_begin_method,
            started_evt=started_evt,
            **kwargs,
        )

    def begin_streaming(self, request, started_evt, id, stream_begin_method):
        """Begin streaming from Fluent."""
        return self.service.begin_streaming(
            request, started_evt, id=id, stream_begin_method=stream_begin_method
        )

    def end_streaming(self, id, stream_begin_method) -> None:
        """End streaming from Fluent."""
        self.service.end_streaming(id, stream_begin_method)


class EventsV251(AbstractEvents):
    """Events backed by the Events gRPC service."""

    def __init__(self, service, scheme_interpreter_service):
        """Initialize ApplicationRuntime."""
        self.service = service
        self.scheme_interpreter_service = scheme_interpreter_service

    def register_pause_on_solution_events(self, solution_event: SolverEvent) -> int:
        """Register pause on solution events."""
        unique_id: int = self.scheme_interpreter_service.eval(
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
                    {"#t" if solution_event.name == "TIMESTEP_ENDED" else "#f"}
                    )
                (car ids)
                )
        """
        )
        return unique_id

    def resume_on_solution_event(self, registration_id: int) -> None:
        """Resume on solution event."""
        self.scheme_interpreter_service.eval(
            f"(grpcserver/auto-resume (is-server-running?) 'pyfluent-{registration_id})"
        )

    def unregister_pause_on_solution_events(self, registration_id: int) -> None:
        """Unregister pause on solution events."""
        self.scheme_interpreter_service.eval(
            f"(cancel-solution-monitor 'pyfluent-{registration_id})"
        )

    def _construct_event_info(self, response, event, event_info_cls):
        return self.service._construct_event_info(response, event, event_info_cls)

    def event_from_proto_field(self, field_name: str) -> str:
        """Convert a proto oneof field name to canonical event enum value."""
        return self.service.event_from_proto_field(field_name)

    def _process_streaming(self, id, stream_begin_method, started_evt, *args, **kwargs):
        """Delegate streaming request creation to the gRPC service."""
        return self.service._process_streaming(
            *args,
            id=id,
            stream_begin_method=stream_begin_method,
            started_evt=started_evt,
            **kwargs,
        )

    def begin_streaming(self, request, started_evt, id, stream_begin_method):
        """Begin streaming from Fluent."""
        return self.service.begin_streaming(
            request, started_evt, id=id, stream_begin_method=stream_begin_method
        )

    def end_streaming(self, id, stream_begin_method) -> None:
        """End streaming from Fluent."""
        self.service.end_streaming(id, stream_begin_method)
