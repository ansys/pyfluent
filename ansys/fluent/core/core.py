###
### Copyright 1987-2022 ANSYS, Inc. All Rights Reserved.
###

import os
import keyword
import grpc

from ansys.api.fluent.v0 import datamodel_pb2 as DataModelProtoModule
from ansys.api.fluent.v0 import datamodel_pb2_grpc as DataModelGrpcModule

MODULE_NAME_ALIAS = "pyfluent"
JOURNAL_FILENAME = None
DATAMODEL_SERVICE = None
CHANNEL = None

def get_datamodel_service():
    return DATAMODEL_SERVICE


def parse_server_info_file(filename: str):
    with open(filename, "rb") as f:
        lines = f.readlines()
    return (lines[0].strip(), lines[1].strip())


def convert_value_to_gvalue(val, gval):
    if isinstance(val, bool):
        gval.bool_value = val
    elif isinstance(val, int) or isinstance(val, float):
        gval.number_value = val
    elif isinstance(val, str):
        gval.string_value = val
    elif isinstance(val, list) or isinstance(val, tuple):
        # set the one_of to variant_vector_state
        gval.list_value.values.add()
        gval.list_value.values.pop()
        for item in val:
            item_gval = gval.list_value.values.add()
            convert_value_to_gvalue(item, item_gval)
    elif isinstance(val, dict):
        for k, v in val.items():
            convert_value_to_gvalue(v, gval.struct_value.fields[k])


def convert_gvalue_to_value(gval):
    if gval.HasField("bool_value"):
        return gval.bool_value
    elif gval.HasField("number_value"):
        return gval.number_value
    elif gval.HasField("string_value"):
        return gval.string_value
    elif gval.HasField("list_value"):
        val = []
        for item in gval.list_value.values:
            val.append(convert_gvalue_to_value(item))
        return val
    elif gval.HasField("struct_value"):
        val = {}
        for k, v in gval.struct_value.fields.items():
            val[k] = convert_gvalue_to_value(v)
        return val

# import_ -> import
def convert_keyword_menu(menu : str):
    return menu[:-1] if menu.endswith('_') and keyword.iskeyword(menu[:-1]) else menu

def convert_path_to_grpc_path(path):
    grpc_path = ''
    if isinstance(path, list):
        for comp in path:
            grpc_path += '/' + convert_keyword_menu(comp)
    elif isinstance(path, dict):
        for k, v in path.items():
            grpc_path += '/' + convert_keyword_menu(k)
            if v:
                grpc_path += ':' + v
    return grpc_path


def convert_path_command_pair_to_grpc_path(path, command):
    grpc_path = ''
    for comp in path:
        grpc_path += '/' + convert_keyword_menu(comp)
    return grpc_path + '/' + command


class DatamodelService:

    def __init__(self, stub, password: str):
        self.stub = stub
        self.__password = password

    def __get_metadata(self):
        return [("password", self.__password)]

    def get_attribute_value(self, request):
        return self.stub.GetAttributeValue(request, metadata=self.__get_metadata())

    def get_state(self, request):
        return self.stub.GetState(request, metadata=self.__get_metadata())

    def set_state(self, request):
        return self.stub.SetState(request, metadata=self.__get_metadata())

    def execute_command(self, request):
        return self.stub.ExecuteCommand(request, metadata=self.__get_metadata())


def start_journal(filename: str):
    global JOURNAL_FILENAME
    JOURNAL_FILENAME = filename
    if os.path.exists(filename):
        os.remove(filename)
    with open(JOURNAL_FILENAME, 'w', encoding='utf8') as f:
        f.write(f'import {__name__} as {MODULE_NAME_ALIAS}\n')


def stop_journal():
    global JOURNAL_FILENAME
    JOURNAL_FILENAME = None


def read_journal(filename: str):
    exec(open(filename, encoding='utf8').read())


class PyMenuJournaler:

    def __init__(self, path=None):
        self.pypath = ""
        if not path:
            return
        for comp in path:
            if self.pypath:
                self.pypath += "."
            if comp[1]:
                self.pypath += f'{comp[0]}[{repr(comp[1])}]'
            else:
                self.pypath += comp[0]

    def __write_to_file(self, code):
        if not JOURNAL_FILENAME:
            return
        with open(JOURNAL_FILENAME, 'a', encoding='utf8') as f:
            f.write(code)

    def journal_set_state(self, state):
        self.__write_to_file(f'{MODULE_NAME_ALIAS}.{self.pypath} = {repr(state)}\n')

    def journal_rename(self, new_name):
        self.__write_to_file(f'{MODULE_NAME_ALIAS}.{self.pypath}.rename({repr(new_name)})\n')

    def journal_delete(self, child_name):
        self.__write_to_file(f'del {MODULE_NAME_ALIAS}.{self.pypath}[{repr(child_name)}]\n')

    def journal_execute(self, args=None, kwargs=None):
        self.__write_to_file(f'{MODULE_NAME_ALIAS}.{self.pypath}(')
        first = True
        if args is not None:
            for arg in args:
                if not first:
                    self.__write_to_file(', ')
                else:
                    first = False
                self.__write_to_file(repr(arg))
        if kwargs is not None:
            for k, v in kwargs.items():
                if not first:
                    self.__write_to_file(', ')
                else:
                    first = False
                self.__write_to_file(f'{k}={repr(v)}')
        self.__write_to_file(')\n')

    def journal_global_fn_call(self, func_name, args=None, kwargs=None):
        self.__write_to_file(f'{MODULE_NAME_ALIAS}.{func_name}(')
        first = True
        if args is not None:
            for arg in args:
                if not first:
                    self.__write_to_file(', ')
                else:
                    first = False
                self.__write_to_file(repr(arg))
        if kwargs is not None:
            for k, v in kwargs.items():
                if not first:
                    self.__write_to_file(', ')
                else:
                    first = False
                self.__write_to_file(f'{k}={repr(v)}')
        self.__write_to_file(')\n')


