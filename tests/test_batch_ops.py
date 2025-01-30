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

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples


@pytest.mark.fluent_version(">=24.1")
def test_batch_ops_create_mesh(new_solver_session):
    solver = new_solver_session
    mesh = solver.results.graphics.mesh
    case_file_name = examples.download_file(
        "mixing_elbow.cas.h5", "pyfluent/mixing_elbow"
    )
    with pyfluent.BatchOps(solver):
        solver.file.read(
            file_name=case_file_name, file_type="case", lightweight_setup=True
        )
        mesh["mesh-1"] = {}
        assert not solver.scheme_eval.scheme_eval("(case-valid?)")
        assert "mesh-1" not in mesh.get_object_names()
    assert solver.scheme_eval.scheme_eval("(case-valid?)")
    assert "mesh-1" in mesh.get_object_names()


@pytest.mark.fluent_version(">=24.1")
def test_batch_ops_create_mesh_and_access_fails(new_solver_session):
    solver = new_solver_session
    mesh = solver.results.graphics.mesh
    case_file_name = examples.download_file(
        "mixing_elbow.cas.h5", "pyfluent/mixing_elbow"
    )
    with pytest.raises(KeyError):
        with pyfluent.BatchOps(solver):
            solver.file.read(
                file_name=case_file_name, file_type="case", lightweight_setup=True
            )
            mesh["mesh-1"] = {}
            mesh["mesh-1"].surfaces_list = ["wall-elbow"]
    assert not solver.scheme_eval.scheme_eval("(case-valid?)")
