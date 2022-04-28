""".. _ref_mixing_elbow_tui_api:

Fluid Flow and Heat Transfer in a Mixing Elbow
----------------------------------------------
This test covers generic meshing workflow behaviour
"""

from functools import partial

from util.meshing_workflow import (  # noqa: F401
    assign_task_arguments,
    execute_task_with_pre_and_postcondition_checks,
    mesh_session,
    watertight_workflow,
    watertight_workflow_session,
)

from ansys.fluent.core.examples import download_file


def test_mixing_elbow_meshing_workflow(
    watertight_workflow_session, watertight_workflow
):

    workflow = watertight_workflow

    import_filename = download_file(
        filename="mixing_elbow.pmdb", directory="pyfluent/mixing_elbow"
    )

    ###############################################################################

    assign_task_args = partial(
        assign_task_arguments, workflow=workflow, check_state=True
    )

    execute_task_with_pre_and_postconditions = partial(
        execute_task_with_pre_and_postcondition_checks, workflow=watertight_workflow
    )

    ###############################################################################
    # Select the Watertight Geometry Meshing Workflow
    workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")

    ###############################################################################
    # Import the CAD geometry
    # Query the task state before and after task execution
    assign_task_args(
        task_name="Import Geometry", FileName=import_filename, LengthUnit="in"
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
    watertight_workflow_session.tui.meshing.mesh.check_mesh()


def test_meshing_workflow_raises_exception_on_invalid_task_name(watertight_workflow):

    try:
        watertight_workflow.TaskObject["no such task"]
    except Exception:
        pass
    else:
        assert False


def test_meshing_workflow_raises_exception_on_invalid_parameter_name_in_task(
    watertight_workflow,
):

    try:
        watertight_workflow.TaskObject["no such task"]
    except Exception:
        pass
    else:
        assert False
