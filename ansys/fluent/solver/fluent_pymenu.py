###
### Copyright 1987-2022 ANSYS, Inc. All Rights Reserved.
###

import grpc
import os

from ansys.api.fluent.v1 import pymenu_pb2 as PyMenuProtoModule
from ansys.api.fluent.v1 import pymenu_pb2_grpc as PyMenuGrpcModule


def parseServerInfoFile(filename: str):
    with open(filename, "rb") as f:
        lines = f.readlines()
    return (lines[0].strip(), lines[1].strip())


def convertValueToVariant(val, var):
    if isinstance(val, bool):
        var.bool_state = val
    elif isinstance(val, int):
        var.int64_state = val
    elif isinstance(val, float):
        var.double_state = val
    elif isinstance(val, str):
        var.string_state = val
    elif isinstance(val, list):
        # set the one_of to variant_vector_state
        var.variant_vector_state.item.add()
        var.variant_vector_state.item.pop()
        for item in val:
            itemVar = var.variant_vector_state.item.add()
            convertValueToVariant(item, itemVar)
    elif isinstance(val, dict):
        for k, v in val.items():
            convertValueToVariant(v, var.variant_map_state.item[k])


def convertVariantToValue(var):
    if var.HasField("bool_state"):
        return var.bool_state
    elif var.HasField("int64_state"):
        return var.int64_state
    elif var.HasField("double_state"):
        return var.double_state
    elif var.HasField("string_state"):
        return var.string_state
    elif var.HasField("variant_vector_state"):
        val = []
        for item in var.variant_vector_state.item:
            val.append(convertVariantToValue(item))
        return val
    elif var.HasField("variant_map_state"):
        val = {}
        for key in var.variant_map_state.item:
            val[key] = convertVariantToValue(var.variant_map_state.item[key])
        return val


def convertPathToGrpcPath(path, gPath):
    for comp in path:
        gComp = gPath.components.add()
        gComp.type = comp[0]
        gComp.name = comp[1]


