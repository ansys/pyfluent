from functools import partial

import pytest
from util.meshing_workflow import (  # noqa: F401; model_object_throws_on_invalid_arg,
    assign_task_arguments,
    execute_task_with_pre_and_postcondition_checks,
    exhaust_system_geometry,
    mixing_elbow_geometry,
    new_mesh_session,
    shared_watertight_workflow,
    shared_watertight_workflow_session,
)

from ansys.fluent.core.meshing.faulttolerant import fault_tolerant_workflow
from ansys.fluent.core.meshing.watertight import watertight_workflow


@pytest.mark.nightly
@pytest.mark.codegen_required
def test_mixing_elbow_meshing_workflow(
    shared_watertight_workflow_session,
    mixing_elbow_geometry,
):
    """This test covers generic meshing workflow behaviour."""
    meshing_session = shared_watertight_workflow_session
    workflow = meshing_session.workflow

    ###############################################################################

    assign_task_args = partial(
        assign_task_arguments, workflow=workflow, check_state=True
    )

    execute_task_with_pre_and_postconditions = partial(
        execute_task_with_pre_and_postcondition_checks,
        workflow=workflow,
    )

    ###############################################################################
    # Import the CAD geometry
    # Query the task state before and after task execution
    assign_task_args(
        task_name="Import Geometry", FileName=mixing_elbow_geometry, LengthUnit="in"
    )

    execute_task_with_pre_and_postconditions(task_name="Import Geometry")

    ###############################################################################
    # Add local sizing
    # Query the task state before and after task execution
    workflow.TaskObject["Add Local Sizing"].AddChildToTask()

    execute_task_with_pre_and_postconditions(task_name="Add Local Sizing")

    ###############################################################################
    # Generate the surface mesh
    # Query the task state before and after task execution
    assign_task_args(
        task_name="Generate the Surface Mesh", CFDSurfaceMeshControls={"MaxSize": 0.3}
    )

    execute_task_with_pre_and_postconditions(task_name="Generate the Surface Mesh")

    ###############################################################################
    # Describe the geometry
    # Query the task state before and after task execution
    workflow.TaskObject["Describe Geometry"].UpdateChildTasks(SetupTypeChanged=False)
    assign_task_args(
        task_name="Describe Geometry",
        SetupType="The geometry consists of only fluid regions with no voids",
    )
    workflow.TaskObject["Describe Geometry"].UpdateChildTasks(SetupTypeChanged=True)

    execute_task_with_pre_and_postconditions(task_name="Describe Geometry")

    ###############################################################################
    # Update Boundaries Task
    # Query the task state before and after task execution
    assign_task_args(
        task_name="Update Boundaries",
        BoundaryLabelList=["wall-inlet"],
        BoundaryLabelTypeList=["wall"],
        OldBoundaryLabelList=["wall-inlet"],
        OldBoundaryLabelTypeList=["velocity-inlet"],
    )

    execute_task_with_pre_and_postconditions(task_name="Update Boundaries")

    ###############################################################################
    # Update your regions
    # Query the task state before and after task execution

    execute_task_with_pre_and_postconditions(task_name="Update Regions")

    ###############################################################################
    # Add Boundary Layers
    # Query the task state before and after task execution
    workflow.TaskObject["Add Boundary Layers"].AddChildToTask()
    workflow.TaskObject["Add Boundary Layers"].InsertCompoundChildTask()
    assign_task_args(
        task_name="smooth-transition_1", BLControlName="smooth-transition_1"
    )
    workflow.TaskObject["Add Boundary Layers"].Arguments = {}

    execute_task_with_pre_and_postconditions(task_name="Add Boundary Layers")

    ###############################################################################
    # Generate the volume mesh
    # Query the task state before and after task execution
    assign_task_args(
        task_name="Generate the Volume Mesh",
        VolumeFill="poly-hexcore",
        VolumeFillControls={"HexMaxCellLength": 0.3},
    )

    execute_task_with_pre_and_postconditions(task_name="Generate the Volume Mesh")

    ###############################################################################
    # Check the mesh in Meshing mode
    # TODO: Remove the if condition after a stable version of 23.1 is available and update the commands as required.
    if float(meshing_session.get_fluent_version()[:-2]) < 23.0:
        meshing_session.tui.mesh.check_mesh()


