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


@pytest.mark.settings_only
@pytest.mark.fluent_version(">=24.1")
def test_expression(mixing_elbow_settings_session):
    solver_session = mixing_elbow_settings_session
    # Case file already has energy model turned on
    # solver_session.setup.models.energy.enabled = True
    expressions = solver_session.setup.named_expressions
    expressions["r"] = {}
    expressions["r"] = {"definition": "(Position.z**2.0 +Position.x**2.0)**0.5"}
    expressions["r1"] = {}
    expressions["r1"] = {"definition": "1-(r/0.014[m])"}
    expressions["v1"] = {}
    expressions["v1"] = {"definition": "r1**(1.0/6.0)"}
    expressions["vel_cold"] = {}
    expressions["vel_cold"] = {"definition": "1.264 * 1.43 [m s^-1] * max(0,v1)"}

    assert expressions["r"].definition() == "(Position.z**2.0 +Position.x**2.0)**0.5"
    assert expressions["r1"].definition() == "1-(r/0.014[m])"
    assert expressions["v1"].definition() == "r1**(1.0/6.0)"
    assert expressions["vel_cold"].definition() == "1.264 * 1.43 [m s^-1] * max(0,v1)"

    velocity_inlet = solver_session.setup.boundary_conditions.velocity_inlet
    velocity_inlet["cold-inlet"].momentum = {"velocity": "vel_cold"}
    velocity_inlet["hot-inlet"].momentum = {"velocity": "max(vel_cold, 1.5 [m/s])"}
    assert velocity_inlet["cold-inlet"].momentum.velocity() == {
        "option": "value",
        "value": "vel_cold",
    }
    assert velocity_inlet["hot-inlet"].momentum.velocity() == {
        "option": "value",
        "value": "max(vel_cold, 1.5 [m/s])",
    }
