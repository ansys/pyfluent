"""Wrappers over SVAR gRPC service of Fluent."""

import math
from typing import Dict, List, Optional

import grpc
import numpy as np

from ansys.api.fluent.v0 import field_data_pb2 as FieldDataProtoModule
from ansys.api.fluent.v0 import svar_pb2 as SvarProtoModule
from ansys.api.fluent.v0 import svar_pb2_grpc as SvarGrpcModule
from ansys.fluent.core.services.error_handler import catch_grpc_error
from ansys.fluent.core.services.field_data import (
    _FieldDataConstants,
    override_help_text,
)
from ansys.fluent.core.services.interceptors import TracingInterceptor
from ansys.fluent.core.solver.error_message import allowed_name_error_message


class SVARService:
    """SVAR service of Fluent."""

    def __init__(self, channel: grpc.Channel, metadata):
        """__init__ method of SVAR service class."""
        tracing_interceptor = TracingInterceptor()
        intercept_channel = grpc.intercept_channel(channel, tracing_interceptor)
        self.__stub = SvarGrpcModule.svarStub(intercept_channel)
        self.__metadata = metadata

    @catch_grpc_error
    def get_svar_data(self, request):
        """GetSvarData rpc of SVAR service."""
        return self.__stub.GetSvarData(request, metadata=self.__metadata)

    @catch_grpc_error
    def set_svar_data(self, request):
        """SetSvarData rpc of SVAR service."""
        return self.__stub.SetSvarData(request, metadata=self.__metadata)

    @catch_grpc_error
    def get_svars_info(self, request):
        """GetSvarsInfo rpc of SVAR service."""
        return self.__stub.GetSvarsInfo(request, metadata=self.__metadata)

    @catch_grpc_error
    def get_zones_info(self, request):
        """GetZonesInfo rpc of SVAR service."""
        return self.__stub.GetZonesInfo(request, metadata=self.__metadata)


