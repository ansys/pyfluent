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

from functools import cached_property

from ansys.fluent.core.services.application_runtime import (
    ApplicationRuntime,
    ApplicationRuntimeOld,
    ApplicationRuntimeV252,
    ApplicationRuntimeV261,
)
from ansys.fluent.core.services.events import Events, EventsV251, EventsV261
from ansys.fluent.core.services.field_data import (
    FieldData,
    FieldDataV251,
    FieldDataV261,
)
from ansys.fluent.core.services.health_check import HealthCheck
from ansys.fluent.core.services.monitors import Monitor
from ansys.fluent.core.services.object_model import ObjectModel, ObjectModelV261
from ansys.fluent.core.services.reduction import Reduction
from ansys.fluent.core.services.scheme_interpreter import SchemeInterpreter
from ansys.fluent.core.services.settings import Settings, SettingsV251, SettingsV261
from ansys.fluent.core.services.solution_variables import (
    SolutionVariableData,
    SolutionVariableInfo,
)
from ansys.fluent.core.services.text_interface import TextInterface
from ansys.fluent.core.services.transcript import Transcript
from ansys.fluent.core.streaming_services.datamodel_event_streaming import (
    DatamodelEvents,
)
from ansys.fluent.core.streaming_services.datamodel_streaming import DatamodelStream
from ansys.fluent.core.streaming_services.events_streaming import EventsManager
from ansys.fluent.core.streaming_services.field_data_streaming import (
    FieldDataStreaming,
)
from ansys.fluent.core.streaming_services.monitor_streaming import MonitorsManager
from ansys.fluent.core.streaming_services.transcript_streaming import (
    Transcript as TranscriptStreaming,
)
from ansys.fluent.core.utils.fluent_version import FluentVersion


class ServiceFactory:
    """Abstract base factory providing version-appropriate high-level service wrappers.

    Wraps low-level service objects (from `GRPCServiceFactory`) in version-specific
    high-level wrappers.  Version-agnostic services are implemented here; version-varying
    services raise :exc:`NotImplementedError` and must be provided by a concrete subclass.

    Use :func:`create_service_factory` to obtain the correct concrete instance.

    Parameters
    ----------
    service_factory : GRPCServiceFactory
        Source of the underlying raw gRPC service objects.
    """

    def __init__(self, service_factory):
        """Initialize ServiceFactory."""
        self._service_factory = service_factory

    # ------------------------------------------------------------------
    # Version-agnostic services (concrete in base)
    # ------------------------------------------------------------------

    @cached_property
    def scheme_interpreter(self) -> SchemeInterpreter:
        """Scheme expression evaluator."""
        return SchemeInterpreter(self._service_factory.scheme_interpreter)

    @cached_property
    def health_check(self):
        """Server health and readiness service."""
        return HealthCheck(self._service_factory.health_check)

    @cached_property
    def reduction(self):
        """Data-reduction service (forces, moments, etc.)."""
        return Reduction(self._service_factory.reduction)

    @cached_property
    def transcript(self):
        """Transcript service."""
        return Transcript(self._service_factory.transcript)

    @property
    def transcript_streaming(self):
        """Transcript streaming service."""
        return TranscriptStreaming(self._service_factory.transcript)

    @cached_property
    def batch_ops(self):
        """Batch operations service."""
        return self._service_factory.batch_ops

    @cached_property
    def text_interface(self):
        """Text interface service."""
        return TextInterface(
            self._service_factory.text_interface,
            self._service_factory.application_runtime,
            self._service_factory.scheme_interpreter,
        )

    @cached_property
    def monitor(self):
        """Monitor service."""
        return Monitor(self._service_factory.monitor)

    @cached_property
    def object_model_streaming(self):
        """Object model streaming service."""
        return DatamodelStream(self._service_factory.object_model)

    @cached_property
    def object_model_events_streaming(self):
        """Object model events streaming service."""
        return DatamodelEvents(self._service_factory.object_model)

    @cached_property
    def solution_variable_info(self):
        """Solution variable info service."""
        return SolutionVariableInfo(self._service_factory.solution_variable)

    @cached_property
    def solution_variable_data(self):
        """Solution variable data service."""
        return SolutionVariableData(
            self._service_factory.solution_variable, self.solution_variable_info
        )

    @property
    def field_data_streaming(self):
        """Field data streaming service."""
        return FieldDataStreaming(
            self._service_factory.field_data,
            self._service_factory._chunk_parser,
        )

    def _get_events_manager(self, event_type, session_ref):
        """Get events manager."""
        return EventsManager[event_type](
            event_type,
            self.events,
            self._service_factory._error_state,
            session_ref,
        )

    def _get_monitors_manager(self, session_id):
        """Get monitors manager."""
        return MonitorsManager(
            session_id,
            self._service_factory.monitor,
        )

    # ------------------------------------------------------------------
    # Version-varying services (abstract — override in subclasses)
    # ------------------------------------------------------------------

    @cached_property
    def application_runtime(self):
        """Application runtime, version and session lifecycle service."""
        raise NotImplementedError

    @cached_property
    def settings(self):
        """Solver settings service."""
        raise NotImplementedError

    @cached_property
    def field_data(self):
        """Field data service."""
        raise NotImplementedError

    @cached_property
    def events(self):
        """Events service."""
        raise NotImplementedError

    @cached_property
    def object_model(self):
        """Object model service."""
        raise NotImplementedError


