import keyword
import os

from ansys.api.fluent.v0 import datamodel_pb2 as DataModelProtoModule
from ansys.api.fluent.v0 import fielddata_pb2 as FieldDataProtoModule

MODULE_NAME_ALIAS = "pyfluent"
JOURNAL_FILENAME = None


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
# type_flag -> type?
def convert_fname_to_tui_menu(fname: str):
    if fname.endswith("_") and keyword.iskeyword(fname[:-1]):
        return fname[:-1]
    # TODO: Following is actually done in the server-side - consolidate
    # if fname.endswith('_flag'):
    #    return fname.rstrip('_flag') + '?'
    return fname


# import -> import_
# type? -> type_flag
def convert_tui_menu_to_fname(menu: str):
    if keyword.iskeyword(menu):
        return menu + "_"
    if menu.endswith("?"):
        return menu[:-1] + "_flag"
    return menu


def convert_path_to_grpc_path(path):
    grpc_path = ""
    for comp in path:
        grpc_path += "/" + convert_fname_to_tui_menu(comp[0])
        if comp[1]:
            grpc_path += ":" + comp[1]
    return grpc_path


def extend_menu_path_to_command_path(path, command):
    return path + "/" + command


class DatamodelService:
    def __init__(self, stub, password: str):
        self.stub = stub
        self.__password = password

    def __get_metadata(self):
        return [("password", self.__password)]

    def get_attribute_value(self, request):
        return self.stub.GetAttributeValue(
            request, metadata=self.__get_metadata()
        )

    def get_state(self, request):
        return self.stub.GetState(request, metadata=self.__get_metadata())

    def set_state(self, request):
        return self.stub.SetState(request, metadata=self.__get_metadata())

    def execute_command(self, request):
        return self.stub.ExecuteCommand(
            request, metadata=self.__get_metadata()
        )

    def execute_query(self, request):
        return self.stub.ExecuteQuery(request, metadata=self.__get_metadata())


class FieldDataService:
    def __init__(self, stub, password: str):
        self.stub = stub
        self.__password = password

    def __get_metadata(self):
        return [("password", self.__password)]

    def get_surfaces(self, request):
        return self.stub.GetSurfaces(request, metadata=self.__get_metadata())

    def get_range(self, request):
        return self.stub.GetRange(request, metadata=self.__get_metadata())

    def get_scalar_field(self, request):
        return self.stub.GetScalarField(
            request, metadata=self.__get_metadata()
        )

    def get_fields_info(self, request):
        return self.stub.GetFieldsInfo(request, metadata=self.__get_metadata())

    def get_surfaces_info(self, request):
        return self.stub.GetSurfacesInfo(
            request, metadata=self.__get_metadata()
        )

def start_journal(filename: str):
    global JOURNAL_FILENAME
    JOURNAL_FILENAME = filename
    if os.path.exists(filename):
        os.remove(filename)
    with open(JOURNAL_FILENAME, "w", encoding="utf8") as f:
        f.write(f"import {__name__} as {MODULE_NAME_ALIAS}\n")


def stop_journal():
    global JOURNAL_FILENAME
    JOURNAL_FILENAME = None


def read_journal(filename: str):
    exec(open(filename, encoding="utf8").read())


