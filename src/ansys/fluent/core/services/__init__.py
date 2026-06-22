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

from ansys.fluent.core.application_runtime import (
    ApplicationRuntime,
    ApplicationRuntimeOld,
    ApplicationRuntimeV0,
    ApplicationRuntimeV252,
    BuildInfo,
    ProcessInfo,
)
from ansys.fluent.core.services.application_runtime import (
    ApplicationRuntimeService,
    ApplicationRuntimeServiceV0,
)

# Backward-compat aliases: callers that import AppUtilities* from services
# continue to work without changes.
AppUtilities = ApplicationRuntime
AppUtilitiesV0 = ApplicationRuntimeV0
AppUtilitiesOld = ApplicationRuntimeOld
from ansys.fluent.core.services.batch_ops import BatchOps, BatchOpsService
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
    "ApplicationRuntime",
    "ApplicationRuntimeOld",
    "ApplicationRuntimeV0",
    "ApplicationRuntimeV252",
    "BuildInfo",
    "ProcessInfo",
    # Backward-compat aliases
    "AppUtilities",
    "AppUtilitiesOld",
    "AppUtilitiesV0",
    "ApplicationRuntimeService",
    "ApplicationRuntimeServiceV0",
    "BatchOpsService",
    "BatchOps",
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
    "service_creator",
)


_service_cls_by_name_v0 = {
    "app_utilities": ApplicationRuntimeV0,
    "health_check": HealthCheckServiceV0,
    "datamodel": DatamodelService_SE_V0,
    "tui": DatamodelService_TUI_V0,
    "settings": SettingsServiceV0,
    "scheme_eval": SchemeEvalV0,
    "events": EventsServiceV0,
    "field_data": LiveFieldDataV0,
    "field_data_old": DeprecatedFieldData,
    "field_info": _FieldInfoV0,
    "monitors": MonitorsServiceV0,
    "reduction": ReductionV0,
    "svar": SolutionVariableServiceV0,
    "svar_data": SolutionVariableDataV0,
    "transcript": TranscriptServiceV0,
    "batch_ops": BatchOpsService,
    "field_data_streaming": FieldDataStreamingV0,
}

_service_cls_by_name = {
    "app_utilities": ApplicationRuntime,
    "health_check": HealthCheckService,
    "datamodel": DatamodelService_SE,
    "tui": DatamodelService_TUI,
    "settings": SettingsService,
    "scheme_eval": SchemeEval,
    "events": EventsService,
    "field_data": LiveFieldData,
    "field_data_old": DeprecatedFieldData,
    "field_info": _FieldInfo,
    "monitors": MonitorsService,
    "reduction": Reduction,
    "svar": SolutionVariableService,
    "svar_data": SolutionVariableData,
    "transcript": TranscriptService,
    "batch_ops": BatchOpsService,
    "field_data_streaming": FieldDataStreaming,
}


# This class is swapped in Fluent Python Console
class service_creator:
    """A gRPC service creator."""

    def __init__(self, service_name: str, supports_v1: bool | None = None):
        """Initialize service_creator."""
        if supports_v1:
            self._service_cls = _service_cls_by_name[service_name]
        else:
            self._service_cls = _service_cls_by_name_v0[service_name]

    def create(self, *args, **kwargs):
        """Create a gRPC service."""
        return self._service_cls(*args, **kwargs)
