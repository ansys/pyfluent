import time
from typing import Iterable

import pytest

from ansys.fluent.core import examples
from ansys.fluent.core.meshing.watertight import watertight_workflow
from ansys.fluent.core.utils.fluent_version import FluentVersion
from tests.test_datamodel_service import disable_datamodel_cache  # noqa: F401


@pytest.mark.nightly
@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=23.2")
def test_new_watertight_workflow(new_mesh_session):
    # Import geometry
    import_file_name = examples.download_file(
        "mixing_elbow.pmdb", "pyfluent/mixing_elbow"
    )
    watertight = new_mesh_session.watertight()
    watertight.import_geometry.file_name.set_state(import_file_name)
    assert watertight.import_geometry.length_unit() == "mm"
    watertight.import_geometry.length_unit.set_state("in")
    assert watertight.import_geometry.length_unit.get_state() == "in"
    watertight.import_geometry()

    # Add local sizing
    watertight.add_local_sizing.add_child_to_task()
    watertight.add_local_sizing()

    # Generate surface mesh
    assert (
        round(
            watertight.create_surface_mesh.cfd_surface_mesh_controls.max_size.get_state(),
            5,
        )
        == 0.41831
    )
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
    watertight.add_boundary_layer.add_child_to_task()
    watertight.add_boundary_layer.insert_compound_child_task()
    watertight.task("smooth-transition_1").bl_control_name.set_state(
        "smooth-transition_1"
    )
    watertight.add_boundary_layer.arguments = {}
    watertight.task("smooth-transition_1")()

    # Generate volume mesh
    watertight.create_volume_mesh.volume_fill.set_state("poly-hexcore")
    watertight.create_volume_mesh.volume_fill_controls.hex_max_cell_length.set_state(
        0.3
    )
    watertight.create_volume_mesh()

    # Switch to solution mode
    solver = new_mesh_session.switch_to_solver()
    assert solver


