"""Wrappers over Meshing queries gRPC service of Fluent."""

from typing import Any, List, Tuple

import grpc

from ansys.api.fluent.v0 import meshing_queries_pb2 as MeshingQueriesProtoModule
from ansys.api.fluent.v0 import meshing_queries_pb2_grpc as MeshingQueriesGrpcModule
from ansys.fluent.core.services.error_handler import catch_grpc_error
from ansys.fluent.core.services.interceptors import BatchInterceptor, TracingInterceptor

Path = List[Tuple[str, str]]


class MeshingQueriesService:
    """
    Meshing Queries Service.
    """

    def __init__(self, channel: grpc.Channel, metadata: List[Tuple[str, str]]):
        """__init__ method of MeshingQueriesService class."""
        intercept_channel = grpc.intercept_channel(
            channel, TracingInterceptor(), BatchInterceptor()
        )
        self._stub = MeshingQueriesGrpcModule.MeshingQueriesStub(intercept_channel)
        self._metadata = metadata

    @catch_grpc_error
    def GetFaceZoneAtLocation(
        self, request: MeshingQueriesProtoModule.GetFaceZoneAtLocationRequest
    ) -> MeshingQueriesProtoModule.GetFaceZoneAtLocationResponse:
        """GetFaceZoneAtLocation rpc of MeshingQueriesService."""
        return self._stub.GetFaceZoneAtLocation(request, metadata=self._metadata)

    @catch_grpc_error
    def GetCellZoneAtLocation(
        self, request: MeshingQueriesProtoModule.GetCellZoneAtLocationRequest
    ) -> MeshingQueriesProtoModule.GetCellZoneAtLocationResponse:
        """GetCellZoneAtLocation rpc of MeshingQueriesService."""
        return self._stub.GetCellZoneAtLocation(request, metadata=self._metadata)

    @catch_grpc_error
    def GetZonesOfType(
        self, request: MeshingQueriesProtoModule.GetZonesOfTypeRequest
    ) -> MeshingQueriesProtoModule.GetZonesOfTypeResponse:
        """GetZonesOfType rpc of MeshingQueriesService."""
        return self._stub.GetZonesOfType(request, metadata=self._metadata)

    @catch_grpc_error
    def GetZonesOfGroup(
        self, request: MeshingQueriesProtoModule.GetZonesOfGroupRequest
    ) -> MeshingQueriesProtoModule.GetZonesOfGroupResponse:
        """GetZonesOfGroup rpc of MeshingQueriesService."""
        return self._stub.GetZonesOfGroup(request, metadata=self._metadata)

    @catch_grpc_error
    def GetFaceZonesOfFilter(
        self, request: MeshingQueriesProtoModule.GetFaceZonesOfFilterRequest
    ) -> MeshingQueriesProtoModule.GetFaceZonesOfFilterResponse:
        """GetFaceZonesOfFilter rpc of MeshingQueriesService."""
        return self._stub.GetFaceZonesOfFilter(request, metadata=self._metadata)

    @catch_grpc_error
    def GetCellZonesOfFilter(
        self, request: MeshingQueriesProtoModule.GetCellZonesOfFilterRequest
    ) -> MeshingQueriesProtoModule.GetCellZonesOfFilterResponse:
        """GetCellZonesOfFilter rpc of MeshingQueriesService."""
        return self._stub.GetCellZonesOfFilter(request, metadata=self._metadata)

    @catch_grpc_error
    def GetEdgeZonesOfFilter(
        self, request: MeshingQueriesProtoModule.GetEdgeZonesOfFilterRequest
    ) -> MeshingQueriesProtoModule.GetEdgeZonesOfFilterResponse:
        """GetEdgeZonesOfFilter rpc of MeshingQueriesService."""
        return self._stub.GetEdgeZonesOfFilter(request, metadata=self._metadata)

    @catch_grpc_error
    def GetNodeZonesOfFilter(
        self, request: MeshingQueriesProtoModule.GetNodeZonesOfFilterRequest
    ) -> MeshingQueriesProtoModule.GetNodeZonesOfFilterResponse:
        """GetNodeZonesOfFilter rpc of MeshingQueriesService."""
        return self._stub.GetNodeZonesOfFilter(request, metadata=self._metadata)


class MeshingQueries:
    """
    MeshingQueries.
    """

    def __init__(self, service: MeshingQueriesService):
        """__init__ method of MeshingQueries class."""
        self.service = service

    docstring = None

    def GetFaceZoneAtLocation(self, location) -> Any:
        """GetFaceZoneAtLocation."""
        request = MeshingQueriesProtoModule.GetFaceZoneAtLocationRequest()
        request.location.x = location[0]
        request.location.y = location[1]
        request.location.z = location[2]
        response = self.service.GetFaceZoneAtLocation(request)
        return response.face_zone_id

    def GetCellZoneAtLocation(self, location) -> Any:
        """GetCellZoneAtLocation."""
        request = MeshingQueriesProtoModule.GetCellZoneAtLocationRequest()
        request.location.x = location[0]
        request.location.y = location[1]
        request.location.z = location[2]
        response = self.service.GetCellZoneAtLocation(request)
        return response.cell_zone_id

    def GetZonesOfType(self, zone_type) -> Any:
        """GetZonesOfType."""
        request = MeshingQueriesProtoModule.GetZonesOfTypeRequest()
        request.zone_type = zone_type
        response = self.service.GetZonesOfType(request)
        return response.zone_ids

    def GetZonesOfGroup(self, group) -> Any:
        """GetZonesOfGroup."""
        request = MeshingQueriesProtoModule.GetZonesOfGroupRequest()
        request.group = group
        response = self.service.GetZonesOfGroup(request)
        return response.zone_ids

    def GetFaceZonesOfFilter(self, filter) -> Any:
        """GetFaceZonesOfFilter."""
        request = MeshingQueriesProtoModule.GetFaceZonesOfFilterRequest()
        request.filter = filter
        response = self.service.GetFaceZonesOfFilter(request)
        return response.face_zone_ids

    def GetCellZonesOfFilter(self, filter) -> Any:
        """GetCellZonesOfFilter."""
        request = MeshingQueriesProtoModule.GetCellZonesOfFilterRequest()
        request.filter = filter
        response = self.service.GetCellZonesOfFilter(request)
        return response.cell_zone_ids

    def GetEdgeZonesOfFilter(self, filter) -> Any:
        """GetEdgeZonesOfFilter."""
        request = MeshingQueriesProtoModule.GetEdgeZonesOfFilterRequest()
        request.filter = filter
        response = self.service.GetEdgeZonesOfFilter(request)
        return response.edge_zone_ids

    def GetNodeZonesOfFilter(self, filter) -> Any:
        """GetNodeZonesOfFilter."""
        request = MeshingQueriesProtoModule.GetNodeZonesOfFilterRequest()
        request.filter = filter
        response = self.service.GetNodeZonesOfFilter(request)
        return response.node_zone_ids
