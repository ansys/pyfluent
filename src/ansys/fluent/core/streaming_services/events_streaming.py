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

"""Module for events management."""

from collections.abc import Callable, Sequence
from functools import partial
import inspect
import logging
from typing import Generic, TypeVar
import warnings

from ansys.fluent.core.exceptions import InvalidArgument
from ansys.fluent.core.pyfluent_warnings import PyFluentDeprecationWarning
from ansys.fluent.core.streaming_services._events_info_store import (
    AboutToInitializeSolutionEventInfo,
    AboutToLoadCaseEventInfo,
    AboutToLoadDataEventInfo,
    CalculationsEndedEventInfo,
    CalculationsPausedEventInfo,
    CalculationsResumedEventInfo,
    CalculationsStartedEventInfo,
    CaseLoadedEventInfo,
    DataLoadedEventInfo,
    EventInfoBase,
    FatalErrorEventInfo,
    IterationEndedEventInfo,
    MeshingEvent,
    ProgressUpdatedEventInfo,
    ReportDefinitionUpdatedEventInfo,
    ReportPlotSetUpdatedEventInfo,
    ResidualPlotUpdatedEventInfo,
    SettingsClearedEventInfo,
    SolutionInitializedEventInfo,
    SolutionPausedEventInfo,
    SolverEvent,
    SolverTimeEstimateUpdatedEventInfo,
    TimestepEndedEventInfo,
    TimestepStartedEventInfo,
)
from ansys.fluent.core.streaming_services.streaming import StreamingService

network_logger = logging.getLogger("pyfluent.networking")

# Backward-compatibility alias
Event = SolverEvent

__all__ = [
    "EventsManager",
    "Event",
    "SolverEvent",
    "MeshingEvent",
    "TimestepStartedEventInfo",
    "TimestepEndedEventInfo",
    "IterationEndedEventInfo",
    "CalculationsStartedEventInfo",
    "CalculationsEndedEventInfo",
    "CalculationsPausedEventInfo",
    "CalculationsResumedEventInfo",
    "AboutToLoadCaseEventInfo",
    "CaseLoadedEventInfo",
    "AboutToLoadDataEventInfo",
    "DataLoadedEventInfo",
    "AboutToInitializeSolutionEventInfo",
    "SolutionInitializedEventInfo",
    "ReportDefinitionUpdatedEventInfo",
    "ReportPlotSetUpdatedEventInfo",
    "ResidualPlotUpdatedEventInfo",
    "SettingsClearedEventInfo",
    "SolutionPausedEventInfo",
    "ProgressUpdatedEventInfo",
    "SolverTimeEstimateUpdatedEventInfo",
    "FatalErrorEventInfo",
]

TEvent = TypeVar("TEvent")


