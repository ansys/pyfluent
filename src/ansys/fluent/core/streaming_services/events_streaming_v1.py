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

"""Module for events management (v1 proto API).

All shared logic lives in events_streaming.py (v0). This module keeps only
v1-specific event enum values required for compatibility.
"""

from enum import Enum

import ansys.fluent.core.streaming_services.events_streaming as _v0

__all__ = _v0.__all__

_missing_for_events = _v0._missing_for_events
EventsManager = _v0.EventsManager
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
