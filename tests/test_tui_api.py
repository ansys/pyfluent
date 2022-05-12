from util.solver_workflow import new_solver_session  # noqa: F401


def test_report_summary_tui(new_solver_session, capsys) -> None:
    new_solver_session.start_transcript()
    # Issue: Transcript missing for the first TUI command
    new_solver_session.tui.solver.report.summary("no")
    new_solver_session.tui.solver.report.summary("no")
    captured = capsys.readouterr()
    assert "Fluent" in captured.out
