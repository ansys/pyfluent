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

from ansys.fluent.core.utils.fluent_version import FluentVersion


@pytest.mark.fluent_version("latest")
def test_solver_calculation(static_mixer_case_session):
    solver_session = static_mixer_case_session
    scheme_eval = solver_session.scheme_eval.scheme_eval
    assert scheme_eval("(client-get-var 'residuals/plot?)") is True
    # TODO: Remove the if condition after a stable version of 23.1 is available and update the commands as required.
    if solver_session.get_fluent_version() < FluentVersion.v231:
        solver_session.tui.solve.monitors.residual.plot("no")
        assert scheme_eval("(client-get-var 'residuals/plot?)") is False
    assert scheme_eval("(data-valid?)") is False
    solver_session.solution.initialization.hybrid_initialize()
    assert scheme_eval("(data-valid?)") is True
    # solver_session.solution.run_calculation.iterate.get_attr("arguments")
    # solver_session.solution.run_calculation.number_of_iterations = 5
    # assert solver_session.solution.run_calculation.number_of_iterations == 5
