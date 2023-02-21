"""Wrappers over FieldData gRPC service of Fluent."""
import difflib
from enum import IntEnum
from functools import partial, reduce
import pydoc
from typing import Callable, Dict, List, Optional, Tuple, Union

import grpc
import numpy as np
import math 
from ansys.api.fluent.v0 import svar_pb2 as SvarProtoModule
from ansys.api.fluent.v0 import field_data_pb2 as FieldDataProtoModule
from ansys.api.fluent.v0 import svar_pb2_grpc as SvarGrpcModule
from ansys.fluent.core.services.error_handler import catch_grpc_error
from ansys.fluent.core.services.interceptors import TracingInterceptor


def override_help_text(func, func_to_be_wrapped):
    func.__doc__ = "\n" + pydoc.text.document(func_to_be_wrapped)
    func.__name__ = func_to_be_wrapped.__qualname__
    return func


# this can be switched to False in scenarios where the field_data request inputs are
# fed by results of field_info queries, which might be true in GUI code.
validate_inputs = True


class SvarService:
    def __init__(self, channel: grpc.Channel, metadata):
        tracing_interceptor = TracingInterceptor()
        intercept_channel = grpc.intercept_channel(channel, tracing_interceptor)
        self.__stub = SvarGrpcModule.svarStub(intercept_channel)
        self.__metadata = metadata


    @catch_grpc_error
    def get_svar_data(self, request):
        return self.__stub.GetSvarData(request, metadata=self.__metadata)
        
    @catch_grpc_error
    def set_svar_data(self, request):
        return self.__stub.SetSvarData(request, metadata=self.__metadata)

    @catch_grpc_error
    def get_svars_info(self, request):
        return self.__stub.GetSvarsInfo(request, metadata=self.__metadata) 

    @catch_grpc_error
    def get_zones_info(self, request):
        return self.__stub.GetZonesInfo(request, metadata=self.__metadata)         

class SvarInfo:
    
    class _SvarsInfo:
        class _SvarInfo:
            def __init__(self, svar_info):
                self.name = svar_info.name
                self.dimension = svar_info.dimension
                self.data_type = self._get_data_type(svar_info.dataType,svar_info.bitSize)
                
            def _get_data_type(self, data_type, bit_size):
                if data_type==SvarProtoModule.DataType.INT: 
                    return np.int32 if bit_size==4 else np.int64 
                if data_type==SvarProtoModule.DataType.REAL: 
                    return np.float32 if bit_size==4 else np.float64
                    
            def __repr__(self):
              return f"name:{self.name} dimension:{self.dimension} data_type:{self.data_type}"                      
                    
        def __init__(self, svars_info):
            self._svars_info = {}
            for svar_info in svars_info:
                self._svars_info[svar_info.name] = SvarInfo._SvarsInfo._SvarInfo(svar_info) 

        def _filter(self, svars_info):
             self._svars_info = {k:v for k,v in self._svars_info.items() if k in [ svar_info.name for svar_info in svars_info]}
        
        def __getitem__(self, name):
            return self._svars_info.get(name, None)
            
        @property    
        def svars(self):
           return list(self._svars_info.keys())
             
                    
    class _ZonesInfo:
        class _ZoneInfo:
            class _PartitionInfo:
                def __init__(self, partition_info):
                    self.count = partition_info.count
                    self.start_index = partition_info.startIndex
                    self.end_index = partition_info.endIndex
                
            def __init__(self, zone_info):
                self.name = zone_info.name
                self.zone_id = zone_info.zoneId
                self.zone_type = zone_info.zoneType
                self.thread_type = zone_info.threadType
                self.partitions_info = [self._PartitionInfo(partition_info)  for partition_info in zone_info.partitionsInfo]
                
            def __repr__(self):
              partition_str = ""
              for i,partition_info in enumerate(self.partitions_info):
                  partition_str += f"\n\t{i}. {partition_info.count}[{partition_info.start_index}:{partition_info.end_index}]"
              return f"name:{self.name} zone_id:{self.zone_id} zone_type:{self.zone_type} threadType:{'Cell' if self.thread_type==SvarProtoModule.ThreadType.CELL_THREAD else 'Face'}{partition_str}"            
                   
                    
        def __init__(self, zones_info, domains_info):
            self._zones_info = {}
            self._domains_info = {}
            for zone_info in zones_info:
                self._zones_info[zone_info.name] = self._ZoneInfo(zone_info)
            for domain_info in domains_info:
                self._domains_info[domain_info.name] = domain_info.domainId            

        def __getitem__(self, name):
            return self._zones_info.get(name, None)
        
        @property         
        def zones(self):
           return list(self._zones_info.keys())
           
        @property         
        def domains(self):
           return list(self._domains_info.keys()) 

        def domain_id(self, domain_name):
            return  self._domains_info.get(domain_name,None)       

    def __init__(self, service: SvarService,):       
        self._service = service
        
    def get_svars_info(self, zone_names, domain_name: str = "mixture"):
        allowed_zone_names = _AllowedZoneNames(self)
        allowed_domain_names = _AllowedDomainNames(self)
        svars_info = None 
        for zone_name in zone_names:
            request = SvarProtoModule.GetSvarsInfoRequest(domainId=allowed_domain_names.valid_name(domain_name), zoneId=allowed_zone_names.valid_name(zone_name))
            response = self._service.get_svars_info(request)
            if svars_info is None:
                svars_info = SvarInfo._SvarsInfo(response.svarsInfo)
            else:
                svars_info._filter(response.svarsInfo)               
        return svars_info        
        

    def get_zones_info(self):
        request = SvarProtoModule.GetZonesInfoRequest()
        response = self._service.get_zones_info(request)
        return SvarInfo._ZonesInfo(response.zonesInfo, response.domainsInfo)         




