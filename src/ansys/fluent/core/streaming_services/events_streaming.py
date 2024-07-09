"""Module for events management."""

from enum import Enum
from functools import partial
import logging
from typing import Callable, Union

from ansys.api.fluent.v0 import events_pb2 as EventsProtoModule
from ansys.fluent.core.exceptions import InvalidArgument
from ansys.fluent.core.streaming_services.streaming import StreamingService

network_logger = logging.getLogger("pyfluent.networking")


class Event(Enum):
    """Enumerates over supported server (Fluent) events."""

    TIMESTEP_STARTED = "TimestepStartedEvent"
    TIMESTEP_ENDED = "TimestepEndedEvent"
    ITERATION_STARTED = "IterationStartedEvent"
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
        for member in cls:
            if member.value.lower() == value:
                return member
        raise ValueError(f"'{value}' is not a supported 'Event'.")


class EventsManager(StreamingService):
    """Manages server-side events.

    This class allows the client to register and unregister callbacks with server
    events.
    """

    def __init__(self, session_events_service, fluent_error_state, session):
        """__init__ method of EventsManager class."""
        super().__init__(
            stream_begin_method="BeginStreaming",
            target=EventsManager._process_streaming,
            streaming_service=session_events_service,
        )
        self._fluent_error_state = fluent_error_state
        # This has been updated from id to session, which
        # can also be done in other streaming services
        self._session = session

    def _process_streaming(self, id, stream_begin_method, started_evt, *args, **kwargs):
        request = EventsProtoModule.BeginStreamingRequest(*args, **kwargs)
        responses = self._streaming_service.begin_streaming(
            request, started_evt, id=id, stream_begin_method=stream_begin_method
        )
        while True:
            try:
                response = next(responses)
                event_name = Event(response.WhichOneof("as"))
                with self._lock:
                    self._streaming = True
                    # error-code 0 from Fluent indicates server running without error
                    if (
                        event_name == Event.FATAL_ERROR
                        and response.errorevent.errorCode != 0
                    ):
                        error_message = response.errorevent.message.rstrip()
                        network_logger.error(
                            f"gRPC - {error_message}, "
                            f"errorCode {response.errorevent.errorCode}"
                        )
                        self._fluent_error_state.set("fatal", error_message)
                        continue
                    callbacks_map = self._service_callbacks.get(event_name, {})
                    for callback in callbacks_map.values():
                        callback(
                            session=self._session,
                            event_info=getattr(response, event_name.value.lower()),
                        )
            except StopIteration:
                break

    @staticmethod
    def _make_callback_to_call(
        callback: Callable, callback_has_new_signature: bool, *args, **kwargs
    ):
        fn = partial(callback, *args, **kwargs)
        return (
            fn
            if callback_has_new_signature
            else lambda session, event_info: fn(
                session_id=session.id, event_info=event_info
            )
        )

    def register_callback(
        self,
        event_name: Union[Event, str],
        callback: Callable,
        callback_has_new_signature: bool = False,
        *args,
        **kwargs,
    ):
        """Register the callback.

        Parameters
        ----------
        event_name : Event or str
            Event to register the callback to.
        callback : Callable
            Callback to register.
        callback_has_new_signature: bool
            Whether the callback has the new
            style signature, where a session object rather than
            a session ID string is passed as the first callback
            argument.
            New style is:
              ``callback(session: object, event_info: object)``
            Old style is:
              ``callback(session_id: str, event_info: object)``
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

        event_name = Event(event_name)
        with self._lock:
            callback_id = f"{event_name}-{next(self._service_callback_id)}"
            callbacks_map = self._service_callbacks.get(event_name)
            callback_to_call = EventsManager._make_callback_to_call(
                callback, callback_has_new_signature, *args, **kwargs
            )
            if callbacks_map:
                callbacks_map.update({callback_id: callback_to_call})
            else:
                self._service_callbacks[event_name] = {callback_id: callback_to_call}

    def unregister_callback(self, callback_id: str):
        """Unregister the callback.

        Parameters
        ----------
        callback_id : str
            ID of the registered callback.
        """
        with self._lock:
            for callbacks_map in self._service_callbacks.values():
                if callback_id in callbacks_map:
                    del callbacks_map[callback_id]