class PyMenuJournaler:
    def __init__(self, path=None):
        self.pypath = ""
        if not path:
            return
        for comp in path:
            if self.pypath:
                self.pypath += "."
            if comp[1]:
                self.pypath += f"{comp[0]}[{repr(comp[1])}]"
            else:
                self.pypath += comp[0]

    def __write_to_file(self, code):
        if not JOURNAL_FILENAME:
            return
        with open(JOURNAL_FILENAME, "a", encoding="utf8") as f:
            f.write(code)

    def journal_set_state(self, state):
        self.__write_to_file(
            f"{MODULE_NAME_ALIAS}.{self.pypath} = {repr(state)}\n"
        )

    def journal_rename(self, new_name):
        self.__write_to_file(
            f"{MODULE_NAME_ALIAS}.{self.pypath}.rename({repr(new_name)})\n"
        )

    def journal_delete(self, child_name):
        self.__write_to_file(
            f"del {MODULE_NAME_ALIAS}.{self.pypath}[{repr(child_name)}]\n"
        )

    def journal_execute(self, args=None, kwargs=None):
        self.__write_to_file(f"{MODULE_NAME_ALIAS}.{self.pypath}(")
        first = True
        if args is not None:
            for arg in args:
                if not first:
                    self.__write_to_file(", ")
                else:
                    first = False
                self.__write_to_file(repr(arg))
        if kwargs is not None:
            for k, v in kwargs.items():
                if not first:
                    self.__write_to_file(", ")
                else:
                    first = False
                self.__write_to_file(f"{k}={repr(v)}")
        self.__write_to_file(")\n")

    def journal_global_fn_call(self, func_name, args=None, kwargs=None):
        self.__write_to_file(f"{MODULE_NAME_ALIAS}.{func_name}(")
        first = True
        if args is not None:
            for arg in args:
                if not first:
                    self.__write_to_file(", ")
                else:
                    first = False
                self.__write_to_file(repr(arg))
        if kwargs is not None:
            for k, v in kwargs.items():
                if not first:
                    self.__write_to_file(", ")
                else:
                    first = False
                self.__write_to_file(f"{k}={repr(v)}")
        self.__write_to_file(")\n")

class FieldData:
    def __init__(self, service):
        self.service = service

    def get_range(self, field, node_value= False, surface_ids=[]):
        request = FieldDataProtoModule.GetRangeRequest()
        request.fieldName = field
        request.nodeValue = node_value
        request.surfaceid.extend(
            [
                FieldDataProtoModule.SurfaceId(id=int(id))
                for id in surface_ids
            ]
        )
        response = self.service.get_range(request)
        return [response.minimum, response.maximum]

    def get_fields_info(self):
        request = FieldDataProtoModule.GetFieldsInfoRequest()
        response = self.service.get_fields_info(request)
        return {
            field_info.displayName: {
                "solver_name": field_info.solverName,
                "section": field_info.section,
                "domain": field_info.domain,
            }
            for field_info in response.fieldInfo
        }

    def get_surfaces_info(self):
        request = FieldDataProtoModule.GetSurfacesInfoResponse()
        response = self.service.get_surfaces_info(request)
        return {
            surface_info.surfaceName: {
                "surface_id": [
                    surf.id for surf in surface_info.surfaceId
                ],
                "zone_id": surface_info.zoneId.id,
                "zone_type": surface_info.zoneType,
                "type": surface_info.type,
            }
            for surface_info in response.surfaceInfo
        }

    def _extract_surfaces_data(self, response_iterator):
        return [
            {
                "vertices": [
                    [point.x, point.y, point.z]
                    for point in response.surfacedata.point
                ],
                "faces": [
                    [len(facet.node)] + [node for node in facet.node]
                    for facet in response.surfacedata.facet
                ],
            }
            for response in response_iterator
        ]

    def get_surfaces(self, surface_ids, overset_mesh=False):
        request = FieldDataProtoModule.GetSurfacesRequest()
        request.surfaceid.extend(
            [
                FieldDataProtoModule.SurfaceId(id=int(id))
                for id in surface_ids
            ]
        )
        request.oversetMesh = overset_mesh
        response_iterator = self.service.get_surfaces(request)
        return self._extract_surfaces_data(response_iterator)

    def _extract_scalar_field_data(self, response_iterator):
        return [
            {
                "vertices": [
                    [point.x, point.y, point.z]
                    for point in response.scalarfielddata.surfacedata.point
                ],
                "faces": [
                    [len(facet.node)] + [node for node in facet.node]
                    for facet in response.scalarfielddata.surfacedata.facet
                ],
                "scalar_field": [
                    data
                    for data in response.scalarfielddata.scalarfield.data
                ],
                "meta_data": response.scalarfielddata.scalarfieldmetadata,
            }
            for response in response_iterator
        ]

    def get_scalar_field(
        self, surface_ids, scalar_field, node_value, boundary_value
    ):
        request = FieldDataProtoModule.GetScalarFieldRequest()
        request.surfaceid.extend(
            [
                FieldDataProtoModule.SurfaceId(id=int(id))
                for id in surface_ids
            ]
        )
        request.scalarfield = scalar_field
        request.nodevalue = node_value
        request.boundaryvalues = boundary_value
        response_iterator = self.service.get_scalar_field(request)
        return self._extract_scalar_field_data(response_iterator)