@pytest.mark.nightly
@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=23.2")
def test_new_fault_tolerant_workflow(new_mesh_session):
    meshing = new_mesh_session

    # Import CAD and part management
    import_file_name = examples.download_file(
        "exhaust_system.fmd", "pyfluent/exhaust_system"
    )
    fault_tolerant = meshing.fault_tolerant()
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
    fault_tolerant.import_cad_and_part_management.context.set_state(0)
    fault_tolerant.import_cad_and_part_management.create_object_per.set_state("Custom")
    fault_tolerant.import_cad_and_part_management.fmd_file_name.set_state(
        import_file_name
    )
    fault_tolerant.import_cad_and_part_management.file_loaded.set_state("yes")
    fault_tolerant.import_cad_and_part_management.object_setting.set_state(
        "DefaultObjectSetting"
    )
    fault_tolerant.import_cad_and_part_management.options.line.set_state(False)
    fault_tolerant.import_cad_and_part_management.options.solid.set_state(False)
    fault_tolerant.import_cad_and_part_management.options.surface.set_state(False)
    fault_tolerant.import_cad_and_part_management()

    # Describe geometry and flow
    fault_tolerant.describe_geometry_and_flow.add_enclosure.set_state("No")
    fault_tolerant.describe_geometry_and_flow.close_caps.set_state("Yes")
    fault_tolerant.describe_geometry_and_flow.flow_type.set_state(
        "Internal flow through the object"
    )
    fault_tolerant.describe_geometry_and_flow.update_child_tasks(
        setup_type_changed=False
    )

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
    fault_tolerant.enclose_fluid_regions_fault.create_patch_preferences.show_create_patch_preferences.set_state(
        False
    )
    fault_tolerant.enclose_fluid_regions_fault.patch_name.set_state("inlet-1")
    fault_tolerant.enclose_fluid_regions_fault.selection_type.set_state("zone")
    fault_tolerant.enclose_fluid_regions_fault.zone_selection_list.set_state(
        ["inlet.1"]
    )

    fault_tolerant.enclose_fluid_regions_fault.create_patch_preferences.show_create_patch_preferences.set_state(
        False
    )
    fault_tolerant.enclose_fluid_regions_fault.patch_name.set_state("inlet-1")
    fault_tolerant.enclose_fluid_regions_fault.selection_type.set_state("zone")
    fault_tolerant.enclose_fluid_regions_fault.zone_location.set_state(
        [
            "1",
            "351.68205",
            "-361.34322",
            "-301.88668",
            "396.96205",
            "-332.84759",
            "-266.69751",
            "inlet.1",
        ]
    )
    fault_tolerant.enclose_fluid_regions_fault.zone_selection_list.set_state(
        ["inlet.1"]
    )
    fault_tolerant.enclose_fluid_regions_fault.add_child_to_task()
    fault_tolerant.enclose_fluid_regions_fault.insert_compound_child_task()
    fault_tolerant.enclose_fluid_regions_fault.arguments.set_state({})
    fault_tolerant.task("inlet-1")()

    fault_tolerant.enclose_fluid_regions_fault.patch_name.set_state("inlet-2")
    fault_tolerant.enclose_fluid_regions_fault.selection_type.set_state("zone")
    fault_tolerant.enclose_fluid_regions_fault.zone_selection_list.set_state(
        ["inlet.2"]
    )

    fault_tolerant.enclose_fluid_regions_fault.patch_name.set_state("inlet-2")
    fault_tolerant.enclose_fluid_regions_fault.selection_type.set_state("zone")
    fault_tolerant.enclose_fluid_regions_fault.zone_location.set_state(
        [
            "1",
            "441.68205",
            "-361.34322",
            "-301.88668",
            "486.96205",
            "-332.84759",
            "-266.69751",
            "inlet.2",
        ]
    )
    fault_tolerant.enclose_fluid_regions_fault.zone_selection_list.set_state(
        ["inlet.2"]
    )
    fault_tolerant.enclose_fluid_regions_fault.add_child_to_task()
    fault_tolerant.enclose_fluid_regions_fault.insert_compound_child_task()
    fault_tolerant.enclose_fluid_regions_fault.arguments.set_state({})
    fault_tolerant.task("inlet-2")()

    fault_tolerant.enclose_fluid_regions_fault.patch_name.set_state("inlet-3")
    fault_tolerant.enclose_fluid_regions_fault.selection_type.set_state("zone")
    fault_tolerant.enclose_fluid_regions_fault.zone_selection_list.set_state(["inlet"])

    fault_tolerant.enclose_fluid_regions_fault.patch_name.set_state("inlet-3")
    fault_tolerant.enclose_fluid_regions_fault.selection_type.set_state("zone")
    fault_tolerant.enclose_fluid_regions_fault.zone_location.set_state(
        [
            "1",
            "261.68205",
            "-361.34322",
            "-301.88668",
            "306.96205",
            "-332.84759",
            "-266.69751",
            "inlet",
        ]
    )
    fault_tolerant.enclose_fluid_regions_fault.zone_selection_list.set_state(["inlet"])
    fault_tolerant.enclose_fluid_regions_fault.add_child_to_task()
    fault_tolerant.enclose_fluid_regions_fault.insert_compound_child_task()
    fault_tolerant.enclose_fluid_regions_fault.arguments.set_state({})
    fault_tolerant.task("inlet-3")()

    fault_tolerant.enclose_fluid_regions_fault.patch_name.set_state("outlet-1")
    fault_tolerant.enclose_fluid_regions_fault.selection_type.set_state("zone")
    fault_tolerant.enclose_fluid_regions_fault.zone_selection_list.set_state(["outlet"])
    fault_tolerant.enclose_fluid_regions_fault.zone_type.set_state("pressure-outlet")

    fault_tolerant.enclose_fluid_regions_fault.patch_name.set_state("outlet-1")
    fault_tolerant.enclose_fluid_regions_fault.selection_type.set_state("zone")
    fault_tolerant.enclose_fluid_regions_fault.zone_location.set_state(
        [
            "1",
            "352.22702",
            "-197.8957",
            "84.102381",
            "394.41707",
            "-155.70565",
            "84.102381",
            "outlet",
        ]
    )
    fault_tolerant.enclose_fluid_regions_fault.zone_selection_list.set_state(["outlet"])
    fault_tolerant.enclose_fluid_regions_fault.zone_type.set_state("pressure-outlet")
    fault_tolerant.enclose_fluid_regions_fault.add_child_to_task()
    fault_tolerant.enclose_fluid_regions_fault.insert_compound_child_task()
    fault_tolerant.enclose_fluid_regions_fault.arguments.set_state({})
    fault_tolerant.task("outlet-1")()

    # Extract edge features
    fault_tolerant.extract_edge_features.extract_method_type.set_state(
        "Intersection Loops"
    )
    fault_tolerant.extract_edge_features.object_selection_list.set_state(
        ["flow_pipe", "main"]
    )
    fault_tolerant.extract_edge_features.add_child_to_task()
    fault_tolerant.extract_edge_features.insert_compound_child_task()

    fault_tolerant.extract_edge_features.extract_edges_name.set_state("edge-group-1")
    fault_tolerant.extract_edge_features.extract_method_type.set_state(
        "Intersection Loops"
    )
    fault_tolerant.extract_edge_features.object_selection_list.set_state(
        ["flow_pipe", "main"]
    )

    fault_tolerant.extract_edge_features.arguments.set_state({})
    fault_tolerant.task("edge-group-1")()

    # Identify regions
    fault_tolerant.identify_regions.selection_type.set_state("zone")
    fault_tolerant.identify_regions.x.set_state(377.322045740589)
    fault_tolerant.identify_regions.y.set_state(-176.800676988458)
    fault_tolerant.identify_regions.z.set_state(-37.0764628583475)
    fault_tolerant.identify_regions.zone_selection_list.set_state(["main.1"])

    fault_tolerant.identify_regions.selection_type.set_state("zone")
    fault_tolerant.identify_regions.x.set_state(377.322045740589)
    fault_tolerant.identify_regions.y.set_state(-176.800676988458)
    fault_tolerant.identify_regions.z.set_state(-37.0764628583475)
    fault_tolerant.identify_regions.zone_location.set_state(
        [
            "1",
            "213.32205",
            "-225.28068",
            "-158.25531",
            "541.32205",
            "-128.32068",
            "84.102381",
            "main.1",
        ]
    )
    fault_tolerant.identify_regions.zone_selection_list.set_state(["main.1"])
    fault_tolerant.identify_regions.add_child_to_task()
    fault_tolerant.identify_regions.insert_compound_child_task()

    fault_tolerant.task("fluid-region-1").material_points_name.set_state(
        "fluid-region-1"
    )
    fault_tolerant.task("fluid-region-1").selection_type.set_state("zone")
    fault_tolerant.identify_regions.x.set_state(377.322045740589)
    fault_tolerant.identify_regions.y.set_state(-176.800676988458)
    fault_tolerant.identify_regions.z.set_state(-37.0764628583475)
    fault_tolerant.identify_regions.zone_location.set_state(
        [
            "1",
            "213.32205",
            "-225.28068",
            "-158.25531",
            "541.32205",
            "-128.32068",
            "84.102381",
            "main.1",
        ]
    )
    fault_tolerant.identify_regions.zone_selection_list.set_state(["main.1"])
    fault_tolerant.identify_regions.arguments.set_state({})
    fault_tolerant.task("fluid-region-1")()

    fault_tolerant.identify_regions.material_points_name.set_state("void-region-1")
    fault_tolerant.identify_regions.new_region_type.set_state("void")
    fault_tolerant.identify_regions.object_selection_list.set_state(
        ["inlet-1", "inlet-2", "inlet-3", "main"]
    )
    fault_tolerant.identify_regions.x.set_state(374.722045740589)
    fault_tolerant.identify_regions.y.set_state(-278.9775145640143)
    fault_tolerant.identify_regions.z.set_state(-161.1700719416913)
    fault_tolerant.identify_regions.add_child_to_task()
    fault_tolerant.identify_regions.insert_compound_child_task()
    fault_tolerant.identify_regions.arguments.set_state({})
    fault_tolerant.task("void-region-1")()

    # Define leakage threshold
    fault_tolerant.define_leakage_threshold.add_child.set_state("yes")
    fault_tolerant.define_leakage_threshold.flip_direction.set_state(True)
    fault_tolerant.define_leakage_threshold.plane_direction.set_state("X")
    fault_tolerant.define_leakage_threshold.region_selection_single.set_state(
        "void-region-1"
    )
    fault_tolerant.define_leakage_threshold.add_child_to_task()
    fault_tolerant.define_leakage_threshold.insert_compound_child_task()

    fault_tolerant.task("leakage-1").arguments.set_state(
        {
            "add_child": "yes",
            "flip_direction": True,
            "leakage_name": "leakage-1",
            "plane_direction": "X",
            "region_selection_single": "void-region-1",
        }
    )

    fault_tolerant.define_leakage_threshold.add_child.set_state("yes")

    fault_tolerant.task("leakage-1")()

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
    fault_tolerant.update_region_settings.old_region_leakage_size_list.set_state([""])
    fault_tolerant.update_region_settings.old_region_mesh_method_list.set_state(
        ["wrap"]
    )
    fault_tolerant.update_region_settings.old_region_name_list.set_state(
        ["fluid-region-1"]
    )
    fault_tolerant.update_region_settings.old_region_overset_componen_list.set_state(
        ["no"]
    )
    fault_tolerant.update_region_settings.old_region_type_list.set_state(["fluid"])
    fault_tolerant.update_region_settings.old_region_volume_fill_list.set_state(
        ["hexcore"]
    )
    fault_tolerant.update_region_settings.region_leakage_size_list.set_state([""])
    fault_tolerant.update_region_settings.region_mesh_method_list.set_state(["wrap"])
    fault_tolerant.update_region_settings.region_name_list.set_state(["fluid-region-1"])
    fault_tolerant.update_region_settings.region_overset_componen_list.set_state(["no"])
    fault_tolerant.update_region_settings.region_type_list.set_state(["fluid"])
    fault_tolerant.update_region_settings.region_volume_fill_list.set_state(["tet"])
    fault_tolerant.update_region_settings()

    # Choose mesh control options
    fault_tolerant.choose_mesh_control_options()

    # Generate surface mesh
    fault_tolerant.generate_the_surface_mesh()

    # Update boundaries
    fault_tolerant.update_boundaries_ftm()

    # Add boundary layers
    fault_tolerant.add_boundary_layer_ftm.add_child_to_task()
    fault_tolerant.add_boundary_layer_ftm.insert_compound_child_task()
    fault_tolerant.task("aspect-ratio_1").bl_control_name.set_state("aspect-ratio_1")
    fault_tolerant.add_boundary_layer_ftm.arguments.set_state({})
    fault_tolerant.task("aspect-ratio_1")()

    # Generate volume mesh
    fault_tolerant.generate_the_volume_mesh.all_region_name_list.set_state(
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
    fault_tolerant.generate_the_volume_mesh.all_region_size_list.set_state(
        ["11.33375"] * 7
    )
    fault_tolerant.generate_the_volume_mesh.all_region_volume_fill_list.set_state(
        ["none"] * 6 + ["tet"]
    )
    fault_tolerant.generate_the_volume_mesh.enable_parallel.set_state(True)
    fault_tolerant.generate_the_volume_mesh()

    # Generate volume mesh
    solver = meshing.switch_to_solver()
    assert solver


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=23.2")
def test_updating_state_in_new_meshing_workflow(new_mesh_session):
    # Import geometry
    import_file_name = examples.download_file(
        "mixing_elbow.pmdb", "pyfluent/mixing_elbow"
    )
    watertight = new_mesh_session.watertight()
    watertight.import_geometry.file_name.set_state(import_file_name)
    assert watertight.import_geometry.length_unit() == "mm"
    watertight.import_geometry.length_unit = "in"
    assert watertight.import_geometry.length_unit.get_state() == "in"
    assert watertight.import_geometry.cad_import_options.feature_angle() == 40.0
    watertight.import_geometry.cad_import_options.feature_angle.set_state(25.0)
    assert watertight.import_geometry.cad_import_options.feature_angle() == 25.0
    assert (
        watertight.import_geometry.cad_import_options.one_zone_per.allowed_values()
        == ["body", "face", "object"]
    )
    assert watertight.import_geometry.cad_import_options.one_zone_per() == "body"
    watertight.import_geometry.cad_import_options.one_zone_per = "face"
    assert watertight.import_geometry.cad_import_options.one_zone_per() == "face"
    watertight.import_geometry()


def _assert_snake_case_attrs(attrs: Iterable):
    for attr in attrs:
        assert str(attr).islower()


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=23.2")
def test_snake_case_attrs_in_new_meshing_workflow(new_mesh_session):
    # Import geometry
    import_file_name = examples.download_file(
        "mixing_elbow.pmdb", "pyfluent/mixing_elbow"
    )
    watertight = new_mesh_session.watertight()
    _assert_snake_case_attrs(dir(watertight))
    _assert_snake_case_attrs(dir(watertight.import_geometry))
    _assert_snake_case_attrs(watertight.import_geometry.arguments())
    _assert_snake_case_attrs(watertight.import_geometry.cad_import_options())
    _assert_snake_case_attrs(dir(watertight.import_geometry.cad_import_options))
    watertight.import_geometry.file_name.set_state(import_file_name)
    watertight.import_geometry.length_unit = "in"
    watertight.import_geometry()


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=24.1")
def test_workflow_and_data_model_methods_new_meshing_workflow(new_mesh_session):
    # Import geometry
    meshing = new_mesh_session
    import_file_name = examples.download_file(
        "mixing_elbow.pmdb", "pyfluent/mixing_elbow"
    )
    watertight = meshing.watertight()

    # Checks if any of the unwanted attrs are present in dir call
    assert (set(dir(watertight)) - watertight._unwanted_attrs) == set(dir(watertight))

    for attr in watertight._unwanted_attrs:
        with pytest.raises(AttributeError):
            getattr(watertight, attr)

    watertight.import_geometry.rename(new_name="import_geom_wtm")
    assert len(watertight._task_list) == 11
    watertight.insert_new_task("import_geometry")
    assert len(watertight._task_list) == 12
    watertight.task("import_geom_wtm").file_name = import_file_name
    watertight.task("import_geom_wtm").length_unit = "in"
    watertight.task("import_geom_wtm")()
    _next_possible_tasks = [
        "import_body_of_influence_geometry",
        "set_up_periodic_boundaries",
        "create_local_refinement_regions",
        "load_cad_geometry",
        "run_custom_journal",
    ]
    if meshing.get_fluent_version() < FluentVersion.v242:
        _next_possible_tasks.remove("load_cad_geometry")
    assert (
        watertight.task("import_geom_wtm").get_next_possible_tasks()
        == _next_possible_tasks
    )
    watertight.task("import_geom_wtm").insert_next_task(
        "import_body_of_influence_geometry"
    )
    watertight.task("import_geom_wtm").insert_next_task("set_up_periodic_boundaries")
    assert len(watertight._task_list) == 14


@pytest.mark.fluent_version(">=23.2")
@pytest.mark.codegen_required
def test_watertight_workflow(mixing_elbow_geometry, new_mesh_session):
    watertight = watertight_workflow(
        geometry_file_name=mixing_elbow_geometry, session=new_mesh_session
    )
    add_local_sizing = watertight.add_local_sizing
    assert not add_local_sizing.ordered_children()
    add_local_sizing._add_child(state={"boi_face_label_list": ["cold-inlet"]})
    assert not add_local_sizing.ordered_children()
    added_sizing = add_local_sizing.add_child_and_update(
        state={"boi_face_label_list": ["elbow-fluid"]}
    )
    assert len(add_local_sizing.ordered_children()) == 1
    assert added_sizing
    assert added_sizing.boi_face_label_list() == ["elbow-fluid"]


@pytest.mark.fluent_version(">=23.2")
@pytest.mark.codegen_required
def test_watertight_workflow_children(mixing_elbow_geometry, new_mesh_session):
    watertight = watertight_workflow(
        geometry_file_name=mixing_elbow_geometry, session=new_mesh_session
    )
    add_local_sizing = watertight.add_local_sizing
    assert not add_local_sizing.ordered_children()
    add_local_sizing._add_child(state={"boi_face_label_list": ["cold-inlet"]})
    assert not add_local_sizing.ordered_children()
    added_sizing = add_local_sizing.add_child_and_update(
        state={"boi_face_label_list": ["elbow-fluid"]}
    )
    assert len(add_local_sizing.ordered_children()) == 1
    assert added_sizing
    assert added_sizing.boi_face_label_list() == ["elbow-fluid"]
    assert added_sizing.name() == "facesize_1"
    assert len(added_sizing.arguments())
    added_sizing_by_name = add_local_sizing.compound_child("facesize_1")
    added_sizing_by_pos = add_local_sizing.last_child()
    assert added_sizing.arguments() == added_sizing_by_name.arguments()
    assert added_sizing.arguments() == added_sizing_by_pos.arguments()
    assert not added_sizing.python_name()
    describe_geometry = watertight.describe_geometry
    describe_geometry_children = describe_geometry.ordered_children()
    assert len(describe_geometry_children) == 2
    describe_geometry_child_task_python_names = (
        describe_geometry.child_task_python_names()
    )
    assert describe_geometry_child_task_python_names == [
        "enclose_fluid_regions",
        "create_regions",
    ]


@pytest.mark.skip("Randomly failing in CI")
@pytest.mark.fluent_version(">=23.2")
@pytest.mark.codegen_required
def test_watertight_workflow_dynamic_interface(mixing_elbow_geometry, new_mesh_session):
    watertight = watertight_workflow(
        geometry_file_name=mixing_elbow_geometry, session=new_mesh_session
    )
    create_volume_mesh = watertight.create_volume_mesh
    assert create_volume_mesh is not None
    watertight.delete_tasks(list_of_tasks=["create_volume_mesh"])
    # I assume that what's going on here is that due to DeleteTasks we are triggering
    # change events in the server but those events are (still) being transmitted after
    # DeleteTasks has returned. Hence, the dynamic watertight Python interface
    # is still updating after the command has returned and the client can try to access
    # while it is in that update phase, leading to (difficult to understand) exceptions.
    # Temporarily sleeping in the test. I note that the core event tests use sleeps also.
    with pytest.raises(AttributeError):
        watertight.create_volume_mesh

    watertight.insert_new_task(command_name="create_volume_mesh")
    time.sleep(2.5)
    create_volume_mesh = watertight.create_volume_mesh
    assert create_volume_mesh is not None

    watertight_geom = watertight.describe_geometry
    assert watertight_geom.create_regions.arguments()["number_of_flow_volumes"] == 1
    watertight.delete_tasks(list_of_tasks=["create_regions"])
    assert watertight_geom.create_regions is None
    assert watertight_geom.enclose_fluid_regions
    watertight_geom.enclose_fluid_regions.delete()
    assert watertight_geom.enclose_fluid_regions is None
    watertight.create_volume_mesh.delete()
    with pytest.raises(AttributeError):
        watertight.create_volume_mesh


@pytest.mark.fluent_version(">=23.2")
@pytest.mark.codegen_required
def test_extended_wrapper(new_mesh_session, mixing_elbow_geometry):
    watertight = new_mesh_session.watertight()
    import_geometry = watertight.import_geometry
    assert import_geometry.Arguments() == {}
    import_geometry.Arguments = dict(FileName=mixing_elbow_geometry)
    assert 8 < len(import_geometry.arguments.get_state()) < 15
    assert len(import_geometry.arguments.get_state(explicit_only=True)) == 1
    import_geometry.arguments.set_state(dict(file_name=None))
    time.sleep(5)
    assert import_geometry.arguments.get_state(explicit_only=True) == dict(
        file_name=None
    )
    assert import_geometry.arguments.get_state()["file_name"] is None
    import_geometry.arguments.set_state(dict(file_name=mixing_elbow_geometry))
    time.sleep(5)
    assert import_geometry.arguments.get_state(explicit_only=True) == dict(
        file_name=mixing_elbow_geometry
    )
    assert import_geometry.file_name() == mixing_elbow_geometry
    import_geometry.file_name.set_state("bob")
    time.sleep(5)
    assert import_geometry.file_name() == "bob"
    import_geometry.file_name.set_state(mixing_elbow_geometry)
    import_geometry()
    add_local_sizing = watertight.add_local_sizing
    assert not add_local_sizing.ordered_children()
    # new_mesh_session.workflow.TaskObject["Add Local Sizing"]._add_child(state={"BOIFaceLabelList": ["elbow-fluid"]})
    add_local_sizing._add_child(state={"boi_face_label_list": ["cold-inlet"]})
    assert not add_local_sizing.ordered_children()

    added_sizing = add_local_sizing.add_child_and_update(
        state={"boi_face_label_list": ["elbow-fluid"]}
    )
    assert len(add_local_sizing.ordered_children()) == 1
    assert added_sizing
    assert added_sizing.boi_face_label_list() == ["elbow-fluid"]
    # restart
    watertight = new_mesh_session.watertight()
    assert import_geometry.state() == "Out-of-date"
    import_geometry(FileName=mixing_elbow_geometry, AppendMesh=False)
    assert import_geometry.state() == "Up-to-date"
    import_geometry_state = import_geometry.arguments()
    assert len(import_geometry_state) > 2


@pytest.mark.fluent_version(">=23.1")
@pytest.mark.skip
def test_meshing_workflow_structure(new_mesh_session):
    """
    o Workflow
    |
    |--o Import Geometry
    |
    |--o Add Local Sizing
    |
    |--o Generate the Surface Mesh
    |
    |--o Describe Geometry
    |  |
    |  |--o Enclose Fluid Regions (Capping)
    |  |
    |  |--o Create Regions
    |
    |--o Update Regions
    |
    |--o Add Boundary Layers
    |
    |--o Generate the Volume Mesh
    """
    w = new_mesh_session.workflow
    w.InitializeWorkflow(WorkflowType="Watertight Geometry")

    task_names = (
        "Import Geometry",
        "Add Local Sizing",
        "Generate the Surface Mesh",
        "Describe Geometry",
        "Enclose Fluid Regions (Capping)",
        "Create Regions",
        "Update Regions",
        "Add Boundary Layers",
        "Generate the Volume Mesh",
    )

    (
        import_geom,
        add_sizing,
        gen_surf_mesh,
        describe_geometry,
        cap,
        create_regions,
        update_regions,
        add_boundary_layers,
        gen_vol_mesh,
    ) = all_tasks = [w.task(name) for name in task_names]

    def upstream_names(task):
        return {upstream.name() for upstream in task.get_direct_upstream_tasks()}

    def downstream_names(task):
        return {downstream.name() for downstream in task.get_direct_downstream_tasks()}

    assert upstream_names(import_geom) == set()
    assert downstream_names(import_geom) == {
        "Generate the Surface Mesh",
        "Add Local Sizing",
    }

    assert upstream_names(add_sizing) == {"Import Geometry"}
    assert downstream_names(add_sizing) == {"Generate the Surface Mesh"}

    assert upstream_names(gen_surf_mesh) == {"Import Geometry", "Add Local Sizing"}
    assert downstream_names(gen_surf_mesh) == {
        "Describe Geometry",
        "Add Boundary Layers",
        "Generate the Volume Mesh",
    }

    assert upstream_names(describe_geometry) == {
        "Generate the Surface Mesh",
        "Add Boundary Layers",
    }
    assert downstream_names(describe_geometry) == {
        "Update Regions",
        "Add Boundary Layers",
        "Generate the Volume Mesh",
    }

    assert upstream_names(cap) == {
        "Describe Geometry",
        "Add Boundary Layers",
        "Generate the Surface Mesh",
    }
    assert downstream_names(cap) == {
        "Describe Geometry",
        "Add Boundary Layers",
        "Generate the Volume Mesh",
    }

    assert upstream_names(create_regions) == {
        "Describe Geometry",
        "Add Boundary Layers",
        "Generate the Surface Mesh",
    }
    assert downstream_names(create_regions) == {
        "Describe Geometry",
        "Add Boundary Layers",
        "Generate the Volume Mesh",
        "Update Regions",
    }

    assert upstream_names(update_regions) == {"Describe Geometry"}
    assert downstream_names(update_regions) == {"Generate the Volume Mesh"}

    assert upstream_names(add_boundary_layers) == {
        "Describe Geometry",
        "Generate the Surface Mesh",
    }
    assert downstream_names(add_boundary_layers) == {
        "Describe Geometry",
        "Generate the Volume Mesh",
    }

    assert upstream_names(gen_vol_mesh) == {
        "Update Regions",
        "Describe Geometry",
        "Add Boundary Layers",
        "Generate the Surface Mesh",
    }
    assert downstream_names(gen_vol_mesh) == set()

    for task in all_tasks:
        assert {sub_task.name() for sub_task in task.ordered_children()} == (
            {
                "Enclose Fluid Regions (Capping)",
                "Create Regions",
            }
            if task is describe_geometry
            else set()
        )

    for task in all_tasks:
        assert {sub_task.name() for sub_task in task.inactive_ordered_children()} == (
            {
                "Apply Share Topology",
                "Update Boundaries",
            }
            if task is describe_geometry
            else set()
        )

    task_ids = [task.get_id() for task in all_tasks]
    # uniqueness test
    assert len(set(task_ids)) == len(task_ids)
    # ordering test
    idxs = [int(id[len("TaskObject") :]) for id in task_ids]
    assert sorted(idxs) == idxs
    """Given the workflow::

            Workflow
            ├── Import Geometry
            ├── Add Local Sizing
            ├── Generate the Surface Mesh ── Insert Next Task
                                            ├── Add Boundary Type
                                            ├── Update Boundaries
                                            ├── ...
    """
    assert set(gen_surf_mesh.GetNextPossibleTasks()) == {
        "AddBoundaryType",
        "UpdateBoundaries",
        "SetUpPeriodicBoundaries",
        "LinearMeshPattern",
        "ManageZones",
        "ModifyMeshRefinement",
        "ImproveSurfaceMesh",
        "RunCustomJournal",
    }

    children = w.ordered_children()
    expected_task_order = (
        "Import Geometry",
        "Add Local Sizing",
        "Generate the Surface Mesh",
        "Describe Geometry",
        "Update Regions",
        "Add Boundary Layers",
        "Generate the Volume Mesh",
    )

    actual_task_order = tuple(child.name() for child in children)

    assert actual_task_order == expected_task_order

    assert [child.name() for child in children[3].ordered_children()] == [
        "Enclose Fluid Regions (Capping)",
        "Create Regions",
    ]

    gen_surf_mesh.InsertNextTask(CommandName="AddBoundaryType")

    children = w.ordered_children()
    expected_task_order = (
        "Import Geometry",
        "Add Local Sizing",
        "Generate the Surface Mesh",
        "Add Boundary Type",
        "Describe Geometry",
        "Update Regions",
        "Add Boundary Layers",
        "Generate the Volume Mesh",
    )

    actual_task_order = tuple(child.name() for child in children)

    assert actual_task_order == expected_task_order

    assert [child.name() for child in children[4].ordered_children()] == [
        "Enclose Fluid Regions (Capping)",
        "Create Regions",
    ]


@pytest.mark.skip("Randomly failing in CI")
@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=23.2")
def test_attrs_in_watertight_meshing_workflow(new_mesh_session):
    # Import geometry
    import_file_name = examples.download_file(
        "mixing_elbow.pmdb", "pyfluent/mixing_elbow"
    )
    watertight = new_mesh_session.watertight()
    unwanted_attrs = {"fault_tolerant", "part_management", "pm_file_management"}
    assert set(dir(watertight)) - unwanted_attrs == set(dir(watertight))

    for attr in unwanted_attrs:
        with pytest.raises(AttributeError):
            getattr(watertight, attr)

    watertight.import_geometry.file_name.set_state(import_file_name)
    watertight.import_geometry.length_unit = "in"
    watertight.import_geometry()

    assert watertight.import_geometry.file_name()
    # Reinitialize the workflow:
    watertight.reinitialize()

    assert not watertight.import_geometry.file_name()


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=23.2")
def test_ordered_children_in_enhanced_meshing_workflow(new_mesh_session):
    watertight = new_mesh_session.watertight()
    assert set([repr(x) for x in watertight.ordered_children()]) == {
        "<Task 'Add Boundary Layers'>",
        "<Task 'Add Local Sizing'>",
        "<Task 'Apply Share Topology'>",
        "<Task 'Create Regions'>",
        "<Task 'Describe Geometry'>",
        "<Task 'Enclose Fluid Regions (Capping)'>",
        "<Task 'Generate the Surface Mesh'>",
        "<Task 'Generate the Volume Mesh'>",
        "<Task 'Import Geometry'>",
        "<Task 'Update Boundaries'>",
        "<Task 'Update Regions'>",
    }


@pytest.mark.skip("Randomly failing in CI")
@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=23.2")
def test_attrs_in_fault_tolerant_meshing_workflow(new_mesh_session):
    # Import CAD
    import_file_name = examples.download_file(
        "exhaust_system.fmd", "pyfluent/exhaust_system"
    )

    fault_tolerant = new_mesh_session.fault_tolerant()
    assert "watertight" not in dir(fault_tolerant)

    with pytest.raises(AttributeError):
        fault_tolerant.watertight()

    fault_tolerant.import_cad_and_part_management.context.set_state(0)
    fault_tolerant.import_cad_and_part_management.create_object_per.set_state("Custom")
    fault_tolerant.import_cad_and_part_management.fmd_file_name.set_state(
        import_file_name
    )

    assert fault_tolerant.import_cad_and_part_management.fmd_file_name()
    # Reinitialize the workflow:
    fault_tolerant.reinitialize()

    assert not fault_tolerant.import_cad_and_part_management.fmd_file_name()


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=23.2")
def test_switch_between_workflows(new_mesh_session):
    meshing = new_mesh_session

    # Initialize to watertight and store
    watertight = meshing.watertight()

    assert watertight.import_geometry.arguments()

    # Wrong Attribute
    with pytest.raises(AttributeError):
        watertight.import_cad_and_part_management.arguments()

    # Initialize to fault-tolerant and store
    fault_tolerant = meshing.fault_tolerant()

    assert fault_tolerant.import_cad_and_part_management.arguments()

    # 'import_geometry' is a watertight workflow command which is not available now
    # since we have changed to fault-tolerant in the backend.
    with pytest.raises(RuntimeError):
        watertight.import_geometry.arguments()

    # Re-initialize watertight
    watertight.reinitialize()

    # 'import_cad_and_part_management' is a fault-tolerant workflow command which is not
    # available now since we have changed to watertight in the backend.
    with pytest.raises(RuntimeError):
        fault_tolerant.import_cad_and_part_management.arguments()

    assert watertight.import_geometry.arguments()

    meshing.workflow.InitializeWorkflow(WorkflowType="Fault-tolerant Meshing")

    # 'import_geometry' is a watertight workflow command which is not available now
    # since we have changed to fault-tolerant in the backend.
    with pytest.raises(RuntimeError):
        watertight.import_geometry.arguments()

    meshing.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")

    # 'import_cad_and_part_management' is a fault-tolerant workflow command which is not
    # available now since we have changed to watertight in the backend.
    with pytest.raises(RuntimeError):
        fault_tolerant.import_cad_and_part_management.arguments()

    # Re-initialize fault-tolerant
    fault_tolerant.reinitialize()
    assert fault_tolerant.import_cad_and_part_management.arguments()


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=24.1")
def test_new_meshing_workflow_without_dm_caching(
    disable_datamodel_cache, new_mesh_session
):
    import_file_name = examples.download_file(
        "mixing_elbow.pmdb", "pyfluent/mixing_elbow"
    )

    watertight = new_mesh_session.watertight()
    watertight.import_geometry.file_name = import_file_name
    watertight.import_geometry.length_unit.set_state("in")
    watertight.import_geometry()

    watertight.add_local_sizing.add_child_to_task()
    watertight.add_local_sizing()

    watertight.create_volume_mesh()

    watertight.import_geometry.rename(new_name="import_geom_wtm")
    assert watertight.task("import_geom_wtm").arguments()

    watertight.delete_tasks(list_of_tasks=["add_local_sizing"])
    with pytest.raises(AttributeError):
        watertight.add_local_sizing
    watertight.insert_new_task(command_name="add_local_sizing")
    time.sleep(2.5)
    assert watertight.add_local_sizing

    fault_tolerant = new_mesh_session.fault_tolerant()
    with pytest.raises(RuntimeError):
        watertight.import_geometry.arguments()
    assert fault_tolerant.import_cad_and_part_management.arguments()

    watertight.reinitialize()
    with pytest.raises(RuntimeError):
        fault_tolerant.import_cad_and_part_management.arguments()
    assert watertight.import_geometry.arguments()
