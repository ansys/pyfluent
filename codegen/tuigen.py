import os
from pathlib import Path
import keyword
from ansys.fluent.core.core import (
    convertPathToGrpcPath,
    PyMenu,
    start
)


this_file = os.path.dirname(__file__)
tui_file = os.path.join(this_file, "..", "ansys", "fluent", "solver", "tui.py")
init_file = os.path.join(this_file, "..", "ansys", "fluent", "solver", "__init__.py")
indent_step = 4


class TUIMenuGenerator:
    def __init__(self, path):
        self.path = path
        self.grpcPath = convertPathToGrpcPath(path)

    def getChildNames(self):
        return PyMenu.getChildNames(self.grpcPath, True)

    def getDocString(self):
        return PyMenu.getDocString(self.grpcPath, True)


class TUIMenu:
    def __init__(self, path):
        self.path = path
        self.name = ''
        if path:
            self.name = path[-1]
            if keyword.iskeyword(self.name):
                # "import" -> "import_"
                self.name = self.name + '_'
        self.doc = None
        self.children = {}
        self.isMethod = False

class TUIGenerator:
    def __init__(self, serverInfoFile, tuiFile=tui_file, initFile=init_file):
        self.tuiFile = tui_file
        self.initFile = init_file
        Path(tui_file).unlink(missing_ok=True)
        Path(init_file).unlink(missing_ok=True)
        start(serverInfoFile)
        self.mainMenu = TUIMenu([])

    def populateMenu(self, menu : TUIMenu):
        menugen = TUIMenuGenerator(menu.path)
        menu.doc = menugen.getDocString()
        childNames = menugen.getChildNames()
        #if childNames and len(menu.path) <= 3:
        if childNames:
            for childName in childNames:
                if childName:
                    childMenu = TUIMenu(menu.path + [childName])
                    menu.children[childMenu.name] = childMenu
                    self.populateMenu(childMenu)
        else:
            menu.isMethod = True

    def writeCodeToTUIFile(self, code, indent=0):
        with open(self.tuiFile, 'a') as f:
            f.write(' ' * indent_step * indent + code)

    def writeCodeToInitFile(self, code, indent=0):
        with open(self.initFile, 'a') as f:
            f.write(' ' * indent_step * indent + code)

    def writeMenuToTUIFile(self, menu : TUIMenu, indent=0):
        if menu.name:
            self.writeCodeToTUIFile('\n')
            self.writeCodeToTUIFile('class {}(metaclass=PyMenuMeta):\n'.format(menu.name), indent)
            indent += 1
            self.writeCodeToTUIFile('__doc__ = {}\n'.format(repr(menu.doc)), indent)
        methodNames = [k for k, v in menu.children.items() if v.isMethod]
        if methodNames:
            self.writeCodeToTUIFile('doc_by_method = {\n', indent)
            indent += 1
            for methodName in methodNames:
                self.writeCodeToTUIFile("'{}' : {},\n".format(methodName, repr(menu.children[methodName].doc)), indent)
            indent -= 1
            self.writeCodeToTUIFile('}\n', indent)
        for k, v in menu.children.items():
            if not v.isMethod:
                self.writeMenuToTUIFile(v, indent)

    def generate(self):
        self.populateMenu(self.mainMenu)
        self.writeCodeToTUIFile('# This is an auto-generated file.  DO NOT EDIT!\n\n')
        self.writeCodeToTUIFile('from ansys.fluent.solver.meta import PyMenuMeta\n\n\n')
        self.writeMenuToTUIFile(self.mainMenu)

        self.writeCodeToInitFile('# This is an auto-generated file.  DO NOT EDIT!\n\n')
        self.writeCodeToInitFile('from ansys.fluent.core.core import (\n')
        self.writeCodeToInitFile('    start,\n')
        self.writeCodeToInitFile('    stop\n')
        self.writeCodeToInitFile(')\n\n')
        self.writeCodeToInitFile('from ansys.fluent.solver.tui import (\n')
        for k, v in self.mainMenu.children.items():
            if not v.isMethod:
                self.writeCodeToInitFile('    {},\n'.format(k))
        self.writeCodeToInitFile(')\n')
