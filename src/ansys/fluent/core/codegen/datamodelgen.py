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

"""Module to generate Fluent datamodel API classes."""

import argparse
from io import FileIO, StringIO
import os
from pathlib import Path
import shutil
import string
from typing import Any, Dict

import ansys.fluent.core as pyfluent
from ansys.fluent.core import FluentMode, launch_fluent
from ansys.fluent.core.codegen import StaticInfoType
from ansys.fluent.core.codegen.data.meshing_utilities_examples import (
    meshing_utility_examples,
)
from ansys.fluent.core.services.datamodel_se import (
    PySingletonCommandArgumentsSubItem,
    arg_class_by_type,
)
from ansys.fluent.core.utils.fix_doc import escape_wildcards
from ansys.fluent.core.utils.fluent_version import (
    FluentVersion,
    get_version_for_file_name,
)

_ROOT_DIR = Path(__file__) / ".." / ".." / ".." / ".." / ".." / ".."

_PY_TYPE_BY_DM_TYPE = {
    **dict.fromkeys(["Logical", "Bool"], "bool"),
    **dict.fromkeys(["Logical List", "ListBool"], "list[bool]"),
    "String": "str",
    **dict.fromkeys(["String List", "ListString"], "list[str]"),
    **dict.fromkeys(["Integer", "Int"], "int"),
    **dict.fromkeys(["Integer List", "ListInt"], "list[int]"),
    "Real": "float",
    **dict.fromkeys(
        [
            "Real List",
            "ListReal",
            "Real Triplet",
            "RealTriplet",
            "Real Triplet List",
            "ListRealTriplet",
        ],
        "list[float]",
    ),
    **dict.fromkeys(["Dict", "ModelObject"], "dict[str, Any]"),
    "None": "None",
}

# TODO: Move doc specific variables to docgen

_MESHING_DM_DOC_DIR = os.path.normpath(
    os.path.join(
        _ROOT_DIR,
        "doc",
        "source",
        "api",
        "meshing",
        "datamodel",
    )
)
_SOLVER_DM_DOC_DIR = os.path.normpath(
    os.path.join(
        _ROOT_DIR,
        "doc",
        "source",
        "api",
        "solver",
        "datamodel",
    )
)


digits = {
    0: "Zero",
    1: "One",
    2: "Two",
    3: "Three",
    4: "Four",
    5: "Five",
    6: "Six",
    7: "Seven",
    8: "Eight",
    9: "Nine",
}


def _convert_to_py_name(name: str) -> str:
    ttable = str.maketrans(string.punctuation, "_" * len(string.punctuation))
    name = name.translate(ttable)
    if name[0].isdigit():
        name = f"{digits[int(name[0])]}{name[1:]}"
    return name


def _write_command_query_stub(name: str, info: Any, f: FileIO):
    signature = StringIO()
    indent = "        "
    signature.write(f"(\n{indent}self,\n")
    if info.get("args"):
        for arg in info.get("args"):
            signature.write(
                f'{indent}{arg["name"]}: {_PY_TYPE_BY_DM_TYPE[arg["type"]]} | None = None,\n'
            )
    signature.write(f'{indent}) -> {_PY_TYPE_BY_DM_TYPE[info["returntype"]]}: ...')
    f.write(f"\n    def {name}{signature.getvalue()}\n")


def _build_singleton_docstring(name: str):
    return f"Singleton {name}."


def _build_parameter_docstring(name: str, t: str):
    return f"Parameter {name} of value type {_PY_TYPE_BY_DM_TYPE[t]}."


def _build_command_query_docstring(
    name: str, static_info: Any, indent: str, is_command: bool
):
    doc = StringIO()
    info = static_info["commandinfo"] if is_command else static_info["queryinfo"]
    if static_info.get("helpstring"):
        for line in static_info["helpstring"].splitlines():
            doc.write(f"{indent}{line}\n")
    elif info.get("docstring"):
        for line in info["docstring"].split("."):
            if line and len(info["docstring"].split(".")) > 2:
                doc.write(f"{indent}- {line.lstrip(' ')}.\n")
            elif line:
                doc.write(f"{indent}{line.lstrip(' ')}.\n")
    else:
        doc.write(
            f"{indent}Command {name}.\n\n"
            if is_command
            else f"{indent}Query {name}.\n\n"
        )
    if info.get("args"):
        doc.write(f"{indent}Parameters\n")
        doc.write(f"{indent}{'-' * len('Parameters')}\n")
        for arg in info.get("args"):
            doc.write(f'{indent}{arg["name"]} : {_PY_TYPE_BY_DM_TYPE[arg["type"]]}\n')
            if arg.get("helpstring"):
                for line in arg["helpstring"].splitlines():
                    doc.write(f"{indent}    {line}\n")
            elif arg.get("docstring"):
                doc.write(f'{indent}    {arg["docstring"]}\n')
    doc.write(f"\n{indent}Returns\n")
    doc.write(f"{indent}{'-' * len('Returns')}\n")
    doc.write(f'{indent}{_PY_TYPE_BY_DM_TYPE[info["returntype"]]}\n')
    if meshing_utility_examples.get(name):
        doc.write(f"\n{indent}Examples\n")
        doc.write(f"{indent}{'-' * len('Examples')}\n")
        for example in meshing_utility_examples[name]:
            doc.write(f"{indent}>>> {example}\n")
    return doc.getvalue()


