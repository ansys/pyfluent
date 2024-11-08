"""Wrappers over SVAR gRPC service of Fluent."""

import math
from typing import Dict, List
import warnings

import grpc
import numpy as np

from ansys.api.fluent.v0 import field_data_pb2 as FieldDataProtoModule
from ansys.api.fluent.v0 import svar_pb2 as SvarProtoModule
from ansys.api.fluent.v0 import svar_pb2_grpc as SvarGrpcModule
from ansys.fluent.core.services.field_data import (
    _FieldDataConstants,
    override_help_text,
)
from ansys.fluent.core.services.interceptors import (
    GrpcErrorInterceptor,
    TracingInterceptor,
)
from ansys.fluent.core.solver.error_message import allowed_name_error_message
from ansys.fluent.core.warnings import PyFluentDeprecationWarning


class SolutionVariableService:
    """SVAR service of Fluent."""

    def __init__(self, channel: grpc.Channel, metadata):
        """__init__ method of SVAR service class."""
        intercept_channel = grpc.intercept_channel(
            channel,
            GrpcErrorInterceptor(),
            TracingInterceptor(),
        )
        self.__stub = SvarGrpcModule.svarStub(intercept_channel)
        self.__metadata = metadata

    def get_data(self, request):
        """GetSvarData RPC of SVAR service."""
        return self.__stub.GetSvarData(request, metadata=self.__metadata)

    def set_data(self, request):
        """SetSvarData RPC of SVAR service."""
        return self.__stub.SetSvarData(request, metadata=self.__metadata)

    def get_variables_info(self, request):
        """GetSvarsInfo RPC of SVAR service."""
        return self.__stub.GetSvarsInfo(request, metadata=self.__metadata)

    def get_zones_info(self, request):
        """GetZonesInfo RPC of SVAR service."""
        return self.__stub.GetZonesInfo(request, metadata=self.__metadata)


