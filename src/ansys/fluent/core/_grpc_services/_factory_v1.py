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

"""gRPC service factory for v1 proto (Fluent >= 27R1)."""

from functools import cached_property

from ansys.fluent.core._grpc_services import GRPCServiceFactory
from ansys.fluent.core._grpc_services._chunk_parser import ChunkParser
from ansys.fluent.core._grpc_services.application_runtime_service import (
    ApplicationRuntimeService,
)
from ansys.fluent.core._grpc_services.events_service import EventsService
from ansys.fluent.core._grpc_services.field_data_service import FieldDataService
from ansys.fluent.core._grpc_services.health_check_service import HealthCheckService
from ansys.fluent.core._grpc_services.monitor_service import MonitorService
from ansys.fluent.core._grpc_services.object_model_service import ObjectModelService
from ansys.fluent.core._grpc_services.reduction_service import ReductionService
from ansys.fluent.core._grpc_services.scheme_interpreter_service import (
    SchemeInterpreterService,
)
from ansys.fluent.core._grpc_services.settings_service import SettingsService
from ansys.fluent.core._grpc_services.solution_variable_service import (
    SolutionVariableService,
)
from ansys.fluent.core._grpc_services.text_interface_service import TextInterfaceService
from ansys.fluent.core._grpc_services.transcript_service import TranscriptService


class GRPCServiceFactoryV1(GRPCServiceFactory):
    """Factory for v1 proto (Fluent >= 27R1) gRPC service stubs."""

    @cached_property
    def scheme_interpreter(self) -> SchemeInterpreterService:
        """gRPC stub for Scheme expression evaluation."""
        return SchemeInterpreterService(
            intercept_channel=self._intercept_channel,
            metadata=self._metadata,
        )

    @cached_property
    def application_runtime(self) -> ApplicationRuntimeService:
        """gRPC stub for application runtime and product version queries."""
        return ApplicationRuntimeService(
            intercept_channel=self._intercept_channel,
            metadata=self._metadata,
        )

    @cached_property
    def health_check(self) -> HealthCheckService:
        """gRPC stub for server health/readiness checks."""
        return HealthCheckService(
            intercept_channel=self._intercept_channel,
            metadata=self._metadata,
        )

    @cached_property
    def reduction(self) -> ReductionService:
        """gRPC stub for data-reduction operations (forces, moments, etc.)."""
        return ReductionService(
            intercept_channel=self._intercept_channel,
            metadata=self._metadata,
        )

    @cached_property
    def settings(self) -> SettingsService:
        """gRPC stub for reading and writing solver settings."""
        return SettingsService(
            intercept_channel=self._intercept_channel,
            metadata=self._metadata,
        )

    @cached_property
    def field_data(self) -> FieldDataService:
        """gRPC stub for field data operations."""
        return FieldDataService(
            intercept_channel=self._intercept_channel,
            metadata=self._metadata,
        )

    @cached_property
    def _chunk_parser(self) -> type[ChunkParser]:
        """Chunk parser class for field data operations."""
        return ChunkParser

    @cached_property
    def object_model(self) -> ObjectModelService:
        """gRPC stub for object model operations."""
        return ObjectModelService(
            intercept_channel=self._intercept_channel,
            metadata=self._metadata,
        )

    @cached_property
    def events(self) -> EventsService:
        """gRPC stub for events operations."""
        return EventsService(
            channel=self._channel,
            metadata=self._metadata,
        )

    @cached_property
    def transcript(self) -> TranscriptService:
        """gRPC stub for transcript operations."""
        return TranscriptService(
            channel=self._channel,
            metadata=self._metadata,
        )

    @cached_property
    def text_interface(self) -> TextInterfaceService:
        """gRPC stub for text interface operations."""
        return TextInterfaceService(
            intercept_channel=self._intercept_channel,
            metadata=self._metadata,
        )

    @cached_property
    def monitor(self) -> MonitorService:
        """gRPC stub for monitor operations."""
        return MonitorService(
            intercept_channel=self._intercept_channel,
            metadata=self._metadata,
        )

    @cached_property
    def solution_variable(self) -> SolutionVariableService:
        """gRPC stub for solution variable operations."""
        return SolutionVariableService(
            intercept_channel=self._intercept_channel,
            metadata=self._metadata,
        )
