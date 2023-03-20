"""Wrappers over Reduction gRPC service of Fluent."""

from typing import Any, List, Tuple

import grpc

from ansys.api.fluent.v0 import reduction_pb2 as ReductionProtoModule
from ansys.api.fluent.v0 import reduction_pb2_grpc as ReductionGrpcModule
from ansys.fluent.core.services.error_handler import catch_grpc_error
from ansys.fluent.core.services.interceptors import BatchInterceptor, TracingInterceptor

Path = List[Tuple[str, str]]


class ReductionService:
    """Wraps the StateEngine-based datamodel gRPC service of Fluent.

    Using the methods from the ``PyMenu`` class is recommended.
    """

    def __init__(self, channel: grpc.Channel, metadata: List[Tuple[str, str]]):
        """__init__ method of DatamodelService class."""
        intercept_channel = grpc.intercept_channel(
            channel, TracingInterceptor(), BatchInterceptor()
        )
        self._stub = ReductionGrpcModule.ReductionQueriesStub(intercept_channel)
        self._metadata = metadata
        super().__init__(
            stub=self._stub,
            request=ReductionProtoModule.AreaRequest(),
            metadata=metadata,
        )
        self.event_streaming = None
        self.events = {}

    @catch_grpc_error
    def area(
        self, request: ReductionProtoModule.AreaRequest
    ) -> ReductionProtoModule.AreaResponse:
        """Area rpc of Reduction service."""
        return self._stub.Area(request, metadata=self._metadata)

    @catch_grpc_error
    def area_average(
        self, request: ReductionProtoModule.AreaAveRequest
    ) -> ReductionProtoModule.AreaAveResponse:
        """Area average rpc of Reduction service."""
        return self._stub.AreaAve(request, metadata=self._metadata)

    @catch_grpc_error
    def area_integral(
        self, request: ReductionProtoModule.AreaIntRequest
    ) -> ReductionProtoModule.AreaIntResponse:
        """Area integral rpc of Reduction service."""
        return self._stub.AreaInt(request, metadata=self._metadata)

    @catch_grpc_error
    def centroid(
        self, request: ReductionProtoModule.CentroidRequest
    ) -> ReductionProtoModule.CentroidResponse:
        """Centroid rpc of Reduction service."""
        return self._stub.Centroid(request, metadata=self._metadata)

    @catch_grpc_error
    def count(
        self, request: ReductionProtoModule.CountRequest
    ) -> ReductionProtoModule.CountResponse:
        """Count rpc of Reduction service."""
        return self._stub.Count(request, metadata=self._metadata)

    @catch_grpc_error
    def force(
        self, request: ReductionProtoModule.ForceRequest
    ) -> ReductionProtoModule.ForceResponse:
        """Force rpc of Reduction service."""
        return self._stub.Force(request, metadata=self._metadata)

    @catch_grpc_error
    def mass_average(
        self, request: ReductionProtoModule.MassAveRequest
    ) -> ReductionProtoModule.MassAveResponse:
        """Mass average rpc of Reduction service."""
        return self._stub.MassAve(request, metadata=self._metadata)

    @catch_grpc_error
    def mass_flow_average(
        self, request: ReductionProtoModule.MassFlowAveRequest
    ) -> ReductionProtoModule.MassFlowAveResponse:
        """Mass flow average rpc of Reduction service."""
        return self._stub.MassFlowAve(request, metadata=self._metadata)

    @catch_grpc_error
    def mass_flow_average_absolute(
        self, request: ReductionProtoModule.MassFlowAveAbsRequest
    ) -> ReductionProtoModule.MassFlowAveAbsResponse:
        """Absolute mass flow average rpc of Reduction service."""
        return self._stub.MassFlowAveAbs(request, metadata=self._metadata)

    @catch_grpc_error
    def mass_flow_integral(
        self, request: ReductionProtoModule.MassFlowIntRequest
    ) -> ReductionProtoModule.MassFlowIntResponse:
        """Mass flow integral rpc of Reduction service."""
        return self._stub.MassFlowInt(request, metadata=self._metadata)

    @catch_grpc_error
    def mass_integral(
        self, request: ReductionProtoModule.MassIntRequest
    ) -> ReductionProtoModule.MassIntResponse:
        """Mass integral rpc of Reduction service."""
        return self._stub.MassInt(request, metadata=self._metadata)

    @catch_grpc_error
    def maximum(
        self, request: ReductionProtoModule.MaximumRequest
    ) -> ReductionProtoModule.MaximumResponse:
        """Maximum rpc of Reduction service."""
        return self._stub.Maximum(request, metadata=self._metadata)

    @catch_grpc_error
    def minimum(
        self, request: ReductionProtoModule.MinimumRequest
    ) -> ReductionProtoModule.MinimumResponse:
        """Minimum rpc of Reduction service."""
        return self._stub.Minimum(request, metadata=self._metadata)

    @catch_grpc_error
    def pressure_force(
        self, request: ReductionProtoModule.PressureForceRequest
    ) -> ReductionProtoModule.PressureForceResponse:
        """Pressure force rpc of Reduction service."""
        return self._stub.PressureForce(request, metadata=self._metadata)

    @catch_grpc_error
    def viscous_force(
        self, request: ReductionProtoModule.ViscousForceRequest
    ) -> ReductionProtoModule.ViscousForceResponse:
        """Viscous force rpc of Reduction service."""
        return self._stub.ViscousForce(request, metadata=self._metadata)

    @catch_grpc_error
    def volume(
        self, request: ReductionProtoModule.VolumeRequest
    ) -> ReductionProtoModule.VolumeResponse:
        """Volume rpc of Reduction service."""
        return self._stub.Volume(request, metadata=self._metadata)

    @catch_grpc_error
    def volume_average(
        self, request: ReductionProtoModule.VolumeAveRequest
    ) -> ReductionProtoModule.VolumeAveResponse:
        """Volume rpc of Reduction service."""
        return self._stub.VolumeAve(request, metadata=self._metadata)

    @catch_grpc_error
    def volume_integral(
        self, request: ReductionProtoModule.VolumeIntRequest
    ) -> ReductionProtoModule.VolumeIntResponse:
        """Volume rpc of Reduction service."""
        return self._stub.VolumeInt(request, metadata=self._metadata)


