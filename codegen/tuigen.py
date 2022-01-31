"""Usage:
from codegen.tuigen import TUIGenerator
TUIGenerator().generate()
"""

import os
from pathlib import Path

from ansys.fluent.services.datamodel_tui import (
    PyMenu,
    convert_path_to_grpc_path,
    convert_tui_menu_to_func_name,
)
from ansys.fluent.launcher.launcher import launch_fluent

THIS_DIRNAME = os.path.dirname(__file__)
TUI_FILE = os.path.normpath(os.path.join(
    THIS_DIRNAME, "..", "ansys", "fluent", "solver", "tui.py"))
INIT_FILE = os.path.normpath(os.path.join(
    THIS_DIRNAME, "..", "ansys", "fluent", "solver", "__init__.py")
)
INDENT_STEP = 4


class TUIMenuGenerator:
    def __init__(self, path, service):
        self.path = path
        self.grpc_path = convert_path_to_grpc_path(path)
        self.service = service

    def get_child_names(self):
        return PyMenu(self.service).get_child_names(self.grpc_path, True)

    def get_doc_string(self):
        return PyMenu(self.service).get_doc_string(self.grpc_path, True)

    def is_extended_tui(self):
        return PyMenu(self.service).is_extended_tui(self.grpc_path, True)

    def is_container(self):
        return PyMenu(self.service).is_container(self.grpc_path, True)


class TUIMenu:
    def __init__(self, path):
        self.path = path
        self.name = convert_tui_menu_to_func_name(path[-1][0]) if path else ""
        self.grpc_path = convert_path_to_grpc_path(path)
        self.doc = None
        self.children = {}
        self.is_command = False
        self.is_extended_tui = False
        self.is_container = False

    def get_command_path(self, command):
        return convert_path_to_grpc_path(self.path + [(command, None)])


class TUIGenerator:
    def __init__(self, tui_file=TUI_FILE, init_file=INIT_FILE):
        self.tui_file = tui_file
        self.init_file = init_file
        if Path(TUI_FILE).exists():
            Path(TUI_FILE).unlink()
        if Path(INIT_FILE).exists():
            Path(INIT_FILE).unlink()
        self.session = launch_fluent()
        self.service = self.session._Session__datamodel_service_tui
        self.main_menu = TUIMenu([])

    def __populate_menu(self, menu: TUIMenu):
        menugen = TUIMenuGenerator(menu.path, self.service)
        menu.doc = menugen.get_doc_string()
        menu.is_extended_tui = menugen.is_extended_tui()
        menu.is_container = menugen.is_container()
        child_names = menugen.get_child_names()
        # if child_names and (not menu.path or menu.path[0] == 'results'):
        if child_names:
            for child_name in child_names:
                if child_name:
                    child_menu = TUIMenu(menu.path + [(child_name, None)])
                    menu.children[child_menu.name] = child_menu
                    self.__populate_menu(child_menu)
        elif not menu.is_extended_tui:
            menu.is_command = True

    def __write_code_to_tui_file(self, code, indent=0):
        with open(self.tui_file, "a", encoding="utf8") as f:
            f.write(" " * INDENT_STEP * indent + code)

    def __write_code_to_init_file(self, code, indent=0):
        with open(self.init_file, "a", encoding="utf8") as f:
            f.write(" " * INDENT_STEP * indent + code)

    def __write_menu_to_tui_file(self, menu: TUIMenu, indent=0):
        if menu.name:
            self.__write_code_to_tui_file("\n")
            if menu.is_container:
                self.__write_code_to_tui_file(
                    f"class {menu.name}(metaclass=PyNamedObjectMeta):\n",
                    indent,
                )
            else:
                self.__write_code_to_tui_file(
                    f"class {menu.name}(metaclass=PyMenuMeta):\n", indent
                )
            indent += 1
            self.__write_code_to_tui_file(
                f"__doc__ = {repr(menu.doc)}\n", indent
            )
            if menu.is_extended_tui:
                self.__write_code_to_tui_file(
                    "is_extended_tui = True\n", indent
                )
        command_names = [k for k, v in menu.children.items() if v.is_command]
        if command_names:
            for command in command_names:
                self.__write_code_to_tui_file(
                    f"def {command}(self, *args, **kwargs):\n", indent
                )
                indent += 1
                self.__write_code_to_tui_file('"""\n', indent)
                doc_lines = menu.children[command].doc.splitlines()
                for line in doc_lines:
                    self.__write_code_to_tui_file(f"{line}\n", indent)
                self.__write_code_to_tui_file('"""\n', indent)
                self.__write_code_to_tui_file(
                    f"return PyMenu(self.service).execute("
                    f"'{menu.get_command_path(command)}', *args, **kwargs)\n",
                    indent,
                )
                indent -= 1
        for _, v in menu.children.items():
            if not v.is_command:
                self.__write_menu_to_tui_file(v, indent)

    def __write_to_init_file(self):
        self.__write_code_to_init_file(
            "\"\"\"\n"
            "This is an auto-generated file.  DO NOT EDIT!\n"
            "\"\"\"\n\n"
            "from ansys.fluent.session import Session\n"
            "from ansys.fluent.launcher.launcher import launch_fluent\n\n"
            "from ansys.fluent.solver import tui\n"
            "from ansys.fluent.solver.tui import (\n"
        )
        for k, v in self.main_menu.children.items():
            if not v.is_command:
                self.__write_code_to_init_file(f"{k},\n", 1)
        self.__write_code_to_init_file(
            ")\n\n"
            "from ansys.fluent.solver.logging import (\n"
            "    set_log_level,\n"
            "    enable_logging_to_stdout,\n"
            "    disable_logging_to_stdout,\n"
            "    enable_logging_to_file,\n"
            "    disable_logging_to_file,\n"
            ")\n\n\n"
            "Session.Tui.register_module(tui)\n\n"
        )

    def generate(self):
        self.__populate_menu(self.main_menu)
        self.__write_code_to_tui_file(
            "\"\"\"\n"
            "This is an auto-generated file.  DO NOT EDIT!\n"
            "\"\"\"\n"
            "# pylint: disable=line-too-long\n\n"
            "from ansys.fluent.solver.meta "
            "import PyMenuMeta, PyNamedObjectMeta\n"
            "from ansys.fluent.services.datamodel_tui import PyMenu\n\n\n"
        )
        self.__write_menu_to_tui_file(self.main_menu)
        self.__write_to_init_file()
        self.session.exit()

if __name__ == "__main__":
    TUIGenerator().generate()
