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
from data.tui_menu_descriptions import MENU_DESCRIPTIONS

import ansys.fluent.core as pyfluent
from ansys.fluent.core.launcher.launcher import get_ansys_version
from ansys.fluent.core.services.datamodel_tui import (
    PyMenu,
    convert_path_to_grpc_path,
    convert_tui_menu_to_func_name,
)
from ansys.fluent.core.utils.fluent_version import get_version_for_filepath

logger = logging.getLogger("pyfluent.tui")

_THIS_DIRNAME = os.path.dirname(__file__)


def _get_tui_filepath(mode: str, version: str):
    return os.path.normpath(
        os.path.join(
            _THIS_DIRNAME,
            "..",
            "src",
            "ansys",
            "fluent",
            "core",
            mode,
            f"tui_{version}.py",
        )
    )


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
        image_tag = os.getenv("FLUENT_IMAGE_TAG", "v23.1.0")
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
            get_ansys_version()
        )  # picking up the file from the latest install location
        awp_root = os.environ["AWP_ROOT" + "".join(str(ansys_version).split("."))[:-1]]
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
        self.doc = self.doc.replace("\\*", "*")
        self.doc = self.doc.replace("*", "\*")
        self.doc = self.doc.strip()
        if not self.doc.endswith("."):
            self.doc = self.doc + "."
        self.children = {}

    def get_command_path(self, command: str) -> str:
        return convert_path_to_grpc_path(self.path + [command])


class TUIGenerator:
    """Class to generate explicit TUI menu classes."""

    def __init__(self, mode: str, version: str):
        self._mode = mode
        self._version = version
        self._tui_file = _get_tui_filepath(mode, version)
        if Path(self._tui_file).exists():
            Path(self._tui_file).unlink()
        self._tui_doc_dir = _get_tui_docdir(mode)
        self._tui_heading = mode + ".tui"
        self._tui_module = "ansys.fluent.core." + self._tui_heading + f"_{version}"
        if Path(self._tui_doc_dir).exists():
            shutil.rmtree(Path(self._tui_doc_dir))
        self.session = pyfluent.launch_fluent(mode=mode)
        self._service = self.session.datamodel_service_tui
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
        self._write_code_to_tui_file("def __init__(self, path, service):\n", indent)
        indent += 1
        self._write_code_to_tui_file("self.path = path\n", indent)
        self._write_code_to_tui_file("self.service = service\n", indent)
        for k, v in menu.children.items():
            if not v.is_command:
                self._write_code_to_tui_file(
                    f"self.{k} = self.__class__.{k}"
                    f'(path + ["{v.tui_name}"], service)\n',
                    indent,
                )
        self._write_code_to_tui_file("super().__init__(path, service)\n", indent)
        indent -= 1

        command_names = [v.name for _, v in menu.children.items() if v.is_command]
        if command_names:
            for command in command_names:
                self._write_code_to_tui_file(
                    f"def {command}(self, *args, **kwargs):\n", indent
                )
                indent += 1
                self._write_code_to_tui_file('"""\n', indent)
                doc_lines = menu.children[command].doc.splitlines()
                for line in doc_lines:
                    line = line.strip()
                    if line:
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

    def _write_doc_for_menu(self, menu, doc_dir: Path, heading, class_name) -> None:
        doc_dir.mkdir(exist_ok=True)
        index_file = doc_dir / "index.rst"
        with open(index_file, "w", encoding="utf8") as f:
            ref = "_ref_" + "_".join([x.strip("_") for x in heading.split(".")])
            f.write(f".. {ref}:\n\n")
            if class_name == "main_menu":
                heading_ = heading.replace("_", "\_")
            else:
                heading_ = class_name.split(".")[-1]
            f.write(f"{heading_}\n")
            f.write(f"{'=' * len(heading_)}\n")
            desc = MENU_DESCRIPTIONS.get(heading)
            if desc:
                f.write(desc)
            f.write("\n")

            command_names = [v.name for _, v in menu.children.items() if v.is_command]
            child_menu_names = [
                v.name for _, v in menu.children.items() if not v.is_command
            ]

            f.write(f".. autoclass:: {self._tui_module}.{class_name}\n")
            if class_name != "main_menu":
                f.write("   :noindex:\n")
            f.write("   :members:\n")
            f.write("   :show-inheritance:\n")
            f.write("   :undoc-members:\n")
            f.write('   :exclude-members: "__weakref__, __dict__"\n')
            f.write('   :special-members: " __init__"\n')
            f.write("   :autosummary:\n\n")

            if child_menu_names:
                f.write(".. toctree::\n")
                f.write("   :hidden:\n\n")

                for _, v in menu.children.items():
                    if not v.is_command:
                        f.write(f"   {v.name}/index\n")
                        self._write_doc_for_menu(
                            v,
                            doc_dir / v.name,
                            heading + "." + v.name,
                            class_name + "." + v.name,
                        )

    def generate(self) -> None:
        Path(self._tui_file).parent.mkdir(exist_ok=True)
        with open(self._tui_file, "w", encoding="utf8") as self.__writer:
            if self._version == "222":
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
                info = PyMenu(self._service, self._main_menu.path).get_static_info()
                self._populate_menu(self._main_menu, info)
            self.session.exit()
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
                "import PyMenu, TUIMenu\n\n\n"
            )
            self._main_menu.name = "main_menu"
            self._write_menu_to_tui_file(self._main_menu)
            self._write_doc_for_menu(
                self._main_menu,
                Path(self._tui_doc_dir),
                self._tui_heading,
                self._main_menu.name,
            )


def generate():
    # pyfluent.set_log_level("WARNING")
    version = get_version_for_filepath()
    if version > "222":
        _copy_tui_help_xml_file(version)
    _populate_xml_helpstrings()
    TUIGenerator("meshing", version).generate()
    TUIGenerator("solver", version).generate()
    logger.warning(
        "XML help is available but not picked for the following %i paths:",
        len(_XML_HELPSTRINGS),
    )
    for k, _ in _XML_HELPSTRINGS.items():
        logger.info(k)


if __name__ == "__main__":
    generate()
