# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Provide a module to generate explicit Fluent TUI menu classes.

This module starts up Fluent and calls the underlying gRPC APIs to generate the
following TUI Python modules:

- src/ansys/fluent/core/solver/tui.py
- src/ansys/fluent/core/meshing/tui.py.

Usage
-----

`python codegen/tuigen.py`
"""

import argparse
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

from defusedxml.ElementTree import parse

import ansys.fluent.core as pyfluent
from ansys.fluent.core import FluentMode, launch_fluent
from ansys.fluent.core.codegen import StaticInfoType
from ansys.fluent.core.codegen.data.fluent_gui_help_patch import XML_HELP_PATCH
from ansys.fluent.core.docker.utils import get_ghcr_fluent_image_name
from ansys.fluent.core.services.datamodel_tui import (
    convert_path_to_grpc_path,
    convert_tui_menu_to_func_name,
)
from ansys.fluent.core.utils.fix_doc import escape_wildcards
from ansys.fluent.core.utils.fluent_version import (
    FluentVersion,
    get_version_for_file_name,
)

logger = logging.getLogger("pyfluent.tui")

_ROOT_DIR = Path(__file__) / ".." / ".." / ".." / ".." / ".." / ".."


def _get_tui_filepath(mode: str, version: str):
    return (pyfluent.config.codegen_outdir / mode / f"tui_{version}.py").resolve()


_INDENT_STEP = 4


# TODO: Move doc-specific variables to docgen


def _get_tui_docdir(mode: str):
    return os.path.normpath(
        os.path.join(
            _ROOT_DIR,
            "doc",
            "source",
            "api",
            mode,
            "tui",
        )
    )


_XML_HELP_FILE = (Path(__file__) / ".." / "data" / "fluent_gui_help.xml").resolve()
_XML_HELPSTRINGS = {}


def _copy_tui_help_xml_file(version: str):
    if pyfluent.config.launch_fluent_container:
        image_tag = pyfluent.config.fluent_image_tag
        image_name = f"{get_ghcr_fluent_image_name(image_tag)}:{image_tag}"
        container_name = uuid.uuid4().hex
        is_linux = platform.system() == "Linux"
        subprocess.run(
            f"docker container create --name {container_name} {image_name}",
            shell=is_linux,
        )
        xml_source = f"/ansys_inc/v{version}/commonfiles/help/en-us/fluent_gui_help/fluent_gui_help.xml"
        subprocess.run(
            f"docker cp {container_name}:{xml_source} {str(_XML_HELP_FILE)}",
            shell=is_linux,
        )
        subprocess.run(f"docker container rm {container_name}", shell=is_linux)

    else:
        try:
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
        except FileNotFoundError:
            logger.warning("fluent_gui_help.xml is not found.")


def _populate_xml_helpstrings():
    if not Path(_XML_HELP_FILE).exists():
        return

    tree = parse(_XML_HELP_FILE)
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
    _XML_HELP_FILE.unlink(missing_ok=True)


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
        """Get the full path to a command."""
        return convert_path_to_grpc_path(self.path + [command])


class _RenameModuleUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        renamed_module = module
        if module == "tuigen":
            renamed_module = "ansys.fluent.core.codegen.tuigen"

        return super(_RenameModuleUnpickler, self).find_class(renamed_module, name)


class TUIGenerator:
    """Generates explicit TUI menu classes."""

    def __init__(
        self, mode: str, version: str, static_infos: dict, verbose: bool = False
    ):
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
        self._main_menu = _TUIMenu([], "")
        self._static_infos = static_infos
        self._verbose = verbose

    def _populate_menu(self, menu: _TUIMenu, info: Dict[str, Any]):
        for child_menu_name, child_menu_info in sorted(info["menus"].items()):
            if _is_valid_tui_menu_name(child_menu_name):
                child_menu = _TUIMenu(
                    menu.path + [child_menu_name], child_menu_info["help"]
                )
                menu.children[child_menu.name] = child_menu
                self._populate_menu(child_menu, child_menu_info)
        for child_command_name, child_command_info in sorted(info["commands"].items()):
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
        """Generate TUI API classes."""
        api_tree = {}
        Path(self._tui_file).parent.mkdir(exist_ok=True)
        if self._verbose:
            print(f"{str(self._tui_file)}")
        with open(self._tui_file, "w", encoding="utf8") as self.__writer:
            if FluentVersion(self._version) == FluentVersion.v222:
                with open(
                    (
                        Path(__file__)
                        / ".."
                        / "data"
                        / f"static_info_{self._version}_{self._mode}.pickle"
                    ).resolve(),
                    "rb",
                ) as f:
                    self._main_menu = _RenameModuleUnpickler(f).load()
            else:
                info = self._static_infos[
                    (
                        StaticInfoType.TUI_MESHING
                        if self._mode == "meshing"
                        else StaticInfoType.TUI_SOLVER
                    )
                ]
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


def generate(version, static_infos: dict, verbose: bool = False):
    """Generate TUI API classes."""
    api_tree = {}
    gt_222 = FluentVersion(version) > FluentVersion.v222
    if gt_222:
        if (
            StaticInfoType.TUI_MESHING not in static_infos
            and StaticInfoType.TUI_SOLVER not in static_infos
        ):
            return api_tree
        _copy_tui_help_xml_file(version)
    _populate_xml_helpstrings()
    if not gt_222 or StaticInfoType.TUI_MESHING in static_infos:
        api_tree["<meshing_session>"] = TUIGenerator(
            "meshing", version, static_infos, verbose
        ).generate()
    if not gt_222 or StaticInfoType.TUI_SOLVER in static_infos:
        api_tree["<solver_session>"] = TUIGenerator(
            "solver", version, static_infos, verbose
        ).generate()
    if not pyfluent.config.hide_log_secrets:
        logger.info(
            "XML help is available but not picked for the following %i paths: ",
            len(_XML_HELPSTRINGS),
        )
        for k in _XML_HELPSTRINGS:
            logger.info(k)
    return api_tree


if __name__ == "__main__":
    solver = launch_fluent()
    meshing = launch_fluent(mode=FluentMode.MESHING)
    version = get_version_for_file_name(session=solver)
    static_infos = {}
    if FluentVersion(version) > FluentVersion.v222:
        static_infos[StaticInfoType.TUI_SOLVER] = (
            solver._datamodel_service_tui.get_static_info("")
        )
        static_infos[StaticInfoType.TUI_MESHING] = (
            meshing._datamodel_service_tui.get_static_info("")
        )
    parser = argparse.ArgumentParser(
        description="A script to write Fluent API files with an optional verbose output."
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show paths of written Fluent API files.",
    )
    args = parser.parse_args()
    generate(version, static_infos, args.verbose)