def closest_allowed_names(trial_name: str, allowed_names: str) -> List[str]:
    f = partial(difflib.get_close_matches, trial_name, allowed_names)
    return f(cutoff=0.6, n=5) or f(cutoff=0.3, n=1)


def allowed_name_error_message(
    context: str, trial_name: str, allowed_values: List[str]
) -> str:
    message = f"{trial_name} is not an allowed {context} name.\n"
    matches = closest_allowed_names(trial_name, allowed_values)
    if matches:
        message += f"The most similar names are: {', '.join(matches)}."
    return message


def unavailable_field_error_message(context: str, field_name: str) -> str:
    return f"{field_name} is not a currently available {context}."



class SvarError(ValueError):
    def __init__(self, svar_name: str, allowed_values: List[str]):
        self.svar_name = svar_name
        super().__init__(
            allowed_name_error_message("svar", svar_name, allowed_values)
        )

class SvarUnavailable(RuntimeError):
    def __init__(self, svar_name: str):
        self.svar_name = svar_name
        super().__init__(unavailable_field_error_message("svar", svar_name))


class ZoneError(ValueError):
    def __init__(self, zone_name: str, allowed_values: List[str]):
        self.zone_name = zone_name
        super().__init__(
            allowed_name_error_message("zone", zone_name, allowed_values)
        )

class ZoneUnavailable(RuntimeError):
    def __init__(self, zone_name: str):
        self.zone_name = zone_name
        super().__init__(unavailable_field_error_message("zone name", zone_name))


class _AllowedNames:

    def is_valid(self, name): 
        return name in self()
        
    def is_available(self, name):
        return True
        return name in self(provide_only_available=True)        


class _AllowedSvarNames(_AllowedNames):
    def __init__(self, svar_info: SvarInfo):
        #self._svars_info = svar_info.get_svars_info()
        pass 
        
    def __call__(self, provide_only_available: bool = True) -> List[str]:
        return  self._svars_info.svars 
        

    def valid_name(self, svar_name):
        return svar_name
        if validate_inputs:
            if not self.is_valid(svar_name):
                raise SvarError(
                    svar_name=svar_name,
                    allowed_values=self(),
                )
            if not self.is_available(svar_name):
                raise SvarUnavailable(svar_name)
        return svar_name


