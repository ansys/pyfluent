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
    meshing.PartManagement.InputFileChanged(
        FilePath=import_file_name, IgnoreSolidNames=False, PartPerBody=False
    )
    meshing.PMFileManagement.FileManager.LoadFiles()
    meshing.PartManagement.Node["Meshing Model"].Copy(
        Paths=[
            "/dirty_manifold-for-wrapper," + "1/dirty_manifold-for-wrapper,1/main,1",
            "/dirty_manifold-for-wrapper,"
            + "1/dirty_manifold-for-wrapper,1/flow-pipe,1",
            "/dirty_manifold-for-wrapper,"
            + "1/dirty_manifold-for-wrapper,1/outpipe3,1",
            "/dirty_manifold-for-wrapper," + "1/dirty_manifold-for-wrapper,1/object2,1",
            "/dirty_manifold-for-wrapper," + "1/dirty_manifold-for-wrapper,1/object1,1",
        ]
    )
    meshing.PartManagement.ObjectSetting["DefaultObjectSetting"].OneZonePer.set_state(
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
    watertight.task_object.import_geometry["Import Geometry"].arguments.length_unit = (
        "m"
    )
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
