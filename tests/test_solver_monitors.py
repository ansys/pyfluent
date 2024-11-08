import pytest

from ansys.fluent.core import examples
from ansys.fluent.core.utils.execution import timeout_loop


@pytest.mark.fluent_version(">=23.2")
def test_solver_monitors(new_solver_session):

    solver = new_solver_session

    import_case = examples.download_file(
        file_name="exhaust_system.cas.h5", directory="pyfluent/exhaust_system"
    )

    solver.file.read_case(file_name=import_case)

    ordered_report_plot_names = [
        "mass-bal-rplot",
        "mass-in-rplot",
        "mass-tot-rplot",
        "point-vel-rplot",
    ]

    assert (
        sorted(solver.settings.solution.monitor.report_plots())
        == ordered_report_plot_names
    )

    # monitor set names unavailable without data
    assert len(solver.monitors.get_monitor_set_names()) == 0

    import_data = examples.download_file(
        file_name="exhaust_system.dat.h5", directory="pyfluent/exhaust_system"
    )

    solver.file.read_data(file_name=import_data)

    # monitor set names remains unavailable after loading data
    assert len(solver.monitors.get_monitor_set_names()) == 0

    # monitor set names becomes available after initializing
    solver.solution.initialization.hybrid_initialize()

    monitor_set_names = ordered_report_plot_names + ["residual"]
    assert sorted(solver.monitors.get_monitor_set_names()) == sorted(monitor_set_names)

    # no data in monitors at this point
    assert all(
        all(
            len(elem) == 0
            for elem in solver.monitors.get_monitor_set_data(monitor_set_name=name)
        )
        for name in monitor_set_names
    ), "One or more monitor sets contain non-empty elements."

    # run the solver...
    solver.solution.run_calculation.iterate(iter_count=1)

    # ...data is in monitors
    assert all(
        all(
            len(elem) != 0
            for elem in solver.monitors.get_monitor_set_data(monitor_set_name=name)
        )
        for name in monitor_set_names
    ), "One or more monitor sets contain empty elements."

    def monitor_callback():
        monitor_callback.called = True

    monitor_callback.called = False

    # n.b. there is no checking of the callback signature at registration. Instead
    # we would get a TypeError at callback time if the signature is wrong. The correct
    # signature is undocumented.
    solver.monitors.register_callback(monitor_callback)

    # trigger callback by running the solver
    assert not monitor_callback.called
    solver.solution.run_calculation.iterate(iter_count=1)
    assert timeout_loop(lambda: monitor_callback.called, 5)
    assert monitor_callback.called