datamodel_file_name_map = {
    "workflow": "workflow",
    "meshing": "meshing",
    "PartManagement": "part_management",
    "PMFileManagement": "pm_file_management",
    "preferences": "preferences",
    "MeshingUtilities": "meshing_utilities",
    "flicing": "flicing",
    "solverworkflow": "solver_workflow",
}


class DataModelStaticInfo:
    """Stores datamodel static information."""

    _noindices = []

    def __init__(
        self,
        static_info_type: StaticInfoType,
        rules: str,
        modes: tuple,
        version: str,
        rules_save_name: str = "",
    ):
        self.static_info_type = static_info_type
        self.rules = rules
        self.modes = modes
        self.static_info = None
        if rules_save_name == "":
            rules_save_name = rules
        datamodel_dir = (
            pyfluent.config.codegen_outdir / f"datamodel_{version}"
        ).resolve()
        datamodel_dir.mkdir(exist_ok=True)
        self.file_name = (
            datamodel_dir / f"{datamodel_file_name_map[rules_save_name]}.py"
        ).resolve()
        if rules == "MeshingUtilities":
            self.stub_file = (datamodel_dir / "meshing_utilities.pyi").resolve()
        if len(modes) > 1:
            for mode in modes[1:]:
                DataModelStaticInfo._noindices.append(f"{mode}.datamodel.{rules}")


