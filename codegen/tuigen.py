"""Provide a module to generate explicit Fluent TUI menu classes.

This module starts up Fluent and calls the underlying gRPC APIs to generate the
following TUI Python modules:

- ansys/fluent/core/solver/tui.py
- ansys/fluent/core/meshing/tui.py.

Usage
-----

`python codegen/tuigen.py`
"""

import os
from pathlib import Path

from ansys.fluent.core.launcher.launcher import launch_fluent
from ansys.fluent.core.services.datamodel_tui import (
    PyMenu,
    convert_path_to_grpc_path,
    convert_tui_menu_to_func_name,
)

_THIS_DIRNAME = os.path.dirname(__file__)
_MESHING_TUI_FILE = os.path.normpath(
    os.path.join(
        _THIS_DIRNAME, "..", "ansys", "fluent", "core", "meshing", "tui.py"
    )
)
_SOLVER_TUI_FILE = os.path.normpath(
    os.path.join(
        _THIS_DIRNAME, "..", "ansys", "fluent", "core", "solver", "tui.py"
    )
)
_INDENT_STEP = 4


class _TUIMenuGenerator:
    """Wrapper over PyMenu to extract TUI menu metadata from Fluent."""

    def __init__(self, path, service):
        self._menu = PyMenu(service, path)

    def get_child_names(self):
        return self._menu.get_child_names(True)

    def get_doc_string(self):
        return self._menu.get_doc_string(True)

    def is_extended_tui(self):
        return self._menu.is_extended_tui(True)

    def is_container(self):
        return self._menu.is_container(True)


class _TUIMenu:
    """Class representing Fluent's TUI menu."""

    def __init__(self, path):
        self.path = path
        self.name = convert_tui_menu_to_func_name(path[-1][0]) if path else ""
        self.doc = None
        self.children = {}
        self.is_command = False
        self.is_extended_tui = False
        self.is_container = False

    def get_command_path(self, command):
        return convert_path_to_grpc_path(self.path + [(command, None)])


class TUIGenerator:
    """Class to generate explicit TUI menu classes."""

    def __init__(
        self,
        meshing_tui_file=_MESHING_TUI_FILE,
        solver_tui_file=_SOLVER_TUI_FILE,
        meshing=False,
    ):
        self._tui_file = meshing_tui_file if meshing else solver_tui_file
        if Path(self._tui_file).exists():
            Path(self._tui_file).unlink()
        self._session = launch_fluent(meshing_mode=meshing)
        self._service = self._session._datamodel_service_tui
        self._main_menu = _TUIMenu([])

    def _populate_menu(self, menu: _TUIMenu):
        menugen = _TUIMenuGenerator(menu.path, self._service)
        menu.doc = menugen.get_doc_string()
        menu.is_extended_tui = menugen.is_extended_tui()
        menu.is_container = menugen.is_container()
        child_names = menugen.get_child_names()
        if child_names:
            for child_name in child_names:
                if child_name:
                    child_menu = _TUIMenu(menu.path + [(child_name, None)])
                    menu.children[child_menu.name] = child_menu
                    self._populate_menu(child_menu)
        elif not menu.is_extended_tui:
            menu.is_command = True

    def _write_code_to_tui_file(self, code, indent=0):
        self.__writer.write(" " * _INDENT_STEP * indent + code)

    def _write_menu_to_tui_file(self, menu: _TUIMenu, indent=0):
        if menu.name:
            self._write_code_to_tui_file("\n")
            if menu.is_container:
                self._write_code_to_tui_file(
                    f"class {menu.name}(metaclass=PyNamedObjectMeta):\n",
                    indent,
                )
            else:
                self._write_code_to_tui_file(
                    f"class {menu.name}(metaclass=PyMenuMeta):\n", indent
                )
            indent += 1
            self._write_code_to_tui_file('"""\n', indent)
            doc_lines = menu.doc.splitlines()
            for line in doc_lines:
                self._write_code_to_tui_file(f"{line}\n", indent)
            self._write_code_to_tui_file('"""\n', indent)
            if menu.is_extended_tui:
                self._write_code_to_tui_file(
                    "is_extended_tui = True\n", indent
                )
        command_names = [k for k, v in menu.children.items() if v.is_command]
        if command_names:
            for command in command_names:
                self._write_code_to_tui_file(
                    f"def {command}(self, *args, **kwargs):\n", indent
                )
                indent += 1
                self._write_code_to_tui_file('"""\n', indent)
                doc_lines = menu.children[command].doc.splitlines()
                for line in doc_lines:
                    self._write_code_to_tui_file(f"{line}\n", indent)
                self._write_code_to_tui_file('"""\n', indent)
                self._write_code_to_tui_file(
                    f"return PyMenu(self.service, "
                    f'"{menu.get_command_path(command)}").execute('
                    f"*args, **kwargs)\n",
                    indent,
                )
                indent -= 1
        for _, v in menu.children.items():
            if not v.is_command:
                self._write_menu_to_tui_file(v, indent)

    def generate(self):
        with open(self._tui_file, "w", encoding="utf8") as self.__writer:
            self._populate_menu(self._main_menu)
            if self._tui_file == _SOLVER_TUI_FILE:
                self._write_code_to_tui_file(
                    '"""Fluent Solver TUI Commands"""\n'
                )
            else:
                self._write_code_to_tui_file(
                    '"""Fluent Meshing TUI Commands"""\n'
                )
            self._write_code_to_tui_file(
                "#\n"
                "# This is an auto-generated file.  DO NOT EDIT!\n"
                "#\n"
                "# pylint: disable=line-too-long\n\n"
                "from ansys.fluent.core.meta "
                "import PyMenuMeta, PyNamedObjectMeta\n"
                "from ansys.fluent.core.services.datamodel_tui "
                "import PyMenu\n\n\n"
            )
            self._write_menu_to_tui_file(self._main_menu)


if __name__ == "__main__":
    TUIGenerator(meshing=True).generate()
    TUIGenerator(meshing=False).generate()
