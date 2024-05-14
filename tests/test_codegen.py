import importlib
from pathlib import Path
import pickle
import shutil
import tempfile

import pytest
from util.solver_workflow import new_solver_session  # noqa: F401

import ansys.fluent.core as pyfluent
from ansys.fluent.core.codegen import StaticInfoType, allapigen
from ansys.fluent.core.utils.fluent_version import get_version_for_file_name
from ansys.fluent.core.utils.search import get_api_tree_file_name


@pytest.mark.codegen_required
def test_allapigen_files(new_solver_session):
    version = get_version_for_file_name(session=new_solver_session)
    importlib.import_module(f"ansys.fluent.core.generated.fluent_version_{version}")
    importlib.import_module(f"ansys.fluent.core.generated.meshing.tui_{version}")
    importlib.import_module(f"ansys.fluent.core.generated.solver.tui_{version}")
    importlib.import_module(f"ansys.fluent.core.generated.datamodel_{version}.meshing")
    importlib.import_module(f"ansys.fluent.core.generated.datamodel_{version}.workflow")
    importlib.import_module(
        f"ansys.fluent.core.generated.datamodel_{version}.preferences"
    )
    importlib.import_module(
        f"ansys.fluent.core.generated.datamodel_{version}.PartManagement"
    )
    importlib.import_module(
        f"ansys.fluent.core.generated.datamodel_{version}.PMFileManagement"
    )
    importlib.import_module(
        f"ansys.fluent.core.generated.solver.settings_{version}.root"
    )


def test_codegen_with_no_static_info(tmp_path, monkeypatch):
    codegen_outdir = tmp_path / "generated"
    monkeypatch.setattr(pyfluent, "CODEGEN_OUTDIR", codegen_outdir)
    version = "251"
    allapigen.generate(version, {})
    generated_paths = list(codegen_outdir.iterdir())
    assert len(generated_paths) == 1
    assert set(p.name for p in generated_paths) == {f"api_tree_{version}.pickle"}
    api_tree_file = get_api_tree_file_name(version)
    with open(api_tree_file, "rb") as f:
        api_tree = pickle.load(f)
    assert api_tree == {"<meshing_session>": {}, "<solver_session>": {}}


def _get_nth_tui_command_static_info(n):
    return {f"C{n}": {"menus": {}, "commands": {}, "help": f"C{n} help"}}


def _get_nth_tui_menu_static_info(n, menus_static_info, commands_static_info):
    return {
        f"M{n}": {
            "menus": menus_static_info,
            "commands": commands_static_info,
            "help": f"M{n} help",
        }
    }


def _get_expected_tui_api_output(mode):
    return f'''"""Fluent {mode} TUI commands"""
#
# This is an auto-generated file.  DO NOT EDIT!
#
# pylint: disable=line-too-long

from ansys.fluent.core.services.datamodel_tui import PyMenu, TUIMenu, TUIMethod



class main_menu(TUIMenu):
    """
    Fluent {mode} main menu.
    """
    def __init__(self, service, version, mode, path):
        self.M1 = self.__class__.M1(service, version, mode, path + ["M1"])
        self.C1 = self.__class__.C1(service, version, mode, path + ["C1"])
        super().__init__(service, version, mode, path)
    class C1(TUIMethod):
        """
        C1 help.
        """

    class M1(TUIMenu):
        """
        M1 help.
        """
        def __init__(self, service, version, mode, path):
            self.M2 = self.__class__.M2(service, version, mode, path + ["M2"])
            self.C2 = self.__class__.C2(service, version, mode, path + ["C2"])
            super().__init__(service, version, mode, path)
        class C2(TUIMethod):
            """
            C2 help.
            """

        class M2(TUIMenu):
            """
            M2 help.
            """
            def __init__(self, service, version, mode, path):
                self.C3 = self.__class__.C3(service, version, mode, path + ["C3"])
                super().__init__(service, version, mode, path)
            class C3(TUIMethod):
                """
                C3 help.
                """
'''