class _AllowedZoneNames(_AllowedNames):
    def __init__(self, svar_info: SvarInfo):
        self._zones_info = svar_info.get_zones_info()

    def __call__(self) -> List[str]:
        return self._zones_info.zones               
        
    def valid_name(self, zone_name):
        if validate_inputs:
            if not self.is_valid(zone_name):
                raise ZoneError(
                    zone_name=zone_name,
                    allowed_values=self(),
                )
        return self._zones_info[zone_name].zone_id        


class _AllowedDomainNames(_AllowedNames):

    def __init__(self, svar_info: SvarInfo):
        self._zones_info = svar_info.get_zones_info()

    def __call__(self) -> List[str]:
        return self._zones_info.domains               
        
    def valid_name(self, domain_name):
        if validate_inputs:
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



class _FieldDataConstants:
    """Defines constants for Fluent field data."""

    # data mapping
    proto_field_type_to_np_data_type = {
        FieldDataProtoModule.FieldType.INT_ARRAY: np.int32,
        FieldDataProtoModule.FieldType.LONG_ARRAY: np.int64,
        FieldDataProtoModule.FieldType.FLOAT_ARRAY: np.float32,
        FieldDataProtoModule.FieldType.DOUBLE_ARRAY: np.float64,
    }
    np_data_type_to_proto_field_type = {
        np.int32: FieldDataProtoModule.FieldType.INT_ARRAY,
        np.int64: FieldDataProtoModule.FieldType.LONG_ARRAY,
        np.float32: FieldDataProtoModule.FieldType.FLOAT_ARRAY,
        np.float64: FieldDataProtoModule.FieldType.DOUBLE_ARRAY,
    }      
    chunk_size = 256 
    bytes_stream = True
    payloadTags = {
        FieldDataProtoModule.PayloadTag.OVERSET_MESH: 1,
        FieldDataProtoModule.PayloadTag.ELEMENT_LOCATION: 2,
        FieldDataProtoModule.PayloadTag.NODE_LOCATION: 4,
        FieldDataProtoModule.PayloadTag.BOUNDARY_VALUES: 8,
    }


def _get_zone_ids(
    svar_info: SvarInfo,
    allowed_zone_names,
    zone_ids: Optional[List[int]] = None,
    zone_names: Optional[List[str]] = None,
    zone_name: Optional[str] = None,
) -> List[int]:
    """Get surface ids' based on surface names or ids'.

    Parameters
    ----------
    surface_ids : List[int], optional
        List of surface IDs.
    surface_names: List[str], optional
        List of surface names.
    surface_name: str, optional
        List of surface name.

    Returns
    -------
    List[int]
    """
    if zone_ids and (zone_name or zone_names):
        raise RuntimeError("Please provide either surface names or surface ids.")
    if not zone_ids:
        zone_ids = []
        if zone_names:
            for zone_name in zone_names:
                zone_ids.extend(
                    svar_info.get_zones_info()[zone_name]["zone_id"]
                )
        elif zone_name:
            zone_ids = svar_info.get_zones_info()[
                allowed_zone_names.valid_name(zone_name)
            ]["zone_id"]
        else:
            raise RuntimeError("Please provide either surface names or surface ids.")
    return zone_ids




def extract_svars(svars_data):
    """Extracts field data via a server call."""

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

        if array.WhichOneof('array')=='payloadInfo':            
            zones_svar_data[array.payloadInfo.zone] = _extract_svar(
                _FieldDataConstants.proto_field_type_to_np_data_type[
                    array.payloadInfo.fieldType
                ],
                array.payloadInfo.fieldSize,
                svars_data,
            )
        elif array.WhichOneof('array')=='header':
            continue             
            
    return zones_svar_data


