# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Wrapper over the field data gRPC service of Fluent (v1 proto API)."""

import grpc
import numpy as np

from ansys.api.fluent.v1 import field_data_pb2, field_data_pb2_grpc
from ansys.fluent.core._grpc_services.streaming_service import StreamingService
from ansys.fluent.core.field_data_interfaces import (
    SurfaceDataType,
    _to_field_name_str,
)
from ansys.fluent.core.services._protocols import ServiceProtocol
from ansys.fluent.core.services.interceptors import (
    BatchInterceptor,
    ErrorStateInterceptor,
    GrpcErrorInterceptor,
    TracingInterceptor,
)


def get_fields_request() -> field_data_pb2.GetFieldsRequest:
    """Populates a new field request."""
    return field_data_pb2.GetFieldsRequest(
        provide_bytes_stream=_FieldDataConstants.bytes_stream,
        chunk_size=_FieldDataConstants.chunk_size,
    )


class FieldDataService(  # pyright: ignore[reportUnsafeMultipleInheritance]
    StreamingService, ServiceProtocol
):
    """FieldData service of Fluent (v1 proto API)."""

    def __init__(
        self, channel: grpc.Channel, metadata: list[tuple[str, str]], fluent_error_state
    ):
        """Initialize FieldDataService."""
        intercept_channel = grpc.intercept_channel(
            channel,
            GrpcErrorInterceptor(),
            ErrorStateInterceptor(fluent_error_state),
            TracingInterceptor(),
            BatchInterceptor(),
        )
        super().__init__(
            stub=field_data_pb2_grpc.FieldDataStub(intercept_channel), metadata=metadata
        )
        self._batched_fields_request = get_fields_request()

    def get_scalar_field_range(
        self, field: str, node_value: bool = False, surface_ids: list[int] | None = None
    ) -> list[float]:
        """Get the range (minimum and maximum values) of the field.

        Parameters
        ----------
        field: str
            Field name
        node_value: bool
        surface_ids : List[int], optional
            List of surface IDS for the surface data.

        Returns
        -------
        List[float]
        """
        if not surface_ids:
            surface_ids = []
        request = field_data_pb2.GetRangeRequest()
        request.field_name = _to_field_name_str(field)
        request.node_value = node_value
        request.surface_ids.extend(
            [field_data_pb2.SurfaceId(id=int(id)) for id in surface_ids]
        )
        response = self._stub.GetRange(request, metadata=self._metadata)
        return [response.minimum, response.maximum]

    def get_scalar_fields_info(self) -> dict[str, dict]:
        """Get fields information (field name, domain, and section).

        Returns
        -------
        Dict
        """
        request = field_data_pb2.GetFieldsInfoRequest()
        response = self._stub.GetFieldsInfo(request, metadata=self._metadata)
        return {
            field_info.solver_name: {
                "display_name": field_info.display_name,
                "section": field_info.section,
                "domain": field_info.domain,
                "quantity_name": field_info.quantity_name,
            }
            for field_info in response.field_info
        }

    def get_vector_fields_info(self) -> dict[str, dict]:
        """Get vector fields information (vector components).

        Returns
        -------
        Dict
        """
        request = field_data_pb2.GetVectorFieldsInfoRequest()
        response = self._stub.GetVectorFieldsInfo(request, metadata=self._metadata)
        return {
            vector_field_info.display_name: {
                "x-component": vector_field_info.x_component,
                "y-component": vector_field_info.y_component,
                "z-component": vector_field_info.z_component,
            }
            for vector_field_info in response.vector_field_info
        }

    def get_surfaces_info(self) -> dict[str, dict]:
        """Get surfaces information (surface name, ID, and type).

        Returns
        -------
        Dict
        """
        request = field_data_pb2.GetSurfacesInfoRequest()
        response = self._stub.GetSurfacesInfo(request, metadata=self._metadata)
        info = {
            surface_info.surface_name: {
                "surface_id": [surf.id for surf in surface_info.surface_ids],
                "zone_id": surface_info.zone_id.id,
                "zone_type": surface_info.zone_type,
                "type": surface_info.type,
            }
            for surface_info in response.surface_info
        }
        return info

    def _add_scalar_fields_request(
        self,
        field_name: str,
        surfaces: list[int | str],
        node_value: bool,
        boundary_value: bool,
    ):
        fetched_data = _FetchFieldData()
        self._batched_fields_request.scalar_field_requests.extend(
            fetched_data._scalar_data(
                field_name,
                surfaces,
                node_value,
                boundary_value,
            )
        )

    def _get_scalar_field_data(
        self,
        field_name: str,
        surface_ids: list[int],
        node_value: bool,
        boundary_value: bool,
    ):
        fields_request = get_fields_request()
        fetched_data = _FetchFieldData()
        fields_request.scalar_field_requests.extend(
            fetched_data._scalar_data(
                field_name,
                surface_ids,
                node_value,
                boundary_value,
            )
        )
        return self.get_fields(fields_request)

    def _add_surfaces_request(
        self, data_types, surfaces: list[int | str], overset_mesh: bool
    ):
        fetched_data = _FetchFieldData()
        self._batched_fields_request.surface_requests.extend(
            fetched_data._surface_data(
                data_types,
                surfaces,
                overset_mesh,
            )
        )

    def _get_surface_data(self, data_types, surface_ids: list[int], overset_mesh: bool):
        fields_request = get_fields_request()
        fetched_data = _FetchFieldData()
        fields_request.surface_requests.extend(
            fetched_data._surface_data(
                data_types,
                surface_ids,
                overset_mesh,
            )
        )
        return self.get_fields(fields_request)

    def _add_vector_fields_request(self, field_name: str, surfaces: list[int | str]):
        fetched_data = _FetchFieldData()
        self._batched_fields_request.vector_field_requests.extend(
            fetched_data._vector_data(
                field_name,
                surfaces,
            )
        )

    def _get_vector_field_data(self, field_name: str, surface_ids: list[int]):
        fields_request = get_fields_request()
        fetched_data = _FetchFieldData()
        fields_request.vector_field_requests.extend(
            fetched_data._vector_data(
                field_name,
                surface_ids,
            )
        )
        return self.get_fields(fields_request)

    def _add_pathlines_fields_request(
        self,
        field_name: str,
        surfaces: list[int | str],
        additional_field_name: str = "",
        provide_particle_time_field: bool | None = False,
        node_value: bool | None = True,
        steps: int | None = 500,
        step_size: float | None = 500,
        skip: int | None = 0,
        reverse: bool | None = False,
        accuracy_control_on: bool | None = False,
        tolerance: float | None = 0.001,
        coarsen: int | None = 1,
        velocity_domain: str | None = "all-phases",
        zones: list | None = None,
    ) -> None:
        zones = zones or []
        fetched_data = _FetchFieldData()
        self._batched_fields_request.pathlines_field_requests.extend(
            fetched_data._pathlines_data(
                field_name=field_name,
                surface_ids=surfaces,
                additional_field=additional_field_name,
                provide_particle_time_field=provide_particle_time_field,
                data_location=(
                    field_data_pb2.DataLocation.DATA_LOCATION_NODES
                    if node_value
                    else field_data_pb2.DataLocation.DATA_LOCATION_ELEMENTS
                ),
                steps=steps,
                step_size=step_size,
                skip=skip,
                reverse=reverse,
                accuracy_control_enabled=accuracy_control_on,
                tolerance=tolerance,
                coarsen=coarsen,
                velocity_domain=velocity_domain,
                zones=zones,
            )
        )

    def _get_pathlines_field_data(
        self,
        field_name: str,
        surfaces: list[int | str],
        additional_field_name: str = "",
        provide_particle_time_field: bool | None = False,
        node_value: bool | None = True,
        steps: int | None = 500,
        step_size: float | None = 500,
        skip: int | None = 0,
        reverse: bool | None = False,
        accuracy_control_on: bool | None = False,
        tolerance: float | None = 0.001,
        coarsen: int | None = 1,
        velocity_domain: str | None = "all-phases",
        zones: list | None = None,
    ):
        fields_request = get_fields_request()
        fetched_data = _FetchFieldData()
        fields_request.pathlines_field_requests.extend(
            fetched_data._pathlines_data(
                field_name=field_name,
                surface_ids=surfaces,
                additional_field=additional_field_name,
                provide_particle_time_field=provide_particle_time_field,
                data_location=(
                    field_data_pb2.DataLocation.DATA_LOCATION_NODES
                    if node_value
                    else field_data_pb2.DataLocation.DATA_LOCATION_ELEMENTS
                ),
                steps=steps,
                step_size=step_size,
                skip=skip,
                reverse=reverse,
                accuracy_control_enabled=accuracy_control_on,
                tolerance=tolerance,
                coarsen=coarsen,
                velocity_domain=velocity_domain,
                zones=zones,
            )
        )
        return self.get_fields(fields_request)

    def get_fields(self, request):
        """GetFields RPC of FieldData service.

        Raises
        ------
        RuntimeError
            If an empty chunk encountered during field extraction.
        """
        chunk_iterator = self._stub.GetFields(request, metadata=self._metadata)
        if not chunk_iterator.is_active():
            raise RuntimeError(
                "Unexpectedly encountered empty chunk during field extraction."
            )
        return chunk_iterator

    def is_data_available(
        self, request: field_data_pb2.IsDataAvailableRequest
    ) -> field_data_pb2.IsDataAvailableResponse:
        """IsDataAvailable RPC of FieldData service (v1)."""
        return self._stub.IsDataAvailable(request, metadata=self._metadata)

    def is_solution_data_available(self) -> bool:
        """Return whether solution data is currently available."""
        request = field_data_pb2.IsDataAvailableRequest()
        response = self.is_data_available(request)
        return response.is_data_available

    def get_solver_mesh_nodes_float(
        self, domain_id: int, thread_id: int
    ) -> list[float]:
        """Get mesh node -> floating point precision."""
        request = field_data_pb2.GetSolverMeshNodesRequest(
            domain_id=domain_id, thread_id=thread_id
        )
        responses = self._stub.GetSolverMeshNodesFloat(request, metadata=self._metadata)
        nested_nodes = []
        for response in responses:
            nested_nodes.append(response.nodes)
        return nested_nodes

    def get_solver_mesh_nodes_double(
        self, domain_id: int, thread_id: int
    ) -> list[float]:
        """Get mesh node -> double precision."""
        request = field_data_pb2.GetSolverMeshNodesRequest(
            domain_id=domain_id, thread_id=thread_id
        )
        responses = self._stub.GetSolverMeshNodesDouble(
            request, metadata=self._metadata
        )
        nested_nodes = []
        for response in responses:
            nested_nodes.append(response.nodes)
        return nested_nodes

    def get_solver_mesh_elements(self, domain_id: int, thread_id: int) -> list[float]:
        """Get mesh elements."""
        request = field_data_pb2.GetSolverMeshElementsRequest(
            domain_id=domain_id, thread_id=thread_id
        )
        responses = self._stub.GetSolverMeshElements(request, metadata=self._metadata)
        elementss = []
        for response in responses:
            elementss.append(response.elements)
        return elementss


