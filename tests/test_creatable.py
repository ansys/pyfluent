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
def test_creatable(mixing_elbow_case_data_session) -> None:
    solver = mixing_elbow_case_data_session
    fluent_version = solver.get_fluent_version()
    has_not = (
        solver.setup.boundary_conditions.velocity_inlet,
        solver.setup.cell_zone_conditions.fluid,
    )
    has = (
        solver.results.graphics.contour,
        solver.results.graphics.vector,
    )

    for obj in has_not:
        # creatability condition is dynamic since 25.1
        if fluent_version >= FluentVersion.v251:
            assert not getattr(obj, "create").is_active()
        else:
            assert not hasattr(obj, "create")
            assert "create" not in dir(obj)

    for obj in has:
        assert hasattr(obj, "create")
        assert "create" in dir(obj)
        if fluent_version >= FluentVersion.v251:
            assert getattr(obj, "create").is_active()
