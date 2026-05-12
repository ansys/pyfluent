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

"""Provides a module to create gRPC services."""

from ansys.fluent.core.services.app_utilities import (
    AppUtilitiesService as AppUtilitiesServiceV0,
)
from ansys.fluent.core.services.app_utilities import AppUtilities as AppUtilitiesV0
from ansys.fluent.core.services.app_utilities_v1 import (
    AppUtilities,
    AppUtilitiesService,
)
from ansys.fluent.core.services.batch_ops import BatchOps as BatchOpsV0
from ansys.fluent.core.services.batch_ops import BatchOpsService as BatchOpsServiceV0
from ansys.fluent.core.services.datamodel_se import (
    DatamodelService as DatamodelService_SE_V0,
)
from ansys.fluent.core.services.datamodel_se_v1 import (
    DatamodelService as DatamodelService_SE,
)
from ansys.fluent.core.services.datamodel_tui import (
    DatamodelService as DatamodelService_TUI_V0,
)
from ansys.fluent.core.services.datamodel_tui_v1 import (
    DatamodelService as DatamodelService_TUI,
)
from ansys.fluent.core.services.deprecated_field_data import (
    DeprecatedFieldData as DeprecatedFieldDataV0,
)
from ansys.fluent.core.services.deprecated_field_data import DeprecatedFieldData
from ansys.fluent.core.services.events import EventsService as EventsServiceV0
from ansys.fluent.core.services.events_v1 import EventsService
from ansys.fluent.core.services.field_data import (
    ZoneInfo,
)
from ansys.fluent.core.services.field_data import FieldDataService as FieldDataServiceV0
from ansys.fluent.core.services.field_data import LiveFieldData as LiveFieldDataV0
from ansys.fluent.core.services.field_data import _FieldInfo as _FieldInfoV0
from ansys.fluent.core.services.field_data_v1 import (
    FieldDataService,
    LiveFieldData,
    _FieldInfo,
)
from ansys.fluent.core.services.health_check import (
    HealthCheckService as HealthCheckServiceV0,
)
from ansys.fluent.core.services.health_check_v1 import HealthCheckService
from ansys.fluent.core.services.monitor import MonitorsService as MonitorsServiceV0
from ansys.fluent.core.services.monitor_v1 import MonitorsService as MonitorsService
from ansys.fluent.core.services.reduction import Reduction as ReductionV0
from ansys.fluent.core.services.reduction_v1 import Reduction
from ansys.fluent.core.services.scheme_eval import (
    SchemeEvalService as SchemeEvalServiceV0,
)
from ansys.fluent.core.services.scheme_eval import SchemeEval as SchemeEvalV0
from ansys.fluent.core.services.scheme_eval_v1 import SchemeEval, SchemeEvalService
from ansys.fluent.core.services.settings import SettingsService as SettingsServiceV0
from ansys.fluent.core.services.settings_v1 import SettingsService
from ansys.fluent.core.services.solution_variables import (
    SolutionVariableData as SolutionVariableDataV0,
)
from ansys.fluent.core.services.solution_variables import (
    SolutionVariableService as SolutionVariableServiceV0,
)
from ansys.fluent.core.services.solution_variables_v1 import (
    SolutionVariableData,
    SolutionVariableService,
)
from ansys.fluent.core.services.transcript import (
    TranscriptService as TranscriptServiceV0,
)
from ansys.fluent.core.services.transcript_v1 import TranscriptService
from ansys.fluent.core.streaming_services.field_data_streaming import (
    FieldDataStreaming as FieldDataStreamingV0,
)
from ansys.fluent.core.streaming_services.field_data_streaming_v1 import (
    FieldDataStreaming,
)

__all__ = (
    "AppUtilities",
    "AppUtilitiesV0",
    "AppUtilitiesService",
    "AppUtilitiesServiceV0",
    "BatchOpsService",
    "BatchOps",
    "BatchOpsServiceV0",
    "BatchOpsV0",
    "DatamodelService_SE",
    "DatamodelService_SE_V0",
    "DatamodelService_TUI",
    "DatamodelService_TUI_V0",
    "DeprecatedFieldData",
    "DeprecatedFieldDataV0",
    "EventsService",
    "EventsServiceV0",
    "FieldDataService",
    "FieldDataServiceV0",
    "FieldDataStreaming",
    "FieldDataStreamingV0",
    "HealthCheckService",
    "HealthCheckServiceV0",
    "LiveFieldData",
    "LiveFieldDataV0",
    "MonitorsService",
    "MonitorsServiceV0",
    "Reduction",
    "ReductionV0",
    "SchemeEval",
    "SchemeEvalService",
    "SchemeEvalServiceV0",
    "SchemeEvalV0",
    "SettingsService",
    "SettingsServiceV0",
    "SolutionVariableData",
    "SolutionVariableDataV0",
    "SolutionVariableService",
    "SolutionVariableServiceV0",
    "TranscriptService",
    "TranscriptServiceV0",
    "_FieldInfo",
    "_FieldInfoV0",
    "ZoneInfo",
)
