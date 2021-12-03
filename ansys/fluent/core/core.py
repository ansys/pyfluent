###
### Copyright 1987-2022 ANSYS, Inc. All Rights Reserved.
###

import grpc
import os
import keyword

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
    for comp in path:
        if isinstance(comp, tuple):
            grpc_path += '/' + convert_keyword_menu(comp[0])
            if comp[1]:
                grpc_path += ':' + comp[1]
        elif isinstance(comp, str):
            grpc_path += '/' + convert_keyword_menu(comp)
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
    with open(JOURNAL_FILENAME, "w") as f:
        f.write("import {} as {}\n".format(__name__, MODULE_NAME_ALIAS))


def stop_journal():
    global JOURNAL_FILENAME
    JOURNAL_FILENAME = None


def read_journal(filename: str):
    exec(open(filename).read())


class PyMenuJournaler:

    def __init__(self, path=None):
        self.pypath = ""
        if not path:
            return
        for c in path:
            if self.pypath:
                self.pypath += "."
            if c[1]:
                self.pypath += "{}[{}]".format(c[0], repr(c[1]))
            else:
                self.pypath += c[0]

    def journal_set_state(self, state):
        if not JOURNAL_FILENAME:
            return
        with open(JOURNAL_FILENAME, "a") as f:
            f.write("{}.{} = {}\n".format(MODULE_NAME_ALIAS, self.pypath, repr(state)))

    def journal_rename(self, new_name):
        if not JOURNAL_FILENAME:
            return
        with open(JOURNAL_FILENAME, "a") as f:
            f.write(
                "{}.{}.rename({})\n".format(MODULE_NAME_ALIAS, self.pypath, repr(new_name))
            )

    def journal_delete(self, child_name):
        if not JOURNAL_FILENAME:
            return
        with open(JOURNAL_FILENAME, "a") as f:
            f.write(
                "del {}.{}[{}]\n".format(MODULE_NAME_ALIAS, self.pypath, repr(child_name))
            )

    def journal_execute(self, args=None, kwargs=None):
        if not JOURNAL_FILENAME:
            return
        with open(JOURNAL_FILENAME, "a") as f:
            f.write("{}.{}(".format(MODULE_NAME_ALIAS, self.pypath))
            first = True
            if args is not None:
                for arg in args:
                    if not first:
                        f.write(", ")
                    else:
                        first = False
                    f.write("{}".format(repr(arg)))
            if kwargs is not None:
                for k, v in kwargs.items():
                    if not first:
                        f.write(", ")
                    else:
                        first = False
                    f.write("{}={}".format(k, repr(v)))
            f.write(")\n")

    def journal_global_fn_call(self, funcName, args=None, kwargs=None):
        if not JOURNAL_FILENAME:
            return
        with open(JOURNAL_FILENAME, "a") as f:
            f.write("{}.{}(".format(MODULE_NAME_ALIAS, funcName))
            first = True
            if args is not None:
                for arg in args:
                    if not first:
                        f.write(", ")
                    else:
                        first = False
                    f.write("{}".format(repr(arg)))
            if kwargs is not None:
                for k, v in kwargs.items():
                    if not first:
                        f.write(", ")
                    else:
                        first = False
                    f.write("{}={}".format(k, repr(v)))
            f.write(")\n")


class PyMenu:

    @staticmethod
    def is_extended_tui(path, includeUnavailable=False):
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.path = path
        request.attribute = DataModelProtoModule.Attribute.CUSTOM
        request.args['is_extended_tui'] = 1
        if includeUnavailable:
            request.args['include_unavailable'] = 1
        response = get_datamodel_service().get_attribute_value(request)
        return convert_gvalue_to_value(response.value)

    @staticmethod
    def is_container(path, includeUnavailable=False):
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.path = path
        request.attribute = DataModelProtoModule.Attribute.DATA_TYPE
        if includeUnavailable:
            request.args['include_unavailable'] = 1
        response = get_datamodel_service().get_attribute_value(request)
        return convert_gvalue_to_value(response.value) == "NamedObjectContainer"

    @staticmethod
    def get_child_names(path, includeUnavailable=False):
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.path = path
        request.attribute = DataModelProtoModule.Attribute.CHILD_NAMES
        if includeUnavailable:
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
    def get_doc_string(path, includeUnavailable=False):
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.path = path
        request.attribute = DataModelProtoModule.Attribute.HELP_STRING
        if includeUnavailable:
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


def start(serverInfoFile):
    global CHANNEL, transcriptThread
    address, password = parse_server_info_file(serverInfoFile)
    CHANNEL = grpc.insecure_channel(address)
    dataModelStub = DataModelGrpcModule.DataModelStub(CHANNEL)
    global DATAMODEL_SERVICE
    DATAMODEL_SERVICE = DatamodelService(dataModelStub, password)
    PyMenuJournaler().journal_global_fn_call("start", [serverInfoFile])


def stop():
    if CHANNEL:
        CHANNEL.close()
    PyMenuJournaler().journal_global_fn_call("stop")
