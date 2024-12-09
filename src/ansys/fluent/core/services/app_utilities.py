"""Wrappers over AppUtilities gRPC service of Fluent."""

from typing import Any, List, Tuple

import grpc

from ansys.api.fluent.v0 import app_utilities_pb2 as AppUtilitiesProtoModule
from ansys.api.fluent.v0 import app_utilities_pb2_grpc as AppUtilitiesGrpcModule
from ansys.fluent.core.services.interceptors import (
    BatchInterceptor,
    ErrorStateInterceptor,
    GrpcErrorInterceptor,
    TracingInterceptor,
)


class AppUtilitiesService:
    """AppUtilities Service."""

    def __init__(
        self, channel: grpc.Channel, metadata: List[Tuple[str, str]], fluent_error_state
    ):
        """__init__ method of AppUtilities class."""
        intercept_channel = grpc.intercept_channel(
            channel,
            GrpcErrorInterceptor(),
            ErrorStateInterceptor(fluent_error_state),
            TracingInterceptor(),
            BatchInterceptor(),
        )
        self._stub = AppUtilitiesGrpcModule.AppUtilitiesStub(intercept_channel)
        self._metadata = metadata

    def get_product_version(
        self, request: AppUtilitiesProtoModule.GetProductVersionRequest
    ) -> AppUtilitiesProtoModule.GetProductVersionResponse:
        """Get product version RPC of AppUtilities service."""
        return self._stub.GetProductVersion(request, metadata=self._metadata)

    def get_build_info(
        self, request: AppUtilitiesProtoModule.GetBuildInfoRequest
    ) -> AppUtilitiesProtoModule.GetBuildInfoResponse:
        """Get build info RPC of AppUtilities service."""
        return self._stub.GetBuildInfo(request, metadata=self._metadata)

    def get_controller_process_info(
        self, request: AppUtilitiesProtoModule.GetControllerProcessInfoRequest
    ) -> AppUtilitiesProtoModule.GetControllerProcessInfoResponse:
        """Get controller process info RPC of AppUtilities service."""
        return self._stub.GetControllerProcessInfo(request, metadata=self._metadata)

    def get_solver_process_info(
        self, request: AppUtilitiesProtoModule.GetSolverProcessInfoRequest
    ) -> AppUtilitiesProtoModule.GetSolverProcessInfoResponse:
        """Get solver process info RPC of AppUtilities service."""
        return self._stub.GetSolverProcessInfo(request, metadata=self._metadata)

    def get_app_mode(
        self, request: AppUtilitiesProtoModule.GetAppModeRequest
    ) -> AppUtilitiesProtoModule.GetAppModeResponse:
        """Get app mode RPC of AppUtilities service."""
        return self._stub.GetAppMode(request, metadata=self._metadata)

    def start_python_journal(
        self, request: AppUtilitiesProtoModule.StartPythonJournalRequest
    ) -> AppUtilitiesProtoModule.StartPythonJournalResponse:
        """Start python journal RPC of AppUtilities service."""
        return self._stub.StartPythonJournal(request, metadata=self._metadata)

    def stop_python_journal(
        self, request: AppUtilitiesProtoModule.StopPythonJournalRequest
    ) -> AppUtilitiesProtoModule.StopPythonJournalResponse:
        """Stop python journal RPC of AppUtilities service."""
        return self._stub.StopPythonJournal(request, metadata=self._metadata)

    def is_beta_enabled(
        self, request: AppUtilitiesProtoModule.IsBetaEnabledRequest
    ) -> AppUtilitiesProtoModule.IsBetaEnabledResponse:
        """Is beta enabled RPC of AppUtilities service."""
        return self._stub.IsBetaEnabled(request, metadata=self._metadata)

    def is_wildcard(
        self, request: AppUtilitiesProtoModule.IsWildcardRequest
    ) -> AppUtilitiesProtoModule.IsWildcardResponse:
        """Is wildcard RPC of AppUtilities service."""
        return self._stub.IsWildcard(request, metadata=self._metadata)

    def is_solution_data_available(
        self, request: AppUtilitiesProtoModule.IsSolutionDataAvailableRequest
    ) -> AppUtilitiesProtoModule.IsSolutionDataAvailableResponse:
        """Is solution data available RPC of AppUtilities service."""
        return self._stub.IsSolutionDataAvailable(request, metadata=self._metadata)

    def register_on_pause_solution_events(
        self, request: AppUtilitiesProtoModule.RegisterPauseOnSolutionEventsRequest
    ) -> AppUtilitiesProtoModule.RegisterPauseOnSolutionEventsResponse:
        """Register on pause solution events RPC of AppUtilities service."""
        return self._stub.RegisterPauseOnSolutionEvents(
            request, metadata=self._metadata
        )

    def resume_on_solution_event(
        self, request: AppUtilitiesProtoModule.ResumeOnSolutionEventRequest
    ) -> AppUtilitiesProtoModule.ResumeOnSolutionEventResponse:
        """Resume on solution event RPC of AppUtilities service."""
        return self._stub.ResumeOnSolutionEvent(request, metadata=self._metadata)

    def unregister_on_pause_solution_events(
        self, request: AppUtilitiesProtoModule.UnregisterPauseOnSolutionEventsRequest
    ) -> AppUtilitiesProtoModule.UnregisterPauseOnSolutionEventsResponse:
        """Unregister on pause solution events RPC of AppUtilities service."""
        return self._stub.UnregisterPauseOnSolutionEvents(
            request, metadata=self._metadata
        )

    def exit(
        self, request: AppUtilitiesProtoModule.ExitRequest
    ) -> AppUtilitiesProtoModule.ExitResponse:
        """Exit RPC of AppUtilities service."""
        return self._stub.Exit(request, metadata=self._metadata)


class AppUtilities:
    """AppUtilities."""

    def __init__(self, service: AppUtilitiesService):
        """__init__ method of AppUtilities class."""
        self.service = service

    def get_product_version(self) -> Any:
        """Get product version."""
        request = AppUtilitiesProtoModule.GetProductVersionRequest()
        response = self.service.get_product_version(request)
        return f"{response.major}.{response.minor}.{response.patch}"
