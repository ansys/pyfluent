# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
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

from ansys.fluent.core.services.app_utilities import AppUtilities
from ansys.fluent.core.services.batch_ops import BatchOpsService
from ansys.fluent.core.services.datamodel_se import (
    DatamodelService as DatamodelService_SE,
)
from ansys.fluent.core.services.datamodel_tui import (
    DatamodelService as DatamodelService_TUI,
)
from ansys.fluent.core.services.deprecated_field_data import DeprecatedFieldData
from ansys.fluent.core.services.events import EventsService
from ansys.fluent.core.services.field_data import FieldInfo, LiveFieldData
from ansys.fluent.core.services.health_check import HealthCheckService
from ansys.fluent.core.services.monitor import MonitorsService
from ansys.fluent.core.services.reduction import Reduction
from ansys.fluent.core.services.scheme_eval import SchemeEval
from ansys.fluent.core.services.settings import SettingsService
from ansys.fluent.core.services.solution_variables import (
    SolutionVariableData,
    SolutionVariableService,
)
from ansys.fluent.core.services.transcript import TranscriptService

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
    "field_info": FieldInfo,
    "monitors": MonitorsService,
    "reduction": Reduction,
    "svar": SolutionVariableService,
    "svar_data": SolutionVariableData,
    "transcript": TranscriptService,
    "batch_ops": BatchOpsService,
}


class service_creator:
    """A gRPC service creator."""

    def __init__(self, service_name: str):
        """Initialize service_creator."""
        self._service_cls = _service_cls_by_name[service_name]

    def create(self, *args, **kwargs):
        """Create a gRPC service."""
        return self._service_cls(*args, **kwargs)
