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
@pytest.mark.fluent_version("latest")
def test_post_elbow(mixing_elbow_settings_session):
    mixing_elbow_settings_session.results.graphics.vector[
        "velocity_vector_symmetry"
    ] = {}
    vector_graphics = mixing_elbow_settings_session.results.graphics.vector[
        "velocity_vector_symmetry"
    ]
    vector_graphics.field = "temperature"
    vector_graphics.surfaces_list = ["symmetry-xyplane"]
    vector_graphics.scale.scale_f = 4
    vector_graphics.style = "arrow"
    vel_vector = vector_graphics()
    assert vel_vector.get("name") == "velocity_vector_symmetry"
    assert vel_vector.get("field") == "temperature"
    assert vel_vector.get("surfaces_list") == ["symmetry-xyplane"]
    assert vel_vector.get("scale") == {"auto_scale": True, "scale_f": 4.0}
    assert vel_vector.get("style") == "arrow"
