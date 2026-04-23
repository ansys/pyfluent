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

"""Wrappers over SVAR gRPC service of Fluent (v1 proto API).

All shared logic lives in solution_variables.py (v0). This module keeps only
v1-specific proto construction/parsing required for compatibility.
"""

import math
from typing import Dict, List

import numpy as np

from ansys.api.fluent.v1 import field_data_pb2 as FieldDataProtoModule
from ansys.api.fluent.v1 import svar_pb2 as SvarProtoModule
from ansys.api.fluent.v1 import svar_pb2_grpc as SvarGrpcModule
from ansys.fluent.core.services import solution_variables as _v0
from ansys.fluent.core.services.field_data_v1 import _FieldDataConstants
from ansys.fluent.core.utils.deprecate import deprecate_arguments

override_help_text = _v0.override_help_text
PyFluentDeprecationWarning = _v0.PyFluentDeprecationWarning
allowed_name_error_message = _v0.allowed_name_error_message
_to_field_name_str = _v0._to_field_name_str

InvalidSolutionVariableNameError = _v0.InvalidSolutionVariableNameError
ZoneError = _v0.ZoneError
_AllowedNames = _v0._AllowedNames
_AllowedSvarNames = _v0._AllowedSvarNames
_AllowedZoneNames = _v0._AllowedZoneNames
_AllowedDomainNames = _v0._AllowedDomainNames
_SvarMethod = _v0._SvarMethod


class SolutionVariableService(_v0.SolutionVariableService):
    """SVAR service of Fluent (v1 proto API)."""

    def _create_stub(self, intercept_channel):
        """Create the v1 gRPC stub."""
        return SvarGrpcModule.SvarStub(intercept_channel)


class SolutionVariableInfo(_v0.SolutionVariableInfo):
    """Provide access to Fluent SVARs and Zones information (v1 proto API)."""

    class SolutionVariables(_v0.SolutionVariableInfo.SolutionVariables):
        """Class containing information for multiple solution variables."""

        class SolutionVariable(
            _v0.SolutionVariableInfo.SolutionVariables.SolutionVariable
        ):
            """Class containing information for single solution variable."""

            def __init__(self, solution_variable_info):
                """Initialize SolutionVariable."""
                self.name = solution_variable_info.name
                self.dimension = solution_variable_info.dimension
                self.field_type = _FieldDataConstants.proto_field_type_to_np_data_type[
                    solution_variable_info.field_type
                ]

        def __init__(self, solution_variables_info):
            """Initialize SolutionVariables."""
            self._solution_variables_info = {}
            for solution_variable_info in solution_variables_info:
                self._solution_variables_info[solution_variable_info.name] = (
                    self.SolutionVariable(solution_variable_info)
                )

    class ZonesInfo(_v0.SolutionVariableInfo.ZonesInfo):
        """Class containing information for multiple zones."""

        class ZoneInfo(_v0.SolutionVariableInfo.ZonesInfo.ZoneInfo):
            """Class containing information for single zone."""

            class PartitionsInfo(
                _v0.SolutionVariableInfo.ZonesInfo.ZoneInfo.PartitionsInfo
            ):
                """Class containing information for partitions."""

                def __init__(self, partition_info):
                    """Initialize PartitionsInfo."""
                    self.count = partition_info.count
                    self.start_index = (
                        partition_info.start_index if self.count > 0 else 0
                    )
                    self.end_index = partition_info.end_index if self.count > 0 else 0

            def __init__(self, zone_info):
                """Initialize ZoneInfo."""
                self.name = zone_info.name
                self.zone_id = zone_info.zone_id
                self.zone_type = zone_info.zone_type
                self.thread_type = zone_info.thread_type
                self.partitions_info = [
                    self.PartitionsInfo(partition_info)
                    for partition_info in zone_info.partitions_info
                ]

        def __init__(self, zones_info, domains_info):
            """Initialize ZonesInfo."""
            self._zones_info = {}
            self._domains_info = {}
            for zone_info in zones_info:
                self._zones_info[zone_info.name] = self.ZoneInfo(zone_info)
            for domain_info in domains_info:
                self._domains_info[domain_info.name] = domain_info.domain_id

    def get_variables_info(
        self, zone_names: List[str], domain_name: str | None = "mixture"
    ) -> SolutionVariables:
        """Get SVARs info for zones in the domain."""
        allowed_zone_names = _AllowedZoneNames(self)
        allowed_domain_names = _AllowedDomainNames(self)
        solution_variables_info = None
        for zone_name in zone_names:
            request = SvarProtoModule.GetSvarsInfoRequest(
                domain_id=allowed_domain_names.valid_name(domain_name),
                zone_id=allowed_zone_names.valid_name(zone_name),
            )
            response = self._service.get_variables_info(request)
            if solution_variables_info is None:
                solution_variables_info = SolutionVariableInfo.SolutionVariables(
                    response.svars_info
                )
            else:
                solution_variables_info._filter(response.svars_info)
        return solution_variables_info

    def get_zones_info(self) -> ZonesInfo:
        """Get zones info."""
        request = SvarProtoModule.GetZonesInfoRequest()
        response = self._service.get_zones_info(request)
        return SolutionVariableInfo.ZonesInfo(
            response.zones_info, response.domains_info
        )


