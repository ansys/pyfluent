# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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

"""Wrapper over the solution variable gRPC service of Fluent (v0 proto API)."""

import math
from typing import Any, Sequence

import grpc
import numpy as np
import numpy.typing as npt

from ansys.api.fluent.v0 import field_data_pb2, svar_pb2, svar_pb2_grpc
from ansys.fluent.core._grpc_services.field_data_service_v0 import _FieldDataConstants
from ansys.fluent.core.services._protocols import ServiceProtocol
from ansys.fluent.core.services.interceptors import (
    GrpcErrorInterceptor,
    TracingInterceptor,
)


class SolutionVariables:
    """Class containing information for multiple solution variables."""

    class SolutionVariable:
        """Class containing information for single solution variable."""

        def __init__(self, solution_variable_info: svar_pb2.SvarInfo):
            """Initialize SolutionVariable."""
            self.name = solution_variable_info.name
            self.dimension = solution_variable_info.dimension
            self.field_type = _FieldDataConstants.proto_field_type_to_np_data_type[
                solution_variable_info.fieldType
            ]

        def __repr__(self):
            return f"name:{self.name} dimension:{self.dimension} field_type:{self.field_type}"

    def __init__(self, solution_variables_info: Sequence[svar_pb2.SvarInfo]):
        """Initialize SolutionVariables."""
        self._solution_variables_info: dict[
            str, "SolutionVariables.SolutionVariable"
        ] = {
            solution_variable_info.name: SolutionVariables.SolutionVariable(
                solution_variable_info
            )
            for solution_variable_info in solution_variables_info
        }

    def _filter(self, solution_variables_info):
        self._solution_variables_info = {
            k: v
            for k, v in self._solution_variables_info.items()
            if k
            in [
                solution_variable_info.name
                for solution_variable_info in solution_variables_info
            ]
        }

    def __getitem__(self, name: str) -> "SolutionVariables.SolutionVariable":
        return self._solution_variables_info[name]

    def get(self, name: str) -> "SolutionVariables.SolutionVariable | None":
        """Get name from solution variables"""
        return self._solution_variables_info.get(name)

    @property
    def solution_variables(self) -> list[str]:
        """Solution variables."""
        return list(self._solution_variables_info.keys())


class ZonesInfo:
    """Class containing information for multiple zones."""

    class ZoneInfo:
        """Class containing information for single zone."""

        class PartitionsInfo:
            """Class containing information for partitions."""

            def __init__(self, partition_info):
                """Initialize PartitionsInfo."""
                self.count = partition_info.count
                self.start_index = partition_info.startIndex if self.count > 0 else 0
                self.end_index = partition_info.endIndex if self.count > 0 else 0

        def __init__(self, zone_info):
            """Initialize ZoneInfo."""
            self.name = zone_info.name
            self.zone_id = zone_info.zoneId
            self.zone_type = zone_info.zoneType
            self.thread_type = zone_info.threadType
            self.partitions_info = [
                self.PartitionsInfo(partition_info)
                for partition_info in zone_info.partitionsInfo
            ]

        @property
        def count(self) -> int:
            """Get zone count."""
            return sum(
                [partition_info.count for partition_info in self.partitions_info]
            )

        def __repr__(self):
            partition_str = ""
            for i, partition_info in enumerate(self.partitions_info):
                partition_str += f"\n\t{i}. {partition_info.count}[{partition_info.start_index}:{partition_info.end_index}]"
            return f"name:{self.name} count: {self.count} zone_id:{self.zone_id} zone_type:{self.zone_type} threadType:{'Cell' if self.thread_type == svar_pb2.ThreadType.CELL_THREAD else 'Face'}{partition_str}"

    def __init__(self, zones_info, domains_info):
        """Initialize ZonesInfo."""
        self._zones_info: dict[str, "ZonesInfo.ZoneInfo"] = {
            zone_info.name: self.ZoneInfo(zone_info) for zone_info in zones_info
        }
        self._domains_info: dict[str, int] = {
            domain_info.name: domain_info.domainId for domain_info in domains_info
        }

    def __getitem__(self, name: str) -> "ZonesInfo.ZoneInfo":
        return self._zones_info[name]

    def get(self, name: str) -> "ZonesInfo.ZoneInfo | None":
        """Get name from zones info"""
        return self._zones_info.get(name)

    @property
    def zone_names(self) -> list[str]:
        """Get zone names."""
        return list(self._zones_info.keys())

    @property
    def domains(self) -> list[str]:
        """Get domain names."""
        return list(self._domains_info.keys())

    def domain_id(self, domain_name) -> int:
        """Get domain id."""
        return self._domains_info.get(domain_name, None)