class PyMenuService:
    def __init__(self, stub, password: str):
        self.stub = stub
        self.__password = password

    def __getMetaData(self):
        return [("password", self.__password)]

    def getInfo(self, request):
        return self.stub.GetInfo(request, metadata=self.__getMetaData())

    def getChildNames(self, request):
        return self.stub.GetChildNames(request, metadata=self.__getMetaData())

    def getChildObjectNames(self, request):
        return self.stub.GetChildObjectNames(request, metadata=self.__getMetaData())

    def getState(self, request):
        return self.stub.GetState(request, metadata=self.__getMetaData())

    def setState(self, request):
        return self.stub.SetState(request, metadata=self.__getMetaData())

    def rename(self, request):
        return self.stub.Rename(request, metadata=self.__getMetaData())

    def delete(self, request):
        return self.stub.Delete(request, metadata=self.__getMetaData())

    def execute(self, request):
        return self.stub.Execute(request, metadata=self.__getMetaData())

    def getHelpString(self, request):
        return self.stub.GetHelpString(request, metadata=self.__getMetaData())


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
        "children",
        "parent",
        "journaler",
        "pyMenuProtoModule",
    ]  # better alternative?

    def __init__(self, service: PyMenuService, path, parent=None):
        self.service = service
        self.path = path
        self.children = {}
        self.parent = parent
        self.journaler = PyMenuJournaler(path)

    def isApiMenu(self):  # can be cached
        request = PyMenuProtoModule.GetInfoRequest()
        convertPathToGrpcPath(self.path, request.path)
        response = self.service.getInfo(request)
        return response.isapimenu

    def isChildContainer(self, childName):
        childPath = list(self.path)
        childPath.append((childName, ""))
        request = PyMenuProtoModule.GetInfoRequest()
        convertPathToGrpcPath(childPath, request.path)
        response = self.service.getInfo(request)
        return response.iscontainer

    def getChildNames(self):
        request = PyMenuProtoModule.GetChildNamesRequest()
        convertPathToGrpcPath(self.path, request.path)
        response = self.service.getChildNames(request)
        names = []
        for item in response.names:
            names.append(item)
        return names

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
            request = PyMenuProtoModule.SetStateRequest()
            convertPathToGrpcPath(child.path, request.path)
            convertValueToVariant(value, request.state)
            ret = child.service.setState(request)
            child.journaler.journalSetState(value)
            return ret
        else:
            raise AttributeError(name + " is not available")

    def __call__(self, *args, **kwargs):
        if kwargs:
            request = PyMenuProtoModule.ExecuteRequest()
            convertPathToGrpcPath(self.path, request.path)
            for k, v in kwargs.items():
                convertValueToVariant(v, request.kwargs[k])
            ret = self.service.execute(request)
            self.journaler.journalExecute(args, kwargs)
            return convertVariantToValue(ret.results)
        elif self.isApiMenu():
            request = PyMenuProtoModule.GetStateRequest()
            convertPathToGrpcPath(self.path, request.path)
            response = self.service.getState(request)
            return convertVariantToValue(response.state)
        else:
            request = PyMenuProtoModule.ExecuteRequest()
            convertPathToGrpcPath(self.path, request.path)
            for arg in args:
                gArgs = request.args.add()
                convertValueToVariant(arg, gArgs)
            ret = self.service.execute(request)
            self.journaler.journalExecute(args, kwargs)
            return convertVariantToValue(ret.results)

    def help(self):
        request = PyMenuProtoModule.GetHelpStringRequest()
        convertPathToGrpcPath(self.path, request.path)
        response = self.service.getHelpString(request)
        print(response.help)

    def rename(self, newName):
        oldName = self.path[-1][1]
        request = PyMenuProtoModule.RenameRequest()
        request.name = newName
        convertPathToGrpcPath(self.path, request.path)
        response = self.service.rename(request)
        self.parent.children[newName] = self.parent.children.pop(oldName)
        self.journaler.journalRename(newName)


class PyNamedObjectContainer(PyMenu):
    def __init__(self, service: PyMenuService, path, parent):
        PyMenu.__init__(self, service, path, parent)

    def getChildObjectNames(self):
        request = PyMenuProtoModule.GetChildObjectNamesRequest()
        convertPathToGrpcPath(self.path, request.path)
        response = self.service.getChildObjectNames(request)
        names = []
        for item in response.names:
            names.append(item)
        return names

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
        request = PyMenuProtoModule.SetStateRequest()
        convertPathToGrpcPath(child.path, request.path)
        convertValueToVariant(value, request.state)
        ret = child.service.setState(request)
        child.journaler.journalSetState(value)
        return ret

    def __delitem__(self, name):
        request = PyMenuProtoModule.DeleteRequest()
        convertPathToGrpcPath(self.path, request.path)
        self.service.delete(request)
        del self.children[name]
        self.journaler.journalDelete(name)

    def __call__(self, *args, **kwargs):
        request = PyMenuProtoModule.GetStateRequest()
        convertPathToGrpcPath(self.path, request.path)
        response = self.service.getState(request)
        ret = convertVariantToValue(response.state)
        return ret


channel = None

def start(serverInfoFile):
    global channel, transcriptThread
    address, password = parseServerInfoFile(serverInfoFile)
    channel = grpc.insecure_channel(address)
    pyMenuStub = PyMenuGrpcModule.PyMenuStub(channel)
    pyMenuService = PyMenuService(pyMenuStub, password)
    mainMenu = PyMenu(pyMenuService, [])
    for subMenu in dir(mainMenu):
        globals()[subMenu] = getattr(mainMenu, subMenu)
    PyMenuJournaler().journalGlobalFnCall("start", [serverInfoFile])


def stop():
    if channel:
        channel.close()
    PyMenuJournaler().journalGlobalFnCall("stop")
