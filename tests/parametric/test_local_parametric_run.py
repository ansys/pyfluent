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
from ansys.fluent.core.parametric import (
    LocalParametricStudy,
    convert_design_point_parameter_units,
)


@pytest.mark.standalone
def test_local_parametric_run():
    case_filepath = examples.download_file(
        "Static_Mixer_Parameters.cas.h5",
        "pyfluent/static_mixer",
        return_without_path=False,
    )

    local_study = LocalParametricStudy(case_filepath=case_filepath)

    for idx in range(4):
        design_point = local_study.add_design_point("dp_" + str(idx))
        design_point.input_parameters["inlet1_vel"] = float(2 + idx)

    local_study.run_in_fluent(num_servers=2)

    table = local_study.design_point_table

    assert len(table) == 5

    for point in table:
        ins = convert_design_point_parameter_units(point.input_parameters)
        outs = point.output_parameters
        new_inlet_velocity = ins["inlet1_vel"]
        new_outlet_velocity = outs["outlet-vel-avg-op"]
        assert new_inlet_velocity
        assert new_outlet_velocity