@pytest.mark.parametrize("mode", ["solver", "meshing"])
def test_codegen_with_tui_solver_static_info(mode, monkeypatch):
    codegen_outdir = Path(tempfile.mkdtemp())
    monkeypatch.setattr(pyfluent, "CODEGEN_OUTDIR", codegen_outdir)
    version = "251"
    static_infos = {}
    static_info_type = (
        StaticInfoType.TUI_SOLVER if mode == "solver" else StaticInfoType.TUI_MESHING
    )
    static_infos[static_info_type] = {
        "menus": _get_nth_tui_menu_static_info(
            1,
            _get_nth_tui_menu_static_info(2, {}, _get_nth_tui_command_static_info(3)),
            _get_nth_tui_command_static_info(2),
        ),
        "commands": _get_nth_tui_command_static_info(1),
        "help": "Root",
    }
    allapigen.generate(version, static_infos)
    generated_paths = list(codegen_outdir.iterdir())
    assert len(generated_paths) == 2
    assert set(p.name for p in generated_paths) == {f"api_tree_{version}.pickle", mode}
    solver_paths = list((codegen_outdir / mode).iterdir())
    assert len(solver_paths) == 1
    assert set(p.name for p in solver_paths) == {f"tui_{version}.py"}
    with open(codegen_outdir / mode / f"tui_{version}.py", "r") as f:
        assert f.read() == _get_expected_tui_api_output(mode)
    api_tree_file = get_api_tree_file_name(version)
    with open(api_tree_file, "rb") as f:
        api_tree = pickle.load(f)
    tui_tree = {
        "tui": {"M1": {"M2": {"C3": "Command"}, "C2": "Command"}, "C1": "Command"}
    }
    api_tree_expected = {"<meshing_session>": {}, "<solver_session>": {}}
    api_tree_expected[f"<{mode}_session>"] = tui_tree
    assert api_tree == api_tree_expected
    shutil.rmtree(str(codegen_outdir))


_static_info_type_by_rules = {
    "workflow": StaticInfoType.DATAMODEL_WORKFLOW,
    "meshing": StaticInfoType.DATAMODEL_MESHING,
    "PartManagement": StaticInfoType.DATAMODEL_PART_MANAGEMENT,
    "PMFileManagement": StaticInfoType.DATAMODEL_PM_FILE_MANAGEMENT,
    "flicing": StaticInfoType.DATAMODEL_FLICING,
    "preferences": StaticInfoType.DATAMODEL_PREFERENCES,
    "solverworkflow": StaticInfoType.DATAMODEL_SOLVER_WORKFLOW,
    "MeshingUtilities": StaticInfoType.DATAMODEL_MESHING_UTILITIES,
}


def _get_datamodel_entity_static_info(
    name, singletons, namedobjects, commands, parameters
):
    return {
        name: {
            "singletons": singletons,
            "namedobjects": namedobjects,
            "commands": commands,
            "parameters": parameters,
        }
    }


def _get_datamodel_command_static_info(name, args, returntype):
    args = [{"name": arg[0], "type": arg[1]} for arg in args]
    return {name: {"commandinfo": {"args": args, "returntype": returntype}}}


