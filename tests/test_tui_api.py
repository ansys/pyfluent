import pytest
from util.solver_workflow import new_solver_session  # noqa: F401


@pytest.mark.skip("randomly failing due to missing transcript capture")
def test_report_system_proc_stats_tui(new_solver_session, capsys) -> None:
    new_solver_session.transcript.start()
    # Issue: Transcript missing for the first TUI command
    new_solver_session.solver.tui.report.system.sys_stats()
    new_solver_session.solver.tui.report.system.sys_stats()
    captured = capsys.readouterr()
    assert "CPU" in captured.out
