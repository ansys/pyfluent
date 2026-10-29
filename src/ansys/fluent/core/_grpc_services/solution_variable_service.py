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

"""Wrapper over the solution variable gRPC service of Fluent (v1 proto API)."""

import math
from typing import Any, Sequence

import numpy as np
import numpy.typing as npt

from ansys.api.fluent.v1 import (
    field_data_pb2,
    solution_variable_pb2,
    solution_variable_pb2_grpc,
)
from ansys.fluent.core._grpc_services.field_data_service import _FieldDataConstants
from ansys.fluent.core.services._protocols import ServiceProtocol


class SolutionVariables:
    """Class containing information for multiple solution variables."""

    class SolutionVariable:
        """Class containing information for single solution variable."""

        def __init__(
            self, solution_variable_info: solution_variable_pb2.SolutionVariableInfo
        ):
            """Initialize SolutionVariable."""
            self.name = solution_variable_info.name
            self.dimension = solution_variable_info.dimension
            self.field_type = _FieldDataConstants.proto_field_type_to_np_data_type[
                solution_variable_info.field_type
            ]

        def __repr__(self):
            return f"name:{self.name} dimension:{self.dimension} field_type:{self.field_type}"

    def __init__(
        self,
        solution_variables_info: Sequence[solution_variable_pb2.SolutionVariableInfo],
    ):
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
                self.start_index = partition_info.start_index if self.count > 0 else 0
                self.end_index = partition_info.end_index if self.count > 0 else 0

        def __init__(self, zone_info):
            """Initialize ZoneInfo."""
            self.name = zone_info.name
            self.zone_id = zone_info.zone_id
            self.zone_type = zone_info.zone_type
            self.thread_type = zone_info.thread_type
            self.is_cell_thread: bool = (
                zone_info.thread_type
                == solution_variable_pb2.ThreadType.THREAD_TYPE_CELL
            )
            self.partitions_info = [
                self.PartitionsInfo(partition_info)
                for partition_info in zone_info.partitions_info
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
            return f"name:{self.name} count: {self.count} zone_id:{self.zone_id} zone_type:{self.zone_type} thread_type:{'Cell' if self.thread_type == solution_variable_pb2.ThreadType.THREAD_TYPE_CELL else 'Face'}{partition_str}"

    def __init__(self, zones_info, domains_info):
        """Initialize ZonesInfo."""
        self._zones_info: dict[str, "ZonesInfo.ZoneInfo"] = {
            zone_info.name: self.ZoneInfo(zone_info) for zone_info in zones_info
        }
        self._domains_info: dict[str, int] = {
            domain_info.name: domain_info.domain_id for domain_info in domains_info
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
    """Class wrapping the solution variable gRPC service of Fluent (v1 proto API)."""

    def __init__(self, intercept_channel, metadata):
        """__init__ method of SVAR service class."""

        self._stub = solution_variable_pb2_grpc.SolutionVariableStub(intercept_channel)
        self._metadata = metadata

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
        svars_request = solution_variable_pb2.GetSolutionVariableDataRequest(
            provide_bytes_stream=_FieldDataConstants.bytes_stream,
            chunk_size=_FieldDataConstants.chunk_size,
        )
        svars_request.domain_id = allowed_domain_names.valid_name(domain_name)
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
            self._stub.GetSolutionVariableData(svars_request, metadata=self._metadata)
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
                solution_variable_pb2.SetSolutionVariableDataRequest(
                    header=solution_variable_pb2.SolutionVariableHeader(
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
                    solution_variable_pb2.SetSolutionVariableDataRequest(
                        payload_info=solution_variable_pb2.Info(
                            field_type=_FieldDataConstants.np_data_type_to_proto_field_type[
                                solution_variable_data.dtype.type
                            ],
                            field_size=solution_variable_data.size,
                            zone=zone_id,
                        )
                    )
                )
                set_data_requests += [
                    solution_variable_pb2.SetSolutionVariableDataRequest(
                        payload=(
                            solution_variable_pb2.Payload(
                                float_payload=field_data_pb2.FloatPayload(
                                    payloads=solution_variable_data
                                )
                            )
                            if solution_variable_data.dtype.type == np.float32
                            else (
                                solution_variable_pb2.Payload(
                                    double_payload=field_data_pb2.DoublePayload(
                                        payloads=solution_variable_data
                                    )
                                )
                                if solution_variable_data.dtype.type == np.float64
                                else (
                                    solution_variable_pb2.Payload(
                                        int_payload=field_data_pb2.IntPayload(
                                            payloads=solution_variable_data
                                        )
                                    )
                                    if solution_variable_data.dtype.type == np.int32
                                    else solution_variable_pb2.Payload(
                                        long_payload=field_data_pb2.LongPayload(
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

        self._stub.SetSolutionVariableData(
            generate_set_data_requests(), metadata=self._metadata
        )

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
            request = solution_variable_pb2.GetSolutionVariableInfoRequest(
                domain_id=allowed_domain_names.valid_name(domain_name),
                zone_id=allowed_zone_names.valid_name(zone_name),
            )
            response = self._stub.GetSolutionVariableInfo(
                request, metadata=self._metadata
            )
            if solution_variables_info is None:
                solution_variables_info = SolutionVariables(response.svars_info)
            else:
                solution_variables_info._filter(response.svars_info)
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
        request = solution_variable_pb2.GetZonesInfoRequest()
        response = self._stub.GetZonesInfo(request, metadata=self._metadata)
        return ZonesInfo(response.zones_info, response.domains_info)


def _format_bytes(num_bytes: int) -> str:
    """Return a human-readable binary size string for a byte count."""
    size = float(num_bytes)
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if size < 1024.0 or unit == "TiB":
            return f"{int(size)} B" if unit == "B" else f"{size:.2f} {unit}"
        size /= 1024.0


class IncompleteSolutionVariableDataError(RuntimeError):
    """Raised when streamed solution variable data ends before all elements arrive.

    The server first declares how many elements it will send for a zone
    (``field_size``), and the client reconstructs the array from the streamed
    chunks. If the stream ends before ``field_size`` elements have been
    received, the data for that zone is incomplete and this error is raised.

    The usual cause is that a *single* zone's data is too large to be streamed
    in one response: a single gRPC/protobuf message cannot exceed ~2 GiB, so the
    server stops sending once that ceiling is reached. This is common for large
    multi-component fields -- for example ``SV_CENTROID`` (3 components) on a
    cell zone with hundreds of millions of cells.

    Note that the client ``chunk_size`` setting does not help here: it only
    controls how a response is sliced into messages, not the total amount of
    data requested for a zone.

    To work around it:

    * If several zones were requested in one call, request each zone separately
      so no single response is oversized.
    * If a single zone is itself too large, reduce the amount of data (for
      example request a scalar field rather than a multi-component one), split
      the zone into smaller cell zones, or read the values from the case/data
      file offline instead of over gRPC.

    Attributes
    ----------
    received : int
        Number of elements actually received before the stream ended.
    expected : int
        Number of elements the server declared it would send for the zone.
    item_size : int | None
        Size in bytes of a single element, when known. Used to report the
        approximate payload size in the error message.
    """

    def __init__(self, received: int, expected: int, item_size: int | None = None):
        """Initialize IncompleteSolutionVariableDataError."""
        self.received = received
        self.expected = expected
        self.item_size = item_size

        if item_size:
            size_note = (
                f" (~{_format_bytes(expected * item_size)} requested; a single "
                f"gRPC/protobuf message cannot exceed ~2 GiB)"
            )
        else:
            size_note = " (a single gRPC/protobuf message cannot exceed ~2 GiB)"

        super().__init__(
            f"Solution variable data stream ended prematurely: received "
            f"{received:,} of {expected:,} expected elements{size_note}. "
            f"This usually means a single zone's data is too large for the "
            f"server to stream in one response. Note that changing the client "
            f"chunk size does not help, because it does not reduce the per-zone "
            f"total. To work around it: if you requested several zones in one "
            f"call, request each zone separately; if a single zone is too large "
            f"(common for multi-component fields such as 'SV_CENTROID' on very "
            f"large cell zones), request a smaller field, or split the zone into "
            f"smaller cell zones."
        )


def extract_svars(solution_variables_data):
    """Extract SVAR data via a server call (v1 proto payload shape).

    Raises
    ------
    IncompleteSolutionVariableDataError
        If the streamed data for a zone ends before all declared elements are
        received. This typically means a single zone's data exceeds the
        ~2 GiB gRPC/protobuf message-size limit; see the exception's
        documentation for ways to work around it.
    """

    def _extract_svar(field_datatype, field_size, solution_variables_data):
        field_arr = np.empty(field_size, dtype=field_datatype)
        if field_size == 0:
            return field_arr
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
        raise IncompleteSolutionVariableDataError(
            index, field_size, field_datatype_item_size
        )

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
