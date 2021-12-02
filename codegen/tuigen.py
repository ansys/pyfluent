import os
from pathlib import Path
from ansys.api.fluent.v0 import datamodel_pb2 as DataModelProtoModule
from ansys.fluent.core.core import (
    convertPathToGrpcPath,
    convertGValueToValue,
    getDataModelService,
    start
)


this_file = os.path.dirname(__file__)
tui_file = os.path.join(this_file, "..", "ansys", "fluent", "solver", "tui.py")
indent_step = 4


class TUIMenuGenerator:
    def __init__(self, path):
        self.path = path
        self.grpcPath = convertPathToGrpcPath(path)

    def getAllChildNames(self):
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.path = self.grpcPath
        print(request.path)
        request.attribute = DataModelProtoModule.Attribute.CHILD_NAMES
        request.args['include_unavailable'] = 1
        response = getDataModelService().getAttributeValue(request)
        return convertGValueToValue(response.value)

    def getDocString(self):
        request = DataModelProtoModule.GetAttributeValueRequest()
        request.path = self.grpcPath
        request.attribute = DataModelProtoModule.Attribute.HELP_STRING
        request.args['include_unavailable'] = 1
        response = getDataModelService().getAttributeValue(request)
        self._helpString = convertGValueToValue(response.value)
        return self._helpString


class TUIMenu:
    def __init__(self, path):
        self.path = path
        self.name = path[-1] if path else ''
        self.doc = None
        self.children = {}
        self.isMethod = False


class TUIGenerator:
    def __init__(self, serverInfoFile, outFile=tui_file):
        self.outFile = outFile
        Path(outFile).unlink(missing_ok=True)
        start(serverInfoFile)
        self.mainMenu = TUIMenu([])

    def populateMenu(self, menu : TUIMenu):
        menugen = TUIMenuGenerator(menu.path)
        menu.doc = menugen.getDocString()
        childNames = menugen.getAllChildNames()
        if childNames and len(menu.path) <= 3:
            for childName in childNames:
                if childName:
                    childMenu = TUIMenu(menu.path + [childName])
                    menu.children[childName] = childMenu
                    self.populateMenu(childMenu)
        else:
            menu.isMethod = True

    def writeCodeToFile(self, code, indent=0):
        with open(self.outFile, 'a') as f:
            f.write(' ' * indent_step * indent + code)

    def writeMenuToFile(self, menu : TUIMenu, indent=0):
        if menu.name:
            self.writeCodeToFile('class {}(metaclass=PyMenuMeta):\n'.format(menu.name), indent)
            indent += 1
            self.writeCodeToFile('"""{}"""\n'.format(menu.doc), indent)
        methodNames = [k for k, v in menu.children.items() if v.isMethod]
        if methodNames:
            self.writeCodeToFile('doc_by_method = {\n', indent)
            indent += 1
            for methodName in methodNames:
                self.writeCodeToFile("'{}' : '{}',\n".format(methodName, menu.children[methodName].doc), indent)
            indent -= 1
            self.writeCodeToFile('}\n', indent)
        for k, v in menu.children.items():
            if not v.isMethod:
                self.writeMenuToFile(v, indent)

    def generate(self):
        self.populateMenu(self.mainMenu)
        self.writeCodeToFile('# This is an auto-generated file.  DO NOT EDIT!\n\n')
        self.writeCodeToFile('from ansys.fluent.solver.meta import PyMenuMeta\n\n\n')
        self.writeMenuToFile(self.mainMenu)

