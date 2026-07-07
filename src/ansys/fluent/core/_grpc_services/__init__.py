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

from functools import cached_property

from google.protobuf.descriptor_pool import DescriptorPool
from grpc_reflection.v1alpha.proto_reflection_descriptor_database import (
    ProtoReflectionDescriptorDatabase,
)

from ansys.fluent.core._grpc_services.application_runtime_service import (
    ApplicationRuntimeService,
)
from ansys.fluent.core._grpc_services.application_runtime_service_v0 import (
    ApplicationRuntimeService as ApplicationRuntimeServiceV0,
)
from ansys.fluent.core._grpc_services.health_check_service import HealthCheckService
from ansys.fluent.core._grpc_services.health_check_service_v0 import (
    HealthCheckService as HealthCheckServiceV0,
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
from ansys.fluent.core.services.application_runtime import (
    ApplicationRuntime,
    ApplicationRuntimeOld,
    ApplicationRuntimeV252,
    ApplicationRuntimeV261,
)
from ansys.fluent.core.services.health_check import HealthCheck
from ansys.fluent.core.services.reduction import Reduction
from ansys.fluent.core.services.scheme_interpreter import SchemeInterpreter
from ansys.fluent.core.services.settings import Settings, SettingsV251, SettingsV261
from ansys.fluent.core.utils.fluent_version import FluentVersion


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
    """Factory that creates and caches version-appropriate gRPC service wrappers.

    ``GRPCServiceFactory`` is the single entry point for obtaining all high-level service
    objects that communicate with a running Fluent server over gRPC.  It inspects
    the connected server's product version at construction time and thereafter
    returns the correct concrete wrapper class (v1 proto API for Fluent 27.1 and
    later, v0/legacy proto API for earlier releases) for every service.

    All service properties are ``cached_property`` instances, meaning each wrapper
    is instantiated at most once per factory and the same object is returned on
    every subsequent access.

    Parameters
    ----------
    channel : grpc.Channel
        Active gRPC channel connected to the Fluent server.
    metadata : list[tuple[str, str]]
        gRPC call metadata, typically containing authentication credentials.
    error_state : object, optional
        Shared error-state object passed to interceptors so that fatal server
        errors can be surfaced to callers.  When ``None``, no error-state
        checking is performed.
    product_version : FluentVersion, optional
        Explicit Fluent product version to use instead of auto-detecting it
        from the server.  Primarily intended for testing or when the version
        is already known, avoiding the extra RPC round-trip needed for
        auto-detection.

    Attributes
    ----------
    scheme_interpreter : SchemeInterpreter
        Service for evaluating Fluent Scheme expressions.
    application_runtime : ApplicationRuntime | ApplicationRuntimeV261 | ApplicationRuntimeV252 | ApplicationRuntimeOld
        Service exposing application-level runtime information such as the
        product version and session lifecycle management.  The concrete type
        depends on ``product_version``.
    health_check : HealthCheck
        Service for querying the health/serving status of the Fluent server.
    reduction : Reduction
        Service for performing data-reduction operations (e.g., force/moment
        integrals) on solver results.
    settings : Settings | SettingsV261 | SettingsV251
        Service for reading and writing Fluent solver settings.  The concrete
        type depends on ``product_version``.
    field_data : FieldData | FieldDataV261 | FieldDataV251
        Service for retrieving surface and volume field data from the solver.
        The concrete type depends on ``product_version``.
    field_data_streaming : FieldDataStreaming | FieldDataStreamingV261
        Streaming variant of the field-data service used to receive field data
        as a stream of chunks rather than a single response.
    object_model : ObjectModel | ObjectModelV261
        Service for interacting with Fluent's state-engine datamodel,
        including reading/writing object state, executing commands, and
        subscribing to datamodel events.  The concrete type depends on
        ``product_version``.

    Notes
    -----
    Underlying gRPC service objects (stubs + interceptors) are themselves
    lazily instantiated and cached via ``_get_instantiated_grpc_service``, so
    services that share the same underlying proto stub (e.g. ``scheme_interpreter``
    and ``application_runtime`` on older Fluent builds) reuse a single stub
    instance.
    """

    def __init__(
        self, channel, metadata, error_state=None, product_version: FluentVersion = None
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
        self._product_version = product_version or self._detect_product_version()

    def _detect_product_version(self) -> FluentVersion:
        """Determines the version using fallback detection logic."""
        grpc_service = (
            self._get_instantiated_grpc_service(SchemeInterpreterService)
            if _server_supports_v1(channel=self._channel)
            else self._get_instantiated_grpc_service(SchemeInterpreterServiceV0)
        )
        return FluentVersion(grpc_service.version)

    def _get_instantiated_grpc_service(self, grpc_service_class):
        """Generic lookup method that instantiates services lazily and caches them."""
        if grpc_service_class not in self._instantiated_services:
            self._instantiated_services[grpc_service_class] = grpc_service_class(
                **self._service_kwargs
            )
        return self._instantiated_services[grpc_service_class]

    @cached_property
    def scheme_interpreter(self) -> SchemeInterpreter:
        """Scheme interpreter service."""
        grpc_service = (
            self._get_instantiated_grpc_service(SchemeInterpreterService)
            if self._product_version >= FluentVersion.v271
            else self._get_instantiated_grpc_service(SchemeInterpreterServiceV0)
        )
        return SchemeInterpreter(grpc_service)

    @cached_property
    def application_runtime(self):
        """Application runtime service."""
        match self._product_version:
            case v if v >= FluentVersion.v271:
                return ApplicationRuntime(
                    self._get_instantiated_grpc_service(ApplicationRuntimeService)
                )
            case FluentVersion.v261:
                return ApplicationRuntimeV261(
                    self._get_instantiated_grpc_service(ApplicationRuntimeServiceV0)
                )
            case FluentVersion.v252:
                return ApplicationRuntimeV252(
                    self._get_instantiated_grpc_service(ApplicationRuntimeServiceV0),
                    self._get_instantiated_grpc_service(SchemeInterpreterServiceV0),
                )
            case _:
                return ApplicationRuntimeOld(
                    self._get_instantiated_grpc_service(SchemeInterpreterServiceV0)
                )

    @cached_property
    def health_check(self):
        """Health check service."""
        grpc_service = (
            self._get_instantiated_grpc_service(HealthCheckService)
            if self._product_version >= FluentVersion.v271
            else self._get_instantiated_grpc_service(HealthCheckServiceV0)
        )
        return HealthCheck(grpc_service)

    @cached_property
    def reduction(self):
        """Reduction service."""
        grpc_service = (
            self._get_instantiated_grpc_service(ReductionService)
            if self._product_version >= FluentVersion.v271
            else self._get_instantiated_grpc_service(ReductionServiceV0)
        )
        return Reduction(grpc_service)

    @cached_property
    def settings(self):
        """Settings service."""
        match self._product_version:
            case v if v >= FluentVersion.v271:
                return Settings(self._get_instantiated_grpc_service(SettingsService))
            case v if v >= FluentVersion.v252 and v < FluentVersion.v271:
                return SettingsV261(
                    self._get_instantiated_grpc_service(SettingsServiceV0),
                    self._get_instantiated_grpc_service(ApplicationRuntimeServiceV0),
                    self._get_instantiated_grpc_service(SchemeInterpreterServiceV0),
                )
            case _:
                return SettingsV251(
                    self._get_instantiated_grpc_service(SettingsServiceV0),
                    self._get_instantiated_grpc_service(SchemeInterpreterServiceV0),
                )
