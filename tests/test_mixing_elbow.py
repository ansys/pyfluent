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

from pytest import approx

###############################################################################
# Start Fluent
import ansys.fluent.core as pyfluent
from ansys.fluent.core.examples import download_file

def test_mixing_elbow():

    import_filename = download_file(
        filename="mixing_elbow.pmdb", directory="pyfluent/mixing_elbow"
    )

    session = pyfluent.launch_fluent(
        meshing_mode=True, precision="double", processor_count=2
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


    def test_task_state_before_import_geometry():
        assert (
            session.workflow.TaskObject["Import Geometry"].get_state()["State"]
            == "Out-of-date"
        )

    test_task_state_before_import_geometry()

    session.workflow.TaskObject["Import Geometry"].Execute()

    def test_task_state_after_import_geometry():
        assert (
            session.workflow.TaskObject["Import Geometry"].get_state()["State"]
            == "Up-to-date"
        )

    test_task_state_after_import_geometry()

    ###############################################################################
    # Add local sizing
    # Query the task state before and after task execution
    session.workflow.TaskObject["Add Local Sizing"].AddChildToTask()


    def test_task_state_before_local_sizing():
        assert (
            session.workflow.TaskObject["Add Local Sizing"].get_state()["State"]
            == "Out-of-date"
        )


    session.workflow.TaskObject["Add Local Sizing"].Execute()


    def test_task_state_after_local_sizing():
        assert (
            session.workflow.TaskObject["Add Local Sizing"].get_state()["State"]
            == "Up-to-date"
        )


    ###############################################################################
    # Generate the surface mesh
    # Query the task state before and after task execution
    session.workflow.TaskObject["Generate the Surface Mesh"].Arguments = {
        "CFDSurfaceMeshControls": {"MaxSize": 0.3}
    }


    def test_task_state_before_surface_mesh():
        assert (
            session.workflow.TaskObject["Generate the Surface Mesh"].get_state()[
                "State"
            ]
            == "Out-of-date"
        )


    session.workflow.TaskObject["Generate the Surface Mesh"].Execute()


    def test_task_state_after_surface_mesh():
        assert (
            session.workflow.TaskObject["Generate the Surface Mesh"].get_state()[
                "State"
            ]
            == "Up-to-date"
        )


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


    def test_task_state_before_describe_geometry():
        assert (
            session.workflow.TaskObject["Describe Geometry"].get_state()["State"]
            == "Out-of-date"
        )


    session.workflow.TaskObject["Describe Geometry"].Execute()


    def test_task_state_after_describe_geometry():
        assert (
            session.workflow.TaskObject["Describe Geometry"].get_state()["State"]
            == "Up-to-date"
        )


    ###############################################################################
    # Update Boundaries Task
    # Query the task state before and after task execution
    session.workflow.TaskObject["Update Boundaries"].Arguments = {
        "BoundaryLabelList": ["wall-inlet"],
        "BoundaryLabelTypeList": ["wall"],
        "OldBoundaryLabelList": ["wall-inlet"],
        "OldBoundaryLabelTypeList": ["velocity-inlet"],
    }


    def test_task_state_before_update_boundaries():
        assert (
            session.workflow.TaskObject["Update Boundaries"].get_state()["State"]
            == "Out-of-date"
        )


    session.workflow.TaskObject["Update Boundaries"].Execute()


    def test_task_state_after_update_boundaries():
        assert (
            session.workflow.TaskObject["Update Boundaries"].get_state()["State"]
            == "Up-to-date"
        )


    ###############################################################################
    # Update your regions
    # Query the task state before and after task execution


    def test_task_state_before_update_regions():
        assert (
            session.workflow.TaskObject["Update Regions"].get_state()["State"]
            == "Out-of-date"
        )


    session.workflow.TaskObject["Update Regions"].Execute()


    def test_task_state_after_update_regions():
        assert (
            session.workflow.TaskObject["Update Regions"].get_state()["State"]
            == "Up-to-date"
        )


    ###############################################################################
    # Add Boundary Layers
    # Query the task state before and after task execution
    session.workflow.TaskObject["Add Boundary Layers"].AddChildToTask()
    session.workflow.TaskObject["Add Boundary Layers"].InsertCompoundChildTask()
    session.workflow.TaskObject["smooth-transition_1"].Arguments = {
        "BLControlName": "smooth-transition_1",
    }
    session.workflow.TaskObject["Add Boundary Layers"].Arguments = {}


    def test_task_state_before_boundary_layers():
        assert (
            session.workflow.TaskObject["Add Boundary Layers"].get_state()["State"]
            == "Out-of-date"
        )


    session.workflow.TaskObject["smooth-transition_1"].Execute()


    def test_task_state_after_boundary_layers():
        assert (
            session.workflow.TaskObject["Add Boundary Layers"].get_state()["State"]
            == "Up-to-date"
        )


    ###############################################################################
    # Generate the volume mesh
    # Query the task state before and after task execution
    session.workflow.TaskObject["Generate the Volume Mesh"].Arguments = {
        "VolumeFill": "poly-hexcore",
        "VolumeFillControls": {
            "HexMaxCellLength": 0.3,
        },
    }


    def test_task_state_before_volume_mesh():
        assert (
            session.workflow.TaskObject["Generate the Volume Mesh"].get_state()[
                "State"
            ]
            == "Out-of-date"
        )


    session.workflow.TaskObject["Generate the Volume Mesh"].Execute()


    def test_task_state_after_volume_mesh():
        assert (
            session.workflow.TaskObject["Generate the Volume Mesh"].get_state()[
                "State"
            ]
            == "Up-to-date"
        )


    ###############################################################################
    # Check the mesh in Meshing mode
    session.tui.meshing.mesh.check_mesh()

    return

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
    root.solution.report_definitions.compute(report_defs=["report_mfr"])


    def test_report_mfr():
        assert root.solution.report_definitions.compute(
            report_defs=["report_mfr"]
        )["report_mfr"][0] == approx(-2.985690364942784e-06, abs=1e-3)


    ###############################################################################
    # Assert the returned temperature report definition value on the outlet surface
    root.solution.report_definitions.surface["outlet-temp-avg"] = {}
    root.solution.report_definitions.surface[
        "outlet-temp-avg"
    ].report_type = "surface-massavg"
    root.solution.report_definitions.surface[
        "outlet-temp-avg"
    ].field = "temperature"
    root.solution.report_definitions.surface["outlet-temp-avg"].surface_names = [
        "outlet"
    ]
    root.solution.report_definitions.compute(report_defs=["outlet-temp-avg"])


    def test_outlet_temp_avg():
        assert root.solution.report_definitions.compute(
            report_defs=["outlet-temp-avg"]
        )["outlet-temp-avg"][0] == approx(296.229, rel=1e-3)


    ###############################################################################
    # Write final case and data.
    # session.tui.solver.file.write_case_data("mixing_elbow2_tui.cas.h5")

    ###############################################################################
