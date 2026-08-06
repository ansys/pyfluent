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

"""Low-level gRPC service stubs and factory for Fluent server communication."""

from enum import Enum
from functools import cached_property

from google.protobuf.descriptor_pool import DescriptorPool
import grpc
from grpc_reflection.v1alpha.proto_reflection_descriptor_database import (
    ProtoReflectionDescriptorDatabase,
)

from ansys.fluent.core._grpc_services._chunk_parser import ChunkParser, ChunkParserV0
from ansys.fluent.core._grpc_services.application_runtime_service import (
    ApplicationRuntimeService,
)
from ansys.fluent.core._grpc_services.application_runtime_service_v0 import (
    ApplicationRuntimeService as ApplicationRuntimeServiceV0,
)
from ansys.fluent.core._grpc_services.batch_ops_service_v0 import (
    BatchOpsService as BatchOpsServiceV0,
)
from ansys.fluent.core._grpc_services.events_service import EventsService
from ansys.fluent.core._grpc_services.events_service_v0 import (
    EventsService as EventsServiceV0,
)
from ansys.fluent.core._grpc_services.field_data_service import FieldDataService
from ansys.fluent.core._grpc_services.field_data_service_v0 import (
    FieldDataService as FieldDataServiceV0,
)
from ansys.fluent.core._grpc_services.health_check_service import HealthCheckService
from ansys.fluent.core._grpc_services.health_check_service_v0 import (
    HealthCheckService as HealthCheckServiceV0,
)
from ansys.fluent.core._grpc_services.monitor_service import MonitorService
from ansys.fluent.core._grpc_services.monitor_service_v0 import (
    MonitorService as MonitorServiceV0,
)
from ansys.fluent.core._grpc_services.object_model_service import ObjectModelService
from ansys.fluent.core._grpc_services.object_model_service_v0 import (
    ObjectModelService as ObjectModelServiceV0,
)
from ansys.fluent.core._grpc_services.reduction_service import ReductionService
from ansys.fluent.core._grpc_services.reduction_service_v0 import (
    ReductionService as ReductionServiceV0,
)
from ansys.fluent.core._grpc_services.scheme_interpreter_service import (
    SchemeInterpreterService,
)
from ansys.fluent.core._grpc_services.scheme_interpreter_service_v0 import (
    SchemeInterpreterService as SchemeInterpreterServiceV0,
)
from ansys.fluent.core._grpc_services.settings_service import SettingsService
from ansys.fluent.core._grpc_services.settings_service_v0 import (
    SettingsService as SettingsServiceV0,
)
from ansys.fluent.core._grpc_services.solution_variable_service import (
    SolutionVariableService,
)
from ansys.fluent.core._grpc_services.solution_variable_service_v0 import (
    SolutionVariableService as SolutionVariableServiceV0,
)
from ansys.fluent.core._grpc_services.text_interface_service import TextInterfaceService
from ansys.fluent.core._grpc_services.text_interface_service_v0 import (
    TextInterfaceService as TextInterfaceServiceV0,
)
from ansys.fluent.core._grpc_services.transcript_service import TranscriptService
from ansys.fluent.core._grpc_services.transcript_service_v0 import (
    TranscriptService as TranscriptServiceV0,
)
from ansys.fluent.core.services.interceptors import (
    BatchInterceptor,
    ErrorStateInterceptor,
    GrpcErrorInterceptor,
    TracingInterceptor,
)


class ProtoVersion(Enum):
    """Enum for gRPC proto versions."""

    V0 = "v0"
    V1 = "v1"


def _server_supports_v1(channel) -> bool:
    try:
        reflection_db = ProtoReflectionDescriptorDatabase(channel)
        desc_pool = DescriptorPool(reflection_db)
        service_desc = desc_pool.FindServiceByName(
            "ansys.api.fluent.v1.application_runtime.ApplicationRuntime"
        )
        method_desc = service_desc.FindMethodByName("GetProductVersion")
        return (
            method_desc.full_name
            == "ansys.api.fluent.v1.application_runtime.ApplicationRuntime.GetProductVersion"
        )
    except KeyError:
        return False