class PyMenu:
    class ExecuteCommandResult:
        def __init__(self, result):
            self.result = result

    def __init__(self, service):
        self.service = service

    def is_extended_tui(self, path, include_unavailable=False):
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.path = path
        request.attribute = DataModelProtoModule.Attribute.CUSTOM
        request.args["is_extended_tui"] = 1
        if include_unavailable:
            request.args["include_unavailable"] = 1
        response = self.service.get_attribute_value(request)
        return convert_gvalue_to_value(response.value)

    def is_container(self, path, include_unavailable=False):
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.path = path
        request.attribute = DataModelProtoModule.Attribute.DATA_TYPE
        if include_unavailable:
            request.args["include_unavailable"] = 1
        response = self.service.get_attribute_value(request)
        return (
            convert_gvalue_to_value(response.value) == "NamedObjectContainer"
        )

    def get_child_names(self, path, include_unavailable=False):
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.path = path
        request.attribute = DataModelProtoModule.Attribute.CHILD_NAMES
        if include_unavailable:
            request.args["include_unavailable"] = 1
        response = self.service.get_attribute_value(request)
        return convert_gvalue_to_value(response.value)

    def get_state(self, path):
        request = DataModelProtoModule.GetStateRequest()
        request.path = path
        response = self.service.get_state(request)
        return convert_gvalue_to_value(response.state)

    def set_state(self, path, value):
        request = DataModelProtoModule.SetStateRequest()
        request.path = path
        convert_value_to_gvalue(value, request.state)
        ret = self.service.set_state(request)
        return ret

    def execute(self, path: str, *args, **kwargs):
        request = DataModelProtoModule.ExecuteCommandRequest()
        request.path = path
        if kwargs:
            for k, v in kwargs.items():
                convert_value_to_gvalue(v, request.args.fields[k])
        else:
            convert_value_to_gvalue(args, request.args.fields["tui_args"])
        if path.startswith("/query/"):
            ret = self.service.execute_query(request)
            return convert_gvalue_to_value(ret.result)
        else:
            ret = self.service.execute_command(request)
            return PyMenu.ExecuteCommandResult(
                convert_gvalue_to_value(ret.result)
            )

        ret = self.service.execute_command(request)
        return PyMenu.ExecuteCommandResult(convert_gvalue_to_value(ret.result))

    def get_doc_string(self, path, include_unavailable=False):
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.path = path
        request.attribute = DataModelProtoModule.Attribute.HELP_STRING
        if include_unavailable:
            request.args["include_unavailable"] = 1
        response = self.service.get_attribute_value(request)
        return convert_gvalue_to_value(response.value)

    def rename(self, path, new_name):
        request = DataModelProtoModule.SetStateRequest()
        request.path = path
        convert_value_to_gvalue(
            new_name, request.state.struct_value.fields["name"]
        )
        ret = self.service.set_state(request)
        return ret

    def get_child_object_names(self, path):
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.path = path
        request.attribute = DataModelProtoModule.Attribute.OBJECT_NAMES
        response = self.service.get_attribute_value(request)
        return convert_gvalue_to_value(response.value)

    def set_item(self, path, name, value):
        request = DataModelProtoModule.SetStateRequest()
        request.path = path
        convert_value_to_gvalue(value, request.state)
        if request.state.HasField("null_value"):  # creation with default value
            convert_value_to_gvalue(
                name, request.state.struct_value.fields["name"]
            )
        ret = self.service.set_state(request)
        return ret

    def del_item(self, path):
        request = DataModelProtoModule.SetStateRequest()
        request.path = path
        ret = self.service.set_state(request)
        return ret