class SolutionVariableInfo:
    """Provide access to Fluent SVARs and Zones information.

    Examples
    --------
    >>> solution_variable_info = solver_session.fields.solution_variable_info
    >>> wall_fluid_info = solution_variable_info.get_variables_info(zone_names=['wall' , "fluid"], domain_name="mixture")
    >>> print(wall_fluid_info.solution_variables)
    >>> ['SV_CENTROID', 'SV_D', 'SV_H', 'SV_K', 'SV_P', 'SV_T', 'SV_U', 'SV_V', 'SV_W']
    >>> solution_variable_info_centroid = wall_fluid_info['SV_CENTROID']
    >>> print(solution_variable_info_centroid)
    >>> name:SV_CENTROID dimension:3 field_type:<class 'numpy.float64'>
    >>> zones_info = solution_variable_info.get_zones_info()
    >>> print(zones_info.zones)
    >>> ['fluid', 'wall', 'symmetry', 'pressure-outlet-7', 'velocity-inlet-6', 'velocity-inlet-5', 'default-interior']
    >>> zone_info = zones_info['wall']
    >>> print(zone_info)
    >>> name:wall count: 3630 zone_id:3 zone_type:wall thread_type:Face
    """

    class SolutionVariables:
        """Class containing information for multiple solution variables."""

        class SolutionVariable:
            """Class containing information for single solution variable."""

            def __init__(self, solution_variable_info):
                """Initialize SolutionVariable."""
                self.name = solution_variable_info.name
                self.dimension = solution_variable_info.dimension
                self.field_type = _FieldDataConstants.proto_field_type_to_np_data_type[
                    solution_variable_info.fieldType
                ]

            def __repr__(self):
                return f"name:{self.name} dimension:{self.dimension} field_type:{self.field_type}"

        def __init__(self, solution_variables_info):
            """Initialize SolutionVariables."""
            self._solution_variables_info = {}
            for solution_variable_info in solution_variables_info:
                self._solution_variables_info[solution_variable_info.name] = (
                    SolutionVariableInfo.SolutionVariables.SolutionVariable(
                        solution_variable_info
                    )
                )

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

        def __getitem__(self, name):
            return self._solution_variables_info.get(name, None)

        @property
        def solution_variables(self) -> List[str]:
            """Solution variables."""
            return list(self._solution_variables_info.keys())

        @property
        def svars(self) -> List[str]:
            """Solution variables."""
            warnings.warn(
                "svars is deprecated, use solution_variables instead",
                PyFluentDeprecationWarning,
            )
            return self.solution_variables

    class ZonesInfo:
        """Class containing information for multiple zones."""

        class ZoneInfo:
            """Class containing information for single zone."""

            class PartitionsInfo:
                """Class containing information for partitions."""

                def __init__(self, partition_info):
                    """Initialize PartitionsInfo."""
                    self.count = partition_info.count
                    self.start_index = (
                        partition_info.startIndex if self.count > 0 else 0
                    )
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
                return f"name:{self.name} count: {self.count} zone_id:{self.zone_id} zone_type:{self.zone_type} threadType:{'Cell' if self.thread_type == SvarProtoModule.ThreadType.CELL_THREAD else 'Face'}{partition_str}"

        def __init__(self, zones_info, domains_info):
            """Initialize ZonesInfo."""
            self._zones_info = {}
            self._domains_info = {}
            for zone_info in zones_info:
                self._zones_info[zone_info.name] = self.ZoneInfo(zone_info)
            for domain_info in domains_info:
                self._domains_info[domain_info.name] = domain_info.domainId

        def __getitem__(self, name):
            return self._zones_info.get(name, None)

        @property
        def zones(self) -> List[str]:
            """Get zone names."""
            return list(self._zones_info.keys())

        @property
        def domains(self) -> List[str]:
            """Get domain names."""
            return list(self._domains_info.keys())

        def domain_id(self, domain_name) -> int:
            """Get domain id."""
            return self._domains_info.get(domain_name, None)

    def __init__(
        self,
        service: SolutionVariableService,
    ):
        """Initialize SolutionVariableInfo."""
        self._service = service

    def get_variables_info(
        self, zone_names: List[str], domain_name: str | None = "mixture"
    ) -> SolutionVariables:
        """Get SVARs info for zones in the domain.

        Parameters
        ----------
        zone_names : List[str]
            List of zone names.
        domain_name: str, optional
            Domain name.The default is ``mixture``.

        Returns
        -------
        SolutionVariableInfo.SolutionVariables
            Object containing information for SVARs which are common for list of zone names.
        """

        allowed_zone_names = _AllowedZoneNames(self)
        allowed_domain_names = _AllowedDomainNames(self)
        solution_variables_info = None
        for zone_name in zone_names:
            request = SvarProtoModule.GetSvarsInfoRequest(
                domainId=allowed_domain_names.valid_name(domain_name),
                zoneId=allowed_zone_names.valid_name(zone_name),
            )
            response = self._service.get_variables_info(request)
            if solution_variables_info is None:
                solution_variables_info = SolutionVariableInfo.SolutionVariables(
                    response.svarsInfo
                )
            else:
                solution_variables_info._filter(response.svarsInfo)
        return solution_variables_info

    def get_svars_info(
        self, zone_names: List[str], domain_name: str | None = "mixture"
    ) -> SolutionVariables:
        """Get solution variables info."""
        warnings.warn(
            "get_svars_info is deprecated, use get_variables_info instead",
            PyFluentDeprecationWarning,
        )
        return self.get_variables_info(zone_names=zone_names, domain_name=domain_name)

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
        request = SvarProtoModule.GetZonesInfoRequest()
        response = self._service.get_zones_info(request)
        return SolutionVariableInfo.ZonesInfo(response.zonesInfo, response.domainsInfo)


class SvarError(ValueError):
    """Exception class for errors in solution variable name."""

    def __init__(self, solution_variable_name: str, allowed_values: List[str]):
        """Initialize SvarError."""
        self.solution_variable_name = solution_variable_name
        super().__init__(
            allowed_name_error_message(
                context="solution variable",
                trial_name=solution_variable_name,
                allowed_values=allowed_values,
            )
        )


