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
from ansys.fluent.core.utils.fluent_version import FluentVersion


@pytest.mark.fluent_version(">=23.1")
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
    describe_geo = workflow.TaskObject["Describe Geometry"]
    describe_geo.UpdateChildTasks(SetupTypeChanged=False)
    assign_task_args(
        task_name="Describe Geometry",
        SetupType="The geometry consists of only fluid regions with no voids",
    )
    describe_geo.UpdateChildTasks(SetupTypeChanged=True)

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
    add_boundary_layer = workflow.TaskObject["Add Boundary Layers"]
    add_boundary_layer.AddChildToTask()
    add_boundary_layer.InsertCompoundChildTask()
    assign_task_args(
        task_name="smooth-transition_1", BLControlName="smooth-transition_1"
    )
    add_boundary_layer.Arguments = {}

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
    if meshing_session.get_fluent_version() < FluentVersion.v231:
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
    igt = w.TaskObject["Import Geometry"]
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


@pytest.mark.fluent_version(">=23.2")
@pytest.mark.codegen_required
def test_accessors_for_argument_sub_items(new_mesh_session):
    session_new = new_mesh_session

    w = session_new.workflow

    w.InitializeWorkflow(WorkflowType="Watertight Geometry")
    import_geom = w.TaskObject["Import Geometry"]
    assert import_geom.arguments.LengthUnit.default_value() == "mm"
    assert import_geom.arguments.LengthUnit.allowed_values() == [
        "m",
        "cm",
        "mm",
        "in",
        "ft",
        "um",
        "nm",
    ]
    assert import_geom.arguments.LengthUnit() == "mm"
    import_geom.arguments.LengthUnit.set_state("cm")
    assert import_geom.arguments.LengthUnit.get_state() == "cm"
    import_geom.arguments.LengthUnit = "in"
    assert import_geom.arguments.LengthUnit() == "in"

    assert not import_geom.arguments.MeshUnit.is_read_only()
    assert import_geom.arguments.LengthUnit.is_active()
    assert not import_geom.arguments.FileName.is_read_only()
    assert not import_geom.arguments.FileName()
    import_geom.arguments.FileName = "xyz.txt"
    assert import_geom.arguments.FileName() == "xyz.txt"
    with pytest.raises(AttributeError) as msg:
        import_geom.arguments.File = "sample.txt"
    assert msg.value.args[0] == "No attribute named 'File' in 'Import Geometry'."
    assert not import_geom.arguments.CadImportOptions.OneZonePer.is_read_only()

    assert import_geom.arguments.CadImportOptions.OneZonePer() == "body"
    import_geom.arguments.CadImportOptions.OneZonePer.set_state("face")
    assert import_geom.arguments.CadImportOptions.OneZonePer() == "face"

    volume_mesh_gen = w.TaskObject["Generate the Volume Mesh"]
    assert (
        volume_mesh_gen.arguments.VolumeFillControls.Type.default_value() == "Cartesian"
    )

    # Test particular to string type (allowed_values() only available in string types)
    assert volume_mesh_gen.arguments.VolumeFillControls.Type.allowed_values() == [
        "Octree",
        "Cartesian",
    ]
    feat_angle = import_geom.arguments.CadImportOptions.FeatureAngle
    assert feat_angle.default_value() == 40.0

    # Test particular to numerical type (min() only available in numerical types)
    assert feat_angle.min() == 0.0

    # Test intended to fail in numerical type (allowed_values() only available in string types)
    with pytest.raises(AttributeError) as msg:
        assert feat_angle.allowed_values()
    assert (
        msg.value.args[0]
        == "'PyNumericalCommandArgumentsSubItem' object has no attribute 'allowed_values'"
    )

    # Test intended to fail in numerical type (allowed_values() only available in string types)
    with pytest.raises(AttributeError) as msg:
        assert import_geom.arguments.NumParts.allowed_values()
    assert (
        msg.value.args[0]
        == "'PyNumericalCommandArgumentsSubItem' object has no attribute 'allowed_values'"
    )

    # Test intended to fail in string type (min() only available in numerical types)
    with pytest.raises(AttributeError) as msg:
        assert import_geom.arguments.LengthUnit.min()
    assert (
        msg.value.args[0]
        == "'PyTextualCommandArgumentsSubItem' object has no attribute 'min'"
    )


@pytest.mark.skip("Wait for later implementation.")
@pytest.mark.fluent_version(">=23.1")
@pytest.mark.codegen_required
def test_read_only_behaviour_of_command_arguments(new_mesh_session):
    session_new = new_mesh_session
    w = session_new.workflow
    m = session_new.meshing.ImportGeometry.create_instance
    w.InitializeWorkflow(WorkflowType="Watertight Geometry")
    import_geom = w.TaskObject["Import Geometry"]

    with pytest.raises(AttributeError) as msg:
        import_geom.arguments.MeshUnit.set_state("in")

    with pytest.raises(AttributeError) as msg:
        import_geom.arguments.CadImportOptions.OneZonePer.set_state(None)

    assert "set_state" in dir(m())
    assert "set_state" in dir(m().NumParts)