class SVARInfo:
    """Provide access to Fluent SVARs and Zones information.

    Example
    -------

    .. code-block:: python

        >>> svar_info = solver_session.svar_info
        >>>
        >>> svars_info_wall_fluid = svar_info.get_svars_info(zone_names=['wall' , "fluid"], domain_name="mixture")
        >>> svars_info_wall_fluid.svars
        >>> ['SV_CENTROID', 'SV_D', 'SV_H', 'SV_K', 'SV_P', 'SV_T', 'SV_U', 'SV_V', 'SV_W']
        >>> svar_info_centroid = svars_info_wall_fluid['SV_CENTROID']
        >>> svar_info_centroid
        >>> name:SV_CENTROID dimension:3 field_type:<class 'numpy.float64'>
        >>>
        >>> zones_info = svar_info.get_zones_info()
        >>> zones_info.zones
        >>> ['fluid', 'wall', 'symmetry', 'pressure-outlet-7', 'velocity-inlet-6', 'velocity-inlet-5', 'default-interior']
        >>> zone_info = zones_info['wall']
        >>> zone_info
        >>> name:wall count: 3630 zone_id:3 zone_type:wall thread_type:Face

    """

    class SVARS:
        """Class containing information for multiple SVARs."""

        class SVAR:
            """Class containing information for single SVAR."""

            def __init__(self, svar_info):
                self.name = svar_info.name
                self.dimension = svar_info.dimension
                self.field_type = _FieldDataConstants.proto_field_type_to_np_data_type[
                    svar_info.fieldType
                ]

            def __repr__(self):
                return f"name:{self.name} dimension:{self.dimension} field_type:{self.field_type}"

        def __init__(self, svars_info):
            self._svars_info = {}
            for svar_info in svars_info:
                self._svars_info[svar_info.name] = SVARInfo.SVARS.SVAR(svar_info)

        def _filter(self, svars_info):
            self._svars_info = {
                k: v
                for k, v in self._svars_info.items()
                if k in [svar_info.name for svar_info in svars_info]
            }

        def __getitem__(self, name):
            return self._svars_info.get(name, None)

        @property
        def svars(self) -> List[str]:
            return list(self._svars_info.keys())

    class ZonesInfo:
        """Class containing information for multiple zones."""

        class ZoneInfo:
            """Class containing information for single zone."""

            class PartitionsInfo:
                """Class containing information for partitions."""

                def __init__(self, partition_info):
                    self.count = partition_info.count
                    self.start_index = (
                        partition_info.startIndex if self.count > 0 else 0
                    )
                    self.end_index = partition_info.endIndex if self.count > 0 else 0

            def __init__(self, zone_info):
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
                return sum(
                    [partition_info.count for partition_info in self.partitions_info]
                )

            def __repr__(self):
                partition_str = ""
                for i, partition_info in enumerate(self.partitions_info):
                    partition_str += f"\n\t{i}. {partition_info.count}[{partition_info.start_index}:{partition_info.end_index}]"
                return f"name:{self.name} count: {self.count} zone_id:{self.zone_id} zone_type:{self.zone_type} threadType:{'Cell' if self.thread_type==SvarProtoModule.ThreadType.CELL_THREAD else 'Face'}{partition_str}"

        def __init__(self, zones_info, domains_info):
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
            return list(self._zones_info.keys())

        @property
        def domains(self) -> List[str]:
            return list(self._domains_info.keys())

        def domain_id(self, domain_name) -> int:
            return self._domains_info.get(domain_name, None)

    def __init__(
        self,
        service: SVARService,
    ):
        self._service = service

    def get_svars_info(
        self, zone_names: List[str], domain_name: str = "mixture"
    ) -> SVARS:
        """Get SVARs info for zones in the domain.

        Parameters
        ----------
        zone_names : List[str]
            List of zone names.
        domain_name: str, optional
            Domain name.The default is ``mixture``.

        Returns
        -------
        SVARInfo.SVARS
            Object containing information for SVARs which are common for list of zone names.
        """

        allowed_zone_names = _AllowedZoneNames(self)
        allowed_domain_names = _AllowedDomainNames(self)
        svars_info = None
        for zone_name in zone_names:
            request = SvarProtoModule.GetSvarsInfoRequest(
                domainId=allowed_domain_names.valid_name(domain_name),
                zoneId=allowed_zone_names.valid_name(zone_name),
            )
            response = self._service.get_svars_info(request)
            if svars_info is None:
                svars_info = SVARInfo.SVARS(response.svarsInfo)
            else:
                svars_info._filter(response.svarsInfo)
        return svars_info

    def get_zones_info(self) -> ZonesInfo:
        """Get Zones info.

        Parameters
        ----------
        None

        Returns
        -------
        SVARInfo.ZonesInfo
            Object containing information for all zones.
        """
        request = SvarProtoModule.GetZonesInfoRequest()
        response = self._service.get_zones_info(request)
        return SVARInfo.ZonesInfo(response.zonesInfo, response.domainsInfo)


class SvarError(ValueError):
    """Exception class for errors in SVAR name."""

    def __init__(self, svar_name: str, allowed_values: List[str]):
        self.svar_name = svar_name
        super().__init__(allowed_name_error_message("svar", svar_name, allowed_values))


class ZoneError(ValueError):
    """Exception class for errors in Zone name."""

    def __init__(self, zone_name: str, allowed_values: List[str]):
        self.zone_name = zone_name
        super().__init__(allowed_name_error_message("zone", zone_name, allowed_values))


class _AllowedNames:
    def is_valid(self, name):
        return name in self()


class _AllowedSvarNames:
    def __init__(self, svar_info: SVARInfo):
        self._svar_info = svar_info

    def __call__(
        self, zone_names: List[str], domain_name: str = "mixture"
    ) -> List[str]:
        return self._svar_info.get_svars_info(
            zone_names=zone_names, domain_name=domain_name
        ).svars

    def is_valid(self, svar_name, zone_names: List[str], domain_name: str = "mixture"):
        return svar_name in self(zone_names=zone_names, domain_name=domain_name)

    def valid_name(
        self, svar_name, zone_names: List[str], domain_name: str = "mixture"
    ):
        if not self.is_valid(svar_name, zone_names=zone_names, domain_name=domain_name):
            raise SvarError(
                svar_name=svar_name,
                allowed_values=self(zone_names=zone_names, domain_name=domain_name),
            )
        return svar_name


class _AllowedZoneNames(_AllowedNames):
    def __init__(self, svar_info: SVARInfo):
        self._zones_info = svar_info.get_zones_info()

    def __call__(self) -> List[str]:
        return self._zones_info.zones

    def valid_name(self, zone_name):
        if not self.is_valid(zone_name):
            raise ZoneError(
                zone_name=zone_name,
                allowed_values=self(),
            )
        return self._zones_info[zone_name].zone_id


