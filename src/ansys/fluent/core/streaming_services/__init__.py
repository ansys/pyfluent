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

"""Provide streaming access to Fluent events, data, monitors, and transcripts.

The package includes common streaming-service support for registering callbacks
and specialized streams for datamodel updates, field data, monitor values,
server events, and transcript output. Event enums and event-info classes are
also provided for identifying and handling Fluent notifications.
"""

from .datamodel_event_streaming import DatamodelEvents
from .datamodel_streaming import DatamodelStream
from .events_streaming import (
    AboutToInitializeSolutionEventInfo,
    AboutToLoadCaseEventInfo,
    AboutToLoadDataEventInfo,
    CalculationsEndedEventInfo,
    CalculationsPausedEventInfo,
    CalculationsResumedEventInfo,
    CalculationsStartedEventInfo,
    CaseLoadedEventInfo,
    DataLoadedEventInfo,
    Event,
    EventsManager,
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
from .field_data_streaming import FieldDataStreaming
from .monitor_streaming import MonitorsManager
from .streaming import StreamingService
from .transcript_streaming import AppendToFile, Transcript

__all__ = [
    "StreamingService",
    "DatamodelEvents",
    "DatamodelStream",
    "FieldDataStreaming",
    "MonitorsManager",
    "Transcript",
    "AppendToFile",
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
