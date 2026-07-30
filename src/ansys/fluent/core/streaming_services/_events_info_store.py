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

"""Module for storing common events."""

from dataclasses import dataclass, field, fields
from enum import Enum
import warnings

from ansys.fluent.core.pyfluent_warnings import PyFluentDeprecationWarning


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

    TIMESTEP_STARTED = "timestep_started"
    TIMESTEP_ENDED = "timestep_ended"
    ITERATION_ENDED = "iteration_ended"
    CALCULATIONS_STARTED = "calculations_started"
    CALCULATIONS_ENDED = "calculations_ended"
    CALCULATIONS_PAUSED = "calculations_paused"
    CALCULATIONS_RESUMED = "calculations_resumed"
    ABOUT_TO_LOAD_CASE = "about_to_load_case"
    CASE_LOADED = "case_loaded"
    ABOUT_TO_LOAD_DATA = "about_to_load_data"
    DATA_LOADED = "data_loaded"
    ABOUT_TO_INITIALIZE_SOLUTION = "about_to_initialize_solution"
    SOLUTION_INITIALIZED = "solution_initialized"
    REPORT_DEFINITION_UPDATED = "report_definition_updated"
    REPORT_PLOT_SET_UPDATED = "report_plot_set_updated"
    RESIDUAL_PLOT_UPDATED = "residual_plot_updated"
    SETTINGS_CLEARED = "settings_cleared"
    SOLUTION_PAUSED = "solution_paused"
    PROGRESS_UPDATED = "progress_updated"
    SOLVER_TIME_ESTIMATE_UPDATED = "solver_time_estimate_updated"
    FATAL_ERROR = "fatal_error"

    @classmethod
    def _missing_(cls, value):
        return _missing_for_events(cls, value)


class MeshingEvent(Enum):
    """Enumerates over supported server (Fluent) events."""

    ABOUT_TO_LOAD_CASE = "about_to_load_case"
    CASE_LOADED = "case_loaded"
    SETTINGS_CLEARED = "settings_cleared"
    PROGRESS_UPDATED = "progress_updated"
    FATAL_ERROR = "fatal_error"

    @classmethod
    def _missing_(cls, value):
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
