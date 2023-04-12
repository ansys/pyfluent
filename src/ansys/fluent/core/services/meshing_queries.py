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

    # @catch_grpc_error
    # def GetSharedBoundaryZones(
    #     self,
    #     request: MeshingQueriesProtoModule.GetSharedBoundaryZonesRequest,
    # ) -> MeshingQueriesProtoModule.GetSharedBoundaryZonesResponse:
    #     """GetSharedBoundaryZones rpc of MeshingQueriesService."""
    #     return self._stub.GetSharedBoundaryZones(
    #         request, metadata=self._metadata
    #     )

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
    def GetRegionNameListOfFaceZones(
        self,
        request: MeshingQueriesProtoModule.GetRegionNameListOfFaceZonesRequest,
    ) -> MeshingQueriesProtoModule.GetRegionNameListOfFaceZonesResponse:
        """GetRegionNameListOfFaceZones rpc of MeshingQueriesService."""
        return self._stub.GetRegionNameListOfFaceZones(request, metadata=self._metadata)

    @catch_grpc_error
    def ConvertZoneNameSymbolsToIds(
        self,
        request: MeshingQueriesProtoModule.ConvertZoneNameSymbolsToIdsRequest,
    ) -> MeshingQueriesProtoModule.ConvertZoneNameSymbolsToIdsResponse:
        """ConvertZoneNameSymbolsToIds rpc of MeshingQueriesService."""
        return self._stub.ConvertZoneNameSymbolsToIds(request, metadata=self._metadata)

    @catch_grpc_error
    def ConvertZoneNameStringsToIds(
        self,
        request: MeshingQueriesProtoModule.ConvertZoneNameStringsToIdsRequest,
    ) -> MeshingQueriesProtoModule.ConvertZoneNameStringsToIdsResponse:
        """ConvertZoneNameStringsToIds rpc of MeshingQueriesService."""
        return self._stub.ConvertZoneNameStringsToIds(request, metadata=self._metadata)

    @catch_grpc_error
    def ConvertZoneIdsToNameStrings(
        self,
        request: MeshingQueriesProtoModule.ConvertZoneIdsToNameStringsRequest,
    ) -> MeshingQueriesProtoModule.ConvertZoneIdsToNameStringsResponse:
        """ConvertZoneIdsToNameStrings rpc of MeshingQueriesService."""
        return self._stub.ConvertZoneIdsToNameStrings(request, metadata=self._metadata)

    @catch_grpc_error
    def ConvertZoneIdsToNameSymbols(
        self,
        request: MeshingQueriesProtoModule.ConvertZoneIdsToNameSymbolsRequest,
    ) -> MeshingQueriesProtoModule.ConvertZoneIdsToNameSymbolsResponse:
        """ConvertZoneIdsToNameSymbols rpc of MeshingQueriesService."""
        return self._stub.ConvertZoneIdsToNameSymbols(request, metadata=self._metadata)

    @catch_grpc_error
    def ConvertSymbolListToString(
        self,
        request: MeshingQueriesProtoModule.ConvertSymbolListToStringRequest,
    ) -> MeshingQueriesProtoModule.ConvertSymbolListToStringResponse:
        """ConvertSymbolListToString rpc of MeshingQueriesService."""
        return self._stub.ConvertSymbolListToString(request, metadata=self._metadata)

    @catch_grpc_error
    def CreateStringFromSymbolList(
        self,
        request: MeshingQueriesProtoModule.CreateStringFromSymbolListRequest,
    ) -> MeshingQueriesProtoModule.CreateStringFromSymbolListResponse:
        """CreateStringFromSymbolList rpc of MeshingQueriesService."""
        return self._stub.CreateStringFromSymbolList(request, metadata=self._metadata)

    @catch_grpc_error
    def IntegerListSubstract(
        self,
        request: MeshingQueriesProtoModule.IntegerListSubstractRequest,
    ) -> MeshingQueriesProtoModule.IntegerListSubstractResponse:
        """IntegerListSubstract rpc of MeshingQueriesService."""
        return self._stub.IntegerListSubstract(request, metadata=self._metadata)

    @catch_grpc_error
    def ListReplace(
        self,
        request: MeshingQueriesProtoModule.ListReplaceRequest,
    ) -> MeshingQueriesProtoModule.ListReplaceResponse:
        """ListReplace rpc of MeshingQueriesService."""
        return self._stub.ListReplace(request, metadata=self._metadata)

    @catch_grpc_error
    def RemoveElementFromList(
        self,
        request: MeshingQueriesProtoModule.RemoveElementFromListRequest,
    ) -> MeshingQueriesProtoModule.RemoveElementFromListResponse:
        """RemoveElementFromList rpc of MeshingQueriesService."""
        return self._stub.RemoveElementFromList(request, metadata=self._metadata)

    @catch_grpc_error
    def ListContains(
        self,
        request: MeshingQueriesProtoModule.ListContainsRequest,
    ) -> MeshingQueriesProtoModule.ListContainsResponse:
        """ListContains rpc of MeshingQueriesService."""
        return self._stub.ListContains(request, metadata=self._metadata)


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
        request.input = type
        response = self.service.GetZonesOfType(request)
        return response.outputs

    def GetZonesOfGroup(self, group) -> Any:
        """GetZonesOfGroup."""
        request = MeshingQueriesProtoModule.GetZonesOfGroupRequest()
        request.input = group
        response = self.service.GetZonesOfGroup(request)
        return response.outputs

    def GetFaceZonesOfFilter(self, filter) -> Any:
        """GetFaceZonesOfFilter."""
        request = MeshingQueriesProtoModule.GetFaceZonesOfFilterRequest()
        request.input = filter
        response = self.service.GetFaceZonesOfFilter(request)
        return response.outputs

    def GetCellZonesOfFilter(self, filter) -> Any:
        """GetCellZonesOfFilter."""
        request = MeshingQueriesProtoModule.GetCellZonesOfFilterRequest()
        request.input = filter
        response = self.service.GetCellZonesOfFilter(request)
        return response.outputs

    def GetEdgeZonesOfFilter(self, filter) -> Any:
        """GetEdgeZonesOfFilter."""
        request = MeshingQueriesProtoModule.GetEdgeZonesOfFilterRequest()
        request.input = filter
        response = self.service.GetEdgeZonesOfFilter(request)
        return response.outputs

    def GetNodeZonesOfFilter(self, filter) -> Any:
        """GetNodeZonesOfFilter."""
        request = MeshingQueriesProtoModule.GetNodeZonesOfFilterRequest()
        request.input = filter
        response = self.service.GetNodeZonesOfFilter(request)
        return response.outputs

    def GetObjectsOfType(self, type) -> Any:
        """GetObjectsOfType."""
        request = MeshingQueriesProtoModule.GetObjectsOfTypeRequest()
        request.input = type
        response = self.service.GetObjectsOfType(request)
        return response.outputs

    def GetFaceZoneIdListOfObject(self, object) -> Any:
        """GetFaceZoneIdListOfObject."""
        request = MeshingQueriesProtoModule.GetFaceZoneIdListOfObjectRequest()
        request.input = object
        response = self.service.GetFaceZoneIdListOfObject(request)
        return response.outputs

    def GetEdgeZoneIdListOfObject(self, object) -> Any:
        """GetEdgeZoneIdListOfObject."""
        request = MeshingQueriesProtoModule.GetEdgeZoneIdListOfObjectRequest()
        request.input = object
        response = self.service.GetEdgeZoneIdListOfObject(request)
        return response.outputs

    def GetCellZoneIdListOfObject(self, object) -> Any:
        """GetCellZoneIdListOfObject."""
        request = MeshingQueriesProtoModule.GetCellZoneIdListOfObjectRequest()
        request.input = object
        response = self.service.GetCellZoneIdListOfObject(request)
        return response.outputs

    def GetFaceZonesSharedByRegionsOfType(self, mesh_object, region_type) -> Any:
        """GetFaceZonesSharedByRegionsOfType."""
        request = MeshingQueriesProtoModule.GetFaceZonesSharedByRegionsOfTypeRequest()
        request.input_1 = mesh_object
        request.input_2 = region_type
        response = self.service.GetFaceZonesSharedByRegionsOfType(request)
        return response.outputs

    def GetFaceZonesOfRegions(self, object, region_name_list) -> Any:
        """GetFaceZonesOfRegions."""
        request = MeshingQueriesProtoModule.GetFaceZonesOfRegionsRequest()
        request.input = object
        for region in region_name_list:
            request.inputs.append(region)
        response = self.service.GetFaceZonesOfRegions(request)
        return response.outputs

    def GetFaceZonesOfLabels(self, object, label_name_list) -> Any:
        """GetFaceZonesOfLabels."""
        request = MeshingQueriesProtoModule.GetFaceZonesOfLabelsRequest()
        request.input = object
        for label in label_name_list:
            request.inputs.append(label)
        response = self.service.GetFaceZonesOfLabels(request)
        return response.outputs

    def GetFaceZoneIdListOfLabels(self, object, zone_label_list) -> Any:
        """GetFaceZoneIdListOfLabels."""
        request = MeshingQueriesProtoModule.GetFaceZoneIdListOfLabelsRequest()
        request.input = object
        for zone_label in zone_label_list:
            request.inputs.append(zone_label)
        response = self.service.GetFaceZoneIdListOfLabels(request)
        return response.outputs

    def GetFaceZonesOfObjects(self, object_list) -> Any:
        """GetFaceZonesOfObjects."""
        request = MeshingQueriesProtoModule.GetFaceZonesOfObjectsRequest()
        for object in object_list:
            request.inputs.append(object)
        response = self.service.GetFaceZonesOfObjects(request)
        return response.outputs

    def GetEdgeZonesOfObjects(self, object_list) -> Any:
        """GetEdgeZonesOfObjects."""
        request = MeshingQueriesProtoModule.GetEdgeZonesOfObjectsRequest()
        for object in object_list:
            request.inputs.append(object)
        response = self.service.GetEdgeZonesOfObjects(request)
        return response.outputs

    def GetFaceZoneIdListOfRegions(self, object, region_list) -> Any:
        """GetFaceZoneIdListOfRegions."""
        request = MeshingQueriesProtoModule.GetFaceZoneIdListOfRegionsRequest()
        request.input = object
        for region in region_list:
            request.inputs.append(region)
        response = self.service.GetFaceZoneIdListOfRegions(request)
        return response.outputs

    def GetPrismCellZones(self, list_or_pattern) -> Any:
        """GetPrismCellZones."""
        request = MeshingQueriesProtoModule.GetPrismCellZonesRequest()
        if isinstance(list_or_pattern, str):
            request.input = list_or_pattern
        elif isinstance(list_or_pattern, list):
            for items in list_or_pattern:
                request.inputs.append(items)
        response = self.service.GetPrismCellZones(request)
        return response.outputs

    def GetTetCellZones(self, list_or_pattern) -> Any:
        """GetTetCellZones."""
        request = MeshingQueriesProtoModule.GetTetCellZonesRequest()
        if isinstance(list_or_pattern, str):
            request.input = list_or_pattern
        elif isinstance(list_or_pattern, list):
            for items in list_or_pattern:
                request.inputs.append(items)
        response = self.service.GetTetCellZones(request)
        return response.outputs

    def GetAdjacentCellZones(self, list_or_pattern) -> Any:
        """GetAdjacentCellZones."""
        request = MeshingQueriesProtoModule.GetAdjacentCellZonesRequest()
        if isinstance(list_or_pattern, str):
            request.input = list_or_pattern
        elif isinstance(list_or_pattern, list):
            for items in list_or_pattern:
                request.inputs.append(items)
        response = self.service.GetAdjacentCellZones(request)
        return response.outputs

    def GetAdjacentFaceZones(self, list_or_pattern) -> Any:
        """GetAdjacentFaceZones."""
        request = MeshingQueriesProtoModule.GetAdjacentFaceZonesRequest()
        if isinstance(list_or_pattern, str):
            request.input = list_or_pattern
        elif isinstance(list_or_pattern, list):
            for items in list_or_pattern:
                request.inputs.append(items)
        response = self.service.GetAdjacentFaceZones(request)
        return response.outputs

    def GetAdjacentInteriorAndBoundaryFaceZones(self, list_or_pattern) -> Any:
        """GetAdjacentInteriorAndBoundaryFaceZones."""
        request = (
            MeshingQueriesProtoModule.GetAdjacentInteriorAndBoundaryFaceZonesRequest()
        )
        if isinstance(list_or_pattern, str):
            request.input = list_or_pattern
        elif isinstance(list_or_pattern, list):
            for items in list_or_pattern:
                request.inputs.append(items)
        response = self.service.GetAdjacentInteriorAndBoundaryFaceZones(request)
        return response.outputs

    def GetAdjacentZonesByEdgeConnectivity(self, list_or_pattern) -> Any:
        """GetAdjacentZonesByEdgeConnectivity."""
        request = MeshingQueriesProtoModule.GetAdjacentZonesByEdgeConnectivityRequest()
        if isinstance(list_or_pattern, str):
            request.input = list_or_pattern
        elif isinstance(list_or_pattern, list):
            for items in list_or_pattern:
                request.inputs.append(items)
        response = self.service.GetAdjacentZonesByEdgeConnectivity(request)
        return response.outputs

    def GetAdjacentZonesByNodeConnectivity(self, list_or_pattern) -> Any:
        """GetAdjacentZonesByNodeConnectivity."""
        request = MeshingQueriesProtoModule.GetAdjacentZonesByNodeConnectivityRequest()
        if isinstance(list_or_pattern, str):
            request.input = list_or_pattern
        elif isinstance(list_or_pattern, list):
            for items in list_or_pattern:
                request.inputs.append(items)
        response = self.service.GetAdjacentZonesByNodeConnectivity(request)
        return response.outputs

    # def GetSharedBoundaryZones(self, list_or_pattern) -> Any:
    #     """GetSharedBoundaryZones."""
    #     request = MeshingQueriesProtoModule.GetSharedBoundaryZonesRequest()
    #     if isinstance(list_or_pattern, str):
    #         request.input = list_or_pattern
    #     elif isinstance(list_or_pattern, list):
    #         for items in list_or_pattern:
    #             request.inputs.append(items)
    #     response = self.service.GetSharedBoundaryZones(request)
    #     return response.outputs

    def GetInteriorZonesConnectedToCellZones(self, list_or_pattern) -> Any:
        """GetInteriorZonesConnectedToCellZones."""
        request = (
            MeshingQueriesProtoModule.GetInteriorZonesConnectedToCellZonesRequest()
        )
        if isinstance(list_or_pattern, str):
            request.input = list_or_pattern
        elif isinstance(list_or_pattern, list):
            for items in list_or_pattern:
                request.inputs.append(items)
        response = self.service.GetInteriorZonesConnectedToCellZones(request)
        return response.outputs

    def GetFaceZonesWithZoneSpecificPrismsApplied(self) -> Any:
        """GetFaceZonesWithZoneSpecificPrismsApplied."""
        request = MeshingQueriesProtoModule.Empty()
        response = self.service.GetFaceZonesWithZoneSpecificPrismsApplied(request)
        return response.outputs

    def GetFaceZonesOfPrismControls(self, control_name) -> Any:
        """GetInteriorZonesConnectedToCellZones."""
        request = MeshingQueriesProtoModule.GetFaceZonesOfPrismControlsRequest()
        request.input = control_name
        response = self.service.GetFaceZonesOfPrismControls(request)
        return response.outputs

    def GetBaffles(self, face_zone_list) -> Any:
        """GetBaffles."""
        request = MeshingQueriesProtoModule.GetBafflesRequest()
        for items in face_zone_list:
            request.inputs.append(items)
        response = self.service.GetBaffles(request)
        return response.outputs

    def GetEmbeddedBaffles(self) -> Any:
        """GetEmbeddedBaffles."""
        request = MeshingQueriesProtoModule.Empty()
        response = self.service.GetEmbeddedBaffles(request)
        return response.outputs

    def GetWrappedZones(self) -> Any:
        """GetWrappedZones."""
        request = MeshingQueriesProtoModule.Empty()
        response = self.service.GetWrappedZones(request)
        return response.outputs

    def GetUnreferencedEdgeZones(self) -> Any:
        """GetUnreferencedEdgeZones."""
        request = MeshingQueriesProtoModule.Empty()
        response = self.service.GetUnreferencedEdgeZones(request)
        return response.outputs

    def GetUnreferencedFaceZones(self) -> Any:
        """GetUnreferencedFaceZones."""
        request = MeshingQueriesProtoModule.Empty()
        response = self.service.GetUnreferencedFaceZones(request)
        return response.outputs

    def GetUnreferencedCellZones(self) -> Any:
        """GetUnreferencedCellZones."""
        request = MeshingQueriesProtoModule.Empty()
        response = self.service.GetUnreferencedCellZones(request)
        return response.outputs

    def GetUnreferencedEdgeZonesOfFilter(self, filter) -> Any:
        """GetUnreferencedEdgeZonesOfFilter."""
        request = MeshingQueriesProtoModule.GetUnreferencedEdgeZonesOfFilterRequest()
        request.input = filter
        response = self.service.GetUnreferencedEdgeZonesOfFilter(request)
        return response.outputs

    def GetUnreferencedFaceZonesOfFilter(self, filter) -> Any:
        """GetUnreferencedFaceZonesOfFilter."""
        request = MeshingQueriesProtoModule.GetUnreferencedFaceZonesOfFilterRequest()
        request.input = filter
        response = self.service.GetUnreferencedFaceZonesOfFilter(request)
        return response.outputs

    def GetUnreferencedCellZonesOfFilter(self, filter) -> Any:
        """GetUnreferencedEdgeZonesOfFilter."""
        request = MeshingQueriesProtoModule.GetUnreferencedCellZonesOfFilterRequest()
        request.input = filter
        response = self.service.GetUnreferencedCellZonesOfFilter(request)
        return response.outputs

    def GetUnreferencedEdgeZoneIdListOfPattern(self, pattern) -> Any:
        """GetUnreferencedEdgeZoneIdListOfPattern."""
        request = (
            MeshingQueriesProtoModule.GetUnreferencedEdgeZoneIdListOfPatternRequest()
        )
        request.input = pattern
        response = self.service.GetUnreferencedEdgeZoneIdListOfPattern(request)
        return response.outputs

    def GetUnreferencedFaceZoneIdListOfPattern(self, pattern) -> Any:
        """GetUnreferencedFaceZoneIdListOfPattern."""
        request = (
            MeshingQueriesProtoModule.GetUnreferencedFaceZoneIdListOfPatternRequest()
        )
        request.input = pattern
        response = self.service.GetUnreferencedFaceZoneIdListOfPattern(request)
        return response.outputs

    def GetUnreferencedCellZoneIdListOfPattern(self, pattern) -> Any:
        """GetUnreferencedCellZoneIdListOfPattern."""
        request = (
            MeshingQueriesProtoModule.GetUnreferencedCellZoneIdListOfPatternRequest()
        )
        request.input = pattern
        response = self.service.GetUnreferencedCellZoneIdListOfPattern(request)
        return response.outputs

    def GetMaxsizeCellZoneByVolume(self, list_or_pattern) -> Any:
        """GetMaxsizeCellZoneByVolume."""
        request = MeshingQueriesProtoModule.GetMaxsizeCellZoneByVolumeRequest()
        if isinstance(list_or_pattern, str):
            request.string_input = list_or_pattern
        elif isinstance(list_or_pattern, list):
            if isinstance(list_or_pattern[0], int):
                for items in list_or_pattern:
                    request.int_inputs.append(items)
            elif isinstance(list_or_pattern[0], str):
                for items in list_or_pattern:
                    request.string_inputs.append(items)
        response = self.service.GetMaxsizeCellZoneByVolume(request)
        return response.output

    def GetMaxsizeCellZoneByCount(self, list_or_pattern) -> Any:
        """GetMaxsizeCellZoneByCount."""
        request = MeshingQueriesProtoModule.GetMaxsizeCellZoneByCountRequest()
        if isinstance(list_or_pattern, str):
            request.string_input = list_or_pattern
        elif isinstance(list_or_pattern, list):
            if isinstance(list_or_pattern[0], int):
                for items in list_or_pattern:
                    request.int_inputs.append(items)
            elif isinstance(list_or_pattern[0], str):
                for items in list_or_pattern:
                    request.string_inputs.append(items)
        response = self.service.GetMaxsizeCellZoneByCount(request)
        return response.output

    def GetMinsizeFaceZoneByArea(self, list_or_pattern) -> Any:
        """GetMinsizeFaceZoneByArea."""
        request = MeshingQueriesProtoModule.GetMinsizeFaceZoneByAreaRequest()
        if isinstance(list_or_pattern, str):
            request.string_input = list_or_pattern
        elif isinstance(list_or_pattern, list):
            if isinstance(list_or_pattern[0], int):
                for items in list_or_pattern:
                    request.int_inputs.append(items)
            elif isinstance(list_or_pattern[0], str):
                for items in list_or_pattern:
                    request.string_inputs.append(items)
        response = self.service.GetMinsizeFaceZoneByArea(request)
        return response.output

    def GetMinsizeFaceZoneByCount(self, list_or_pattern) -> Any:
        """GetMinsizeFaceZoneByCount."""
        request = MeshingQueriesProtoModule.GetMinsizeFaceZoneByCountRequest()
        if isinstance(list_or_pattern, str):
            request.string_input = list_or_pattern
        elif isinstance(list_or_pattern, list):
            if isinstance(list_or_pattern[0], int):
                for items in list_or_pattern:
                    request.int_inputs.append(items)
            elif isinstance(list_or_pattern[0], str):
                for items in list_or_pattern:
                    request.string_inputs.append(items)
        response = self.service.GetMinsizeFaceZoneByCount(request)
        return response.output

    def GetFaceZoneListByMaximumEntityCount(
        self, max_entity_count, only_boundary
    ) -> Any:
        """GetFaceZoneListByMaximumEntityCount."""
        request = MeshingQueriesProtoModule.GetFaceZoneListByMaximumEntityCountRequest()
        request.int_input = max_entity_count
        request.bool_input = only_boundary
        response = self.service.GetFaceZoneListByMaximumEntityCount(request)
        return response.outputs

    def GetEdgeZoneListByMaximumEntityCount(
        self, max_entity_count, only_boundary
    ) -> Any:
        """GetEdgeZoneListByMaximumEntityCount."""
        request = MeshingQueriesProtoModule.GetEdgeZoneListByMaximumEntityCountRequest()
        request.int_input = max_entity_count
        request.bool_input = only_boundary
        response = self.service.GetEdgeZoneListByMaximumEntityCount(request)
        return response.outputs

    def GetCellZoneListByMaximumEntityCount(self, max_entity_count) -> Any:
        """GetCellZoneListByMaximumEntityCount."""
        request = MeshingQueriesProtoModule.GetCellZoneListByMaximumEntityCountRequest()
        request.int_input = max_entity_count
        response = self.service.GetCellZoneListByMaximumEntityCount(request)
        return response.outputs

    def GetFaceZoneListByMaximumZoneArea(self, max_entity_count) -> Any:
        """GetFaceZoneListByMaximumZoneArea."""
        request = MeshingQueriesProtoModule.GetFaceZoneListByMaximumZoneAreaRequest()
        request.int_input = max_entity_count
        response = self.service.GetFaceZoneListByMaximumZoneArea(request)
        return response.outputs

    def GetFaceZoneListByMinimumZoneArea(self, max_entity_count) -> Any:
        """GetFaceZoneListByMinimumZoneArea."""
        request = MeshingQueriesProtoModule.GetFaceZoneListByMinimumZoneAreaRequest()
        request.int_input = max_entity_count
        response = self.service.GetFaceZoneListByMinimumZoneArea(request)
        return response.outputs

    def GetZonesWithFreeFaces(self, list_or_pattern) -> Any:
        """GetZonesWithFreeFaces."""
        request = MeshingQueriesProtoModule.GetZonesWithFreeFacesRequest()
        if isinstance(list_or_pattern, str):
            request.string_input = list_or_pattern
        elif isinstance(list_or_pattern, list):
            if isinstance(list_or_pattern[0], int):
                for items in list_or_pattern:
                    request.int_inputs.append(items)
            elif isinstance(list_or_pattern[0], str):
                for items in list_or_pattern:
                    request.string_inputs.append(items)
        response = self.service.GetZonesWithFreeFaces(request)
        return response.outputs

    def GetZonesWithMultiFaces(self, list_or_pattern) -> Any:
        """GetZonesWithMultiFaces."""
        request = MeshingQueriesProtoModule.GetZonesWithMultiFacesRequest()
        if isinstance(list_or_pattern, str):
            request.string_input = list_or_pattern
        elif isinstance(list_or_pattern, list):
            if isinstance(list_or_pattern[0], int):
                for items in list_or_pattern:
                    request.int_inputs.append(items)
            elif isinstance(list_or_pattern[0], str):
                for items in list_or_pattern:
                    request.string_inputs.append(items)
        response = self.service.GetZonesWithMultiFaces(request)
        return response.outputs

    def GetOverlappingFaceZones(
        self, zone_name_pattern, areal_tolerance, distance_tolerance
    ) -> Any:
        """GetOverlappingFaceZones."""
        request = MeshingQueriesProtoModule.GetOverlappingFaceZonesRequest()
        request.string_input = zone_name_pattern
        request.double_input_1 = areal_tolerance
        request.double_input_2 = distance_tolerance
        response = self.service.GetOverlappingFaceZones(request)
        return response.outputs

    def GetZonesWithMarkedFaces(self, list_or_pattern) -> Any:
        """GetZonesWithMarkedFaces."""
        request = MeshingQueriesProtoModule.GetZonesWithMarkedFacesRequest()
        if isinstance(list_or_pattern, str):
            request.string_input = list_or_pattern
        elif isinstance(list_or_pattern, list):
            if isinstance(list_or_pattern[0], int):
                for items in list_or_pattern:
                    request.int_inputs.append(items)
            elif isinstance(list_or_pattern[0], str):
                for items in list_or_pattern:
                    request.string_inputs.append(items)
        response = self.service.GetZonesWithMarkedFaces(request)
        return response.outputs

    def GetAllObjectNameList(self) -> Any:
        """GetAllObjectNameList."""
        request = MeshingQueriesProtoModule.Empty()
        response = self.service.GetAllObjectNameList(request)
        return response.outputs

    def GetObjectNameListOfType(self, type) -> Any:
        """GetObjectNameListOfType."""
        request = MeshingQueriesProtoModule.GetObjectNameListOfTypeRequest()
        request.input = type
        response = self.service.GetObjectNameListOfType(request)
        return response.outputs

    def GetObjectsOfFilter(self, filter) -> Any:
        """GetObjectsOfFilter."""
        request = MeshingQueriesProtoModule.GetObjectsOfFilterRequest()
        request.input = filter
        response = self.service.GetObjectsOfFilter(request)
        return response.outputs

    def GetRegionsOfObject(self, object) -> Any:
        """GetRegionsOfObject."""
        request = MeshingQueriesProtoModule.GetRegionsOfObjectRequest()
        request.input = object
        response = self.service.GetRegionsOfObject(request)
        return response.outputs

    def GetRegionNameListOfObject(self, object) -> Any:
        """GetRegionNameListOfObject."""
        request = MeshingQueriesProtoModule.GetRegionNameListOfObjectRequest()
        request.input = object
        response = self.service.GetRegionNameListOfObject(request)
        return response.outputs

    def GetRegionVolume(self, object_name, region_name) -> Any:
        """GetRegionVolume."""
        request = MeshingQueriesProtoModule.GetRegionVolumeRequest()
        request.string_input_1 = object_name
        request.string_input_2 = region_name
        response = self.service.GetRegionVolume(request)
        return response.output

    def GetRegionsOfFilter(self, object, filter) -> Any:
        """GetRegionsOfFilter."""
        request = MeshingQueriesProtoModule.GetRegionsOfFilterRequest()
        request.string_input_1 = object
        request.string_input_2 = filter
        response = self.service.GetRegionsOfFilter(request)
        return response.outputs

    def GetRegionNameListOfPattern(self, object, region_name_pattern) -> Any:
        """GetRegionNameListOfPattern."""
        request = MeshingQueriesProtoModule.GetRegionNameListOfPatternRequest()
        request.string_input_1 = object
        request.string_input_2 = region_name_pattern
        response = self.service.GetRegionNameListOfPattern(request)
        return response.outputs

    def GetRegionsOfFaceZones(self, face_zone_id_list) -> Any:
        """GetRegionsOfFaceZones."""
        request = MeshingQueriesProtoModule.GetRegionsOfFaceZonesRequest()
        for id in face_zone_id_list:
            request.inputs.append(id)
        response = self.service.GetRegionsOfFaceZones(request)
        return response.outputs

    def GetRegionNameListOfFaceZones(self, list_or_pattern) -> Any:
        """GetRegionNameListOfFaceZones."""
        request = MeshingQueriesProtoModule.GetRegionNameListOfFaceZonesRequest()
        if isinstance(list_or_pattern, str):
            request.input = list_or_pattern
        elif isinstance(list_or_pattern, list):
            for items in list_or_pattern:
                request.inputs.append(items)
        response = self.service.GetRegionNameListOfFaceZones(request)
        return response.outputs

    def ConvertZoneNameSymbolsToIds(self, zone_name_list) -> Any:
        """ConvertZoneNameSymbolsToIds."""
        request = MeshingQueriesProtoModule.ConvertZoneNameSymbolsToIdsRequest()
        for zone_name in zone_name_list:
            request.inputs.append(zone_name)
        response = self.service.ConvertZoneNameSymbolsToIds(request)
        return response.outputs

    def ConvertZoneNameStringsToIds(self, zone_name_list) -> Any:
        """ConvertZoneNameStringsToIds."""
        request = MeshingQueriesProtoModule.ConvertZoneNameStringsToIdsRequest()
        for zone_name in zone_name_list:
            request.inputs.append(zone_name)
        response = self.service.ConvertZoneNameStringsToIds(request)
        return response.outputs

    def ConvertZoneIdsToNameStrings(self, zone_id_list) -> Any:
        """ConvertZoneIdsToNameStrings."""
        request = MeshingQueriesProtoModule.ConvertZoneIdsToNameStringsRequest()
        for id in zone_id_list:
            request.inputs.append(id)
        response = self.service.ConvertZoneIdsToNameStrings(request)
        return response.outputs

    def ConvertZoneIdsToNameSymbols(self, zone_id_list) -> Any:
        """ConvertZoneIdsToNameSymbols."""
        request = MeshingQueriesProtoModule.ConvertZoneIdsToNameSymbolsRequest()
        for id in zone_id_list:
            request.inputs.append(id)
        response = self.service.ConvertZoneIdsToNameSymbols(request)
        return response.outputs

    def ConvertSymbolListToString(self, symbol_list) -> Any:
        """ConvertSymbolListToString."""
        request = MeshingQueriesProtoModule.ConvertSymbolListToStringRequest()
        for symbol in symbol_list:
            request.inputs.append(symbol)
        response = self.service.ConvertSymbolListToString(request)
        return response.output

    def CreateStringFromSymbolList(self, symbol_list) -> Any:
        """CreateStringFromSymbolList."""
        request = MeshingQueriesProtoModule.CreateStringFromSymbolListRequest()
        for symbol in symbol_list:
            request.inputs.append(symbol)
        response = self.service.CreateStringFromSymbolList(request)
        return response.output

    def IntegerListSubstract(self, list_1, list_2) -> Any:
        """IntegerListSubstract."""
        request = MeshingQueriesProtoModule.IntegerListSubstractRequest()
        for item in list_1:
            request.inputs_1.append(item)
        for item in list_2:
            request.inputs_2.append(item)
        response = self.service.IntegerListSubstract(request)
        return response.outputs

    def ListReplace(self, new_element, old_element, input_list) -> Any:
        """ListReplace."""
        request = MeshingQueriesProtoModule.ListReplaceRequest()
        request.input_1 = new_element
        request.input_2 = old_element
        for item in input_list:
            request.inputs.append(item)
        response = self.service.ListReplace(request)
        return response.outputs

    def RemoveElementFromList(self, new_element, input_list) -> Any:
        """RemoveElementFromList."""
        request = MeshingQueriesProtoModule.RemoveElementFromListRequest()
        request.input = new_element
        for item in input_list:
            request.inputs.append(item)
        response = self.service.RemoveElementFromList(request)
        return response.outputs

    def ListContains(self, element, input_list) -> Any:
        """ListContains."""
        request = MeshingQueriesProtoModule.ListContainsRequest()
        request.input = element
        for item in input_list:
            request.inputs.append(item)
        response = self.service.ListContains(request)
        return response.output
