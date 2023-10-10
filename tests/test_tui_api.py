import pytest
from util.meshing_workflow import new_mesh_session  # noqa: F401
from util.solver_workflow import new_solver_session  # noqa: F401

from ansys.fluent.core.services.datamodel_tui import TUIMenu


@pytest.mark.skip("randomly failing due to missing transcript capture")
def test_report_system_proc_stats_tui(new_solver_session, capsys) -> None:
    new_solver_session.transcript.start()
    # Issue: Transcript missing for the first TUI command
    new_solver_session.solver.tui.report.system.sys_stats()
    new_solver_session.solver.tui.report.system.sys_stats()
    captured = capsys.readouterr()
    assert "CPU" in captured.out


def test_runtime_tui_menus(load_static_mixer_case) -> None:
    solver = load_static_mixer_case
    solver.tui.define.models.addon_module(3)
    rmf = solver.tui.define.models.resolved_MEA_fuelcells
    assert rmf is not None
    assert rmf.__class__ == TUIMenu


def test_python_keyword_menu_name(new_mesh_session):
    meshing = new_mesh_session
    assert "cad_options" in dir(meshing.tui.file.import_)
    assert "create_cad_assemblies" in dir(meshing.tui.file.import_.cad_options)
    meshing.tui.file.import_.cad_options.create_cad_assemblies("yes")
