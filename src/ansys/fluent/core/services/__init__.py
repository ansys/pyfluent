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

"""Provides a module to create gRPC services."""

from ansys.fluent.core.services.batch_ops import BatchOps, BatchOpsService
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
from ansys.fluent.core.utils.fluent_version import FluentVersion

__all__ = (
    "BatchOpsService",
    "BatchOps",
    "DatamodelService_TUI",
    "DatamodelService_TUI_V0",
    "EventsService",
    "EventsServiceV0",
    "MonitorsService",
    "MonitorsServiceV0",
    "SolutionVariableData",
    "SolutionVariableDataV0",
    "SolutionVariableService",
    "SolutionVariableServiceV0",
    "TranscriptService",
    "TranscriptServiceV0",
    "service_creator",
)


_service_cls_by_name_v0 = {
    "tui": DatamodelService_TUI_V0,
    "events": EventsServiceV0,
    "monitors": MonitorsServiceV0,
    "svar": SolutionVariableServiceV0,
    "svar_data": SolutionVariableDataV0,
    "transcript": TranscriptServiceV0,
    "batch_ops": BatchOpsService,
}

_service_cls_by_name = {
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


"""Provides a module to create gRPC services."""

from functools import cached_property

from ansys.fluent.core.services.application_runtime import (
    ApplicationRuntime,
    ApplicationRuntimeOld,
    ApplicationRuntimeV252,
    ApplicationRuntimeV261,
)
from ansys.fluent.core.services.field_data import (
    FieldData,
    FieldDataV251,
    FieldDataV261,
)
from ansys.fluent.core.services.health_check import HealthCheck
from ansys.fluent.core.services.object_model import ObjectModel, ObjectModelV261
from ansys.fluent.core.services.reduction import Reduction
from ansys.fluent.core.services.scheme_interpreter import SchemeInterpreter
from ansys.fluent.core.services.settings import Settings, SettingsV251, SettingsV261
from ansys.fluent.core.streaming_services.field_data_streaming import (
    FieldDataStreaming,
    FieldDataStreamingV261,
)


class ServiceFactory:
    """Wraps raw gRPC stubs from ``GRPCServiceFactory`` in version-appropriate high-level service objects.

    Reads the connected server's ``product_version`` once and uses it to
    select the correct concrete wrapper (e.g. ``Settings`` vs ``SettingsV261``)
    for every service property.  All properties are ``cached_property``.

    Parameters
    ----------
    service_factory : GRPCServiceFactory
        Source of the underlying raw gRPC stubs.
    product_version : FluentVersion, optional
        Fluent product version.  Derived from ``service_factory.scheme_interpreter``
        when omitted.
    """

    def __init__(self, service_factory, product_version: FluentVersion = None):
        """Initialize ServiceFactory."""
        self._service_factory = service_factory
        self._product_version = product_version or FluentVersion(
            self.scheme_interpreter.version
        )

    @cached_property
    def scheme_interpreter(self) -> SchemeInterpreter:
        """Scheme expression evaluator."""
        return SchemeInterpreter(self._service_factory.scheme_interpreter)

    @cached_property
    def application_runtime(self):
        """Application runtime, version and session lifecycle service."""
        match self._product_version:
            case v if v >= FluentVersion.v271:
                return ApplicationRuntime(self._service_factory.application_runtime)
            case FluentVersion.v261:
                return ApplicationRuntimeV261(self._service_factory.application_runtime)
            case FluentVersion.v252:
                return ApplicationRuntimeV252(
                    self._service_factory.application_runtime,
                    self._service_factory.scheme_interpreter,
                )
            case _:
                return ApplicationRuntimeOld(self._service_factory.scheme_interpreter)

    @cached_property
    def health_check(self):
        """Server health and readiness service."""
        return HealthCheck(self._service_factory.health_check)

    @cached_property
    def reduction(self):
        """Data-reduction service (forces, moments, etc.)."""
        return Reduction(self._service_factory.reduction)

    @cached_property
    def settings(self):
        """Solver settings service."""
        match self._product_version:
            case v if v >= FluentVersion.v271:
                return Settings(self._service_factory.settings)
            case v if v >= FluentVersion.v252 and v < FluentVersion.v271:
                return SettingsV261(
                    self._service_factory.settings,
                    self._service_factory.application_runtime,
                    self._service_factory.scheme_interpreter,
                )
            case _:
                return SettingsV251(
                    self._service_factory.settings,
                    self._service_factory.scheme_interpreter,
                )

    @cached_property
    def field_data(self):
        """Field data service."""
        match self._product_version:
            case v if v >= FluentVersion.v271:
                return FieldData(
                    self._service_factory.field_data,
                    self._service_factory._chunk_parser(),
                )
            case v if v >= FluentVersion.v252 and v < FluentVersion.v271:
                return FieldDataV261(
                    self._service_factory.field_data,
                    self._service_factory._chunk_parser(),
                    self._service_factory.application_runtime,
                )
            case _:
                return FieldDataV251(
                    self._service_factory.field_data,
                    self._service_factory._chunk_parser(),
                    self._service_factory.scheme_interpreter,
                )

    @cached_property
    def field_data_streaming(self):
        """Field data service."""
        if self._product_version >= FluentVersion.v271:
            return FieldDataStreaming(
                self._service_factory.field_data,
                self._service_factory._chunk_parser,
            )
        else:
            return FieldDataStreamingV261(
                self._service_factory.field_data,
                self._service_factory._chunk_parser,
            )

    @cached_property
    def object_model(self):
        """Object model service."""
        if self._product_version >= FluentVersion.v271:
            return ObjectModel(
                self._service_factory.object_model,
                self._service_factory.scheme_interpreter,
            )
        else:
            return ObjectModelV261(
                self._service_factory.object_model,
                self._service_factory.scheme_interpreter,
            )
