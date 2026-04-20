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

"""Wrappers over FieldData gRPC service of Fluent (v1 proto API).

All shared logic lives in field_data.py (v0). This module keeps only
v1-specific proto construction/parsing.
"""

from collections.abc import Iterable
from functools import reduce
from typing import Dict, List
import warnings

import numpy as np

from ansys.api.fluent.v1 import field_data_pb2 as FieldDataProtoModule
from ansys.api.fluent.v1 import field_data_pb2_grpc as FieldGrpcModule
from ansys.fluent.core.pyfluent_warnings import PyFluentDeprecationWarning
from ansys.fluent.core.services import field_data as _v0

FieldDataSource = _v0.FieldDataSource
SurfaceDataType = _v0.SurfaceDataType
_to_field_name_str = _v0._to_field_name_str
_AllowedSurfaceIDs = _v0._AllowedSurfaceIDs
get_surfaces_from_objects = _v0.get_surfaces_from_objects
PathlinesFieldDataRequest = _v0.PathlinesFieldDataRequest
ScalarFieldDataRequest = _v0.ScalarFieldDataRequest
SurfaceFieldDataRequest = _v0.SurfaceFieldDataRequest
VectorFieldDataRequest = _v0.VectorFieldDataRequest
DisallowedValuesError = _v0.DisallowedValuesError


class FieldDataService(_v0.FieldDataService):
    """FieldData service of Fluent (v1 proto API)."""

    def _create_stub(self, intercept_channel):
        """Create the v1 gRPC stub."""
        return FieldGrpcModule.FieldDataStub(intercept_channel)


class _FieldInfo(_v0._FieldInfo):
    """Provides internal access to Fluent field information."""

    def _get_scalar_field_range(
        self, field: str, node_value: bool = False, surface_ids: List[int] = None
    ) -> List[float]:
        """Get the range (minimum and maximum values) of the field."""
        if not surface_ids:
            surface_ids = []
        request = FieldDataProtoModule.GetRangeRequest()
        request.field_name = _to_field_name_str(field)
        request.node_value = node_value
        request.surface_ids.extend(
            [FieldDataProtoModule.SurfaceId(id=int(id)) for id in surface_ids]
        )
        response = self._service.get_scalar_field_range(request)
        return [response.minimum, response.maximum]

    def _get_scalar_fields_info(self) -> Dict[str, Dict]:
        """Get fields information (field name, domain, and section)."""
        request = FieldDataProtoModule.GetFieldsInfoRequest()
        response = self._service.get_scalar_fields_info(request)
        return {
            field_info.solver_name: {
                "display_name": field_info.display_name,
                "section": field_info.section,
                "domain": field_info.domain,
                "quantity_name": field_info.quantity_name,
            }
            for field_info in response.field_info
        }

    def _get_vector_fields_info(self) -> Dict[str, Dict]:
        """Get vector fields information (vector components)."""
        request = FieldDataProtoModule.GetVectorFieldsInfoRequest()
        response = self._service.get_vector_fields_info(request)
        return {
            vector_field_info.display_name: {
                "x-component": vector_field_info.x_component,
                "y-component": vector_field_info.y_component,
                "z-component": vector_field_info.z_component,
            }
            for vector_field_info in response.vector_field_info
        }

    def _get_surfaces_info(self) -> Dict[str, Dict]:
        """Get surfaces information (surface name, ID, and type)."""
        request = FieldDataProtoModule.GetSurfacesInfoResponse()
        response = self._service.get_surfaces_info(request)
        return {
            surface_info.surface_name: {
                "surface_id": [surf.id for surf in surface_info.surface_ids],
                "zone_id": surface_info.zone_id.id,
                "zone_type": surface_info.zone_type,
                "type": surface_info.type,
            }
            for surface_info in response.surface_info
        }


class FieldInfo(_FieldInfo):
    """Provides access to Fluent field information."""

    def __init__(self, service: FieldDataService, is_data_valid):
        """__init__ method of FieldInfo class."""
        warnings.warn(
            "'FieldInfo' is deprecated and will be removed in a future release. "
            "Please use relevant methods from 'FieldData' instead",
            PyFluentDeprecationWarning,
        )
        super().__init__(service, is_data_valid)


