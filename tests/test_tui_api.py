from util.solver_workflow import new_solver_session  # noqa: F401


def test_report_system_proc_stats_tui(new_solver_session, capsys) -> None:
    new_solver_session.start_transcript()
    # Issue: Transcript missing for the first TUI command
    new_solver_session.tui.solver.report.system.proc_stats()
    new_solver_session.tui.solver.report.system.proc_stats()
    captured = capsys.readouterr()
    assert "Virtual Mem Usage" in captured.out