class _AllowedDomainNames(_AllowedNames):
    def __init__(self, svar_info: SVARInfo):
        self._zones_info = svar_info.get_zones_info()

    def __call__(self) -> List[str]:
        return self._zones_info.domains

    def valid_name(self, domain_name):
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
            return sorted(self._accessor())

    def __init__(self, svar_accessor, args_allowed_values_accessors):
        self._svar_accessor = svar_accessor
        for arg_name, accessor in args_allowed_values_accessors.items():
            setattr(self, arg_name, _SvarMethod._Arg(accessor))

    def __call__(self, *args, **kwargs):
        return self._svar_accessor(*args, **kwargs)


def extract_svars(svars_data):
    """Extracts SVAR data via a server call."""

    def _extract_svar(field_datatype, field_size, svars_data):
        field_arr = np.empty(field_size, dtype=field_datatype)
        field_datatype_item_size = np.dtype(field_datatype).itemsize
        index = 0
        for svar_data in svars_data:
            chunk = svar_data.payload
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
    for array in svars_data:
        if array.WhichOneof("array") == "payloadInfo":
            zones_svar_data[array.payloadInfo.zone] = _extract_svar(
                _FieldDataConstants.proto_field_type_to_np_data_type[
                    array.payloadInfo.fieldType
                ],
                array.payloadInfo.fieldSize,
                svars_data,
            )
        elif array.WhichOneof("array") == "header":
            continue

    return zones_svar_data


