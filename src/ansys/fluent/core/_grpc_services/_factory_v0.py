# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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

"""gRPC service factory for v0 proto (Fluent < 27R1)."""

from functools import cached_property

from ansys.fluent.core._grpc_services import GRPCServiceFactory
from ansys.fluent.core._grpc_services._chunk_parser import ChunkParserV0
from ansys.fluent.core._grpc_services.application_runtime_service_v0 import (
    ApplicationRuntimeService as ApplicationRuntimeServiceV0,
)
from ansys.fluent.core._grpc_services.events_service_v0 import (
    EventsService as EventsServiceV0,
)
from ansys.fluent.core._grpc_services.field_data_service_v0 import (
    FieldDataService as FieldDataServiceV0,
)
from ansys.fluent.core._grpc_services.health_check_service_v0 import (
    HealthCheckService as HealthCheckServiceV0,
)
from ansys.fluent.core._grpc_services.monitor_service_v0 import (
    MonitorService as MonitorServiceV0,
)
from ansys.fluent.core._grpc_services.object_model_service_v0 import (
    ObjectModelService as ObjectModelServiceV0,
)
from ansys.fluent.core._grpc_services.reduction_service_v0 import (
    ReductionService as ReductionServiceV0,
)
from ansys.fluent.core._grpc_services.scheme_interpreter_service_v0 import (
    SchemeInterpreterService as SchemeInterpreterServiceV0,
)
from ansys.fluent.core._grpc_services.settings_service_v0 import (
    SettingsService as SettingsServiceV0,
)
from ansys.fluent.core._grpc_services.solution_variable_service_v0 import (
    SolutionVariableService as SolutionVariableServiceV0,
)
from ansys.fluent.core._grpc_services.text_interface_service_v0 import (
    TextInterfaceService as TextInterfaceServiceV0,
)
from ansys.fluent.core._grpc_services.transcript_service_v0 import (
    TranscriptService as TranscriptServiceV0,
)


class GRPCServiceFactoryV0(GRPCServiceFactory):
    """Factory for v0 proto (Fluent < 27R1) gRPC service stubs."""

    @cached_property
    def scheme_interpreter(self) -> SchemeInterpreterServiceV0:
        """gRPC stub for Scheme expression evaluation."""
        return SchemeInterpreterServiceV0(
            intercept_channel=self._intercept_channel,
            metadata=self._metadata,
        )

    @cached_property
    def application_runtime(self) -> ApplicationRuntimeServiceV0:
        """gRPC stub for application runtime and product version queries."""
        return ApplicationRuntimeServiceV0(
            intercept_channel=self._intercept_channel,
            metadata=self._metadata,
        )

    @cached_property
    def health_check(self) -> HealthCheckServiceV0:
        """gRPC stub for server health/readiness checks."""
        return HealthCheckServiceV0(
            intercept_channel=self._intercept_channel,
            metadata=self._metadata,
        )

    @cached_property
    def reduction(self) -> ReductionServiceV0:
        """gRPC stub for data-reduction operations (forces, moments, etc.)."""
        return ReductionServiceV0(
            intercept_channel=self._intercept_channel,
            metadata=self._metadata,
        )

    @cached_property
    def settings(self) -> SettingsServiceV0:
        """gRPC stub for reading and writing solver settings."""
        return SettingsServiceV0(
            intercept_channel=self._intercept_channel,
            metadata=self._metadata,
        )

    @cached_property
    def field_data(self) -> FieldDataServiceV0:
        """gRPC stub for field data operations."""
        return FieldDataServiceV0(
            intercept_channel=self._intercept_channel,
            metadata=self._metadata,
        )

    @cached_property
    def _chunk_parser(self) -> type[ChunkParserV0]:
        """Chunk parser class for field data operations."""
        return ChunkParserV0

    @cached_property
    def object_model(self) -> ObjectModelServiceV0:
        """gRPC stub for object model operations."""
        return ObjectModelServiceV0(
            intercept_channel=self._intercept_channel,
            metadata=self._metadata,
        )

    @cached_property
    def events(self) -> EventsServiceV0:
        """gRPC stub for events operations."""
        return EventsServiceV0(
            channel=self._channel,
            metadata=self._metadata,
        )

    @cached_property
    def transcript(self) -> TranscriptServiceV0:
        """gRPC stub for transcript operations."""
        return TranscriptServiceV0(
            channel=self._channel,
            metadata=self._metadata,
        )

    @cached_property
    def text_interface(self) -> TextInterfaceServiceV0:
        """gRPC stub for text interface operations."""
        return TextInterfaceServiceV0(
            intercept_channel=self._intercept_channel,
            metadata=self._metadata,
        )

    @cached_property
    def monitor(self) -> MonitorServiceV0:
        """gRPC stub for monitor operations."""
        return MonitorServiceV0(
            intercept_channel=self._intercept_channel,
            metadata=self._metadata,
        )

    @cached_property
    def solution_variable(self) -> SolutionVariableServiceV0:
        """gRPC stub for solution variable operations."""
        return SolutionVariableServiceV0(
            intercept_channel=self._intercept_channel,
            metadata=self._metadata,
        )