@pytest.mark.codegen_required
def test_meshing_workflow_raises_exception_on_invalid_task_name(
    shared_watertight_workflow,
):
    try:
        shared_watertight_workflow.TaskObject["no such task"]
    except Exception:
        pass
    else:
        assert False


"""
Cannot enable this test because meshing workflow makes invalid queries as
soon as the meshing application is started:

Error: workflow/cx-create-workflow-tree:Invalid query for child TaskType from parent /Workflow
Error Object: ()


def test_meshing_workflow_raises_exception_on_invalid_key_in_task_args(
    model_object_throws_on_invalid_arg,
    shared_watertight_workflow,
    mixing_elbow_geometry
):
    # task_names = ("Import Geometry", "Add Local Sizing")
    task_names = ("Add Local Sizing",)
    for task_name in task_names:
        task = shared_watertight_workflow.TaskObject[task_name]
        try:
            task.Arguments = {"no such arg": 42}
        except Exception:
            pass
        else:
            assert False

def test_meshing_workflow_raises_exception_on_invalid_key_in_task_args_2(
    model_object_throws_on_invalid_arg,
    shared_watertight_workflow,
    mixing_elbow_geometry
):
    workflow = shared_watertight_workflow
    assign_task_args = partial(
        assign_task_arguments, workflow=workflow, check_state=False
    )

    assign_task_args(
        task_name="Import Geometry", FileName=mixing_elbow_geometry, LengthUnit="in"
    )

    workflow.TaskObject["Import Geometry"].Execute()

    try:
        assign_task_args(
            task_name="Add Local Sizing", XXX=42
        )
    except:
        pass
    else:
        assert False
"""


@pytest.mark.fluent_version(">=23.1")
@pytest.mark.codegen_required
def test_command_args_datamodel_se(new_mesh_session):
    session_new = new_mesh_session
    w = session_new.workflow
    w.InitializeWorkflow(WorkflowType="Watertight Geometry")
    igt = w.task("Import Geometry")
    assert igt.arguments.CadImportOptions()
    assert igt.arguments.CadImportOptions.OneZonePer()
    assert igt.arguments.CadImportOptions.OneZonePer.getAttribValue("default")


@pytest.mark.fluent_version(">=23.1")
@pytest.mark.codegen_required
def test_command_args_including_task_object_datamodel_se(new_mesh_session):
    session_new = new_mesh_session
    w = session_new.workflow
    w.InitializeWorkflow(WorkflowType="Watertight Geometry")
    igt = w.TaskObject["Import Geometry"]
    assert igt.Arguments() == {}
    assert igt.arguments.CadImportOptions()
    assert igt.arguments.CadImportOptions.OneZonePer()
    assert igt.arguments.CadImportOptions.OneZonePer.getAttribValue("default")


@pytest.mark.fluent_version(">=23.1")
@pytest.mark.codegen_required
def test_attribute_query_list_types(new_mesh_session):
    session_new = new_mesh_session
    w = session_new.workflow
    w.InitializeWorkflow(WorkflowType="Watertight Geometry")
    igt = w.TaskObject["Import Geometry"]
    assert ["CAD", "Mesh"] == igt.arguments.FileFormat.getAttribValue("allowedValues")


