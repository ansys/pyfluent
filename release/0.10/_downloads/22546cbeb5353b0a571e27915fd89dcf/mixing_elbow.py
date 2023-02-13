""".. _ref_mixing_elbow_tui_api:

End-to-end Watertight Meshing Workflow
---------------------------------------
This example illustrates the setup and solution of a three-dimensional
turbulent fluid flow and heat transfer problem in a mixing elbow. The mixing
elbow configuration is encountered in piping systems in power plants and
process industries. It is often important to predict the flow field and
temperature field in the area of the mixing region in order to properly design
the junction.

End-to-end Watertight Meshing Workflow example

- Use the Watertight Geometry guided workflow to:
    - Import a CAD geometry
    - Generate a surface mesh
    - Describe the geometry
    - Generate a volume mesh
- Launch Ansys Fluent.
- Read an existing mesh file into Ansys Fluent.
- Use mixed units to define the geometry and fluid properties.
- Set material properties and boundary conditions for a turbulent
  forced-convection problem.
- Create a surface report definition and use it as a convergence criterion.
- Calculate a solution using the pressure-based solver.
- Visually examine the flow and temperature fields using the postprocessing
  tools available in Ansys Fluent.

Problem Description:
A cold fluid at 20 deg C flows into the pipe through a large inlet, and mixes
with a warmer fluid at 40 deg C that enters through a smaller inlet located at
the elbow. The pipe dimensions are in inches and the fluid properties and
boundary conditions are given in SI units. The Reynolds number for the flow at
the larger inlet is 50, 800, so a turbulent flow model will be required.
"""
# sphinx_gallery_thumbnail_path = '_static/mixing_elbow.png'

###############################################################################
# First, download the geometry file and start Fluent as a service with
# Meshing Mode, Double Precision, Number of Processors 2

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples

import_filename = examples.download_file("mixing_elbow.pmdb", "pyfluent/mixing_elbow")

session = pyfluent.launch_fluent(
    meshing_mode=True, precision="double", processor_count=2
)

###############################################################################
# Select the Watertight Geometry Meshing Workflow
session.meshing.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")


###############################################################################
# Import the CAD geometry. For Length Units, select "in".
# Execute the Import Geometry task.

session.meshing.workflow.TaskObject["Import Geometry"].Arguments = dict(
    FileName=import_filename, LengthUnit="in"
)

session.meshing.workflow.TaskObject["Import Geometry"].Execute()

###############################################################################
# Add local sizing:
# In the Add Local Sizing task, you are prompted as to whether or not you would
# like to add local sizing controls to the faceted geometry. For the purposes of
# this example, you can keep the default setting. Execute to complete this task
# and proceed to the next task in the workflow.
session.meshing.workflow.TaskObject["Add Local Sizing"].AddChildToTask()
session.meshing.workflow.TaskObject["Add Local Sizing"].Execute()

###############################################################################
# Generate the surface mesh:
# In the Generate the Surface Mesh task, you can set various properties of the
# surface mesh for the faceted geometry. Specify 0.3 for Maximum Size. Execute
# the Surface Mesh to complete this task and proceed to the next task in the
# workflow.
session.meshing.workflow.TaskObject["Generate the Surface Mesh"].Arguments = {
    "CFDSurfaceMeshControls": {"MaxSize": 0.3}
}
session.meshing.workflow.TaskObject["Generate the Surface Mesh"].Execute()

###############################################################################
# Describe the geometry:
# When you select the Describe Geometry task, you are prompted with questions
# relating to the nature of the imported geometry. Since the geometry defined
# the fluid region. Select The geometry consists of only fluid regions with no
# voids for Geometry Type. Execute Describe Geometry to complete this task and
# proceed to the next task in the workflow.
session.meshing.workflow.TaskObject["Describe Geometry"].UpdateChildTasks(
    SetupTypeChanged=False
)
session.meshing.workflow.TaskObject["Describe Geometry"].Arguments = dict(
    SetupType="The geometry consists of only fluid regions with no voids"
)
session.meshing.workflow.TaskObject["Describe Geometry"].UpdateChildTasks(
    SetupTypeChanged=True
)
session.meshing.workflow.TaskObject["Describe Geometry"].Execute()

###############################################################################
# Update Boundaries Task:
# For the wall-inlet boundary, change the Boundary Type field to wall. Execute
# Update Boundaries to complete this task and proceed to the next task in the
# workflow.
session.meshing.workflow.TaskObject["Update Boundaries"].Arguments = {
    "BoundaryLabelList": ["wall-inlet"],
    "BoundaryLabelTypeList": ["wall"],
    "OldBoundaryLabelList": ["wall-inlet"],
    "OldBoundaryLabelTypeList": ["velocity-inlet"],
}
session.meshing.workflow.TaskObject["Update Boundaries"].Execute()

###############################################################################
# Update your regions:
# Select the Update Regions task, where you can review the names and types of
# the various regions that have been generated from your imported geometry, and
# change them as needed. Keep the default settings, and execute Update Regions.
session.meshing.workflow.TaskObject["Update Regions"].Execute()