def extract_svars(solution_variables_data):
    """Extract SVAR data via a server call (v1 proto payload shape)."""

    def _extract_svar(field_datatype, field_size, solution_variables_data):
        field_arr = np.empty(field_size, dtype=field_datatype)
        field_datatype_item_size = np.dtype(field_datatype).itemsize
        index = 0
        for solution_variable_data in solution_variables_data:
            chunk = solution_variable_data.payload
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
                    chunk.float_payload.payloads
                    or chunk.int_payload.payloads
                    or chunk.double_payload.payloads
                    or chunk.long_payload.payloads
                )
                count = len(payload)
                field_arr[index : index + count] = np.fromiter(
                    payload, dtype=field_datatype
                )
                index += count
                if index == field_size:
                    return field_arr

    zones_svar_data = {}
    for array in solution_variables_data:
        if array.WhichOneof("array") == "payload_info":
            zones_svar_data[array.payload_info.zone] = _extract_svar(
                _FieldDataConstants.proto_field_type_to_np_data_type[
                    array.payload_info.field_type
                ],
                array.payload_info.field_size,
                solution_variables_data,
            )
        elif array.WhichOneof("array") == "header":
            continue

    return zones_svar_data


class SolutionVariableData(_v0.SolutionVariableData):
    """Provides access to Fluent SVAR data on zones (v1 proto API)."""

    @deprecate_arguments(
        old_args="solution_variable_name",
        new_args="variable_name",
        version="v0.35.1",
    )
    def get_data(
        self,
        variable_name: str,
        zone_names: List[str],
        domain_name: str | None = "mixture",
    ) -> _v0.SolutionVariableData.Data:
        """Get SVAR data on zones."""
        self._update_solution_variable_info()
        svars_request = SvarProtoModule.GetSvarDataRequest(
            provide_bytes_stream=_FieldDataConstants.bytes_stream,
            chunk_size=_FieldDataConstants.chunk_size,
        )
        svars_request.domain_id = self._allowed_domain_names.valid_name(domain_name)
        svars_request.name = self._allowed_solution_variable_names.valid_name(
            variable_name,
            zone_names,
            domain_name,
        )
        zone_id_name_map = {}
        for zone_name in zone_names:
            zone_id = self._allowed_zone_names.valid_name(zone_name)
            zone_id_name_map[zone_id] = zone_name
            svars_request.zones.append(zone_id)

        return _v0.SolutionVariableData.Data(
            domain_name,
            zone_id_name_map,
            extract_svars(self._service.get_data(svars_request)),
        )

    @deprecate_arguments(
        old_args="solution_variable_name",
        new_args="variable_name",
        version="v0.35.1",
    )
    def set_data(
        self,
        variable_name: str,
        zone_names_to_data: Dict[str, np.array],
        domain_name: str | None = "mixture",
    ) -> None:
        """Set SVAR data on zones."""
        self._update_solution_variable_info()
        variable_name = self._allowed_solution_variable_names.valid_name(
            variable_name,
            list(zone_names_to_data.keys()),
            domain_name,
        )
        domain_id = self._allowed_domain_names.valid_name(domain_name)
        zone_ids_to_svar_data = {
            self._allowed_zone_names.valid_name(zone_name): solution_variable_data
            for zone_name, solution_variable_data in zone_names_to_data.items()
        }

        def generate_set_data_requests():
            set_data_requests = []

            set_data_requests.append(
                SvarProtoModule.SetSvarDataRequest(
                    header=SvarProtoModule.SvarHeader(
                        name=variable_name, domain_id=domain_id
                    )
                )
            )

            for zone_id, solution_variable_data in zone_ids_to_svar_data.items():
                max_array_size = (
                    _FieldDataConstants.chunk_size
                    / np.dtype(solution_variable_data.dtype).itemsize
                )
                solution_variable_data_list = np.array_split(
                    solution_variable_data,
                    math.ceil(solution_variable_data.size / max_array_size),
                )
                set_data_requests.append(
                    SvarProtoModule.SetSvarDataRequest(
                        payload_info=SvarProtoModule.Info(
                            field_type=_FieldDataConstants.np_data_type_to_proto_field_type[
                                solution_variable_data.dtype.type
                            ],
                            field_size=solution_variable_data.size,
                            zone=zone_id,
                        )
                    )
                )
                set_data_requests += [
                    SvarProtoModule.SetSvarDataRequest(
                        payload=(
                            SvarProtoModule.Payload(
                                float_payload=FieldDataProtoModule.FloatPayload(
                                    payloads=solution_variable_data
                                )
                            )
                            if solution_variable_data.dtype.type == np.float32
                            else (
                                SvarProtoModule.Payload(
                                    double_payload=FieldDataProtoModule.DoublePayload(
                                        payloads=solution_variable_data
                                    )
                                )
                                if solution_variable_data.dtype.type == np.float64
                                else (
                                    SvarProtoModule.Payload(
                                        int_payload=FieldDataProtoModule.IntPayload(
                                            payloads=solution_variable_data
                                        )
                                    )
                                    if solution_variable_data.dtype.type == np.int32
                                    else SvarProtoModule.Payload(
                                        long_payload=FieldDataProtoModule.LongPayload(
                                            payloads=solution_variable_data
                                        )
                                    )
                                )
                            )
                        )
                    )
                    for solution_variable_data in solution_variable_data_list
                    if solution_variable_data.size > 0
                ]

            for set_data_request in set_data_requests:
                yield set_data_request

        self._service.set_data(generate_set_data_requests())
