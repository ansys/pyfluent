# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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

    assert timeout_loop(
        lambda: sorted(solver.settings.solution.monitor.report_plots())
        == ordered_report_plot_names,
        5,
    )

    # monitor set names unavailable without data
    assert timeout_loop(lambda: len(solver.monitors.get_monitor_set_names()) == 0, 5)

    import_data = examples.download_file(
        file_name="exhaust_system.dat.h5", directory="pyfluent/exhaust_system"
    )

    solver.file.read_data(file_name=import_data)

    # monitor set names remains unavailable after loading data
    assert timeout_loop(lambda: len(solver.monitors.get_monitor_set_names()) == 0, 5)

    # monitor set names becomes available after initializing
    solver.solution.initialization.hybrid_initialize()

    monitor_set_names = ordered_report_plot_names + ["residual"]
    assert timeout_loop(
        lambda: sorted(solver.monitors.get_monitor_set_names())
        == sorted(monitor_set_names),
        5,
    )

    # no data in monitors at this point
    def all_elements_empty(name):
        monitor_data = solver.monitors.get_monitor_set_data(monitor_set_name=name)
        return all(len(elem) == 0 for elem in monitor_data)

    for name in monitor_set_names:
        assert timeout_loop(
            all_elements_empty,
            timeout=5,
            args=(name,),
        ), f"Monitor set '{name}' contains non-empty elements."

    # run the solver...
    solver.solution.run_calculation.iterate(iter_count=1)

    # ...data is in monitors
    def all_elements_non_empty(name):
        monitor_data = solver.monitors.get_monitor_set_data(monitor_set_name=name)
        return all(len(elem) != 0 for elem in monitor_data)

    for name in monitor_set_names:
        assert timeout_loop(
            all_elements_non_empty,
            timeout=5,
            args=(name,),
        ), f"Monitor set '{name}' contains one or more empty elements."

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
