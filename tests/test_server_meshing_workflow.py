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


@pytest.mark.fluent_version(">=26.1")
def test_new_watertight_workflow(new_meshing_session_wo_exit):
    # Import geometry
    import_file_name = examples.download_file(
        "mixing_elbow.pmdb", "pyfluent/mixing_elbow"
    )
    new_meshing_session_wo_exit.workflow.InitializeWorkflow(
        WorkflowType="Watertight Geometry"
    )
    watertight = new_meshing_session_wo_exit.meshing_workflow
    watertight.task_object.import_geometry["Import Geometry"].arguments.file_name = (
        import_file_name
    )
    assert (
        watertight.task_object.import_geometry[
            "Import Geometry"
        ].arguments.length_unit()
        == "mm"
    )
    watertight.task_object.import_geometry[
        "Import Geometry"
    ].arguments.length_unit.set_state("in")
    assert (
        watertight.task_object.import_geometry[
            "Import Geometry"
        ].arguments.length_unit.get_state()
        == "in"
    )
    watertight.task_object.import_geometry["Import Geometry"].execute()

    # Add local sizing
    watertight.task_object.add_local_sizing_wtm["Add Local Sizing"].add_child_to_task()
    watertight.task_object.add_local_sizing_wtm["Add Local Sizing"].execute()

    # Generate surface mesh
    watertight.task_object.create_surface_mesh[
        "Generate the Surface Mesh"
    ].arguments.cfd_surface_mesh_controls.max_size = 0.3
    assert (
        watertight.task_object.create_surface_mesh[
            "Generate the Surface Mesh"
        ].arguments.cfd_surface_mesh_controls.max_size()
        == 0.3
    )
    watertight.task_object.create_surface_mesh["Generate the Surface Mesh"].execute()

    # Describe geometry
    watertight.task_object.describe_geometry["Describe Geometry"].update_child_tasks(
        setup_type_changed=False
    )
    watertight.task_object.describe_geometry[
        "Describe Geometry"
    ].arguments.setup_type.set_state(
        "The geometry consists of only fluid regions with no voids"
    )
    watertight.task_object.describe_geometry["Describe Geometry"].update_child_tasks(
        setup_type_changed=False
    )
    watertight.task_object.describe_geometry["Describe Geometry"].execute()

    # Update boundaries
    watertight.task_object.update_boundaries[
        "Update Boundaries"
    ].arguments.boundary_label_list.set_state(["wall-inlet"])
    watertight.task_object.update_boundaries[
        "Update Boundaries"
    ].arguments.boundary_label_type_list.set_state(["wall"])
    watertight.task_object.update_boundaries[
        "Update Boundaries"
    ].arguments.old_boundary_label_list.set_state(["wall-inlet"])
    watertight.task_object.update_boundaries[
        "Update Boundaries"
    ].arguments.old_boundary_label_type_list.set_state(["velocity-inlet"])
    watertight.task_object.update_boundaries["Update Boundaries"].execute()

    # Update regions
    watertight.task_object.update_regions["Update Regions"].execute()

    # Add boundary layers
    watertight.task_object.add_boundary_layers[
        "Add Boundary Layers"
    ].add_child_to_task()
    watertight.task_object.add_boundary_layers[
        "Add Boundary Layers"
    ].arguments.control_name.set_state("smooth-transition_1")
    watertight.task_object.add_boundary_layers[
        "Add Boundary Layers"
    ].insert_compound_child_task()
    watertight.task_object.add_boundary_layers["Add Boundary Layers"].execute()

    # Generate volume mesh
    watertight.task_object.create_volume_mesh[
        "Generate the Volume Mesh"
    ].arguments.volume_fill.set_state("poly-hexcore")
    watertight.task_object.create_volume_mesh[
        "Generate the Volume Mesh"
    ].arguments.hex_max_cell_length = 0.3
    watertight.task_object.create_volume_mesh["Generate the Volume Mesh"].execute()

    # Switch to solution mode
    solver = new_meshing_session_wo_exit.switch_to_solver()
    assert solver.is_active() is True
    assert new_meshing_session_wo_exit.is_active() is False
    solver.exit()
    assert solver.is_active() is False