class ZoneError(ValueError):
    """Exception class for errors in Zone name."""

    def __init__(self, zone_name: str, allowed_values: List[str]):
        """Initialize ZoneError."""
        self.zone_name = zone_name
        super().__init__(
            allowed_name_error_message(
                context="zone", trial_name=zone_name, allowed_values=allowed_values
            )
        )


class _AllowedNames:
    def is_valid(self, name):
        """Check whether a given name is valid or not."""
        return name in self()


class _AllowedSvarNames:
    def __init__(self, solution_variable_info: SolutionVariableInfo):
        self._solution_variable_info = solution_variable_info

    def __call__(
        self, zone_names: List[str], domain_name: str | None = "mixture"
    ) -> List[str]:
        return self._solution_variable_info.get_variables_info(
            zone_names=zone_names, domain_name=domain_name
        ).solution_variables

    def is_valid(
        self,
        solution_variable_name,
        zone_names: List[str],
        domain_name: str | None = "mixture",
    ):
        """Check whether solution variable name is valid or not."""
        return solution_variable_name in self(
            zone_names=zone_names, domain_name=domain_name
        )

    def valid_name(
        self,
        solution_variable_name,
        zone_names: List[str],
        domain_name: str | None = "mixture",
    ):
        """Get a valid solution variable name.

        Raises
        ------
        SvarError
            If the given solution variable name is invalid.
        """
        if not self.is_valid(
            solution_variable_name, zone_names=zone_names, domain_name=domain_name
        ):
            raise SvarError(
                solution_variable_name=solution_variable_name,
                allowed_values=self(zone_names=zone_names, domain_name=domain_name),
            )
        return solution_variable_name


class _AllowedZoneNames(_AllowedNames):
    def __init__(self, solution_variable_info: SolutionVariableInfo):
        self._zones_info = solution_variable_info.get_zones_info()

    def __call__(self) -> List[str]:
        return self._zones_info.zones

    def valid_name(self, zone_name):
        """Get a valid zone name.

        Raises
        ------
        ZoneError
            If the given zone name is invalid.
        """
        if not self.is_valid(zone_name):
            raise ZoneError(
                zone_name=zone_name,
                allowed_values=self(),
            )
        return self._zones_info[zone_name].zone_id


class _AllowedDomainNames(_AllowedNames):
    def __init__(self, solution_variable_info: SolutionVariableInfo):
        self._zones_info = solution_variable_info.get_zones_info()

    def __call__(self) -> List[str]:
        return self._zones_info.domains

    def valid_name(self, domain_name):
        """Get a valid domain name.

        Raises
        ------
        ZoneError
            If the given domain name is invalid.
        """
        if not self.is_valid(domain_name):
            raise ZoneError(
                domain_name=domain_name,
                allowed_values=self(),
            )
        return self._zones_info.domain_id(domain_name)


class _SvarMethod:
    class _Arg:
        def __init__(self, accessor):
            self._accessor = accessor

        def allowed_values(self):
            """Get allowed values."""
            return sorted(self._accessor())

    def __init__(self, svar_accessor, args_allowed_values_accessors):
        self._svar_accessor = svar_accessor
        for arg_name, accessor in args_allowed_values_accessors.items():
            setattr(self, arg_name, _SvarMethod._Arg(accessor))

    def __call__(self, *args, **kwargs):
        return self._svar_accessor(*args, **kwargs)


