"""Module to generate Fluent datamodel API classes."""

from io import FileIO
import os
from pathlib import Path
import shutil
from typing import Any, Dict

from ansys.fluent.core import GENERATED_API_DIR, FluentMode, launch_fluent
from ansys.fluent.core.session import BaseSession as Session
from ansys.fluent.core.utils.fluent_version import (
    FluentVersion,
    get_version_for_file_name,
)

_ROOT_DIR = Path(__file__) / ".." / ".." / ".." / ".." / ".." / ".."

_PY_TYPE_BY_DM_TYPE = {
    **dict.fromkeys(["Logical", "Bool"], "bool"),
    **dict.fromkeys(["Logical List", "ListBool"], "List[bool]"),
    "String": "str",
    **dict.fromkeys(["String List", "ListString"], "List[str]"),
    **dict.fromkeys(["Integer", "Int"], "int"),
    **dict.fromkeys(["Integer List", "ListInt"], "List[int]"),
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
        "List[float]",
    ),
    **dict.fromkeys(["Dict", "ModelObject"], "Dict[str, Any]"),
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


def _build_singleton_docstring(name: str):
    return f"Singleton {name}."


def _build_parameter_docstring(name: str, t: str):
    return f"Parameter {name} of value type {_PY_TYPE_BY_DM_TYPE[t]}."


def _build_command_query_docstring(name: str, info: Any, indent: str, is_command: bool):
    doc = f"{indent}Command {name}.\n\n" if is_command else f"{indent}Query {name}.\n\n"
    if info.get("args"):
        doc += f"{indent}Parameters\n"
        doc += f"{indent}{'-' * len('Parameters')}\n"
        for arg in info.get("args"):
            doc += f'{indent}{arg["name"]} : {_PY_TYPE_BY_DM_TYPE[arg["type"]]}\n'
    doc += f"\n{indent}Returns\n"
    doc += f"{indent}{'-' * len('Returns')}\n"
    doc += f'{indent}{_PY_TYPE_BY_DM_TYPE[info["returntype"]]}\n'
    return doc


class DataModelStaticInfo:
    """Stores datamodel static information."""

    _noindices = []

    def __init__(
        self,
        rules: str,
        modes: tuple,
        version: str,
        rules_save_name: str = "",
    ):
        self.rules = rules
        self.modes = modes
        self.static_info = None
        if rules_save_name == "":
            rules_save_name = rules
        datamodel_dir = (GENERATED_API_DIR / f"datamodel_{version}").resolve()
        datamodel_dir.mkdir(exist_ok=True)
        self.file_name = (datamodel_dir / f"{rules_save_name}.py").resolve()
        if len(modes) > 1:
            for mode in modes[1:]:
                DataModelStaticInfo._noindices.append(f"{mode}.datamodel.{rules}")


