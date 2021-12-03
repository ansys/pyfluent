import os
from pathlib import Path
import keyword
from ansys.fluent.core.core import (
    convert_path_to_grpc_path,
    PyMenu,
    start
)


THIS_FILE = os.path.dirname(__file__)
TUI_FILE = os.path.join(THIS_FILE, "..", "ansys", "fluent", "solver", "tui.py")
INIT_FILE = os.path.join(THIS_FILE, "..", "ansys", "fluent", "solver", "__init__.py")
INDENT_STEP = 4


class TUIMenuGenerator:

    def __init__(self, path):
        self.path = path
        self.grpc_path = convert_path_to_grpc_path(path)

    def get_child_names(self):
        return PyMenu.get_child_names(self.grpc_path, True)

    def get_doc_string(self):
        return PyMenu.get_doc_string(self.grpc_path, True)

    def is_extended_tui(self):
        return PyMenu.is_extended_tui(self.grpc_path, True)

    def is_container(self):
        return PyMenu.is_container(self.grpc_path, True)


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
        self.is_method = False
        self.is_extended_tui = False
        self.is_container = False


class TUIGenerator:

    def __init__(self, serverInfoFile, tui_file=TUI_FILE, init_file=INIT_FILE):
        self.tui_file = TUI_FILE
        self.init_file = INIT_FILE
        Path(TUI_FILE).unlink(missing_ok=True)
        Path(INIT_FILE).unlink(missing_ok=True)
        start(serverInfoFile)
        self.main_menu = TUIMenu([])

    def __populate_menu(self, menu : TUIMenu):
        menugen = TUIMenuGenerator(menu.path)
        menu.doc = menugen.get_doc_string()
        menu.is_extended_tui = menugen.is_extended_tui()
        menu.is_container = menugen.is_container()
        childNames = menugen.get_child_names()
        #if childNames and len(menu.path) <= 3:
        if childNames:
            for child_name in childNames:
                if child_name:
                    child_menu = TUIMenu(menu.path + [child_name])
                    menu.children[child_menu.name] = child_menu
                    self.__populate_menu(child_menu)
        elif not menu.is_extended_tui:
            menu.is_method = True

    def __write_code_to_tui_file(self, code, indent=0):
        with open(self.tui_file, 'a') as f:
            f.write(' ' * INDENT_STEP * indent + code)

    def __write_code_to_init_file(self, code, indent=0):
        with open(self.init_file, 'a') as f:
            f.write(' ' * INDENT_STEP * indent + code)

    def __write_menu_to_tui_file(self, menu : TUIMenu, indent=0):
        if menu.name:
            self.__write_code_to_tui_file('\n')
            self.__write_code_to_tui_file(
                'class {}(metaclass=PyMenuMeta):\n'.format(menu.name), indent)
            indent += 1
            self.__write_code_to_tui_file('__doc__ = {}\n'.format(repr(menu.doc)), indent)
        method_names = [k for k, v in menu.children.items() if v.is_method]
        if method_names:
            self.__write_code_to_tui_file('doc_by_method = {\n', indent)
            indent += 1
            for method_name in method_names:
                self.__write_code_to_tui_file(
                    "'{}' : {},\n".format(
                        method_name, repr(menu.children[method_name].doc)), indent)
            indent -= 1
            self.__write_code_to_tui_file('}\n', indent)
        for k, v in menu.children.items():
            if not v.is_method:
                self.__write_menu_to_tui_file(v, indent)

    def __write_to_init_file(self):
        self.__write_code_to_init_file('# This is an auto-generated file.  DO NOT EDIT!\n\n')
        self.__write_code_to_init_file('from ansys.fluent.core.core import (\n')
        self.__write_code_to_init_file('    start,\n')
        self.__write_code_to_init_file('    stop\n')
        self.__write_code_to_init_file(')\n\n')
        self.__write_code_to_init_file('from ansys.fluent.solver.tui import (\n')
        for k, v in self.main_menu.children.items():
            if not v.is_method:
                self.__write_code_to_init_file('    {},\n'.format(k))
        self.__write_code_to_init_file(')\n')

    def generate(self):
        self.__populate_menu(self.main_menu)
        self.__write_code_to_tui_file('# This is an auto-generated file.  DO NOT EDIT!\n\n')
        self.__write_code_to_tui_file('from ansys.fluent.solver.meta import PyMenuMeta\n\n\n')
        self.__write_menu_to_tui_file(self.main_menu)
        self.__write_to_init_file()
