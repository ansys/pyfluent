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

"""Wrapper over the application runtime gRPC service of Fluent (v1 proto API)."""

from enum import Enum
import os

import grpc

from ansys.api.fluent.v1 import application_runtime_pb2, application_runtime_pb2_grpc
from ansys.fluent.core._types import PathType
from ansys.fluent.core.services._protocols import ServiceProtocol
from ansys.fluent.core.services.abstract_application_runtime import (
    BuildInfo,
    ProcessInfo,
)
from ansys.fluent.core.services.interceptors import (
    BatchInterceptor,
    ErrorStateInterceptor,
    GrpcErrorInterceptor,
    TracingInterceptor,
)
from ansys.fluent.core.utils.fluent_version import FluentVersion


class ApplicationRuntimeService(ServiceProtocol):
    """ApplicationRuntime gRPC service wrapper (v1 proto API)."""

    def __init__(  # pyright: ignore[reportMissingSuperCall]
        self, channel: grpc.Channel, metadata: list[tuple[str, str]], fluent_error_state
    ):
        """Initialize ApplicationRuntimeService."""
        intercept_channel = grpc.intercept_channel(
            channel,
            GrpcErrorInterceptor(),
            ErrorStateInterceptor(fluent_error_state),
            TracingInterceptor(),
            BatchInterceptor(),
        )
        self._stub = application_runtime_pb2_grpc.ApplicationRuntimeStub(
            intercept_channel
        )
        self._metadata = metadata

    def get_product_version(self) -> FluentVersion:
        """GetProductVersion RPC."""
        request = application_runtime_pb2.GetProductVersionRequest()
        response = self._stub.GetProductVersion(request, metadata=self._metadata)
        return FluentVersion(f"{response.major}.{response.minor}.{response.patch}")

    def get_build_info(self) -> BuildInfo:
        """GetBuildInfo RPC."""
        request = application_runtime_pb2.GetBuildInfoRequest()
        response = self._stub.GetBuildInfo(request, metadata=self._metadata)
        return BuildInfo(
            build_time=response.build_time,
            build_id=response.build_id,
            vcs_revision=response.vcs_revision,
            vcs_branch=response.vcs_branch,
        )

    def get_controller_process_info(self) -> ProcessInfo:
        """GetControllerProcessInfo RPC."""
        request = application_runtime_pb2.GetControllerProcessInfoRequest()
        response = self._stub.GetControllerProcessInfo(request, metadata=self._metadata)
        return ProcessInfo(
            process_id=response.process_id,
            hostname=response.hostname,
            working_directory=response.working_directory,
        )

    def get_solver_process_info(self) -> ProcessInfo:
        """GetSolverProcessInfo RPC."""
        request = application_runtime_pb2.GetSolverProcessInfoRequest()
        response = self._stub.GetSolverProcessInfo(request, metadata=self._metadata)
        return ProcessInfo(
            process_id=response.process_id,
            hostname=response.hostname,
            working_directory=response.working_directory,
        )

    def get_app_mode(self) -> Enum:
        """GetAppMode RPC.

        Raises
        ------
        ValueError
            If app mode is unknown.
        """
        from ansys.fluent.core import FluentMode

        request = application_runtime_pb2.GetAppModeRequest()
        response = self._stub.GetAppMode(request, metadata=self._metadata)
        match response.app_mode:
            case application_runtime_pb2.APP_MODE_UNSPECIFIED:
                raise ValueError("Unknown app mode.")
            case application_runtime_pb2.APP_MODE_MESHING:
                return FluentMode.MESHING
            case application_runtime_pb2.APP_MODE_SOLVER:
                return FluentMode.SOLVER
            case application_runtime_pb2.APP_MODE_SOLVER_ICING:
                return FluentMode.SOLVER_ICING
            case application_runtime_pb2.APP_MODE_SOLVER_AERO:
                return FluentMode.SOLVER_AERO

    def start_python_journal(self, journal_name: str | None = None) -> int:
        """StartPythonJournal RPC."""
        request = application_runtime_pb2.StartPythonJournalRequest()
        if journal_name:
            request.journal_name = journal_name
        response = self._stub.StartPythonJournal(request, metadata=self._metadata)
        return response.journal_id

    def stop_python_journal(self, journal_id: str | None = None) -> str:
        """StopPythonJournal RPC."""
        request = application_runtime_pb2.StopPythonJournalRequest()
        if journal_id:
            request.journal_id = journal_id
        response = self._stub.StopPythonJournal(request, metadata=self._metadata)
        return response.journal_str

    def is_beta_enabled(self) -> bool:
        """IsBetaEnabled RPC."""
        request = application_runtime_pb2.IsBetaEnabledRequest()
        response = self._stub.IsBetaEnabled(request, metadata=self._metadata)
        return response.is_beta_enabled

    def enable_beta(self) -> None:
        """EnableBeta RPC."""
        request = application_runtime_pb2.EnableBetaRequest()
        self._stub.EnableBeta(request, metadata=self._metadata)

    def exit(self) -> None:
        """Exit RPC."""
        request = application_runtime_pb2.ExitRequest()
        self._stub.Exit(request, metadata=self._metadata)

    def set_working_directory(self, path: PathType) -> None:
        """SetWorkingDirectory RPC."""
        request = application_runtime_pb2.SetWorkingDirectoryRequest()
        request.path = os.fspath(path)
        self._stub.SetWorkingDirectory(request, metadata=self._metadata)