class PyMenu:

    @staticmethod
    def is_extended_tui(path, include_unavailable=False):
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.path = path
        request.attribute = DataModelProtoModule.Attribute.CUSTOM
        request.args['is_extended_tui'] = 1
        if include_unavailable:
            request.args['include_unavailable'] = 1
        response = get_datamodel_service().get_attribute_value(request)
        return convert_gvalue_to_value(response.value)

    @staticmethod
    def is_container(path, include_unavailable=False):
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.path = path
        request.attribute = DataModelProtoModule.Attribute.DATA_TYPE
        if include_unavailable:
            request.args['include_unavailable'] = 1
        response = get_datamodel_service().get_attribute_value(request)
        return convert_gvalue_to_value(response.value) == "NamedObjectContainer"

    @staticmethod
    def get_child_names(path, include_unavailable=False):
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.path = path
        request.attribute = DataModelProtoModule.Attribute.CHILD_NAMES
        if include_unavailable:
            request.args['include_unavailable'] = 1
        response = get_datamodel_service().get_attribute_value(request)
        return convert_gvalue_to_value(response.value)

    @staticmethod
    def get_state(path):
        request = DataModelProtoModule.GetStateRequest()
        request.path = path
        response = get_datamodel_service().get_state(request)
        return convert_gvalue_to_value(response.state)

    @staticmethod
    def set_state(path, value):
        request = DataModelProtoModule.SetStateRequest()
        request.path = path
        convert_value_to_gvalue(value, request.state)
        ret = get_datamodel_service().set_state(request)
        return ret

    @staticmethod
    def execute(path, *args, **kwargs):
        request = DataModelProtoModule.ExecuteCommandRequest()
        request.path = path
        if kwargs:
            for k, v in kwargs.items():
                convert_value_to_gvalue(v, request.args.fields[k])
        else:
            convert_value_to_gvalue(args, request.args.fields['tui_args'])
        ret = get_datamodel_service().execute_command(request)
        return convert_gvalue_to_value(ret.result)

    @staticmethod
    def get_doc_string(path, include_unavailable=False):
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.path = path
        request.attribute = DataModelProtoModule.Attribute.HELP_STRING
        if include_unavailable:
            request.args['include_unavailable'] = 1
        response = get_datamodel_service().get_attribute_value(request)
        return convert_gvalue_to_value(response.value)

    @staticmethod
    def rename(path, new_name):
        request = DataModelProtoModule.SetStateRequest()
        request.path = path
        convert_value_to_gvalue(new_name, request.state.struct_value.fields['name'])
        ret = get_datamodel_service().set_state(request)
        return ret


class PyNamedObjectContainer:

    @staticmethod
    def get_child_object_names(path):
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.path = path
        request.attribute = DataModelProtoModule.Attribute.OBJECT_NAMES
        response = get_datamodel_service().get_attribute_value(request)
        return convert_gvalue_to_value(response.value)

    @staticmethod
    def set_item(path, name, value):
        request = DataModelProtoModule.SetStateRequest()
        request.path = path
        convert_value_to_gvalue(value, request.state)
        if request.state.HasField('null_value'): # creation with default value
            convert_value_to_gvalue(name, request.state.struct_value.fields['name'])
        ret = get_datamodel_service().set_state(request)
        return ret

    @staticmethod
    def del_item(path):
        request = DataModelProtoModule.SetStateRequest()
        request.path = path
        ret = get_datamodel_service().set_state(request)
        return ret


def start(server_info_file):
    global CHANNEL
    address, password = parse_server_info_file(server_info_file)
    CHANNEL = grpc.insecure_channel(address)
    datamodel_stub = DataModelGrpcModule.DataModelStub(CHANNEL)
    global DATAMODEL_SERVICE
    DATAMODEL_SERVICE = DatamodelService(datamodel_stub, password)
    PyMenuJournaler().journal_global_fn_call("start", [server_info_file])


def stop():
    if CHANNEL:
        CHANNEL.close()
    PyMenuJournaler().journal_global_fn_call("stop")