@pytest.mark.fluent_version(">=23.1")
@pytest.mark.codegen_required
def test_sample_use_of_command_arguments(new_mesh_session):
    w = new_mesh_session.workflow
    w.InitializeWorkflow(WorkflowType="Watertight Geometry")

    assert w.TaskObject["Import Geometry"].arguments.LengthUnit.allowed_values() == [
        "m",
        "cm",
        "mm",
        "in",
        "ft",
        "um",
        "nm",
    ]
    assert w.TaskObject["Import Geometry"].arguments.LengthUnit.default_value() == "mm"
    w.TaskObject["Import Geometry"].Arguments = dict(LengthUnit="in")
    assert w.TaskObject["Import Geometry"].arguments.LengthUnit() == "in"


@pytest.mark.codegen_required
def test_dummy_journal_data_model_methods(new_mesh_session):
    session_new = new_mesh_session
    w = session_new.workflow
    w.InitializeWorkflow(WorkflowType="Watertight Geometry")
    import_geom = w.TaskObject["Import Geometry"]

    with pytest.raises(AttributeError) as msg:
        import_geom.delete_child()


@pytest.mark.codegen_required
def test_iterate_meshing_workflow_task_container(new_mesh_session):
    workflow = new_mesh_session.workflow
    workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
    tasks = [task for task in workflow.TaskObject]
    assert len(tasks) == 11
    assert tasks[0].name() == "Import Geometry"


@pytest.mark.fluent_version("==23.2")
@pytest.mark.codegen_required
def test_fault_tolerant_workflow(exhaust_system_geometry, new_mesh_session):
    fault_tolerant = fault_tolerant_workflow(session=new_mesh_session)
    part_management = fault_tolerant.part_management
    file_name = exhaust_system_geometry
    part_management.LoadFmdFile(FilePath=file_name)
    part_management.MoveCADComponentsToNewObject(
        Paths=[r"/Bottom,1", r"/Left,1", r"/Others,1", r"/Right,1", r"/Top,1"]
    )
    part_management.Node["Object"].Rename(NewName=r"Engine")
    import_cad = fault_tolerant.task("Import CAD and Part Management")
    import_cad.Arguments.setState(
        {
            r"CreateObjectPer": r"Custom",
            r"FMDFileName": file_name,
            r"FileLoaded": r"yes",
            r"ObjectSetting": r"DefaultObjectSetting",
        }
    )
    import_cad()


@pytest.mark.codegen_required
def test_modified_workflow(new_mesh_session):
    meshing = new_mesh_session
    meshing.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")

    task_object_display_names = {
        "Import Geometry",
        "Add Local Sizing",
        "Generate the Surface Mesh",
        "Describe Geometry",
        "Apply Share Topology",
        "Enclose Fluid Regions (Capping)",
        "Update Boundaries",
        "Create Regions",
        "Update Regions",
        "Add Boundary Layers",
        "Generate the Volume Mesh",
    }

    task_display_names = []
    for task in meshing.workflow.TaskObject:
        task_display_names.append(task.display_name())

    assert set(task_display_names) == task_object_display_names

    task_display_names = []
    for name, _ in meshing.workflow.TaskObject.items():
        task_display_names.append(name)

    assert set(task_display_names) == task_object_display_names


def test_nonexistent_attrs(new_mesh_session):
    meshing = new_mesh_session
    assert not hasattr(meshing.workflow, "xyz")
    with pytest.raises(AttributeError) as msg:
        meshing.workflow.xyz
    assert msg.value.args[0] == "'ClassicMeshingWorkflow' object has no attribute 'xyz'"


@pytest.mark.fluent_version(">=23.2")
def test_old_workflow_structure(new_mesh_session):
    meshing = new_mesh_session
    meshing.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
    assert meshing.workflow.TaskObject["Import Geometry"].arguments()
    with pytest.raises(AttributeError) as msg:
        meshing.workflow.import_geometry
    assert (
        msg.value.args[0]
        == "'ClassicMeshingWorkflow' object has no attribute 'import_geometry'"
    )


@pytest.mark.fluent_version(">=23.2")
def test_new_workflow_structure(new_mesh_session):
    meshing = new_mesh_session
    watertight = meshing.watertight()
    assert watertight.import_geometry.arguments()
    with pytest.raises(AttributeError) as msg:
        watertight.TaskObject["Import Geometry"]
    assert (
        msg.value.args[0]
        == "'WatertightMeshingWorkflow' object has no attribute 'TaskObject'"
    )
