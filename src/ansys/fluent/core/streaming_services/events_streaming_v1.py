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

"""Module for events management (v1 proto API).

All shared logic lives in events_streaming.py (v0). This module keeps only
v1-specific event enum values required for compatibility.
"""

from enum import Enum

import ansys.fluent.core.streaming_services.events_streaming as _v0

__all__ = _v0.__all__

_missing_for_events = _v0._missing_for_events
EventInfoBase = _v0.EventInfoBase
TimestepStartedEventInfo = _v0.TimestepStartedEventInfo
TimestepEndedEventInfo = _v0.TimestepEndedEventInfo
IterationEndedEventInfo = _v0.IterationEndedEventInfo
CalculationsStartedEventInfo = _v0.CalculationsStartedEventInfo
CalculationsEndedEventInfo = _v0.CalculationsEndedEventInfo
CalculationsPausedEventInfo = _v0.CalculationsPausedEventInfo
CalculationsResumedEventInfo = _v0.CalculationsResumedEventInfo
AboutToLoadCaseEventInfo = _v0.AboutToLoadCaseEventInfo
CaseLoadedEventInfo = _v0.CaseLoadedEventInfo
AboutToLoadDataEventInfo = _v0.AboutToLoadDataEventInfo
DataLoadedEventInfo = _v0.DataLoadedEventInfo
AboutToInitializeSolutionEventInfo = _v0.AboutToInitializeSolutionEventInfo
SolutionInitializedEventInfo = _v0.SolutionInitializedEventInfo
ReportDefinitionUpdatedEventInfo = _v0.ReportDefinitionUpdatedEventInfo
ReportPlotSetUpdatedEventInfo = _v0.ReportPlotSetUpdatedEventInfo
ResidualPlotUpdatedEventInfo = _v0.ResidualPlotUpdatedEventInfo
SettingsClearedEventInfo = _v0.SettingsClearedEventInfo
SolutionPausedEventInfo = _v0.SolutionPausedEventInfo
ProgressUpdatedEventInfo = _v0.ProgressUpdatedEventInfo
SolverTimeEstimateUpdatedEventInfo = _v0.SolverTimeEstimateUpdatedEventInfo
FatalErrorEventInfo = _v0.FatalErrorEventInfo
network_logger = _v0.network_logger


class SolverEvent(Enum):
    """Enumerates over supported server (Fluent) events."""

    TIMESTEP_STARTED = "timestep_started_event"
    TIMESTEP_ENDED = "timestep_ended_event"
    ITERATION_ENDED = "iteration_ended_event"
    CALCULATIONS_STARTED = "calculations_started_event"
    CALCULATIONS_ENDED = "calculations_ended_event"
    CALCULATIONS_PAUSED = "calculations_paused_event"
    CALCULATIONS_RESUMED = "calculations_resumed_event"
    ABOUT_TO_LOAD_CASE = "pre_read_case_event"
    CASE_LOADED = "case_read_event"
    ABOUT_TO_LOAD_DATA = "pre_read_data_event"
    DATA_LOADED = "data_read_event"
    ABOUT_TO_INITIALIZE_SOLUTION = "pre_initialize_event"
    SOLUTION_INITIALIZED = "initialized_event"
    REPORT_DEFINITION_UPDATED = "report_definition_changed_event"
    REPORT_PLOT_SET_UPDATED = "plot_set_changed_event"
    RESIDUAL_PLOT_UPDATED = "residual_plot_changed_event"
    SETTINGS_CLEARED = "clear_settings_done_event"
    SOLUTION_PAUSED = "auto_pause_event"
    PROGRESS_UPDATED = "progress_event"
    SOLVER_TIME_ESTIMATE_UPDATED = "solver_time_estimate_event"
    FATAL_ERROR = "error_event"

    @classmethod
    def _missing_(cls, value: str):
        return _missing_for_events(cls, value)


Event = SolverEvent


class MeshingEvent(Enum):
    """Enumerates over supported server (Fluent) events."""

    ABOUT_TO_LOAD_CASE = "pre_read_case_event"
    CASE_LOADED = "case_read_event"
    SETTINGS_CLEARED = "clear_settings_done_event"
    PROGRESS_UPDATED = "progress_event"
    FATAL_ERROR = "error_event"

    @classmethod
    def _missing_(cls, value: str):
        return _missing_for_events(cls, value)


class EventsManager(_v0.EventsManager, _v0.Generic[_v0.TEvent]):
    """Manages server-side events.

    This class allows the client to register and unregister callbacks with server
    events.
    """

    def __init__(
        self,
        event_type: type[_v0.TEvent],
        session_events_service,
        fluent_error_state,
        session,
    ):
        """__init__ method of EventsManager class."""
        super().__init__(
            event_type,
            session_events_service,
            fluent_error_state,
            session,
        )
        self._service = session_events_service

    def _construct_event_info(
        self, response: _v0.EventsProtoModule.BeginStreamingResponse, event: _v0.TEvent
    ):
        event_info_msg = getattr(response, event.value.lower())
        # Note: MessageToDict's parameter names are different in different protobuf versions
        event_info_dict = _v0.MessageToDict(event_info_msg, True)
        event_info_cls = EventInfoBase.derived_classes.get(event.name)
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

    def _register_solution_event_sync_callback(
        self,
        event_type,
        callback_id: str,
        callback: _v0.Callable,
    ) -> tuple[_v0.TEvent, _v0.Callable]:
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
