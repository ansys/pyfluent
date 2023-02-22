import pytest
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
