from io import FileIO
from pathlib import Path
from typing import Any

from ansys.api.fluent.v0 import datamodel_se_pb2 as DataModelProtoModule
from ansys.fluent.core.session import Session

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


def _build_singleton_docstring(name: str):
    return f"Singleton {name}."


def _build_parameter_docstring(name: str, t: str):
    return f"Parameter {name} of value type {_PY_TYPE_BY_DM_TYPE[t]}."


def _build_command_docstring(name: str, info: Any):
    return_type = _PY_TYPE_BY_DM_TYPE[info.returntype]
    arg_strings = [
        arg.name + ": " + _PY_TYPE_BY_DM_TYPE[arg.type] for arg in info.args
    ]
    arg_string = ", ".join(arg_strings)
    return name + "(" + arg_string + ") -> " + return_type


class DataModelStaticInfo:
    def __init__(self, rules: str, mode: str):
        self.rules = rules
        self.mode = mode
        self.static_info = None
        self.filepath = (
            _THIS_DIR
            / ".."
            / "src"
            / "ansys"
            / "fluent"
            / "core"
            / "datamodel"
            / f"{rules}.py"
        ).resolve()


class DataModelGenerator:
    def __init__(self):
        self._static_info = {
            "workflow": DataModelStaticInfo("workflow", "meshing"),
            "meshing": DataModelStaticInfo("meshing", "meshing"),
            "PartManagement": DataModelStaticInfo("PartManagement", "meshing"),
            "PMFileManagement": DataModelStaticInfo(
                "PMFileManagement", "meshing"
            ),
        }
        self._delete_generated_files()
        self._populate_static_info()

    def _get_static_info(self, rules: str, session: Session):
        request = DataModelProtoModule.GetStaticInfoRequest()
        request.rules = rules
        response = session._datamodel_service_se.get_static_info(request)
        return response.info

    def _populate_static_info(self):
        run_meshing_mode = any(
            info.mode == "meshing" for _, info in self._static_info.items()
        )
        run_solver_mode = any(
            info.mode == "solver" for _, info in self._static_info.items()
        )
        import ansys.fluent.core as pyfluent

        if run_meshing_mode:
            session = pyfluent.launch_fluent(meshing_mode=True)
            for _, info in self._static_info.items():
                if info.mode == "meshing":
                    info.static_info = self._get_static_info(
                        info.rules, session
                    )
            session.exit()

        if run_solver_mode:
            session = pyfluent.launch_fluent()
            for _, info in self._static_info.items():
                if info.mode == "solver":
                    info.static_info = self._get_static_info(
                        info.rules, session
                    )
            session.exit()

    def _write_static_info(
        self, name: str, info: Any, f: FileIO, level: int = 0
    ):
        indent = " " * level * 4
        f.write(f"{indent}class {name}(PyMenu):\n")
        f.write(f'{indent}    """\n')
        f.write(f"{indent}    {_build_singleton_docstring(name)}\n")
        f.write(f'{indent}    """\n')
        f.write(f"{indent}    def __init__(self, service, rules, path):\n")
        for k in info.namedobjects:
            f.write(
                f"{indent}        self.{k} = "
                f'self.__class__.{k}(service, rules, path + [("{k}", "")])\n'
            )
        for k in info.singletons:
            f.write(
                f"{indent}        self.{k} = "
                f'self.__class__.{k}(service, rules, path + [("{k}", "")])\n'
            )
        for k in info.parameters:
            f.write(
                f"{indent}        self.{k} = "
                f'self.__class__.{k}(service, rules, path + [("{k}", "")])\n'
            )
        for k in info.commands:
            f.write(
                f"{indent}        self.{k} = "
                f'self.__class__.{k}(service, rules, "{k}", path)\n'
            )
        f.write(f"{indent}        super().__init__(service, rules, path)\n\n")
        for k in info.namedobjects:
            f.write(f"{indent}    class {k}(PyNamedObjectContainer):\n")
            self._write_static_info(
                f"_{k}", info.namedobjects[k], f, level + 2
            )
            # Specify the concrete named object type for __getitem__
            f.write(
                f"{indent}        def __getitem__(self, key: str) -> "
                f"_{k}:\n"
            )
            f.write(f"{indent}            return super().__getitem__(key)\n\n")
        for k in info.singletons:
            self._write_static_info(k, info.singletons[k], f, level + 1)
        for k in info.parameters:
            f.write(f"{indent}    class {k}(PyMenu):\n")
            f.write(f'{indent}        """\n')
            f.write(
                f"{indent}        "
                f"{_build_parameter_docstring(k, info.parameters[k].type)}\n"
            )
            f.write(f'{indent}        """\n')
            f.write(f"{indent}        pass\n\n")
        for k in info.commands:
            f.write(f"{indent}    class {k}(PyCommand):\n")
            f.write(f'{indent}        """\n')
            f.write(
                f"{indent}        "
                f"{_build_command_docstring(k, info.commands[k].commandinfo)}"
                "\n"
            )
            f.write(f'{indent}        """\n')
            f.write(f"{indent}        pass\n\n")

    def write_static_info(self) -> None:
        for _, info in self._static_info.items():
            with open(info.filepath, "w", encoding="utf8") as f:
                f.write("#\n")
                f.write("# This is an auto-generated file.  DO NOT EDIT!\n")
                f.write("#\n")
                f.write("# pylint: disable=line-too-long\n\n")
                f.write(
                    "from ansys.fluent.core.services.datamodel_se import (\n"
                )
                f.write("    PyMenu,\n")
                f.write("    PyNamedObjectContainer,\n")
                f.write("    PyCommand\n")
                f.write(")\n\n\n")
                self._write_static_info("Root", info.static_info, f)

    def _delete_generated_files(self):
        for _, info in self._static_info.items():
            if info.filepath.exists():
                info.filepath.unlink()


if __name__ == "__main__":
    DataModelGenerator().write_static_info()
