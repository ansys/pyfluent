"""Provide a module to generate explicit Fluent TUI menu classes.

This module starts up Fluent and calls the underlying gRPC APIs to generate the
following TUI Python modules:

- src/ansys/fluent/core/solver/tui.py
- src/ansys/fluent/core/meshing/tui.py.

Usage
-----

`python codegen/tuigen.py`
"""

import logging
import os
from pathlib import Path
import pickle
import platform
import shutil
import string
import subprocess
from typing import Any, Dict
import uuid
import xml.etree.ElementTree as ET

from data.fluent_gui_help_patch import XML_HELP_PATCH

from ansys.fluent.core import FluentMode, launch_fluent
from ansys.fluent.core.services.datamodel_tui import (
    PyMenu,
    convert_path_to_grpc_path,
    convert_tui_menu_to_func_name,
)
from ansys.fluent.core.utils.fix_doc import escape_wildcards
from ansys.fluent.core.utils.fluent_version import (
    FluentVersion,
    get_version_for_file_name,
)

logger = logging.getLogger("pyfluent.tui")

_THIS_DIRNAME = os.path.dirname(__file__)


def _get_tui_filepath(mode: str, version: str, pyfluent_path: str):
    return (
        (Path(pyfluent_path) if pyfluent_path else (Path(_THIS_DIRNAME) / ".." / "src"))
        / "ansys"
        / "fluent"
        / "core"
        / mode
        / f"tui_{version}.py"
    ).resolve()


_INDENT_STEP = 4


def _get_tui_docdir(mode: str):
    return os.path.normpath(
        os.path.join(
            _THIS_DIRNAME,
            "..",
            "doc",
            "source",
            "api",
            mode,
            f"tui",
        )
    )


_XML_HELP_FILE = os.path.normpath(
    os.path.join(_THIS_DIRNAME, "data", "fluent_gui_help.xml")
)
_XML_HELPSTRINGS = {}


def _copy_tui_help_xml_file(version: str):
    if os.getenv("PYFLUENT_LAUNCH_CONTAINER") == "1":
        image_tag = os.getenv("FLUENT_IMAGE_TAG", "v23.2.0")
        image_name = f"ghcr.io/ansys/pyfluent:{image_tag}"
        container_name = uuid.uuid4().hex
        is_linux = platform.system() == "Linux"
        subprocess.run(
            f"docker container create --name {container_name} {image_name}",
            shell=is_linux,
        )
        xml_source = f"/ansys_inc/v{version}/commonfiles/help/en-us/fluent_gui_help/fluent_gui_help.xml"
        subprocess.run(
            f"docker cp {container_name}:{xml_source} {_XML_HELP_FILE}", shell=is_linux
        )
        subprocess.run(f"docker container rm {container_name}", shell=is_linux)

    else:
        ansys_version = (
            FluentVersion.get_latest_installed()
        )  # picking up the file from the latest install location
        awp_root = os.environ[ansys_version.awp_var]
        xml_source = (
            Path(awp_root)
            / "commonfiles"
            / "help"
            / "en-us"
            / "fluent_gui_help"
            / "fluent_gui_help.xml"
        )
        if xml_source.exists():
            shutil.copy(str(xml_source), _XML_HELP_FILE)
        else:
            logger.warning("fluent_gui_help.xml is not found.")


def _populate_xml_helpstrings():
    if not Path(_XML_HELP_FILE).exists():
        return

    tree = ET.parse(_XML_HELP_FILE)
    root = tree.getroot()
    help_contents_node = root.find(".//*[@id='flu_tui_help_contents']")
    field_help_node = help_contents_node.find(".//*[@id='fluent_tui_field_help']")

    for node in field_help_node.findall("sect2"):
        id = node.get("id")
        k = node.find("h3").text
        k = k.strip().strip("/")
        path = k.split("/")
        path = [c.rstrip("?").replace("-", "_") for c in path]
        k = "/" + "/".join(path)
        patched_doc = XML_HELP_PATCH.get(id)
        if patched_doc:
            _XML_HELPSTRINGS[k] = patched_doc
        else:
            v = "".join(node.find("p").itertext())
            _XML_HELPSTRINGS[k] = v


def _is_valid_tui_menu_name(name):
    return name and not all(x in string.punctuation for x in name)


class _TUIMenu:
    """Class representing Fluent's TUI menu."""

    def __init__(self, path: str, doc: str, is_command: bool = False):
        self.path = path
        self.tui_name = path[-1] if path else ""
        self.name = convert_tui_menu_to_func_name(self.tui_name)
        self.is_command = is_command
        tui_path = convert_path_to_grpc_path(path)
        self.doc = _XML_HELPSTRINGS.get(tui_path, None)
        if self.doc:
            del _XML_HELPSTRINGS[tui_path]
        else:
            self.doc = doc
        self.doc = escape_wildcards(self.doc)
        self.doc = self.doc.strip()
        if not self.doc.endswith("."):
            self.doc = self.doc + "."
        self.children = {}

    def get_command_path(self, command: str) -> str:
        return convert_path_to_grpc_path(self.path + [command])


