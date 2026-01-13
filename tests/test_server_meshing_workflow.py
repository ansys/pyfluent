# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
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
from ansys.fluent.core.services.datamodel_se import PyMenu


@pytest.mark.nightly
@pytest.mark.codegen_required
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
    watertight.task_object.import_geometry[
        "Import Geometry"
    ].arguments.file_name = import_file_name
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
    watertight.task_object.create_volume_mesh_wtm[
        "Generate the Volume Mesh"
    ].arguments.volume_fill.set_state("poly-hexcore")
    watertight.task_object.create_volume_mesh_wtm[
        "Generate the Volume Mesh"
    ].arguments.volume_fill_controls.hex_max_cell_length = 0.3
    watertight.task_object.create_volume_mesh_wtm["Generate the Volume Mesh"].execute()

    # Switch to solution mode
    solver = new_meshing_session_wo_exit.switch_to_solver()
    assert solver.is_active() is True
    assert new_meshing_session_wo_exit.is_active() is False
    solver.exit()
    assert solver.is_active() is False


@pytest.mark.nightly
@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=26.1")
def test_new_fault_tolerant_workflow(new_meshing_session_wo_exit):
    meshing = new_meshing_session_wo_exit

    # Import CAD and part management
    import_file_name = examples.download_file(
        "exhaust_system.fmd", "pyfluent/exhaust_system"
    )
    new_meshing_session_wo_exit.workflow.InitializeWorkflow(
        WorkflowType="Fault-tolerant Meshing"
    )
    fault_tolerant = meshing.meshing_workflow
    fault_tolerant.parts.input_file_changed(
        file_path=import_file_name, ignore_solid_names=False, part_per_body=False
    )
    fault_tolerant.parts_files.file_manager.load_files()
    fault_tolerant.parts.node["Meshing Model"].copy(
        paths=[
            "/dirty_manifold-for-wrapper," + "1/dirty_manifold-for-wrapper,1/main,1",
            "/dirty_manifold-for-wrapper,"
            + "1/dirty_manifold-for-wrapper,1/flow-pipe,1",
            "/dirty_manifold-for-wrapper,"
            + "1/dirty_manifold-for-wrapper,1/outpipe3,1",
            "/dirty_manifold-for-wrapper," + "1/dirty_manifold-for-wrapper,1/object2,1",
            "/dirty_manifold-for-wrapper," + "1/dirty_manifold-for-wrapper,1/object1,1",
        ]
    )
    fault_tolerant.parts.object_setting["DefaultObjectSetting"].one_zone_per.set_state(
        "part"
    )
    fault_tolerant.task_object.import_cad_and_part_management[
        "Import CAD and Part Management"
    ].arguments.context.set_state(0)
    fault_tolerant.task_object.import_cad_and_part_management[
        "Import CAD and Part Management"
    ].arguments.create_object_per = "Custom"
    fault_tolerant.task_object.import_cad_and_part_management[
        "Import CAD and Part Management"
    ].arguments.fmd_file_name.set_state(import_file_name)
    fault_tolerant.task_object.import_cad_and_part_management[
        "Import CAD and Part Management"
    ].arguments.file_loaded = True
    fault_tolerant.task_object.import_cad_and_part_management[
        "Import CAD and Part Management"
    ].arguments.object_setting = "DefaultObjectSetting"
    fault_tolerant.task_object.import_cad_and_part_management[
        "Import CAD and Part Management"
    ].execute()

    # Describe geometry and flow
    fault_tolerant.task_object.describe_geometry_and_flow[
        "Describe Geometry and Flow"
    ].arguments.add_enclosure.set_state(False)
    fault_tolerant.task_object.describe_geometry_and_flow[
        "Describe Geometry and Flow"
    ].arguments.close_caps = True
    fault_tolerant.task_object.describe_geometry_and_flow[
        "Describe Geometry and Flow"
    ].arguments.describe_geometry_and_flow_options.advanced_options = True
    fault_tolerant.task_object.describe_geometry_and_flow[
        "Describe Geometry and Flow"
    ].arguments.describe_geometry_and_flow_options.extract_edge_features = True
    fault_tolerant.task_object.describe_geometry_and_flow[
        "Describe Geometry and Flow"
    ].arguments.flow_type = "Internal flow through the object"
    fault_tolerant.task_object.describe_geometry_and_flow[
        "Describe Geometry and Flow"
    ].update_child_tasks(setup_type_changed=False)
    fault_tolerant.task_object.describe_geometry_and_flow[
        "Describe Geometry and Flow"
    ].execute()

    # Enclose fluid regions (capping)
    fault_tolerant.task_object.capping[
        "Enclose Fluid Regions (Capping)"
    ].arguments.patch_name.set_state("inlet-1")
    fault_tolerant.task_object.capping[
        "Enclose Fluid Regions (Capping)"
    ].arguments.selection_type.set_state("zone")
    fault_tolerant.task_object.capping[
        "Enclose Fluid Regions (Capping)"
    ].arguments.zone_selection_list.set_state(["inlet.1"])
    fault_tolerant.task_object.capping[
        "Enclose Fluid Regions (Capping)"
    ].insert_compound_child_task()
    fault_tolerant.task_object.capping["inlet-1"].execute()

    fault_tolerant.task_object.capping[
        "Enclose Fluid Regions (Capping)"
    ].arguments.patch_name.set_state("inlet-2")
    fault_tolerant.task_object.capping[
        "Enclose Fluid Regions (Capping)"
    ].arguments.selection_type.set_state("zone")
    fault_tolerant.task_object.capping[
        "Enclose Fluid Regions (Capping)"
    ].arguments.zone_selection_list.set_state(["inlet.2"])
    fault_tolerant.task_object.capping[
        "Enclose Fluid Regions (Capping)"
    ].insert_compound_child_task()
    fault_tolerant.task_object.capping["inlet-2"].execute()

    fault_tolerant.task_object.capping[
        "Enclose Fluid Regions (Capping)"
    ].arguments.patch_name.set_state("inlet-3")
    fault_tolerant.task_object.capping[
        "Enclose Fluid Regions (Capping)"
    ].arguments.selection_type.set_state("zone")
    fault_tolerant.task_object.capping[
        "Enclose Fluid Regions (Capping)"
    ].arguments.zone_selection_list.set_state(["inlet"])
    fault_tolerant.task_object.capping[
        "Enclose Fluid Regions (Capping)"
    ].insert_compound_child_task()
    fault_tolerant.task_object.capping["inlet-3"].execute()

    fault_tolerant.task_object.capping[
        "Enclose Fluid Regions (Capping)"
    ].arguments.patch_name.set_state("outlet-1")
    fault_tolerant.task_object.capping[
        "Enclose Fluid Regions (Capping)"
    ].arguments.selection_type.set_state("zone")
    fault_tolerant.task_object.capping[
        "Enclose Fluid Regions (Capping)"
    ].arguments.zone_selection_list.set_state(["outlet"])
    fault_tolerant.task_object.capping[
        "Enclose Fluid Regions (Capping)"
    ].arguments.zone_type.set_state("pressure-outlet")
    fault_tolerant.task_object.capping[
        "Enclose Fluid Regions (Capping)"
    ].insert_compound_child_task()
    fault_tolerant.task_object.capping["outlet-1"].execute()

    # Extract edge features
    fault_tolerant.task_object.extract_edge_features[
        "Extract Edge Features"
    ].arguments.extract_edges_name.set_state("edge-group-1")
    fault_tolerant.task_object.extract_edge_features[
        "Extract Edge Features"
    ].arguments.extract_method_type.set_state("Intersection Loops")
    fault_tolerant.task_object.extract_edge_features[
        "Extract Edge Features"
    ].arguments.object_selection_list.set_state(["flow_pipe", "main"])
    fault_tolerant.task_object.extract_edge_features[
        "Extract Edge Features"
    ].insert_compound_child_task()
    fault_tolerant.task_object.extract_edge_features["edge-group-1"].execute()

    # Identify regions
    fault_tolerant.task_object.identify_regions[
        "Identify Regions"
    ].arguments.show_coordinates = True
    fault_tolerant.task_object.identify_regions[
        "Identify Regions"
    ].arguments.material_points_name.set_state("fluid-region-1")
    fault_tolerant.task_object.identify_regions[
        "Identify Regions"
    ].arguments.selection_type.set_state("zone")
    fault_tolerant.task_object.identify_regions[
        "Identify Regions"
    ].arguments.x.set_state(377.322045740589)
    fault_tolerant.task_object.identify_regions[
        "Identify Regions"
    ].arguments.y.set_state(-176.800676988458)
    fault_tolerant.task_object.identify_regions[
        "Identify Regions"
    ].arguments.z.set_state(-37.0764628583475)
    fault_tolerant.task_object.identify_regions[
        "Identify Regions"
    ].arguments.zone_selection_list.set_state(["main.1"])
    fault_tolerant.task_object.identify_regions[
        "Identify Regions"
    ].insert_compound_child_task()
    fault_tolerant.task_object.identify_regions["fluid-region-1"].execute()

    fault_tolerant.task_object.identify_regions[
        "Identify Regions"
    ].arguments.show_coordinates = True
    fault_tolerant.task_object.identify_regions[
        "Identify Regions"
    ].arguments.material_points_name.set_state("void-region-1")
    fault_tolerant.task_object.identify_regions[
        "Identify Regions"
    ].arguments.new_region_type.set_state("void")
    fault_tolerant.task_object.identify_regions[
        "Identify Regions"
    ].arguments.object_selection_list.set_state(
        ["inlet-1", "inlet-2", "inlet-3", "main"]
    )
    fault_tolerant.task_object.identify_regions[
        "Identify Regions"
    ].arguments.x.set_state(374.722045740589)
    fault_tolerant.task_object.identify_regions[
        "Identify Regions"
    ].arguments.y.set_state(-278.9775145640143)
    fault_tolerant.task_object.identify_regions[
        "Identify Regions"
    ].arguments.z.set_state(-161.1700719416913)
    fault_tolerant.task_object.identify_regions[
        "Identify Regions"
    ].arguments.zone_selection_list.set_state(["main.1"])
    fault_tolerant.task_object.identify_regions[
        "Identify Regions"
    ].insert_compound_child_task()
    fault_tolerant.task_object.identify_regions["void-region-1"].execute()

    # Define leakage threshold
    fault_tolerant.task_object.define_leakage_threshold[
        "Define Leakage Threshold"
    ].arguments.set_state(
        {
            "add_child": "yes",
            "flip_direction": True,
            "leakage_name": "leakage-1",
            "plane_direction": "X",
            "region_selection_single": "void-region-1",
        }
    )
    fault_tolerant.task_object.define_leakage_threshold[
        "Define Leakage Threshold"
    ].insert_compound_child_task()
    fault_tolerant.task_object.define_leakage_threshold["leakage-1"].execute()

    # Update regions settings
    fault_tolerant.task_object.update_region_settings[
        "Update Region Settings"
    ].arguments.all_region_filter_categories.set_state(["2"] * 5 + ["1"] * 2)
    fault_tolerant.task_object.update_region_settings[
        "Update Region Settings"
    ].arguments.all_region_leakage_size_list.set_state(["none"] * 6 + ["6.4"])
    fault_tolerant.task_object.update_region_settings[
        "Update Region Settings"
    ].arguments.all_region_linked_construction_surface_list.set_state(
        ["n/a"] * 6 + ["no"]
    )
    fault_tolerant.task_object.update_region_settings[
        "Update Region Settings"
    ].arguments.all_region_mesh_method_list.set_state(["none"] * 6 + ["wrap"])
    fault_tolerant.task_object.update_region_settings[
        "Update Region Settings"
    ].arguments.all_region_name_list.set_state(
        [
            "main",
            "flow_pipe",
            "outpipe3",
            "object2",
            "object1",
            "void-region-1",
            "fluid-region-1",
        ]
    )
    fault_tolerant.task_object.update_region_settings[
        "Update Region Settings"
    ].arguments.all_region_overset_componen_list.set_state(["no"] * 7)
    fault_tolerant.task_object.update_region_settings[
        "Update Region Settings"
    ].arguments.all_region_source_list.set_state(["object"] * 5 + ["mpt"] * 2)
    fault_tolerant.task_object.update_region_settings[
        "Update Region Settings"
    ].arguments.all_region_type_list.set_state(["void"] * 6 + ["fluid"])
    fault_tolerant.task_object.update_region_settings[
        "Update Region Settings"
    ].arguments.all_region_volume_fill_list.set_state(["none"] * 6 + ["tet"])
    fault_tolerant.task_object.update_region_settings[
        "Update Region Settings"
    ].arguments.filter_category.set_state("Identified Regions")
    fault_tolerant.task_object.update_region_settings[
        "Update Region Settings"
    ].arguments.all_region_leakage_size_list.set_state([""])
    fault_tolerant.task_object.update_region_settings[
        "Update Region Settings"
    ].arguments.all_region_mesh_method_list.set_state(["wrap"])
    fault_tolerant.task_object.update_region_settings[
        "Update Region Settings"
    ].arguments.all_region_name_list.set_state(["fluid-region-1"])
    fault_tolerant.task_object.update_region_settings[
        "Update Region Settings"
    ].arguments.all_region_overset_componen_list.set_state(["no"])
    fault_tolerant.task_object.update_region_settings[
        "Update Region Settings"
    ].arguments.all_region_type_list.set_state(["fluid"])
    fault_tolerant.task_object.update_region_settings[
        "Update Region Settings"
    ].arguments.all_region_volume_fill_list.set_state(["hexcore"])
    fault_tolerant.task_object.update_region_settings[
        "Update Region Settings"
    ].arguments.all_region_leakage_size_list.set_state([""])
    fault_tolerant.task_object.update_region_settings[
        "Update Region Settings"
    ].arguments.all_region_mesh_method_list.set_state(["wrap"])
    fault_tolerant.task_object.update_region_settings[
        "Update Region Settings"
    ].arguments.all_region_name_list.set_state(["fluid-region-1"])
    fault_tolerant.task_object.update_region_settings[
        "Update Region Settings"
    ].arguments.all_region_overset_componen_list.set_state(["no"])
    fault_tolerant.task_object.update_region_settings[
        "Update Region Settings"
    ].arguments.all_region_type_list.set_state(["fluid"])
    fault_tolerant.task_object.update_region_settings[
        "Update Region Settings"
    ].arguments.all_region_volume_fill_list.set_state(["tet"])
    fault_tolerant.task_object.update_region_settings[
        "Update Region Settings"
    ].execute()

    # Choose mesh control options
    fault_tolerant.task_object.choose_mesh_control_options[
        "Choose Mesh Control Options"
    ].execute()

    # Generate surface mesh
    fault_tolerant.task_object.generate_surface_mesh[
        "Generate the Surface Mesh"
    ].execute()

    # Update boundaries
    fault_tolerant.task_object.update_boundaries["Update Boundaries"].execute()

    # Add boundary layers
    fault_tolerant.task_object.add_boundary_layers[
        "Add Boundary Layers"
    ].arguments.control_name.set_state("aspect-ratio_1")
    fault_tolerant.task_object.add_boundary_layers[
        "Add Boundary Layers"
    ].insert_compound_child_task()
    fault_tolerant.task_object.add_boundary_layers["aspect-ratio_1"].execute()

    # Generate volume mesh
    fault_tolerant.task_object.create_volume_mesh_ftm[
        "Generate the Volume Mesh"
    ].arguments.all_region_name_list.set_state(
        [
            "main",
            "flow_pipe",
            "outpipe3",
            "object2",
            "object1",
            "void-region-1",
            "fluid-region-1",
        ]
    )
    fault_tolerant.task_object.create_volume_mesh_ftm[
        "Generate the Volume Mesh"
    ].arguments.all_region_size_list.set_state(["11.33375"] * 7)
    fault_tolerant.task_object.create_volume_mesh_ftm[
        "Generate the Volume Mesh"
    ].arguments.all_region_volume_fill_list.set_state(["none"] * 6 + ["tet"])
    fault_tolerant.task_object.create_volume_mesh_ftm[
        "Generate the Volume Mesh"
    ].execute()

    # Generate volume mesh
    solver = meshing.switch_to_solver()
    assert solver.is_active() is True
    assert meshing.is_active() is False
    solver.exit()
    assert solver.is_active() is False


