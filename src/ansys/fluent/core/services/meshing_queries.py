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
    def get_face_zone_at_location(
        self, request: MeshingQueriesProtoModule.GetFaceZoneAtLocationRequest
    ) -> MeshingQueriesProtoModule.GetFaceZoneAtLocationResponse:
        """get_face_zone_at_location rpc of MeshingQueriesService."""
        return self._stub.GetFaceZoneAtLocation(request, metadata=self._metadata)

    @catch_grpc_error
    def get_cell_zone_at_location(
        self, request: MeshingQueriesProtoModule.GetCellZoneAtLocationRequest
    ) -> MeshingQueriesProtoModule.GetCellZoneAtLocationResponse:
        """get_cell_zone_at_location rpc of MeshingQueriesService."""
        return self._stub.GetCellZoneAtLocation(request, metadata=self._metadata)

    @catch_grpc_error
    def get_zones_of_type(
        self, request: MeshingQueriesProtoModule.GetZonesOfTypeRequest
    ) -> MeshingQueriesProtoModule.GetZonesOfTypeResponse:
        """get_zones_of_type rpc of MeshingQueriesService."""
        return self._stub.GetZonesOfType(request, metadata=self._metadata)

    @catch_grpc_error
    def get_zones_of_group(
        self, request: MeshingQueriesProtoModule.GetZonesOfGroupRequest
    ) -> MeshingQueriesProtoModule.GetZonesOfGroupResponse:
        """get_zones_of_group rpc of MeshingQueriesService."""
        return self._stub.GetZonesOfGroup(request, metadata=self._metadata)

    @catch_grpc_error
    def get_face_zones_of_filter(
        self, request: MeshingQueriesProtoModule.GetFaceZonesOfFilterRequest
    ) -> MeshingQueriesProtoModule.GetFaceZonesOfFilterResponse:
        """get_face_zones_of_filter rpc of MeshingQueriesService."""
        return self._stub.GetFaceZonesOfFilter(request, metadata=self._metadata)

    @catch_grpc_error
    def get_cell_zones_of_filter(
        self, request: MeshingQueriesProtoModule.GetCellZonesOfFilterRequest
    ) -> MeshingQueriesProtoModule.GetCellZonesOfFilterResponse:
        """get_cell_zones_of_filter rpc of MeshingQueriesService."""
        return self._stub.GetCellZonesOfFilter(request, metadata=self._metadata)

    @catch_grpc_error
    def get_edge_zones_of_filter(
        self, request: MeshingQueriesProtoModule.GetEdgeZonesOfFilterRequest
    ) -> MeshingQueriesProtoModule.GetEdgeZonesOfFilterResponse:
        """get_edge_zones_of_filter rpc of MeshingQueriesService."""
        return self._stub.GetEdgeZonesOfFilter(request, metadata=self._metadata)

    @catch_grpc_error
    def get_node_zones_of_filter(
        self, request: MeshingQueriesProtoModule.GetNodeZonesOfFilterRequest
    ) -> MeshingQueriesProtoModule.GetNodeZonesOfFilterResponse:
        """get_node_zones_of_filter rpc of MeshingQueriesService."""
        return self._stub.GetNodeZonesOfFilter(request, metadata=self._metadata)

    @catch_grpc_error
    def get_objects_of_type(
        self, request: MeshingQueriesProtoModule.GetObjectsOfTypeRequest
    ) -> MeshingQueriesProtoModule.GetObjectsOfTypeResponse:
        """get_objects_of_type rpc of MeshingQueriesService."""
        return self._stub.GetObjectsOfType(request, metadata=self._metadata)

    @catch_grpc_error
    def get_face_zone_id_list_of_object(
        self, request: MeshingQueriesProtoModule.GetFaceZoneIdListOfObjectRequest
    ) -> MeshingQueriesProtoModule.GetFaceZoneIdListOfObjectResponse:
        """get_face_zone_id_list_of_object rpc of MeshingQueriesService."""
        return self._stub.GetFaceZoneIdListOfObject(request, metadata=self._metadata)

    @catch_grpc_error
    def get_edge_zone_id_list_of_object(
        self, request: MeshingQueriesProtoModule.GetEdgeZoneIdListOfObjectRequest
    ) -> MeshingQueriesProtoModule.GetEdgeZoneIdListOfObjectResponse:
        """get_edge_zone_id_list_of_object rpc of MeshingQueriesService."""
        return self._stub.GetEdgeZoneIdListOfObject(request, metadata=self._metadata)

    @catch_grpc_error
    def get_cell_zone_id_list_of_object(
        self, request: MeshingQueriesProtoModule.GetCellZoneIdListOfObjectRequest
    ) -> MeshingQueriesProtoModule.GetCellZoneIdListOfObjectResponse:
        """get_cell_zone_id_list_of_object rpc of MeshingQueriesService."""
        return self._stub.GetCellZoneIdListOfObject(request, metadata=self._metadata)

    @catch_grpc_error
    def get_face_zones_shared_by_regions_of_type(
        self,
        request: MeshingQueriesProtoModule.GetFaceZonesSharedByRegionsOfTypeRequest,
    ) -> MeshingQueriesProtoModule.GetFaceZonesSharedByRegionsOfTypeResponse:
        """get_face_zones_shared_by_regions_of_type rpc of MeshingQueriesService."""
        return self._stub.GetFaceZonesSharedByRegionsOfType(
            request, metadata=self._metadata
        )

    @catch_grpc_error
    def get_face_zones_of_regions(
        self, request: MeshingQueriesProtoModule.GetFaceZonesOfRegionsRequest
    ) -> MeshingQueriesProtoModule.GetFaceZonesOfRegionsResponse:
        """get_face_zones_of_regions rpc of MeshingQueriesService."""
        return self._stub.GetFaceZonesOfRegions(request, metadata=self._metadata)

    @catch_grpc_error
    def get_face_zones_of_labels(
        self, request: MeshingQueriesProtoModule.GetFaceZonesOfLabelsRequest
    ) -> MeshingQueriesProtoModule.GetFaceZonesOfLabelsResponse:
        """get_face_zones_of_labels rpc of MeshingQueriesService."""
        return self._stub.GetFaceZonesOfLabels(request, metadata=self._metadata)

    @catch_grpc_error
    def get_face_zone_id_list_of_labels(
        self,
        request: MeshingQueriesProtoModule.GetFaceZoneIdListOfLabelsRequest,
    ) -> MeshingQueriesProtoModule.GetFaceZoneIdListOfLabelsResponse:
        """get_face_zone_id_list_of_labels rpc of MeshingQueriesService."""
        return self._stub.GetFaceZoneIdListOfLabels(request, metadata=self._metadata)

    @catch_grpc_error
    def get_face_zones_of_objects(
        self, request: MeshingQueriesProtoModule.GetFaceZonesOfObjectsRequest
    ) -> MeshingQueriesProtoModule.GetFaceZonesOfObjectsResponse:
        """get_face_zones_of_objects rpc of MeshingQueriesService."""
        return self._stub.GetFaceZonesOfObjects(request, metadata=self._metadata)

    @catch_grpc_error
    def get_edge_zones_of_objects(
        self, request: MeshingQueriesProtoModule.GetEdgeZonesOfObjectsRequest
    ) -> MeshingQueriesProtoModule.GetEdgeZonesOfObjectsResponse:
        """get_edge_zones_of_objects rpc of MeshingQueriesService."""
        return self._stub.GetEdgeZonesOfObjects(request, metadata=self._metadata)

    @catch_grpc_error
    def get_face_zone_id_list_of_regions(
        self,
        request: MeshingQueriesProtoModule.GetFaceZoneIdListOfRegionsRequest,
    ) -> MeshingQueriesProtoModule.GetFaceZoneIdListOfRegionsResponse:
        """get_face_zone_id_list_of_regions rpc of MeshingQueriesService."""
        return self._stub.GetFaceZoneIdListOfRegions(request, metadata=self._metadata)

    @catch_grpc_error
    def get_prism_cell_zones(
        self,
        request: MeshingQueriesProtoModule.GetPrismCellZonesRequest,
    ) -> MeshingQueriesProtoModule.GetPrismCellZonesResponse:
        """get_prism_cell_zones rpc of MeshingQueriesService."""
        return self._stub.GetPrismCellZones(request, metadata=self._metadata)

    @catch_grpc_error
    def get_tet_cell_zones(
        self,
        request: MeshingQueriesProtoModule.GetTetCellZonesRequest,
    ) -> MeshingQueriesProtoModule.GetTetCellZonesResponse:
        """get_tet_cell_zones rpc of MeshingQueriesService."""
        return self._stub.GetTetCellZones(request, metadata=self._metadata)

    @catch_grpc_error
    def get_adjacent_cell_zones(
        self,
        request: MeshingQueriesProtoModule.GetAdjacentCellZonesRequest,
    ) -> MeshingQueriesProtoModule.GetAdjacentCellZonesResponse:
        """get_adjacent_cell_zones rpc of MeshingQueriesService."""
        return self._stub.GetAdjacentCellZones(request, metadata=self._metadata)

    @catch_grpc_error
    def get_adjacent_face_zones(
        self,
        request: MeshingQueriesProtoModule.GetAdjacentFaceZonesRequest,
    ) -> MeshingQueriesProtoModule.GetAdjacentFaceZonesResponse:
        """get_adjacent_face_zones rpc of MeshingQueriesService."""
        return self._stub.GetAdjacentFaceZones(request, metadata=self._metadata)

    @catch_grpc_error
    def get_adjacent_interior_and_boundary_face_zones(
        self,
        request: MeshingQueriesProtoModule.GetAdjacentInteriorAndBoundaryFaceZonesRequest,
    ) -> MeshingQueriesProtoModule.GetAdjacentInteriorAndBoundaryFaceZonesResponse:
        """get_adjacent_interior_and_boundary_face_zones rpc of MeshingQueriesService."""
        return self._stub.GetAdjacentInteriorAndBoundaryFaceZones(
            request, metadata=self._metadata
        )

    @catch_grpc_error
    def get_adjacent_zones_by_edge_connectivity(
        self,
        request: MeshingQueriesProtoModule.GetAdjacentZonesByEdgeConnectivityRequest,
    ) -> MeshingQueriesProtoModule.GetAdjacentZonesByEdgeConnectivityResponse:
        """get_adjacent_zones_by_edge_connectivity rpc of MeshingQueriesService."""
        return self._stub.GetAdjacentZonesByEdgeConnectivity(
            request, metadata=self._metadata
        )

    @catch_grpc_error
    def get_adjacent_zones_by_node_connectivity(
        self,
        request: MeshingQueriesProtoModule.GetAdjacentZonesByNodeConnectivityRequest,
    ) -> MeshingQueriesProtoModule.GetAdjacentZonesByNodeConnectivityResponse:
        """get_adjacent_zones_by_node_connectivity rpc of MeshingQueriesService."""
        return self._stub.GetAdjacentZonesByNodeConnectivity(
            request, metadata=self._metadata
        )

    @catch_grpc_error
    def get_shared_boundary_zones(
        self,
        request: MeshingQueriesProtoModule.GetSharedBoundaryZonesRequest,
    ) -> MeshingQueriesProtoModule.GetSharedBoundaryZonesResponse:
        """get_shared_boundary_zones rpc of MeshingQueriesService."""
        return self._stub.GetSharedBoundaryZones(request, metadata=self._metadata)

    @catch_grpc_error
    def get_interior_zones_connected_to_cell_zones(
        self,
        request: MeshingQueriesProtoModule.GetInteriorZonesConnectedToCellZonesRequest,
    ) -> MeshingQueriesProtoModule.GetInteriorZonesConnectedToCellZonesResponse:
        """get_interior_zones_connected_to_cell_zones rpc of MeshingQueriesService."""
        return self._stub.GetInteriorZonesConnectedToCellZones(
            request, metadata=self._metadata
        )

    @catch_grpc_error
    def get_face_zones_with_zone_specific_prisms_applied(
        self,
        request: MeshingQueriesProtoModule.Empty,
    ) -> MeshingQueriesProtoModule.GetFaceZonesWithZoneSpecificPrismsAppliedResponse:
        """get_face_zones_with_zone_specific_prisms_applied rpc of MeshingQueriesService."""
        return self._stub.GetFaceZonesWithZoneSpecificPrismsApplied(
            request, metadata=self._metadata
        )

    @catch_grpc_error
    def get_face_zones_of_prism_controls(
        self,
        request: MeshingQueriesProtoModule.GetFaceZonesOfPrismControlsRequest,
    ) -> MeshingQueriesProtoModule.GetFaceZonesOfPrismControlsResponse:
        """get_face_zones_of_prism_controls rpc of MeshingQueriesService."""
        return self._stub.GetFaceZonesOfPrismControls(request, metadata=self._metadata)

    @catch_grpc_error
    def get_baffles(
        self,
        request: MeshingQueriesProtoModule.GetBafflesRequest,
    ) -> MeshingQueriesProtoModule.GetBafflesResponse:
        """get_baffles rpc of MeshingQueriesService."""
        return self._stub.GetBaffles(request, metadata=self._metadata)

    @catch_grpc_error
    def get_embedded_baffles(
        self,
        request: MeshingQueriesProtoModule.Empty,
    ) -> MeshingQueriesProtoModule.GetEmbeddedBafflesResponse:
        """get_embedded_baffles rpc of MeshingQueriesService."""
        return self._stub.GetEmbeddedBaffles(request, metadata=self._metadata)

    @catch_grpc_error
    def get_wrapped_zones(
        self,
        request: MeshingQueriesProtoModule.Empty,
    ) -> MeshingQueriesProtoModule.GetWrappedZonesResponse:
        """get_wrapped_zones rpc of MeshingQueriesService."""
        return self._stub.GetWrappedZones(request, metadata=self._metadata)

    @catch_grpc_error
    def get_unreferenced_edge_zones(
        self,
        request: MeshingQueriesProtoModule.Empty,
    ) -> MeshingQueriesProtoModule.GetUnreferencedEdgeZonesResponse:
        """get_unreferenced_edge_zones rpc of MeshingQueriesService."""
        return self._stub.GetUnreferencedEdgeZones(request, metadata=self._metadata)

    @catch_grpc_error
    def get_unreferenced_face_zones(
        self,
        request: MeshingQueriesProtoModule.Empty,
    ) -> MeshingQueriesProtoModule.GetUnreferencedFaceZonesResponse:
        """get_unreferenced_face_zones rpc of MeshingQueriesService."""
        return self._stub.GetUnreferencedFaceZones(request, metadata=self._metadata)

    @catch_grpc_error
    def get_unreferenced_cell_zones(
        self,
        request: MeshingQueriesProtoModule.Empty,
    ) -> MeshingQueriesProtoModule.GetUnreferencedCellZonesResponse:
        """get_unreferenced_cell_zones rpc of MeshingQueriesService."""
        return self._stub.GetUnreferencedCellZones(request, metadata=self._metadata)

    @catch_grpc_error
    def get_unreferenced_edge_zones_of_filter(
        self,
        request: MeshingQueriesProtoModule.GetUnreferencedEdgeZonesOfFilterRequest,
    ) -> MeshingQueriesProtoModule.GetUnreferencedEdgeZonesOfFilterResponse:
        """get_unreferenced_edge_zones_of_filter rpc of MeshingQueriesService."""
        return self._stub.GetUnreferencedEdgeZonesOfFilter(
            request, metadata=self._metadata
        )

    @catch_grpc_error
    def get_unreferenced_face_zones_of_filter(
        self,
        request: MeshingQueriesProtoModule.GetUnreferencedFaceZonesOfFilterRequest,
    ) -> MeshingQueriesProtoModule.GetUnreferencedFaceZonesOfFilterResponse:
        """get_unreferenced_face_zones_of_filter rpc of MeshingQueriesService."""
        return self._stub.GetUnreferencedFaceZonesOfFilter(
            request, metadata=self._metadata
        )

    @catch_grpc_error
    def get_unreferenced_cell_zones_of_filter(
        self,
        request: MeshingQueriesProtoModule.GetUnreferencedCellZonesOfFilterRequest,
    ) -> MeshingQueriesProtoModule.GetUnreferencedCellZonesOfFilterResponse:
        """get_unreferenced_cell_zones_of_filter rpc of MeshingQueriesService."""
        return self._stub.GetUnreferencedCellZonesOfFilter(
            request, metadata=self._metadata
        )

    @catch_grpc_error
    def get_unreferenced_edge_zone_id_list_of_pattern(
        self,
        request: MeshingQueriesProtoModule.GetUnreferencedEdgeZoneIdListOfPatternRequest,
    ) -> MeshingQueriesProtoModule.GetUnreferencedEdgeZoneIdListOfPatternResponse:
        """get_unreferenced_edge_zone_id_list_of_pattern rpc of MeshingQueriesService."""
        return self._stub.GetUnreferencedEdgeZoneIdListOfPattern(
            request, metadata=self._metadata
        )

    @catch_grpc_error
    def get_unreferenced_face_zone_id_list_of_pattern(
        self,
        request: MeshingQueriesProtoModule.GetUnreferencedFaceZoneIdListOfPatternRequest,
    ) -> MeshingQueriesProtoModule.GetUnreferencedFaceZoneIdListOfPatternResponse:
        """get_unreferenced_face_zone_id_list_of_pattern rpc of MeshingQueriesService."""
        return self._stub.GetUnreferencedFaceZoneIdListOfPattern(
            request, metadata=self._metadata
        )

    @catch_grpc_error
    def get_unreferenced_cell_zone_id_list_of_pattern(
        self,
        request: MeshingQueriesProtoModule.GetUnreferencedCellZoneIdListOfPatternRequest,
    ) -> MeshingQueriesProtoModule.GetUnreferencedCellZoneIdListOfPatternResponse:
        """get_unreferenced_cell_zone_id_list_of_pattern rpc of MeshingQueriesService."""
        return self._stub.GetUnreferencedCellZoneIdListOfPattern(
            request, metadata=self._metadata
        )

    @catch_grpc_error
    def get_maxsize_cell_zone_by_volume(
        self,
        request: MeshingQueriesProtoModule.GetMaxsizeCellZoneByVolumeRequest,
    ) -> MeshingQueriesProtoModule.GetMaxsizeCellZoneByVolumeResponse:
        """get_maxsize_cell_zone_by_volume rpc of MeshingQueriesService."""
        return self._stub.GetMaxsizeCellZoneByVolume(request, metadata=self._metadata)

    @catch_grpc_error
    def get_maxsize_cell_zone_by_count(
        self,
        request: MeshingQueriesProtoModule.GetMaxsizeCellZoneByCountRequest,
    ) -> MeshingQueriesProtoModule.GetMaxsizeCellZoneByCountResponse:
        """get_maxsize_cell_zone_by_count rpc of MeshingQueriesService."""
        return self._stub.GetMaxsizeCellZoneByCount(request, metadata=self._metadata)

    @catch_grpc_error
    def get_minsize_face_zone_by_area(
        self,
        request: MeshingQueriesProtoModule.GetMinsizeFaceZoneByAreaRequest,
    ) -> MeshingQueriesProtoModule.GetMinsizeFaceZoneByAreaResponse:
        """get_minsize_face_zone_by_area rpc of MeshingQueriesService."""
        return self._stub.GetMinsizeFaceZoneByArea(request, metadata=self._metadata)

    @catch_grpc_error
    def get_minsize_face_zone_by_count(
        self,
        request: MeshingQueriesProtoModule.GetMinsizeFaceZoneByCountRequest,
    ) -> MeshingQueriesProtoModule.GetMinsizeFaceZoneByCountResponse:
        """get_minsize_face_zone_by_count rpc of MeshingQueriesService."""
        return self._stub.GetMinsizeFaceZoneByCount(request, metadata=self._metadata)

    @catch_grpc_error
    def get_face_zone_list_by_maximum_entity_count(
        self,
        request: MeshingQueriesProtoModule.GetFaceZoneListByMaximumEntityCountRequest,
    ) -> MeshingQueriesProtoModule.GetFaceZoneListByMaximumEntityCountResponse:
        """get_face_zone_list_by_maximum_entity_count rpc of MeshingQueriesService."""
        return self._stub.GetFaceZoneListByMaximumEntityCount(
            request, metadata=self._metadata
        )

    @catch_grpc_error
    def get_edge_zone_list_by_maximum_entity_count(
        self,
        request: MeshingQueriesProtoModule.GetEdgeZoneListByMaximumEntityCountRequest,
    ) -> MeshingQueriesProtoModule.GetEdgeZoneListByMaximumEntityCountResponse:
        """get_edge_zone_list_by_maximum_entity_count rpc of MeshingQueriesService."""
        return self._stub.GetEdgeZoneListByMaximumEntityCount(
            request, metadata=self._metadata
        )

    @catch_grpc_error
    def get_cell_zone_list_by_maximum_entity_count(
        self,
        request: MeshingQueriesProtoModule.GetCellZoneListByMaximumEntityCountRequest,
    ) -> MeshingQueriesProtoModule.GetCellZoneListByMaximumEntityCountResponse:
        """get_cell_zone_list_by_maximum_entity_count rpc of MeshingQueriesService."""
        return self._stub.GetCellZoneListByMaximumEntityCount(
            request, metadata=self._metadata
        )

    @catch_grpc_error
    def get_face_zone_list_by_maximum_zone_area(
        self,
        request: MeshingQueriesProtoModule.GetFaceZoneListByMaximumZoneAreaRequest,
    ) -> MeshingQueriesProtoModule.GetFaceZoneListByMaximumZoneAreaResponse:
        """get_face_zone_list_by_maximum_zone_area rpc of MeshingQueriesService."""
        return self._stub.GetFaceZoneListByMaximumZoneArea(
            request, metadata=self._metadata
        )

    @catch_grpc_error
    def get_face_zone_list_by_minimum_zone_area(
        self,
        request: MeshingQueriesProtoModule.GetFaceZoneListByMinimumZoneAreaRequest,
    ) -> MeshingQueriesProtoModule.GetFaceZoneListByMinimumZoneAreaResponse:
        """get_face_zone_list_by_minimum_zone_area rpc of MeshingQueriesService."""
        return self._stub.GetFaceZoneListByMinimumZoneArea(
            request, metadata=self._metadata
        )

    @catch_grpc_error
    def get_zones_with_free_faces(
        self,
        request: MeshingQueriesProtoModule.GetZonesWithFreeFacesRequest,
    ) -> MeshingQueriesProtoModule.GetZonesWithFreeFacesResponse:
        """get_zones_with_free_faces rpc of MeshingQueriesService."""
        return self._stub.GetZonesWithFreeFaces(request, metadata=self._metadata)

    @catch_grpc_error
    def get_zones_with_free_faces(
        self,
        request: MeshingQueriesProtoModule.GetZonesWithFreeFacesRequest,
    ) -> MeshingQueriesProtoModule.GetZonesWithFreeFacesResponse:
        """get_zones_with_free_faces rpc of MeshingQueriesService."""
        return self._stub.GetZonesWithFreeFaces(request, metadata=self._metadata)

    @catch_grpc_error
    def get_zones_with_multi_faces(
        self,
        request: MeshingQueriesProtoModule.GetZonesWithMultiFacesRequest,
    ) -> MeshingQueriesProtoModule.GetZonesWithMultiFacesResponse:
        """get_zones_with_multi_faces rpc of MeshingQueriesService."""
        return self._stub.GetZonesWithMultiFaces(request, metadata=self._metadata)

    @catch_grpc_error
    def get_overlapping_face_zones(
        self,
        request: MeshingQueriesProtoModule.GetOverlappingFaceZonesRequest,
    ) -> MeshingQueriesProtoModule.GetOverlappingFaceZonesResponse:
        """get_overlapping_face_zones rpc of MeshingQueriesService."""
        return self._stub.GetOverlappingFaceZones(request, metadata=self._metadata)

    @catch_grpc_error
    def get_zones_with_multi_faces(
        self,
        request: MeshingQueriesProtoModule.GetZonesWithMultiFacesRequest,
    ) -> MeshingQueriesProtoModule.GetZonesWithMultiFacesResponse:
        """get_zones_with_multi_faces rpc of MeshingQueriesService."""
        return self._stub.GetZonesWithMultiFaces(request, metadata=self._metadata)

    @catch_grpc_error
    def get_zones_with_marked_faces(
        self,
        request: MeshingQueriesProtoModule.GetZonesWithMarkedFacesRequest,
    ) -> MeshingQueriesProtoModule.GetZonesWithMarkedFacesResponse:
        """get_zones_with_marked_faces rpc of MeshingQueriesService."""
        return self._stub.GetZonesWithMarkedFaces(request, metadata=self._metadata)

    @catch_grpc_error
    def get_all_object_name_list(
        self,
        request: MeshingQueriesProtoModule.Empty,
    ) -> MeshingQueriesProtoModule.GetAllObjectNameListResponse:
        """get_all_object_name_list rpc of MeshingQueriesService."""
        return self._stub.GetAllObjectNameList(request, metadata=self._metadata)

    @catch_grpc_error
    def get_object_name_list_of_type(
        self,
        request: MeshingQueriesProtoModule.GetObjectNameListOfTypeRequest,
    ) -> MeshingQueriesProtoModule.GetObjectNameListOfTypeResponse:
        """get_object_name_list_of_type rpc of MeshingQueriesService."""
        return self._stub.GetObjectNameListOfType(request, metadata=self._metadata)

    @catch_grpc_error
    def get_objects_of_filter(
        self,
        request: MeshingQueriesProtoModule.GetObjectsOfFilterRequest,
    ) -> MeshingQueriesProtoModule.GetObjectsOfFilterResponse:
        """get_objects_of_filter rpc of MeshingQueriesService."""
        return self._stub.GetObjectsOfFilter(request, metadata=self._metadata)

    @catch_grpc_error
    def get_regions_of_object(
        self,
        request: MeshingQueriesProtoModule.GetRegionsOfObjectRequest,
    ) -> MeshingQueriesProtoModule.GetRegionsOfObjectResponse:
        """get_regions_of_object rpc of MeshingQueriesService."""
        return self._stub.GetRegionsOfObject(request, metadata=self._metadata)

    @catch_grpc_error
    def get_region_name_list_of_object(
        self,
        request: MeshingQueriesProtoModule.GetRegionNameListOfObjectRequest,
    ) -> MeshingQueriesProtoModule.GetRegionNameListOfObjectResponse:
        """get_region_name_list_of_object rpc of MeshingQueriesService."""
        return self._stub.GetRegionNameListOfObject(request, metadata=self._metadata)

    @catch_grpc_error
    def sort_regions_by_volume(
        self,
        request: MeshingQueriesProtoModule.SortRegionsByVolumeRequest,
    ) -> MeshingQueriesProtoModule.SortRegionsByVolumeResponse:
        """sort_regions_by_volume rpc of MeshingQueriesService."""
        return self._stub.SortRegionsByVolume(request, metadata=self._metadata)

    @catch_grpc_error
    def get_region_volume(
        self,
        request: MeshingQueriesProtoModule.GetRegionVolumeRequest,
    ) -> MeshingQueriesProtoModule.GetRegionVolumeResponse:
        """get_region_volume rpc of MeshingQueriesService."""
        return self._stub.GetRegionVolume(request, metadata=self._metadata)

    @catch_grpc_error
    def get_regions_of_filter(
        self,
        request: MeshingQueriesProtoModule.GetRegionsOfFilterRequest,
    ) -> MeshingQueriesProtoModule.GetRegionsOfFilterResponse:
        """get_regions_of_filter rpc of MeshingQueriesService."""
        return self._stub.GetRegionsOfFilter(request, metadata=self._metadata)

    @catch_grpc_error
    def get_region_name_list_of_pattern(
        self,
        request: MeshingQueriesProtoModule.GetRegionNameListOfPatternRequest,
    ) -> MeshingQueriesProtoModule.GetRegionNameListOfPatternResponse:
        """get_region_name_list_of_pattern rpc of MeshingQueriesService."""
        return self._stub.GetRegionNameListOfPattern(request, metadata=self._metadata)

    @catch_grpc_error
    def get_regions_of_face_zones(
        self,
        request: MeshingQueriesProtoModule.GetRegionsOfFaceZonesRequest,
    ) -> MeshingQueriesProtoModule.GetRegionsOfFaceZonesResponse:
        """get_regions_of_face_zones rpc of MeshingQueriesService."""
        return self._stub.GetRegionsOfFaceZones(request, metadata=self._metadata)

    @catch_grpc_error
    def find_join_pairs(
        self,
        request: MeshingQueriesProtoModule.FindJoinPairsRequest,
    ) -> MeshingQueriesProtoModule.FindJoinPairsResponse:
        """find_join_pairs rpc of MeshingQueriesService."""
        return self._stub.FindJoinPairs(request, metadata=self._metadata)

    @catch_grpc_error
    def get_region_name_list_of_face_zones(
        self,
        request: MeshingQueriesProtoModule.GetRegionNameListOfFaceZonesRequest,
    ) -> MeshingQueriesProtoModule.GetRegionNameListOfFaceZonesResponse:
        """get_region_name_list_of_face_zones rpc of MeshingQueriesService."""
        return self._stub.GetRegionNameListOfFaceZones(request, metadata=self._metadata)