class SolutionVariableService(ServiceProtocol):
    """SVAR service of Fluent."""

    def __init__(self, channel: grpc.Channel, metadata, fluent_error_state):
        """__init__ method of SVAR service class."""
        intercept_channel = grpc.intercept_channel(
            channel,
            GrpcErrorInterceptor(),
            TracingInterceptor(),
        )
        self._stub = svar_pb2_grpc.svarStub(intercept_channel)
        self._metadata = metadata
        del fluent_error_state  # unused variable

    def get_data(
        self,
        variable_name: str,
        zone_names: list[str],
        domain_name: str,
        allowed_solution_variable_names,
        allowed_domain_names,
        allowed_zone_names,
    ) -> tuple[dict[int, str], dict[Any, npt.NDArray[Any]]]:
        """Get SVAR data on zones.

        Parameters
        ----------
        variable_name : str
            Name of the solution variable.
        zone_names: List[str]
            Zone names list for solution variable data.
        domain_name : str, optional
            Domain name. The default is ``mixture``.
        allowed_solution_variable_names: AllowedSolutionVariableNames
            AllowedSolutionVariableNames object to validate solution variable names.
        allowed_domain_names: AllowedDomainNames
            AllowedDomainNames object to validate domain names.
        allowed_zone_names: AllowedZoneNames
            AllowedZoneNames object to validate zone names.

        Returns
        -------
        dict[Any, npt.NDArray[Any]]
            Dictionary containing SVAR data.
        """
        svars_request = svar_pb2.GetSvarDataRequest(
            provideBytesStream=_FieldDataConstants.bytes_stream,
            chunkSize=_FieldDataConstants.chunk_size,
        )
        svars_request.domainId = allowed_domain_names.valid_name(domain_name)
        svars_request.name = allowed_solution_variable_names.valid_name(
            variable_name,
            zone_names,
            domain_name,
        )
        zone_id_name_map = {}
        for zone_name in zone_names:
            zone_id = allowed_zone_names.valid_name(zone_name)
            zone_id_name_map[zone_id] = zone_name
            svars_request.zones.append(zone_id)

        return zone_id_name_map, extract_svars(
            self._stub.GetSvarData(svars_request, metadata=self._metadata)
        )

    def set_data(
        self,
        variable_name: str,
        zone_names_to_data: dict[str, np.ndarray],
        domain_name: str,
        allowed_solution_variable_names,
        allowed_domain_names,
        allowed_zone_names,
    ) -> None:
        """Set SVAR data on zones.

        Parameters
        ----------
        variable_name : str
            Name of the solution variable.
        zone_names_to_data: Dict[str, np.array]
            Dictionary containing zone names for solution variable data.
        domain_name : str, optional
            Domain name. The default is ``mixture``.
        allowed_solution_variable_names: AllowedSolutionVariableNames
            AllowedSolutionVariableNames object to validate solution variable names.
        allowed_domain_names: AllowedDomainNames
            AllowedDomainNames object to validate domain names.
        allowed_zone_names: AllowedZoneNames
            AllowedZoneNames object to validate zone names.

        Returns
        -------
        None
        """
        variable_name = allowed_solution_variable_names.valid_name(
            variable_name,
            list(zone_names_to_data.keys()),
            domain_name,
        )
        domain_id = allowed_domain_names.valid_name(domain_name)
        zone_ids_to_svar_data = {
            allowed_zone_names.valid_name(zone_name): solution_variable_data
            for zone_name, solution_variable_data in zone_names_to_data.items()
        }

        def generate_set_data_requests():
            set_data_requests = []

            set_data_requests.append(
                svar_pb2.SetSvarDataRequest(
                    header=svar_pb2.SvarHeader(name=variable_name, domainId=domain_id)
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
                    svar_pb2.SetSvarDataRequest(
                        payloadInfo=svar_pb2.Info(
                            fieldType=_FieldDataConstants.np_data_type_to_proto_field_type[
                                solution_variable_data.dtype.type
                            ],
                            fieldSize=solution_variable_data.size,
                            zone=zone_id,
                        )
                    )
                )
                set_data_requests += [
                    svar_pb2.SetSvarDataRequest(
                        payload=(
                            svar_pb2.Payload(
                                floatPayload=field_data_pb2.FloatPayload(
                                    payload=solution_variable_data
                                )
                            )
                            if solution_variable_data.dtype.type == np.float32
                            else (
                                svar_pb2.Payload(
                                    doublePayload=field_data_pb2.DoublePayload(
                                        payload=solution_variable_data
                                    )
                                )
                                if solution_variable_data.dtype.type == np.float64
                                else (
                                    svar_pb2.Payload(
                                        intPayload=field_data_pb2.IntPayload(
                                            payload=solution_variable_data
                                        )
                                    )
                                    if solution_variable_data.dtype.type == np.int32
                                    else svar_pb2.Payload(
                                        longPayload=field_data_pb2.LongPayload(
                                            payload=solution_variable_data
                                        )
                                    )
                                )
                            )
                        )
                    )
                    for solution_variable_data in solution_variable_data_list
                    if solution_variable_data.size > 0
                ]

            yield from set_data_requests

        self._stub.SetSvarData(generate_set_data_requests(), metadata=self._metadata)

    def get_variables_info(
        self,
        zone_names: list[str],
        domain_name: str,
        allowed_zone_names,
        allowed_domain_names,
    ) -> SolutionVariables:
        """Get SVARs info for zones in the domain.

        Parameters
        ----------
        zone_names : List[str]
            List of zone names.
        domain_name: str, optional
            Domain name.The default is ``mixture``.
        allowed_zone_names: AllowedZoneNames
            AllowedZoneNames object to validate zone names.
        allowed_domain_names: AllowedDomainNames
            AllowedDomainNames object to validate domain names.

        Returns
        -------
        SolutionVariables
            Object containing information for SVARs which are common for list of zone names.
        """
        solution_variables_info = None
        for zone_name in zone_names:
            request = svar_pb2.GetSvarsInfoRequest(
                domainId=allowed_domain_names.valid_name(domain_name),
                zoneId=allowed_zone_names.valid_name(zone_name),
            )
            response = self._stub.GetSvarsInfo(request, metadata=self._metadata)
            if solution_variables_info is None:
                solution_variables_info = SolutionVariables(response.svarsInfo)
            else:
                solution_variables_info._filter(response.svarsInfo)
        return solution_variables_info

    def get_zones_info(self) -> ZonesInfo:
        """Get Zones info.

        Parameters
        ----------
        None

        Returns
        -------
        SolutionVariableInfo.ZonesInfo
            Object containing information for all zones.
        """
        request = svar_pb2.GetZonesInfoRequest()
        response = self._stub.GetZonesInfo(request, metadata=self._metadata)
        return ZonesInfo(response.zonesInfo, response.domainsInfo)


def extract_svars(solution_variables_data):
    """Extracts SVAR data via a server call."""

    def _extract_svar(
        field_datatype: npt.DTypeLike, field_size: int, solution_variables_data
    ) -> npt.NDArray[np.float64] | None:
        field_arr = np.empty(field_size, dtype=field_datatype)
        field_datatype_item_size = np.dtype(field_datatype).itemsize
        index = 0
        for solution_variable_data in solution_variables_data:
            chunk = solution_variable_data.payload
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

    zones_svar_data = dict[Any, npt.NDArray[Any] | None]()
    for array in solution_variables_data:
        if array.WhichOneof("array") == "payloadInfo":
            zones_svar_data[array.payloadInfo.zone] = _extract_svar(
                _FieldDataConstants.proto_field_type_to_np_data_type[
                    array.payloadInfo.fieldType
                ],
                array.payloadInfo.fieldSize,
                solution_variables_data,
            )
        elif array.WhichOneof("array") == "header":
            continue

    return zones_svar_data