class _FetchFieldData:

    @staticmethod
    def _surface_data(
        data_types: list[SurfaceDataType] | list[str],
        surface_ids: list[int],
        overset_mesh: bool | None = False,
    ):
        """Build surface-data requests."""
        return [
            field_data_pb2.SurfaceRequest(
                surface_id=surface_id,
                overset_mesh=overset_mesh,
                provide_faces=SurfaceDataType.FacesConnectivity in data_types,
                provide_vertices=SurfaceDataType.Vertices in data_types,
                provide_faces_centroid=SurfaceDataType.FacesCentroid in data_types,
                provide_faces_normal=SurfaceDataType.FacesNormal in data_types,
            )
            for surface_id in surface_ids
        ]

    @staticmethod
    def _scalar_data(
        field_name: str,
        surface_ids: list[int],
        node_value: bool,
        boundary_value: bool,
    ):
        """Build scalar-field requests."""
        return [
            field_data_pb2.ScalarFieldRequest(
                surface_id=surface_id,
                scalar_field_name=field_name,
                data_location=(
                    field_data_pb2.DataLocation.DATA_LOCATION_NODES
                    if node_value
                    else field_data_pb2.DataLocation.DATA_LOCATION_ELEMENTS
                ),
                provide_boundary_values=boundary_value,
            )
            for surface_id in surface_ids
        ]

    @staticmethod
    def _vector_data(
        field_name: str,
        surface_ids: list[int],
    ):
        """Build vector-field requests."""
        return [
            field_data_pb2.VectorFieldRequest(
                surface_id=surface_id, vector_field_name=field_name
            )
            for surface_id in surface_ids
        ]

    @staticmethod
    def _pathlines_data(
        field_name: str,
        surface_ids: list[int],
        **kwargs,
    ):
        """Build pathlines-field requests."""
        return [
            field_data_pb2.PathlinesFieldRequest(
                surface_id=surface_id,
                field=field_name,
                **kwargs,
            )
            for surface_id in surface_ids
        ]


