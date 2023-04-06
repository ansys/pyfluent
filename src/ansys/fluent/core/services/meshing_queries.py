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

    # @catch_grpc_error
    # def GetFaceZonesOfPrismControls(
    #     self,
    #     request: MeshingQueriesProtoModule.GetFaceZonesOfPrismControlsRequest,
    # ) -> MeshingQueriesProtoModule.GetFaceZonesOfPrismControlsResponse:
    #     """GetFaceZonesOfPrismControls rpc of MeshingQueriesService."""
    #     return self._stub.GetFaceZonesOfPrismControls(
    #         request, metadata=self._metadata
    #     )

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

    # def GetFaceZonesOfPrismControls(self, control_name) -> Any:
    #     """GetInteriorZonesConnectedToCellZones."""
    #     request = MeshingQueriesProtoModule.GetFaceZonesOfPrismControlsRequest()
    #     request.input = control_name
    #     response = self.service.GetFaceZonesOfPrismControls(request)
    #     return response.outputs

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
