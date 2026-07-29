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

from functools import cached_property

from google.protobuf.descriptor_pool import DescriptorPool
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
    """Lazily instantiates and caches raw gRPC service stubs for a Fluent server.

    Selects between v1 and v0 proto stubs based on what the server advertises
    via gRPC reflection.  Each property returns the underlying gRPC stub object
    directly — higher-level wrapping is left to callers.

    Parameters
    ----------
    channel : grpc.Channel
        Active gRPC channel to the Fluent server.
    metadata : list[tuple[str, str]]
        gRPC call metadata (e.g. authentication credentials).
    error_state : object, optional
        Shared error-state object forwarded to interceptors.
    proto_version : str, optional
        Override proto version (``"v1"`` or ``"v0"``).  Auto-detected from
        the server when omitted.
    """

    def __init__(
        self,
        channel,
        metadata,
        error_state=None,
        proto_version=None,
    ):
        """Initialize GRPCServiceFactory."""
        self._channel = channel
        self._metadata = metadata
        self._error_state = error_state
        self._service_kwargs = {
            "channel": self._channel,
            "metadata": self._metadata,
            "fluent_error_state": self._error_state,
        }
        self._instantiated_services = {}
        self._proto_version = proto_version or self._detect_proto_version()

    def _detect_proto_version(self) -> str:
        """Determines the version using fallback detection logic."""
        if _server_supports_v1(channel=self._channel):
            return "v1"
        else:
            return "v0"

    def _get_instantiated_grpc_service(self, grpc_service_class):
        """Generic lookup method that instantiates services lazily and caches them."""
        if grpc_service_class not in self._instantiated_services:
            self._instantiated_services[grpc_service_class] = grpc_service_class(
                **self._service_kwargs
            )
        return self._instantiated_services[grpc_service_class]

    @cached_property
    def scheme_interpreter(
        self,
    ) -> SchemeInterpreterService | SchemeInterpreterServiceV0:
        """gRPC stub for Scheme expression evaluation."""
        return (
            self._get_instantiated_grpc_service(SchemeInterpreterService)
            if self._proto_version == "v1"
            else self._get_instantiated_grpc_service(SchemeInterpreterServiceV0)
        )

    @cached_property
    def application_runtime(
        self,
    ) -> ApplicationRuntimeService | ApplicationRuntimeServiceV0:
        """gRPC stub for application runtime and product version queries."""
        return (
            self._get_instantiated_grpc_service(ApplicationRuntimeService)
            if self._proto_version == "v1"
            else self._get_instantiated_grpc_service(ApplicationRuntimeServiceV0)
        )

    @cached_property
    def health_check(self) -> HealthCheckService | HealthCheckServiceV0:
        """gRPC stub for server health/readiness checks."""
        return (
            self._get_instantiated_grpc_service(HealthCheckService)
            if self._proto_version == "v1"
            else self._get_instantiated_grpc_service(HealthCheckServiceV0)
        )

    @cached_property
    def reduction(self) -> ReductionService | ReductionServiceV0:
        """gRPC stub for data-reduction operations (forces, moments, etc.)."""
        return (
            self._get_instantiated_grpc_service(ReductionService)
            if self._proto_version == "v1"
            else self._get_instantiated_grpc_service(ReductionServiceV0)
        )

    @cached_property
    def settings(self) -> SettingsService | SettingsServiceV0:
        """gRPC stub for reading and writing solver settings."""
        return (
            self._get_instantiated_grpc_service(SettingsService)
            if self._proto_version == "v1"
            else self._get_instantiated_grpc_service(SettingsServiceV0)
        )

    @cached_property
    def field_data(self) -> FieldDataService | FieldDataServiceV0:
        """gRPC stub for field data operations."""
        return (
            self._get_instantiated_grpc_service(FieldDataService)
            if self._proto_version == "v1"
            else self._get_instantiated_grpc_service(FieldDataServiceV0)
        )

    @cached_property
    def _chunk_parser(self) -> ChunkParser | ChunkParserV0:
        """Chunk parser for field data operations."""
        return ChunkParser if self._proto_version == "v1" else ChunkParserV0

    @cached_property
    def object_model(self) -> ObjectModelService | ObjectModelServiceV0:
        """gRPC stub for object model operations."""
        return (
            self._get_instantiated_grpc_service(ObjectModelService)
            if self._proto_version == "v1"
            else self._get_instantiated_grpc_service(ObjectModelServiceV0)
        )

    @cached_property
    def events(self) -> EventsService | EventsServiceV0:
        """gRPC stub for events operations."""
        return (
            self._get_instantiated_grpc_service(EventsService)
            if self._proto_version == "v1"
            else self._get_instantiated_grpc_service(EventsServiceV0)
        )

    @cached_property
    def batch_ops(self) -> BatchOpsServiceV0:
        """gRPC stub for batch RPC operations (v0 only — no v1 implementation)."""
        return self._get_instantiated_grpc_service(BatchOpsServiceV0)

    @cached_property
    def transcript(self) -> TranscriptService | TranscriptServiceV0:
        """gRPC stub for transcript operations."""
        return (
            self._get_instantiated_grpc_service(TranscriptService)
            if self._proto_version == "v1"
            else self._get_instantiated_grpc_service(TranscriptServiceV0)
        )

    @cached_property
    def text_interface(self) -> TextInterfaceService | TextInterfaceServiceV0:
        """gRPC stub for text interface operations."""
        return (
            self._get_instantiated_grpc_service(TextInterfaceService)
            if self._proto_version == "v1"
            else self._get_instantiated_grpc_service(TextInterfaceServiceV0)
        )

    @cached_property
    def monitor(self) -> MonitorService | MonitorServiceV0:
        """gRPC stub for monitor operations."""
        return (
            self._get_instantiated_grpc_service(MonitorService)
            if self._proto_version == "v1"
            else self._get_instantiated_grpc_service(MonitorServiceV0)
        )

    @cached_property
    def solution_variable(self) -> SolutionVariableService | SolutionVariableServiceV0:
        """gRPC stub for solution variable operations."""
        return (
            self._get_instantiated_grpc_service(SolutionVariableService)
            if self._proto_version == "v1"
            else self._get_instantiated_grpc_service(SolutionVariableServiceV0)
        )
