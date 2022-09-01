from functools import partial
import os

import pytest
from util.meshing_workflow import (  # noqa: F401; model_object_throws_on_invalid_arg,
    assign_task_arguments,
    execute_task_with_pre_and_postcondition_checks,
    mixing_elbow_geometry,
    new_mesh_session,
    shared_mesh_session,
    shared_watertight_workflow,
    shared_watertight_workflow_session,
)

import ansys.fluent.core as pyfluent


@pytest.mark.nightly
def test_mixing_elbow_meshing_workflow(
    shared_watertight_workflow_session,
    mixing_elbow_geometry,
):
    """
    This test covers generic meshing workflow behaviour
    """
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


@pytest.mark.dev
@pytest.mark.fluent_231
def test_command_args_datamodel_se(new_mesh_session):
    session_new = new_mesh_session
    w = session_new.workflow
    w.InitializeWorkflow(WorkflowType="Watertight Geometry")
    igt = w.task("Import Geometry")
    assert igt.CommandArguments.CadImportOptions()
    assert igt.CommandArguments.CadImportOptions.OneZonePer()
    assert igt.CommandArguments.CadImportOptions.OneZonePer.getAttribValue("default")


@pytest.mark.dev
@pytest.mark.fluent_231
def test_command_args_including_task_object_datamodel_se(new_mesh_session):
    session_new = new_mesh_session
    w = session_new.workflow
    w.InitializeWorkflow(WorkflowType="Watertight Geometry")
    igt = w.TaskObject["Import Geometry"]
    assert igt.Arguments() == {}
    assert igt.CommandArguments.CadImportOptions()
    assert igt.CommandArguments.CadImportOptions.OneZonePer()
    assert igt.CommandArguments.CadImportOptions.OneZonePer.getAttribValue("default")


@pytest.mark.dev
@pytest.mark.fluent_231
def test_meshing_object_commands(new_mesh_session, tmp_path=pyfluent.EXAMPLES_PATH):
    session_new = new_mesh_session
    file_path = os.path.join(tmp_path, "sample_py_journal.txt")
    m = session_new.meshing
    m.execute_tui("(api-setup-python-console)")
    m.execute_tui(f'(api-start-python-journal "{file_path}")')
    m.switch_to_solver()
    m.execute_tui(f"(api-stop-python-journal)")

    with open(file_path) as f:
        returned = f.readlines()

    if os.path.exists(file_path):
        os.remove(file_path)

    assert returned


@pytest.mark.dev
@pytest.mark.fluent_231
def test_attribute_query_list_types(new_mesh_session):
    session_new = new_mesh_session
    w = session_new.workflow
    w.InitializeWorkflow(WorkflowType="Watertight Geometry")
    igt = w.TaskObject["Import Geometry"]
    assert ["CAD", "Mesh"] == igt.CommandArguments.FileFormat.getAttribValue(
        "allowedValues"
    )
