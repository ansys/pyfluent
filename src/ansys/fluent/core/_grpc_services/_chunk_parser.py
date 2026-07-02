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

"""Parses field data stream received from Fluent"""

from collections.abc import Sequence
from functools import reduce
from typing import Any
import warnings

import numpy as np
import numpy.typing as npt

from ansys.fluent.core._grpc_services.field_data_service import _FieldDataConstants
from ansys.fluent.core._grpc_services.field_data_service_v0 import (
    _FieldDataConstants as _FieldDataConstantsV0,
)


class ChunkParserV0:
    """Class for parsing field data stream received from Fluent.

    Parameters
    ----------
    callbacks_provider : object
    The object which can register and unregister callbacks.
    It provides callbacks, which are triggered with following arguments:
        zone_id : int

        field_name : str

        field : numpy array
    """

    def __init__(self, callbacks_provider: object = None):
        """__init__ method of ChunkParserV0 class."""
        self._callbacks_provider = callbacks_provider

    def extract_fields(self, chunk_iterator) -> dict[Any, dict[str, npt.NDArray[Any]]]:
        """Extracts field data received from Fluent.

        if callbacks_provider is set then callbacks are triggered with extracted data.
        """

        def _get_tag_for_surface_request() -> tuple[tuple[str, str]]:
            return (("type", "surface-data"),)

        def _get_tag_for_vector_field_request() -> tuple[tuple[str, str]]:
            return (("type", "vector-field"),)

        def _get_tag_for_scalar_field_request(
            scalar_field_request,
        ) -> tuple[tuple[str, str], tuple[str, Any], tuple[str, Any]]:
            return (
                ("type", "scalar-field"),
                ("dataLocation", scalar_field_request.dataLocation),
                ("boundaryValues", scalar_field_request.provideBoundaryValues),
            )

        def _get_tag_for_pathlines_field_request(
            pathlines_field_request,
        ) -> tuple[tuple[str, str], tuple[str, Any]]:
            return (
                ("type", "pathlines-field"),
                ("field", pathlines_field_request.field),
            )

        def _extract_field(
            field_datatype: npt.DTypeLike, field_size: int, chunk_iterator
        ) -> npt.NDArray[Any] | None:
            field_arr = np.empty(field_size, dtype=field_datatype)
            field_datatype_item_size = np.dtype(field_datatype).itemsize
            index = 0
            for chunk in chunk_iterator:
                if chunk.bytePayload:
                    count = min(
                        len(chunk.bytePayload) // field_datatype_item_size,
                        field_size - index,
                    )
                    field_arr[index : index + count] = np.frombuffer(
                        chunk.bytePayload, field_datatype, count=count
                    )
                    index += count
                    if index == field_size:
                        return field_arr
                else:
                    payload: Sequence[float] = (
                        chunk.floatPayload.payload
                        or chunk.intPayload.payload
                        or chunk.doublePayload.payload
                        or chunk.longPayload.payload
                    )
                    count = len(payload)
                    field_arr[index : index + count] = np.fromiter(
                        payload, dtype=field_datatype
                    )
                    index += count
                    if index == field_size:
                        return field_arr

        fields_data = dict[Any, dict[str, npt.NDArray[Any]]]()
        for chunk in chunk_iterator:
            payload_info = chunk.payloadInfo
            surface_id = payload_info.surfaceId
            field_request_info = payload_info.fieldRequestInfo
            request_type = field_request_info.WhichOneof("request")
            if request_type is not None:
                payload_tag_id = (
                    _get_tag_for_surface_request()
                    if request_type == "surfaceRequest"
                    else (
                        _get_tag_for_scalar_field_request(
                            field_request_info.scalarFieldRequest
                        )
                        if request_type == "scalarFieldRequest"
                        else (
                            _get_tag_for_vector_field_request()
                            if request_type == "vectorFieldRequest"
                            else (
                                _get_tag_for_pathlines_field_request(
                                    field_request_info.pathlinesFieldRequest
                                )
                                if request_type == "pathlinesFieldRequest"
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
                            _FieldDataConstantsV0.payloadTags[tag]
                            for tag in payload_info.payloadTag
                        ]
                        or [0],
                    )
                else:
                    payload_tag_id = None
            field: npt.NDArray[Any] | None = None
            if payload_tag_id is not None:
                if payload_info.fieldSize > 0:
                    field = _extract_field(
                        _FieldDataConstantsV0.proto_field_type_to_np_data_type[
                            payload_info.fieldType
                        ],
                        payload_info.fieldSize,
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
                    # print('cb', surface_id, payload_info.fieldName)
                    callback(surface_id, payload_info.fieldName, field, *args, **kwargs)
            else:
                payload_data = fields_data.get(payload_tag_id)
                if not payload_data:
                    payload_data = fields_data[payload_tag_id] = {}
                surface_data = payload_data.get(surface_id)
                if surface_data:
                    if payload_info.fieldName in surface_data:
                        surface_data[payload_info.fieldName] = np.concatenate(
                            (surface_data[payload_info.fieldName], field)
                        )
                    else:
                        surface_data[payload_info.fieldName] = field
                else:
                    payload_data[surface_id] = {payload_info.fieldName: field}
        return fields_data


class ChunkParser(ChunkParserV0):
    """Class for parsing field data stream received from Fluent."""

    def extract_fields(self, chunk_iterator) -> dict[Any, dict[str, npt.NDArray[Any]]]:
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
