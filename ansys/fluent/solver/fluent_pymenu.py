###
### Copyright 1987-2022 ANSYS, Inc. All Rights Reserved.
###

import grpc
import os

from ansys.api.fluent.v0 import datamodel_pb2 as DataModelProtoModule
from ansys.api.fluent.v0 import datamodel_pb2_grpc as DataModelGrpcModule


def parseServerInfoFile(filename: str):
    with open(filename, "rb") as f:
        lines = f.readlines()
    return (lines[0].strip(), lines[1].strip())


def convertValueToGValue(val, gVal):
    if isinstance(val, bool):
        gVal.bool_value = val
    elif isinstance(val, int) or isinstance(val, float):
        gVal.number_value = val
    elif isinstance(val, str):
        gVal.string_value = val
    elif isinstance(val, list) or isinstance(val, tuple):
        # set the one_of to variant_vector_state
        gVal.list_value.values.add()
        gVal.list_value.values.pop()
        for item in val:
            itemGVal= gVal.list_value.values.add()
            convertValueToGValue(item, itemGVal)
    elif isinstance(val, dict):
        for k, v in val.items():
            convertValueToGValue(v, gVal.struct_value.fields[k])


def convertGValueToValue(gVal):
    if gVal.HasField("bool_value"):
        return gVal.bool_value
    elif gVal.HasField("number_value"):
        return gVal.number_value
    elif gVal.HasField("string_value"):
        return gVal.string_value
    elif gVal.HasField("list_value"):
        val = []
        for item in gVal.list_value.values:
            val.append(convertGValueToValue(item))
        return val
    elif gVal.HasField("struct_value"):
        val = {}
        for k, v in gVal.struct_value.fields.items():
            val[k] = convertGValueToValue(v)
        return val


def convertPathToGrpcPath(path):
    grpcPath = ""
    for comp in path:
        grpcPath += "/" + comp[0]
        if comp[1]:
            grpcPath += ":" + comp[1]
    return grpcPath


class DataModelService:
    def __init__(self, stub, password: str):
        self.stub = stub
        self.__password = password

    def __getMetaData(self):
        return [("password", self.__password)]

    def getAttributeValue(self, request):
        return self.stub.GetAttributeValue(request, metadata=self.__getMetaData())

    def getState(self, request):
        return self.stub.GetState(request, metadata=self.__getMetaData())

    def setState(self, request):
        return self.stub.SetState(request, metadata=self.__getMetaData())

    def executeCommand(self, request):
        return self.stub.ExecuteCommand(request, metadata=self.__getMetaData())


journalFilename = None
moduleNameAlias = "fluent"


def startJournal(filename: str):
    global journalFilename
    journalFilename = filename
    if os.path.exists(filename):
        os.remove(filename)
    with open(journalFilename, "w") as f:
        f.write("import {} as {}\n".format(__name__, moduleNameAlias))


def stopJournal():
    global journalFilename
    journalFilename = None


