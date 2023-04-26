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

    @catch_grpc_error
    def GetObjectsOfType(
        self, request: MeshingQueriesProtoModule.GetObjectsOfTypeRequest
    ) -> MeshingQueriesProtoModule.GetObjectsOfTypeResponse:
        """GetObjectsOfType rpc of MeshingQueriesService."""
        return self._stub.GetObjectsOfType(request, metadata=self._metadata)

    @catch_grpc_error
    def GetFaceZoneIdListOfObject(
        self, request: MeshingQueriesProtoModule.GetFaceZoneIdListOfObjectRequest
    ) -> MeshingQueriesProtoModule.GetFaceZoneIdListOfObjectResponse:
        """GetFaceZoneIdListOfObject rpc of MeshingQueriesService."""
        return self._stub.GetFaceZoneIdListOfObject(request, metadata=self._metadata)

    @catch_grpc_error
    def GetEdgeZoneIdListOfObject(
        self, request: MeshingQueriesProtoModule.GetEdgeZoneIdListOfObjectRequest
    ) -> MeshingQueriesProtoModule.GetEdgeZoneIdListOfObjectResponse:
        """GetEdgeZoneIdListOfObject rpc of MeshingQueriesService."""
        return self._stub.GetEdgeZoneIdListOfObject(request, metadata=self._metadata)

    @catch_grpc_error
    def GetCellZoneIdListOfObject(
        self, request: MeshingQueriesProtoModule.GetCellZoneIdListOfObjectRequest
    ) -> MeshingQueriesProtoModule.GetCellZoneIdListOfObjectResponse:
        """GetCellZoneIdListOfObject rpc of MeshingQueriesService."""
        return self._stub.GetCellZoneIdListOfObject(request, metadata=self._metadata)

    @catch_grpc_error
    def GetFaceZonesSharedByRegionsOfType(
        self,
        request: MeshingQueriesProtoModule.GetFaceZonesSharedByRegionsOfTypeRequest,
    ) -> MeshingQueriesProtoModule.GetFaceZonesSharedByRegionsOfTypeResponse:
        """GetFaceZonesSharedByRegionsOfType rpc of MeshingQueriesService."""
        return self._stub.GetFaceZonesSharedByRegionsOfType(
            request, metadata=self._metadata
        )

    @catch_grpc_error
    def GetFaceZonesOfRegions(
        self, request: MeshingQueriesProtoModule.GetFaceZonesOfRegionsRequest
    ) -> MeshingQueriesProtoModule.GetFaceZonesOfRegionsResponse:
        """GetFaceZonesOfRegions rpc of MeshingQueriesService."""
        return self._stub.GetFaceZonesOfRegions(request, metadata=self._metadata)

    @catch_grpc_error
    def GetFaceZonesOfLabels(
        self, request: MeshingQueriesProtoModule.GetFaceZonesOfLabelsRequest
    ) -> MeshingQueriesProtoModule.GetFaceZonesOfLabelsResponse:
        """GetFaceZonesOfLabels rpc of MeshingQueriesService."""
        return self._stub.GetFaceZonesOfLabels(request, metadata=self._metadata)

    @catch_grpc_error
    def GetFaceZoneIdListOfLabels(
        self,
        request: MeshingQueriesProtoModule.GetFaceZoneIdListOfLabelsRequest,
    ) -> MeshingQueriesProtoModule.GetFaceZoneIdListOfLabelsResponse:
        """GetFaceZoneIdListOfLabels rpc of MeshingQueriesService."""
        return self._stub.GetFaceZoneIdListOfLabels(request, metadata=self._metadata)

    @catch_grpc_error
    def GetFaceZonesOfObjects(
        self, request: MeshingQueriesProtoModule.GetFaceZonesOfObjectsRequest
    ) -> MeshingQueriesProtoModule.GetFaceZonesOfObjectsResponse:
        """GetFaceZonesOfObjects rpc of MeshingQueriesService."""
        return self._stub.GetFaceZonesOfObjects(request, metadata=self._metadata)

    @catch_grpc_error
    def GetEdgeZonesOfObjects(
        self, request: MeshingQueriesProtoModule.GetEdgeZonesOfObjectsRequest
    ) -> MeshingQueriesProtoModule.GetEdgeZonesOfObjectsResponse:
        """GetEdgeZonesOfObjects rpc of MeshingQueriesService."""
        return self._stub.GetEdgeZonesOfObjects(request, metadata=self._metadata)

    @catch_grpc_error
    def GetFaceZoneIdListOfRegions(
        self,
        request: MeshingQueriesProtoModule.GetFaceZoneIdListOfRegionsRequest,
    ) -> MeshingQueriesProtoModule.GetFaceZoneIdListOfRegionsResponse:
        """GetEdgeZonesOfObjects rpc of MeshingQueriesService."""
        return self._stub.GetFaceZoneIdListOfRegions(request, metadata=self._metadata)

    @catch_grpc_error
    def GetPrismCellZones(
        self,
        request: MeshingQueriesProtoModule.GetPrismCellZonesRequest,
    ) -> MeshingQueriesProtoModule.GetPrismCellZonesResponse:
        """GetPrismCellZones rpc of MeshingQueriesService."""
        return self._stub.GetPrismCellZones(request, metadata=self._metadata)

    @catch_grpc_error
    def GetTetCellZones(
        self,
        request: MeshingQueriesProtoModule.GetTetCellZonesRequest,
    ) -> MeshingQueriesProtoModule.GetTetCellZonesResponse:
        """GetTetCellZones rpc of MeshingQueriesService."""
        return self._stub.GetTetCellZones(request, metadata=self._metadata)

    @catch_grpc_error
    def GetAdjacentCellZones(
        self,
        request: MeshingQueriesProtoModule.GetAdjacentCellZonesRequest,
    ) -> MeshingQueriesProtoModule.GetAdjacentCellZonesResponse:
        """GetAdjacentCellZones rpc of MeshingQueriesService."""
        return self._stub.GetAdjacentCellZones(request, metadata=self._metadata)

    @catch_grpc_error
    def GetAdjacentFaceZones(
        self,
        request: MeshingQueriesProtoModule.GetAdjacentFaceZonesRequest,
    ) -> MeshingQueriesProtoModule.GetAdjacentFaceZonesResponse:
        """GetAdjacentFaceZones rpc of MeshingQueriesService."""
        return self._stub.GetAdjacentFaceZones(request, metadata=self._metadata)

    @catch_grpc_error
    def GetAdjacentInteriorAndBoundaryFaceZones(
        self,
        request: MeshingQueriesProtoModule.GetAdjacentInteriorAndBoundaryFaceZonesRequest,
    ) -> MeshingQueriesProtoModule.GetAdjacentInteriorAndBoundaryFaceZonesResponse:
        """GetAdjacentInteriorAndBoundaryFaceZones rpc of MeshingQueriesService."""
        return self._stub.GetAdjacentInteriorAndBoundaryFaceZones(
            request, metadata=self._metadata
        )

    @catch_grpc_error
    def GetAdjacentZonesByEdgeConnectivity(
        self,
        request: MeshingQueriesProtoModule.GetAdjacentZonesByEdgeConnectivityRequest,
    ) -> MeshingQueriesProtoModule.GetAdjacentZonesByEdgeConnectivityResponse:
        """GetAdjacentZonesByEdgeConnectivity rpc of MeshingQueriesService."""
        return self._stub.GetAdjacentZonesByEdgeConnectivity(
            request, metadata=self._metadata
        )

    @catch_grpc_error
    def GetAdjacentZonesByNodeConnectivity(
        self,
        request: MeshingQueriesProtoModule.GetAdjacentZonesByNodeConnectivityRequest,
    ) -> MeshingQueriesProtoModule.GetAdjacentZonesByNodeConnectivityResponse:
        """GetAdjacentZonesByNodeConnectivity rpc of MeshingQueriesService."""
        return self._stub.GetAdjacentZonesByNodeConnectivity(
            request, metadata=self._metadata
        )

    @catch_grpc_error
    def GetSharedBoundaryZones(
        self,
        request: MeshingQueriesProtoModule.GetSharedBoundaryZonesRequest,
    ) -> MeshingQueriesProtoModule.GetSharedBoundaryZonesResponse:
        """GetSharedBoundaryZones rpc of MeshingQueriesService."""
        return self._stub.GetSharedBoundaryZones(request, metadata=self._metadata)

    @catch_grpc_error
    def GetInteriorZonesConnectedToCellZones(
        self,
        request: MeshingQueriesProtoModule.GetInteriorZonesConnectedToCellZonesRequest,
    ) -> MeshingQueriesProtoModule.GetInteriorZonesConnectedToCellZonesResponse:
        """GetInteriorZonesConnectedToCellZones rpc of MeshingQueriesService."""
        return self._stub.GetInteriorZonesConnectedToCellZones(
            request, metadata=self._metadata
        )

    @catch_grpc_error
    def GetFaceZonesWithZoneSpecificPrismsApplied(
        self,
        request: MeshingQueriesProtoModule.Empty,
    ) -> MeshingQueriesProtoModule.GetFaceZonesWithZoneSpecificPrismsAppliedResponse:
        """GetFaceZonesWithZoneSpecificPrismsApplied rpc of MeshingQueriesService."""
        return self._stub.GetFaceZonesWithZoneSpecificPrismsApplied(
            request, metadata=self._metadata
        )

    @catch_grpc_error
    def GetFaceZonesOfPrismControls(
        self,
        request: MeshingQueriesProtoModule.GetFaceZonesOfPrismControlsRequest,
    ) -> MeshingQueriesProtoModule.GetFaceZonesOfPrismControlsResponse:
        """GetFaceZonesOfPrismControls rpc of MeshingQueriesService."""
        return self._stub.GetFaceZonesOfPrismControls(request, metadata=self._metadata)

    @catch_grpc_error
    def GetBaffles(
        self,
        request: MeshingQueriesProtoModule.GetBafflesRequest,
    ) -> MeshingQueriesProtoModule.GetBafflesResponse:
        """GetBaffles rpc of MeshingQueriesService."""
        return self._stub.GetBaffles(request, metadata=self._metadata)

    @catch_grpc_error
    def GetEmbeddedBaffles(
        self,
        request: MeshingQueriesProtoModule.Empty,
    ) -> MeshingQueriesProtoModule.GetEmbeddedBafflesResponse:
        """GetEmbeddedBaffles rpc of MeshingQueriesService."""
        return self._stub.GetEmbeddedBaffles(request, metadata=self._metadata)

    @catch_grpc_error
    def GetWrappedZones(
        self,
        request: MeshingQueriesProtoModule.Empty,
    ) -> MeshingQueriesProtoModule.GetWrappedZonesResponse:
        """GetWrappedZones rpc of MeshingQueriesService."""
        return self._stub.GetWrappedZones(request, metadata=self._metadata)

    @catch_grpc_error
    def GetUnreferencedEdgeZones(
        self,
        request: MeshingQueriesProtoModule.Empty,
    ) -> MeshingQueriesProtoModule.GetUnreferencedEdgeZonesResponse:
        """GetUnreferencedEdgeZones rpc of MeshingQueriesService."""
        return self._stub.GetUnreferencedEdgeZones(request, metadata=self._metadata)

    @catch_grpc_error
    def GetUnreferencedFaceZones(
        self,
        request: MeshingQueriesProtoModule.Empty,
    ) -> MeshingQueriesProtoModule.GetUnreferencedFaceZonesResponse:
        """GetUnreferencedFaceZones rpc of MeshingQueriesService."""
        return self._stub.GetUnreferencedFaceZones(request, metadata=self._metadata)

    @catch_grpc_error
    def GetUnreferencedCellZones(
        self,
        request: MeshingQueriesProtoModule.Empty,
    ) -> MeshingQueriesProtoModule.GetUnreferencedCellZonesResponse:
        """GetUnreferencedCellZones rpc of MeshingQueriesService."""
        return self._stub.GetUnreferencedCellZones(request, metadata=self._metadata)

    @catch_grpc_error
    def GetUnreferencedEdgeZonesOfFilter(
        self,
        request: MeshingQueriesProtoModule.GetUnreferencedEdgeZonesOfFilterRequest,
    ) -> MeshingQueriesProtoModule.GetUnreferencedEdgeZonesOfFilterResponse:
        """GetUnreferencedEdgeZonesOfFilter rpc of MeshingQueriesService."""
        return self._stub.GetUnreferencedEdgeZonesOfFilter(
            request, metadata=self._metadata
        )

    @catch_grpc_error
    def GetUnreferencedFaceZonesOfFilter(
        self,
        request: MeshingQueriesProtoModule.GetUnreferencedFaceZonesOfFilterRequest,
    ) -> MeshingQueriesProtoModule.GetUnreferencedFaceZonesOfFilterResponse:
        """GetUnreferencedFaceZonesOfFilter rpc of MeshingQueriesService."""
        return self._stub.GetUnreferencedFaceZonesOfFilter(
            request, metadata=self._metadata
        )

    @catch_grpc_error
    def GetUnreferencedCellZonesOfFilter(
        self,
        request: MeshingQueriesProtoModule.GetUnreferencedCellZonesOfFilterRequest,
    ) -> MeshingQueriesProtoModule.GetUnreferencedCellZonesOfFilterResponse:
        """GetUnreferencedCellZonesOfFilter rpc of MeshingQueriesService."""
        return self._stub.GetUnreferencedCellZonesOfFilter(
            request, metadata=self._metadata
        )

    @catch_grpc_error
    def GetUnreferencedEdgeZoneIdListOfPattern(
        self,
        request: MeshingQueriesProtoModule.GetUnreferencedEdgeZoneIdListOfPatternRequest,
    ) -> MeshingQueriesProtoModule.GetUnreferencedEdgeZoneIdListOfPatternResponse:
        """GetUnreferencedEdgeZoneIdListOfPattern rpc of MeshingQueriesService."""
        return self._stub.GetUnreferencedEdgeZoneIdListOfPattern(
            request, metadata=self._metadata
        )

    @catch_grpc_error
    def GetUnreferencedFaceZoneIdListOfPattern(
        self,
        request: MeshingQueriesProtoModule.GetUnreferencedFaceZoneIdListOfPatternRequest,
    ) -> MeshingQueriesProtoModule.GetUnreferencedFaceZoneIdListOfPatternResponse:
        """GetUnreferencedFaceZoneIdListOfPattern rpc of MeshingQueriesService."""
        return self._stub.GetUnreferencedFaceZoneIdListOfPattern(
            request, metadata=self._metadata
        )

    @catch_grpc_error
    def GetUnreferencedCellZoneIdListOfPattern(
        self,
        request: MeshingQueriesProtoModule.GetUnreferencedCellZoneIdListOfPatternRequest,
    ) -> MeshingQueriesProtoModule.GetUnreferencedCellZoneIdListOfPatternResponse:
        """GetUnreferencedCellZoneIdListOfPattern rpc of MeshingQueriesService."""
        return self._stub.GetUnreferencedCellZoneIdListOfPattern(
            request, metadata=self._metadata
        )

    @catch_grpc_error
    def GetMaxsizeCellZoneByVolume(
        self,
        request: MeshingQueriesProtoModule.GetMaxsizeCellZoneByVolumeRequest,
    ) -> MeshingQueriesProtoModule.GetMaxsizeCellZoneByVolumeResponse:
        """GetMaxsizeCellZoneByVolume rpc of MeshingQueriesService."""
        return self._stub.GetMaxsizeCellZoneByVolume(request, metadata=self._metadata)

    @catch_grpc_error
    def GetMaxsizeCellZoneByCount(
        self,
        request: MeshingQueriesProtoModule.GetMaxsizeCellZoneByCountRequest,
    ) -> MeshingQueriesProtoModule.GetMaxsizeCellZoneByCountResponse:
        """GetMaxsizeCellZoneByCount rpc of MeshingQueriesService."""
        return self._stub.GetMaxsizeCellZoneByCount(request, metadata=self._metadata)

    @catch_grpc_error
    def GetMinsizeFaceZoneByArea(
        self,
        request: MeshingQueriesProtoModule.GetMinsizeFaceZoneByAreaRequest,
    ) -> MeshingQueriesProtoModule.GetMinsizeFaceZoneByAreaResponse:
        """GetMinsizeFaceZoneByArea rpc of MeshingQueriesService."""
        return self._stub.GetMinsizeFaceZoneByArea(request, metadata=self._metadata)

    @catch_grpc_error
    def GetMinsizeFaceZoneByCount(
        self,
        request: MeshingQueriesProtoModule.GetMinsizeFaceZoneByCountRequest,
    ) -> MeshingQueriesProtoModule.GetMinsizeFaceZoneByCountResponse:
        """GetMinsizeFaceZoneByCount rpc of MeshingQueriesService."""
        return self._stub.GetMinsizeFaceZoneByCount(request, metadata=self._metadata)

    @catch_grpc_error
    def GetFaceZoneListByMaximumEntityCount(
        self,
        request: MeshingQueriesProtoModule.GetFaceZoneListByMaximumEntityCountRequest,
    ) -> MeshingQueriesProtoModule.GetFaceZoneListByMaximumEntityCountResponse:
        """GetFaceZoneListByMaximumEntityCount rpc of MeshingQueriesService."""
        return self._stub.GetFaceZoneListByMaximumEntityCount(
            request, metadata=self._metadata
        )

    @catch_grpc_error
    def GetEdgeZoneListByMaximumEntityCount(
        self,
        request: MeshingQueriesProtoModule.GetEdgeZoneListByMaximumEntityCountRequest,
    ) -> MeshingQueriesProtoModule.GetEdgeZoneListByMaximumEntityCountResponse:
        """GetEdgeZoneListByMaximumEntityCount rpc of MeshingQueriesService."""
        return self._stub.GetEdgeZoneListByMaximumEntityCount(
            request, metadata=self._metadata
        )

    @catch_grpc_error
    def GetCellZoneListByMaximumEntityCount(
        self,
        request: MeshingQueriesProtoModule.GetCellZoneListByMaximumEntityCountRequest,
    ) -> MeshingQueriesProtoModule.GetCellZoneListByMaximumEntityCountResponse:
        """GetCellZoneListByMaximumEntityCount rpc of MeshingQueriesService."""
        return self._stub.GetCellZoneListByMaximumEntityCount(
            request, metadata=self._metadata
        )

    @catch_grpc_error
    def GetFaceZoneListByMaximumZoneArea(
        self,
        request: MeshingQueriesProtoModule.GetFaceZoneListByMaximumZoneAreaRequest,
    ) -> MeshingQueriesProtoModule.GetFaceZoneListByMaximumZoneAreaResponse:
        """GetFaceZoneListByMaximumZoneArea rpc of MeshingQueriesService."""
        return self._stub.GetFaceZoneListByMaximumZoneArea(
            request, metadata=self._metadata
        )

    @catch_grpc_error
    def GetFaceZoneListByMinimumZoneArea(
        self,
        request: MeshingQueriesProtoModule.GetFaceZoneListByMinimumZoneAreaRequest,
    ) -> MeshingQueriesProtoModule.GetFaceZoneListByMinimumZoneAreaResponse:
        """GetFaceZoneListByMinimumZoneArea rpc of MeshingQueriesService."""
        return self._stub.GetFaceZoneListByMinimumZoneArea(
            request, metadata=self._metadata
        )

    @catch_grpc_error
    def GetZonesWithFreeFaces(
        self,
        request: MeshingQueriesProtoModule.GetZonesWithFreeFacesRequest,
    ) -> MeshingQueriesProtoModule.GetZonesWithFreeFacesResponse:
        """GetZonesWithFreeFaces rpc of MeshingQueriesService."""
        return self._stub.GetZonesWithFreeFaces(request, metadata=self._metadata)

    @catch_grpc_error
    def GetZonesWithFreeFaces(
        self,
        request: MeshingQueriesProtoModule.GetZonesWithFreeFacesRequest,
    ) -> MeshingQueriesProtoModule.GetZonesWithFreeFacesResponse:
        """GetZonesWithFreeFaces rpc of MeshingQueriesService."""
        return self._stub.GetZonesWithFreeFaces(request, metadata=self._metadata)

    @catch_grpc_error
    def GetZonesWithMultiFaces(
        self,
        request: MeshingQueriesProtoModule.GetZonesWithMultiFacesRequest,
    ) -> MeshingQueriesProtoModule.GetZonesWithMultiFacesResponse:
        """GetZonesWithMultiFaces rpc of MeshingQueriesService."""
        return self._stub.GetZonesWithMultiFaces(request, metadata=self._metadata)

    @catch_grpc_error
    def GetOverlappingFaceZones(
        self,
        request: MeshingQueriesProtoModule.GetOverlappingFaceZonesRequest,
    ) -> MeshingQueriesProtoModule.GetOverlappingFaceZonesResponse:
        """GetOverlappingFaceZones rpc of MeshingQueriesService."""
        return self._stub.GetOverlappingFaceZones(request, metadata=self._metadata)

    @catch_grpc_error
    def GetZonesWithMultiFaces(
        self,
        request: MeshingQueriesProtoModule.GetZonesWithMultiFacesRequest,
    ) -> MeshingQueriesProtoModule.GetZonesWithMultiFacesResponse:
        """GetZonesWithMultiFaces rpc of MeshingQueriesService."""
        return self._stub.GetZonesWithMultiFaces(request, metadata=self._metadata)

    @catch_grpc_error
    def GetZonesWithMarkedFaces(
        self,
        request: MeshingQueriesProtoModule.GetZonesWithMarkedFacesRequest,
    ) -> MeshingQueriesProtoModule.GetZonesWithMarkedFacesResponse:
        """GetZonesWithMarkedFaces rpc of MeshingQueriesService."""
        return self._stub.GetZonesWithMarkedFaces(request, metadata=self._metadata)

    @catch_grpc_error
    def GetZonesWithMarkedFaces(
        self,
        request: MeshingQueriesProtoModule.GetZonesWithMarkedFacesRequest,
    ) -> MeshingQueriesProtoModule.GetZonesWithMarkedFacesResponse:
        """GetZonesWithMarkedFaces rpc of MeshingQueriesService."""
        return self._stub.GetZonesWithMarkedFaces(request, metadata=self._metadata)

    @catch_grpc_error
    def GetAllObjectNameList(
        self,
        request: MeshingQueriesProtoModule.Empty,
    ) -> MeshingQueriesProtoModule.GetAllObjectNameListResponse:
        """GetAllObjectNameList rpc of MeshingQueriesService."""
        return self._stub.GetAllObjectNameList(request, metadata=self._metadata)

    @catch_grpc_error
    def GetObjectNameListOfType(
        self,
        request: MeshingQueriesProtoModule.GetObjectNameListOfTypeRequest,
    ) -> MeshingQueriesProtoModule.GetObjectNameListOfTypeResponse:
        """GetObjectNameListOfType rpc of MeshingQueriesService."""
        return self._stub.GetObjectNameListOfType(request, metadata=self._metadata)

    @catch_grpc_error
    def GetObjectsOfFilter(
        self,
        request: MeshingQueriesProtoModule.GetObjectsOfFilterRequest,
    ) -> MeshingQueriesProtoModule.GetObjectsOfFilterResponse:
        """GetObjectsOfFilter rpc of MeshingQueriesService."""
        return self._stub.GetObjectsOfFilter(request, metadata=self._metadata)

    @catch_grpc_error
    def GetObjectsOfFilter(
        self,
        request: MeshingQueriesProtoModule.GetObjectsOfFilterRequest,
    ) -> MeshingQueriesProtoModule.GetObjectsOfFilterResponse:
        """GetObjectsOfFilter rpc of MeshingQueriesService."""
        return self._stub.GetObjectsOfFilter(request, metadata=self._metadata)

    @catch_grpc_error
    def GetRegionsOfObject(
        self,
        request: MeshingQueriesProtoModule.GetRegionsOfObjectRequest,
    ) -> MeshingQueriesProtoModule.GetRegionsOfObjectResponse:
        """GetRegionsOfObject rpc of MeshingQueriesService."""
        return self._stub.GetRegionsOfObject(request, metadata=self._metadata)

    @catch_grpc_error
    def GetRegionNameListOfObject(
        self,
        request: MeshingQueriesProtoModule.GetRegionNameListOfObjectRequest,
    ) -> MeshingQueriesProtoModule.GetRegionNameListOfObjectResponse:
        """GetRegionNameListOfObject rpc of MeshingQueriesService."""
        return self._stub.GetRegionNameListOfObject(request, metadata=self._metadata)

    @catch_grpc_error
    def SortRegionsByVolume(
        self,
        request: MeshingQueriesProtoModule.SortRegionsByVolumeRequest,
    ) -> MeshingQueriesProtoModule.SortRegionsByVolumeResponse:
        """SortRegionsByVolume rpc of MeshingQueriesService."""
        return self._stub.SortRegionsByVolume(request, metadata=self._metadata)

    @catch_grpc_error
    def GetRegionVolume(
        self,
        request: MeshingQueriesProtoModule.GetRegionVolumeRequest,
    ) -> MeshingQueriesProtoModule.GetRegionVolumeResponse:
        """GetRegionVolume rpc of MeshingQueriesService."""
        return self._stub.GetRegionVolume(request, metadata=self._metadata)

    @catch_grpc_error
    def GetRegionsOfFilter(
        self,
        request: MeshingQueriesProtoModule.GetRegionsOfFilterRequest,
    ) -> MeshingQueriesProtoModule.GetRegionsOfFilterResponse:
        """GetRegionsOfFilter rpc of MeshingQueriesService."""
        return self._stub.GetRegionsOfFilter(request, metadata=self._metadata)

    @catch_grpc_error
    def GetRegionNameListOfPattern(
        self,
        request: MeshingQueriesProtoModule.GetRegionNameListOfPatternRequest,
    ) -> MeshingQueriesProtoModule.GetRegionNameListOfPatternResponse:
        """GetRegionNameListOfPattern rpc of MeshingQueriesService."""
        return self._stub.GetRegionNameListOfPattern(request, metadata=self._metadata)

    @catch_grpc_error
    def GetRegionsOfFaceZones(
        self,
        request: MeshingQueriesProtoModule.GetRegionsOfFaceZonesRequest,
    ) -> MeshingQueriesProtoModule.GetRegionsOfFaceZonesResponse:
        """GetRegionsOfFaceZones rpc of MeshingQueriesService."""
        return self._stub.GetRegionsOfFaceZones(request, metadata=self._metadata)

    @catch_grpc_error
    def FindJoinPairs(
        self,
        request: MeshingQueriesProtoModule.FindJoinPairsRequest,
    ) -> MeshingQueriesProtoModule.FindJoinPairsResponse:
        """FindJoinPairs rpc of MeshingQueriesService."""
        return self._stub.FindJoinPairs(request, metadata=self._metadata)

    @catch_grpc_error
    def GetRegionNameListOfFaceZones(
        self,
        request: MeshingQueriesProtoModule.GetRegionNameListOfFaceZonesRequest,
    ) -> MeshingQueriesProtoModule.GetRegionNameListOfFaceZonesResponse:
        """GetRegionNameListOfFaceZones rpc of MeshingQueriesService."""
        return self._stub.GetRegionNameListOfFaceZones(request, metadata=self._metadata)


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

    def GetZonesOfType(self, type) -> Any:
        """GetZonesOfType."""
        request = MeshingQueriesProtoModule.GetZonesOfTypeRequest()
        request.type = type
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

    def GetObjectsOfType(self, type) -> Any:
        """GetObjectsOfType."""
        request = MeshingQueriesProtoModule.GetObjectsOfTypeRequest()
        request.type = type
        response = self.service.GetObjectsOfType(request)
        return response.objects

    def GetFaceZoneIdListOfObject(self, object) -> Any:
        """GetFaceZoneIdListOfObject."""
        request = MeshingQueriesProtoModule.GetFaceZoneIdListOfObjectRequest()
        request.object = object
        response = self.service.GetFaceZoneIdListOfObject(request)
        return response.face_zone_ids

    def GetEdgeZoneIdListOfObject(self, object) -> Any:
        """GetEdgeZoneIdListOfObject."""
        request = MeshingQueriesProtoModule.GetEdgeZoneIdListOfObjectRequest()
        request.object = object
        response = self.service.GetEdgeZoneIdListOfObject(request)
        return response.edge_zone_ids

    def GetCellZoneIdListOfObject(self, object) -> Any:
        """GetCellZoneIdListOfObject."""
        request = MeshingQueriesProtoModule.GetCellZoneIdListOfObjectRequest()
        request.object = object
        response = self.service.GetCellZoneIdListOfObject(request)
        return response.cell_zone_ids

    def GetFaceZonesSharedByRegionsOfType(self, mesh_object, region_type) -> Any:
        """GetFaceZonesSharedByRegionsOfType."""
        request = MeshingQueriesProtoModule.GetFaceZonesSharedByRegionsOfTypeRequest()
        request.mesh_object = mesh_object
        request.region_type = region_type
        response = self.service.GetFaceZonesSharedByRegionsOfType(request)
        return response.shared_face_zone_ids

    def GetFaceZonesOfRegions(self, object, region_name_list) -> Any:
        """GetFaceZonesOfRegions."""
        request = MeshingQueriesProtoModule.GetFaceZonesOfRegionsRequest()
        request.object = object
        for region in region_name_list:
            request.regions.append(region)
        response = self.service.GetFaceZonesOfRegions(request)
        return response.zone_ids

    def GetFaceZonesOfLabels(self, object, label_name_list) -> Any:
        """GetFaceZonesOfLabels."""
        request = MeshingQueriesProtoModule.GetFaceZonesOfLabelsRequest()
        request.object = object
        for label in label_name_list:
            request.labels.append(label)
        response = self.service.GetFaceZonesOfLabels(request)
        return response.zone_ids

    def GetFaceZoneIdListOfLabels(self, object, zone_label_list) -> Any:
        """GetFaceZoneIdListOfLabels."""
        request = MeshingQueriesProtoModule.GetFaceZoneIdListOfLabelsRequest()
        request.object = object
        for zone_label in zone_label_list:
            request.labels.append(zone_label)
        response = self.service.GetFaceZoneIdListOfLabels(request)
        return response.zone_ids

    def GetFaceZonesOfObjects(self, object_list) -> Any:
        """GetFaceZonesOfObjects."""
        request = MeshingQueriesProtoModule.GetFaceZonesOfObjectsRequest()
        for object in object_list:
            request.object_list.append(object)
        response = self.service.GetFaceZonesOfObjects(request)
        return response.face_zone_ids

    def GetEdgeZonesOfObjects(self, object_list) -> Any:
        """GetEdgeZonesOfObjects."""
        request = MeshingQueriesProtoModule.GetEdgeZonesOfObjectsRequest()
        for object in object_list:
            request.object_list.append(object)
        response = self.service.GetEdgeZonesOfObjects(request)
        return response.edge_zone_ids

    def GetFaceZoneIdListOfRegions(self, object, region_list) -> Any:
        """GetFaceZoneIdListOfRegions."""
        request = MeshingQueriesProtoModule.GetFaceZoneIdListOfRegionsRequest()
        request.object = object
        for region in region_list:
            request.labels.append(region)
        response = self.service.GetFaceZoneIdListOfRegions(request)
        return response.zone_ids

    def GetPrismCellZones(self, list_or_pattern) -> Any:
        """GetPrismCellZones."""
        request = MeshingQueriesProtoModule.GetPrismCellZonesRequest()
        if isinstance(list_or_pattern, str):
            request.zone_name_or_pattern = list_or_pattern
        elif isinstance(list_or_pattern, list):
            for items in list_or_pattern:
                request.zones.append(items)
        response = self.service.GetPrismCellZones(request)
        return response.prism_cell_zones

    def GetTetCellZones(self, list_or_pattern) -> Any:
        """GetTetCellZones."""
        request = MeshingQueriesProtoModule.GetTetCellZonesRequest()
        if isinstance(list_or_pattern, str):
            request.zone_name_or_pattern = list_or_pattern
        elif isinstance(list_or_pattern, list):
            for items in list_or_pattern:
                request.zones.append(items)
        response = self.service.GetTetCellZones(request)
        return response.tet_cell_zones

    def GetAdjacentCellZones(self, list_or_name_or_pattern) -> Any:
        """GetAdjacentCellZones."""
        request = MeshingQueriesProtoModule.GetAdjacentCellZonesRequest()
        if isinstance(list_or_name_or_pattern, str):
            request.zone_name_or_pattern = list_or_name_or_pattern
        elif isinstance(list_or_name_or_pattern, list):
            for items in list_or_name_or_pattern:
                request.face_zone_ids.append(items)
        response = self.service.GetAdjacentCellZones(request)
        return response.adjacent_cell_zones

    def GetAdjacentFaceZones(self, list_or_name_or_pattern) -> Any:
        """GetAdjacentFaceZones."""
        request = MeshingQueriesProtoModule.GetAdjacentFaceZonesRequest()
        if isinstance(list_or_name_or_pattern, str):
            request.zone_name_or_pattern = list_or_name_or_pattern
        elif isinstance(list_or_name_or_pattern, list):
            for items in list_or_name_or_pattern:
                request.cell_zone_ids.append(items)
        response = self.service.GetAdjacentFaceZones(request)
        return response.adjacent_boundary_face_zones

    def GetAdjacentInteriorAndBoundaryFaceZones(self, list_or_name_or_pattern) -> Any:
        """GetAdjacentInteriorAndBoundaryFaceZones."""
        request = (
            MeshingQueriesProtoModule.GetAdjacentInteriorAndBoundaryFaceZonesRequest()
        )
        if isinstance(list_or_name_or_pattern, str):
            request.zone_name_or_pattern = list_or_name_or_pattern
        elif isinstance(list_or_name_or_pattern, list):
            for items in list_or_name_or_pattern:
                request.cell_zone_ids.append(items)
        response = self.service.GetAdjacentInteriorAndBoundaryFaceZones(request)
        return response.adjacent_interior_and_boundary_face_zones

    def GetAdjacentZonesByEdgeConnectivity(self, list_or_name_or_pattern) -> Any:
        """GetAdjacentZonesByEdgeConnectivity."""
        request = MeshingQueriesProtoModule.GetAdjacentZonesByEdgeConnectivityRequest()
        if isinstance(list_or_name_or_pattern, str):
            request.zone_name_or_pattern = list_or_name_or_pattern
        elif isinstance(list_or_name_or_pattern, list):
            for items in list_or_name_or_pattern:
                request.zone_ids.append(items)
        response = self.service.GetAdjacentZonesByEdgeConnectivity(request)
        return response.adjacent_zone_ids

    def GetAdjacentZonesByNodeConnectivity(self, list_or_name_or_pattern) -> Any:
        """GetAdjacentZonesByNodeConnectivity."""
        request = MeshingQueriesProtoModule.GetAdjacentZonesByNodeConnectivityRequest()
        if isinstance(list_or_name_or_pattern, str):
            request.zone_name_or_pattern = list_or_name_or_pattern
        elif isinstance(list_or_name_or_pattern, list):
            for items in list_or_name_or_pattern:
                request.zone_ids.append(items)
        response = self.service.GetAdjacentZonesByNodeConnectivity(request)
        return response.adjacent_zone_ids

    def GetSharedBoundaryZones(self, list_or_name_or_pattern) -> Any:
        """GetSharedBoundaryZones."""
        request = MeshingQueriesProtoModule.GetSharedBoundaryZonesRequest()
        if isinstance(list_or_name_or_pattern, str):
            request.cell_zone_name_or_pattern = list_or_name_or_pattern
        elif isinstance(list_or_name_or_pattern, list):
            for items in list_or_name_or_pattern:
                request.cell_zone_ids.append(items)
        response = self.service.GetSharedBoundaryZones(request)
        return response.shared_boundary_zone_ids

    def GetInteriorZonesConnectedToCellZones(self, list_or_name_or_pattern) -> Any:
        """GetInteriorZonesConnectedToCellZones."""
        request = (
            MeshingQueriesProtoModule.GetInteriorZonesConnectedToCellZonesRequest()
        )
        if isinstance(list_or_name_or_pattern, str):
            request.cell_zone_name_or_pattern = list_or_name_or_pattern
        elif isinstance(list_or_name_or_pattern, list):
            for items in list_or_name_or_pattern:
                request.face_zone_ids.append(items)
        response = self.service.GetInteriorZonesConnectedToCellZones(request)
        return response.interior_zone_ids

    def GetFaceZonesWithZoneSpecificPrismsApplied(self) -> Any:
        """GetFaceZonesWithZoneSpecificPrismsApplied."""
        request = MeshingQueriesProtoModule.Empty()
        response = self.service.GetFaceZonesWithZoneSpecificPrismsApplied(request)
        return response.face_zone_ids

    def GetFaceZonesOfPrismControls(self, control_name) -> Any:
        """GetInteriorZonesConnectedToCellZones."""
        request = MeshingQueriesProtoModule.GetFaceZonesOfPrismControlsRequest()
        request.control_name = control_name
        response = self.service.GetFaceZonesOfPrismControls(request)
        return response.face_zone_ids

    def GetBaffles(self, face_zone_list) -> Any:
        """GetBaffles."""
        request = MeshingQueriesProtoModule.GetBafflesRequest()
        for items in face_zone_list:
            request.face_zone_ids.append(items)
        response = self.service.GetBaffles(request)
        return response.baffle_zone_ids

    def GetEmbeddedBaffles(self) -> Any:
        """GetEmbeddedBaffles."""
        request = MeshingQueriesProtoModule.Empty()
        response = self.service.GetEmbeddedBaffles(request)
        return response.embedded_baffles_zone_ids

    def GetWrappedZones(self) -> Any:
        """GetWrappedZones."""
        request = MeshingQueriesProtoModule.Empty()
        response = self.service.GetWrappedZones(request)
        return response.wrapped_face_zone_ids

    def GetUnreferencedEdgeZones(self) -> Any:
        """GetUnreferencedEdgeZones."""
        request = MeshingQueriesProtoModule.Empty()
        response = self.service.GetUnreferencedEdgeZones(request)
        return response.unreferenced_edge_zone_ids

    def GetUnreferencedFaceZones(self) -> Any:
        """GetUnreferencedFaceZones."""
        request = MeshingQueriesProtoModule.Empty()
        response = self.service.GetUnreferencedFaceZones(request)
        return response.unreferenced_face_zone_ids

    def GetUnreferencedCellZones(self) -> Any:
        """GetUnreferencedCellZones."""
        request = MeshingQueriesProtoModule.Empty()
        response = self.service.GetUnreferencedCellZones(request)
        return response.unreferenced_cell_zone_ids

    def GetUnreferencedEdgeZonesOfFilter(self, filter) -> Any:
        """GetUnreferencedEdgeZonesOfFilter."""
        request = MeshingQueriesProtoModule.GetUnreferencedEdgeZonesOfFilterRequest()
        request.filter = filter
        response = self.service.GetUnreferencedEdgeZonesOfFilter(request)
        return response.unreferenced_edge_zone_ids

    def GetUnreferencedFaceZonesOfFilter(self, filter) -> Any:
        """GetUnreferencedFaceZonesOfFilter."""
        request = MeshingQueriesProtoModule.GetUnreferencedFaceZonesOfFilterRequest()
        request.filter = filter
        response = self.service.GetUnreferencedFaceZonesOfFilter(request)
        return response.unreferenced_face_zone_ids

    def GetUnreferencedCellZonesOfFilter(self, filter) -> Any:
        """GetUnreferencedEdgeZonesOfFilter."""
        request = MeshingQueriesProtoModule.GetUnreferencedCellZonesOfFilterRequest()
        request.filter = filter
        response = self.service.GetUnreferencedCellZonesOfFilter(request)
        return response.unreferenced_cell_zone_ids

    def GetUnreferencedEdgeZoneIdListOfPattern(self, pattern) -> Any:
        """GetUnreferencedEdgeZoneIdListOfPattern."""
        request = (
            MeshingQueriesProtoModule.GetUnreferencedEdgeZoneIdListOfPatternRequest()
        )
        request.pattern = pattern
        response = self.service.GetUnreferencedEdgeZoneIdListOfPattern(request)
        return response.unreferenced_edge_zone_ids

    def GetUnreferencedFaceZoneIdListOfPattern(self, pattern) -> Any:
        """GetUnreferencedFaceZoneIdListOfPattern."""
        request = (
            MeshingQueriesProtoModule.GetUnreferencedFaceZoneIdListOfPatternRequest()
        )
        request.pattern = pattern
        response = self.service.GetUnreferencedFaceZoneIdListOfPattern(request)
        return response.unreferenced_face_zone_ids

    def GetUnreferencedCellZoneIdListOfPattern(self, pattern) -> Any:
        """GetUnreferencedCellZoneIdListOfPattern."""
        request = (
            MeshingQueriesProtoModule.GetUnreferencedCellZoneIdListOfPatternRequest()
        )
        request.pattern = pattern
        response = self.service.GetUnreferencedCellZoneIdListOfPattern(request)
        return response.unreferenced_cell_zone_ids

    def GetMaxsizeCellZoneByVolume(self, list_or_pattern) -> Any:
        """GetMaxsizeCellZoneByVolume."""
        request = MeshingQueriesProtoModule.GetMaxsizeCellZoneByVolumeRequest()
        if isinstance(list_or_pattern, str):
            request.cell_zone_pattern = list_or_pattern
        elif isinstance(list_or_pattern, list):
            if isinstance(list_or_pattern[0], int):
                for items in list_or_pattern:
                    request.cell_zone_ids.append(items)
            elif isinstance(list_or_pattern[0], str):
                for items in list_or_pattern:
                    request.cell_zone_names.append(items)
        response = self.service.GetMaxsizeCellZoneByVolume(request)
        return response.cell_zone_id

    def GetMaxsizeCellZoneByCount(self, list_or_pattern) -> Any:
        """GetMaxsizeCellZoneByCount."""
        request = MeshingQueriesProtoModule.GetMaxsizeCellZoneByCountRequest()
        if isinstance(list_or_pattern, str):
            request.cell_zone_pattern = list_or_pattern
        elif isinstance(list_or_pattern, list):
            if isinstance(list_or_pattern[0], int):
                for items in list_or_pattern:
                    request.cell_zone_ids.append(items)
            elif isinstance(list_or_pattern[0], str):
                for items in list_or_pattern:
                    request.cell_zone_names.append(items)
        response = self.service.GetMaxsizeCellZoneByCount(request)
        return response.cell_zone_id

    def GetMinsizeFaceZoneByArea(self, list_or_pattern) -> Any:
        """GetMinsizeFaceZoneByArea."""
        request = MeshingQueriesProtoModule.GetMinsizeFaceZoneByAreaRequest()
        if isinstance(list_or_pattern, str):
            request.face_zone_pattern = list_or_pattern
        elif isinstance(list_or_pattern, list):
            if isinstance(list_or_pattern[0], int):
                for items in list_or_pattern:
                    request.face_zone_ids.append(items)
            elif isinstance(list_or_pattern[0], str):
                for items in list_or_pattern:
                    request.face_zone_names.append(items)
        response = self.service.GetMinsizeFaceZoneByArea(request)
        return response.face_zone_id

    def GetMinsizeFaceZoneByCount(self, list_or_pattern) -> Any:
        """GetMinsizeFaceZoneByCount."""
        request = MeshingQueriesProtoModule.GetMinsizeFaceZoneByCountRequest()
        if isinstance(list_or_pattern, str):
            request.face_zone_pattern = list_or_pattern
        elif isinstance(list_or_pattern, list):
            if isinstance(list_or_pattern[0], int):
                for items in list_or_pattern:
                    request.face_zone_ids.append(items)
            elif isinstance(list_or_pattern[0], str):
                for items in list_or_pattern:
                    request.face_zone_names.append(items)
        response = self.service.GetMinsizeFaceZoneByCount(request)
        return response.face_zone_id

    def GetFaceZoneListByMaximumEntityCount(
        self, max_entity_count, only_boundary
    ) -> Any:
        """GetFaceZoneListByMaximumEntityCount."""
        request = MeshingQueriesProtoModule.GetFaceZoneListByMaximumEntityCountRequest()
        request.maximum_entity_count = max_entity_count
        request.only_boundary = only_boundary
        response = self.service.GetFaceZoneListByMaximumEntityCount(request)
        return response.face_zone_ids

    def GetEdgeZoneListByMaximumEntityCount(
        self, max_entity_count, only_boundary
    ) -> Any:
        """GetEdgeZoneListByMaximumEntityCount."""
        request = MeshingQueriesProtoModule.GetEdgeZoneListByMaximumEntityCountRequest()
        request.maximum_entity_count = max_entity_count
        request.only_boundary = only_boundary
        response = self.service.GetEdgeZoneListByMaximumEntityCount(request)
        return response.edge_zone_ids

    def GetCellZoneListByMaximumEntityCount(self, maximum_entity_count) -> Any:
        """GetCellZoneListByMaximumEntityCount."""
        request = MeshingQueriesProtoModule.GetCellZoneListByMaximumEntityCountRequest()
        request.maximum_entity_count = maximum_entity_count
        response = self.service.GetCellZoneListByMaximumEntityCount(request)
        return response.cell_zone_ids

    def GetFaceZoneListByMaximumZoneArea(self, maximum_zone_area) -> Any:
        """GetFaceZoneListByMaximumZoneArea."""
        request = MeshingQueriesProtoModule.GetFaceZoneListByMaximumZoneAreaRequest()
        request.maximum_zone_area = maximum_zone_area
        response = self.service.GetFaceZoneListByMaximumZoneArea(request)
        return response.face_zone_ids

    def GetFaceZoneListByMinimumZoneArea(self, minimum_zone_area) -> Any:
        """GetFaceZoneListByMinimumZoneArea."""
        request = MeshingQueriesProtoModule.GetFaceZoneListByMinimumZoneAreaRequest()
        request.minimum_zone_area = minimum_zone_area
        response = self.service.GetFaceZoneListByMinimumZoneArea(request)
        return response.face_zone_ids

    def GetZonesWithFreeFaces(self, list_or_pattern) -> Any:
        """GetZonesWithFreeFaces."""
        request = MeshingQueriesProtoModule.GetZonesWithFreeFacesRequest()
        if isinstance(list_or_pattern, str):
            request.face_zone_pattern = list_or_pattern
        elif isinstance(list_or_pattern, list):
            if isinstance(list_or_pattern[0], int):
                for items in list_or_pattern:
                    request.face_zone_ids.append(items)
            elif isinstance(list_or_pattern[0], str):
                for items in list_or_pattern:
                    request.face_zone_names.append(items)
        response = self.service.GetZonesWithFreeFaces(request)
        return response.zones_with_free_faces

    def GetZonesWithMultiFaces(self, list_or_pattern) -> Any:
        """GetZonesWithMultiFaces."""
        request = MeshingQueriesProtoModule.GetZonesWithMultiFacesRequest()
        if isinstance(list_or_pattern, str):
            request.face_zone_pattern = list_or_pattern
        elif isinstance(list_or_pattern, list):
            if isinstance(list_or_pattern[0], int):
                for items in list_or_pattern:
                    request.face_zone_ids.append(items)
            elif isinstance(list_or_pattern[0], str):
                for items in list_or_pattern:
                    request.face_zone_names.append(items)
        response = self.service.GetZonesWithMultiFaces(request)
        return response.zones_with_multi_connected_faces

    def GetOverlappingFaceZones(
        self, zone_name_pattern, area_tolerance, distance_tolerance
    ) -> Any:
        """GetOverlappingFaceZones."""
        request = MeshingQueriesProtoModule.GetOverlappingFaceZonesRequest()
        request.face_zone_name_or_pattern = zone_name_pattern
        request.area_tolerance = area_tolerance
        request.distance_tolerance = distance_tolerance
        response = self.service.GetOverlappingFaceZones(request)
        return response.overlapping_face_zone_ids

    def GetZonesWithMarkedFaces(self, list_or_pattern) -> Any:
        """GetZonesWithMarkedFaces."""
        request = MeshingQueriesProtoModule.GetZonesWithMarkedFacesRequest()
        if isinstance(list_or_pattern, str):
            request.face_zone_pattern = list_or_pattern
        elif isinstance(list_or_pattern, list):
            if isinstance(list_or_pattern[0], int):
                for items in list_or_pattern:
                    request.face_zone_ids.append(items)
            elif isinstance(list_or_pattern[0], str):
                for items in list_or_pattern:
                    request.face_zone_names.append(items)
        response = self.service.GetZonesWithMarkedFaces(request)
        return response.zones_with_marked_faces

    def GetAllObjectNameList(self) -> Any:
        """GetAllObjectNameList."""
        request = MeshingQueriesProtoModule.Empty()
        response = self.service.GetAllObjectNameList(request)
        return response.objects

    def GetObjectNameListOfType(self, type) -> Any:
        """GetObjectNameListOfType."""
        request = MeshingQueriesProtoModule.GetObjectNameListOfTypeRequest()
        request.type = type
        response = self.service.GetObjectNameListOfType(request)
        return response.objects

    def GetObjectsOfFilter(self, filter) -> Any:
        """GetObjectsOfFilter."""
        request = MeshingQueriesProtoModule.GetObjectsOfFilterRequest()
        request.filter = filter
        response = self.service.GetObjectsOfFilter(request)
        return response.objects

    def GetRegionsOfObject(self, object) -> Any:
        """GetRegionsOfObject."""
        request = MeshingQueriesProtoModule.GetRegionsOfObjectRequest()
        request.object = object
        response = self.service.GetRegionsOfObject(request)
        return response.regions

    def GetRegionNameListOfObject(self, object) -> Any:
        """GetRegionNameListOfObject."""
        request = MeshingQueriesProtoModule.GetRegionNameListOfObjectRequest()
        request.object = object
        response = self.service.GetRegionNameListOfObject(request)
        return response.regions

    def SortRegionsByVolume(self, object_name, order) -> Any:
        """SortRegionsByVolume."""
        request = MeshingQueriesProtoModule.SortRegionsByVolumeRequest()
        request.object_name = object_name
        request.order = order
        response = self.service.SortRegionsByVolume(request)
        return response.regions

    def GetRegionVolume(self, object_name, region_name) -> Any:
        """GetRegionVolume."""
        request = MeshingQueriesProtoModule.GetRegionVolumeRequest()
        request.object_name = object_name
        request.region_name = region_name
        response = self.service.GetRegionVolume(request)
        return response.region_volume

    def GetRegionsOfFilter(self, object, filter) -> Any:
        """GetRegionsOfFilter."""
        request = MeshingQueriesProtoModule.GetRegionsOfFilterRequest()
        request.object = object
        request.filter = filter
        response = self.service.GetRegionsOfFilter(request)
        return response.regions

    def GetRegionNameListOfPattern(self, object, region_name_or_pattern) -> Any:
        """GetRegionNameListOfPattern."""
        request = MeshingQueriesProtoModule.GetRegionNameListOfPatternRequest()
        request.object = object
        request.region_name_or_pattern = region_name_or_pattern
        response = self.service.GetRegionNameListOfPattern(request)
        return response.regions

    def GetRegionsOfFaceZones(self, list_of_face_zone_ids) -> Any:
        """GetRegionsOfFaceZones."""
        request = MeshingQueriesProtoModule.GetRegionsOfFaceZonesRequest()
        for id in list_of_face_zone_ids:
            request.face_zone_ids.append(id)
        response = self.service.GetRegionsOfFaceZones(request)
        return response.regions

    def FindJoinPairs(
        self, face_zone_list_or_pattern, join_tolerance, absolute_tolerance, join_angle
    ) -> Any:
        """FindJoinPairs."""
        request = MeshingQueriesProtoModule.FindJoinPairsRequest()
        if isinstance(face_zone_list_or_pattern, str):
            request.face_zone_name_or_pattern = face_zone_list_or_pattern
        elif isinstance(face_zone_list_or_pattern, list):
            if isinstance(face_zone_list_or_pattern[0], int):
                for items in face_zone_list_or_pattern:
                    request.face_zone_ids.append(items)
            elif isinstance(face_zone_list_or_pattern[0], str):
                for items in face_zone_list_or_pattern:
                    request.face_zone_names.append(items)
        request.join_tolerance = join_tolerance
        request.absolute_tolerance = absolute_tolerance
        request.join_angle = join_angle
        response = self.service.FindJoinPairs(request)
        return response.pairs

    def GetRegionNameListOfFaceZones(self, list_or_pattern) -> Any:
        """GetRegionNameListOfFaceZones."""
        request = MeshingQueriesProtoModule.GetRegionNameListOfFaceZonesRequest()
        if isinstance(list_or_pattern, str):
            request.face_zone_name_or_pattern = list_or_pattern
        elif isinstance(list_or_pattern, list):
            for items in list_or_pattern:
                request.face_zone_ids.append(items)
        response = self.service.GetRegionNameListOfFaceZones(request)
        return response.regions