@pytest.mark.fluent_version(">=23.1")
@pytest.mark.codegen_required
def test_accessors_for_argument_sub_items(new_mesh_session):
    session_new = new_mesh_session

    w = session_new.workflow

    w.InitializeWorkflow(WorkflowType="Watertight Geometry")

    assert w.task("Import Geometry").arguments.LengthUnit.default_value() == "mm"
    assert w.task("Import Geometry").arguments.MeshUnit.is_read_only()
    assert w.task("Import Geometry").arguments.LengthUnit.is_active()
    assert w.task("Import Geometry").arguments.FileName.is_read_only()
    assert w.task(
        "Import Geometry"
    ).arguments.CadImportOptions.OneZonePer.is_read_only()
    assert (
        w.task(
            "Generate the Volume Mesh"
        ).arguments.VolumeFillControls.Type.default_value()
        == "Cartesian"
    )

    # Test particular to string type (allowed_values() only available in string types)
    assert w.task(
        "Generate the Volume Mesh"
    ).arguments.VolumeFillControls.Type.allowed_values() == [
        "Octree",
        "Cartesian",
    ]
    assert (
        w.task(
            "Import Geometry"
        ).arguments.CadImportOptions.FeatureAngle.default_value()
        == 40.0
    )

    # Test particular to numerical type (min() only available in numerical types)
    assert (
        w.task("Import Geometry").arguments.CadImportOptions.FeatureAngle.min() == 0.0
    )

    # Test intended to fail in numerical type (allowed_values() only available in string types)
    with pytest.raises(AttributeError) as msg:
        assert w.task(
            "Import Geometry"
        ).arguments.CadImportOptions.FeatureAngle.allowed_values()
    assert (
        msg.value.args[0]
        == "'PyNumericalCommandArgumentsSubItem' object has no attribute 'allowed_values'"
    )

    # Test intended to fail in numerical type (allowed_values() only available in string types)
    with pytest.raises(AttributeError) as msg:
        assert w.task("Import Geometry").arguments.NumParts.allowed_values()
    assert (
        msg.value.args[0]
        == "'PyNumericalCommandArgumentsSubItem' object has no attribute 'allowed_values'"
    )

    # Test intended to fail in string type (min() only available in numerical types)
    with pytest.raises(AttributeError) as msg:
        assert w.task("Import Geometry").arguments.LengthUnit.min()
    assert (
        msg.value.args[0]
        == "'PyTextualCommandArgumentsSubItem' object has no attribute 'min'"
    )


@pytest.mark.fluent_version(">=23.1")
@pytest.mark.codegen_required
def test_read_only_behaviour_of_command_arguments(new_mesh_session):
    session_new = new_mesh_session
    w = session_new.workflow
    m = session_new.meshing
    w.InitializeWorkflow(WorkflowType="Watertight Geometry")

    with pytest.raises(AttributeError) as msg:
        w.task("Import Geometry").arguments.MeshUnit.set_state("in")
    assert msg.value.args[0] == "Command Arguments are read-only."

    with pytest.raises(AttributeError) as msg:
        w.task("Import Geometry").arguments.CadImportOptions.OneZonePer.set_state(None)
    assert msg.value.args[0] == "Command Arguments are read-only."

    assert "set_state" in dir(m.ImportGeometry.create_instance())
    assert "set_state" in dir(m.ImportGeometry.create_instance().NumParts)


@pytest.mark.fluent_version(">=23.1")
@pytest.mark.codegen_required
def test_sample_use_of_command_arguments(new_mesh_session):
    w = new_mesh_session.workflow

    w.InitializeWorkflow(WorkflowType="Watertight Geometry")

    assert w.task("Import Geometry").arguments.LengthUnit.allowed_values() == [
        "m",
        "cm",
        "mm",
        "in",
        "ft",
        "um",
        "nm",
    ]
    assert w.task("Import Geometry").arguments.LengthUnit.default_value() == "mm"
    w.TaskObject["Import Geometry"].Arguments = dict(LengthUnit="in")
    assert w.task("Import Geometry").arguments.LengthUnit() == "in"