@pytest.mark.nightly
@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=26.1")
def test_new_2d_meshing_workflow(new_meshing_session_wo_exit):
    # Import geometry
    import_file_name = examples.download_file("NACA0012.fmd", "pyfluent/airfoils")
    new_meshing_session_wo_exit.workflow.InitializeWorkflow(WorkflowType="2D Meshing")

    two_dim_mesh = new_meshing_session_wo_exit.meshing_workflow

    two_dim_mesh.task_object.load_cad_geometry[
        "Load CAD Geometry"
    ].arguments.file_name = import_file_name
    two_dim_mesh.task_object.load_cad_geometry[
        "Load CAD Geometry"
    ].arguments.length_unit = "mm"
    two_dim_mesh.task_object.load_cad_geometry[
        "Load CAD Geometry"
    ].arguments.refaceting.refacet = False
    two_dim_mesh.task_object.load_cad_geometry["Load CAD Geometry"].execute()

    # Set regions and boundaries
    two_dim_mesh.task_object.update_boundaries[
        "Update Boundaries"
    ].arguments.selection_type = "zone"
    two_dim_mesh.task_object.update_boundaries["Update Boundaries"].execute()

    # Define global sizing
    two_dim_mesh.task_object.define_global_sizing[
        "Define Global Sizing"
    ].arguments.curvature_normal_angle = 20
    two_dim_mesh.task_object.define_global_sizing[
        "Define Global Sizing"
    ].arguments.max_size = 2000.0
    two_dim_mesh.task_object.define_global_sizing[
        "Define Global Sizing"
    ].arguments.min_size = 5.0
    two_dim_mesh.task_object.define_global_sizing[
        "Define Global Sizing"
    ].arguments.size_functions = "Curvature"
    two_dim_mesh.task_object.define_global_sizing["Define Global Sizing"].execute()

    # Add local sizing
    two_dim_mesh.task_object.add_local_sizing_wtm[
        "Add Local Sizing"
    ].arguments.add_child = True
    two_dim_mesh.task_object.add_local_sizing_wtm[
        "Add Local Sizing"
    ].arguments.boi_control_name = "boi_1"
    two_dim_mesh.task_object.add_local_sizing_wtm[
        "Add Local Sizing"
    ].arguments.boi_execution = "Body Of Influence"
    two_dim_mesh.task_object.add_local_sizing_wtm[
        "Add Local Sizing"
    ].arguments.boi_face_label_list = ["boi"]
    two_dim_mesh.task_object.add_local_sizing_wtm[
        "Add Local Sizing"
    ].arguments.boi_size = 50.0
    two_dim_mesh.task_object.add_local_sizing_wtm[
        "Add Local Sizing"
    ].arguments.boi_zoneor_label = "label"
    two_dim_mesh.task_object.add_local_sizing_wtm[
        "Add Local Sizing"
    ].arguments.draw_size_control = True
    two_dim_mesh.task_object.add_local_sizing_wtm[
        "Add Local Sizing"
    ].add_child_and_update(defer_update=False)

    two_dim_mesh.task_object.add_local_sizing_wtm[
        "Add Local Sizing"
    ].arguments.add_child = True
    two_dim_mesh.task_object.add_local_sizing_wtm[
        "Add Local Sizing"
    ].arguments.boi_control_name = "edgesize_1"
    two_dim_mesh.task_object.add_local_sizing_wtm[
        "Add Local Sizing"
    ].arguments.boi_execution = "Edge Size"
    two_dim_mesh.task_object.add_local_sizing_wtm[
        "Add Local Sizing"
    ].arguments.boi_size = 5.0
    two_dim_mesh.task_object.add_local_sizing_wtm[
        "Add Local Sizing"
    ].arguments.boi_zoneor_label = "label"
    two_dim_mesh.task_object.add_local_sizing_wtm[
        "Add Local Sizing"
    ].arguments.draw_size_control = True
    two_dim_mesh.task_object.add_local_sizing_wtm[
        "Add Local Sizing"
    ].arguments.edge_label_list = ["airfoil-te"]
    two_dim_mesh.task_object.add_local_sizing_wtm[
        "Add Local Sizing"
    ].add_child_and_update(defer_update=False)

    two_dim_mesh.task_object.add_local_sizing_wtm[
        "Add Local Sizing"
    ].arguments.add_child = True
    two_dim_mesh.task_object.add_local_sizing_wtm[
        "Add Local Sizing"
    ].arguments.boi_control_name = "curvature_1"
    two_dim_mesh.task_object.add_local_sizing_wtm[
        "Add Local Sizing"
    ].arguments.boi_curvature_normal_angle = 10
    two_dim_mesh.task_object.add_local_sizing_wtm[
        "Add Local Sizing"
    ].arguments.boi_execution = "Curvature"
    two_dim_mesh.task_object.add_local_sizing_wtm[
        "Add Local Sizing"
    ].arguments.boi_max_size = 2
    two_dim_mesh.task_object.add_local_sizing_wtm[
        "Add Local Sizing"
    ].arguments.boi_min_size = 1.5
    two_dim_mesh.task_object.add_local_sizing_wtm[
        "Add Local Sizing"
    ].arguments.boi_scope_to = "edges"
    two_dim_mesh.task_object.add_local_sizing_wtm[
        "Add Local Sizing"
    ].arguments.boi_zoneor_label = "label"
    two_dim_mesh.task_object.add_local_sizing_wtm[
        "Add Local Sizing"
    ].arguments.draw_size_control = True
    two_dim_mesh.task_object.add_local_sizing_wtm[
        "Add Local Sizing"
    ].arguments.edge_label_list = ["airfoil"]
    two_dim_mesh.task_object.add_local_sizing_wtm[
        "Add Local Sizing"
    ].add_child_and_update(defer_update=False)

    # Add boundary layer
    two_dim_mesh.task_object.add_2d_boundary_layers[
        "Add 2D Boundary Layers"
    ].arguments.add_child = True
    two_dim_mesh.task_object.add_2d_boundary_layers[
        "Add 2D Boundary Layers"
    ].arguments.control_name = "aspect-ratio_1"
    two_dim_mesh.task_object.add_2d_boundary_layers[
        "Add 2D Boundary Layers"
    ].arguments.number_of_layers = 4
    two_dim_mesh.task_object.add_2d_boundary_layers[
        "Add 2D Boundary Layers"
    ].arguments.offset_method_type = "aspect-ratio"
    two_dim_mesh.task_object.add_2d_boundary_layers[
        "Add 2D Boundary Layers"
    ].add_child_and_update(defer_update=False)

    # NOTE: Setting `show_advanced_options = True` is required to configure advanced preferences.
    # This dependency may be removed in a future release as the API evolves.
    two_dim_mesh.task_object.generate_initial_surface_mesh[
        "Generate the Surface Mesh"
    ].arguments.surface_2d_preferences.show_advanced_options = True
    two_dim_mesh.task_object.generate_initial_surface_mesh[
        "Generate the Surface Mesh"
    ].arguments.surface_2d_preferences.merge_edge_zones_based_on_labels = False
    two_dim_mesh.task_object.generate_initial_surface_mesh[
        "Generate the Surface Mesh"
    ].arguments.surface_2d_preferences.merge_face_zones_based_on_labels = False
    two_dim_mesh.task_object.generate_initial_surface_mesh[
        "Generate the Surface Mesh"
    ].execute()

    two_dim_mesh.task_object.add_2d_boundary_layers["Add 2D Boundary Layers"].revert()
    two_dim_mesh.task_object.add_2d_boundary_layers[
        "Add 2D Boundary Layers"
    ].arguments.add_child = "yes"
    two_dim_mesh.task_object.add_2d_boundary_layers[
        "Add 2D Boundary Layers"
    ].arguments.control_name = "uniform_1"
    two_dim_mesh.task_object.add_2d_boundary_layers[
        "Add 2D Boundary Layers"
    ].arguments.first_layer_height = 2
    two_dim_mesh.task_object.add_2d_boundary_layers[
        "Add 2D Boundary Layers"
    ].arguments.number_of_layers = 4
    two_dim_mesh.task_object.add_2d_boundary_layers[
        "Add 2D Boundary Layers"
    ].arguments.offset_method_type = "uniform"
    two_dim_mesh.task_object.add_2d_boundary_layers["Add 2D Boundary Layers"].execute()

    # NOTE: Setting `show_advanced_options = True` is required to configure advanced preferences.
    # This dependency may be removed in a future release as the API evolves.
    two_dim_mesh.task_object.generate_initial_surface_mesh[
        "Generate the Surface Mesh"
    ].arguments.surface_2d_preferences.show_advanced_options = True
    two_dim_mesh.task_object.generate_initial_surface_mesh[
        "Generate the Surface Mesh"
    ].arguments.surface_2d_preferences.merge_edge_zones_based_on_labels = False
    two_dim_mesh.task_object.generate_initial_surface_mesh[
        "Generate the Surface Mesh"
    ].arguments.surface_2d_preferences.merge_face_zones_based_on_labels = False
    two_dim_mesh.task_object.generate_initial_surface_mesh[
        "Generate the Surface Mesh"
    ].execute()

    # Switch to solution mode
    solver = new_meshing_session_wo_exit.switch_to_solver()
    assert solver.is_active() is True
    assert new_meshing_session_wo_exit.is_active() is False
    solver.exit()
    assert solver.is_active() is False


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=26.1")
def test_arguments_and_parameters_in_new_meshing_workflow(new_meshing_session):
    new_meshing_session.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
    watertight = new_meshing_session.meshing_workflow

    # arguments
    assert (
        watertight.task_object.import_geometry[
            "Import Geometry"
        ].arguments.length_unit()
        == "mm"
    )
    assert watertight.task_object.import_geometry[
        "Import Geometry"
    ].arguments.length_unit.allowed_values() == [
        "m",
        "cm",
        "mm",
        "in",
        "ft",
        "um",
        "nm",
    ]
    watertight.task_object.import_geometry[
        "Import Geometry"
    ].arguments.length_unit = "m"
    assert (
        watertight.task_object.import_geometry[
            "Import Geometry"
        ].arguments.length_unit.get_state()
        == "m"
    )
    watertight.task_object.import_geometry["Import Geometry"].arguments.set_state(
        {"length_unit": "in"}
    )
    assert (
        watertight.task_object.import_geometry[
            "Import Geometry"
        ].arguments.length_unit()
        == "in"
    )
    watertight.task_object.import_geometry["Import Geometry"].set_state(
        {"arguments": {"length_unit": "ft"}}
    )
    assert (
        watertight.task_object.import_geometry[
            "Import Geometry"
        ].arguments.length_unit()
        == "ft"
    )

    # parameters
    assert (
        watertight.task_object.import_geometry["Import Geometry"].state()
        == "Out-of-date"
    )
    assert watertight.task_object.import_geometry[
        "Import Geometry"
    ].state.allowed_values() == [
        "Out-of-date",
        "Attention-required",
        "Up-to-date",
        "Forced-up-to-date",
    ]
    watertight.task_object.import_geometry["Import Geometry"].state = "Up-to-date"
    assert (
        watertight.task_object.import_geometry["Import Geometry"].state.get_state()
        == "Up-to-date"
    )
    watertight.task_object.import_geometry["Import Geometry"].set_state(
        {"state": "Out-of-date"}
    )
    assert (
        watertight.task_object.import_geometry["Import Geometry"].state()
        == "Out-of-date"
    )
    assert (
        watertight.task_object.import_geometry[
            "Import Geometry"
        ].check_point.default_value()
        == "default-off"
    )

    # Both in a single set_state operation
    watertight.task_object.import_geometry["Import Geometry"].set_state(
        {"arguments": {"length_unit": "cm"}, "state": "Forced-up-to-date"}
    )
    assert (
        watertight.task_object.import_geometry[
            "Import Geometry"
        ].arguments.length_unit()
        == "cm"
    )
    assert (
        watertight.task_object.import_geometry["Import Geometry"].state()
        == "Forced-up-to-date"
    )


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=26.1")
def test_get_task_by_id(new_meshing_session):
    # This test is only intended for developer level testing
    meshing_session = new_meshing_session
    meshing_session.meshing_workflow.general.initialize_workflow(
        workflow_type="Watertight Geometry"
    )
    service = meshing_session.meshing_workflow.service
    rules = meshing_session.meshing_workflow.rules

    path = [("task_object", "TaskObject1"), ("_name_", "")]
    assert (
        PyMenu(service=service, rules=rules, path=path).get_remote_state()
        == "Import Geometry"
    )

    path = [("task_object", "TaskObject1"), ("CommandName", "")]
    assert (
        PyMenu(service=service, rules=rules, path=path).get_remote_state()
        == "ImportGeometry"
    )

    path = [("task_object", "TaskObject5"), ("_name_", "")]
    assert (
        PyMenu(service=service, rules=rules, path=path).get_remote_state()
        == "Apply Share Topology"
    )

    path = [("task_object", "TaskObject1")]
    assert PyMenu(service=service, rules=rules, path=path).get_remote_state() == {
        "_name_": "Import Geometry",
        "arguments": {},
        "warnings": None,
        "command_name": "ImportGeometry",
        "errors": None,
        "task_type": "Simple",
        "object_path": "",
        "state": "Out-of-date",
        "check_point": "default-off",
    }


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=26.1")
def test_insert_delete_and_rename_task(new_meshing_session):
    meshing_session = new_meshing_session
    meshing_session.meshing_workflow.general.initialize_workflow(
        workflow_type="Watertight Geometry"
    )

    # Insert new task
    assert len(meshing_session.meshing_workflow.task_object()) == 11
    meshing_session.meshing_workflow.task_object.import_geometry[
        "Import Geometry"
    ].insert_next_task(command_name="ImportBodyOfInfluenceGeometry")
    assert len(meshing_session.meshing_workflow.task_object()) == 12
    assert meshing_session.meshing_workflow.task_object.import_boi_geometry[
        "Import Body of Influence Geometry"
    ].arguments() == {
        "type": "CAD",
        "geometry_file_name": None,
        "cad_import_options": {},
    }

    # Delete
    assert len(meshing_session.meshing_workflow.task_object()) == 12
    assert (
        "create_volume_mesh_wtm:Generate the Volume Mesh"
        in meshing_session.meshing_workflow.task_object()
    )
    meshing_session.meshing_workflow.general.delete_tasks(
        list_of_tasks=["Generate the Volume Mesh"]
    )
    assert len(meshing_session.meshing_workflow.task_object()) == 11
    assert (
        "create_volume_mesh_wtm:Generate the Volume Mesh"
        not in meshing_session.meshing_workflow.task_object()
    )

    # Rename
    assert (
        "add_boundary_layers:Add Boundary Layers"
        in meshing_session.meshing_workflow.task_object()
    )
    meshing_session.meshing_workflow.task_object.add_boundary_layers[
        "Add Boundary Layers"
    ].rename(new_name="Add BL")
    assert (
        "add_boundary_layers:Add Boundary Layers"
        not in meshing_session.meshing_workflow.task_object()
    )
    assert (
        "add_boundary_layers:Add BL" in meshing_session.meshing_workflow.task_object()
    )