class MeshingQueries:
    """
    Meshing Queries.
    """

    def __init__(self, service: MeshingQueriesService):
        """__init__ method of MeshingQueries class."""
        self.service = service
        self.region_types = ["fluid-fluid", "solid-solid", "fluid-solid"]
        self.orders = ["ascending", "descending"]

    docstring = None

    def get_allowed_region_type(self, region_type):
        if region_type not in self.region_types:
            raise ValueError(f"Allowed region types - {self.region_types}\n")

    def get_allowed_orders(self, order):
        if order not in self.orders:
            raise ValueError(f"Allowed orders - {self.orders}\n")

    def get_all_object_name_list(self) -> Any:
        """
        Return a list of all objects.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_all_object_name_list()

        """
        request = MeshingQueriesProtoModule.Empty()
        response = self.service.get_all_object_name_list(request)
        return response.objects

    def get_allowed_object(self, object):
        allowed_args = [args for args in self.get_all_object_name_list()]
        if isinstance(object, list):
            for obj in object:
                if obj not in allowed_args:
                    raise ValueError(f"Allowed objects - {allowed_args}\n")
        elif isinstance(object, str):
            if object not in allowed_args:
                raise ValueError(f"Allowed objects - {allowed_args}\n")

    def get_region_name_list_of_object(self, object) -> Any:
        """
        Return a list of regions in the specified object.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_region_name_list_of_object("elbow-fluid")

        """
        self.get_allowed_object(object)
        request = MeshingQueriesProtoModule.GetRegionNameListOfObjectRequest()
        request.object = object
        response = self.service.get_region_name_list_of_object(request)
        return response.regions

    def get_allowed_region(self, region):
        objects = [objs for objs in self.get_all_object_name_list()]
        regions = []
        for obj in objects:
            regions.extend(self.get_region_name_list_of_object(obj))
        if isinstance(region, list):
            for reg in region:
                if reg not in regions:
                    raise ValueError(f"Allowed regions - {regions}\n")
        elif isinstance(region, str):
            if region not in regions:
                raise ValueError(f"Allowed regions - {regions}\n")

    def get_face_zone_at_location(self, location) -> Any:
        """
        Return face zone at or closest to a specified location.

        Note:  This function is not applicable to polyhedral meshes.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_face_zone_at_location([1.4, 1.4, 1.4])

        """
        request = MeshingQueriesProtoModule.GetFaceZoneAtLocationRequest()
        request.location.x = location[0]
        request.location.y = location[1]
        request.location.z = location[2]
        response = self.service.get_face_zone_at_location(request)
        return response.face_zone_id

    def get_cell_zone_at_location(self, location) -> Any:
        """
        Return cell zone at or closest to a specified location.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_cell_zone_at_location([1.4, 1.4, 1.4])

        """
        request = MeshingQueriesProtoModule.GetCellZoneAtLocationRequest()
        request.location.x = location[0]
        request.location.y = location[1]
        request.location.z = location[2]
        response = self.service.get_cell_zone_at_location(request)
        return response.cell_zone_id

    def get_zones_of_type(self, type) -> Any:
        """
        Return a list of zones of the specified default zone type.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_zones_of_type("velocity-inlet")

        """
        request = MeshingQueriesProtoModule.GetZonesOfTypeRequest()
        request.type = type
        response = self.service.get_zones_of_type(request)
        return response.zone_ids

    def get_zones_of_group(self, group) -> Any:
        """
        Return a list of zones of the specified default zone group or user-defined group.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_zones_of_group("inlet")

        """
        request = MeshingQueriesProtoModule.GetZonesOfGroupRequest()
        request.group = group
        response = self.service.get_zones_of_group(request)
        return response.zone_ids

    def get_face_zones_of_filter(self, filter) -> Any:
        """
        Return a list of face zones whose names contain the specified filter string.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_face_zones_of_filter("*")

        """
        request = MeshingQueriesProtoModule.GetFaceZonesOfFilterRequest()
        request.filter = filter
        response = self.service.get_face_zones_of_filter(request)
        return response.face_zone_ids

    def get_cell_zones_of_filter(self, filter) -> Any:
        """
        Return a list of cell zones whose names contain the specified filter string.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_cell_zones_of_filter("*")

        """
        request = MeshingQueriesProtoModule.GetCellZonesOfFilterRequest()
        request.filter = filter
        response = self.service.get_cell_zones_of_filter(request)
        return response.cell_zone_ids

    def get_edge_zones_of_filter(self, filter) -> Any:
        """
        Return a list of edge zones whose names contain the specified filter string.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_edge_zones_of_filter("*")

        """
        request = MeshingQueriesProtoModule.GetEdgeZonesOfFilterRequest()
        request.filter = filter
        response = self.service.get_edge_zones_of_filter(request)
        return response.edge_zone_ids

    def get_node_zones_of_filter(self, filter) -> Any:
        """
        Return a list of node zones whose names contain the specified filter string.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_node_zones_of_filter("*")

        """
        request = MeshingQueriesProtoModule.GetNodeZonesOfFilterRequest()
        request.filter = filter
        response = self.service.get_node_zones_of_filter(request)
        return response.node_zone_ids

    def get_objects_of_type(self, type) -> Any:
        """
        Return a list of objects of the specified type.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_objects_of_type("mesh")

        """
        request = MeshingQueriesProtoModule.GetObjectsOfTypeRequest()
        request.type = type
        response = self.service.get_objects_of_type(request)
        return response.objects

    def get_face_zone_id_list_of_object(self, object) -> Any:
        """
        Return a list of face zones by ID in the specified face zone labels of an object.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_face_zone_id_list_of_object("elbow-fluid")

        """
        self.get_allowed_object(object)
        request = MeshingQueriesProtoModule.GetFaceZoneIdListOfObjectRequest()
        request.object = object
        response = self.service.get_face_zone_id_list_of_object(request)
        return response.face_zone_ids

    def get_edge_zone_id_list_of_object(self, object) -> Any:
        """
        Return a list of edge zones by ID in the specified face zone labels of an object

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_edge_zone_id_list_of_object("elbow-fluid")

        """
        self.get_allowed_object(object)
        request = MeshingQueriesProtoModule.GetEdgeZoneIdListOfObjectRequest()
        request.object = object
        response = self.service.get_edge_zone_id_list_of_object(request)
        return response.edge_zone_ids

    def get_cell_zone_id_list_of_object(self, object) -> Any:
        """
        Return a list of cell zones by ID in the specified face zone labels of an object.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_cell_zone_id_list_of_object("elbow-fluid")

        """
        self.get_allowed_object(object)
        request = MeshingQueriesProtoModule.GetCellZoneIdListOfObjectRequest()
        request.object = object
        response = self.service.get_cell_zone_id_list_of_object(request)
        return response.cell_zone_ids

    def get_face_zones_shared_by_regions_of_type(self, mesh_object, region_type) -> Any:
        """
        Return a list of face zones shared by regions of specified types in the mesh object specified,
        where region-type is fluid-fluid, solid-solid, or fluid-solid.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_face_zones_shared_by_regions_of_type("elbow-fluid", "fluid-fluid")

        """
        self.get_allowed_object(mesh_object)
        self.get_allowed_region_type(region_type)
        request = MeshingQueriesProtoModule.GetFaceZonesSharedByRegionsOfTypeRequest()
        request.mesh_object = mesh_object
        request.region_type = region_type
        response = self.service.get_face_zones_shared_by_regions_of_type(request)
        return response.shared_face_zone_ids

    def get_face_zones_of_regions(self, object, region_name_list) -> Any:
        """
        Return a list of face zones in the specified regions.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_face_zones_of_regions("elbow-fluid", ["fluid"])

        """
        self.get_allowed_object(object)
        self.get_allowed_region(region_name_list)
        request = MeshingQueriesProtoModule.GetFaceZonesOfRegionsRequest()
        request.object = object
        for region in region_name_list:
            request.regions.append(region)
        response = self.service.get_face_zones_of_regions(request)
        return response.zone_ids

    def get_face_zones_of_labels(self, object, label_name_list) -> Any:
        """
        Return a list of face zones in the specified face zone labels of the object specified.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_face_zones_of_labels("elbow-fluid", ["inlet", "outlet", "wall", "internal"])

        """
        request = MeshingQueriesProtoModule.GetFaceZonesOfLabelsRequest()
        request.object = object
        for label in label_name_list:
            request.labels.append(label)
        response = self.service.get_face_zones_of_labels(request)
        return response.zone_ids

    def get_face_zone_id_list_of_labels(self, object, zone_label_list) -> Any:
        """
        Return a list of face zones by ID in the specified face zone labels of an object.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_face_zone_id_list_of_labels("elbow-fluid", ["outlet"])

        """
        request = MeshingQueriesProtoModule.GetFaceZoneIdListOfLabelsRequest()
        request.object = object
        for zone_label in zone_label_list:
            request.labels.append(zone_label)
        response = self.service.get_face_zone_id_list_of_labels(request)
        return response.zone_ids

    def get_face_zones_of_objects(self, object_list) -> Any:
        """
        Return a list of face zones in the specified objects.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_face_zones_of_objects(["elbow-fluid"])

        """
        self.get_allowed_object(object_list)
        request = MeshingQueriesProtoModule.GetFaceZonesOfObjectsRequest()
        for object in object_list:
            request.object_list.append(object)
        response = self.service.get_face_zones_of_objects(request)
        return response.face_zone_ids

    def get_edge_zones_of_objects(self, object_list) -> Any:
        """
        Return a list of edge zones in the specified objects.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_edge_zones_of_objects(["elbow-fluid"])

        """
        self.get_allowed_object(object_list)
        request = MeshingQueriesProtoModule.GetEdgeZonesOfObjectsRequest()
        for object in object_list:
            request.object_list.append(object)
        response = self.service.get_edge_zones_of_objects(request)
        return response.edge_zone_ids

    def get_face_zone_id_list_of_regions(self, object, region_list) -> Any:
        """
        Return a list of face zones by ID in the specified regions of an object.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_face_zone_id_list_of_regions("elbow-fluid", ["fluid"])

        """
        self.get_allowed_object(object)
        self.get_allowed_region(region_list)
        request = MeshingQueriesProtoModule.GetFaceZoneIdListOfRegionsRequest()
        request.object = object
        for region in region_list:
            request.labels.append(region)
        response = self.service.get_face_zone_id_list_of_regions(request)
        return response.zone_ids

    def get_prism_cell_zones(self, list_or_pattern) -> Any:
        """
        Return a list of prism cell zones.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_prism_cell_zones(["inlet", "outlet"])

            >>> meshing_session.meshing_queries.get_prism_cell_zones("*")

        """
        request = MeshingQueriesProtoModule.GetPrismCellZonesRequest()
        if isinstance(list_or_pattern, str):
            request.zone_name_or_pattern = list_or_pattern
        elif isinstance(list_or_pattern, list):
            for items in list_or_pattern:
                request.zones.append(items)
        response = self.service.get_prism_cell_zones(request)
        return response.prism_cell_zones

    def get_tet_cell_zones(self, list_or_pattern) -> Any:
        """
        Return a list of tet cell zones.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_tet_cell_zones(["inlet", "outlet"])

            >>> meshing_session.meshing_queries.get_tet_cell_zones("*")

        """
        request = MeshingQueriesProtoModule.GetTetCellZonesRequest()
        if isinstance(list_or_pattern, str):
            request.zone_name_or_pattern = list_or_pattern
        elif isinstance(list_or_pattern, list):
            for items in list_or_pattern:
                request.zones.append(items)
        response = self.service.get_tet_cell_zones(request)
        return response.tet_cell_zones

    def get_adjacent_cell_zones(self, list_or_name_or_pattern) -> Any:
        """
        Return adjacent cell zones for given face zone

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_adjacent_cell_zones([30])

            >>> meshing_session.meshing_queries.get_adjacent_cell_zones("*")

        """
        request = MeshingQueriesProtoModule.GetAdjacentCellZonesRequest()
        if isinstance(list_or_name_or_pattern, str):
            request.zone_name_or_pattern = list_or_name_or_pattern
        elif isinstance(list_or_name_or_pattern, list):
            for items in list_or_name_or_pattern:
                request.face_zone_ids.append(items)
        response = self.service.get_adjacent_cell_zones(request)
        return response.adjacent_cell_zones

    def get_adjacent_face_zones(self, list_or_name_or_pattern) -> Any:
        """
        Return adjacent boundary face zones for given cell zones.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_adjacent_face_zones([3460])

            >>> meshing_session.meshing_queries.get_adjacent_face_zones("*")

        """
        request = MeshingQueriesProtoModule.GetAdjacentFaceZonesRequest()
        if isinstance(list_or_name_or_pattern, str):
            request.zone_name_or_pattern = list_or_name_or_pattern
        elif isinstance(list_or_name_or_pattern, list):
            for items in list_or_name_or_pattern:
                request.cell_zone_ids.append(items)
        response = self.service.get_adjacent_face_zones(request)
        return response.adjacent_boundary_face_zones

    def get_adjacent_interior_and_boundary_face_zones(
        self, list_or_name_or_pattern
    ) -> Any:
        """
        Return adjacent interior and boundary face zones for given cell zones.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_adjacent_interior_and_boundary_face_zones([30])

            >>> meshing_session.meshing_queries.get_adjacent_interior_and_boundary_face_zones("fluid")

            >>> meshing_session.meshing_queries.get_adjacent_interior_and_boundary_face_zones("*")

        """
        request = (
            MeshingQueriesProtoModule.GetAdjacentInteriorAndBoundaryFaceZonesRequest()
        )
        if isinstance(list_or_name_or_pattern, str):
            request.zone_name_or_pattern = list_or_name_or_pattern
        elif isinstance(list_or_name_or_pattern, list):
            for items in list_or_name_or_pattern:
                request.cell_zone_ids.append(items)
        response = self.service.get_adjacent_interior_and_boundary_face_zones(request)
        return response.adjacent_interior_and_boundary_face_zones

    def get_adjacent_zones_by_edge_connectivity(self, list_or_name_or_pattern) -> Any:
        """
        Return adjacent zones based on edge connectivity

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_adjacent_zones_by_edge_connectivity([30])

            >>> meshing_session.meshing_queries.get_adjacent_zones_by_edge_connectivity("*")

        """
        request = MeshingQueriesProtoModule.GetAdjacentZonesByEdgeConnectivityRequest()
        if isinstance(list_or_name_or_pattern, str):
            request.zone_name_or_pattern = list_or_name_or_pattern
        elif isinstance(list_or_name_or_pattern, list):
            for items in list_or_name_or_pattern:
                request.zone_ids.append(items)
        response = self.service.get_adjacent_zones_by_edge_connectivity(request)
        return response.adjacent_zone_ids

    def get_adjacent_zones_by_node_connectivity(self, list_or_name_or_pattern) -> Any:
        """
        Return adjacent zones based on node connectivity

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_adjacent_zones_by_node_connectivity([30])

            >>> meshing_session.meshing_queries.get_adjacent_zones_by_node_connectivity("*")

        """
        request = MeshingQueriesProtoModule.GetAdjacentZonesByNodeConnectivityRequest()
        if isinstance(list_or_name_or_pattern, str):
            request.zone_name_or_pattern = list_or_name_or_pattern
        elif isinstance(list_or_name_or_pattern, list):
            for items in list_or_name_or_pattern:
                request.zone_ids.append(items)
        response = self.service.get_adjacent_zones_by_node_connectivity(request)
        return response.adjacent_zone_ids

    def get_shared_boundary_zones(self, list_or_name_or_pattern) -> Any:
        """
        Returns the number of faces and the boundary face zones that are shared with the specified cell zones.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_shared_boundary_zones("*")

            >>> meshing_session.meshing_queries.get_shared_boundary_zones([3460])

        """
        request = MeshingQueriesProtoModule.GetSharedBoundaryZonesRequest()
        if isinstance(list_or_name_or_pattern, str):
            request.cell_zone_name_or_pattern = list_or_name_or_pattern
        elif isinstance(list_or_name_or_pattern, list):
            for items in list_or_name_or_pattern:
                request.cell_zone_ids.append(items)
        response = self.service.get_shared_boundary_zones(request)
        return response.shared_boundary_zone_ids

    def get_interior_zones_connected_to_cell_zones(
        self, list_or_name_or_pattern
    ) -> Any:
        """
        Returns interior face zones connected to given cell zones.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_interior_zones_connected_to_cell_zones([3460])

            >>> meshing_session.meshing_queries.get_interior_zones_connected_to_cell_zones("*")

        """
        request = (
            MeshingQueriesProtoModule.GetInteriorZonesConnectedToCellZonesRequest()
        )
        if isinstance(list_or_name_or_pattern, str):
            request.cell_zone_name_or_pattern = list_or_name_or_pattern
        elif isinstance(list_or_name_or_pattern, list):
            for items in list_or_name_or_pattern:
                request.face_zone_ids.append(items)
        response = self.service.get_interior_zones_connected_to_cell_zones(request)
        return response.interior_zone_ids

    def get_face_zones_with_zone_specific_prisms_applied(self) -> Any:
        """
        Return a list of face zones with zone-specific prism settings applied.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_face_zones_with_zone_specific_prisms_applied()

        """
        request = MeshingQueriesProtoModule.Empty()
        response = self.service.get_face_zones_with_zone_specific_prisms_applied(
            request
        )
        return response.face_zone_ids

    def get_face_zones_of_prism_controls(self, control_name) -> Any:
        """
        Return a list of face zones to which the specified prism controls apply.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_face_zones_of_prism_controls("*")

        """
        request = MeshingQueriesProtoModule.GetFaceZonesOfPrismControlsRequest()
        request.control_name = control_name
        response = self.service.get_face_zones_of_prism_controls(request)
        return response.face_zone_ids

    def get_baffles(self, face_zone_list) -> Any:
        """
        Return the baffle zones based on the face zone list specified.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_baffles([29, 30])

        """
        request = MeshingQueriesProtoModule.GetBafflesRequest()
        for items in face_zone_list:
            request.face_zone_ids.append(items)
        response = self.service.get_baffles(request)
        return response.baffle_zone_ids

    def get_embedded_baffles(self) -> Any:
        """
        Return the embedded baffle zones.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_embedded_baffles()

        """
        request = MeshingQueriesProtoModule.Empty()
        response = self.service.get_embedded_baffles(request)
        return response.embedded_baffles_zone_ids

    def get_wrapped_zones(self) -> Any:
        """
        Return a list of wrapped face zones.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_wrapped_zones()

        """
        request = MeshingQueriesProtoModule.Empty()
        response = self.service.get_wrapped_zones(request)
        return response.wrapped_face_zone_ids

    def get_unreferenced_edge_zones(self) -> Any:
        """
        Return a list of unreferenced edge zones.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_unreferenced_edge_zones()

        """
        request = MeshingQueriesProtoModule.Empty()
        response = self.service.get_unreferenced_edge_zones(request)
        return response.unreferenced_edge_zone_ids

    def get_unreferenced_face_zones(self) -> Any:
        """
        Return a list of unreferenced face zones.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_unreferenced_face_zones()

        """
        request = MeshingQueriesProtoModule.Empty()
        response = self.service.get_unreferenced_face_zones(request)
        return response.unreferenced_face_zone_ids

    def get_unreferenced_cell_zones(self) -> Any:
        """
        Return a list of unreferenced cell zones.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_unreferenced_cell_zones()

        """
        request = MeshingQueriesProtoModule.Empty()
        response = self.service.get_unreferenced_cell_zones(request)
        return response.unreferenced_cell_zone_ids

    def get_unreferenced_edge_zones_of_filter(self, filter) -> Any:
        """
        Return a list of unreferenced edge zones whose names contain the specified filter string.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_unreferenced_edge_zones_of_filter("*")

        """
        request = MeshingQueriesProtoModule.GetUnreferencedEdgeZonesOfFilterRequest()
        request.filter = filter
        response = self.service.get_unreferenced_edge_zones_of_filter(request)
        return response.unreferenced_edge_zone_ids

    def get_unreferenced_face_zones_of_filter(self, filter) -> Any:
        """
        Return a list of unreferenced face zones whose names contain the specified filter string.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_unreferenced_face_zones_of_filter("*")

        """
        request = MeshingQueriesProtoModule.GetUnreferencedFaceZonesOfFilterRequest()
        request.filter = filter
        response = self.service.get_unreferenced_face_zones_of_filter(request)
        return response.unreferenced_face_zone_ids

    def get_unreferenced_cell_zones_of_filter(self, filter) -> Any:
        """
        Return a list of unreferenced cell zones whose names contain the specified filter string.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_unreferenced_cell_zones_of_filter("*")

        """
        request = MeshingQueriesProtoModule.GetUnreferencedCellZonesOfFilterRequest()
        request.filter = filter
        response = self.service.get_unreferenced_cell_zones_of_filter(request)
        return response.unreferenced_cell_zone_ids

    def get_unreferenced_edge_zone_id_list_of_pattern(self, pattern) -> Any:
        """
        Return a list of unreferenced edge zones by ID, whose names contain the specified pattern.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_unreferenced_edge_zone_id_list_of_pattern("*")

        """
        request = (
            MeshingQueriesProtoModule.GetUnreferencedEdgeZoneIdListOfPatternRequest()
        )
        request.pattern = pattern
        response = self.service.get_unreferenced_edge_zone_id_list_of_pattern(request)
        return response.unreferenced_edge_zone_ids

    def get_unreferenced_face_zone_id_list_of_pattern(self, pattern) -> Any:
        """
        Return a list of unreferenced face zones by ID, whose names contain the specified pattern.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_unreferenced_face_zone_id_list_of_pattern("*")

        """
        request = (
            MeshingQueriesProtoModule.GetUnreferencedFaceZoneIdListOfPatternRequest()
        )
        request.pattern = pattern
        response = self.service.get_unreferenced_face_zone_id_list_of_pattern(request)
        return response.unreferenced_face_zone_ids

    def get_unreferenced_cell_zone_id_list_of_pattern(self, pattern) -> Any:
        """
        Return a list of unreferenced cell zones by ID, whose names contain the specified pattern.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_unreferenced_cell_zone_id_list_of_pattern("*")

        """
        request = (
            MeshingQueriesProtoModule.GetUnreferencedCellZoneIdListOfPatternRequest()
        )
        request.pattern = pattern
        response = self.service.get_unreferenced_cell_zone_id_list_of_pattern(request)
        return response.unreferenced_cell_zone_ids

    def get_maxsize_cell_zone_by_volume(self, list_or_pattern) -> Any:
        """
        Return cell zone with maximum volume for given list or pattern of cell zones.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_maxsize_cell_zone_by_volume("*")

            >>> meshing_session.meshing_queries.get_maxsize_cell_zone_by_volume([3460])

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
        response = self.service.get_maxsize_cell_zone_by_volume(request)
        return response.cell_zone_id

    def get_maxsize_cell_zone_by_count(self, list_or_pattern) -> Any:
        """
        Return cell zone with maximum count of elements for given list or pattern of cell zones.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_maxsize_cell_zone_by_count("*")

            >>> meshing_session.meshing_queries.get_maxsize_cell_zone_by_count([3460])

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
        response = self.service.get_maxsize_cell_zone_by_count(request)
        return response.cell_zone_id

    def get_minsize_face_zone_by_area(self, list_or_pattern) -> Any:
        """
        Return face zone with minimum area for given list or pattern of face zones.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_minsize_face_zone_by_area("*")

            >>> meshing_session.meshing_queries.get_minsize_face_zone_by_area([29, 30, 31, 32, 33, 34])

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
        response = self.service.get_minsize_face_zone_by_area(request)
        return response.face_zone_id

    def get_minsize_face_zone_by_count(self, list_or_pattern) -> Any:
        """
        Return face zone with minimum count of elements for given list or pattern of face zones.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_minsize_face_zone_by_count("*")

            >>> meshing_session.meshing_queries.get_minsize_face_zone_by_count([29, 30, 31, 32, 33, 34])

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
        response = self.service.get_minsize_face_zone_by_count(request)
        return response.face_zone_id

    def get_face_zone_list_by_maximum_entity_count(
        self, max_entity_count, only_boundary
    ) -> Any:
        """
        Return a list of face zones with a count below the maximum entity count (maximum-entity-count) specified.
        You can choose to restrict the report to only boundary edge zones, if required (only-boundary? set to True or False).

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_face_zone_list_by_maximum_entity_count(20, True)

        """
        request = MeshingQueriesProtoModule.GetFaceZoneListByMaximumEntityCountRequest()
        request.maximum_entity_count = max_entity_count
        request.only_boundary = only_boundary
        response = self.service.get_face_zone_list_by_maximum_entity_count(request)
        return response.face_zone_ids

    def get_edge_zone_list_by_maximum_entity_count(
        self, max_entity_count, only_boundary
    ) -> Any:
        """
        Return a list of edge zones with a count below the maximum entity count (maximum-entity-count) specified.
        You can choose to restrict the report to only boundary edge zones, if required (only-boundary? set to True or False).

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_edge_zone_list_by_maximum_entity_count(20, False)

        """
        request = MeshingQueriesProtoModule.GetEdgeZoneListByMaximumEntityCountRequest()
        request.maximum_entity_count = max_entity_count
        request.only_boundary = only_boundary
        response = self.service.get_edge_zone_list_by_maximum_entity_count(request)
        return response.edge_zone_ids

    def get_cell_zone_list_by_maximum_entity_count(self, maximum_entity_count) -> Any:
        """
        Return a list of cell zones with a count below the maximum entity count (maximum-entity-count) specified.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_cell_zone_list_by_maximum_entity_count(1)

        """
        request = MeshingQueriesProtoModule.GetCellZoneListByMaximumEntityCountRequest()
        request.maximum_entity_count = maximum_entity_count
        response = self.service.get_cell_zone_list_by_maximum_entity_count(request)
        return response.cell_zone_ids

    def get_face_zone_list_by_maximum_zone_area(self, maximum_zone_area) -> Any:
        """
        Return a list of face zones with a maximum zone area below the maximum-zone-area specified.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_face_zone_list_by_maximum_zone_area(100)

        """
        request = MeshingQueriesProtoModule.GetFaceZoneListByMaximumZoneAreaRequest()
        request.maximum_zone_area = maximum_zone_area
        response = self.service.get_face_zone_list_by_maximum_zone_area(request)
        return response.face_zone_ids

    def get_face_zone_list_by_minimum_zone_area(self, minimum_zone_area) -> Any:
        """
        Return a list of face zones with a minimum zone area above the minimum-zone-area specified.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_face_zone_list_by_minimum_zone_area(10)

        """
        request = MeshingQueriesProtoModule.GetFaceZoneListByMinimumZoneAreaRequest()
        request.minimum_zone_area = minimum_zone_area
        response = self.service.get_face_zone_list_by_minimum_zone_area(request)
        return response.face_zone_ids

    def get_zones_with_free_faces(self, list_or_pattern) -> Any:
        """
        Return a list of zones with free faces for the face zones specified.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_zones_with_free_faces("*")

            >>> meshing_session.meshing_queries.get_zones_with_free_faces([29, 30, 31, 32])

            >>> meshing_session.meshing_queries.get_zones_with_free_faces(["inlet", "outlet"])

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
        response = self.service.get_zones_with_free_faces(request)
        return response.zones_with_free_faces

    def get_zones_with_multi_faces(self, list_or_pattern) -> Any:
        """
        Return a list of zones with multi-connected faces for the face zones specified.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_zones_with_multi_faces("*")

            >>> meshing_session.meshing_queries.get_zones_with_multi_faces([29, 30, 31, 32])

            >>> meshing_session.meshing_queries.get_zones_with_multi_faces(["inlet", "outlet"])

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
        response = self.service.get_zones_with_multi_faces(request)
        return response.zones_with_multi_connected_faces

    def get_overlapping_face_zones(
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
        response = self.service.get_overlapping_face_zones(request)
        return response.overlapping_face_zone_ids

    def get_zones_with_marked_faces(self, list_or_pattern) -> Any:
        """
        Return a list of zones with marked faces for the face zones specified.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_zones_with_marked_faces("*")

            >>> meshing_session.meshing_queries.get_zones_with_marked_faces([29, 30, 31, 32])

            >>> meshing_session.meshing_queries.get_zones_with_marked_faces(["inlet", "outlet"])

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
        response = self.service.get_zones_with_marked_faces(request)
        return response.zones_with_marked_faces

    def get_object_name_list_of_type(self, type) -> Any:
        """
        Return a list of objects of the specified type.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_object_name_list_of_type("mesh")

        """
        request = MeshingQueriesProtoModule.GetObjectNameListOfTypeRequest()
        request.type = type
        response = self.service.get_object_name_list_of_type(request)
        return response.objects

    def get_objects_of_filter(self, filter) -> Any:
        """
        Return a list of objects whose names contain the specified filter string.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_objects_of_filter("*")

        """
        request = MeshingQueriesProtoModule.GetObjectsOfFilterRequest()
        request.filter = filter
        response = self.service.get_objects_of_filter(request)
        return response.objects

    def get_regions_of_object(self, object) -> Any:
        """
        Return a list of regions in the specified object.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_regions_of_object("elbow-fluid")

        """
        self.get_allowed_object(object)
        request = MeshingQueriesProtoModule.GetRegionsOfObjectRequest()
        request.object = object
        response = self.service.get_regions_of_object(request)
        return response.regions

    def sort_regions_by_volume(self, object_name, order) -> Any:
        """
        Returns a sorted list of volumetric regions by volume for the object specified.
        Specify the order (ascending or descending).

        .. code-block:: python

            >>> meshing_session.meshing_queries.sort_regions_by_volume("elbow-fluid", "ascending")

        """
        self.get_allowed_object(object_name)
        self.get_allowed_orders(order)
        request = MeshingQueriesProtoModule.SortRegionsByVolumeRequest()
        request.object_name = object_name
        request.order = order
        response = self.service.sort_regions_by_volume(request)
        return response.regions

    def get_region_volume(self, object_name, region_name) -> Any:
        """
        Return the region volume for the specified region of an object.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_region_volume("elbow-fluid", "fluid")

        """
        self.get_allowed_object(object_name)
        self.get_allowed_region(region_name)
        request = MeshingQueriesProtoModule.GetRegionVolumeRequest()
        request.object_name = object_name
        request.region_name = region_name
        response = self.service.get_region_volume(request)
        return response.region_volume

    def get_regions_of_filter(self, object, filter) -> Any:
        """
        Return a list of regions in the specified object, whose names contain the specified filter string.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_regions_of_filter("elbow-fluid", "*")

        """
        request = MeshingQueriesProtoModule.GetRegionsOfFilterRequest()
        request.object = object
        request.filter = filter
        response = self.service.get_regions_of_filter(request)
        return response.regions

    def get_region_name_list_of_pattern(self, object, region_name_or_pattern) -> Any:
        """
        Return a list of regions in the specified object, whose names contain the specified name pattern.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_region_name_list_of_pattern("elbow-fluid", "*")

        """
        request = MeshingQueriesProtoModule.GetRegionNameListOfPatternRequest()
        request.object = object
        request.region_name_or_pattern = region_name_or_pattern
        response = self.service.get_region_name_list_of_pattern(request)
        return response.regions

    def get_regions_of_face_zones(self, list_of_face_zone_ids) -> Any:
        """
        Return a list of regions containing the face zones specified.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_regions_of_face_zones([29, 30, 31, 32, 33, 34])

        """
        request = MeshingQueriesProtoModule.GetRegionsOfFaceZonesRequest()
        for id in list_of_face_zone_ids:
            request.face_zone_ids.append(id)
        response = self.service.get_regions_of_face_zones(request)
        return response.regions

    def find_join_pairs(
        self, face_zone_list_or_pattern, join_tolerance, absolute_tolerance, join_angle
    ) -> Any:
        """
        Return the pairs of overlapping face zones based on the join tolerance and feature angle.

        .. code-block:: python

            >>> meshing_session.meshing_queries.find_join_pairs("outlet", 0.1, True, 40)

            >>> meshing_session.meshing_queries.find_join_pairs([32], 0.1, True, 40))

            >>> meshing_session.meshing_queries.find_join_pairs(["outlet"], 0.1, True, 40)

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
        response = self.service.find_join_pairs(request)
        return response.pairs

    def get_region_name_list_of_face_zones(self, list_or_pattern) -> Any:
        """
        Return a list of regions containing the face zones specified.

        .. code-block:: python

            >>> meshing_session.meshing_queries.get_region_name_list_of_face_zones([29, 30, 31, 32, 33, 34])

        """
        request = MeshingQueriesProtoModule.GetRegionNameListOfFaceZonesRequest()
        if isinstance(list_or_pattern, str):
            request.face_zone_name_or_pattern = list_or_pattern
        elif isinstance(list_or_pattern, list):
            for items in list_or_pattern:
                request.face_zone_ids.append(items)
        response = self.service.get_region_name_list_of_face_zones(request)
        return response.regions
