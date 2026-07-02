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
from ansys.fluent.core.services.events import EventsService as EventsServiceV0
from ansys.fluent.core.services.events_v1 import EventsService
from ansys.fluent.core.services.monitor import MonitorsService as MonitorsServiceV0
from ansys.fluent.core.services.monitor_v1 import MonitorsService as MonitorsService
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

__all__ = (
    "BatchOpsService",
    "BatchOps",
    "DatamodelService_SE",
    "DatamodelService_SE_V0",
    "DatamodelService_TUI",
    "DatamodelService_TUI_V0",
    "EventsService",
    "EventsServiceV0",
    "HealthCheckService",
    "HealthCheckServiceV0",
    "MonitorsService",
    "MonitorsServiceV0",
    "Reduction",
    "ReductionV0",
    "SchemeEvalService",
    "SchemeEvalServiceV0",
    "SolutionVariableData",
    "SolutionVariableDataV0",
    "SolutionVariableService",
    "SolutionVariableServiceV0",
    "TranscriptService",
    "TranscriptServiceV0",
    "service_creator",
)


_service_cls_by_name_v0 = {
    "datamodel": DatamodelService_SE_V0,
    "tui": DatamodelService_TUI_V0,
    "events": EventsServiceV0,
    "monitors": MonitorsServiceV0,
    "svar": SolutionVariableServiceV0,
    "svar_data": SolutionVariableDataV0,
    "transcript": TranscriptServiceV0,
    "batch_ops": BatchOpsService,
}

_service_cls_by_name = {
    "datamodel": DatamodelService_SE,
    "tui": DatamodelService_TUI,
    "events": EventsService,
    "monitors": MonitorsService,
    "svar": SolutionVariableService,
    "svar_data": SolutionVariableData,
    "transcript": TranscriptService,
    "batch_ops": BatchOpsService,
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