############################################################################################
# Test the enhanced meshing workflow
############################################################################################


@pytest.mark.nightly
@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=26.1")
def test_new_watertight_workflow_enhanced_meshing(
    new_meshing_session_wo_exit, use_server_meshing_workflow
):
    # Import geometry
    import_file_name = examples.download_file(
        "mixing_elbow.pmdb", "pyfluent/mixing_elbow"
    )
    watertight = new_meshing_session_wo_exit.watertight()
    watertight.import_geometry.file_name.set_state(import_file_name)
    assert watertight.import_geometry.length_unit() == "mm"
    watertight.import_geometry.length_unit.set_state("in")
    assert watertight.import_geometry.length_unit.get_state() == "in"
    watertight.import_geometry()

    # Add local sizing
    watertight.add_local_sizing_wtm.add_child_to_task()
    watertight.add_local_sizing_wtm()

    # Generate surface mesh
    watertight.create_surface_mesh.cfd_surface_mesh_controls.max_size.set_state(0.3)
    assert watertight.create_surface_mesh.cfd_surface_mesh_controls.max_size() == 0.3
    watertight.create_surface_mesh()

    # Describe geometry
    watertight.describe_geometry.update_child_tasks(setup_type_changed=False)
    watertight.describe_geometry.setup_type.set_state(
        "The geometry consists of only fluid regions with no voids"
    )
    watertight.describe_geometry.update_child_tasks(setup_type_changed=True)
    watertight.describe_geometry()

    # Update boundaries
    watertight.update_boundaries.boundary_zone_list.set_state(["wall-inlet"])
    watertight.update_boundaries.boundary_label_list.set_state(["wall-inlet"])
    watertight.update_boundaries.boundary_label_type_list.set_state(["wall"])
    watertight.update_boundaries.old_boundary_label_list.set_state(["wall-inlet"])
    watertight.update_boundaries.old_boundary_label_type_list.set_state(
        ["velocity-inlet"]
    )
    watertight.update_boundaries()

    # Update regions
    watertight.update_regions()

    # Add boundary layers
    watertight.add_boundary_layers.add_child_to_task()
    watertight.add_boundary_layers.control_name.set_state("smooth-transition_1")
    watertight.add_boundary_layers.insert_compound_child_task()
    watertight.add_boundary_layers_child_1()

    # Generate volume mesh
    watertight.create_volume_mesh_wtm.volume_fill.set_state("poly-hexcore")
    watertight.create_volume_mesh_wtm.volume_fill_controls.hex_max_cell_length.set_state(
        0.3
    )
    watertight.create_volume_mesh_wtm()

    # Switch to solution mode
    solver = new_meshing_session_wo_exit.switch_to_solver()
    assert solver.is_active() is True
    assert new_meshing_session_wo_exit.is_active() is False
    solver.exit()
    assert solver.is_active() is False