class TUIGenerator:
    """Class to generate explicit TUI menu classes."""

    def __init__(self, mode: str, version: str, pyfluent_path: str, sessions: dict):
        self._mode = mode
        self._version = version
        self._tui_file = _get_tui_filepath(mode, version, pyfluent_path)
        if Path(self._tui_file).exists():
            Path(self._tui_file).unlink()
        self._tui_doc_dir = _get_tui_docdir(mode)
        self._tui_heading = mode + ".tui"
        self._tui_module = "ansys.fluent.core." + self._tui_heading + f"_{version}"
        if Path(self._tui_doc_dir).exists():
            shutil.rmtree(Path(self._tui_doc_dir))
        fluent_mode = FluentMode.get_mode(mode)
        if fluent_mode not in sessions:
            sessions[fluent_mode] = launch_fluent(mode=fluent_mode)
        self.session = sessions[fluent_mode]
        self._service = self.session._datamodel_service_tui
        self._main_menu = _TUIMenu([], "")

    def _populate_menu(self, menu: _TUIMenu, info: Dict[str, Any]):
        for child_menu_name, child_menu_info in info["menus"].items():
            if _is_valid_tui_menu_name(child_menu_name):
                child_menu = _TUIMenu(
                    menu.path + [child_menu_name], child_menu_info["help"]
                )
                menu.children[child_menu.name] = child_menu
                self._populate_menu(child_menu, child_menu_info)
        for child_command_name, child_command_info in info["commands"].items():
            if _is_valid_tui_menu_name(child_command_name):
                child_menu = _TUIMenu(
                    menu.path + [child_command_name], child_command_info["help"], True
                )
                menu.children[child_menu.name] = child_menu

    def _write_code_to_tui_file(self, code: str, indent: int = 0):
        self.__writer.write(" " * _INDENT_STEP * indent + code)

    def _write_menu_to_tui_file(self, menu: _TUIMenu, indent: int = 0):
        api_tree = {}
        self._write_code_to_tui_file("\n")
        self._write_code_to_tui_file(f"class {menu.name}(TUIMenu):\n", indent)
        indent += 1
        self._write_code_to_tui_file('"""\n', indent)
        doc_lines = menu.doc.splitlines()
        for line in doc_lines:
            line = line.strip()
            if line:
                self._write_code_to_tui_file(f"{line}\n", indent)
        self._write_code_to_tui_file('"""\n', indent)
        self._write_code_to_tui_file(
            "def __init__(self, service, version, mode, path):\n", indent
        )
        indent += 1
        for k, v in menu.children.items():
            self._write_code_to_tui_file(
                f"self.{k} = self.__class__.{k}"
                f'(service, version, mode, path + ["{v.tui_name}"])\n',
                indent,
            )
        self._write_code_to_tui_file(
            "super().__init__(service, version, mode, path)\n", indent
        )
        indent -= 1

        command_names = [v.name for _, v in menu.children.items() if v.is_command]
        if command_names:
            for command in command_names:
                self._write_code_to_tui_file(f"class {command}(TUIMethod):\n", indent)
                indent += 1
                self._write_code_to_tui_file('"""\n', indent)
                doc_lines = menu.children[command].doc.splitlines()
                for line in doc_lines:
                    line = line.strip()
                    if line:
                        self._write_code_to_tui_file(f"{line}\n", indent)
                self._write_code_to_tui_file('"""\n', indent)
                indent -= 1
        for k, v in menu.children.items():
            if v.is_command:
                api_tree[k] = "Command"
                pass
            else:
                api_tree[k] = self._write_menu_to_tui_file(v, indent)
        return api_tree

    def generate(self) -> None:
        api_tree = {}
        Path(self._tui_file).parent.mkdir(exist_ok=True)
        with open(self._tui_file, "w", encoding="utf8") as self.__writer:
            if FluentVersion(self._version) == FluentVersion.v222:
                with open(
                    os.path.join(
                        _THIS_DIRNAME,
                        "data",
                        f"static_info_{self._version}_{self._mode}.pickle",
                    ),
                    "rb",
                ) as f:
                    self._main_menu = pickle.load(f)
            else:
                info = PyMenu(
                    self._service, self._version, self._mode, self._main_menu.path
                ).get_static_info()
                self._populate_menu(self._main_menu, info)
            self._write_code_to_tui_file(
                f'"""Fluent {self._mode.title().lower()} TUI commands"""\n'
            )
            self._main_menu.doc = f"Fluent {self._mode} main menu."
            self._write_code_to_tui_file(
                "#\n"
                "# This is an auto-generated file.  DO NOT EDIT!\n"
                "#\n"
                "# pylint: disable=line-too-long\n\n"
                "from ansys.fluent.core.services.datamodel_tui "
                "import PyMenu, TUIMenu, TUIMethod\n\n\n"
            )
            self._main_menu.name = "main_menu"
            api_tree["tui"] = self._write_menu_to_tui_file(self._main_menu)
        return api_tree


def generate(version, pyfluent_path, sessions: dict):
    api_tree = {}
    if FluentVersion(version) > FluentVersion.v222:
        _copy_tui_help_xml_file(version)
    _populate_xml_helpstrings()
    api_tree["<meshing_session>"] = TUIGenerator(
        "meshing", version, pyfluent_path, sessions
    ).generate()
    api_tree["<solver_session>"] = TUIGenerator(
        "solver", version, pyfluent_path, sessions
    ).generate()
    if os.getenv("PYFLUENT_HIDE_LOG_SECRETS") != "1":
        logger.info(
            "XML help is available but not picked for the following %i paths: ",
            len(_XML_HELPSTRINGS),
        )
        for k in _XML_HELPSTRINGS:
            logger.info(k)
    return api_tree


if __name__ == "__main__":
    sessions = {FluentMode.SOLVER: launch_fluent()}
    version = get_version_for_file_name(session=sessions[FluentMode.SOLVER])
    generate(version, None, sessions)