def readJournal(filename: str):
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

    def journalSetState(self, state):
        if not journalFilename:
            return
        with open(journalFilename, "a") as f:
            f.write("{}.{} = {}\n".format(moduleNameAlias, self.pypath, repr(state)))

    def journalRename(self, newName):
        if not journalFilename:
            return
        with open(journalFilename, "a") as f:
            f.write(
                "{}.{}.rename({})\n".format(moduleNameAlias, self.pypath, repr(newName))
            )

    def journalDelete(self, childName):
        if not journalFilename:
            return
        with open(journalFilename, "a") as f:
            f.write(
                "del {}.{}[{}]\n".format(moduleNameAlias, self.pypath, repr(childName))
            )

    def journalExecute(self, args=None, kwargs=None):
        if not journalFilename:
            return
        with open(journalFilename, "a") as f:
            f.write("{}.{}(".format(moduleNameAlias, self.pypath))
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

    def journalGlobalFnCall(self, funcName, args=None, kwargs=None):
        if not journalFilename:
            return
        with open(journalFilename, "a") as f:
            f.write("{}.{}(".format(moduleNameAlias, funcName))
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
    members = [
        "service",
        "path",
        "grpcPath",
        "children",
        "parent",
        "journaler",
        "DataModelProtoModule",
    ]  # better alternative?

    def __init__(self, service: DataModelService, path, parent=None):
        self.service = service
        self.path = path
        self.grpcPath = convertPathToGrpcPath(path)
        self.children = {}
        self.parent = parent
        self.journaler = PyMenuJournaler(path)

    def isExtendedTUIMenu(self):  # can be cached
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.path = self.grpcPath
        request.attribute = DataModelProtoModule.Attribute.CUSTOM
        request.args['is_extended_tui'] = 1
        response = self.service.getAttributeValue(request)
        return convertGValueToValue(response.value)

    def isChildContainer(self, childName):
        childPath = list(self.path)
        childPath.append((childName, ""))
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.path = convertPathToGrpcPath(childPath)
        request.attribute = DataModelProtoModule.Attribute.DATA_TYPE
        response = self.service.getAttributeValue(request)
        return convertGValueToValue(response.value) == "NamedObjectContainer"

    def getChildNames(self):
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.path = self.grpcPath
        request.attribute = DataModelProtoModule.Attribute.CHILD_NAMES
        response = self.service.getAttributeValue(request)
        return convertGValueToValue(response.value)

    def __dir__(self):
        return self.getChildNames()

    def __getattr__(self, name):
        if name in PyMenu.members:
            super().__getattr__(name)
        elif name in self.getChildNames():
            if name not in self.children:
                childPath = list(self.path)
                childPath.append([name, ""])
                if self.isChildContainer(name):
                    self.children[name] = PyNamedObjectContainer(
                        self.service, childPath, self
                    )
                else:
                    self.children[name] = PyMenu(self.service, childPath, self)
            return self.children[name]
        else:
            raise AttributeError(name + " is not available")

    def __setattr__(self, name, value):
        if name in PyMenu.members:
            super().__setattr__(name, value)
        elif name in self.getChildNames():
            child = getattr(self, name)
            request = DataModelProtoModule.SetStateRequest()
            request.path = child.grpcPath
            convertValueToGValue(value, request.state)
            ret = child.service.setState(request)
            child.journaler.journalSetState(value)
            return ret
        else:
            raise AttributeError(name + " is not available")

    def __call__(self, *args, **kwargs):
        if kwargs:
            request = DataModelProtoModule.ExecuteCommandRequest()
            request.path = self.grpcPath
            for k, v in kwargs.items():
                convertValueToGValue(v, request.args.fields[k])
            ret = self.service.executeCommand(request)
            self.journaler.journalExecute(args, kwargs)
            return convertGValueToValue(ret.result)
        elif self.isExtendedTUIMenu():
            request = DataModelProtoModule.GetStateRequest()
            request.path = self.grpcPath
            response = self.service.getState(request)
            return convertGValueToValue(response.state)
        else:
            request = DataModelProtoModule.ExecuteCommandRequest()
            request.path = self.grpcPath
            convertValueToGValue(args, request.args.fields['tui_args'])
            ret = self.service.executeCommand(request)
            self.journaler.journalExecute(args, kwargs)
            return convertGValueToValue(ret.result)

    def help(self):
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.path = self.grpcPath
        request.attribute = DataModelProtoModule.Attribute.HELP_STRING
        response = self.service.getAttributeValue(request)
        return convertGValueToValue(response.value)

    def rename(self, newName):
        raise NotImplementedError("setState is not implemented!")
        """
        oldName = self.path[-1][1]
        request = DataModelProtoModule.RenameRequest()
        request.name = newName
        request.path = self.grpcPath
        response = self.service.rename(request)
        self.parent.children[newName] = self.parent.children.pop(oldName)
        self.journaler.journalRename(newName)
        """


class PyNamedObjectContainer(PyMenu):
    def __init__(self, service: DataModelService, path, parent):
        PyMenu.__init__(self, service, path, parent)

    def getChildObjectNames(self):
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.path = self.grpcPath
        request.attribute = DataModelProtoModule.Attribute.OBJECT_NAMES
        response = self.service.getAttributeValue(request)
        return convertGValueToValue(response.value)

    def __getattr__(self, name):
        if name in PyMenu.members:
            super().__getattr__(name)
        else:
            raise AttributeError(name + " is not available")

    def __setattr__(self, name, value):
        if name in PyMenu.members:
            super().__setattr__(name, value)
        else:
            raise AttributeError(name + " is not available")

    def __getitem__(self, name):
        if name not in self.children:
            childPath = list(self.path)
            childPath[-1][1] = name
            self.children[name] = PyMenu(self.service, childPath, self)
        return self.children[name]

    def __setitem__(self, name, value):
        child = self.__getitem__(name)
        request = DataModelProtoModule.SetStateRequest()
        request.path = child.grpcPath
        convertValueToGValue(value, request.state)
        ret = child.service.setState(request)
        child.journaler.journalSetState(value)
        return ret

    def __delitem__(self, name):
        raise NotImplementedError("Container level API methods are not implemented!")
        """
        request = DataModelProtoModule.DeleteRequest()
        request.path = self.grpcPath
        self.service.delete(request)
        del self.children[name]
        self.journaler.journalDelete(name)
        """

    def __call__(self, *args, **kwargs):
        request = DataModelProtoModule.GetStateRequest()
        convertPathToGrpcPath(self.path, request.path)
        response = self.service.getState(request)
        ret = convertGValueToValue(response.state)
        return ret


channel = None

def start(serverInfoFile):
    global channel, transcriptThread
    address, password = parseServerInfoFile(serverInfoFile)
    channel = grpc.insecure_channel(address)
    dataModelStub = DataModelGrpcModule.DataModelStub(channel)
    dataModelService = DataModelService(dataModelStub, password)
    mainMenu = PyMenu(dataModelService, [])
    for subMenu in dir(mainMenu):
        globals()[subMenu] = getattr(mainMenu, subMenu)
    PyMenuJournaler().journalGlobalFnCall("start", [serverInfoFile])


def stop():
    if channel:
        channel.close()
    PyMenuJournaler().journalGlobalFnCall("stop")