@pytest.mark.codegen_required
def test_dummy_journal_data_model_methods(new_mesh_session):
    session_new = new_mesh_session

    w = session_new.workflow

    w.InitializeWorkflow(WorkflowType="Watertight Geometry")

    with pytest.raises(AttributeError) as msg:
        w.task("Import Geometry").delete_child()
    assert msg.value.args[0] == "This method is yet to be implemented in pyfluent."
    with pytest.raises(AttributeError) as msg:
        w.task("Import Geometry").delete_child_objects()
    assert msg.value.args[0] == "This method is yet to be implemented in pyfluent."
    with pytest.raises(AttributeError) as msg:
        w.task("Import Geometry").delete_all_child_objects()
    assert msg.value.args[0] == "This method is yet to be implemented in pyfluent."
    with pytest.raises(AttributeError) as msg:
        w.task("Import Geometry").fix_state()
    assert msg.value.args[0] == "This method is yet to be implemented in pyfluent."


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
    """
    o Workflow
    |
    |--o Import Geometry
    |
    |--o Add Local Sizing
    |
    |--o Generate the Surface Mesh --
                                     /Insert Next Task>
                                                        |-- Add Boundary Type
                                                        |-- Update Boundaries
                                                        |-- ...
    """
    assert set(gen_surf_mesh.GetNextPossibleTasks()) == {
        "AddBoundaryType",
        "UpdateBoundaries",
        "SetUpPeriodicBoundaries",
        "LinearMeshPattern",
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


@pytest.mark.fluent_version(">=23.2")
@pytest.mark.codegen_required
def test_extended_wrapper(new_mesh_session, mixing_elbow_geometry):
    watertight = new_mesh_session.watertight()
    import_geometry = watertight.import_geometry
    assert import_geometry.Arguments() == {}
    import_geometry.Arguments = dict(FileName=mixing_elbow_geometry)
    assert 8 < len(import_geometry.arguments.get_state()) < 15
    assert len(import_geometry.arguments.get_state(explicit_only=True)) == 1
    import_geometry.arguments.set_state(dict(FileName=None))
    assert import_geometry.arguments.get_state(explicit_only=True) == dict(
        FileName=None
    )
    assert import_geometry.arguments.get_state()["FileName"] is None
    import_geometry.arguments.set_state(dict(FileName=mixing_elbow_geometry))
    assert import_geometry.arguments.get_state(explicit_only=True) == dict(
        FileName=mixing_elbow_geometry
    )
    assert import_geometry.FileName() == mixing_elbow_geometry
    import_geometry.FileName.set_state("bob")
    assert import_geometry.FileName() == "bob"
    import_geometry.FileName.set_state(mixing_elbow_geometry)
    import_geometry.Execute()
    add_local_sizing = watertight.add_local_sizing
    assert not add_local_sizing.ordered_children()
    add_local_sizing.add_child(state={"BOIFaceLabelList": ["cold-inlet"]})
    assert not add_local_sizing.ordered_children()

    added_sizing = add_local_sizing.add_child_and_update(
        state={"BOIFaceLabelList": ["elbow-fluid"]}
    )
    assert len(add_local_sizing.ordered_children()) == 1
    assert added_sizing
    assert added_sizing.arguments.BOIFaceLabelList() == ["elbow-fluid"]
    # restart
    watertight = new_mesh_session.watertight()
    assert watertight.import_geometry.State() == "Out-of-date"
    watertight.import_geometry(FileName=mixing_elbow_geometry, AppendMesh=False)
    assert watertight.import_geometry.State() == "Up-to-date"
    import_geometry_state = watertight.import_geometry.arguments()
    assert len(import_geometry_state) > 2


@pytest.mark.codegen_required
def test_iterate_meshing_workflow_task_container(new_mesh_session):
    workflow = new_mesh_session.workflow
    workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
    tasks = [task for task in workflow.TaskObject]
    assert len(tasks) == 11
    assert tasks[0].name() == "Import Geometry"


@pytest.mark.fluent_version(">=23.2")
@pytest.mark.codegen_required
def test_watertight_workflow(mixing_elbow_geometry, new_mesh_session):
    watertight = watertight_workflow(
        geometry_filepath=mixing_elbow_geometry, session=new_mesh_session
    )
    add_local_sizing = watertight.add_local_sizing
    assert not add_local_sizing.ordered_children()
    add_local_sizing.add_child(state={"BOIFaceLabelList": ["cold-inlet"]})
    assert not add_local_sizing.ordered_children()
    added_sizing = add_local_sizing.add_child_and_update(
        state={"BOIFaceLabelList": ["elbow-fluid"]}
    )
    assert len(add_local_sizing.ordered_children()) == 1
    assert added_sizing
    assert added_sizing.arguments.BOIFaceLabelList() == ["elbow-fluid"]


@pytest.mark.fluent_version(">=23.2")
@pytest.mark.codegen_required
def test_watertight_workflow_children(mixing_elbow_geometry, new_mesh_session):
    watertight = watertight_workflow(
        geometry_filepath=mixing_elbow_geometry, session=new_mesh_session
    )
    add_local_sizing = watertight.add_local_sizing
    assert not add_local_sizing.ordered_children()
    add_local_sizing.add_child(state={"BOIFaceLabelList": ["cold-inlet"]})
    assert not add_local_sizing.ordered_children()
    added_sizing = add_local_sizing.add_child_and_update(
        state={"BOIFaceLabelList": ["elbow-fluid"]}
    )
    assert len(add_local_sizing.ordered_children()) == 1
    assert added_sizing
    assert added_sizing.arguments.BOIFaceLabelList() == ["elbow-fluid"]
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


@pytest.mark.fluent_version(">=23.2")
@pytest.mark.codegen_required
def test_watertight_workflow_dynamic_interface(mixing_elbow_geometry, new_mesh_session):
    watertight = watertight_workflow(
        geometry_filepath=mixing_elbow_geometry, session=new_mesh_session
    )
    create_volume_mesh = watertight.create_volume_mesh
    assert create_volume_mesh is not None
    watertight.DeleteTasks(ListOfTasks=["Generate the Volume Mesh"])
    # I assume that what's going on here is that due to DeleteTasks we are triggering
    # change events in the server but those events are (still) being transmitted after
    # DeleteTasks has returned. Hence, the dynamic watertight Python interface
    # is still updating after the command has returned and the client can try to access
    # while it is in that update phase, leading to (difficult to understand) exceptions.
    # Temporarily sleeping in the test. I note that the core event tests use sleeps also.
    create_volume_mesh = watertight.create_volume_mesh
    assert create_volume_mesh is None
    watertight.InsertNewTask(CommandName="GenerateTheVolumeMeshWTM")
    create_volume_mesh = watertight.create_volume_mesh
    assert create_volume_mesh is not None
    assert (
        watertight.describe_geometry.create_regions.arguments()["NumberOfFlowVolumes"]
        == 1
    )
    watertight.DeleteTasks(ListOfTasks=["Create Regions"])
    assert watertight.describe_geometry.create_regions is None
    assert watertight.describe_geometry.enclose_fluid_regions
    watertight.describe_geometry.enclose_fluid_regions.delete()
    assert watertight.describe_geometry.enclose_fluid_regions is None
    watertight.create_volume_mesh.delete()
    assert watertight.create_volume_mesh is None


@pytest.mark.fluent_version("==23.2")
@pytest.mark.codegen_required
def test_fault_tolerant_workflow(exhaust_system_geometry, new_mesh_session):
    fault_tolerant = fault_tolerant_workflow(session=new_mesh_session)
    part_management = fault_tolerant.part_management
    filename = exhaust_system_geometry
    part_management.LoadFmdFile(FilePath=filename)
    part_management.MoveCADComponentsToNewObject(
        Paths=[r"/Bottom,1", r"/Left,1", r"/Others,1", r"/Right,1", r"/Top,1"]
    )
    part_management.Node["Object"].Rename(NewName=r"Engine")
    fault_tolerant.TaskObject["Import CAD and Part Management"].Arguments.setState(
        {
            r"CreateObjectPer": r"Custom",
            r"FMDFileName": filename,
            r"FileLoaded": r"yes",
            r"ObjectSetting": r"DefaultObjectSetting",
        }
    )
    fault_tolerant.TaskObject["Import CAD and Part Management"].Execute()
