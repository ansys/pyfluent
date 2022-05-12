""".. _ref_mixing_elbow_settings_api_beta:

Fluid Flow and Heat Transfer in a Mixing Elbow
----------------------------------------------
This example illustrates the setup and solution of a three-dimensional
turbulent fluid flow and heat transfer problem in a mixing elbow using
settings api (Beta). The mixing elbow configuration is encountered in
piping systems in power plants and process industries. It is often
important to predict the flow field and temperature field in the area
of the mixing region in order to properly design the junction.

This example demonstrates how to do the following:

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


###############################################################################
# First, download the mesh file and start Fluent as a service with
# Solver Mode, Double Precision, Number of Processors 2

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.post import set_config
from ansys.fluent.post.pyvista import Graphics

set_config(blocking=True)
set_config(blocking=True, set_view_on_display="isometric")

import_filename = examples.download_file("mixing_elbow.msh.h5", "pyfluent/mixing_elbow")

session = pyfluent.launch_fluent(precision="double", processor_count=2)
###############################################################################
# The settings objects provide a natural way to access and modify settings.
# The top-level settings object for a session can be accessed with the
# get_settings_root() method of the session object.
# Enabling the settings objects.

settings = session.get_settings_root()
###############################################################################
# Import mesh and perform mesh check:
# The mesh check will list the minimum and maximum x, y, and z values from the
# mesh in the default SI unit of meters. It will also report a number of other
# mesh features that are checked. Any errors in the mesh will be reported at
# this time. Ensure that the minimum volume is not negative, since Ansys Fluent
# cannot begin a calculation when this is the case.

settings.file.read(file_type="case", file_name=import_filename)
session.tui.solver.mesh.check()

###############################################################################
# Set the working units for the mesh:
# select "in" to set inches as the working unit for length. Note:  Because the
# default SI units will be used for everything except length, there is no need
# to change any other units in this problem. If you want a different working
# unit for length, other than inches (for example, millimeters), make the
# appropriate change.

session.tui.solver.define.units("length", "in")

###############################################################################
# Enable heat transfer by activating the energy equation.

settings.setup.models.energy.enabled = True

###############################################################################
# Create a new material called water-liquid.

settings.setup.materials.copy_database_material_by_name(
    type="fluid", name="water-liquid"
)

###############################################################################
# Set up the cell zone conditions for the fluid zone (elbow-fluid). Select
# water-liquid from the Material list.

settings.setup.cell_zone_conditions.fluid["elbow-fluid"].material = "water-liquid"

###############################################################################
# Set up the boundary conditions for the inlets, outlet, and walls for your CFD
# analysis.
# cold inlet (cold-inlet), Setting: Value:
# Velocity Specification Method: Magnitude, Normal to Boundary
# Velocity Magnitude: 0.4 [m/s]
# Specification Method: Intensity and Hydraulic Diameter
# Turbulent Intensity: 5 [%]
# Hydraulic Diameter: 4 [inch]
# Temperature: 293.15 [K]

settings.setup.boundary_conditions.velocity_inlet["cold-inlet"].vmag = {
    "option": "constant or expression",
    "constant": 0.4,
}
settings.setup.boundary_conditions.velocity_inlet[
    "cold-inlet"
].ke_spec = "Intensity and Hydraulic Diameter"
settings.setup.boundary_conditions.velocity_inlet["cold-inlet"].turb_intensity = 5
settings.setup.boundary_conditions.velocity_inlet[
    "cold-inlet"
].turb_hydraulic_diam = "4 [in]"
settings.setup.boundary_conditions.velocity_inlet["cold-inlet"].t = {
    "option": "constant or expression",
    "constant": 293.15,
}

###############################################################################
# hot inlet (hot-inlet), Setting: Value:
# Velocity Specification Method: Magnitude, Normal to Boundary
# Velocity Magnitude: 1.2 [m/s]
# Specification Method: Intensity and Hydraulic Diameter
# Turbulent Intensity: 5 [%]
# Hydraulic Diameter: 1 [inch]
# Temperature: 313.15 [K]

settings.setup.boundary_conditions.velocity_inlet["hot-inlet"].vmag = {
    "option": "constant or expression",
    "constant": 1.2,
}
settings.setup.boundary_conditions.velocity_inlet[
    "hot-inlet"
].ke_spec = "Intensity and Hydraulic Diameter"
settings.setup.boundary_conditions.velocity_inlet[
    "hot-inlet"
].turb_hydraulic_diam = "1 [in]"
settings.setup.boundary_conditions.velocity_inlet["hot-inlet"].t = {
    "option": "constant or expression",
    "constant": 313.15,
}

###############################################################################
# pressure outlet (outlet), Setting: Value:
# Backflow Turbulent Intensity: 5 [%]
# Backflow Turbulent Viscosity Ratio: 4

settings.setup.boundary_conditions.pressure_outlet["outlet"].turb_viscosity_ratio = 4

###############################################################################
# Enable the plotting of residuals during the calculation.

session.tui.solver.solve.monitors.residual.plot("yes")

###############################################################################
# Create a surface report definition of average temperature at the outlet
# (outlet) called outlet-temp-avg

settings.solution.report_definitions.surface["temperature_outlet"] = {}
settings.solution.report_definitions.surface[
    "temperature_outlet"
].report_type = "surface-massavg"
settings.solution.report_definitions.surface["temperature_outlet"].field = "temperature"
settings.solution.report_definitions.surface["temperature_outlet"].surface_names = [
    "outlet"
]
settings.solution.report_definitions.compute(report_defs=["temperature_outlet"])

###############################################################################
# Initialize the flow field using the Hybrid Initialization

settings.solution.initialization.hybrid_initialize()

###############################################################################
# Solve for 150 Iterations.

settings.solution.run_calculation.iterate.get_attr("arguments")
settings.solution.run_calculation.iterate(number_of_iterations=150)

###############################################################################
# Examine the mass flux report for convergence: Select cold-inlet, hot-inlet,
# and outlet from the Boundaries selection list.
# Compute a Mass Flux Report for convergence

settings.solution.report_definitions.flux[
    "mass_flow_rate"
] = {}  # Create a default report flux report
settings.solution.report_definitions.flux["mass_flow_rate"].zone_names = [
    "cold-inlet",
    "hot-inlet",
    "outlet",
]
settings.solution.report_definitions.compute(report_defs=["mass_flow_rate"])

###############################################################################
# Create and display a definition for velocity magnitude contours on the
# symmetry plane:
# Provide velocity_contour_symmetry for Contour Name. Select velocity magnitude. Select
# symmetry-xyplane from the Surfaces list. Display velocity_contour_symmetry contour.

settings.results.graphics.contour["velocity_contour_symmetry"] = {}
settings.results.graphics.contour["velocity_contour_symmetry"].print_state()
settings.results.graphics.contour[
    "velocity_contour_symmetry"
].field = "velocity-magnitude"
settings.results.graphics.contour["velocity_contour_symmetry"].surfaces_list = [
    "symmetry-xyplane"
]
# settings.results.graphics.contour["velocity_contour_symmetry"].display()

###############################################################################
# Create and display a definition for temperature contours on the symmetry
# plane:
# Provide temperature_contour_symmetry for Contour Name. Select temperature. Select
# symmetry-xyplane from the Surfaces list. Display temperature_contour_symmetry contour.

settings.results.graphics.contour["temperature_contour_symmetry"] = {}
settings.results.graphics.contour["temperature_contour_symmetry"].print_state()
settings.results.graphics.contour["temperature_contour_symmetry"].field = "temperature"
settings.results.graphics.contour["temperature_contour_symmetry"].surfaces_list = [
    "symmetry-xyplane"
]
# settings.results.graphics.contour["temperature_contour_symmetry"].display()

###############################################################################
# Create and display velocity vectors on the symmetry-xyplane plane:
# Provide velocity_vector_symmetry for Vector Name. Select arrow for the Style. Select
# symmetry-xyplane from the Surfaces selection list.
settings.results.graphics.vector["velocity_vector_symmetry"] = {}
settings.results.graphics.vector["velocity_vector_symmetry"].print_state()
settings.results.graphics.vector["velocity_vector_symmetry"].field = "temperature"
settings.results.graphics.vector["velocity_vector_symmetry"].surfaces_list = [
    "symmetry-xyplane"
]
settings.results.graphics.vector["velocity_vector_symmetry"].scale.scale_f = 4
settings.results.graphics.vector["velocity_vector_symmetry"].style = "arrow"
# settings.results.graphics.vector["velocity_vector_symmetry"].display()

###############################################################################
# Create an iso-surface representing the intersection of the plane z=0 and the
# surface outlet. Name: z=0_outlet

session.tui.solver.surface.iso_surface(
    "z-coordinate", "z=0_outlet", "outlet", "()", "()", "0", "()"
)

###############################################################################
# Create Contour on the iso-surface

settings.results.graphics.contour["temperature_contour_isosurface"] = {}
settings.results.graphics.contour["temperature_contour_isosurface"].print_state()
settings.results.graphics.contour[
    "temperature_contour_isosurface"
].field = "temperature"
settings.results.graphics.contour["temperature_contour_isosurface"].surfaces_list = [
    "z=0_outlet"
]
# settings.results.graphics.contour["temperature_contour_isosurface"].display()

###############################################################################
# session.tui.solver.file.write_case_data("mixing_elbow1_set.cas.h5")
# Display and save an XY plot of the temperature profile across the centerline
# of the outlet for the initial solution

session.tui.solver.display.objects.create(
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
# Mesh display using PyVista

graphics_session = Graphics(session)
mesh_1 = graphics_session.Meshes["mesh-1"]
mesh_1.show_edges = True
mesh_1.surfaces_list = [
    "cold-inlet",
    "hot-inlet",
    "wall-elbow",
    "wall-inlet",
    "symmetry-xyplane",
    "outlet",
]

mesh_1.display()

###############################################################################
# Write final case and data. Exit.
# session.tui.solver.file.write_case_data('mixing_elbow2_set.cas.h5')
session.exit()

###############################################################################
