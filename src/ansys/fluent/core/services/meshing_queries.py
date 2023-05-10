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
    Meshing Queries.
    """

    def __init__(self, service: MeshingQueriesService):
        """__init__ method of MeshingQueries class."""
        self.service = service

    docstring = None

    def GetFaceZoneAtLocation(self, location) -> Any:
        """
        Return face zone at or closest to a specified location.

        Note:  This function is not applicable to polyhedra meshes.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetFaceZoneAtLocation([1.4, 1.4, 1.4])

        """
        request = MeshingQueriesProtoModule.GetFaceZoneAtLocationRequest()
        request.location.x = location[0]
        request.location.y = location[1]
        request.location.z = location[2]
        response = self.service.GetFaceZoneAtLocation(request)
        return response.face_zone_id

    def GetCellZoneAtLocation(self, location) -> Any:
        """
        Return cell zone at or closest to a specified location.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetCellZoneAtLocation([1.4, 1.4, 1.4])

        """
        request = MeshingQueriesProtoModule.GetCellZoneAtLocationRequest()
        request.location.x = location[0]
        request.location.y = location[1]
        request.location.z = location[2]
        response = self.service.GetCellZoneAtLocation(request)
        return response.cell_zone_id

    def GetZonesOfType(self, type) -> Any:
        """
        Return a list of zones of the specified default zone type.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetZonesOfType("velocity-inlet")

        """
        request = MeshingQueriesProtoModule.GetZonesOfTypeRequest()
        request.type = type
        response = self.service.GetZonesOfType(request)
        return response.zone_ids

    def GetZonesOfGroup(self, group) -> Any:
        """
        Return a list of zones of the specified default zone group or user-defined group.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetZonesOfGroup("inlet")

        """
        request = MeshingQueriesProtoModule.GetZonesOfGroupRequest()
        request.group = group
        response = self.service.GetZonesOfGroup(request)
        return response.zone_ids

    def GetFaceZonesOfFilter(self, filter) -> Any:
        """
        Return a list of face zones whose names contain the specified filter string.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetFaceZonesOfFilter("*")

        """
        request = MeshingQueriesProtoModule.GetFaceZonesOfFilterRequest()
        request.filter = filter
        response = self.service.GetFaceZonesOfFilter(request)
        return response.face_zone_ids

    def GetCellZonesOfFilter(self, filter) -> Any:
        """
        Return a list of cell zones whose names contain the specified filter string.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetCellZonesOfFilter("*")

        """
        request = MeshingQueriesProtoModule.GetCellZonesOfFilterRequest()
        request.filter = filter
        response = self.service.GetCellZonesOfFilter(request)
        return response.cell_zone_ids

    def GetEdgeZonesOfFilter(self, filter) -> Any:
        """
        Return a list of edge zones whose names contain the specified filter string.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetEdgeZonesOfFilter("*")

        """
        request = MeshingQueriesProtoModule.GetEdgeZonesOfFilterRequest()
        request.filter = filter
        response = self.service.GetEdgeZonesOfFilter(request)
        return response.edge_zone_ids

    def GetNodeZonesOfFilter(self, filter) -> Any:
        """
        Return a list of node zones whose names contain the specified filter string.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetNodeZonesOfFilter("*")

        """
        request = MeshingQueriesProtoModule.GetNodeZonesOfFilterRequest()
        request.filter = filter
        response = self.service.GetNodeZonesOfFilter(request)
        return response.node_zone_ids

    def GetObjectsOfType(self, type) -> Any:
        """
        Return a list of objects of the specified type.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetObjectsOfType("mesh")

        """
        request = MeshingQueriesProtoModule.GetObjectsOfTypeRequest()
        request.type = type
        response = self.service.GetObjectsOfType(request)
        return response.objects

    def GetFaceZoneIdListOfObject(self, object) -> Any:
        """
        Return a list of face zones by ID in the specified face zone labels of an object.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetFaceZoneIdListOfObject("elbow-fluid")

        """
        request = MeshingQueriesProtoModule.GetFaceZoneIdListOfObjectRequest()
        request.object = object
        response = self.service.GetFaceZoneIdListOfObject(request)
        return response.face_zone_ids

    def GetEdgeZoneIdListOfObject(self, object) -> Any:
        """
        Return a list of edge zones by ID in the specified face zone labels of an object

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetEdgeZoneIdListOfObject("elbow-fluid")

        """
        request = MeshingQueriesProtoModule.GetEdgeZoneIdListOfObjectRequest()
        request.object = object
        response = self.service.GetEdgeZoneIdListOfObject(request)
        return response.edge_zone_ids

    def GetCellZoneIdListOfObject(self, object) -> Any:
        """
        Return a list of cell zones by ID in the specified face zone labels of an object.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetCellZoneIdListOfObject("elbow-fluid")

        """
        request = MeshingQueriesProtoModule.GetCellZoneIdListOfObjectRequest()
        request.object = object
        response = self.service.GetCellZoneIdListOfObject(request)
        return response.cell_zone_ids

    def GetFaceZonesSharedByRegionsOfType(self, mesh_object, region_type) -> Any:
        """
        Return a list of face zones shared by regions of specified types in the mesh object specified,
        where region-type is fluid-fluid, solid-solid, or fluid-solid.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetFaceZonesSharedByRegionsOfType("elbow-fluid", "fluid-fluid")

        """
        request = MeshingQueriesProtoModule.GetFaceZonesSharedByRegionsOfTypeRequest()
        request.mesh_object = mesh_object
        request.region_type = region_type
        response = self.service.GetFaceZonesSharedByRegionsOfType(request)
        return response.shared_face_zone_ids

    def GetFaceZonesOfRegions(self, object, region_name_list) -> Any:
        """
        Return a list of face zones in the specified regions.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetFaceZonesOfRegions("elbow-fluid", ["fluid"])

        """
        request = MeshingQueriesProtoModule.GetFaceZonesOfRegionsRequest()
        request.object = object
        for region in region_name_list:
            request.regions.append(region)
        response = self.service.GetFaceZonesOfRegions(request)
        return response.zone_ids

    def GetFaceZonesOfLabels(self, object, label_name_list) -> Any:
        """
        Return a list of face zones in the specified face zone labels of the object specified.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetFaceZonesOfLabels("elbow-fluid", ["inlet", "outlet", "wall", "internal"])

        """
        request = MeshingQueriesProtoModule.GetFaceZonesOfLabelsRequest()
        request.object = object
        for label in label_name_list:
            request.labels.append(label)
        response = self.service.GetFaceZonesOfLabels(request)
        return response.zone_ids

    def GetFaceZoneIdListOfLabels(self, object, zone_label_list) -> Any:
        """
        Return a list of face zones by ID in the specified face zone labels of an object.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetFaceZoneIdListOfLabels("elbow-fluid", ["outlet"])

        """
        request = MeshingQueriesProtoModule.GetFaceZoneIdListOfLabelsRequest()
        request.object = object
        for zone_label in zone_label_list:
            request.labels.append(zone_label)
        response = self.service.GetFaceZoneIdListOfLabels(request)
        return response.zone_ids

    def GetFaceZonesOfObjects(self, object_list) -> Any:
        """
        Return a list of face zones in the specified objects.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetFaceZonesOfObjects(["elbow-fluid"])

        """
        request = MeshingQueriesProtoModule.GetFaceZonesOfObjectsRequest()
        for object in object_list:
            request.object_list.append(object)
        response = self.service.GetFaceZonesOfObjects(request)
        return response.face_zone_ids

    def GetEdgeZonesOfObjects(self, object_list) -> Any:
        """
        Return a list of edge zones in the specified objects.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetEdgeZonesOfObjects(["elbow-fluid"])

        """
        request = MeshingQueriesProtoModule.GetEdgeZonesOfObjectsRequest()
        for object in object_list:
            request.object_list.append(object)
        response = self.service.GetEdgeZonesOfObjects(request)
        return response.edge_zone_ids

    def GetFaceZoneIdListOfRegions(self, object, region_list) -> Any:
        """
        Return a list of face zones by ID in the specified regions of an object.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetFaceZoneIdListOfRegions("elbow-fluid", ["fluid"])

        """
        request = MeshingQueriesProtoModule.GetFaceZoneIdListOfRegionsRequest()
        request.object = object
        for region in region_list:
            request.labels.append(region)
        response = self.service.GetFaceZoneIdListOfRegions(request)
        return response.zone_ids

    def GetPrismCellZones(self, list_or_pattern) -> Any:
        """
        Return a list of prism cell zones.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetPrismCellZones(["inlet", "outlet"])

            >>> meshing_session.meshing_queries.GetPrismCellZones("*")

        """
        request = MeshingQueriesProtoModule.GetPrismCellZonesRequest()
        if isinstance(list_or_pattern, str):
            request.zone_name_or_pattern = list_or_pattern
        elif isinstance(list_or_pattern, list):
            for items in list_or_pattern:
                request.zones.append(items)
        response = self.service.GetPrismCellZones(request)
        return response.prism_cell_zones

    def GetTetCellZones(self, list_or_pattern) -> Any:
        """
        Return a list of tet cell zones.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetTetCellZones(["inlet", "outlet"])

            >>> meshing_session.meshing_queries.GetTetCellZones("*")

        """
        request = MeshingQueriesProtoModule.GetTetCellZonesRequest()
        if isinstance(list_or_pattern, str):
            request.zone_name_or_pattern = list_or_pattern
        elif isinstance(list_or_pattern, list):
            for items in list_or_pattern:
                request.zones.append(items)
        response = self.service.GetTetCellZones(request)
        return response.tet_cell_zones

    def GetAdjacentCellZones(self, list_or_name_or_pattern) -> Any:
        """
        Return adjacent cell zones for given face zone

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetAdjacentCellZones([30])

            >>> meshing_session.meshing_queries.GetAdjacentCellZones("*")

        """
        request = MeshingQueriesProtoModule.GetAdjacentCellZonesRequest()
        if isinstance(list_or_name_or_pattern, str):
            request.zone_name_or_pattern = list_or_name_or_pattern
        elif isinstance(list_or_name_or_pattern, list):
            for items in list_or_name_or_pattern:
                request.face_zone_ids.append(items)
        response = self.service.GetAdjacentCellZones(request)
        return response.adjacent_cell_zones

    def GetAdjacentFaceZones(self, list_or_name_or_pattern) -> Any:
        """
        Return adjacent boundary face zones for given cell zones.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetAdjacentFaceZones([3460])

            >>> meshing_session.meshing_queries.GetAdjacentFaceZones("*")

        """
        request = MeshingQueriesProtoModule.GetAdjacentFaceZonesRequest()
        if isinstance(list_or_name_or_pattern, str):
            request.zone_name_or_pattern = list_or_name_or_pattern
        elif isinstance(list_or_name_or_pattern, list):
            for items in list_or_name_or_pattern:
                request.cell_zone_ids.append(items)
        response = self.service.GetAdjacentFaceZones(request)
        return response.adjacent_boundary_face_zones

    def GetAdjacentInteriorAndBoundaryFaceZones(self, list_or_name_or_pattern) -> Any:
        """
        Return adjacent interior and boundary face zones for given cell zones.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetAdjacentInteriorAndBoundaryFaceZones([30])

            >>> meshing_session.meshing_queries.GetAdjacentInteriorAndBoundaryFaceZones("fluid")

            >>> meshing_session.meshing_queries.GetAdjacentInteriorAndBoundaryFaceZones("*")

        """
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
        """
        Return adjacent zones based on edge connectivity

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetAdjacentZonesByEdgeConnectivity([30])

            >>> meshing_session.meshing_queries.GetAdjacentZonesByEdgeConnectivity("*")

        """
        request = MeshingQueriesProtoModule.GetAdjacentZonesByEdgeConnectivityRequest()
        if isinstance(list_or_name_or_pattern, str):
            request.zone_name_or_pattern = list_or_name_or_pattern
        elif isinstance(list_or_name_or_pattern, list):
            for items in list_or_name_or_pattern:
                request.zone_ids.append(items)
        response = self.service.GetAdjacentZonesByEdgeConnectivity(request)
        return response.adjacent_zone_ids

    def GetAdjacentZonesByNodeConnectivity(self, list_or_name_or_pattern) -> Any:
        """
        Return adjacent zones based on node connectivity

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetAdjacentZonesByNodeConnectivity([30])

            >>> meshing_session.meshing_queries.GetAdjacentZonesByNodeConnectivity("*")

        """
        request = MeshingQueriesProtoModule.GetAdjacentZonesByNodeConnectivityRequest()
        if isinstance(list_or_name_or_pattern, str):
            request.zone_name_or_pattern = list_or_name_or_pattern
        elif isinstance(list_or_name_or_pattern, list):
            for items in list_or_name_or_pattern:
                request.zone_ids.append(items)
        response = self.service.GetAdjacentZonesByNodeConnectivity(request)
        return response.adjacent_zone_ids

    def GetSharedBoundaryZones(self, list_or_name_or_pattern) -> Any:
        """
        Returns the number of faces and the boundary face zones that are shared with the specified cell zones.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetSharedBoundaryZones("*")

            >>> meshing_session.meshing_queries.GetSharedBoundaryZones([3460])

        """
        request = MeshingQueriesProtoModule.GetSharedBoundaryZonesRequest()
        if isinstance(list_or_name_or_pattern, str):
            request.cell_zone_name_or_pattern = list_or_name_or_pattern
        elif isinstance(list_or_name_or_pattern, list):
            for items in list_or_name_or_pattern:
                request.cell_zone_ids.append(items)
        response = self.service.GetSharedBoundaryZones(request)
        return response.shared_boundary_zone_ids

    def GetInteriorZonesConnectedToCellZones(self, list_or_name_or_pattern) -> Any:
        """
        Returns interior face zones connected to given cell zones.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetInteriorZonesConnectedToCellZones([3460])

            >>> meshing_session.meshing_queries.GetInteriorZonesConnectedToCellZones("*")

        """
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
        """
        Return a list of face zones with zone-specific prism settings applied.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetFaceZonesWithZoneSpecificPrismsApplied()

        """
        request = MeshingQueriesProtoModule.Empty()
        response = self.service.GetFaceZonesWithZoneSpecificPrismsApplied(request)
        return response.face_zone_ids

    def GetFaceZonesOfPrismControls(self, control_name) -> Any:
        """
        Return a list of face zones to which the specified prism controls apply.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetFaceZonesOfPrismControls("*")

        """
        request = MeshingQueriesProtoModule.GetFaceZonesOfPrismControlsRequest()
        request.control_name = control_name
        response = self.service.GetFaceZonesOfPrismControls(request)
        return response.face_zone_ids

    def GetBaffles(self, face_zone_list) -> Any:
        """
        Return the baffle zones based on the face zone list specified.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetBaffles([29, 30])

        """
        request = MeshingQueriesProtoModule.GetBafflesRequest()
        for items in face_zone_list:
            request.face_zone_ids.append(items)
        response = self.service.GetBaffles(request)
        return response.baffle_zone_ids

    def GetEmbeddedBaffles(self) -> Any:
        """
        Return the embedded baffle zones.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetEmbeddedBaffles()

        """
        request = MeshingQueriesProtoModule.Empty()
        response = self.service.GetEmbeddedBaffles(request)
        return response.embedded_baffles_zone_ids

    def GetWrappedZones(self) -> Any:
        """
        Return a list of wrapped face zones.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetWrappedZones()

        """
        request = MeshingQueriesProtoModule.Empty()
        response = self.service.GetWrappedZones(request)
        return response.wrapped_face_zone_ids

    def GetUnreferencedEdgeZones(self) -> Any:
        """
        Return a list of unreferenced edge zones.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetUnreferencedEdgeZones()

        """
        request = MeshingQueriesProtoModule.Empty()
        response = self.service.GetUnreferencedEdgeZones(request)
        return response.unreferenced_edge_zone_ids

    def GetUnreferencedFaceZones(self) -> Any:
        """
        Return a list of unreferenced face zones.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetUnreferencedFaceZones()

        """
        request = MeshingQueriesProtoModule.Empty()
        response = self.service.GetUnreferencedFaceZones(request)
        return response.unreferenced_face_zone_ids

    def GetUnreferencedCellZones(self) -> Any:
        """
        Return a list of unreferenced cell zones.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetUnreferencedCellZones()

        """
        request = MeshingQueriesProtoModule.Empty()
        response = self.service.GetUnreferencedCellZones(request)
        return response.unreferenced_cell_zone_ids

    def GetUnreferencedEdgeZonesOfFilter(self, filter) -> Any:
        """
        Return a list of unreferenced edge zones whose names contain the specified filter string.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetUnreferencedEdgeZonesOfFilter("*")

        """
        request = MeshingQueriesProtoModule.GetUnreferencedEdgeZonesOfFilterRequest()
        request.filter = filter
        response = self.service.GetUnreferencedEdgeZonesOfFilter(request)
        return response.unreferenced_edge_zone_ids

    def GetUnreferencedFaceZonesOfFilter(self, filter) -> Any:
        """
        Return a list of unreferenced face zones whose names contain the specified filter string.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetUnreferencedFaceZonesOfFilter("*")

        """
        request = MeshingQueriesProtoModule.GetUnreferencedFaceZonesOfFilterRequest()
        request.filter = filter
        response = self.service.GetUnreferencedFaceZonesOfFilter(request)
        return response.unreferenced_face_zone_ids

    def GetUnreferencedCellZonesOfFilter(self, filter) -> Any:
        """
        Return a list of unreferenced cell zones whose names contain the specified filter string.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetUnreferencedCellZonesOfFilter("*")

        """
        request = MeshingQueriesProtoModule.GetUnreferencedCellZonesOfFilterRequest()
        request.filter = filter
        response = self.service.GetUnreferencedCellZonesOfFilter(request)
        return response.unreferenced_cell_zone_ids

    def GetUnreferencedEdgeZoneIdListOfPattern(self, pattern) -> Any:
        """
        Return a list of unreferenced edge zones by ID, whose names contain the specified pattern.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetUnreferencedEdgeZoneIdListOfPattern("*")

        """
        request = (
            MeshingQueriesProtoModule.GetUnreferencedEdgeZoneIdListOfPatternRequest()
        )
        request.pattern = pattern
        response = self.service.GetUnreferencedEdgeZoneIdListOfPattern(request)
        return response.unreferenced_edge_zone_ids

    def GetUnreferencedFaceZoneIdListOfPattern(self, pattern) -> Any:
        """
        Return a list of unreferenced face zones by ID, whose names contain the specified pattern.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetUnreferencedFaceZoneIdListOfPattern("*")

        """
        request = (
            MeshingQueriesProtoModule.GetUnreferencedFaceZoneIdListOfPatternRequest()
        )
        request.pattern = pattern
        response = self.service.GetUnreferencedFaceZoneIdListOfPattern(request)
        return response.unreferenced_face_zone_ids

    def GetUnreferencedCellZoneIdListOfPattern(self, pattern) -> Any:
        """
        Return a list of unreferenced cell zones by ID, whose names contain the specified pattern.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetUnreferencedCellZoneIdListOfPattern("*")

        """
        request = (
            MeshingQueriesProtoModule.GetUnreferencedCellZoneIdListOfPatternRequest()
        )
        request.pattern = pattern
        response = self.service.GetUnreferencedCellZoneIdListOfPattern(request)
        return response.unreferenced_cell_zone_ids

    def GetMaxsizeCellZoneByVolume(self, list_or_pattern) -> Any:
        """
        Return cell zone with maximum volume for given list or pattern of cell zones.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetMaxsizeCellZoneByVolume("*")

            >>> meshing_session.meshing_queries.GetMaxsizeCellZoneByVolume([3460])

        """
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
        """
        Return cell zone with maximum count of elements for given list or pattern of cell zones.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetMaxsizeCellZoneByCount("*")

            >>> meshing_session.meshing_queries.GetMaxsizeCellZoneByCount([3460])

        """
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
        """
        Return face zone with minimum area for given list or pattern of face zones.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetMinsizeFaceZoneByArea("*")

            >>> meshing_session.meshing_queries.GetMinsizeFaceZoneByArea([29, 30, 31, 32, 33, 34])

        """
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
        """
        Return face zone with minimum count of elements for given list or pattern of face zones.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetMinsizeFaceZoneByCount("*")

            >>> meshing_session.meshing_queries.GetMinsizeFaceZoneByCount([29, 30, 31, 32, 33, 34])

        """
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
        """
        Return a list of face zones with a count below the maximum entity count (maximum-entity-count) specified.
        You can choose to restrict the report to only boundary edge zones, if required (only-boundary? set to True or False).

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetFaceZoneListByMaximumEntityCount(20, True)

        """
        request = MeshingQueriesProtoModule.GetFaceZoneListByMaximumEntityCountRequest()
        request.maximum_entity_count = max_entity_count
        request.only_boundary = only_boundary
        response = self.service.GetFaceZoneListByMaximumEntityCount(request)
        return response.face_zone_ids

    def GetEdgeZoneListByMaximumEntityCount(
        self, max_entity_count, only_boundary
    ) -> Any:
        """
        Return a list of edge zones with a count below the maximum entity count (maximum-entity-count) specified.
        You can choose to restrict the report to only boundary edge zones, if required (only-boundary? set to True or False).

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetEdgeZoneListByMaximumEntityCount(20, False)

        """
        request = MeshingQueriesProtoModule.GetEdgeZoneListByMaximumEntityCountRequest()
        request.maximum_entity_count = max_entity_count
        request.only_boundary = only_boundary
        response = self.service.GetEdgeZoneListByMaximumEntityCount(request)
        return response.edge_zone_ids

    def GetCellZoneListByMaximumEntityCount(self, maximum_entity_count) -> Any:
        """
        Return a list of cell zones with a count below the maximum entity count (maximum-entity-count) specified.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetCellZoneListByMaximumEntityCount(1)

        """
        request = MeshingQueriesProtoModule.GetCellZoneListByMaximumEntityCountRequest()
        request.maximum_entity_count = maximum_entity_count
        response = self.service.GetCellZoneListByMaximumEntityCount(request)
        return response.cell_zone_ids

    def GetFaceZoneListByMaximumZoneArea(self, maximum_zone_area) -> Any:
        """
        Return a list of face zones with a maximum zone area below the maximum-zone-area specified.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetFaceZoneListByMaximumZoneArea(100)

        """
        request = MeshingQueriesProtoModule.GetFaceZoneListByMaximumZoneAreaRequest()
        request.maximum_zone_area = maximum_zone_area
        response = self.service.GetFaceZoneListByMaximumZoneArea(request)
        return response.face_zone_ids

    def GetFaceZoneListByMinimumZoneArea(self, minimum_zone_area) -> Any:
        """
        Return a list of face zones with a minimum zone area above the minimum-zone-area specified.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetFaceZoneListByMinimumZoneArea(10)

        """
        request = MeshingQueriesProtoModule.GetFaceZoneListByMinimumZoneAreaRequest()
        request.minimum_zone_area = minimum_zone_area
        response = self.service.GetFaceZoneListByMinimumZoneArea(request)
        return response.face_zone_ids

    def GetZonesWithFreeFaces(self, list_or_pattern) -> Any:
        """
        Return a list of zones with free faces for the face zones specified.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetZonesWithFreeFaces("*")

            >>> meshing_session.meshing_queries.GetZonesWithFreeFaces([29, 30, 31, 32])

            >>> meshing_session.meshing_queries.GetZonesWithFreeFaces(["inlet", "outlet"])

        """
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
        """
        Return a list of zones with multi-connected faces for the face zones specified.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetZonesWithMultiFaces("*")

            >>> meshing_session.meshing_queries.GetZonesWithMultiFaces([29, 30, 31, 32])

            >>> meshing_session.meshing_queries.GetZonesWithMultiFaces(["inlet", "outlet"])

        """
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
        """
        Return a list of overlapping face zones based on the area-tolerance and distance-tolerance specified.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetOverlappingFaceZones("*", 0.1, 0.1)

        """
        request = MeshingQueriesProtoModule.GetOverlappingFaceZonesRequest()
        request.face_zone_name_or_pattern = zone_name_pattern
        request.area_tolerance = area_tolerance
        request.distance_tolerance = distance_tolerance
        response = self.service.GetOverlappingFaceZones(request)
        return response.overlapping_face_zone_ids

    def GetZonesWithMarkedFaces(self, list_or_pattern) -> Any:
        """
        Return a list of zones with marked faces for the face zones specified.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetZonesWithMarkedFaces("*")

            >>> meshing_session.meshing_queries.GetZonesWithMarkedFaces([29, 30, 31, 32])

            >>> meshing_session.meshing_queries.GetZonesWithMarkedFaces(["inlet", "outlet"])

        """
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
        """
        Return a list of all objects.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetAllObjectNameList()

        """
        request = MeshingQueriesProtoModule.Empty()
        response = self.service.GetAllObjectNameList(request)
        return response.objects

    def GetObjectNameListOfType(self, type) -> Any:
        """
        Return a list of objects of the specified type.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetObjectNameListOfType("mesh")

        """
        request = MeshingQueriesProtoModule.GetObjectNameListOfTypeRequest()
        request.type = type
        response = self.service.GetObjectNameListOfType(request)
        return response.objects

    def GetObjectsOfFilter(self, filter) -> Any:
        """
        Return a list of objects whose names contain the specified filter string.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetObjectsOfFilter("*")

        """
        request = MeshingQueriesProtoModule.GetObjectsOfFilterRequest()
        request.filter = filter
        response = self.service.GetObjectsOfFilter(request)
        return response.objects

    def GetRegionsOfObject(self, object) -> Any:
        """
        Return a list of regions in the specified object.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetRegionsOfObject("elbow-fluid")

        """
        request = MeshingQueriesProtoModule.GetRegionsOfObjectRequest()
        request.object = object
        response = self.service.GetRegionsOfObject(request)
        return response.regions

    def GetRegionNameListOfObject(self, object) -> Any:
        """
        Return a list of regions in the specified object.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetRegionNameListOfObject("elbow-fluid")

        """
        request = MeshingQueriesProtoModule.GetRegionNameListOfObjectRequest()
        request.object = object
        response = self.service.GetRegionNameListOfObject(request)
        return response.regions

    def SortRegionsByVolume(self, object_name, order) -> Any:
        """
        Returns a sorted list of volumetric regions by volume for the object specified.
        Specify the order (ascending or descending).

        .. code-block:: python

            >>> meshing_session.meshing_queries.SortRegionsByVolume("elbow-fluid", "ascending")

        """
        request = MeshingQueriesProtoModule.SortRegionsByVolumeRequest()
        request.object_name = object_name
        request.order = order
        response = self.service.SortRegionsByVolume(request)
        return response.regions

    def GetRegionVolume(self, object_name, region_name) -> Any:
        """
        Return the region volume for the specified region of an object.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetRegionVolume("elbow-fluid", "fluid")

        """
        request = MeshingQueriesProtoModule.GetRegionVolumeRequest()
        request.object_name = object_name
        request.region_name = region_name
        response = self.service.GetRegionVolume(request)
        return response.region_volume

    def GetRegionsOfFilter(self, object, filter) -> Any:
        """
        Return a list of regions in the specified object, whose names contain the specified filter string.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetRegionsOfFilter("elbow-fluid", "*")

        """
        request = MeshingQueriesProtoModule.GetRegionsOfFilterRequest()
        request.object = object
        request.filter = filter
        response = self.service.GetRegionsOfFilter(request)
        return response.regions

    def GetRegionNameListOfPattern(self, object, region_name_or_pattern) -> Any:
        """
        Return a list of regions in the specified object, whose names contain the specified name pattern.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetRegionNameListOfPattern("elbow-fluid", "*")

        """
        request = MeshingQueriesProtoModule.GetRegionNameListOfPatternRequest()
        request.object = object
        request.region_name_or_pattern = region_name_or_pattern
        response = self.service.GetRegionNameListOfPattern(request)
        return response.regions

    def GetRegionsOfFaceZones(self, list_of_face_zone_ids) -> Any:
        """
        Return a list of regions containing the face zones specified.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetRegionsOfFaceZones([29, 30, 31, 32, 33, 34])

        """
        request = MeshingQueriesProtoModule.GetRegionsOfFaceZonesRequest()
        for id in list_of_face_zone_ids:
            request.face_zone_ids.append(id)
        response = self.service.GetRegionsOfFaceZones(request)
        return response.regions

    def FindJoinPairs(
        self, face_zone_list_or_pattern, join_tolerance, absolute_tolerance, join_angle
    ) -> Any:
        """
        Return the pairs of overlapping face zones based on the join tolerance and feature angle.

        .. code-block:: python

            >>> meshing_session.meshing_queries.FindJoinPairs("outlet", 0.1, True, 40)

            >>> meshing_session.meshing_queries.FindJoinPairs([32], 0.1, True, 40))

            >>> meshing_session.meshing_queries.FindJoinPairs(["outlet"], 0.1, True, 40)

        """
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
        """
        Return a list of regions containing the face zones specified.

        .. code-block:: python

            >>> meshing_session.meshing_queries.GetRegionNameListOfFaceZones([29, 30, 31, 32, 33, 34])

        """
        request = MeshingQueriesProtoModule.GetRegionNameListOfFaceZonesRequest()
        if isinstance(list_or_pattern, str):
            request.face_zone_name_or_pattern = list_or_pattern
        elif isinstance(list_or_pattern, list):
            for items in list_or_pattern:
                request.face_zone_ids.append(items)
        response = self.service.GetRegionNameListOfFaceZones(request)
        return response.regions
