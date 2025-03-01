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

from ansys.fluent.core.examples import download_file, path
from ansys.fluent.core.filereader.casereader import CaseReader


def test_get_and_set_rp_vars(new_solver_session) -> None:
    case_path = download_file("Static_Mixer_main.cas.h5", "pyfluent/static_mixer")
    solver = new_solver_session
    solver.tui.file.read_case(case_path)
    rp_vars = solver.rp_vars

    # simple integer
    iter_count = 54321
    rp_vars("number-of-iterations", iter_count)
    assert iter_count == rp_vars("number-of-iterations")

    # complex list structure
    before_init_mod = rp_vars("strategy/solution-strategy/before-init-modification")
    assert before_init_mod[1][1][1] == ("value", False)
    before_init_mod[1][1][1] = ("value", True)
    rp_vars("strategy/solution-strategy/before-init-modification", before_init_mod)
    before_init_mod_2 = rp_vars("strategy/solution-strategy/before-init-modification")
    assert before_init_mod_2[1][1][1] == ("value", True)


@pytest.mark.fluent_version(">=23.1, !=24.1")
def test_get_all_rp_vars(new_solver_session) -> None:
    case_path = download_file("Static_Mixer_main.cas.h5", "pyfluent/static_mixer")
    solver = new_solver_session
    solver.tui.file.read_case(case_path)
    rp_vars = solver.rp_vars
    # all vars
    all_vars = rp_vars()
    assert len(all_vars) == pytest.approx(9000, 10)

    # refresh
    solver.file.write(file_type="case", file_name=case_path)
    solver.tui.file.read_case(case_path)

    # all vars again
    all_vars = rp_vars()
    assert len(all_vars) == pytest.approx(9000, 20)

    # CaseFile comparison, note that the PyFluent work dir is not necessarily the same as the Fluent work dir
    case = CaseReader(case_file_name=path(case_path))
    case_vars = case.rp_vars()
    assert len(case_vars) == pytest.approx(9000, 450)


@pytest.mark.fluent_version(">=23.2")
def test_rp_vars_allowed_values(new_solver_session) -> None:
    solver = new_solver_session
    rp_vars = solver.rp_vars

    assert rp_vars("number-of-iterations") == 0

    with pytest.raises(RuntimeError):
        rp_vars("number-of-iterat")

    assert "number-of-iterations" in rp_vars.allowed_values()


@pytest.mark.fluent_version(">=23.2")
def test_rp_vars_boolean(new_solver_session) -> None:
    solver = new_solver_session

    var_name = "rp-lam?"
    rp_vars = solver.rp_vars

    var_val = rp_vars(var_name)
    assert isinstance(var_val, bool)

    for i in range(10):
        var_val = not var_val
        rp_vars(var_name, var_val)
        assert rp_vars(var_name) == var_val
