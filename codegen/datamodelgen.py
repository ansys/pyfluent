from io import FileIO
import os
from pathlib import Path
import shutil
from typing import Any, Dict

from ansys.api.fluent.v0 import datamodel_se_pb2 as DataModelProtoModule
from ansys.fluent.core.session import _BaseSession as Session
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
        "core",
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
        "core",
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
    def __init__(
        self, rules: str, modes: tuple, version: str, rules_save_name: str = ""
    ):
        self.rules = rules
        self.modes = modes
        self.static_info = None
        if rules_save_name == "":
            rules_save_name = rules
        datamodel_dir = (
            _THIS_DIR
            / ".."
            / "src"
            / "ansys"
            / "fluent"
            / "core"
            / f"datamodel_{version}"
        )
        datamodel_dir.mkdir(exist_ok=True)
        self.filepath = (datamodel_dir / f"{rules_save_name}.py").resolve()


class DataModelGenerator:
    def __init__(self):
        self.version = get_version_for_filepath()
        self._static_info: Dict[str, DataModelStaticInfo] = {
            "workflow": DataModelStaticInfo("workflow", ("meshing",), self.version),
            "meshing": DataModelStaticInfo("meshing", ("meshing",), self.version),
            "PartManagement": DataModelStaticInfo(
                "PartManagement", ("meshing",), self.version
            ),
            "PMFileManagement": DataModelStaticInfo(
                "PMFileManagement", ("meshing",), self.version
            ),
            "icing": DataModelStaticInfo(
                "flserver", ("flicing",), self.version, "flicing"
            ),
            "preferences": DataModelStaticInfo(
                "preferences", ("meshing", "solver", "flicing,"), self.version
            ),
        }
        self._delete_generated_files()
        self._populate_static_info()

    def _get_static_info(self, rules: str, session: Session):
        request = DataModelProtoModule.GetStaticInfoRequest()
        request.rules = rules
        response = session.fluent_connection.datamodel_service_se.get_static_info(
            request
        )
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
        if " " in name:
            return
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
            if " " not in k:
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
            self._write_static_info(f"_{k}", info.namedobjects[k], f, level + 2)
            # Specify the concrete named object type for __getitem__
            f.write(f"{indent}        def __getitem__(self, key: str) -> " f"_{k}:\n")
            f.write(f"{indent}            return super().__getitem__(key)\n\n")
        for k in singletons:
            if " " not in k:
                print("included", k)
                self._write_static_info(k, info.singletons[k], f, level + 1)
            else:
                print("\t\texcluded", k)
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

    def _write_doc_for_model_object(
        self, info, doc_dir: Path, heading, module_name, class_name
    ) -> None:
        doc_dir.mkdir(exist_ok=True)
        index_file = doc_dir / "index.rst"
        with open(index_file, "w", encoding="utf8") as f:
            ref = "_ref_" + "_".join([x.strip("_") for x in heading.split(".")])
            f.write(f".. {ref}:\n\n")
            heading_ = heading.replace("_", "\_")
            f.write(f"{heading_}\n")
            f.write(f"{'=' * len(heading_)}\n")
            f.write("\n")
            f.write(f".. currentmodule:: {module_name}\n\n")
            f.write(".. autosummary::\n")
            f.write("   :toctree: _autosummary\n\n")

            named_objects = sorted(info.namedobjects)
            singletons = sorted(info.singletons)
            parameters = sorted(info.parameters)
            commands = sorted(info.commands)

            f.write(f".. autoclass:: {module_name}::{class_name}\n")
            if parameters or commands:
                f.write(f"   :members: {', '.join(parameters + commands)}\n\n")

            if singletons or named_objects:
                f.write(".. toctree::\n")
                f.write("   :hidden:\n\n")

                for k in singletons:
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
                self._write_static_info("Root", info.static_info, f)
                doc_dir = Path(
                    _MESHING_DM_DOC_DIR
                    if "meshing" in info.modes
                    else _SOLVER_DM_DOC_DIR
                )
                index_file = doc_dir / "index.rst"
                with open(index_file, "a", encoding="utf8") as f:
                    f.write(f"   {name}/index\n")
                self._write_doc_for_model_object(
                    info.static_info,
                    doc_dir / name,
                    f"{info.modes[0]}.datamodel.{name}",
                    f"ansys.fluent.core.datamodel_{self.version}.{name}",
                    "Root",
                )

    def _delete_generated_files(self):
        for _, info in self._static_info.items():
            if info.filepath.exists():
                info.filepath.unlink()
        if Path(_MESHING_DM_DOC_DIR).exists():
            shutil.rmtree(Path(_MESHING_DM_DOC_DIR))
        if Path(_SOLVER_DM_DOC_DIR).exists():
            shutil.rmtree(Path(_SOLVER_DM_DOC_DIR))


def generate():
    DataModelGenerator().write_static_info()


if __name__ == "__main__":
    generate()
