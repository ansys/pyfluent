import ansys.fluent.core as pyfluent


def test_report_system_proc_stats_tui(with_running_pytest, capsys) -> None:
    session = pyfluent.launch_fluent()
    session.start_transcript()
    # Issue: Transcript missing for the first TUI command
    session.tui.solver.report.system.proc_stats()
    session.tui.solver.report.system.proc_stats()
    captured = capsys.readouterr()
    assert "Virtual Mem Usage" in captured.out
