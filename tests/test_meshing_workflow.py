""".. _ref_mixing_elbow_tui_api:

Fluid Flow and Heat Transfer in a Mixing Elbow
---------------------------------------------------
This test covers generic meshing workflow behaviour
"""

from functools import partial

from util.meshing_workflow import (  # noqa: F401; model_object_throws_on_invalid_arg,
    assign_task_arguments,
    execute_task_with_pre_and_postcondition_checks,
    mixing_elbow_geometry,
    shared_mesh_session,
    shared_watertight_workflow,
    shared_watertight_workflow_session,
)


def test_mixing_elbow_meshing_workflow(
    shared_watertight_workflow_session,
    mixing_elbow_geometry,
):

    session = shared_watertight_workflow_session
    workflow = session.meshing.workflow

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
    session.meshing.tui.mesh.check_mesh()


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