class DataModelGenerator:
    """Provides the datamodel API class generator."""

    def __init__(self, version, static_infos: dict, verbose: bool = False):
        self.version = version
        self._server_static_infos = static_infos
        self._static_info: Dict[str, DataModelStaticInfo] = {}
        self._verbose = verbose
        if StaticInfoType.DATAMODEL_WORKFLOW in static_infos:
            self._static_info["workflow"] = DataModelStaticInfo(
                StaticInfoType.DATAMODEL_WORKFLOW,
                "workflow",
                (
                    "meshing",
                    "solver",
                ),
                self.version,
            )
        if StaticInfoType.DATAMODEL_MESHING in static_infos:
            self._static_info["meshing"] = DataModelStaticInfo(
                StaticInfoType.DATAMODEL_MESHING, "meshing", ("meshing",), self.version
            )
        if StaticInfoType.DATAMODEL_PART_MANAGEMENT in static_infos:
            self._static_info["PartManagement"] = DataModelStaticInfo(
                StaticInfoType.DATAMODEL_PART_MANAGEMENT,
                "PartManagement",
                ("meshing",),
                self.version,
            )
        if StaticInfoType.DATAMODEL_PM_FILE_MANAGEMENT in static_infos:
            self._static_info["PMFileManagement"] = DataModelStaticInfo(
                StaticInfoType.DATAMODEL_PM_FILE_MANAGEMENT,
                "PMFileManagement",
                ("meshing",),
                self.version,
            )
        if StaticInfoType.DATAMODEL_FLICING in static_infos:
            self._static_info["flicing"] = DataModelStaticInfo(
                StaticInfoType.DATAMODEL_FLICING,
                "flserver",
                ("flicing",),
                self.version,
                "flicing",
            )
        if StaticInfoType.DATAMODEL_PREFERENCES in static_infos:
            self._static_info["preferences"] = DataModelStaticInfo(
                StaticInfoType.DATAMODEL_PREFERENCES,
                "preferences",
                ("meshing", "solver", "flicing"),
                self.version,
            )
        if StaticInfoType.DATAMODEL_SOLVER_WORKFLOW in static_infos:
            self._static_info["solverworkflow"] = DataModelStaticInfo(
                StaticInfoType.DATAMODEL_SOLVER_WORKFLOW,
                "solverworkflow",
                ("solver",),
                self.version,
            )
        if StaticInfoType.DATAMODEL_MESHING_UTILITIES in static_infos:
            self._static_info["MeshingUtilities"] = DataModelStaticInfo(
                StaticInfoType.DATAMODEL_MESHING_UTILITIES,
                "MeshingUtilities",
                ("meshing",),
                self.version,
            )
        self._delete_generated_files()
        self._populate_static_info()

    def _get_static_info(self, static_info_type: StaticInfoType):
        return self._server_static_infos[static_info_type]

    def _populate_static_info(self):
        run_meshing_mode = any(
            "meshing" in info.modes for _, info in self._static_info.items()
        )
        run_solver_mode = any(
            "solver" in info.modes for _, info in self._static_info.items()
        )
        run_icing_mode = FluentVersion(self.version) >= FluentVersion.v231 and any(
            "flicing" in info.modes for _, info in self._static_info.items()
        )

        if run_meshing_mode:
            for _, info in self._static_info.items():
                if "meshing" in info.modes:
                    info.static_info = self._get_static_info(info.static_info_type)

        if run_solver_mode:
            for _, info in self._static_info.items():
                if "solver" in info.modes:
                    info.static_info = self._get_static_info(info.static_info_type)

        if run_icing_mode:
            info = self._static_info.get("flicing")
            if info:
                info.static_info = self._get_static_info(
                    StaticInfoType.DATAMODEL_FLICING
                )
                try:
                    if (
                        len(
                            info.static_info["singletons"]["Case"]["singletons"]["App"][
                                "singletons"
                            ]
                        )
                        == 0
                    ):
                        print(
                            "Information: Icing settings not generated ( R23.1+ is required )\n"
                        )
                except Exception:
                    print(
                        "Information: Problem accessing flserver datamodel for icing settings\n"
                    )

    def _write_arg_class(self, f: FileIO, arg_info, indent: str):
        arg_name = arg_info["name"]
        arg_type = arg_info["type"]
        arg_doc = arg_info.get("helpstring", f"Argument {arg_name}.")
        arg_class = arg_class_by_type[arg_type]
        py_name = _convert_to_py_name(arg_name)
        f.write(f"{indent}class _{py_name}({arg_class.__name__}):\n")
        f.write(f'{indent}    """\n')
        for line in arg_doc.splitlines():
            f.write(f"{indent}    {escape_wildcards(line)}\n")
        f.write(f'{indent}    """\n\n')
        if arg_class == PySingletonCommandArgumentsSubItem:
            f.write(
                f"{indent}    def __init__(self, parent, attr, service, rules, path):\n"
            )
            f.write(
                f"{indent}        super().__init__(parent, attr, service, rules, path)\n"
            )
            info = arg_info.get("info")
            if info:
                parameters_info = info["parameters"]
                for name, parameter_info in parameters_info.items():
                    py_name = _convert_to_py_name(name)
                    f.write(
                        f'{indent}        self.{py_name} = self._{py_name}(self, "{name}", service, rules, path)\n'
                    )
                f.write("\n")
                for name, parameter_info in parameters_info.items():
                    self._write_arg_class(
                        f, parameter_info | {"name": name}, f"{indent}    "
                    )

    def _write_static_info(self, name: str, info: Any, f: FileIO, level: int = 0):
        api_tree = {}
        # preferences contains a deprecated object Meshing Workflow (with a space)
        # which migrates to MeshingWorkflow automatically. Simplest thing to do is
        # filter out invalid names.
        if not name.isidentifier():
            return api_tree
        indent = " " * level * 4
        singleton_doc = info.get("helpstring", _build_singleton_docstring(name))
        f.write(f"{indent}class {name}(PyMenu):\n")
        f.write(f'{indent}    """\n')
        for line in singleton_doc.splitlines():
            f.write(f"{indent}    {escape_wildcards(line)}\n")
        f.write(f'{indent}    """\n')
        f.write(f"{indent}    def __init__(self, service, rules, path):\n")
        named_objects = sorted(info.get("namedobjects", []))
        singletons = sorted(info.get("singletons", []))
        parameters = sorted(info.get("parameters", []))
        commands = sorted(info.get("commands", []))
        queries = sorted(info.get("queries", []))
        for k in named_objects:
            f.write(
                f"{indent}        self.{k} = "
                f'self.__class__.{k}(service, rules, path + [("{k}", "")])\n'
            )
        for k in singletons:
            # This is where filtering these names out really matters (see commsent above)
            if k.isidentifier():
                f.write(
                    f"{indent}        self.{k} = "
                    f'self.__class__.{k}(service, rules, path + [("{k}", "")])\n'
                )
        for k in parameters:
            f.write(
                f"{indent}        self.{k} = "
                f'self.__class__.{k}(service, rules, path + [("{k}", "")])\n'
            )
        for k in commands:
            f.write(
                f"{indent}        self.{k} = "
                f'self.__class__.{k}(service, rules, "{k}", path)\n'
            )
        for k in queries:
            f.write(
                f"{indent}        self.{k} = "
                f'self.__class__.{k}(service, rules, "{k}", path)\n'
            )
        f.write(f"{indent}        super().__init__(service, rules, path)\n\n")
        for k in named_objects:
            f.write(f"{indent}    class {k}(PyNamedObjectContainer):\n")
            f.write(f'{indent}        """\n')
            f.write(f"{indent}        .\n")
            f.write(f'{indent}        """\n')
            api_tree[f"{k}:<name>"] = self._write_static_info(
                f"_{k}", info["namedobjects"][k], f, level + 2
            )
            # Specify the concrete named object type for __getitem__
            f.write(f"{indent}        def __getitem__(self, key: str) -> " f"_{k}:\n")
            f.write(f"{indent}            return super().__getitem__(key)\n\n")
        for k in singletons:
            if k.isidentifier():
                # print("included", k)
                api_tree[k] = self._write_static_info(
                    k, info["singletons"][k], f, level + 1
                )
            else:
                # print("\t\texcluded", k)
                pass
        for parameter_name in parameters:
            parameter_info = info["parameters"][parameter_name]
            parameter_type = parameter_info["type"]
            if parameter_type in {"String", "String List", "ListString"}:
                f.write(f"{indent}    class {parameter_name}(PyTextual):\n")
            elif parameter_type in {"Integer", "Int", "Real"}:
                f.write(f"{indent}    class {parameter_name}(PyNumerical):\n")
            elif parameter_type in {"Dict", "ModelObject"}:
                f.write(f"{indent}    class {parameter_name}(PyDictionary):\n")
            else:
                f.write(f"{indent}    class {parameter_name}(PyParameter):\n")
            parameter_doc = parameter_info.get(
                "helpstring", _build_parameter_docstring(parameter_name, parameter_type)
            )
            f.write(f'{indent}        """\n')
            for line in parameter_doc.splitlines():
                f.write(f"{indent}        {escape_wildcards(line)}\n")
            f.write(f'{indent}        """\n')
            f.write(f"{indent}        pass\n\n")
            api_tree[parameter_name] = "Parameter"
        if "meshing_utilities" in f.name:
            stub_file = self._static_info["MeshingUtilities"].stub_file
            stub_file.unlink(missing_ok=True)
            with open(stub_file, "w", encoding="utf8") as file:
                file.write("#\n")
                file.write("# This is an auto-generated file.  DO NOT EDIT!\n")
                file.write("#\n")
                file.write("# pylint: disable=line-too-long\n\n")
                file.write(
                    "from ansys.fluent.core.services.datamodel_se import PyMenu\n"
                )
                file.write("from typing import Any\n")
                file.write("\n\n")
                file.write("class Root(PyMenu):\n")
                for k in commands:
                    _write_command_query_stub(
                        k,
                        info["commands"][k]["commandinfo"],
                        file,
                    )
                for k in queries:
                    _write_command_query_stub(
                        k,
                        info["queries"][k]["queryinfo"],
                        file,
                    )
        for k in commands:
            f.write(f"{indent}    class {k}(PyCommand):\n")
            f.write(f'{indent}        """\n')
            command_static_info = info["commands"][k]
            f.write(
                _build_command_query_docstring(
                    k, command_static_info, f"{indent}        ", True
                )
            )
            f.write(f'{indent}        """\n')
            f.write(
                f"{indent}        class _{k}CommandArguments(PyCommandArguments):\n"
            )
            f.write(
                f"{indent}            def __init__(self, service, rules, command, path, id):\n"
            )
            f.write(
                f"{indent}                super().__init__(service, rules, command, path, id)\n"
            )
            args_info = command_static_info["commandinfo"].get("args", [])
            for arg_info in args_info:
                arg_name = arg_info["name"]
                py_name = _convert_to_py_name(arg_name)
                f.write(
                    f'{indent}                self.{py_name} = self._{py_name}(self, "{arg_name}", service, rules, path)\n'
                )
            f.write("\n")
            for arg_info in args_info:
                self._write_arg_class(f, arg_info, f"{indent}            ")

            f.write(
                f"{indent}        def create_instance(self) -> _{k}CommandArguments:\n"
            )
            f.write(f"{indent}            args = self._get_create_instance_args()\n")
            f.write(f"{indent}            if args is not None:\n")
            f.write(
                f"{indent}                return self._{k}CommandArguments(*args)\n\n"
            )
            api_tree[k] = "Command"
        for k in queries:
            f.write(f"{indent}    class {k}(PyQuery):\n")
            f.write(f'{indent}        """\n')
            f.write(
                _build_command_query_docstring(
                    k, info["queries"][k], f"{indent}        ", False
                )
            )
            f.write(f'{indent}        """\n')
            f.write(f"{indent}        pass\n\n")
            api_tree[k] = "Query"
        return api_tree

    def write_static_info(self) -> None:
        """Write API classes to files."""
        api_tree = {"<meshing_session>": {}, "<solver_session>": {}}
        for name, info in self._static_info.items():
            if self._verbose:
                print(f"{str(info.file_name)}")
            if info.static_info is None:
                continue
            with open(info.file_name, "w", encoding="utf8") as f:
                f.write("#\n")
                f.write("# This is an auto-generated file.  DO NOT EDIT!\n")
                f.write("#\n")
                f.write("# pylint: disable=line-too-long\n\n")
                f.write("from ansys.fluent.core.services.datamodel_se import (\n")
                f.write("    PyMenu,\n")
                f.write("    PyParameter,\n")
                f.write("    PyTextual,\n")
                f.write("    PyNumerical,\n")
                f.write("    PyDictionary,\n")
                f.write("    PyNamedObjectContainer,\n")
                f.write("    PyCommand,\n")
                f.write("    PyQuery,\n")
                f.write("    PyCommandArguments,\n")
                f.write("    PyTextualCommandArgumentsSubItem,\n")
                f.write("    PyNumericalCommandArgumentsSubItem,\n")
                f.write("    PyDictionaryCommandArgumentsSubItem,\n")
                f.write("    PyParameterCommandArgumentsSubItem,\n")
                f.write("    PySingletonCommandArgumentsSubItem\n")
                f.write(")\n\n\n")
                api_tree_val = {
                    name: self._write_static_info("Root", info.static_info, f)
                }
                for mode in info.modes:
                    if mode in ("solver", "meshing"):
                        key = f"<{mode}_session>"
                        api_tree[key].update(api_tree_val)
        return api_tree

    def _delete_generated_files(self):
        for _, info in self._static_info.items():
            if info.file_name.exists():
                info.file_name.unlink()
        if Path(_MESHING_DM_DOC_DIR).exists():
            shutil.rmtree(Path(_MESHING_DM_DOC_DIR))
        if Path(_SOLVER_DM_DOC_DIR).exists():
            shutil.rmtree(Path(_SOLVER_DM_DOC_DIR))


