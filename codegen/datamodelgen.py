from io import FileIO
import os
from pathlib import Path
import shutil
from typing import Any, Dict

from ansys.api.fluent.v0 import datamodel_se_pb2 as DataModelProtoModule
from ansys.fluent.core.session import BaseSession as Session
from ansys.fluent.core.utils.fluent_version import get_version_for_filepath

_THIS_DIR = Path(__file__).parent


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

_MESHING_DM_DOC_DIR = os.path.normpath(
    os.path.join(
        _THIS_DIR,
        "..",
        "doc",
        "source",
        "api",
        "meshing",
        "datamodel",
    )
)
_SOLVER_DM_DOC_DIR = os.path.normpath(
    os.path.join(
        _THIS_DIR,
        "..",
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


def _build_command_docstring(name: str, info: Any, indent: str):
    doc = f"{indent}Command {name}.\n\n"
    if info.args:
        doc += f"{indent}Parameters\n"
        doc += f"{indent}{'-' * len('Parameters')}\n"
        for arg in info.args:
            doc += f"{indent}{arg.name} : {_PY_TYPE_BY_DM_TYPE[arg.type]}\n"
    doc += f"\n{indent}Returns\n"
    doc += f"{indent}{'-' * len('Returns')}\n"
    doc += f"{indent}{_PY_TYPE_BY_DM_TYPE[info.returntype]}\n"
    return doc


class DataModelStaticInfo:
    _noindices = []

    def __init__(
        self,
        pyfluent_path: str,
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
        datamodel_dir = (
            (Path(pyfluent_path) if pyfluent_path else (Path(_THIS_DIR) / ".." / "src"))
            / "ansys"
            / "fluent"
            / "core"
            / f"datamodel_{version}"
        ).resolve()
        datamodel_dir.mkdir(exist_ok=True)
        self.filepath = (datamodel_dir / f"{rules_save_name}.py").resolve()
        if len(modes) > 1:
            for mode in modes[1:]:
                DataModelStaticInfo._noindices.append(f"{mode}.datamodel.{rules}")


class DataModelGenerator:
    def __init__(self, version, pyfluent_path):
        self.version = version
        self._static_info: Dict[str, DataModelStaticInfo] = {
            "workflow": DataModelStaticInfo(
                pyfluent_path,
                "workflow",
                (
                    "meshing",
                    "solver",
                ),
                self.version,
            ),
            "meshing": DataModelStaticInfo(
                pyfluent_path, "meshing", ("meshing",), self.version
            ),
            "PartManagement": DataModelStaticInfo(
                pyfluent_path, "PartManagement", ("meshing",), self.version
            ),
            "PMFileManagement": DataModelStaticInfo(
                pyfluent_path, "PMFileManagement", ("meshing",), self.version
            ),
            "flicing": DataModelStaticInfo(
                pyfluent_path, "flserver", ("flicing",), self.version, "flicing"
            ),
            "preferences": DataModelStaticInfo(
                pyfluent_path,
                "preferences",
                ("meshing", "solver", "flicing,"),
                self.version,
            ),
            "solverworkflow": DataModelStaticInfo(
                pyfluent_path, "solverworkflow", ("solver",), self.version
            )
            if int(self.version) >= 231
            else None,
        }
        if not self._static_info["solverworkflow"]:
            del self._static_info["solverworkflow"]
        self._delete_generated_files()
        self._populate_static_info()

    def _get_static_info(self, rules: str, session: Session):
        request = DataModelProtoModule.GetStaticInfoRequest()
        request.rules = rules
        response = session.datamodel_service_se.get_static_info(request)
        return response.info

    def _populate_static_info(self):
        run_meshing_mode = any(
            "meshing" in info.modes for _, info in self._static_info.items()
        )
        run_solver_mode = any(
            "solver" in info.modes for _, info in self._static_info.items()
        )
        run_icing_mode = int(self.version) >= 231 and any(
            "flicing" in info.modes for _, info in self._static_info.items()
        )
        import ansys.fluent.core as pyfluent

        if run_meshing_mode:
            session = pyfluent.launch_fluent(mode="meshing")
            for _, info in self._static_info.items():
                if "meshing" in info.modes:
                    info.static_info = self._get_static_info(info.rules, session)
            session.exit()

        if run_solver_mode:
            session = pyfluent.launch_fluent(mode="solver")
            for _, info in self._static_info.items():
                if "solver" in info.modes:
                    info.static_info = self._get_static_info(info.rules, session)
            session.exit()

        if run_icing_mode:
            session = pyfluent.launch_fluent(mode="solver-icing")
            for _, info in self._static_info.items():
                if "flicing" in info.modes:
                    info.static_info = self._get_static_info(info.rules, session)
                    try:
                        if (
                            len(
                                info.static_info.singletons["Case"]
                                .singletons["App"]
                                .singletons
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
            session.exit()

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
        named_objects = sorted(info.namedobjects)
        singletons = sorted(info.singletons)
        parameters = sorted(info.parameters)
        commands = sorted(info.commands)
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
        f.write(f"{indent}        super().__init__(service, rules, path)\n\n")
        for k in named_objects:
            f.write(f"{indent}    class {k}(PyNamedObjectContainer):\n")
            f.write(f'{indent}        """\n')
            f.write(f"{indent}        .\n")
            f.write(f'{indent}        """\n')
            api_tree[f"{k}:<name>"] = self._write_static_info(
                f"_{k}", info.namedobjects[k], f, level + 2
            )
            # Specify the concrete named object type for __getitem__
            f.write(f"{indent}        def __getitem__(self, key: str) -> " f"_{k}:\n")
            f.write(f"{indent}            return super().__getitem__(key)\n\n")
        for k in singletons:
            if k.isidentifier():
                # print("included", k)
                api_tree[k] = self._write_static_info(
                    k, info.singletons[k], f, level + 1
                )
            else:
                # print("\t\texcluded", k)
                pass
        for k in parameters:
            k_type = _PY_TYPE_BY_DM_TYPE[info.parameters[k].type]
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
                f"{_build_parameter_docstring(k, info.parameters[k].type)}\n"
            )
            f.write(f'{indent}        """\n')
            f.write(f"{indent}        pass\n\n")
            api_tree[k] = "Parameter"
        for k in commands:
            f.write(f"{indent}    class {k}(PyCommand):\n")
            f.write(f'{indent}        """\n')
            f.write(
                _build_command_docstring(
                    k, info.commands[k].commandinfo, f"{indent}        "
                )
            )
            f.write(f'{indent}        """\n')
            f.write(f"{indent}        pass\n\n")
            api_tree[k] = "Command"
        return api_tree

    def _write_doc_for_model_object(
        self, info, doc_dir: Path, heading, module_name, class_name, noindex=True
    ) -> None:
        doc_dir.mkdir(exist_ok=True)
        index_file = doc_dir / "index.rst"
        with open(index_file, "w", encoding="utf8") as f:
            ref = "_ref_" + "_".join([x.strip("_") for x in heading.split(".")])
            f.write(f".. {ref}:\n\n")
            if class_name == "Root":
                heading_ = heading.replace("_", "\_")
            else:
                heading_ = class_name.split(".")[-1]
            f.write(f"{heading_}\n")
            f.write(f"{'=' * len(heading_)}\n")
            f.write("\n")

            named_objects = sorted(info.namedobjects)
            singletons = sorted(info.singletons)
            parameters = sorted(info.parameters)
            commands = sorted(info.commands)

            f.write(f".. autoclass:: {module_name}.{class_name}\n")
            if noindex:
                f.write("   :noindex:\n")
            f.write("   :members:\n")
            f.write("   :show-inheritance:\n")
            f.write("   :undoc-members:\n")
            f.write('   :exclude-members: "__weakref__, __dict__"\n')
            f.write('   :special-members: " __init__"\n')
            f.write("   :autosummary:\n\n")

            if singletons or named_objects:
                f.write(".. toctree::\n")
                f.write("   :hidden:\n\n")

                for k in singletons:
                    if k.isidentifier():
                        f.write(f"   {k}/index\n")
                        self._write_doc_for_model_object(
                            info.singletons[k],
                            doc_dir / k,
                            heading + "." + k,
                            module_name,
                            class_name + "." + k,
                        )

                for k in named_objects:
                    f.write(f"   {k}/index\n")
                    self._write_doc_for_model_object(
                        info.namedobjects[k],
                        doc_dir / k,
                        heading + "." + k,
                        module_name,
                        f"{class_name}.{k}._{k}",
                    )

    def write_static_info(self) -> None:
        api_tree = {"<meshing_session>": {}, "<solver_session>": {}}
        for mode in ["meshing", "solver"]:
            doc_dir = Path(
                _MESHING_DM_DOC_DIR if mode == "meshing" else _SOLVER_DM_DOC_DIR
            )
            doc_dir.mkdir(exist_ok=True)
            index_file = doc_dir / "index.rst"
            with open(index_file, "w", encoding="utf8") as f:
                f.write(f".. _ref_{mode}_datamodel:\n\n")
                heading = mode + ".datamodel"
                f.write(f"{heading}\n")
                f.write(f"{'=' * len(heading)}\n")
                f.write("\n")
                f.write(f".. currentmodule:: ansys.fluent.core.datamodel\n\n")
                f.write(".. autosummary::\n")
                f.write("   :toctree: _autosummary\n\n")
                f.write(".. toctree::\n")
                f.write("   :hidden:\n\n")

        for name, info in self._static_info.items():
            if info.static_info == None:
                continue
            with open(info.filepath, "w", encoding="utf8") as f:
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
                f.write("    PyCommand\n")
                f.write(")\n\n\n")
                api_tree_val = {
                    name: self._write_static_info("Root", info.static_info, f)
                }
                mode_to_dir = dict(
                    meshing=_MESHING_DM_DOC_DIR,
                    solver=_SOLVER_DM_DOC_DIR,
                    flicing=_SOLVER_DM_DOC_DIR,
                )
                for mode in info.modes:
                    if mode in ("solver", "meshing"):
                        key = f"<{mode}_session>"
                        api_tree[key].update(api_tree_val)
                    dir_type = mode_to_dir.get(mode)
                    first_heading = "solver" if mode == "flicing" else mode
                    if dir_type:
                        doc_dir = Path(dir_type)
                        index_file = doc_dir / "index.rst"
                        with open(index_file, "a", encoding="utf8") as f:
                            f.write(f"   {name}/index\n")
                        self._write_doc_for_model_object(
                            info=info.static_info,
                            doc_dir=doc_dir / name,
                            heading=f"{first_heading}.datamodel.{name}",
                            module_name=f"ansys.fluent.core.datamodel_{self.version}.{name}",
                            class_name="Root",
                            noindex=len(info.modes) > 1 and mode != "solver",
                        )
        return api_tree

    def _delete_generated_files(self):
        for _, info in self._static_info.items():
            if info.filepath.exists():
                info.filepath.unlink()
        if Path(_MESHING_DM_DOC_DIR).exists():
            shutil.rmtree(Path(_MESHING_DM_DOC_DIR))
        if Path(_SOLVER_DM_DOC_DIR).exists():
            shutil.rmtree(Path(_SOLVER_DM_DOC_DIR))


def generate(version, pyfluent_path):
    return DataModelGenerator(version, pyfluent_path).write_static_info()


if __name__ == "__main__":
    version = get_version_for_filepath()
    generate(version, None)