class ServiceFactoryV271(ServiceFactory):
    """Service factory for Fluent >= v271 (v1 proto era)."""

    @cached_property
    def application_runtime(self):
        """Application runtime, version and session lifecycle service."""
        return ApplicationRuntime(self._service_factory.application_runtime)

    @cached_property
    def settings(self):
        """Solver settings service."""
        return Settings(self._service_factory.settings)

    @cached_property
    def field_data(self):
        """Field data service."""
        return FieldData(
            self._service_factory.field_data,
            self._service_factory._chunk_parser(),
        )

    @cached_property
    def events(self):
        """Events service."""
        return Events(self._service_factory.events)

    @cached_property
    def object_model(self):
        """Object model service."""
        return ObjectModel(
            self._service_factory.object_model,
            self._service_factory.scheme_interpreter,
        )


class ServiceFactoryV261(ServiceFactory):
    """Service factory for Fluent v252 <= v < v271 (v0 proto era).

    Parameters
    ----------
    service_factory : GRPCServiceFactory
        Source of the underlying raw gRPC stubs.
    product_version : FluentVersion
        Exact product version; used to distinguish ``ApplicationRuntimeV261``
        from ``ApplicationRuntimeV252``.
    """

    def __init__(self, service_factory, product_version):
        """Initialize ServiceFactoryV261."""
        super().__init__(service_factory)
        self._product_version = product_version

    @cached_property
    def application_runtime(self):
        """Application runtime, version and session lifecycle service."""
        if self._product_version == FluentVersion.v261:
            return ApplicationRuntimeV261(
                self._service_factory.application_runtime,
                self._service_factory.scheme_interpreter,
            )
        if self._product_version == FluentVersion.v252:
            return ApplicationRuntimeV252(
                self._service_factory.application_runtime,
                self._service_factory.scheme_interpreter,
            )
        return ApplicationRuntimeOld(self._service_factory.scheme_interpreter)

    @cached_property
    def settings(self):
        """Solver settings service."""
        return SettingsV261(
            self._service_factory.settings,
            self._service_factory.application_runtime,
            self._service_factory.scheme_interpreter,
        )

    @cached_property
    def field_data(self):
        """Field data service."""
        return FieldDataV261(
            self._service_factory.field_data,
            self._service_factory._chunk_parser(),
            self._service_factory.application_runtime,
        )

    @cached_property
    def events(self):
        """Events service."""
        return EventsV261(
            self._service_factory.events,
            self._service_factory.application_runtime,
        )

    @cached_property
    def object_model(self):
        """Object model service."""
        return ObjectModelV261(
            self._service_factory.object_model,
            self._service_factory.scheme_interpreter,
        )


class ServiceFactoryLegacy(ServiceFactory):
    """Service factory for Fluent < v252 (legacy / v0 era)."""

    @cached_property
    def application_runtime(self):
        """Application runtime, version and session lifecycle service."""
        return ApplicationRuntimeOld(self._service_factory.scheme_interpreter)

    @cached_property
    def settings(self):
        """Solver settings service."""
        return SettingsV251(
            self._service_factory.settings,
            self._service_factory.scheme_interpreter,
        )

    @cached_property
    def field_data(self):
        """Field data service."""
        return FieldDataV251(
            self._service_factory.field_data,
            self._service_factory._chunk_parser(),
            self._service_factory.scheme_interpreter,
        )

    @cached_property
    def events(self):
        """Events service."""
        return EventsV251(
            self._service_factory.events,
            self._service_factory.scheme_interpreter,
        )

    @cached_property
    def object_model(self):
        """Object model service."""
        return ObjectModelV261(
            self._service_factory.object_model,
            self._service_factory.scheme_interpreter,
        )


def create_service_factory(
    service_factory, product_version: FluentVersion = None
) -> ServiceFactory:
    """Return the correct :class:`ServiceFactory` subclass for *service_factory*.

    Parameters
    ----------
    service_factory : GRPCServiceFactory
        Source of the underlying raw gRPC stubs.
    product_version : FluentVersion, optional
        Fluent product version.  Derived from ``service_factory.scheme_interpreter``
        when omitted.
    """
    version = product_version or FluentVersion(
        ".".join(
            service_factory.scheme_interpreter.string_eval("(cx-version)")
            .strip("()")
            .split()
        )
    )
    if version >= FluentVersion.v271:
        return ServiceFactoryV271(service_factory)
    elif version >= FluentVersion.v252:
        return ServiceFactoryV261(service_factory, version)
    else:
        return ServiceFactoryLegacy(service_factory)