def extract_svars(solution_variables_data):
    """Extracts SVAR data via a server call."""

    def _extract_svar(field_datatype, field_size, solution_variables_data):
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
                payload = (
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

    zones_svar_data = {}
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


class SolutionVariableData:
    """Provides access to Fluent SVAR data on zones.

    Examples
    --------
    >>> solution_variable_data = solver_session.fields.solution_variable_data
    >>> sv_t_wall_fluid=solver_session.fields.solution_variable_data.get_data(solution_variable_name="SV_T", domain_name="mixture", zone_names=["fluid", "wall"])
    >>> print(sv_t_wall_fluid.domain)
    >>> 'mixture'
    >>> print(sv_t_wall_fluid.zones)
    >>> ['fluid', 'wall']
    >>> fluid_temp = sv_t_wall_fluid['fluid']
    >>> print(fluid_temp.size)
    >>> 13852
    >>> print(fluid_temp.dtype)
    >>> float64
    >>> print(fluid_temp)
    >>> array([600., 600., 600., ..., 600., 600., 600.])
    >>> wall_temp_array = solution_variable_data.create_empty_array("SV_T", "wall")
    >>> fluid_temp_array =solution_variable_data.create_empty_array("SV_T", "fluid")
    >>> wall_temp_array[:]= 500
    >>> fluid_temp_array[:]= 600
    >>> zone_names_to_solution_variable_data = {'wall':wall_temp_array, 'fluid':fluid_temp_array}
    >>> solution_variable_data.set_data(solution_variable_name="SV_T", domain_name="mixture", zone_names_to_solution_variable_data=zone_names_to_solution_variable_data)
    """

    class Data:
        """Solution variable data."""

        def __init__(self, domain_name, zone_id_name_map, solution_variable_data):
            """Initialize Data."""
            self._domain_name = domain_name
            self._data = {
                zone_id_name_map[zone_id]: zone_data
                for zone_id, zone_data in solution_variable_data.items()
            }

        @property
        def domain(self):
            """Domain name."""
            return self._domain_name

        @property
        def zones(self):
            """Zone name."""
            return list(self._data.keys())

        @property
        def data(self):
            """Solution variable data."""
            return self._data

        def __getitem__(self, name):
            return self._data.get(name, None)

    def __init__(
        self,
        service: SolutionVariableService,
        solution_variable_info: SolutionVariableInfo,
    ):
        """Initialize SolutionVariableData."""
        self._service = service
        self._solution_variable_info = solution_variable_info

        self.get_data = override_help_text(
            _SvarMethod(
                svar_accessor=self.get_data,
                args_allowed_values_accessors={},
            ),
            SolutionVariableData.get_data,
        )

    def _update_solution_variable_info(self):
        self._allowed_zone_names = _AllowedZoneNames(self._solution_variable_info)

        self._allowed_domain_names = _AllowedDomainNames(self._solution_variable_info)

        self._allowed_solution_variable_names = _AllowedSvarNames(
            self._solution_variable_info
        )

    def create_empty_array(
        self,
        solution_variable_name: str,
        zone_name: str,
        domain_name: str | None = "mixture",
    ) -> np.zeros:
        """Get numpy zeros array for the SVAR on a zone.

        This array can be populated  with values to set SVAR data.
        """
        self._update_solution_variable_info()

        zones_info = self._solution_variable_info.get_zones_info()
        if zone_name in zones_info.zones:
            solution_variables_info = self._solution_variable_info.get_variables_info(
                zone_names=[zone_name], domain_name=domain_name
            )
            if solution_variable_name in solution_variables_info.solution_variables:
                return np.zeros(
                    zones_info[zone_name].count
                    * solution_variables_info[solution_variable_name].dimension,
                    dtype=solution_variables_info[solution_variable_name].field_type,
                )

    def get_data(
        self,
        solution_variable_name: str,
        zone_names: List[str],
        domain_name: str | None = "mixture",
    ) -> Data:
        """Get SVAR data on zones.

        Parameters
        ----------
        solution_variable_name : str
            Name of the SVAR.
        zone_names: List[str]
            Zone names list for SVAR data.
        domain_name : str, optional
            Domain name. The default is ``mixture``.

        Returns
        -------
        SolutionVariableData.Data
            Object containing SVAR data.
        """
        self._update_solution_variable_info()
        svars_request = SvarProtoModule.GetSvarDataRequest(
            provideBytesStream=_FieldDataConstants.bytes_stream,
            chunkSize=_FieldDataConstants.chunk_size,
        )
        svars_request.domainId = self._allowed_domain_names.valid_name(domain_name)
        svars_request.name = self._allowed_solution_variable_names.valid_name(
            solution_variable_name, zone_names, domain_name
        )
        zone_id_name_map = {}
        for zone_name in zone_names:
            zone_id = self._allowed_zone_names.valid_name(zone_name)
            zone_id_name_map[zone_id] = zone_name
            svars_request.zones.append(zone_id)

        return SolutionVariableData.Data(
            domain_name,
            zone_id_name_map,
            extract_svars(self._service.get_data(svars_request)),
        )

    def get_svar_data(
        self,
        svar_name: str,
        zone_names: List[str],
        domain_name: str | None = "mixture",
    ) -> Data:
        """Get solution variable data."""
        warnings.warn(
            "get_svar_data is deprecated, use get_data instead",
            PyFluentDeprecationWarning,
        )
        return self.get_data(
            solution_variable_name=svar_name,
            zone_names=zone_names,
            domain_name=domain_name,
        )

    def set_data(
        self,
        solution_variable_name: str,
        zone_names_to_solution_variable_data: Dict[str, np.array],
        domain_name: str | None = "mixture",
    ) -> None:
        """Set SVAR data on zones.

        Parameters
        ----------
        solution_variable_name : str
            Name of the SVAR.
        zone_names_to_solution_variable_data: Dict[str, np.array]
            Dictionary containing zone names for SVAR data.
        domain_name : str, optional
            Domain name. The default is ``mixture``.

        Returns
        -------
        None
        """
        self._update_solution_variable_info()
        domain_id = self._allowed_domain_names.valid_name(domain_name)
        zone_ids_to_svar_data = {
            self._allowed_zone_names.valid_name(zone_name): solution_variable_data
            for zone_name, solution_variable_data in zone_names_to_solution_variable_data.items()
        }

        def generate_set_data_requests():
            set_data_requests = []

            set_data_requests.append(
                SvarProtoModule.SetSvarDataRequest(
                    header=SvarProtoModule.SvarHeader(
                        name=solution_variable_name, domainId=domain_id
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
                        payloadInfo=SvarProtoModule.Info(
                            fieldType=_FieldDataConstants.np_data_type_to_proto_field_type[
                                solution_variable_data.dtype.type
                            ],
                            fieldSize=solution_variable_data.size,
                            zone=zone_id,
                        )
                    )
                )
                set_data_requests += [
                    SvarProtoModule.SetSvarDataRequest(
                        payload=(
                            SvarProtoModule.Payload(
                                floatPayload=FieldDataProtoModule.FloatPayload(
                                    payload=solution_variable_data
                                )
                            )
                            if solution_variable_data.dtype.type == np.float32
                            else (
                                SvarProtoModule.Payload(
                                    doublePayload=FieldDataProtoModule.DoublePayload(
                                        payload=solution_variable_data
                                    )
                                )
                                if solution_variable_data.dtype.type == np.float64
                                else (
                                    SvarProtoModule.Payload(
                                        intPayload=FieldDataProtoModule.IntPayload(
                                            payload=solution_variable_data
                                        )
                                    )
                                    if solution_variable_data.dtype.type == np.int32
                                    else SvarProtoModule.Payload(
                                        longPayload=FieldDataProtoModule.LongPayload(
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

            for set_data_request in set_data_requests:
                yield set_data_request

        self._service.set_data(generate_set_data_requests())

    def set_svar_data(
        self,
        svar_name: str,
        zone_names_to_svar_data: List[str],
        domain_name: str | None = "mixture",
    ) -> Data:
        """Set solution variable data."""
        warnings.warn(
            "set_svar_data is deprecated, use set_data instead",
            PyFluentDeprecationWarning,
        )
        return self.set_data(
            solution_variable_name=svar_name,
            zone_names_to_solution_variable_data=zone_names_to_svar_data,
            domain_name=domain_name,
        )