class SvarData:
    """Provides access to Fluent field data on surfaces."""
    
    class _SvarData:
    
        def __init__(self, domain_name, zone_id_name_map, svar_data):
            self._domain_name = domain_name
            self._data = {zone_id_name_map[zone_id]:zone_data   for zone_id, zone_data in svar_data.items()}
            
        @property
        def domain(self):
            return self._domain_name 
            
        @property
        def zones(self):
            return list(self._data.keys())
            
        @property
        def data(self):
            return  self._data       
            
        def __getitem__(self, name):
            return self._data.get(name, None)            

                   

    def __init__(
        self,
        service: SvarService,
        svar_info: SvarInfo,
    ):
        self._service = service
        self._svar_info = svar_info

        self._allowed_zone_names = _AllowedZoneNames(svar_info)

        self._allowed_domain_names = _AllowedDomainNames(svar_info)

        self._allowed_svar_names = _AllowedSvarNames(
            svar_info
        )
        svar_args = dict(
            zone_names=self._allowed_zone_names,
            svar_name = self._allowed_svar_names
        )
       
        self.get_svar_data = override_help_text(_SvarMethod(
            svar_accessor=self.get_svar_data,
            args_allowed_values_accessors=svar_args,
        ), self.get_svar_data)


    def get_svar_data(
        self,
        svar_name: str,               
        zone_names: List[str],
        domain_name: Optional[str] = "mixture", 
    ) -> Dict[int, np.array]:
        """Get scalar field data on a surface.

        Parameters
        ----------
        field_name : str
            Name of the scalar field.
        surface_ids : List[int], optional
            List of surface IDs for scalar field data.
        surface_name: str, optional
            Surface Name for scalar field data.
        node_value : bool, optional
            Whether to provide data for the nodal location. The default is ``True``.
            When ``False``, data is provided for the element location.
        boundary_value : bool, optional
            Whether to provide slip velocity at the wall boundaries. The default is
            ``False``. When ``True``, no slip velocity is provided.

        Returns
        -------
        Dict[int, np.array]
            Dictionary containing a map of surface IDs to the scalar field.
        """
        svars_request = SvarProtoModule.GetSvarDataRequest(
            provideBytesStream=_FieldDataConstants.bytes_stream,
            chunkSize=_FieldDataConstants.chunk_size
        )  
        svars_request.domainId = self._allowed_domain_names.valid_name(domain_name)
        svars_request.name=self._allowed_svar_names.valid_name(
            svar_name
        )    
        zone_id_name_map = {}    
        for zone_name in zone_names:
            zone_id = self._allowed_zone_names.valid_name(zone_name)
            zone_id_name_map[zone_id] = zone_name
            svars_request.zones.append(zone_id)    
       
        return SvarData._SvarData(domain_name,  zone_id_name_map, extract_svars(self._service.get_svar_data(svars_request)))
        
    def set_svar_data(
        self,
        svar_name: str,        
        zone_names_to_svar_data,
        domain_name : str = "mixture"
    ) -> Dict[int, np.array]:
        
        domain_id = self._allowed_domain_names.valid_name(domain_name)
        zone_ids_to_svar_data = {self._allowed_zone_names.valid_name(zone_name):svar_data  for zone_name,svar_data in zone_names_to_svar_data.items()}
        def generate_set_svar_data_requests():
            set_svar_data_requests = []
            
            set_svar_data_requests.append(
                SvarProtoModule.SetSvarDataRequest(
                    header = SvarProtoModule.SvarHeader(
                          name = svar_name,
                          domainId = domain_id
                    )    
                )
            )            
            
            for zone_id, svar_data in zone_ids_to_svar_data.items():
                max_array_size  = _FieldDataConstants.chunk_size/np.dtype(svar_data.dtype).itemsize
                svar_data_list = np.array_split(svar_data, math.ceil(svar_data.size/max_array_size))                                
                set_svar_data_requests.append(
                  SvarProtoModule.SetSvarDataRequest(
                    payloadInfo = SvarProtoModule.Info (
                      fieldType = _FieldDataConstants.np_data_type_to_proto_field_type[svar_data.dtype.type],
                      fieldSize = svar_data.size,
                      zone = zone_id
                    )
                  )
                )  
                set_svar_data_requests+=[
                  SvarProtoModule.SetSvarDataRequest(
                    payload = SvarProtoModule.Payload (
                      floatPayload = FieldDataProtoModule.FloatPayload (
                          payload = svar_data
                      )
                    )
                  )
                  for svar_data in svar_data_list if svar_data.size > 0
                ]
                
            for set_svar_data_request in set_svar_data_requests:              
                yield set_svar_data_request              

   
      
        return self._service.set_svar_data(generate_set_svar_data_requests())