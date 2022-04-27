""".. _ref_mixing_elbow_tui_api:

Fluid Flow and Heat Transfer in a Mixing Elbow
----------------------------------------------
This test covers the setup and solution of a three-dimensional
turbulent fluid flow and heat transfer problem in a mixing elbow. The mixing
elbow configuration is encountered in piping systems in power plants and
processindustries. It is often important to predict the flow field and
temperature field in the area of the mixing regionin order to properly design
the junction.

This test queries the following using PyTest:

- Meshing workflow tasks state before and after the task execution
- Flux report after solution, approximately 0 kg/s
- Temperature on the outlet boundary after solution, approximately 296.2 K
"""

from functools import partial

from pytest import approx

import ansys.fluent.core as pyfluent
from ansys.fluent.core.examples import download_file


def check_task_execute_preconditions(task_state):
    assert task_state() == "Out-of-date"


def check_task_execute_postconditions(task_state):
    assert task_state() == "Up-to-date"


def execute_task_with_pre_and_postcondition_checks(workflow, task_name):
    task = workflow.TaskObject[task_name]
    task_state = task.State
    check_task_execute_preconditions(task_state)
    # Some tasks are wrongly returning False in meshing workflow itself
    # so we add a temporary caveat below
    result = task.Execute()
    if task_name not in ("Add Local Sizing", "Add Boundary Layers"):
        assert result is True
    check_task_execute_postconditions(task_state)


def check_report_definition_result(
    report_definitions, report_definition_name, expected_result
):
    assert (
        report_definitions.compute(report_defs=[report_definition_name])[
            report_definition_name
        ][0]
        == expected_result
    )


