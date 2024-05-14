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
    static_infos[
        StaticInfoType.TUI_SOLVER if mode == "solver" else StaticInfoType.TUI_MESHING
    ] = {
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
