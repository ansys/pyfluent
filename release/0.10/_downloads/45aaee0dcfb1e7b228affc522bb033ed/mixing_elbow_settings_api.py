""".. _ref_mixing_elbow_settings_api_beta:

Fluent Setup and Solution using Settings Objects
------------------------------------------------
This example illustrates the setup and solution of a three-dimensional
turbulent fluid flow and heat transfer problem in a mixing elbow. The mixing
elbow configuration is encountered in piping systems in power plants and
process industries. It is often important to predict the flow field and
temperature field in the area of the mixing region in order to properly design
the junction.

This example demonstrates use of 'settings' modules (Beta)

- Launch Ansys Fluent
- Import Mesh
- Define Material
- Setup Cell Zone Conditions
- Setup Boundary Conditions
- Initialize and Solve
- Compute Mass Flow Rate and Temperature

Problem Description:
A cold fluid at 20 deg C flows into the pipe through a large inlet, and mixes
with a warmer fluid at 40 deg C that enters through a smaller inlet located at
the elbow. The pipe dimensions are in inches and the fluid properties and
boundary conditions are given in SI units. The Reynolds number for the flow at
the larger inlet is 50, 800, so a turbulent flow model will be required.
"""
# sphinx_gallery_thumbnail_path = '_static/mixing_elbow_settings.png'
###############################################################################
# First, download the mesh file and start Fluent as a service with
# Solver Mode, Double Precision, Number of Processors 2

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples

import_filename = examples.download_file("mixing_elbow.msh.h5", "pyfluent/mixing_elbow")

session = pyfluent.launch_fluent(precision="double", processor_count=2)
###############################################################################
# Import mesh and perform mesh check:
# The mesh check will list the minimum and maximum x, y, and z values from the
# mesh in the default SI unit of meters. It will also report a number of other
# mesh features that are checked. Any errors in the mesh will be reported at
# this time. Ensure that the minimum volume is not negative, since Ansys Fluent
# cannot begin a calculation when this is the case.

session.solver.root.file.read(file_type="case", file_name=import_filename)
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

session.solver.root.setup.models.energy.enabled = True

###############################################################################
# Create a new material called water-liquid.

session.solver.root.setup.materials.copy_database_material_by_name(
    type="fluid", name="water-liquid"
)

###############################################################################
# Set up the cell zone conditions for the fluid zone (elbow-fluid). Select
# water-liquid from the Material list.

session.solver.root.setup.cell_zone_conditions.fluid[
    "elbow-fluid"
].material = "water-liquid"

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

session.solver.root.setup.boundary_conditions.velocity_inlet["cold-inlet"].vmag = {
    "option": "constant or expression",
    "constant": 0.4,
}
session.solver.root.setup.boundary_conditions.velocity_inlet[
    "cold-inlet"
].ke_spec = "Intensity and Hydraulic Diameter"
session.solver.root.setup.boundary_conditions.velocity_inlet[
    "cold-inlet"
].turb_intensity = 5
session.solver.root.setup.boundary_conditions.velocity_inlet[
    "cold-inlet"
].turb_hydraulic_diam = "4 [in]"
session.solver.root.setup.boundary_conditions.velocity_inlet["cold-inlet"].t = {
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

session.solver.root.setup.boundary_conditions.velocity_inlet["hot-inlet"].vmag = {
    "option": "constant or expression",
    "constant": 1.2,
}
session.solver.root.setup.boundary_conditions.velocity_inlet[
    "hot-inlet"
].ke_spec = "Intensity and Hydraulic Diameter"
session.solver.root.setup.boundary_conditions.velocity_inlet[
    "hot-inlet"
].turb_hydraulic_diam = "1 [in]"
session.solver.root.setup.boundary_conditions.velocity_inlet["hot-inlet"].t = {
    "option": "constant or expression",
    "constant": 313.15,
}

###############################################################################
# pressure outlet (outlet), Setting: Value:
# Backflow Turbulent Intensity: 5 [%]
# Backflow Turbulent Viscosity Ratio: 4

session.solver.root.setup.boundary_conditions.pressure_outlet[
    "outlet"
].turb_viscosity_ratio = 4

###############################################################################
# Disable the plotting of residuals during the calculation.

session.solver.tui.solve.monitors.residual.plot("no")

###############################################################################
# Initialize the flow field using the Hybrid Initialization

session.solver.root.solution.initialization.hybrid_initialize()

###############################################################################
# Solve for 150 Iterations.

session.solver.root.solution.run_calculation.iterate.get_attr("arguments")
session.solver.root.solution.run_calculation.iterate(number_of_iterations=150)

###############################################################################
# Create and display velocity vectors on the symmetry-xyplane plane.

session.solver.root.results.graphics.vector["velocity_vector_symmetry"] = {}
session.solver.root.results.graphics.vector["velocity_vector_symmetry"].print_state()
session.solver.root.results.graphics.vector[
    "velocity_vector_symmetry"
].field = "temperature"
session.solver.root.results.graphics.vector[
    "velocity_vector_symmetry"
].surfaces_list = [
    "symmetry-xyplane",
]
session.solver.root.results.graphics.vector[
    "velocity_vector_symmetry"
].scale.scale_f = 4
session.solver.root.results.graphics.vector["velocity_vector_symmetry"].style = "arrow"

###############################################################################
# Compute mass flow rate

session.solver.root.solution.report_definitions.flux["mass_flow_rate"] = {}
session.solver.root.solution.report_definitions.flux[
    "mass_flow_rate"
].zone_names.get_attr("allowed-values")
session.solver.root.solution.report_definitions.flux["mass_flow_rate"].zone_names = [
    "cold-inlet",
    "hot-inlet",
    "outlet",
]
session.solver.root.solution.report_definitions.flux["mass_flow_rate"].print_state()
session.solver.root.solution.report_definitions.compute(report_defs=["mass_flow_rate"])

#########################################################################
# Close Fluent

session.exit()
