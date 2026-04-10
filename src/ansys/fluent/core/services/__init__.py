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

from ansys.fluent.core.services.app_utilities import AppUtilities as AppUtilitiesV0
from ansys.fluent.core.services.app_utilities_v1 import AppUtilities
from ansys.fluent.core.services.batch_ops import BatchOpsService as BatchOpsServiceV0
from ansys.fluent.core.services.batch_ops_v1 import BatchOpsService
from ansys.fluent.core.services.datamodel_se import (
    DatamodelService as DatamodelService_SE,
)
from ansys.fluent.core.services.datamodel_tui import (
    DatamodelService as DatamodelService_TUI,
)
from ansys.fluent.core.services.deprecated_field_data import DeprecatedFieldData
from ansys.fluent.core.services.events import EventsService as EventsServiceV0
from ansys.fluent.core.services.events_v1 import EventsService
from ansys.fluent.core.services.field_data import LiveFieldData as LiveFieldDataV0
from ansys.fluent.core.services.field_data import _FieldInfo as _FieldInfoV0
from ansys.fluent.core.services.field_data_v1 import LiveFieldData, _FieldInfo
from ansys.fluent.core.services.health_check import (
    HealthCheckService as HealthCheckServiceV0,
)
from ansys.fluent.core.services.health_check_v1 import HealthCheckService
from ansys.fluent.core.services.monitor import MonitorsService
from ansys.fluent.core.services.reduction import Reduction as ReductionV0
from ansys.fluent.core.services.reduction_v1 import Reduction
from ansys.fluent.core.services.scheme_eval import SchemeEval as SchemeEvalV0
from ansys.fluent.core.services.scheme_eval_v1 import SchemeEval
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

_service_cls_by_name_v0 = {
    "app_utilities": AppUtilitiesV0,
    "health_check": HealthCheckServiceV0,
    "datamodel": DatamodelService_SE,
    "tui": DatamodelService_TUI,
    "settings": SettingsServiceV0,
    "scheme_eval": SchemeEvalV0,
    "events": EventsServiceV0,
    "field_data": LiveFieldDataV0,
    "field_data_old": DeprecatedFieldData,
    "field_info": _FieldInfoV0,
    "monitors": MonitorsService,
    "reduction": ReductionV0,
    "svar": SolutionVariableServiceV0,
    "svar_data": SolutionVariableDataV0,
    "transcript": TranscriptServiceV0,
    "batch_ops": BatchOpsServiceV0,
    "field_data_streaming": FieldDataStreamingV0,
}

_service_cls_by_name = {
    "app_utilities": AppUtilities,
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
