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

from ansys.fluent.core import examples
from ansys.fluent.core.parametric import LocalParametricStudy


def test_local_parametric_setup():
    case_filepath = examples.download_file(
        "Static_Mixer_Parameters.cas.h5",
        "pyfluent/static_mixer",
        return_without_path=False,
    )

    local_study = LocalParametricStudy(case_filepath=case_filepath)

    base_design_point = local_study.design_point("Base DP")

    input_parameters = base_design_point.input_parameters

    assert len(input_parameters) == 4

    assert input_parameters["inlet1_temp"] == "300 [K]"

    assert input_parameters["inlet1_vel"] == "1 [m/s]"

    assert input_parameters["inlet2_temp"] == "350 [K]"

    assert input_parameters["inlet2_vel"] == "1 [m/s]"

    output_parameters = base_design_point.output_parameters

    assert len(output_parameters) == 2

    assert not output_parameters["outlet-temp-avg-op"]

    assert not output_parameters["outlet-vel-avg-op"]