class SVARData:
    """Provides access to Fluent SVAR data on zones.

    Example
    -------
    .. code-block:: python
        >>>
        >>> svar_data = solver_session.svar_data
        >>>
        >>> sv_t_wall_fluid=solver_session.svar_data.get_svar_data(svar_name="SV_T", domain_name="mixture", zone_names=["fluid", "wall"])
        >>>
        >>> sv_t_wall_fluid.domain
        >>> 'mixture'
        >>>
        >>> sv_t_wall_fluid.zones
        >>> ['fluid', 'wall']
        >>>
        >>> fluid_temp = sv_t_wall_fluid['fluid']
        >>> fluid_temp.size
        >>> 13852
        >>> fluid_temp.dtype
        >>> float64
        >>> fluid_temp
        >>> array([600., 600., 600., ..., 600., 600., 600.])
        >>>
        >>> wall_temp_array = svar_data.get_array("SV_T", "wall")
        >>> fluid_temp_array =svar_data.get_array("SV_T", "fluid")
        >>> wall_temp_array[:]= 500
        >>> fluid_temp_array[:]= 600
        >>> zone_names_to_svar_data = {'wall':wall_temp_array, 'fluid':fluid_temp_array}
        >>> svar_data.set_svar_data(svar_name="SV_T", domain_name="mixture", zone_names_to_svar_data=zone_names_to_svar_data)
    """

    class Data:
        def __init__(self, domain_name, zone_id_name_map, svar_data):
            self._domain_name = domain_name
            self._data = {
                zone_id_name_map[zone_id]: zone_data
                for zone_id, zone_data in svar_data.items()
            }

        @property
        def domain(self):
            return self._domain_name

        @property
        def zones(self):
            return list(self._data.keys())

        @property
        def data(self):
            return self._data

        def __getitem__(self, name):
            return self._data.get(name, None)

    def __init__(
        self,
        service: SVARService,
        svar_info: SVARInfo,
    ):
        self._service = service
        self._svar_info = svar_info

        self._allowed_zone_names = _AllowedZoneNames(svar_info)

        self._allowed_domain_names = _AllowedDomainNames(svar_info)

        self._allowed_svar_names = _AllowedSvarNames(svar_info)
        svar_args = dict(
            zone_names=self._allowed_zone_names, svar_name=self._allowed_svar_names
        )

        self.get_svar_data = override_help_text(
            _SvarMethod(
                svar_accessor=self.get_svar_data,
                args_allowed_values_accessors=svar_args,
            ),
            self.get_svar_data,
        )

    def get_array(
        self, svar_name: str, zone_name: str, domain_name: str = "mixture"
    ) -> np.zeros:
        """Get numpy zeros array for the SVAR on a zone.

        This array can be populated  with values to set SVAR data.
        """

        zones_info = self._svar_info.get_zones_info()
        if zone_name in zones_info.zones:
            svars_info = self._svar_info.get_svars_info(
                zone_names=[zone_name], domain_name=domain_name
            )
            if svar_name in svars_info.svars:
                return np.zeros(
                    zones_info[zone_name].count * svars_info[svar_name].dimension,
                    dtype=svars_info[svar_name].field_type,
                )

    def get_svar_data(
        self,
        svar_name: str,
        zone_names: List[str],
        domain_name: Optional[str] = "mixture",
    ) -> Data:
        """Get SVAR data on zones.

        Parameters
        ----------
        svar_name : str
            Name of the SVAR.
        zone_names: List[str]
            Zone names list for SVAR data.
        domain_name : str, optional
            Domain name. The default is ``mixture``.

        Returns
        -------
        SVARData.Data
            Object containing SVAR data.
        """
        svars_request = SvarProtoModule.GetSvarDataRequest(
            provideBytesStream=_FieldDataConstants.bytes_stream,
            chunkSize=_FieldDataConstants.chunk_size,
        )
        svars_request.domainId = self._allowed_domain_names.valid_name(domain_name)
        svars_request.name = self._allowed_svar_names.valid_name(
            svar_name, zone_names, domain_name
        )
        zone_id_name_map = {}
        for zone_name in zone_names:
            zone_id = self._allowed_zone_names.valid_name(zone_name)
            zone_id_name_map[zone_id] = zone_name
            svars_request.zones.append(zone_id)

        return SVARData.Data(
            domain_name,
            zone_id_name_map,
            extract_svars(self._service.get_svar_data(svars_request)),
        )

    def set_svar_data(
        self,
        svar_name: str,
        zone_names_to_svar_data: Dict[str, np.array],
        domain_name: str = "mixture",
    ) -> None:
        """Set SVAR data on zones.

        Parameters
        ----------
        svar_name : str
            Name of the SVAR.
        zone_names_to_svar_data: Dict[str, np.array]
            Dictionary containing zone names for SVAR data.
        domain_name : str, optional
            Domain name. The default is ``mixture``.

        Returns
        -------
        None
        """
        domain_id = self._allowed_domain_names.valid_name(domain_name)
        zone_ids_to_svar_data = {
            self._allowed_zone_names.valid_name(zone_name): svar_data
            for zone_name, svar_data in zone_names_to_svar_data.items()
        }

        def generate_set_svar_data_requests():
            set_svar_data_requests = []

            set_svar_data_requests.append(
                SvarProtoModule.SetSvarDataRequest(
                    header=SvarProtoModule.SvarHeader(
                        name=svar_name, domainId=domain_id
                    )
                )
            )

            for zone_id, svar_data in zone_ids_to_svar_data.items():
                max_array_size = (
                    _FieldDataConstants.chunk_size / np.dtype(svar_data.dtype).itemsize
                )
                svar_data_list = np.array_split(
                    svar_data, math.ceil(svar_data.size / max_array_size)
                )
                set_svar_data_requests.append(
                    SvarProtoModule.SetSvarDataRequest(
                        payloadInfo=SvarProtoModule.Info(
                            fieldType=_FieldDataConstants.np_data_type_to_proto_field_type[
                                svar_data.dtype.type
                            ],
                            fieldSize=svar_data.size,
                            zone=zone_id,
                        )
                    )
                )
                set_svar_data_requests += [
                    SvarProtoModule.SetSvarDataRequest(
                        payload=SvarProtoModule.Payload(
                            floatPayload=FieldDataProtoModule.FloatPayload(
                                payload=svar_data
                            )
                        )
                        if svar_data.dtype.type == np.float32
                        else SvarProtoModule.Payload(
                            doublePayload=FieldDataProtoModule.DoublePayload(
                                payload=svar_data
                            )
                        )
                        if svar_data.dtype.type == np.float64
                        else SvarProtoModule.Payload(
                            intPayload=FieldDataProtoModule.IntPayload(
                                payload=svar_data
                            )
                        )
                        if svar_data.dtype.type == np.int32
                        else SvarProtoModule.Payload(
                            longPayload=FieldDataProtoModule.LongPayload(
                                payload=svar_data
                            )
                        )
                    )
                    for svar_data in svar_data_list
                    if svar_data.size > 0
                ]

            for set_svar_data_request in set_svar_data_requests:
                yield set_svar_data_request

        self._service.set_svar_data(generate_set_svar_data_requests())
