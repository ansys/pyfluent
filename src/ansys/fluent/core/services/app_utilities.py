"""Wrappers over AppUtilities gRPC service of Fluent."""

from typing import Any, List, Tuple

from google.protobuf.json_format import MessageToDict
import grpc

from ansys.api.fluent.v0 import app_utilities_pb2 as AppUtilitiesProtoModule
from ansys.api.fluent.v0 import app_utilities_pb2_grpc as AppUtilitiesGrpcModule
import ansys.fluent.core as pyfluent
from ansys.fluent.core.services.interceptors import (
    BatchInterceptor,
    ErrorStateInterceptor,
    GrpcErrorInterceptor,
    TracingInterceptor,
)
from ansys.fluent.core.streaming_services.events_streaming import SolverEvent


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

    def register_pause_on_solution_events(
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

    def unregister_pause_on_solution_events(
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

    def get_product_version(self, with_patch: bool = True) -> Any:
        """Get product version."""
        request = AppUtilitiesProtoModule.GetProductVersionRequest()
        response = self.service.get_product_version(request)
        if with_patch:
            return f"{response.major}.{response.minor}.{response.patch}"
        else:
            return f"{response.major}{response.minor}"

    def get_build_info(self) -> Any:
        """Get build info."""
        request = AppUtilitiesProtoModule.GetBuildInfoRequest()
        response = self.service.get_build_info(request)
        return MessageToDict(response)

    def get_controller_process_info(self) -> Any:
        """Get controller process info."""
        request = AppUtilitiesProtoModule.GetControllerProcessInfoRequest()
        response = self.service.get_controller_process_info(request)
        return MessageToDict(response)

    def get_solver_process_info(self) -> Any:
        """Get solver process info."""
        request = AppUtilitiesProtoModule.GetSolverProcessInfoRequest()
        response = self.service.get_solver_process_info(request)
        return MessageToDict(response)

    def get_app_mode(self) -> Any:
        """Get app mode.

        Raises
        ------
        ValueError
            If app mode is unknown.
        """
        request = AppUtilitiesProtoModule.GetAppModeRequest()
        response = self.service.get_app_mode(request)
        match response.app_mode:
            case AppUtilitiesProtoModule.APP_MODE_UNKNOWN:
                raise ValueError("Unknown app mode.")
            case AppUtilitiesProtoModule.APP_MODE_MESHING:
                return pyfluent.FluentMode.MESHING
            case AppUtilitiesProtoModule.APP_MODE_SOLVER:
                return pyfluent.FluentMode.SOLVER
            case AppUtilitiesProtoModule.APP_MODE_SOLVER_ICING:
                return pyfluent.FluentMode.SOLVER_ICING
            case AppUtilitiesProtoModule.APP_MODE_SOLVER_AERO:
                return pyfluent.FluentMode.SOLVER_AERO

    def start_python_journal(self, journal_name: str | None = None) -> Any:
        """Start python journal."""
        request = AppUtilitiesProtoModule.StartPythonJournalRequest()
        request.journal_name = journal_name
        response = self.service.start_python_journal(request)
        return response

    def stop_python_journal(self) -> Any:
        """Stop python journal."""
        request = AppUtilitiesProtoModule.StopPythonJournalRequest()
        response = self.service.stop_python_journal(request)
        return response

    def is_beta_enabled(self) -> Any:
        """Is beta enabled."""
        request = AppUtilitiesProtoModule.IsBetaEnabledRequest()
        response = self.service.is_beta_enabled(request)
        return response.is_beta_enabled

    def is_wildcard(self, input: str | None = None) -> Any:
        """Is wildcard."""
        request = AppUtilitiesProtoModule.IsWildcardRequest()
        request.input = input
        response = self.service.is_wildcard(request)
        return response.is_wildcard

    def is_solution_data_available(self) -> Any:
        """Is solution data available."""
        request = AppUtilitiesProtoModule.IsSolutionDataAvailableRequest()
        response = self.service.is_solution_data_available(request)
        return response.is_solution_data_available

    def register_pause_on_solution_events(self, solution_event: SolverEvent) -> Any:
        """Register pause on solution events."""
        request = AppUtilitiesProtoModule.RegisterPauseOnSolutionEventsRequest()
        if solution_event == SolverEvent.TIMESTEP_ENDED:
            request.solution_event = 2
        elif solution_event == SolverEvent.ITERATION_ENDED:
            request.solution_event = 1
        else:
            request.solution_event = 0
        response = self.service.register_pause_on_solution_events(request)
        return response.registration_id

    def resume_on_solution_event(self, registration_id: str) -> Any:
        """Resume on solution event."""
        request = AppUtilitiesProtoModule.ResumeOnSolutionEventRequest()
        request.registration_id = registration_id
        response = self.service.resume_on_solution_event(request)
        return response

    def unregister_pause_on_solution_events(self, registration_id: str) -> Any:
        """Unregister pause on solution events."""
        request = AppUtilitiesProtoModule.UnregisterPauseOnSolutionEventsRequest()
        request.registration_id = registration_id
        response = self.service.unregister_pause_on_solution_events(request)
        return response

    def exit(self) -> Any:
        """Exit."""
        request = AppUtilitiesProtoModule.ExitRequest()
        response = self.service.exit(request)
        return response
