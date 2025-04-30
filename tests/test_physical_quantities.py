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

import ansys.fluent.core as pf  # noqa: F401
from ansys.fluent.core import examples
from ansys.physicalquantities import PhysicalQuantities


def test_field_data_transactions_deprecated_interface(new_solver_session) -> None:
    solver = new_solver_session
    case_name = examples.download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
    solver.file.read(file_type="case", file_name=case_name)

    solver.settings.solution.initialization.hybrid_initialize()

    temperature = PhysicalQuantities.TEMPERATURE

    temperature_field_data = solver.fields.field_data.get_scalar_field_data(
        field_name=temperature, surfaces=["hot-inlet"]
    )
    assert round(temperature_field_data["hot-inlet"][0]) == 305

    temperature_min = solver.fields.reduction.minimum(
        expression=temperature, locations=["hot-inlet"]
    )
    assert round(temperature_min) == 313

    temperature_solution_data = solver.fields.solution_variable_data.get_data(
        solution_variable_name=temperature, zone_names=["hot-inlet"]
    )
    assert round(temperature_solution_data["hot-inlet"][0]) == 313
