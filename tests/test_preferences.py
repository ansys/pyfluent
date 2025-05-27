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

from ansys.fluent.core.services.datamodel_se import ReadOnlyObjectError


@pytest.mark.codegen_required
def test_solver_preferences(new_solver_session):
    solver = new_solver_session
    preferred_meshing = solver.preferences.MeshingWorkflow
    preferred_meshing.Verbosity = "off"
    assert preferred_meshing.Verbosity() == "off"

    with pytest.raises(ReadOnlyObjectError):
        preferred_meshing.CheckpointingOption = "Write into memory"
    assert preferred_meshing.CheckpointingOption() == "Write mesh files"

    preferred_drawing = preferred_meshing.DrawSettings
    preferred_drawing.FacetLimit = 6000000
    assert preferred_drawing.FacetLimit() == 6000000
    preferred_drawing.FaceZoneLimit = 15000
    assert preferred_drawing.FaceZoneLimit() == 15000

    ansys_logo = solver.preferences.Appearance.AnsysLogo
    ansys_logo.Color = "white"
    assert ansys_logo.Color() == "white"

    ansys_logo.Color = "black"
    assert ansys_logo.Color() == "black"

    ansys_logo.Visible = True
    assert ansys_logo.Visible() is True

    perfered_graphics = solver.preferences.Graphics
    perfered_graphics.AnimationOption = "wireframe"
    assert perfered_graphics.AnimationOption() == "wireframe"

    solver.exit()


@pytest.mark.codegen_required
def test_meshing_preferences(new_meshing_session):
    meshing = new_meshing_session
    preferred_meshing = meshing.preferences.MeshingWorkflow
    preferred_meshing.Verbosity = "off"
    assert preferred_meshing.Verbosity() == "off"

    with pytest.raises(ReadOnlyObjectError):
        preferred_meshing.CheckpointingOption = "Write into memory"
    assert preferred_meshing.CheckpointingOption() == "Write mesh files"

    preferred_drawing = preferred_meshing.DrawSettings
    preferred_drawing.FacetLimit = 6000000
    assert preferred_drawing.FacetLimit() == 6000000

    preferred_drawing.FaceZoneLimit = 15000
    assert preferred_drawing.FaceZoneLimit() == 15000

    ansys_logo = meshing.preferences.Appearance.AnsysLogo
    ansys_logo.Color = "white"
    assert ansys_logo.Color() == "white"

    ansys_logo.Color = "black"
    assert ansys_logo.Color() == "black"

    ansys_logo.Visible = True
    assert ansys_logo.Visible() is True

    preferred_graphics = meshing.preferences.Graphics
    preferred_graphics.AnimationOption = "wireframe"
    assert preferred_graphics.AnimationOption() == "wireframe"


@pytest.mark.codegen_required
def test_read_only_preferences(new_solver_session):
    solver = new_solver_session
    m = solver.preferences.MeshingWorkflow
    m.SaveCheckpointFiles = True
    assert m.SaveCheckpointFiles() is True
    assert m.CheckpointingOption() == "Write mesh files"
    assert m.CheckpointingOption.is_read_only() is True
    with pytest.raises(RuntimeError):
        m.CheckpointingOption = "Write into memory"
    m.SaveCheckpointFiles = False
    assert m.SaveCheckpointFiles() is False
    assert m.CheckpointingOption.is_read_only() is False
    m.CheckpointingOption = "Write into memory"
    assert m.CheckpointingOption() == "Write into memory"