@pytest.mark.nightly
@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=26.1")
def test_new_fault_tolerant_workflow_enhanced_meshing(
    new_meshing_session_wo_exit, use_server_meshing_workflow
):
    meshing = new_meshing_session_wo_exit

    # Import CAD and part management
    import_file_name = examples.download_file(
        "exhaust_system.fmd", "pyfluent/exhaust_system"
    )
    fault_tolerant = meshing.fault_tolerant()
    fault_tolerant.parts.input_file_changed(
        file_path=import_file_name, ignore_solid_names=False, part_per_body=False
    )
    fault_tolerant.parts_files.file_manager.load_files()
    fault_tolerant.parts.node["Meshing Model"].copy(
        paths=[
            "/dirty_manifold-for-wrapper," + "1/dirty_manifold-for-wrapper,1/main,1",
            "/dirty_manifold-for-wrapper,"
            + "1/dirty_manifold-for-wrapper,1/flow-pipe,1",
            "/dirty_manifold-for-wrapper,"
            + "1/dirty_manifold-for-wrapper,1/outpipe3,1",
            "/dirty_manifold-for-wrapper," + "1/dirty_manifold-for-wrapper,1/object2,1",
            "/dirty_manifold-for-wrapper," + "1/dirty_manifold-for-wrapper,1/object1,1",
        ]
    )
    fault_tolerant.parts.object_setting["DefaultObjectSetting"].one_zone_per.set_state(
        "part"
    )
    fault_tolerant.import_cad_and_part_management.context.set_state(0)
    fault_tolerant.import_cad_and_part_management.create_object_per.set_state("Custom")
    fault_tolerant.import_cad_and_part_management.fmd_file_name.set_state(
        import_file_name
    )
    fault_tolerant.import_cad_and_part_management.file_loaded.set_state("yes")
    fault_tolerant.import_cad_and_part_management.object_setting.set_state(
        "DefaultObjectSetting"
    )
    fault_tolerant.import_cad_and_part_management()

    # Describe geometry and flow
    fault_tolerant.describe_geometry_and_flow.add_enclosure.set_state("No")
    fault_tolerant.describe_geometry_and_flow.close_caps.set_state("Yes")
    fault_tolerant.describe_geometry_and_flow.describe_geometry_and_flow_options.advanced_options.set_state(
        True
    )
    fault_tolerant.describe_geometry_and_flow.describe_geometry_and_flow_options.extract_edge_features.set_state(
        "Yes"
    )
    fault_tolerant.describe_geometry_and_flow.flow_type.set_state(
        "Internal flow through the object"
    )
    fault_tolerant.describe_geometry_and_flow.update_child_tasks(
        setup_type_changed=False
    )
    fault_tolerant.describe_geometry_and_flow()

    # Enclose fluid regions (capping)
    fault_tolerant.capping.create_patch_preferences.show_in_gui.set_state(False)

    fault_tolerant.capping.patch_name.set_state("inlet-1")
    fault_tolerant.capping.selection_type.set_state("zone")
    fault_tolerant.capping.zone_selection_list.set_state(["inlet.1"])
    fault_tolerant.capping.insert_compound_child_task()
    fault_tolerant.capping_child_1()

    fault_tolerant.capping.patch_name.set_state("inlet-2")
    fault_tolerant.capping.selection_type.set_state("zone")
    fault_tolerant.capping.zone_selection_list.set_state(["inlet.2"])
    fault_tolerant.capping.insert_compound_child_task()
    fault_tolerant.capping_child_2()

    fault_tolerant.capping.patch_name.set_state("inlet-3")
    fault_tolerant.capping.selection_type.set_state("zone")
    fault_tolerant.capping.zone_selection_list.set_state(["inlet"])
    fault_tolerant.capping.insert_compound_child_task()
    fault_tolerant.capping_child_3()

    fault_tolerant.capping.patch_name.set_state("outlet-1")
    fault_tolerant.capping.selection_type.set_state("zone")
    fault_tolerant.capping.zone_selection_list.set_state(["outlet"])
    fault_tolerant.capping.zone_type.set_state("pressure-outlet")
    fault_tolerant.capping.insert_compound_child_task()
    fault_tolerant.capping_child_4()

    # Extract edge features
    fault_tolerant.extract_edge_features.extract_edges_name.set_state("edge-group-1")
    fault_tolerant.extract_edge_features.extract_method_type.set_state(
        "Intersection Loops"
    )
    fault_tolerant.extract_edge_features.object_selection_list.set_state(
        ["flow_pipe", "main"]
    )
    fault_tolerant.extract_edge_features.insert_compound_child_task()
    fault_tolerant.extract_edge_features_child_1()

    # Identify regions
    fault_tolerant.identify_regions.show_coordinates = True
    fault_tolerant.identify_regions.material_points_name.set_state("fluid-region-1")
    fault_tolerant.identify_regions.selection_type.set_state("zone")
    fault_tolerant.identify_regions.x.set_state(377.322045740589)
    fault_tolerant.identify_regions.y.set_state(-176.800676988458)
    fault_tolerant.identify_regions.z.set_state(-37.0764628583475)
    fault_tolerant.identify_regions.zone_selection_list.set_state(["main.1"])
    fault_tolerant.identify_regions.insert_compound_child_task()
    fault_tolerant.identify_regions_child_1()

    fault_tolerant.identify_regions.show_coordinates = True
    fault_tolerant.identify_regions.material_points_name.set_state("void-region-1")
    fault_tolerant.identify_regions.new_region_type.set_state("void")
    fault_tolerant.identify_regions.selection_type = "object"
    fault_tolerant.identify_regions.object_selection_list.set_state(
        ["inlet-1", "inlet-2", "inlet-3", "main"]
    )
    fault_tolerant.identify_regions.x.set_state(374.722045740589)
    fault_tolerant.identify_regions.y.set_state(-278.9775145640143)
    fault_tolerant.identify_regions.z.set_state(-161.1700719416913)
    fault_tolerant.identify_regions.insert_compound_child_task()
    fault_tolerant.identify_regions_child_2()

    # Define leakage threshold
    fault_tolerant.define_leakage_threshold.add_child.set_state("yes")
    fault_tolerant.define_leakage_threshold.flip_direction.set_state(True)
    fault_tolerant.define_leakage_threshold.plane_direction.set_state("X")
    fault_tolerant.define_leakage_threshold.region_selection_single.set_state(
        "void-region-1"
    )

    fault_tolerant.define_leakage_threshold.add_child = "yes"
    fault_tolerant.define_leakage_threshold.flip_direction = True
    fault_tolerant.define_leakage_threshold.leakage_name = "leakage-1"
    fault_tolerant.define_leakage_threshold.plane_direction = "X"
    fault_tolerant.define_leakage_threshold.region_selection_single = "void-region-1"
    fault_tolerant.define_leakage_threshold.insert_compound_child_task()
    fault_tolerant.define_leakage_threshold_child_1()

    # Update regions settings
    fault_tolerant.update_region_settings.all_region_filter_categories.set_state(
        ["2"] * 5 + ["1"] * 2
    )
    fault_tolerant.update_region_settings.all_region_leakage_size_list.set_state(
        ["none"] * 6 + ["6.4"]
    )
    fault_tolerant.update_region_settings.all_region_linked_construction_surface_list.set_state(
        ["n/a"] * 6 + ["no"]
    )
    fault_tolerant.update_region_settings.all_region_mesh_method_list.set_state(
        ["none"] * 6 + ["wrap"]
    )
    fault_tolerant.update_region_settings.all_region_name_list.set_state(
        [
            "main",
            "flow_pipe",
            "outpipe3",
            "object2",
            "object1",
            "void-region-1",
            "fluid-region-1",
        ]
    )
    fault_tolerant.update_region_settings.all_region_overset_componen_list.set_state(
        ["no"] * 7
    )
    fault_tolerant.update_region_settings.all_region_source_list.set_state(
        ["object"] * 5 + ["mpt"] * 2
    )
    fault_tolerant.update_region_settings.all_region_type_list.set_state(
        ["void"] * 6 + ["fluid"]
    )
    fault_tolerant.update_region_settings.all_region_volume_fill_list.set_state(
        ["none"] * 6 + ["tet"]
    )
    fault_tolerant.update_region_settings.filter_category.set_state(
        "Identified Regions"
    )
    fault_tolerant.update_region_settings.all_region_leakage_size_list.set_state([""])
    fault_tolerant.update_region_settings.all_region_mesh_method_list.set_state(
        ["wrap"]
    )
    fault_tolerant.update_region_settings.all_region_name_list.set_state(
        ["fluid-region-1"]
    )
    fault_tolerant.update_region_settings.all_region_overset_componen_list.set_state(
        ["no"]
    )
    fault_tolerant.update_region_settings.all_region_type_list.set_state(["fluid"])
    fault_tolerant.update_region_settings.all_region_volume_fill_list.set_state(
        ["hexcore"]
    )
    fault_tolerant.update_region_settings.all_region_leakage_size_list.set_state([""])
    fault_tolerant.update_region_settings.all_region_mesh_method_list.set_state(
        ["wrap"]
    )
    fault_tolerant.update_region_settings.all_region_name_list.set_state(
        ["fluid-region-1"]
    )
    fault_tolerant.update_region_settings.all_region_overset_componen_list.set_state(
        ["no"]
    )
    fault_tolerant.update_region_settings.all_region_type_list.set_state(["fluid"])
    fault_tolerant.update_region_settings.all_region_volume_fill_list.set_state(["tet"])
    fault_tolerant.update_region_settings()

    # Setup size controls
    fault_tolerant.setup_size_controls.local_settings_name = "default-curvature"
    fault_tolerant.setup_size_controls.local_size_control_parameters.sizing_type = (
        "curvature"
    )
    fault_tolerant.setup_size_controls.object_selection_list = [
        "inlet-1",
        "inlet-2",
        "inlet-3",
    ]
    fault_tolerant.setup_size_controls.add_child_and_update(defer_update=False)
    fault_tolerant.setup_size_controls.local_settings_name = "default-proximity"
    fault_tolerant.setup_size_controls.local_size_control_parameters.sizing_type = (
        "proximity"
    )
    fault_tolerant.setup_size_controls.object_selection_list = [
        "inlet-1",
        "inlet-2",
        "inlet-3",
    ]
    fault_tolerant.setup_size_controls.add_child_and_update(defer_update=False)

    # Choose mesh control options
    fault_tolerant.choose_mesh_control_options()

    # Generate surface mesh
    fault_tolerant.generate_surface_mesh()

    # Update boundaries
    fault_tolerant.update_boundaries()

    # Add boundary layers
    fault_tolerant.add_boundary_layers.control_name.set_state("aspect-ratio_1")
    fault_tolerant.add_boundary_layers.insert_compound_child_task()
    fault_tolerant.add_boundary_layers_child_1()

    # Generate volume mesh
    generate_volume_mesh = fault_tolerant.create_volume_mesh_ftm
    generate_volume_mesh.all_region_name_list.set_state(
        [
            "main",
            "flow_pipe",
            "outpipe3",
            "object2",
            "object1",
            "void-region-1",
            "fluid-region-1",
        ]
    )
    generate_volume_mesh.all_region_size_list.set_state(["11.33375"] * 7)
    generate_volume_mesh.all_region_volume_fill_list.set_state(["none"] * 6 + ["tet"])
    generate_volume_mesh()

    solver = meshing.switch_to_solver()
    assert solver.is_active() is True
    assert meshing.is_active() is False
    solver.exit()
    assert solver.is_active() is False


