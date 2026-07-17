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

import os

import grpc

from ansys.api.fluent.v1 import application_runtime_pb2, application_runtime_pb2_grpc
from ansys.fluent.core._types import PathType
from ansys.fluent.core.services._protocols import ServiceProtocol
from ansys.fluent.core.services.interceptors import (
    BatchInterceptor,
    ErrorStateInterceptor,
    GrpcErrorInterceptor,
    TracingInterceptor,
)


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

    def get_product_version(self) -> str:
        """GetProductVersion RPC."""
        request = application_runtime_pb2.GetProductVersionRequest()
        response = self._stub.GetProductVersion(request, metadata=self._metadata)
        return f"{response.major}.{response.minor}.{response.patch}"

    def get_build_info(self) -> tuple[str, str, str, str]:
        """GetBuildInfo RPC."""
        request = application_runtime_pb2.GetBuildInfoRequest()
        response = self._stub.GetBuildInfo(request, metadata=self._metadata)
        return (
            response.build_time,
            response.build_id,
            response.vcs_revision,
            response.vcs_branch,
        )

    def get_controller_process_info(self) -> tuple[int, str, str]:
        """GetControllerProcessInfo RPC."""
        request = application_runtime_pb2.GetControllerProcessInfoRequest()
        response = self._stub.GetControllerProcessInfo(request, metadata=self._metadata)
        return (
            response.process_id,
            response.hostname,
            response.working_directory,
        )

    def get_solver_process_info(self) -> tuple[int, str, str]:
        """GetSolverProcessInfo RPC."""
        request = application_runtime_pb2.GetSolverProcessInfoRequest()
        response = self._stub.GetSolverProcessInfo(request, metadata=self._metadata)
        return (
            response.process_id,
            response.hostname,
            response.working_directory,
        )

    def get_mode(self) -> str:
        """GetMode RPC.

        Raises
        ------
        ValueError
            If app mode is unknown.
        """
        request = application_runtime_pb2.GetModeRequest()
        response = self._stub.GetMode(request, metadata=self._metadata)
        match response.mode:
            case application_runtime_pb2.MODE_UNSPECIFIED:
                raise ValueError("Unknown app mode.")
            case application_runtime_pb2.MODE_MESHING:
                return "meshing"
            case application_runtime_pb2.MODE_SOLVER:
                return "solver"
            case application_runtime_pb2.MODE_SOLVER_ICING:
                return "solver_icing"
            case application_runtime_pb2.MODE_SOLVER_AERO:
                return "solver_aero"

    def get_dimension(self) -> int:
        """GetDimension RPC.

        Raises
        ------
        ValueError
            If dimension is unknown.
        """
        request = application_runtime_pb2.GetDimensionRequest()
        response = self._stub.GetDimension(request, metadata=self._metadata)
        match response.dimension:
            case application_runtime_pb2.DIMENSION_UNSPECIFIED:
                raise ValueError("Unknown dimension.")
            case application_runtime_pb2.DIMENSION_TWO:
                return 2
            case application_runtime_pb2.DIMENSION_THREE:
                return 3

    def get_precision(self) -> str:
        """GetPrecision RPC.

        Raises
        ------
        ValueError
            If precision is unknown.
        """
        request = application_runtime_pb2.GetPrecisionRequest()
        response = self._stub.GetPrecision(request, metadata=self._metadata)
        match response.precision:
            case application_runtime_pb2.PRECISION_UNSPECIFIED:
                raise ValueError("Unknown precision.")
            case application_runtime_pb2.PRECISION_SINGLE:
                return "single"
            case application_runtime_pb2.PRECISION_DOUBLE:
                return "double"

    def get_processor_count(self) -> int:
        """GetProcessorCount RPC."""
        request = application_runtime_pb2.GetProcessorCountRequest()
        response = self._stub.GetProcessorCount(request, metadata=self._metadata)
        return response.processor_count

    def get_ui_mode(self) -> str:
        """GetUIMode RPC.

        Raises
        ------
        ValueError
            If UI mode is unknown.
        """
        request = application_runtime_pb2.GetUIModeRequest()
        response = self._stub.GetUIMode(request, metadata=self._metadata)
        match response.ui_mode:
            case application_runtime_pb2.UI_MODE_UNSPECIFIED:
                raise ValueError("Unknown UI mode.")
            case application_runtime_pb2.UI_MODE_NO_GUI_OR_GRAPHICS:
                return "no_gui_or_graphics"
            case application_runtime_pb2.UI_MODE_NO_GRAPHICS:
                return "no_graphics"
            case application_runtime_pb2.UI_MODE_NO_GUI:
                return "no_gui"
            case application_runtime_pb2.UI_MODE_HIDDEN_GUI:
                return "hidden_gui"
            case application_runtime_pb2.UI_MODE_GUI:
                return "gui"

    def get_graphics_driver(self) -> str:
        """GetGraphicsDriver RPC.

        Raises
        ------
        ValueError
            If graphics driver is unknown.
        """
        request = application_runtime_pb2.GetGraphicsDriverRequest()
        response = self._stub.GetGraphicsDriver(request, metadata=self._metadata)
        match response.WhichOneof("driver"):
            case "windows_graphics_driver":
                match response.windows_graphics_driver:
                    case application_runtime_pb2.WINDOWS_GRAPHICS_DRIVER_UNSPECIFIED:
                        raise ValueError("Unknown graphics driver.")
                    case application_runtime_pb2.WINDOWS_GRAPHICS_DRIVER_NULL:
                        return "null"
                    case application_runtime_pb2.WINDOWS_GRAPHICS_DRIVER_MSW:
                        return "msw"
                    case application_runtime_pb2.WINDOWS_GRAPHICS_DRIVER_DX11:
                        return "dx11"
                    case application_runtime_pb2.WINDOWS_GRAPHICS_DRIVER_OPENGL2:
                        return "opengl2"
                    case application_runtime_pb2.WINDOWS_GRAPHICS_DRIVER_OPENGL:
                        return "opengl"
                    case application_runtime_pb2.WINDOWS_GRAPHICS_DRIVER_AUTO:
                        return "auto"
            case "linux_graphics_driver":
                match response.linux_graphics_driver:
                    case application_runtime_pb2.LINUX_GRAPHICS_DRIVER_UNSPECIFIED:
                        raise ValueError("Unknown graphics driver.")
                    case application_runtime_pb2.LINUX_GRAPHICS_DRIVER_NULL:
                        return "null"
                    case application_runtime_pb2.LINUX_GRAPHICS_DRIVER_X11:
                        return "x11"
                    case application_runtime_pb2.LINUX_GRAPHICS_DRIVER_OPENGL2:
                        return "opengl2"
                    case application_runtime_pb2.LINUX_GRAPHICS_DRIVER_OPENGL:
                        return "opengl"
                    case application_runtime_pb2.LINUX_GRAPHICS_DRIVER_AUTO:
                        return "auto"

    def get_gpu_config(self) -> bool | list[int]:
        """GetGPUConfig RPC."""
        request = application_runtime_pb2.GetGPUConfigRequest()
        response = self._stub.GetGPUConfig(request, metadata=self._metadata)
        match response.WhichOneof("config"):
            case "auto_allocate":
                return response.auto_allocate
            case "specific_gpu_ids":
                return list(response.specific_gpu_ids.gpu_ids)

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

    def set_idle_timeout(self, timeout: int) -> None:
        """Set the Fluent session idle timeout.

        Parameters
        ----------
        timeout : int
            Idle timeout duration in seconds. Pass 0 to disable the idle timeout.
        """
        request = application_runtime_pb2.SetIdleTimeoutRequest()
        request.timeout.seconds = timeout
        self._stub.SetIdleTimeout(request, metadata=self._metadata)