def test_mixing_elbow():

    import_filename = download_file(
        filename="mixing_elbow.pmdb", directory="pyfluent/mixing_elbow"
    )

    ###############################################################################
    # Start Fluent
    session = pyfluent.launch_fluent(
        meshing_mode=True, precision="double", processor_count=2
    )

    execute_task_with_pre_and_postconditions = partial(
        execute_task_with_pre_and_postcondition_checks, workflow=session.workflow
    )

    ###############################################################################
    # Select the Watertight Geometry Meshing Workflow
    session.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")

    ###############################################################################
    # Import the CAD geometry
    # Query the task state before and after task execution
    session.workflow.TaskObject["Import Geometry"].Arguments = dict(
        FileName=import_filename, LengthUnit="in"
    )

    execute_task_with_pre_and_postconditions(task_name="Import Geometry")

    ###############################################################################
    # Add local sizing
    # Query the task state before and after task execution
    session.workflow.TaskObject["Add Local Sizing"].AddChildToTask()

    execute_task_with_pre_and_postconditions(task_name="Add Local Sizing")

    ###############################################################################
    # Generate the surface mesh
    # Query the task state before and after task execution
    session.workflow.TaskObject["Generate the Surface Mesh"].Arguments = {
        "CFDSurfaceMeshControls": {"MaxSize": 0.3}
    }

    execute_task_with_pre_and_postconditions(task_name="Generate the Surface Mesh")

    ###############################################################################
    # Describe the geometry
    # Query the task state before and after task execution
    session.workflow.TaskObject["Describe Geometry"].UpdateChildTasks(
        SetupTypeChanged=False
    )
    session.workflow.TaskObject["Describe Geometry"].Arguments = dict(
        SetupType="The geometry consists of only fluid regions with no voids"
    )
    session.workflow.TaskObject["Describe Geometry"].UpdateChildTasks(
        SetupTypeChanged=True
    )

    execute_task_with_pre_and_postconditions(task_name="Describe Geometry")

    ###############################################################################
    # Update Boundaries Task
    # Query the task state before and after task execution
    session.workflow.TaskObject["Update Boundaries"].Arguments = {
        "BoundaryLabelList": ["wall-inlet"],
        "BoundaryLabelTypeList": ["wall"],
        "OldBoundaryLabelList": ["wall-inlet"],
        "OldBoundaryLabelTypeList": ["velocity-inlet"],
    }

    execute_task_with_pre_and_postconditions(task_name="Update Boundaries")

    ###############################################################################
    # Update your regions
    # Query the task state before and after task execution

    execute_task_with_pre_and_postconditions(task_name="Update Regions")

    ###############################################################################
    # Add Boundary Layers
    # Query the task state before and after task execution
    session.workflow.TaskObject["Add Boundary Layers"].AddChildToTask()
    session.workflow.TaskObject["Add Boundary Layers"].InsertCompoundChildTask()
    session.workflow.TaskObject["smooth-transition_1"].Arguments = {
        "BLControlName": "smooth-transition_1",
    }
    session.workflow.TaskObject["Add Boundary Layers"].Arguments = {}

    execute_task_with_pre_and_postconditions(task_name="Add Boundary Layers")

    ###############################################################################
    # Generate the volume mesh
    # Query the task state before and after task execution
    session.workflow.TaskObject["Generate the Volume Mesh"].Arguments = {
        "VolumeFill": "poly-hexcore",
        "VolumeFillControls": {
            "HexMaxCellLength": 0.3,
        },
    }

    execute_task_with_pre_and_postconditions(task_name="Generate the Volume Mesh")

    ###############################################################################
    # Check the mesh in Meshing mode
    session.tui.meshing.mesh.check_mesh()

    ###############################################################################
    # Switch to Solution mode
    session.tui.meshing.switch_to_solution_mode("yes")

    ###############################################################################
    # Check the mesh in Solver mode
    session.tui.solver.mesh.check()

    ###############################################################################
    # Set the working units for the mesh
    session.tui.solver.define.units("length", "in")

    ###############################################################################
    # Enable heat transfer by activating the energy equation.
    session.tui.solver.define.models.energy("yes", ", ", ", ", ", ", ", ")

    ###############################################################################
    # Create a new material called water-liquid.
    session.tui.solver.define.materials.copy("fluid", "water-liquid")

    ###############################################################################
    # Set up the cell zone conditions for the fluid zone (elbow-fluid). Select
    # water-liquid from the Material list.
    session.tui.solver.define.boundary_conditions.fluid(
        "elbow-fluid",
        "yes",
        "water-liquid",
        "no",
        "no",
        "no",
        "no",
        "0",
        "no",
        "0",
        "no",
        "0",
        "no",
        "0",
        "no",
        "0",
        "no",
        "1",
        "no",
        "no",
        "no",
        "no",
        "no",
    )

    ###############################################################################
    # Set up the boundary conditions
    session.tui.solver.define.boundary_conditions.set.velocity_inlet(
        "cold-inlet", [], "vmag", "no", 0.4, "quit"
    )
    session.tui.solver.define.boundary_conditions.set.velocity_inlet(
        "cold-inlet", [], "ke-spec", "no", "no", "no", "yes", "quit"
    )
    session.tui.solver.define.boundary_conditions.set.velocity_inlet(
        "cold-inlet", [], "turb-intensity", 5, "quit"
    )
    session.tui.solver.define.boundary_conditions.set.velocity_inlet(
        "cold-inlet", [], "turb-hydraulic-diam", 4, "quit"
    )
    session.tui.solver.define.boundary_conditions.set.velocity_inlet(
        "cold-inlet", [], "temperature", "no", 293.15, "quit"
    )

    session.tui.solver.define.boundary_conditions.set.velocity_inlet(
        "hot-inlet", [], "vmag", "no", 1.2, "quit"
    )
    session.tui.solver.define.boundary_conditions.set.velocity_inlet(
        "hot-inlet", [], "ke-spec", "no", "no", "no", "yes", "quit"
    )
    session.tui.solver.define.boundary_conditions.set.velocity_inlet(
        "hot-inlet", [], "turb-intensity", 5, "quit"
    )
    session.tui.solver.define.boundary_conditions.set.velocity_inlet(
        "hot-inlet", [], "turb-hydraulic-diam", 1, "quit"
    )
    session.tui.solver.define.boundary_conditions.set.velocity_inlet(
        "hot-inlet", [], "temperature", "no", 313.15, "quit"
    )

    session.tui.solver.define.boundary_conditions.set.pressure_outlet(
        "outlet", [], "turb-intensity", 5, "quit"
    )
    session.tui.solver.define.boundary_conditions.set.pressure_outlet(
        "outlet", [], "turb-viscosity-ratio", 4, "quit"
    )

    ###############################################################################
    # Enable the plotting of residuals during the calculation.
    session.tui.solver.solve.monitors.residual.plot("yes")

    ###############################################################################
    # Initialize the flow field using the Hybrid Initialization
    session.tui.solver.solve.initialize.hyb_initialization()

    ###############################################################################
    # Solve for 250 Iterations.
    session.tui.solver.solve.iterate(250)

    ###############################################################################
    # Assert the returned mass flux report definition value
    root = session.get_settings_root()
    root.solution.report_definitions.flux["report_mfr"] = {}
    root.solution.report_definitions.flux["report_mfr"].zone_names = [
        "cold-inlet",
        "hot-inlet",
        "outlet",
    ]

    check_report_definition = partial(
        check_report_definition_result,
        report_definitions=root.solution.report_definitions,
    )

    check_report_definition(
        report_definition_name="report_mfr",
        expected_result=approx(-2.985690364942784e-06, abs=1e-3),
    )

    ###############################################################################
    # Assert the returned temperature report definition value on the outlet surface
    root.solution.report_definitions.surface["outlet-temp-avg"] = {}
    root.solution.report_definitions.surface[
        "outlet-temp-avg"
    ].report_type = "surface-massavg"
    root.solution.report_definitions.surface["outlet-temp-avg"].field = "temperature"
    root.solution.report_definitions.surface["outlet-temp-avg"].surface_names = [
        "outlet"
    ]

    check_report_definition(
        report_definition_name="outlet-temp-avg",
        expected_result=approx(296.229, rel=1e-3),
    )

    ###############################################################################
    # Write final case and data.
    # session.tui.solver.file.write_case_data("mixing_elbow2_tui.cas.h5")

    ###############################################################################