@pytest.mark.nightly
@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=26.1")
def test_new_2d_meshing_workflow_enhanced_meshing(
    new_meshing_session_wo_exit, use_server_meshing_workflow
):
    # Import geometry
    import_file_name = examples.download_file("NACA0012.fmd", "pyfluent/airfoils")
    two_dim_mesh = new_meshing_session_wo_exit.two_dimensional_meshing()

    two_dim_mesh.load_cad_geometry.file_name = import_file_name
    two_dim_mesh.load_cad_geometry.length_unit = "mm"
    two_dim_mesh.load_cad_geometry.refaceting.refacet = False
    two_dim_mesh.load_cad_geometry()

    # Set regions and boundaries
    two_dim_mesh.update_boundaries.selection_type = "zone"
    two_dim_mesh.update_boundaries()

    # Define global sizing
    two_dim_mesh.define_global_sizing.curvature_normal_angle = 20
    two_dim_mesh.define_global_sizing.max_size = 2000.0
    two_dim_mesh.define_global_sizing.min_size = 5.0
    two_dim_mesh.define_global_sizing.size_functions = "Curvature"
    two_dim_mesh.define_global_sizing()

    # Add local sizing
    two_dim_mesh.add_local_sizing_wtm.add_child = "yes"
    two_dim_mesh.add_local_sizing_wtm.boi_control_name = "boi_1"
    two_dim_mesh.add_local_sizing_wtm.boi_execution = "Body Of Influence"
    two_dim_mesh.add_local_sizing_wtm.boi_face_label_list = ["boi"]
    two_dim_mesh.add_local_sizing_wtm.boi_size = 50.0
    two_dim_mesh.add_local_sizing_wtm.boi_zoneor_label = "label"
    two_dim_mesh.add_local_sizing_wtm.draw_size_control = True
    two_dim_mesh.add_local_sizing_wtm.add_child_and_update(defer_update=False)

    two_dim_mesh.add_local_sizing_wtm.add_child = "yes"
    two_dim_mesh.add_local_sizing_wtm.boi_control_name = "edgesize_1"
    two_dim_mesh.add_local_sizing_wtm.boi_execution = "Edge Size"
    two_dim_mesh.add_local_sizing_wtm.boi_size = 5.0
    two_dim_mesh.add_local_sizing_wtm.boi_zoneor_label = "label"
    two_dim_mesh.add_local_sizing_wtm.draw_size_control = True
    two_dim_mesh.add_local_sizing_wtm.edge_label_list = ["airfoil-te"]
    two_dim_mesh.add_local_sizing_wtm.add_child_and_update(defer_update=False)

    two_dim_mesh.add_local_sizing_wtm.add_child = "yes"
    two_dim_mesh.add_local_sizing_wtm.boi_control_name = "curvature_1"
    two_dim_mesh.add_local_sizing_wtm.boi_curvature_normal_angle = 10
    two_dim_mesh.add_local_sizing_wtm.boi_execution = "Curvature"
    two_dim_mesh.add_local_sizing_wtm.boi_max_size = 2
    two_dim_mesh.add_local_sizing_wtm.boi_min_size = 1.5
    two_dim_mesh.add_local_sizing_wtm.boi_scope_to = "edges"
    two_dim_mesh.add_local_sizing_wtm.boi_zoneor_label = "label"
    two_dim_mesh.add_local_sizing_wtm.draw_size_control = True
    two_dim_mesh.add_local_sizing_wtm.edge_label_list = ["airfoil"]
    two_dim_mesh.add_local_sizing_wtm.add_child_and_update(defer_update=False)

    # Add boundary layer
    two_dim_mesh.add_2d_boundary_layers.add_child = "yes"
    two_dim_mesh.add_2d_boundary_layers.bl_control_name = "aspect-ratio_1"
    two_dim_mesh.add_2d_boundary_layers.number_of_layers = 4
    two_dim_mesh.add_2d_boundary_layers.offset_method_type = "aspect-ratio"
    two_dim_mesh.add_2d_boundary_layers.add_child_and_update(defer_update=False)

    # NOTE: Setting `show_advanced_options = True` is required to configure advanced preferences.
    # This dependency may be removed in a future release as the API evolves.
    two_dim_mesh.generate_initial_surface_mesh.surface_2d_preferences.show_advanced_options = True
    two_dim_mesh.generate_initial_surface_mesh.surface_2d_preferences.merge_edge_zones_based_on_labels = "no"
    two_dim_mesh.generate_initial_surface_mesh.surface_2d_preferences.merge_face_zones_based_on_labels = "no"
    two_dim_mesh.generate_initial_surface_mesh()

    two_dim_mesh.add_2d_boundary_layers_child_1.revert()
    two_dim_mesh.add_2d_boundary_layers_child_1.add_child = "yes"
    two_dim_mesh.add_2d_boundary_layers_child_1.bl_control_name = "uniform_1"
    two_dim_mesh.add_2d_boundary_layers_child_1.first_layer_height = 2
    two_dim_mesh.add_2d_boundary_layers_child_1.number_of_layers = 4
    two_dim_mesh.add_2d_boundary_layers_child_1.offset_method_type = "uniform"
    two_dim_mesh.add_2d_boundary_layers_child_1()

    # NOTE: Setting `show_advanced_options = True` is required to configure advanced preferences.
    # This dependency may be removed in a future release as the API evolves.
    two_dim_mesh.generate_initial_surface_mesh.surface_2d_preferences.show_advanced_options = True
    two_dim_mesh.generate_initial_surface_mesh.surface_2d_preferences.merge_edge_zones_based_on_labels = "no"
    two_dim_mesh.generate_initial_surface_mesh.surface_2d_preferences.merge_face_zones_based_on_labels = "no"
    two_dim_mesh.generate_initial_surface_mesh()

    # Switch to solution mode
    solver = new_meshing_session_wo_exit.switch_to_solver()
    assert solver.is_active() is True
    assert new_meshing_session_wo_exit.is_active() is False
    solver.exit()
    assert solver.is_active() is False


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=26.1")
def test_workflow_and_data_model_methods_new_meshing_workflow(
    new_meshing_session, use_server_meshing_workflow
):
    meshing = new_meshing_session
    watertight = meshing.watertight()
    _next_possible_tasks = [
        "<Insertable 'import_boi_geometry' task>",
        "<Insertable 'set_up_rotational_periodic_boundaries' task>",
        "<Insertable 'create_local_refinement_regions' task>",
        "<Insertable 'custom_journal_task' task>",
    ]
    assert sorted(
        [repr(x) for x in watertight.import_geometry.insertable_tasks()]
    ) == sorted(_next_possible_tasks)
    watertight.import_geometry.insertable_tasks.import_boi_geometry.insert()
    assert sorted(
        [repr(x) for x in watertight.import_geometry.insertable_tasks()]
    ) == sorted(_next_possible_tasks)
    watertight.import_geometry.insertable_tasks.set_up_rotational_periodic_boundaries.insert()
    assert len(watertight.tasks()) == 13


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=26.1")
def test_duplicate_tasks(new_meshing_session, use_server_meshing_workflow):
    meshing = new_meshing_session
    watertight = meshing.watertight()

    _next_possible_tasks = [
        "<Insertable 'import_boi_geometry' task>",
        "<Insertable 'set_up_rotational_periodic_boundaries' task>",
        "<Insertable 'create_local_refinement_regions' task>",
        "<Insertable 'custom_journal_task' task>",
    ]
    assert sorted(
        [repr(x) for x in watertight.import_geometry.insertable_tasks()]
    ) == sorted(_next_possible_tasks)
    watertight.import_geometry.insertable_tasks.import_boi_geometry.insert()
    watertight.import_geometry.insertable_tasks.import_boi_geometry.insert()
    watertight.import_geometry.insertable_tasks.import_boi_geometry.insert()

    assert watertight.import_boi_geometry.name() == "Import Body of Influence Geometry"
    assert (
        watertight.import_boi_geometry[1].name()
        == "Import Body of Influence Geometry 1"
    )
    assert (
        watertight.import_boi_geometry[2].name()
        == "Import Body of Influence Geometry 2"
    )

    watertight.import_boi_geometry[1].rename(new_name="Renamed BOI task")

    with pytest.raises(LookupError):
        watertight.import_boi_geometry[1].name()

    assert (
        watertight.import_boi_geometry["Renamed BOI task"].name() == "Renamed BOI task"
    )


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=26.1")
def test_watertight_workflow(
    mixing_elbow_geometry_filename, new_meshing_session, use_server_meshing_workflow
):
    watertight = new_meshing_session.watertight()
    watertight.import_geometry.file_name = mixing_elbow_geometry_filename
    watertight.import_geometry()
    add_local_sizing = watertight.add_local_sizing_wtm
    assert not add_local_sizing.task_list()
    add_local_sizing.add_child = True
    add_local_sizing.boi_face_label_list = ["cold-inlet", "hot-inlet"]
    add_local_sizing.add_child_and_update()
    assert add_local_sizing._task_names() == ["facesize_1"]
    assert watertight.add_local_sizing_wtm_child_1.name() == "facesize_1"
    assert watertight.add_local_sizing_wtm["facesize_1"].name() == "facesize_1"


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=26.1")
def test_delete_interface(new_meshing_session, use_server_meshing_workflow):
    watertight = new_meshing_session.watertight()

    watertight.import_geometry.insertable_tasks.import_boi_geometry.insert()
    watertight.import_geometry.insertable_tasks.import_boi_geometry.insert()

    assert watertight.import_boi_geometry.name() == "Import Body of Influence Geometry"
    assert (
        watertight.import_boi_geometry[1].name()
        == "Import Body of Influence Geometry 1"
    )

    assert len(watertight.tasks()) == 13
    del watertight.import_boi_geometry[1]
    watertight.import_boi_geometry.delete()
    assert len(watertight.tasks()) == 11

    assert "create_volume_mesh_wtm" in watertight.task_names()
    assert "add_boundary_layers" in watertight.task_names()
    watertight.delete_tasks(
        list_of_tasks=[
            watertight.create_volume_mesh_wtm,
            watertight.add_boundary_layers,
        ]
    )
    assert "create_volume_mesh_wtm" not in watertight.task_names()
    assert "add_boundary_layers" not in watertight.task_names()

    assert "update_regions" in watertight.task_names()
    watertight.update_regions.delete()
    assert "update_regions" not in watertight.task_names()

    assert "create_regions" in watertight.task_names()
    del watertight.create_regions
    assert "create_regions" not in watertight.task_names()


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=26.1")
def test_ordering_of_tasks(new_meshing_session, use_server_meshing_workflow):
    watertight = new_meshing_session.watertight()
    assert len(watertight.children()) == 7
    _watertight_tasks = [
        "task < import_geometry: 0 >",
        "task < add_local_sizing_wtm: 0 >",
        "task < create_surface_mesh: 0 >",
        "task < describe_geometry: 0 >",
        "task < update_regions: 0 >",
        "task < add_boundary_layers: 0 >",
        "task < create_volume_mesh_wtm: 0 >",
    ]
    assert sorted([repr(x) for x in watertight.children()]) == sorted(_watertight_tasks)

    assert watertight.import_geometry.children() == []
    assert len(watertight.describe_geometry.children()) == 2

    assert repr(watertight.describe_geometry.first_child()) == "task < capping: 0 >"
    assert watertight.describe_geometry.first_child().has_parent()
    assert (
        repr(watertight.describe_geometry.first_child().parent())
        == "task < describe_geometry: 0 >"
    )
    assert (
        repr(watertight.describe_geometry.first_child().next())
        == "task < create_regions: 0 >"
    )

    assert not watertight.describe_geometry.first_child().has_previous()
    assert watertight.describe_geometry.first_child().has_next()
    assert (
        watertight.describe_geometry.first_child().next().previous().name()
        == "Enclose Fluid Regions (Capping)"
    )

    assert repr(watertight.first_child()) == "task < import_geometry: 0 >"
    assert (
        watertight.import_geometry.next().next().next().next().name()
        == "Update Regions"
    )

    watertight.import_geometry.insertable_tasks.import_boi_geometry.insert()
    watertight.import_geometry.insertable_tasks.import_boi_geometry.insert()

    assert watertight.import_boi_geometry[1].previous().name() == "Import Geometry"
    assert (
        watertight.import_boi_geometry[1].next().name()
        == "Import Body of Influence Geometry"
    )
    assert watertight.import_boi_geometry[1].next().next().name() == "Add Local Sizing"


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=26.1")
def test_workflow_type_checking(new_meshing_session, use_server_meshing_workflow):
    meshing = new_meshing_session
    watertight = meshing.watertight()

    wf_1 = watertight.first_child()

    assert repr(wf_1) == "task < import_geometry: 0 >"

    assert wf_1.insertable_tasks()

    wf_1.insertable_tasks.import_boi_geometry.insert()
    wf_1.insertable_tasks.import_boi_geometry.insert()

    assert repr(wf_1.next()) == "task < import_boi_geometry: 1 >"
    assert repr(wf_1.next().next()) == "task < import_boi_geometry: 0 >"


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=26.1")
def test_workflow_traversal(new_meshing_session, use_server_meshing_workflow):
    meshing = new_meshing_session
    watertight = meshing.watertight()

    assert len(watertight.children()) == 7

    wf_1 = watertight.first_child()
    assert wf_1.name() == "Import Geometry"
    assert wf_1.has_parent()
    assert wf_1.parent().__class__.__name__ == "WatertightMeshingWorkflow"
    assert wf_1.has_previous() is False
    assert wf_1.has_next()
    assert wf_1.first_child() is None
    assert wf_1.last_child() is None

    with pytest.raises(IndexError):
        wf_1.previous()

    wf_2 = wf_1.next()
    assert wf_2.name() == "Add Local Sizing"
    assert wf_2.has_previous()
    assert wf_2.has_next()

    wf_4 = wf_2.next().next()
    assert wf_4.name() == "Describe Geometry"
    wf_4_1 = wf_4.first_child()
    assert wf_4_1.name() == "Enclose Fluid Regions (Capping)"
    assert wf_4_1.has_next()
    assert wf_4_1.has_previous() is False

    assert wf_4_1.has_parent()
    assert wf_4_1.parent().name() == "Describe Geometry"

    wf_4_2 = wf_4.first_child().next()
    assert wf_4_2.name() == wf_4.last_child().name() == "Create Regions"
    assert wf_4_2.has_next() is False
    assert wf_4_2.has_previous()

    assert wf_4.next().name() == "Update Regions"

    wf_7 = watertight.last_child()
    assert wf_7.name() == "Generate the Volume Mesh"
    assert wf_7.has_previous()
    assert wf_7.has_next() is False

    with pytest.raises(IndexError):
        wf_7.next()

    wf_6 = wf_7.previous()
    assert wf_6.name() == "Add Boundary Layers"


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=26.1")
def test_new_watertight_workflow_using_traversal(
    new_meshing_session_wo_exit, use_server_meshing_workflow
):
    # Import geometry
    import_file_name = examples.download_file(
        "mixing_elbow.pmdb", "pyfluent/mixing_elbow"
    )
    watertight = new_meshing_session_wo_exit.watertight()
    wf_1 = watertight.first_child()
    wf_1.file_name.set_state(import_file_name)
    wf_1.length_unit = "in"
    wf_1()

    # Add local sizing
    assert wf_1.has_next()
    wf_2 = wf_1.next()
    wf_2.add_child_to_task()
    wf_2()

    # Generate surface mesh
    assert wf_2.has_next()
    wf_3 = wf_2.next()
    wf_3.cfd_surface_mesh_controls.max_size.set_state(0.3)
    wf_3()

    # Describe geometry
    assert wf_3.has_next()
    wf_4 = wf_3.next()
    wf_4.update_child_tasks(setup_type_changed=False)
    assert wf_4.setup_type.allowed_values() == ["fluid", "fluid_solid_voids", "solid"]
    wf_4.setup_type = "fluid"
    wf_4.update_child_tasks(setup_type_changed=True)
    wf_4()

    # Update boundaries
    wf_4_1 = wf_4.first_child()
    wf_4_1.boundary_zone_list.set_state(["wall-inlet"])
    wf_4_1.boundary_label_list.set_state(["wall-inlet"])
    wf_4_1.boundary_label_type_list.set_state(["wall"])
    wf_4_1.old_boundary_label_list.set_state(["wall-inlet"])
    wf_4_1.old_boundary_label_type_list.set_state(["velocity-inlet"])
    wf_4_1()

    # Update regions
    assert wf_4.has_next()
    wf_5 = wf_4.next()
    wf_5()

    # Add boundary layers
    assert wf_5.has_next()
    wf_6 = wf_5.next()
    wf_6.add_child_to_task()
    wf_6.control_name.set_state("smooth-transition_1")
    wf_6.insert_compound_child_task()
    assert wf_6.has_next()
    assert wf_6.first_child() is not None
    wf_6.first_child()()

    # Generate volume mesh
    assert wf_6.has_next()
    wf_7 = wf_6.next()

    wf_7.volume_fill.set_state("poly-hexcore")
    wf_7.volume_fill_controls.hex_max_cell_length = 0.3
    wf_7()

    assert wf_7.has_next() is False

    # Switch to solution mode
    solver = new_meshing_session_wo_exit.switch_to_solver()
    assert solver.is_active() is True
    assert new_meshing_session_wo_exit.is_active() is False
    solver.exit()
    assert solver.is_active() is False


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=26.1")
def test_created_workflow(new_meshing_session, use_server_meshing_workflow):
    meshing = new_meshing_session
    created_workflow = meshing.create_workflow()

    assert sorted([repr(x) for x in created_workflow.insertable_tasks()]) == sorted(
        [
            "<Insertable 'import_geometry' task>",
            "<Insertable 'import_cad_and_part_management' task>",
            "<Insertable 'custom_journal_task' task>",
        ]
    )

    created_workflow.insertable_tasks()[0].insert()

    assert created_workflow.insertable_tasks() == []

    assert "<Insertable 'add_local_sizing' task>" in [
        repr(x) for x in created_workflow.import_geometry.insertable_tasks()
    ]
    created_workflow.import_geometry.insertable_tasks.add_local_sizing.insert()
    assert "<Insertable 'add_local_sizing' task>" not in [
        repr(x) for x in created_workflow.import_geometry.insertable_tasks()
    ]
    assert sorted(created_workflow.task_names()) == sorted(
        ["import_geometry", "add_local_sizing_wtm"]
    )


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=26.1")
def test_loaded_workflow(new_meshing_session, use_server_meshing_workflow):
    meshing = new_meshing_session
    saved_workflow_path = examples.download_file(
        "sample_watertight_workflow.wft", "pyfluent/meshing_workflows"
    )
    loaded_workflow = meshing.load_workflow(file_path=saved_workflow_path)
    assert "set_up_rotational_periodic_boundaries" in loaded_workflow.task_names()
    assert "import_boi_geometry" in loaded_workflow.task_names()
