import os

import pytest

from ansys.fluent.core import FluentVersion
from ansys.fluent.core.examples.downloads import download_file
from ansys.fluent.core.services.datamodel_tui import TUIMenu


@pytest.mark.skip("Failing in github")
def test_report_system_proc_stats_tui(new_solver_session, capsys) -> None:
    new_solver_session.tui.report.system.sys_stats()
    captured = capsys.readouterr()
    assert "CPU" in captured.out


def test_runtime_tui_menus(static_mixer_case_session) -> None:
    solver = static_mixer_case_session
    solver.tui.define.models.addon_module(3)
    rmf = solver.tui.define.models.resolved_MEA_fuelcells
    assert rmf is not None
    assert rmf.__class__ == TUIMenu


@pytest.mark.codegen_required
def test_python_keyword_menu_name(new_meshing_session):
    meshing = new_meshing_session
    assert "cad_options" in dir(meshing.tui.file.import_)
    assert "create_cad_assemblies" in dir(meshing.tui.file.import_.cad_options)
    meshing.tui.file.import_.cad_options.create_cad_assemblies("yes")


@pytest.mark.skip("Failing in github")
def test_api_upgrade_message(new_solver_session):
    solver = new_solver_session
    case_name = download_file(
        "Static_Mixer_main.cas.h5", "pyfluent/static_mixer", save_path=os.getcwd()
    )
    from contextlib import redirect_stdout
    import io

    f = io.StringIO()
    with redirect_stdout(f):
        solver.tui.file.read_case(case_name)
    s = f.getvalue()
    if solver.get_fluent_version() >= FluentVersion.v251:
        assert (
            s.split("\n")[-2].split("(")[0]
            == r"<solver_session>.settings.file.read_case"
        )
    else:
        assert s.split("\n")[-2].split("(")[0] == r"<solver_session>.file.read_case"


def test_exit_not_in_meshing_tui(new_meshing_session):
    meshing = new_meshing_session

    assert "exit" not in dir(meshing.tui)

    with pytest.raises(AttributeError):
        meshing.tui.exit()


def test_commands_not_in_solver_tui(new_solver_session):
    solver = new_solver_session

    for command in ["exit", "switch_to_meshing_mode"]:
        assert command not in dir(solver.tui)
        with pytest.raises(AttributeError):
            getattr(solver.tui, command)