_expected_datamodel_api_output = '''#
# This is an auto-generated file.  DO NOT EDIT!
#
# pylint: disable=line-too-long

from ansys.fluent.core.services.datamodel_se import (
    PyMenu,
    PyParameter,
    PyTextual,
    PyNumerical,
    PyDictionary,
    PyNamedObjectContainer,
    PyCommand,
    PyQuery
)


class Root(PyMenu):
    """
    Singleton Root.
    """
    def __init__(self, service, rules, path):
        self.N1 = self.__class__.N1(service, rules, path + [("N1", "")])
        self.S1 = self.__class__.S1(service, rules, path + [("S1", "")])
        self.P1 = self.__class__.P1(service, rules, path + [("P1", "")])
        self.C1 = self.__class__.C1(service, rules, "C1", path)
        super().__init__(service, rules, path)

    class N1(PyNamedObjectContainer):
        """
        .
        """
        class _N1(PyMenu):
            """
            Singleton _N1.
            """
            def __init__(self, service, rules, path):
                self.S3 = self.__class__.S3(service, rules, path + [("S3", "")])
                super().__init__(service, rules, path)

            class S3(PyMenu):
                """
                Singleton S3.
                """
                def __init__(self, service, rules, path):
                    super().__init__(service, rules, path)

        def __getitem__(self, key: str) -> _N1:
            return super().__getitem__(key)

    class S1(PyMenu):
        """
        Singleton S1.
        """
        def __init__(self, service, rules, path):
            self.S2 = self.__class__.S2(service, rules, path + [("S2", "")])
            self.P2 = self.__class__.P2(service, rules, path + [("P2", "")])
            self.C2 = self.__class__.C2(service, rules, "C2", path)
            super().__init__(service, rules, path)

        class S2(PyMenu):
            """
            Singleton S2.
            """
            def __init__(self, service, rules, path):
                super().__init__(service, rules, path)

        class P2(PyNumerical):
            """
            Parameter P2 of value type float.
            """
            pass

        class C2(PyCommand):
            """
            Command C2.

            Parameters
            ----------
            A2 : float

            Returns
            -------
            bool
            """
            pass

    class P1(PyTextual):
        """
        Parameter P1 of value type str.
        """
        pass

    class C1(PyCommand):
        """
        Command C1.

        Parameters
        ----------
        A1 : str

        Returns
        -------
        bool
        """
        pass

'''


@pytest.mark.parametrize(
    "rules",
    [
        "workflow",
        "meshing",
        "PartManagement",
        "PMFileManagement",
        "preferences",
        "solverworkflow",
        "MeshingUtilities",
    ],
)
def test_codegen_with_datamodel_static_info(monkeypatch, rules):
    codegen_outdir = Path(tempfile.mkdtemp())
    monkeypatch.setattr(pyfluent, "CODEGEN_OUTDIR", codegen_outdir)
    version = "251"
    static_infos = {}
    static_info_type = _static_info_type_by_rules[rules]
    static_infos[static_info_type] = {
        "singletons": _get_datamodel_entity_static_info(
            "S1",
            _get_datamodel_entity_static_info("S2", {}, {}, {}, {}),
            {},
            _get_datamodel_command_static_info("C2", [("A2", "Real")], "Logical"),
            {"P2": {"type": "Real"}},
        ),
        "namedobjects": _get_datamodel_entity_static_info(
            "N1", _get_datamodel_entity_static_info("S3", {}, {}, {}, {}), {}, {}, {}
        ),
        "commands": _get_datamodel_command_static_info(
            "C1", [("A1", "String")], "Logical"
        ),
        "parameters": {"P1": {"type": "String"}},
        "help": "Root",
    }
    allapigen.generate(version, static_infos)
    generated_paths = list(codegen_outdir.iterdir())
    assert len(generated_paths) == 2
    assert set(p.name for p in generated_paths) == {
        f"api_tree_{version}.pickle",
        f"datamodel_{version}",
    }
    datamodel_paths = list((codegen_outdir / f"datamodel_{version}").iterdir())
    assert len(datamodel_paths) == 1
    assert set(p.name for p in datamodel_paths) == {f"{rules}.py"}
    with open(codegen_outdir / f"datamodel_{version}" / f"{rules}.py", "r") as f:
        assert f.read() == _expected_datamodel_api_output
    api_tree_file = get_api_tree_file_name(version)
    with open(api_tree_file, "rb") as f:
        api_tree = pickle.load(f)
    datamodel_tree = {
        rules: {
            "C1": "Command",
            "N1:<name>": {"S3": {}},
            "P1": "Parameter",
            "S1": {"C2": "Command", "P2": "Parameter", "S2": {}},
        }
    }
    api_tree_expected = {"<meshing_session>": {}, "<solver_session>": {}}
    if rules in [
        "workflow",
        "meshing",
        "PartManagement",
        "PMFileManagement",
        "preferences",
        "MeshingUtilities",
    ]:
        api_tree_expected["<meshing_session>"] = datamodel_tree
    if rules in ["workflow", "flicing", "preferences", "solverworkflow"]:
        api_tree_expected["<solver_session>"] = datamodel_tree
    assert api_tree == api_tree_expected
    shutil.rmtree(str(codegen_outdir))
