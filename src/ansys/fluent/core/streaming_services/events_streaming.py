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

"""Module for events management."""

from dataclasses import dataclass, field, fields
from enum import Enum
from functools import partial
import inspect
import logging
from typing import Callable, Generic, Sequence, Type, TypeVar
import warnings

from google.protobuf.json_format import MessageToDict

from ansys.api.fluent.v0 import events_pb2 as EventsProtoModule
from ansys.fluent.core.exceptions import InvalidArgument
from ansys.fluent.core.pyfluent_warnings import PyFluentDeprecationWarning
from ansys.fluent.core.streaming_services.streaming import StreamingService

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

network_logger = logging.getLogger("pyfluent.networking")


def _missing_for_events(cls, value):
    # Top-level imports can expose the v0 or v1 event enums depending on how
    # the package was imported. Accept equivalent enum members from either
    # version by matching on the stable enum name first.
    if isinstance(value, Enum):
        for member in cls:
            if member.name == value.name:
                return member
        value = value.value
    # Fall back to value-based matching for string inputs and for cross-version
    # enum values whose wire names differ only by case or naming convention.
    for member in cls:
        if member.value.lower() == str(value).lower():
            return member
    raise ValueError(f"'{value}' is not a supported '{cls.__name__}'.")


class SolverEvent(Enum):
    """Enumerates over supported server (Fluent) events."""

    TIMESTEP_STARTED = "TimestepStartedEvent"
    TIMESTEP_ENDED = "TimestepEndedEvent"
    ITERATION_ENDED = "IterationEndedEvent"
    CALCULATIONS_STARTED = "CalculationsStartedEvent"
    CALCULATIONS_ENDED = "CalculationsEndedEvent"
    CALCULATIONS_PAUSED = "CalculationsPausedEvent"
    CALCULATIONS_RESUMED = "CalculationsResumedEvent"
    ABOUT_TO_LOAD_CASE = "AboutToReadCaseEvent"
    CASE_LOADED = "CaseReadEvent"
    ABOUT_TO_LOAD_DATA = "AboutToReadDataEvent"
    DATA_LOADED = "DataReadEvent"
    ABOUT_TO_INITIALIZE_SOLUTION = "AboutToInitializeEvent"
    SOLUTION_INITIALIZED = "InitializedEvent"
    REPORT_DEFINITION_UPDATED = "ReportDefinitionChangedEvent"
    REPORT_PLOT_SET_UPDATED = "PlotSetChangedEvent"
    RESIDUAL_PLOT_UPDATED = "ResidualPlotChangedEvent"
    SETTINGS_CLEARED = "ClearSettingsDoneEvent"
    SOLUTION_PAUSED = "AutoPauseEvent"
    PROGRESS_UPDATED = "ProgressEvent"
    SOLVER_TIME_ESTIMATE_UPDATED = "SolverTimeEstimateEvent"
    FATAL_ERROR = "ErrorEvent"

    @classmethod
    def _missing_(cls, value: str):
        return _missing_for_events(cls, value)


# alias for backward compatibility
Event = SolverEvent


class MeshingEvent(Enum):
    """Enumerates over supported server (Fluent) events."""

    ABOUT_TO_LOAD_CASE = "AboutToReadCaseEvent"
    CASE_LOADED = "CaseReadEvent"
    SETTINGS_CLEARED = "ClearSettingsDoneEvent"
    PROGRESS_UPDATED = "ProgressEvent"
    FATAL_ERROR = "ErrorEvent"

    @classmethod
    def _missing_(cls, value: str):
        return _missing_for_events(cls, value)