class DataModelGenerator:
    """Provides the datamodel API class generator."""

    def __init__(self, version, sessions: dict):
        self.version = version
        self.sessions = sessions
        self._static_info: Dict[str, DataModelStaticInfo] = {
            "workflow": DataModelStaticInfo(
                "workflow",
                (
                    "meshing",
                    "solver",
                ),
                self.version,
            ),
            "meshing": DataModelStaticInfo("meshing", ("meshing",), self.version),
            "PartManagement": DataModelStaticInfo(
                "PartManagement", ("meshing",), self.version
            ),
            "PMFileManagement": DataModelStaticInfo(
                "PMFileManagement", ("meshing",), self.version
            ),
            "flicing": DataModelStaticInfo(
                "flserver", ("flicing",), self.version, "flicing"
            ),
            "preferences": DataModelStaticInfo(
                "preferences",
                ("meshing", "solver", "flicing,"),
                self.version,
            ),
            "solverworkflow": (
                DataModelStaticInfo("solverworkflow", ("solver",), self.version)
                if FluentVersion(self.version) >= FluentVersion.v231
                else None
            ),
        }
        if FluentVersion(self.version) >= FluentVersion.v242:
            self._static_info["meshing_utilities"] = DataModelStaticInfo(
                "MeshingUtilities", ("meshing",), self.version
            )
        if not self._static_info["solverworkflow"]:
            del self._static_info["solverworkflow"]
        self._delete_generated_files()
        self._populate_static_info()

    def _get_static_info(self, rules: str, session: Session):
        response = session._datamodel_service_se.get_static_info(rules)
        return response

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
            if FluentMode.MESHING_MODE not in self.sessions:
                self.sessions[FluentMode.MESHING_MODE] = launch_fluent(
                    mode=FluentMode.MESHING_MODE
                )
            session = self.sessions[FluentMode.MESHING_MODE]
            for _, info in self._static_info.items():
                if "meshing" in info.modes:
                    info.static_info = self._get_static_info(info.rules, session)
            self.sessions.pop(FluentMode.MESHING_MODE)

        if run_solver_mode:
            if FluentMode.SOLVER not in self.sessions:
                self.sessions[FluentMode.SOLVER] = launch_fluent(mode=FluentMode.SOLVER)
            session = self.sessions[FluentMode.SOLVER]
            for _, info in self._static_info.items():
                if "solver" in info.modes:
                    info.static_info = self._get_static_info(info.rules, session)

        if run_icing_mode:
            if FluentMode.SOLVER_ICING not in self.sessions:
                self.sessions[FluentMode.SOLVER_ICING] = launch_fluent(
                    mode=FluentMode.SOLVER_ICING
                )
            session = self.sessions[FluentMode.SOLVER_ICING]
            for _, info in self._static_info.items():
                if "flicing" in info.modes:
                    info.static_info = self._get_static_info(info.rules, session)
                    try:
                        if (
                            len(
                                info.static_info["singletons"]["Case"]["singletons"][
                                    "App"
                                ]["singletons"]
                            )
                            == 0
                        ):
                            print(
                                "Information: Icing settings not generated ( R23.1+ is required )\n"
                            )
                    except:
                        print(
                            "Information: Problem accessing flserver datamodel for icing settings\n"
                        )
            self.sessions.pop(FluentMode.SOLVER_ICING)

    def _write_static_info(self, name: str, info: Any, f: FileIO, level: int = 0):
        api_tree = {}
        # preferences contains a deprecated object Meshing Workflow (with a space)
        # which migrates to MeshingWorkflow automatically. Simplest thing to do is
        # filter out invalid names.
        if not name.isidentifier():
            return api_tree
        indent = " " * level * 4
        f.write(f"{indent}class {name}(PyMenu):\n")
        f.write(f'{indent}    """\n')
        f.write(f"{indent}    {_build_singleton_docstring(name)}\n")
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
        for k in parameters:
            k_type = _PY_TYPE_BY_DM_TYPE[info["parameters"][k]["type"]]
            if k_type in ["str", "List[str]"]:
                f.write(f"{indent}    class {k}(PyTextual):\n")
            elif k_type in ["int", "float"]:
                f.write(f"{indent}    class {k}(PyNumerical):\n")
            elif k_type in ["Dict", "Dict[str, Any]"]:
                f.write(f"{indent}    class {k}(PyDictionary):\n")
            else:
                f.write(f"{indent}    class {k}(PyParameter):\n")
            f.write(f'{indent}        """\n')
            f.write(
                f"{indent}        "
                f'{_build_parameter_docstring(k, info["parameters"][k]["type"])}\n'
            )
            f.write(f'{indent}        """\n')
            f.write(f"{indent}        pass\n\n")
            api_tree[k] = "Parameter"
        for k in commands:
            f.write(f"{indent}    class {k}(PyCommand):\n")
            f.write(f'{indent}        """\n')
            f.write(
                _build_command_query_docstring(
                    k, info["commands"][k]["commandinfo"], f"{indent}        ", True
                )
            )
            f.write(f'{indent}        """\n')
            f.write(f"{indent}        pass\n\n")
            api_tree[k] = "Command"
        for k in queries:
            f.write(f"{indent}    class {k}(PyQuery):\n")
            f.write(f'{indent}        """\n')
            f.write(
                _build_command_query_docstring(
                    k, info["queries"][k]["queryinfo"], f"{indent}        ", False
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
            if info.static_info == None:
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
                f.write("    PyQuery\n")
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


def generate(version, sessions: dict):
    """Generate datamodel API classes."""
    return DataModelGenerator(version, sessions).write_static_info()


if __name__ == "__main__":
    sessions = {FluentMode.SOLVER: launch_fluent()}
    version = get_version_for_file_name(session=sessions[FluentMode.SOLVER])
    generate(version, sessions)