class _FieldDataConstants:
    """Defines constants for Fluent field data."""

    proto_field_type_to_np_data_type = {
        field_data_pb2.FieldType.FIELD_TYPE_INT_ARRAY: np.int32,
        field_data_pb2.FieldType.FIELD_TYPE_LONG_ARRAY: np.int64,
        field_data_pb2.FieldType.FIELD_TYPE_FLOAT_ARRAY: np.float32,
        field_data_pb2.FieldType.FIELD_TYPE_DOUBLE_ARRAY: np.float64,
    }
    np_data_type_to_proto_field_type = {
        np.int32: field_data_pb2.FieldType.FIELD_TYPE_INT_ARRAY,
        np.int64: field_data_pb2.FieldType.FIELD_TYPE_LONG_ARRAY,
        np.float32: field_data_pb2.FieldType.FIELD_TYPE_FLOAT_ARRAY,
        np.float64: field_data_pb2.FieldType.FIELD_TYPE_DOUBLE_ARRAY,
    }
    chunk_size = 256 * 1024
    bytes_stream = True
    payloadTags = {
        field_data_pb2.PayloadTag.PAYLOAD_TAG_OVERSET_MESH: 1,
        field_data_pb2.PayloadTag.PAYLOAD_TAG_ELEMENT_LOCATION: 2,
        field_data_pb2.PayloadTag.PAYLOAD_TAG_NODE_LOCATION: 4,
        field_data_pb2.PayloadTag.PAYLOAD_TAG_BOUNDARY_VALUES: 8,
    }
