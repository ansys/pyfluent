"""Module for events management."""

from enum import Enum
from functools import partial
import inspect
import logging
from typing import Callable, Generic, Type, TypeVar
import warnings

from ansys.api.fluent.v0 import events_pb2 as EventsProtoModule
from ansys.fluent.core.exceptions import InvalidArgument
from ansys.fluent.core.streaming_services.streaming import StreamingService
from ansys.fluent.core.warnings import PyFluentDeprecationWarning

network_logger = logging.getLogger("pyfluent.networking")


def _missing_for_events(cls, value):
    for member in cls:
        if member.value.lower() == value:
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
                with service._lock:
                    service._streaming = True
                    # error-code 0 from Fluent indicates server running without error
                    if (
                        event_name == self._event_type.FATAL_ERROR
                        and response.errorevent.errorCode != 0
                    ):
                        error_message = response.errorevent.message.rstrip()
                        network_logger.error(
                            f"gRPC - {error_message}, "
                            f"errorCode {response.errorevent.errorCode}"
                        )
                        self._fluent_error_state.set("fatal", error_message)
                        continue
                    callbacks_map = self._impl._service_callbacks.get(event_name, {})
                    for callback in callbacks_map.values():
                        callback(
                            session=self._session,
                            event_info=getattr(response, event_name.value.lower()),
                        )
            except StopIteration:
                break

    @staticmethod
    def _make_callback_to_call(callback: Callable, args, kwargs):
        old_style = "session_id" in inspect.signature(callback).parameters
        if old_style:
            warnings.warn(
                "Update event callback function signatures"
                " substituting 'session' for 'session_id'.",
                PyFluentDeprecationWarning,
            )
        fn = partial(callback, *args, **kwargs)
        return (
            (
                lambda session, event_info: fn(
                    session_id=session.id, event_info=event_info
                )
            )
            if old_style
            else fn
        )

    def register_callback(
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
            callbacks_map = self._impl._service_callbacks.get(event_name)
            callback_to_call = EventsManager._make_callback_to_call(
                callback, args, kwargs
            )
            if callbacks_map:
                callbacks_map.update({callback_id: callback_to_call})
            else:
                self._impl._service_callbacks[event_name] = {
                    callback_id: callback_to_call
                }

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

    def start(self, *args, **kwargs) -> None:
        """Start streaming."""
        self._impl.start(*args, **kwargs)

    def stop(self) -> None:
        """Stop streaming."""
        self._impl.stop()