class _FetchFieldData:
    """Helper for building field-data request payloads."""

    @staticmethod
    def _surface_data(
        data_types: List[SurfaceDataType] | List[str],
        surface_ids: List[int],
        overset_mesh: bool | None = False,
    ):
        """Build surface-data requests."""
        return [
            FieldDataProtoModule.SurfaceRequest(
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
        surface_ids: List[int],
        node_value: bool,
        boundary_value: bool,
    ):
        """Build scalar-field requests."""
        return [
            FieldDataProtoModule.ScalarFieldRequest(
                surface_id=surface_id,
                scalar_field_name=field_name,
                data_location=(
                    FieldDataProtoModule.DataLocation.DATA_LOCATION_NODES
                    if node_value
                    else FieldDataProtoModule.DataLocation.DATA_LOCATION_ELEMENTS
                ),
                provide_boundary_values=boundary_value,
            )
            for surface_id in surface_ids
        ]

    @staticmethod
    def _vector_data(
        field_name: str,
        surface_ids: List[int],
    ):
        """Build vector-field requests."""
        return [
            FieldDataProtoModule.VectorFieldRequest(
                surface_id=surface_id, vector_field_name=field_name
            )
            for surface_id in surface_ids
        ]

    @staticmethod
    def _pathlines_data(
        field_name: str,
        surface_ids: List[int],
        **kwargs,
    ):
        """Build pathlines-field requests."""
        return [
            FieldDataProtoModule.PathlinesFieldRequest(
                surface_id=surface_id,
                field=field_name,
                **kwargs,
            )
            for surface_id in surface_ids
        ]


class BaseFieldData(_v0.BaseFieldData):
    """The base field data interface."""

    def _get_scalar_field_data(
        self,
        **kwargs,
    ) -> Dict[int | str, np.array]:
        """Get scalar field data on surfaces from cached batch data."""
        data_location = (
            FieldDataProtoModule.DataLocation.DATA_LOCATION_NODES
            if kwargs.get("node_value")
            else FieldDataProtoModule.DataLocation.DATA_LOCATION_ELEMENTS
        )
        scalar_field_data = self.data[
            (
                ("type", "scalar-field"),
                ("dataLocation", data_location),
                ("boundaryValues", kwargs.get("boundary_value")),
            )
        ]
        return self._returned_data._scalar_data(
            _to_field_name_str(kwargs.get("field_name")),
            kwargs.get("surfaces"),
            self.get_surface_ids(kwargs.get("surfaces")),
            scalar_field_data,
        )


class BatchFieldData(BaseFieldData, _v0.BatchFieldData):
    """Provides access to Fluent field data on surfaces collected via batches."""

    pass


class TransactionFieldData(BatchFieldData):
    """TransactionFieldData class - deprecated."""

    def __init__(self, *args, **kwargs):
        """__init__ method of TransactionFieldData class."""
        warnings.warn(
            "'TransactionFieldData' is deprecated, use 'BatchFieldData' instead.",
            PyFluentDeprecationWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)


class Batch(_v0.Batch):
    """Populates Fluent field data on surfaces."""

    def __init__(
        self,
        service: FieldDataService,
        field_info: _FieldInfo,
        allowed_surface_ids,
        allowed_surface_names,
        allowed_scalar_field_names,
        allowed_vector_field_names,
    ):
        """__init__ method of Batch class."""
        super().__init__(
            service,
            field_info,
            allowed_surface_ids,
            allowed_surface_names,
            allowed_scalar_field_names,
            allowed_vector_field_names,
        )
        self._fields_request = get_fields_request()
        self._fetched_data = _FetchFieldData()

    def _add_surfaces_request(self, **kwargs) -> None:
        """Add an internal request to fetch surface data."""
        updated_data_types = []
        for d_type in kwargs.get("data_types"):
            if isinstance(d_type, str):
                updated_data_types.append(SurfaceDataType(d_type))
            else:
                updated_data_types.append(d_type)
        data_types = updated_data_types
        self._fields_request.surface_requests.extend(
            self._fetched_data._surface_data(
                data_types,
                kwargs.get("surfaces"),
                kwargs.get("overset_mesh"),
            )
        )

    def _add_scalar_fields_request(self, **kwargs) -> None:
        """Add an internal request to fetch scalar field data."""
        self._fields_request.scalar_field_requests.extend(
            self._fetched_data._scalar_data(
                self._allowed_scalar_field_names.valid_name(kwargs.get("field_name")),
                kwargs.get("surfaces"),
                kwargs.get("node_value"),
                kwargs.get("boundary_value"),
            )
        )

    def _add_vector_fields_request(self, **kwargs) -> None:
        """Add an internal request to fetch vector field data."""
        self._fields_request.vector_field_requests.extend(
            self._fetched_data._vector_data(
                self._allowed_vector_field_names.valid_name(kwargs.get("field_name")),
                kwargs.get("surfaces"),
            )
        )

    def _add_pathlines_fields_request(
        self,
        **kwargs,
    ) -> None:
        """Add an internal request to fetch path-lines field data."""
        zones = kwargs.get("zones", [])
        field_name = self._allowed_scalar_field_names.valid_name(
            kwargs.get("field_name")
        )
        if field_name in self._pathline_field_data:
            raise ValueError("For 'path-lines' `field_name` should be unique.")
        else:
            self._pathline_field_data.append(field_name)
        additional_field_name = kwargs.get("additional_field_name")
        if additional_field_name:
            additional_field_name = self._allowed_scalar_field_names.valid_name(
                additional_field_name
            )
        self._fields_request.pathlines_field_requests.extend(
            self._fetched_data._pathlines_data(
                field_name,
                kwargs.get("surfaces"),
                additional_field=additional_field_name,
                provide_particle_time_field=kwargs.get("provide_particle_time_field"),
                data_location=(
                    FieldDataProtoModule.DataLocation.DATA_LOCATION_NODES
                    if kwargs.get("node_value")
                    else FieldDataProtoModule.DataLocation.DATA_LOCATION_ELEMENTS
                ),
                steps=kwargs.get("steps"),
                step_size=kwargs.get("step_size"),
                skip=kwargs.get("skip"),
                reverse=kwargs.get("reverse"),
                accuracy_control_enabled=kwargs.get("accuracy_control_on"),
                tolerance=kwargs.get("tolerance"),
                coarsen=kwargs.get("coarsen"),
                velocity_domain=kwargs.get("velocity_domain"),
                zones=zones,
            )
        )

    def get_response(self) -> BatchFieldData:
        """Get data for previously added requests."""
        return BatchFieldData(
            ChunkParser().extract_fields(
                self._service.get_fields(self._fields_request)
            ),
            self._field_info,
            self._allowed_surface_names,
            self._allowed_scalar_field_names,
        )


class Transaction(Batch):
    """Transaction class - deprecated."""

    def __init__(self, *args, **kwargs):
        """__init__ method of Transaction class."""
        warnings.warn(
            "'Transaction' is deprecated, use 'Batch' instead.",
            PyFluentDeprecationWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)


class _FieldDataConstants:
    """Defines constants for Fluent field data."""

    proto_field_type_to_np_data_type = {
        FieldDataProtoModule.FieldType.FIELD_TYPE_INT_ARRAY: np.int32,
        FieldDataProtoModule.FieldType.FIELD_TYPE_LONG_ARRAY: np.int64,
        FieldDataProtoModule.FieldType.FIELD_TYPE_FLOAT_ARRAY: np.float32,
        FieldDataProtoModule.FieldType.FIELD_TYPE_DOUBLE_ARRAY: np.float64,
    }
    np_data_type_to_proto_field_type = {
        np.int32: FieldDataProtoModule.FieldType.FIELD_TYPE_INT_ARRAY,
        np.int64: FieldDataProtoModule.FieldType.FIELD_TYPE_LONG_ARRAY,
        np.float32: FieldDataProtoModule.FieldType.FIELD_TYPE_FLOAT_ARRAY,
        np.float64: FieldDataProtoModule.FieldType.FIELD_TYPE_DOUBLE_ARRAY,
    }
    chunk_size = 256 * 1024
    bytes_stream = True
    payloadTags = {
        FieldDataProtoModule.PayloadTag.PAYLOAD_TAG_OVERSET_MESH: 1,
        FieldDataProtoModule.PayloadTag.PAYLOAD_TAG_ELEMENT_LOCATION: 2,
        FieldDataProtoModule.PayloadTag.PAYLOAD_TAG_NODE_LOCATION: 4,
        FieldDataProtoModule.PayloadTag.PAYLOAD_TAG_BOUNDARY_VALUES: 8,
    }


def _get_surface_ids(
    field_info: _FieldInfo,
    allowed_surface_names,
    surfaces: List[int | str | object],
) -> List[int]:
    """Get surface IDs based on surface names or IDs."""
    surface_ids = []
    updated_surfaces = get_surfaces_from_objects(surfaces)
    for surf in updated_surfaces:
        if isinstance(surf, str):
            surface_ids.extend(
                field_info._get_surfaces_info()[allowed_surface_names.valid_name(surf)][
                    "surface_id"
                ]
            )
        else:
            allowed_surf_ids = _AllowedSurfaceIDs(field_info)()
            if surf in allowed_surf_ids:
                surface_ids.append(surf)
            elif isinstance(surf, Iterable) and not isinstance(surf, (str, bytes)):
                raise DisallowedValuesError("surface", surf, list(surf))
            else:
                raise DisallowedValuesError("surface", surf, allowed_surf_ids)
    return surface_ids


def get_fields_request():
    """Populates a new field request."""
    return FieldDataProtoModule.GetFieldsRequest(
        provide_bytes_stream=_FieldDataConstants.bytes_stream,
        chunk_size=_FieldDataConstants.chunk_size,
    )


class ChunkParser(_v0.ChunkParser):
    """Class for parsing field data stream received from Fluent."""

    def extract_fields(self, chunk_iterator) -> Dict[int, Dict[str, np.array]]:
        """Extracts field data received from Fluent."""

        def _get_tag_for_surface_request():
            return (("type", "surface-data"),)

        def _get_tag_for_vector_field_request():
            return (("type", "vector-field"),)

        def _get_tag_for_scalar_field_request(scalar_field_request):
            return (
                ("type", "scalar-field"),
                ("dataLocation", scalar_field_request.data_location),
                ("boundaryValues", scalar_field_request.provide_boundary_values),
            )

        def _get_tag_for_pathlines_field_request(pathlines_field_request):
            return (
                ("type", "pathlines-field"),
                ("field", pathlines_field_request.field),
            )

        def _extract_field(field_datatype, field_size, chunk_iterator):
            field_arr = np.empty(field_size, dtype=field_datatype)
            field_datatype_item_size = np.dtype(field_datatype).itemsize
            index = 0
            for chunk in chunk_iterator:
                if chunk.byte_payload:
                    count = min(
                        len(chunk.byte_payload) // field_datatype_item_size,
                        field_size - index,
                    )
                    field_arr[index : index + count] = np.frombuffer(
                        chunk.byte_payload, field_datatype, count=count
                    )
                    index += count
                    if index == field_size:
                        return field_arr
                else:
                    payload = (
                        chunk.float_payload.payload
                        or chunk.int_payload.payload
                        or chunk.double_payload.payload
                        or chunk.long_payload.payload
                    )
                    count = len(payload)
                    field_arr[index : index + count] = np.fromiter(
                        payload, dtype=field_datatype
                    )
                    index += count
                    if index == field_size:
                        return field_arr

        fields_data = {}
        for chunk in chunk_iterator:
            payload_info = chunk.payload_info
            surface_id = payload_info.surface_id
            field_request_info = payload_info.field_request_info
            request_type = field_request_info.WhichOneof("request")
            if request_type is not None:
                payload_tag_id = (
                    _get_tag_for_surface_request()
                    if request_type == "surface_request"
                    else (
                        _get_tag_for_scalar_field_request(
                            field_request_info.scalar_field_request
                        )
                        if request_type == "scalar_field_request"
                        else (
                            _get_tag_for_vector_field_request()
                            if request_type == "vector_field_request"
                            else (
                                _get_tag_for_pathlines_field_request(
                                    field_request_info.pathlines_field_request
                                )
                                if request_type == "pathlines_field_request"
                                else None
                            )
                        )
                    )
                )
            else:
                if self._callbacks_provider is None:
                    payload_tag_id = reduce(
                        lambda x, y: x | y,
                        [
                            _FieldDataConstants.payloadTags[tag]
                            for tag in payload_info.payload_tags
                        ]
                        or [0],
                    )
                else:
                    payload_tag_id = None
            field = None
            if payload_tag_id is not None:
                if payload_info.field_size > 0:
                    field = _extract_field(
                        _FieldDataConstants.proto_field_type_to_np_data_type[
                            payload_info.field_type
                        ],
                        payload_info.field_size,
                        chunk_iterator,
                    )
                else:
                    warnings.warn(
                        f"Field data is not available for surface: {surface_id}"
                    )
                    field = np.array([])

            if self._callbacks_provider is not None:
                for callback_data in self._callbacks_provider.callbacks():
                    callback, args, kwargs = callback_data
                    callback(
                        surface_id, payload_info.field_name, field, *args, **kwargs
                    )
            else:
                payload_data = fields_data.get(payload_tag_id)
                if not payload_data:
                    payload_data = fields_data[payload_tag_id] = {}
                surface_data = payload_data.get(surface_id)
                if surface_data:
                    if payload_info.field_name in surface_data:
                        surface_data.update(
                            {
                                payload_info.field_name: np.concatenate(
                                    (surface_data[payload_info.field_name], field)
                                )
                            }
                        )
                    else:
                        surface_data.update({payload_info.field_name: field})
                else:
                    payload_data[surface_id] = {payload_info.field_name: field}
        return fields_data


class LiveFieldData(_v0.LiveFieldData):
    """Provides access to Fluent field data on surfaces."""

    def __init__(
        self,
        service: FieldDataService,
        field_info: _FieldInfo,
        is_data_valid,
        scheme_eval=None,
        get_zones_info=None,
    ):
        """__init__ method of FieldData class."""
        super().__init__(
            service,
            field_info,
            is_data_valid,
            scheme_eval=scheme_eval,
            get_zones_info=get_zones_info,
        )
        self._fetched_data = _FetchFieldData()

    def new_batch(self):
        """Create a new field batch."""
        return Batch(
            self._service,
            self._field_info,
            self._allowed_surface_ids,
            self._allowed_surface_names,
            self._allowed_scalar_field_names,
            self._allowed_vector_field_names,
        )

    def _get_scalar_field_data(self, **kwargs):
        """Get scalar field data on a surface."""
        surfaces = kwargs.get("surfaces")
        surface_ids = self.get_surface_ids(surfaces)
        fields_request = get_fields_request()
        field_name = self._allowed_scalar_field_names.valid_name(
            kwargs.get("field_name")
        )
        fields_request.scalar_field_requests.extend(
            self._fetched_data._scalar_data(
                field_name,
                self.get_surface_ids(surfaces),
                kwargs.get("node_value"),
                kwargs.get("boundary_value"),
            )
        )
        fields = ChunkParser().extract_fields(self._service.get_fields(fields_request))
        scalar_field_data = next(iter(fields.values()))
        return self._returned_data._scalar_data(
            field_name, surfaces, surface_ids, scalar_field_data
        )

    def _get_surface_data(
        self,
        **kwargs,
    ) -> Dict[int | str, Dict[SurfaceDataType, np.array | List[np.array]]]:
        """Get surface data (vertices, faces connectivity, centroids, and normals)."""
        surface_ids = self.get_surface_ids(kwargs.get("surfaces"))
        fields_request = get_fields_request()
        fields_request.surface_requests.extend(
            self._fetched_data._surface_data(
                kwargs.get("data_types"),
                surface_ids,
                kwargs.get("overset_mesh"),
            )
        )
        fields = ChunkParser().extract_fields(self._service.get_fields(fields_request))
        surface_data = next(iter(fields.values()))
        if self._deprecated_flag:
            self._deprecated_flag = False
            return self._returned_data._surface_data(
                kwargs.get("data_types"),
                kwargs.get("surfaces"),
                surface_ids,
                surface_data,
                deprecated_flag=True,
                flatten_connectivity=kwargs.get("flatten_connectivity"),
            )

        return self._returned_data._surface_data(
            kwargs.get("data_types"),
            kwargs.get("surfaces"),
            surface_ids,
            surface_data,
            flatten_connectivity=kwargs.get("flatten_connectivity"),
        )

    def _get_vector_field_data(
        self,
        **kwargs,
    ) -> Dict[int | str, np.array]:
        """Get vector field data on a surface."""
        surface_ids = self.get_surface_ids(kwargs.get("surfaces"))
        field_name = self._allowed_vector_field_names.valid_name(
            kwargs.get("field_name")
        )
        for surface_id in surface_ids:
            self.scheme.string_eval(f"(surface? {surface_id})")
        fields_request = get_fields_request()
        fields_request.vector_field_requests.extend(
            self._fetched_data._vector_data(
                field_name,
                surface_ids,
            )
        )
        fields = ChunkParser().extract_fields(self._service.get_fields(fields_request))
        vector_field_data = next(iter(fields.values()))

        return self._returned_data._vector_data(
            field_name,
            kwargs.get("surfaces"),
            surface_ids,
            vector_field_data,
        )

    def _get_pathlines_field_data(
        self,
        **kwargs,
    ) -> Dict:
        """Get the pathlines field data on a surface."""
        zones = kwargs.get("zones", [])
        surface_ids = self.get_surface_ids(kwargs.get("surfaces"))
        field_name = self._allowed_scalar_field_names.valid_name(
            kwargs.get("field_name")
        )
        fields_request = get_fields_request()
        additional_field_name = kwargs.get("additional_field_name")
        if additional_field_name:
            additional_field_name = self._allowed_scalar_field_names.valid_name(
                additional_field_name
            )
        fields_request.pathlines_field_requests.extend(
            self._fetched_data._pathlines_data(
                field_name,
                surface_ids,
                additional_field=additional_field_name,
                provide_particle_time_field=kwargs.get("provide_particle_time_field"),
                data_location=(
                    FieldDataProtoModule.DataLocation.DATA_LOCATION_NODES
                    if kwargs.get("node_value")
                    else FieldDataProtoModule.DataLocation.DATA_LOCATION_ELEMENTS
                ),
                steps=kwargs.get("steps"),
                step_size=kwargs.get("step_size"),
                skip=kwargs.get("skip"),
                reverse=kwargs.get("reverse"),
                accuracy_control_enabled=kwargs.get("accuracy_control_on"),
                tolerance=kwargs.get("tolerance"),
                coarsen=kwargs.get("coarsen"),
                velocity_domain=kwargs.get("velocity_domain"),
                zones=zones,
            )
        )
        fields = ChunkParser().extract_fields(self._service.get_fields(fields_request))
        pathlines_data = next(iter(fields.values()))

        if self._deprecated_flag:
            self._deprecated_flag = False
            return self._returned_data._pathlines_data(
                field_name,
                kwargs.get("surfaces"),
                surface_ids,
                pathlines_data,
                deprecated_flag=True,
                flatten_connectivity=kwargs.get("flatten_connectivity"),
            )

        return self._returned_data._pathlines_data(
            field_name,
            kwargs.get("surfaces"),
            surface_ids,
            pathlines_data,
            flatten_connectivity=kwargs.get("flatten_connectivity"),
        )
