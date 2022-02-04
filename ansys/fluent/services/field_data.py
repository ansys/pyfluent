from typing import List, Dict
import grpc
from ansys.api.fluent.v0 import fielddata_pb2 as FieldDataProtoModule
from ansys.api.fluent.v0 import fielddata_pb2_grpc as FieldGrpcModule


class FieldDataService:
    def __init__(self, channel: grpc.Channel, metadata):
        self.__stub = FieldGrpcModule.FieldDataStub(channel)
        self.__metadata = metadata

    def get_surfaces(self, request):
        return self.__stub.GetSurfaces(request, metadata=self.__metadata)

    def get_range(self, request):
        return self.__stub.GetRange(request, metadata=self.__metadata)

    def get_scalar_field(self, request):
        return self.__stub.GetScalarField(request, metadata=self.__metadata)

    def get_fields_info(self, request):
        return self.__stub.GetFieldsInfo(request, metadata=self.__metadata)

    def get_surfaces_info(self, request):
        return self.__stub.GetSurfacesInfo(request, metadata=self.__metadata)


class FieldData:
    """
    Provide the field data.

    Methods
    -------
    get_range(field: str, node_value: bool, surface_ids: List[int])
    -> List[float]
        Get field range i.e. minimum and maximum value.

    get_fields_info(self) -> dict
        Get fields information i.e. field name, domain and  section.

    get_surfaces_info(self) -> dict
        Get surfaces information i.e. surface name, id and type.

    get_surfaces(surface_ids: List[int], overset_mesh: bool) -> List[Dict]
        Get surfaces data i.e. coordinates and connectivity.

    def get_scalar_field(
        surface_ids: List[int], scalar_field: str, node_value: bool,
        boundary_value: bool) -> List[Dict]
        Get field data i.e. surface data and associated scalar field values.

    """

    def __init__(self, service: FieldDataService):
        self.__service = service

    def get_range(
        self, field: str, node_value: bool = False, surface_ids: List[int] = []
    ) -> List[float]:
        request = FieldDataProtoModule.GetRangeRequest()
        request.fieldName = field
        request.nodeValue = node_value
        request.surfaceid.extend(
            [FieldDataProtoModule.SurfaceId(id=int(id)) for id in surface_ids]
        )
        response = self.__service.get_range(request)
        return [response.minimum, response.maximum]

    def get_fields_info(self) -> dict:
        request = FieldDataProtoModule.GetFieldsInfoRequest()
        response = self.__service.get_fields_info(request)
        return {
            field_info.displayName: {
                "solver_name": field_info.solverName,
                "section": field_info.section,
                "domain": field_info.domain,
            }
            for field_info in response.fieldInfo
        }

    def get_surfaces_info(self) -> dict:
        request = FieldDataProtoModule.GetSurfacesInfoResponse()
        response = self.__service.get_surfaces_info(request)
        return {
            surface_info.surfaceName: {
                "surface_id": [surf.id for surf in surface_info.surfaceId],
                "zone_id": surface_info.zoneId.id,
                "zone_type": surface_info.zoneType,
                "type": surface_info.type,
            }
            for surface_info in response.surfaceInfo
        }

    def _extract_surfaces_data(self, response_iterator):
        return [
            {
                "vertices": [
                    [point.x, point.y, point.z]
                    for point in response.surfacedata.point
                ],
                "faces": [
                    [len(facet.node)] + [node for node in facet.node]
                    for facet in response.surfacedata.facet
                ],
            }
            for response in response_iterator
        ]

    def get_surfaces(
        self, surface_ids: List[int], overset_mesh: bool = False
    ) -> List[Dict]:
        request = FieldDataProtoModule.GetSurfacesRequest()
        request.surfaceid.extend(
            [FieldDataProtoModule.SurfaceId(id=int(id)) for id in surface_ids]
        )
        request.oversetMesh = overset_mesh
        response_iterator = self.__service.get_surfaces(request)
        return self._extract_surfaces_data(response_iterator)

    def _extract_scalar_field_data(self, response_iterator):
        return [
            {
                "vertices": [
                    [point.x, point.y, point.z]
                    for point in response.scalarfielddata.surfacedata.point
                ],
                "faces": [
                    [len(facet.node)] + [node for node in facet.node]
                    for facet in response.scalarfielddata.surfacedata.facet
                ],
                "scalar_field": [
                    data for data in response.scalarfielddata.scalarfield.data
                ],
                "meta_data": response.scalarfielddata.scalarfieldmetadata,
            }
            for response in response_iterator
        ]

    def get_scalar_field(
        self,
        surface_ids: List[int],
        scalar_field: str,
        node_value: bool,
        boundary_value: bool,
    ) -> List[Dict]:
        request = FieldDataProtoModule.GetScalarFieldRequest()
        request.surfaceid.extend(
            [FieldDataProtoModule.SurfaceId(id=int(id)) for id in surface_ids]
        )
        request.scalarfield = scalar_field
        request.nodevalue = node_value
        request.boundaryvalues = boundary_value
        response_iterator = self.__service.get_scalar_field(request)
        return self._extract_scalar_field_data(response_iterator)