class EventsManager(Generic[TEvent]):
    """Manages server-side events.

    This class allows the client to register and unregister callbacks with server
    events.
    """

    def __init__(
        self,
        event_type: type[TEvent],
        session_events_service,
        fluent_error_state,
        session,
    ):
        """__init__ method of EventsManager class."""
        self._event_type = event_type
        self._impl = StreamingService(
            stream_begin_method="BeginStreaming",
            target=partial(EventsManager._process_streaming, self),
            streaming_service=session_events_service,
        )
        self._fluent_error_state = fluent_error_state
        # This has been updated from id to session, which
        # can also be done in other streaming services
        self._session = session
        self._sync_event_ids = {}
        self._service = session_events_service

    def _construct_event_info(self, response, event: TEvent):
        return self._service._construct_event_info(
            response, event, EventInfoBase.derived_classes.get(event.name)
        )

    def _process_streaming(
        self, service, id, stream_begin_method, started_evt, *args, **kwargs
    ):
        responses = self._service._process_streaming(
            *args,
            id=id,
            stream_begin_method=stream_begin_method,
            started_evt=started_evt,
            **kwargs,
        )
        while True:
            try:
                response = next(responses)
                raw_field = response.WhichOneof("as")
                event_name = self._event_type(
                    self._service.event_from_proto_field(raw_field)
                )
                event_info = self._construct_event_info(response, event_name)
                with service._lock:
                    service._streaming = True
                    # error-code 0 from Fluent indicates server running without error
                    if event_name.name == "FATAL_ERROR" and event_info.error_code != 0:
                        error_message = event_info.message.rstrip()
                        network_logger.error(
                            f"gRPC - {error_message}, "
                            f"errorCode {event_info.error_code}"
                        )
                        self._fluent_error_state.set("fatal", error_message)
                        continue
                    callbacks_map = self._impl._service_callbacks.get(event_name, {})
                    for callback in callbacks_map.values():
                        callback(
                            session=self._session,
                            event_info=event_info,
                        )
            except StopIteration:
                break

    @staticmethod
    def _make_callback_to_call(callback: Callable, args, kwargs):
        params = inspect.signature(callback).parameters
        if "session_id" in params:
            warnings.warn(
                "Update event callback function signatures"
                " substituting 'session' for 'session_id'.",
                PyFluentDeprecationWarning,
            )
            return lambda session, event_info: callback(
                *args, session_id=session.id, event_info=event_info, **kwargs
            )
        else:
            positional_args = [
                p
                for p in params
                if p not in kwargs and p not in ("session", "event_info")
            ]
            kwargs.update(dict(zip(positional_args, args)))
            return lambda session, event_info: callback(
                session=session, event_info=event_info, **kwargs
            )

    def _register_single_callback(
        self,
        event_name: TEvent | str,
        callback: Callable,
        *args,
        **kwargs,
    ):
        """Register the callback.

        Parameters
        ----------
        event_name : TEvent or str
            Event to register the callback to.
        callback : Callable
            Callback to register. If the custom arguments,
            args and kwargs, are empty then the callback
            signature must be precisely <function>(session, event_info).
            Otherwise, the arguments for args and/or kwargs
            must precede the other arguments in the signature.
        args : Any
            Arguments.
        kwargs : Any
            Keyword arguments.

        Returns
        -------
        str
            Registered callback ID.

        Raises
        ------
        InvalidArgument
            If event name is not valid.
        """
        if event_name is None or callback is None:
            raise InvalidArgument("'event_name' and 'callback' ")

        event_name = self._event_type(event_name)
        with self._impl._lock:
            callback_id = f"{event_name}-{next(self._impl._service_callback_id)}"
            callback_to_call = EventsManager._make_callback_to_call(
                callback, args, kwargs
            )
            if event_name.name in ["ITERATION_ENDED", "TIMESTEP_ENDED"]:
                event_name, callback_to_call = (
                    self._register_solution_event_sync_callback(
                        event_name, callback_id, callback_to_call
                    )
                )
            callbacks_map = self._impl._service_callbacks.get(event_name)
            if callbacks_map:
                callbacks_map.update({callback_id: callback_to_call})
            else:
                self._impl._service_callbacks[event_name] = {
                    callback_id: callback_to_call
                }
            return callback_id

    def register_callback(
        self,
        event_types: (
            SolverEvent | MeshingEvent | Sequence[SolverEvent] | Sequence[MeshingEvent]
        ),
        callback: Callable,
        *args,
        **kwargs,
    ):
        """Register the callback.

        Parameters
        ----------
        event_types : TEvent or str
            Events to register the callback to.
        callback : Callable
            Callback to register. If the custom arguments,
            args and kwargs, are empty then the callback
            signature must be precisely <function>(session, event_info).
            Otherwise, the arguments for args and/or kwargs
            must precede the other arguments in the signature.
        args : Any
            Arguments.
        kwargs : Any
            Keyword arguments.

        Returns
        -------
        str
            Registered callback ID.

        Raises
        ------
        InvalidArgument
            If event name is not valid.
        """
        cb_ids = []
        if not isinstance(event_types, (list, tuple)):
            event_types = (event_types,)

        for event in event_types:
            cb_ids.append(
                self._register_single_callback(event, callback, *args, **kwargs)
            )
        return cb_ids[0] if len(cb_ids) == 1 else cb_ids

    def unregister_callback(self, callback_id: str):
        """Unregister the callback.

        Parameters
        ----------
        callback_id : str
            ID of the registered callback.
        """
        with self._impl._lock:
            for callbacks_map in self._impl._service_callbacks.values():
                if callback_id in callbacks_map:
                    del callbacks_map[callback_id]
            sync_event_id = self._sync_event_ids.pop(callback_id, None)
            if sync_event_id:
                self._service.unregister_pause_on_solution_events(
                    registration_id=sync_event_id
                )

    def start(self, *args, **kwargs) -> None:
        """Start streaming."""
        self._impl.start(*args, **kwargs)

    def stop(self) -> None:
        """Stop streaming."""
        self._impl.stop()

    def _register_solution_event_sync_callback(
        self,
        event_type,
        callback_id: str,
        callback: Callable,
    ) -> tuple[TEvent, Callable]:
        unique_id: int = self._service.register_pause_on_solution_events(
            solution_event=event_type
        )

        def on_pause(session, event_info: SolutionPausedEventInfo):
            if unique_id == int(event_info.level):
                if event_type.name == "ITERATION_ENDED":
                    event_info = IterationEndedEventInfo(index=event_info.index)
                else:
                    event_info = TimestepEndedEventInfo(
                        # TODO: Timestep size is currently not available
                        index=event_info.index,
                        size=0,
                    )
                try:
                    callback(session, event_info)
                except Exception as e:
                    network_logger.error(
                        f"Error in callback for event {event_type}: {e}",
                        exc_info=True,
                    )
                finally:
                    self._service.resume_on_solution_event(registration_id=unique_id)

        self._sync_event_ids[callback_id] = unique_id
        return self._event_type.SOLUTION_PAUSED, on_pause
