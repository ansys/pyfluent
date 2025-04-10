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

import time

import pytest


@pytest.mark.fluent_version(">=23.1")
@pytest.mark.parametrize(
    "error_code,raises",
    [
        (0, pytest.wont_raise()),
        (1, pytest.raises(RuntimeError)),
    ],
)
def test_fluent_fatal_error(error_code, raises, new_solver_session):
    scheme_eval = new_solver_session.scheme_eval.scheme_eval
    with raises:
        scheme_eval(
            "(events/transmit 'error-event "
            f'(cons (format #f "fatal error: ~a~%" "testing") {error_code}))'
        )
        for _ in range(10):
            # as these are mostly instant, exception should usually be raised on the second gRPC call
            scheme_eval("(pp 'fatal_error_testing)")
            time.sleep(0.1)


@pytest.mark.fluent_version(">=25.2")
def test_custom_python_error_via_grpc(datamodel_api_version_new, new_solver_session):
    solver = new_solver_session
    # This may need to be updated if the error type changes in the server
    with pytest.raises(RuntimeError, match="prefereces not found!"):
        solver._se_service.get_state("prefereces", "General")
    with pytest.raises(ValueError, match="Datamodel rules for prefereces not found!"):
        solver._se_service.get_specs("prefereces", "General")