class Reduction:
    """
    Reduction.
    """

    def __init__(
        self, service: ReductionService, locations: str, expression: str = None
    ):
        """__init__ method of Reduction class."""
        self.service = service
        self.locations = locations
        self.expression = expression

    docstring = None

    def area(self) -> Any:
        """Get area."""
        request = ReductionProtoModule.AreaRequest()
        request.locations.append(self.locations)
        response = self.service.area(request)
        return response.value

    def area_average(self) -> Any:
        """Get area average."""
        request = ReductionProtoModule.AreaAveRequest()
        request.expression = self.expression
        request.locations.append(self.locations)
        response = self.service.area_average(request)
        return response.value

    def area_integral(self) -> Any:
        """Get area integral."""
        request = ReductionProtoModule.AreaIntRequest()
        request.expression = self.expression
        request.locations.append(self.locations)
        response = self.service.area_integral(request)
        return response.value

    def centroid(self) -> Any:
        """Get centroid."""
        request = ReductionProtoModule.CentroidRequest()
        request.locations.append(self.locations)
        response = self.service.centroid(request)
        return response.value

    def count(self) -> Any:
        """Get count."""
        request = ReductionProtoModule.CountRequest()
        request.locations.append(self.locations)
        response = self.service.count(request)
        return response.value

    def force(self) -> Any:
        """Get force."""
        request = ReductionProtoModule.ForceRequest()
        request.locations.append(self.locations)
        response = self.service.force(request)
        return response.value

    def mass_average(self) -> Any:
        """Get mass average."""
        request = ReductionProtoModule.MassAveRequest()
        request.expression = self.expression
        request.locations.append(self.locations)
        response = self.service.mass_average(request)
        return response.value

    def mass_flow_average(self) -> Any:
        """Get mass flow average."""
        request = ReductionProtoModule.MassFlowAveRequest()
        request.expression = self.expression
        request.locations.append(self.locations)
        response = self.service.mass_flow_average(request)
        return response.value

    def mass_flow_average_absolute(self) -> Any:
        """Get absolute mass flow average."""
        request = ReductionProtoModule.MassFlowAveAbsRequest()
        request.expression = self.expression
        request.locations.append(self.locations)
        response = self.service.mass_flow_average_absolute(request)
        return response.value

    def mass_flow_integral(self) -> Any:
        """Get mass flow integral."""
        request = ReductionProtoModule.MassFlowIntRequest()
        request.expression = self.expression
        request.locations.append(self.locations)
        response = self.service.mass_flow_integral(request)
        return response.value

    def mass_integral(self) -> Any:
        """Get mass integral."""
        request = ReductionProtoModule.MassIntRequest()
        request.expression = self.expression
        request.locations.append(self.locations)
        response = self.service.mass_integral(request)
        return response.value

    def maximum(self) -> Any:
        """Get maximum."""
        request = ReductionProtoModule.MaximumRequest()
        request.expression = self.expression
        request.locations.append(self.locations)
        response = self.service.maximum(request)
        return response.value

    def minimum(self) -> Any:
        """Get minimum."""
        request = ReductionProtoModule.MinimumRequest()
        request.expression = self.expression
        request.locations.append(self.locations)
        response = self.service.minimum(request)
        return response.value

    def pressure_force(self) -> Any:
        """Get pressure force."""
        request = ReductionProtoModule.PressureForceRequest()
        request.locations.append(self.locations)
        response = self.service.pressure_force(request)
        return response.value

    def viscous_force(self) -> Any:
        """Get viscous force."""
        request = ReductionProtoModule.ViscousForceRequest()
        request.locations.append(self.locations)
        response = self.service.viscous_force(request)
        return response.value

    def volume(self) -> Any:
        """Get volume."""
        request = ReductionProtoModule.VolumeRequest()
        request.locations.append(self.locations)
        response = self.service.volume(request)
        return response.value

    def volume_average(self) -> Any:
        """Get volume average."""
        request = ReductionProtoModule.VolumeAveRequest()
        request.expression = self.expression
        request.locations.append(self.locations)
        response = self.service.volume_average(request)
        return response.value

    def volume_integral(self) -> Any:
        """Get volume integral."""
        request = ReductionProtoModule.VolumeIntRequest()
        request.expression = self.expression
        request.locations.append(self.locations)
        response = self.service.volume_integral(request)
        return response.value