###############################################################################
# Add Boundary Layers:
# Select the Add Boundary Layers task, where you can set properties of the
# boundary layer mesh. Keep the default settings, and Add Boundary Layers.

session.meshing.workflow.TaskObject["Add Boundary Layers"].AddChildToTask()
session.meshing.workflow.TaskObject["Add Boundary Layers"].InsertCompoundChildTask()
session.meshing.workflow.TaskObject["smooth-transition_1"].Arguments = {
    "BLControlName": "smooth-transition_1",
}
session.meshing.workflow.TaskObject["Add Boundary Layers"].Arguments = {}
session.meshing.workflow.TaskObject["smooth-transition_1"].Execute()

###############################################################################
# Generate the volume mesh:
# Select the Generate the Volume Mesh task, where you can set properties of the
# volume mesh. Select the poly-hexcore for Fill With. Execute Generate the
# Volume Mesh.
session.meshing.workflow.TaskObject["Generate the Volume Mesh"].Arguments = {
    "VolumeFill": "poly-hexcore",
    "VolumeFillControls": {
        "HexMaxCellLength": 0.3,
    },
}
session.meshing.workflow.TaskObject["Generate the Volume Mesh"].Execute()

###############################################################################
# Check the mesh in Meshing mode
session.meshing.tui.mesh.check_mesh()

###############################################################################
# Save the mesh file (mixing_elbow.msh.h5)
# session.meshing.tui.file.write_mesh('mixing_elbow.msh.h5')

###############################################################################
# Switch to Solution mode:
# Now that a high-quality mesh has been generated using Ansys Fluent in meshing
# mode, you can now switch to solver mode to complete the setup of the
# simulation. We have just checked the mesh, so select Yes to switch to
# solution mode.
session.meshing.tui.switch_to_solution_mode("yes")

###############################################################################
# Check the mesh in Solver mode:
# The mesh check will list the minimum and maximum x, y, and z values from the
# mesh in the default SI unit of meters. It will also report a number of other
# mesh features that are checked. Any errors in the mesh will be reported at
# this time. Ensure that the minimum volume is not negative, since Ansys Fluent
# cannot begin a calculation when this is the case.
session.solver.tui.mesh.check()

###############################################################################
# Set the working units for the mesh:
# select "in" to set inches as the working unit for length. Note:  Because the
# default SI units will be used for everything except length, there is no need
# to change any other units in this problem. If you want a different working
# unit for length, other than inches (for example, millimeters), make the
# appropriate change.
session.solver.tui.define.units("length", "in")

###############################################################################
# Enable heat transfer by activating the energy equation.
session.solver.tui.define.models.energy("yes", ", ", ", ", ", ", ", ")

###############################################################################
# Create a new material called water-liquid.
session.solver.tui.define.materials.copy("fluid", "water-liquid")