def generate(version, static_infos: dict, verbose: bool = False):
    """Generate datamodel API classes."""
    return DataModelGenerator(version, static_infos, verbose).write_static_info()


if __name__ == "__main__":
    solver = launch_fluent()
    meshing = launch_fluent(mode=FluentMode.MESHING)
    version = get_version_for_file_name(session=meshing)
    static_infos = {
        StaticInfoType.DATAMODEL_WORKFLOW: meshing._datamodel_service_se.get_static_info(
            "workflow"
        ),
        StaticInfoType.DATAMODEL_MESHING: meshing._datamodel_service_se.get_static_info(
            "meshing"
        ),
        StaticInfoType.DATAMODEL_PART_MANAGEMENT: meshing._datamodel_service_se.get_static_info(
            "PartManagement"
        ),
        StaticInfoType.DATAMODEL_PM_FILE_MANAGEMENT: meshing._datamodel_service_se.get_static_info(
            "PMFileManagement"
        ),
        StaticInfoType.DATAMODEL_PREFERENCES: solver._datamodel_service_se.get_static_info(
            "preferences"
        ),
    }
    if FluentVersion(version) >= FluentVersion.v231:
        flicing = launch_fluent(mode=FluentMode.SOLVER_ICING)
        static_infos[StaticInfoType.DATAMODEL_FLICING] = (
            flicing._datamodel_service_se.get_static_info("flserver")
        )
        static_infos[StaticInfoType.DATAMODEL_SOLVER_WORKFLOW] = (
            solver._datamodel_service_se.get_static_info("solverworkflow")
        )
    if FluentVersion(version) >= FluentVersion.v242:
        static_infos[StaticInfoType.DATAMODEL_MESHING_UTILITIES] = (
            meshing._datamodel_service_se.get_static_info("MeshingUtilities")
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
