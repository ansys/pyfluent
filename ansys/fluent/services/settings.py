"""
Wrapper to settings grpc service of Fluent
"""
from ansys.api.fluent.v0 import settings_pb2 as SettingsModule
from ansys.api.fluent.v0 import settings_pb2_grpc as SettingsGrpcModule

from typing import List, Any

trace = False
_indent = 0
def _trace(fn):
    def _fn(self, *args, **kwds):
        global _indent
        if trace:
            print (f"{' '*_indent}fn={fn.__name__}, args={args} {{")
            try:
                _indent += 1
                ret = fn(self, *args, **kwds)
            finally:
                _indent -= 1
            print (f"{' '*_indent}fn = {fn.__name__}, ret={ret} }}")
            return ret
        else:
            return fn(self, *args, **kwds)
    return _fn

def _get_request_instance_for_path(request_class, path):
    request = request_class()
    request.path_info.path = path
    request.path_info.root = 'fluent'
    return request


class SettingsService:
    """
    Service for accessing and modifying Fluent settings
    """
    def __init__(self, channel, metadata):
        self.__stub = SettingsGrpcModule.SettingsStub(channel)
        self.__metadata = metadata

    @_trace
    def _set_state_from_value(self, state, value):
        if isinstance(value, bool):
            state.boolean = value
        elif isinstance(value, int):
            state.integer = value
        elif isinstance(value, float):
            state.real = value
        elif isinstance(value, str):
            state.string = value
        elif isinstance(value, list):
            for v in value:
                self._set_state_from_value(state.value_list.lst.add(), v)
        elif isinstance(value, dict):
            for k, v in value.items():
                self._set_state_from_value(state.value_map.m[k], v)

    @_trace
    def _get_state_from_value(self, state):
        t = state.WhichOneof('value')
        if t == 'boolean':
            return state.boolean
        elif t == 'integer':
            return state.integer
        elif t == 'real':
            return state.real
        elif t == 'string':
            return state.string
        elif t == 'value_list':
            return [self._get_state_from_value(v)
                    for v in state.value_list.lst]
        elif t == 'value_map':
            return {k : self._get_state_from_value(v) for k, v in
                    state.value_map.m.items()}
        else:
            return None

    @_trace
    def set_var(self, path: str, value: Any):
        """
        Set the value for the given path
        """
        request = _get_request_instance_for_path(
                SettingsModule.SetVarRequest,
                path)
        self._set_state_from_value(request.value, value)
        self.__stub.SetVar(request, metadata=self.__metadata)

    @_trace
    def get_var(self, path: str) -> Any:
        """
        Get the value for the given path
        """
        request = _get_request_instance_for_path(
                SettingsModule.GetVarRequest,
                path)
        response = self.__stub.GetVar(request, metadata=self.__metadata)
        return self._get_state_from_value(response.value)

    @_trace
    def rename(self, path: str, new: str, old: str):
        """
        Rename the object at the given path
        """
        request = _get_request_instance_for_path(
                SettingsModule.RenameRequest,
                path)
        request.old_name = old
        request.new_name = new

        self.__stub.Rename(request, metadata=self.__metadata)

    @_trace
    def create(self, path: str, name: str):
        """
        Create a new named object child for the given path
        """
        request = _get_request_instance_for_path(
                SettingsModule.CreateRequest,
                path)
        request.name = name

        self.__stub.Create(request, metadata=self.__metadata)

    @_trace
    def delete(self, path: str, name: str):
        """
        Delete the object with the given name at the give path
        """
        request = _get_request_instance_for_path(
                SettingsModule.DeleteRequest,
                path)
        request.name = name

        self.__stub.Delete(request, metadata=self.__metadata)

    @_trace
    def get_object_names(self, path: str) -> List[int]:
        """
        Get the list of named objects
        """
        request = _get_request_instance_for_path(
                SettingsModule.GetObjectNamesRequest,
                path)
        return self.__stub.GetObjectNames(request,
                metadata=self.__metadata).names

    @_trace
    def get_list_size(self, path: str) -> int:
        """
        Get the number of elements in a list object
        """
        request = _get_request_instance_for_path(
                SettingsModule.GetListSizeRequest,
                path)
        return self.__stub.GetListSize(request,
                metata=self.__metadata).size

    @_trace
    def resize_list_object(self, path: str, size: int):
        """
        Resize a list object
        """
        request = _get_request_instance_for_path(
                SettingsModule.ResizeListObjectRequest,
                path)
        request.size = size
        return self.__stub.ResizeListObject(request,
                metadata=self.__metadata)

    @_trace
    def _extract_info(self, info):
        ret = {}
        ret['type'] = info.type
        if info.children:
            ret['children'] = { k : self._extract_info(v)
                    for k, v in info.children.items() }
        if info.commands:
            ret['commands'] = { k : self._extract_info(v)
                    for k, v in info.commands.items() }
        if info.arguments:
            ret['arguments'] = { k : self._extract_info(v)
                    for k, v in info.arguments.items() }
        if info.HasField('object_type'):
            ret['object-type'] = self._extract_info(info.object_type)
        return ret

    @_trace
    def get_obj_static_info(self):
        request = SettingsModule.GetObjectStaticInfoRequest()
        request.root = 'fluent'
        response = self.__stub.GetObjectStaticInfo(request,
                metadata=self.__metadata)

        return self._extract_info(response.info)

    @_trace
    def execute_cmd(self, path: str, command: str, **kwds) -> Any:
        """
        Execute a command of given name with the provided keyword arguments
        """
        request = _get_request_instance_for_path(
                SettingsModule.ExecuteCommandRequest,
                path)
        request.command = command
        self._set_state_from_value(request.args, kwds)

        response = self.__stub.ExecuteCommand(request,
                metadata=self.__metadata)
        return self._get_state_from_value(response.reply)