###############################################################################
# Set up the cell zone conditions for the fluid zone (elbow-fluid). Select
# water-liquid from the Material list.
session.solver.tui.define.boundary_conditions.fluid(
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
# Set up the boundary conditions for the inlets, outlet, and walls for your CFD
# analysis.

# cold inlet (cold-inlet), Setting: Value:
# Velocity Specification Method: Magnitude, Normal to Boundary

session.solver.tui.define.boundary_conditions.set.velocity_inlet(
    "cold-inlet", [], "vmag", "no", 0.4, "quit"
)
session.solver.tui.define.boundary_conditions.set.velocity_inlet(
    "cold-inlet", [], "ke-spec", "no", "no", "no", "yes", "quit"
)
session.solver.tui.define.boundary_conditions.set.velocity_inlet(
    "cold-inlet", [], "turb-intensity", 5, "quit"
)
session.solver.tui.define.boundary_conditions.set.velocity_inlet(
    "cold-inlet", [], "turb-hydraulic-diam", 4, "quit"
)
session.solver.tui.define.boundary_conditions.set.velocity_inlet(
    "cold-inlet", [], "temperature", "no", 293.15, "quit"
)

###############################################################################
# hot inlet (hot-inlet), Setting: Value:
# Velocity Specification Method: Magnitude, Normal to Boundary


session.solver.tui.define.boundary_conditions.set.velocity_inlet(
    "hot-inlet", [], "vmag", "no", 1.2, "quit"
)
session.solver.tui.define.boundary_conditions.set.velocity_inlet(
    "hot-inlet", [], "ke-spec", "no", "no", "no", "yes", "quit"
)
session.solver.tui.define.boundary_conditions.set.velocity_inlet(
    "hot-inlet", [], "turb-intensity", 5, "quit"
)
session.solver.tui.define.boundary_conditions.set.velocity_inlet(
    "hot-inlet", [], "turb-hydraulic-diam", 1, "quit"
)
session.solver.tui.define.boundary_conditions.set.velocity_inlet(
    "hot-inlet", [], "temperature", "no", 313.15, "quit"
)

###############################################################################
# pressure outlet (outlet), Setting: Value:
# Backflow Turbulent Intensity: 5 [%]
# Backflow Turbulent Viscosity Ratio: 4

session.solver.tui.define.boundary_conditions.set.pressure_outlet(
    "outlet", [], "turb-intensity", 5, "quit"
)
session.solver.tui.define.boundary_conditions.set.pressure_outlet(
    "outlet", [], "turb-viscosity-ratio", 4, "quit"
)

###############################################################################
# Enable the plotting of residuals during the calculation.
session.solver.tui.solve.monitors.residual.plot("yes")

###############################################################################
# Create a surface report definition of average temperature at the outlet
# (outlet) called "outlet-temp-avg
session.solver.tui.solve.report_definitions.add(
    "outlet-temp-avg",
    "surface-massavg",
    "field",
    "temperature",
    "surface-names",
    "outlet",
    "()",
    "quit",
)

###############################################################################
# Create a convergence condition for outlet-temp-avg:
# Provide con-outlet-temp-avg for Conditions. Select outlet-temp-avg Report
# Definition. Provide 1e-5 for Stop Criterion. Provide 20 for Ignore Iterations
# Before. Provide 15 for Use Iterations. Enable Print. Set Every Iteration to
# 3.


# These settings will cause Fluent to consider the solution converged when the
# surface report definition value for each of the previous 15 iterations is
# within 0.001% of the current value. Convergence of the values will be checked
# every 3 iterations. The first 20 iterations will be ignored, allowing for any
# initial solution dynamics to settle out. Note that the value printed to the
# console is the deviation between the current and previous iteration values
# only.
session.solver.tui.solve.convergence_conditions(
    "conv-reports",
    "add",
    "con-outlet-temp-avg",
    "initial-values-to-ignore",
    "20",
    "previous-values-to-consider",
    "15",
    "print?",
    "yes",
    "report-defs",
    "outlet-temp-avg",
    "stop-criterion",
    "1e-04",
    "quit",
    "quit",
    "condition",
    "1",
    "frequency",
    "3",
    "quit",
)
session.solver.tui.solve.convergence_conditions("frequency", "3", "quit")

###############################################################################
# Initialize the flow field using the Hybrid Initialization
session.solver.tui.solve.initialize.hyb_initialization()

###############################################################################
# Save the case file (mixing_elbow1.cas.h5).
# session.solver.tui.file.write_case('mixing_elbow1.cas.h5')

###############################################################################
# Solve for 100 Iterations.
session.solver.tui.solve.iterate(100)

###############################################################################
# Save the data file (mixing_elbow1.dat.h5).
# session.solver.tui.file.write_data('mixing_elbow1.dat.h5')

###############################################################################
# Create and display a definition for velocity magnitude contours on the
# symmetry plane:
# Provide contour-vel for Contour Name. Select velocity magnitude. Select
# symmetry-xyplane from the Surfaces list. Display contour-vel contour.

session.solver.tui.display.objects.create(
    "contour",
    "contour-vel",
    "filled?",
    "yes",
    "node-values?",
    "yes",
    "field",
    "velocity-magnitude",
    "surfaces-list",
    "symmetry-xyplane",
    "()",
    "coloring",
    "banded",
    "quit",
)

###############################################################################
# Create and display a definition for temperature contours on the symmetry
# plane:
# Provide contour-temp for Contour Name. Select temperature. Select
# symmetry-xyplane from the Surfaces list. Display contour-temp contour.

session.solver.tui.display.objects.create(
    "contour",
    "contour-temp",
    "filled?",
    "yes",
    "node-values?",
    "yes",
    "field",
    "temperature",
    "surfaces-list",
    "symmetry-xyplane",
    "()",
    "coloring",
    "smooth",
    "quit",
)

###############################################################################
# Create and display velocity vectors on the symmetry-xyplane plane:

# Provide vector-vel for Vector Name. Select arrow for the Style. Select
# symmetry-xyplane from the Surfaces selection list. Provide 4 for Scale. Set
# Skip to 2.
session.solver.tui.display.objects.create(
    "vector",
    "vector-vel",
    "style",
    "arrow",
    "surface-list",
    "symmetry-xyplane",
    "()",
    "scale",
    "scale-f",
    "4",
    "quit",
    "skip",
    "2",
    "quit",
)

###############################################################################
# Create an iso-surface representing the intersection of the plane z=0 and the
# surface outlet. Name: z=0_outlet
session.solver.tui.surface.iso_surface(
    "z-coordinate", "z=0_outlet", "outlet", "()", "()", "0", "()"
)

###############################################################################
# Display and save an XY plot of the temperature profile across the centerline
# of the outlet for the initial solution
session.solver.tui.display.objects.create(
    "xy",
    "xy-outlet-temp",
    "y-axis-function",
    "temperature",
    "surfaces-list",
    "z=0_outlet",
    "()",
    "quit",
)

###############################################################################
# Write final case and data.
# session.solver.tui.file.write_case_data("mixing_elbow2_tui.cas.h5")

#########################################################################
# Close Fluent

session.exit()

###############################################################################
