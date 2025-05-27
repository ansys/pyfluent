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


@pytest.mark.nightly
@pytest.mark.fluent_version("==23.2")
def test_allowed_values_on_report_definitions_1364(new_solver_session):
    solver = new_solver_session

    import_file_name = examples.download_file(
        "elbow.cas.h5", "pyfluent/examples/DOE-ML-Mixing-Elbow"
    )

    solver.file.read(
        file_name=import_file_name, file_type="case", lightweight_setup=True
    )

    report_def = solver.solution.report_definitions.volume.create("xxx")

    report_def.set_state(
        {
            "report_type": "volume-max",
            "field": "temperature",
            "average_over": 1,
            "per_zone": False,
            "zone_names": ["fluid"],
            "expr_list": None,
        }
    )

    assert report_def.zone_names.allowed_values() == ["fluid"]

    assert report_def.expr_list.allowed_values() is None


@pytest.mark.fluent_version(">=23.2")
def test_monitors_list_set_data_637_974_1744_2188(new_solver_session):
    solver_session = new_solver_session

    import_case = examples.download_file(
        file_name="exhaust_system.cas.h5", directory="pyfluent/exhaust_system"
    )

    examples.download_file(
        file_name="exhaust_system.dat.h5", directory="pyfluent/exhaust_system"
    )

    solver_session.file.read_case_data(file_name=import_case)
    solver_session.solution.run_calculation.iterate(iter_count=1)

    monitors_list = solver_session.monitors.get_monitor_set_names()

    assert monitors_list == [
        "residual",
        "mass-bal-rplot",
        "mass-tot-rplot",
        "mass-in-rplot",
        "point-vel-rplot",
    ]

    mp = solver_session.monitors.get_monitor_set_data(monitor_set_name="residual")

    assert mp

    sample_report_plot = solver_session.solution.monitor.report_plots.create(
        "sample-report-plot"
    )
    sample_report_plot.report_defs = "mass-bal"

    solver_session.solution.initialization.hybrid_initialize()
    solver_session.solution.run_calculation.iterate(iter_count=1)

    new_monitors_list = solver_session.monitors.get_monitor_set_names()

    assert new_monitors_list == [
        "residual",
        "mass-bal-rplot",
        "mass-tot-rplot",
        "mass-in-rplot",
        "point-vel-rplot",
        "sample-report-plot",
    ]


@pytest.mark.fluent_version(">=24.2")
def test_empty_vector_field_data_2339(new_solver_session):
    solver = new_solver_session

    import_case = examples.download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")

    import_data = examples.download_file("mixing_elbow.dat.h5", "pyfluent/mixing_elbow")

    assert import_case
    assert import_data

    solver.file.read_case(file_name=import_case)

    solver.file.read_data(file_name=import_data)

    assert [
        a[0]
        for a in solver.fields.field_data.get_vector_field_data(
            field_name="velocity", surfaces=[1]
        )[1]
    ][:5]