class EventInfoBase:
    """Base class for event information classes."""

    derived_classes = {}

    def __init_subclass__(cls, event, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.derived_classes[event.name] = cls

    def __post_init__(self):
        for f in fields(self):
            # Cast to the correct type
            setattr(self, f.name, f.type(getattr(self, f.name)))

    def __getattr__(self, name):
        for f in fields(self):
            if f.metadata.get("deprecated_name") == name:
                warnings.warn(
                    f"'{name}' is deprecated. Use '{f.name}' instead.",
                    PyFluentDeprecationWarning,
                )
                return getattr(self, f.name)
        return self.__getattribute__(name)


@dataclass
class TimestepStartedEventInfo(EventInfoBase, event=SolverEvent.TIMESTEP_STARTED):
    """Information about the event triggered when a timestep is started.

    Attributes
    ----------
    index : int
        Timestep index.
    size : float
        Timestep size.
    """

    index: int
    size: float


@dataclass
class TimestepEndedEventInfo(EventInfoBase, event=SolverEvent.TIMESTEP_ENDED):
    """Information about the event triggered when a timestep is ended.

    Attributes
    ----------
    index : int
        Timestep index.
    size : float
        Timestep size.
    """

    index: int
    size: float


@dataclass
class IterationEndedEventInfo(EventInfoBase, event=SolverEvent.ITERATION_ENDED):
    """Information about the event triggered when an iteration is ended.

    Attributes
    ----------
    index : int
        Iteration index.
    """

    index: int


class CalculationsStartedEventInfo(
    EventInfoBase, event=SolverEvent.CALCULATIONS_STARTED
):
    """Information about the event triggered when calculations are started."""


class CalculationsEndedEventInfo(EventInfoBase, event=SolverEvent.CALCULATIONS_ENDED):
    """Information about the event triggered when calculations are ended."""


class CalculationsPausedEventInfo(EventInfoBase, event=SolverEvent.CALCULATIONS_PAUSED):
    """Information about the event triggered when calculations are paused."""


class CalculationsResumedEventInfo(
    EventInfoBase, event=SolverEvent.CALCULATIONS_RESUMED
):
    """Information about the event triggered when calculations are resumed."""


@dataclass
class AboutToLoadCaseEventInfo(EventInfoBase, event=SolverEvent.ABOUT_TO_LOAD_CASE):
    """Information about the event triggered just before a case file is loaded.

    Attributes
    ----------
    case_file_name : str
        Case filename.
    """

    case_file_name: str = field(metadata=dict(deprecated_name="casefilepath"))


@dataclass
class CaseLoadedEventInfo(EventInfoBase, event=SolverEvent.CASE_LOADED):
    """Information about the event triggered after a case file is loaded.

    Attributes
    ----------
    case_file_name : str
        Case filename.
    """

    case_file_name: str = field(metadata=dict(deprecated_name="casefilepath"))


@dataclass
class AboutToLoadDataEventInfo(EventInfoBase, event=SolverEvent.ABOUT_TO_LOAD_DATA):
    """Information about the event triggered just before a data file is loaded.

    Attributes
    ----------
    data_file_name : str
        Data filename.
    """

    data_file_name: str = field(metadata=dict(deprecated_name="datafilepath"))


@dataclass
class DataLoadedEventInfo(EventInfoBase, event=SolverEvent.DATA_LOADED):
    """Information about the event triggered after a data file is loaded.

    Attributes
    ----------
    data_file_name : str
        Data filename.
    """

    data_file_name: str = field(metadata=dict(deprecated_name="datafilepath"))


class AboutToInitializeSolutionEventInfo(
    EventInfoBase, event=SolverEvent.ABOUT_TO_INITIALIZE_SOLUTION
):
    """Information about the event triggered just before solution is initialized."""


class SolutionInitializedEventInfo(
    EventInfoBase, event=SolverEvent.SOLUTION_INITIALIZED
):
    """Information about the event triggered after solution is initialized."""


@dataclass
class ReportDefinitionUpdatedEventInfo(
    EventInfoBase, event=SolverEvent.REPORT_DEFINITION_UPDATED
):
    """Information about the event triggered when a report definition is updated."""


@dataclass
class ReportPlotSetUpdatedEventInfo(
    EventInfoBase, event=SolverEvent.REPORT_PLOT_SET_UPDATED
):
    """Information about the event triggered when a report plot set is updated."""


class ResidualPlotUpdatedEventInfo(
    EventInfoBase, event=SolverEvent.RESIDUAL_PLOT_UPDATED
):
    """Information about the event triggered when residual plots are updated."""


class SettingsClearedEventInfo(EventInfoBase, event=SolverEvent.SETTINGS_CLEARED):
    """Information about the event triggered when settings are cleared."""


@dataclass
class SolutionPausedEventInfo(EventInfoBase, event=SolverEvent.SOLUTION_PAUSED):
    """Information about the event triggered when solution is paused.

    Attributes
    ----------
    level : str
        Level of the pause event.
    index : int
        Index of the pause event.
    """

    level: str
    index: int


@dataclass
class ProgressUpdatedEventInfo(EventInfoBase, event=SolverEvent.PROGRESS_UPDATED):
    """Information about the event triggered when progress is updated.

    Attributes
    ----------
    message : str
        Progress message.
    percentage : int
        Progress percentage.
    """

    message: str
    percentage: int = field(metadata=dict(deprecated_name="percentComplete"))


@dataclass
class SolverTimeEstimateUpdatedEventInfo(
    EventInfoBase, event=SolverEvent.SOLVER_TIME_ESTIMATE_UPDATED
):
    """Information about the event triggered when solver time estimate is updated.

    Attributes
    ----------
    hours : float
        Hours of solver time estimate.
    minutes : float
        Minutes of solver time estimate.
    seconds : float
        Seconds of solver time estimate.
    """

    hours: float
    minutes: float
    seconds: float


@dataclass
class FatalErrorEventInfo(EventInfoBase, event=SolverEvent.FATAL_ERROR):
    """Information about the event triggered when a fatal error occurs.

    Attributes
    ----------
    message : str
        Error message.
    error_code : int
        Error code.
    """

    message: str
    error_code: int = field(metadata=dict(deprecated_name="errorCode"))


TEvent = TypeVar("TEvent")


class EventsManager(Generic[TEvent]):
    """Manages server-side events.

    This class allows the client to register and unregister callbacks with server
    events.
    """

    def __init__(
        self,
        event_type: Type[TEvent],
        session_events_service,
        fluent_error_state,
        session,
        server_supports_v1: bool = False,
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
        self._server_supports_v1 = server_supports_v1
        self._sync_event_ids = {}

    def _construct_event_info(
        self, response: EventsProtoModule.BeginStreamingResponse, event: TEvent
    ):
        event_info_msg = getattr(response, event.value.lower())
        # Note: MessageToDict's parameter names are different in different protobuf versions
        event_info_dict = MessageToDict(event_info_msg, True)
        event_info_cls = EventInfoBase.derived_classes.get(event.name)
        # Some event-info classes intentionally have no fields. Instantiate them without payload.
        dataclass_fields = getattr(event_info_cls, "__dataclass_fields__", None)
        if dataclass_fields is None or len(dataclass_fields) == 0:
            return event_info_cls()
        # v1 servers can emit empty payloads for some events; keep fallback v1-only
        # to avoid changing backward-compatible v0 behavior.
        if self._server_supports_v1 and not event_info_dict:
            return event_info_cls()
        # Key names can be different, but their order is the same
        return event_info_cls(*event_info_dict.values())

    def _process_streaming(
        self, service, id, stream_begin_method, started_evt, *args, **kwargs
    ):
        request = EventsProtoModule.BeginStreamingRequest(*args, **kwargs)
        responses = service._streaming_service.begin_streaming(
            request, started_evt, id=id, stream_begin_method=stream_begin_method
        )
        while True:
            try:
                response = next(responses)
                event_name = self._event_type(response.WhichOneof("as"))
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
                self._session._app_utilities.unregister_pause_on_solution_events(
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
        unique_id: int = self._session._app_utilities.register_pause_on_solution_events(
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
                    session._app_utilities.resume_on_solution_event(
                        registration_id=unique_id
                    )

        self._sync_event_ids[callback_id] = unique_id
        return self._event_type.SOLUTION_PAUSED, on_pause