class GRPCServiceFactory:
    """Abstract base factory for raw gRPC service stubs.

    Concrete subclasses select the right stub class for a particular proto
    version.  Each property returns a lazily-instantiated stub object directly;
    higher-level wrapping is left to callers.

    Parameters
    ----------
    channel : grpc.Channel
        Active gRPC channel to the Fluent server.
    metadata : list[tuple[str, str]]
        gRPC call metadata (e.g. authentication credentials).
    error_state : object, optional
        Shared error-state object forwarded to interceptors.
    """

    def __init__(self, channel, metadata, error_state=None):
        """Initialize GRPCServiceFactory."""
        self._channel = channel
        self._metadata = metadata
        self._error_state = error_state
        self._intercept_channel = grpc.intercept_channel(
            self._channel,
            GrpcErrorInterceptor(),
            ErrorStateInterceptor(self._error_state),
            TracingInterceptor(),
            BatchInterceptor(),
        )

    @cached_property
    def scheme_interpreter(self):
        """gRPC stub for Scheme expression evaluation."""
        raise NotImplementedError

    @cached_property
    def application_runtime(self):
        """gRPC stub for application runtime and product version queries."""
        raise NotImplementedError

    @cached_property
    def health_check(self):
        """gRPC stub for server health/readiness checks."""
        raise NotImplementedError

    @cached_property
    def reduction(self):
        """gRPC stub for data-reduction operations (forces, moments, etc.)."""
        raise NotImplementedError

    @cached_property
    def settings(self):
        """gRPC stub for reading and writing solver settings."""
        raise NotImplementedError

    @cached_property
    def field_data(self):
        """gRPC stub for field data operations."""
        raise NotImplementedError

    @cached_property
    def _chunk_parser(self):
        """Chunk parser class for field data operations."""
        raise NotImplementedError

    @cached_property
    def object_model(self):
        """gRPC stub for object model operations."""
        raise NotImplementedError

    @cached_property
    def events(self):
        """gRPC stub for events operations."""
        raise NotImplementedError

    @cached_property
    def batch_ops(self) -> BatchOpsServiceV0:
        """gRPC stub for batch RPC operations (v0 only — no v1 implementation)."""
        return BatchOpsServiceV0(
            intercept_channel=grpc.intercept_channel(
                self._channel,
                GrpcErrorInterceptor(),
            ),
            metadata=self._metadata,
        )

    @cached_property
    def transcript(self):
        """gRPC stub for transcript operations."""
        raise NotImplementedError

    @cached_property
    def text_interface(self):
        """gRPC stub for text interface operations."""
        raise NotImplementedError

    @cached_property
    def monitor(self):
        """gRPC stub for monitor operations."""
        raise NotImplementedError

    @cached_property
    def solution_variable(self):
        """gRPC stub for solution variable operations."""
        raise NotImplementedError


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


def create_grpc_service_factory(
    channel,
    metadata,
    error_state=None,
    proto_version: ProtoVersion | str = None,
) -> GRPCServiceFactory:
    """Return the correct :class:`GRPCServiceFactory` subclass for *channel*.

    Parameters
    ----------
    channel : grpc.Channel
        Active gRPC channel to the Fluent server.
    metadata : list[tuple[str, str]]
        gRPC call metadata.
    error_state : object, optional
        Shared error-state object forwarded to interceptors.
    proto_version : ProtoVersion | str, optional
        ``ProtoVersion.V1``/``"v1"`` or ``ProtoVersion.V0``/``"v0"``.
        Auto-detected via gRPC reflection when omitted.
    """
    version = proto_version or (
        ProtoVersion.V1 if _server_supports_v1(channel) else ProtoVersion.V0
    )
    cls = GRPCServiceFactoryV1 if version == ProtoVersion.V1 else GRPCServiceFactoryV0
    return cls(channel, metadata, error_state)
