""".. _ref_mixing_elbow_settings_api_beta:

Fluent setup and solution using settings objects
------------------------------------------------
This example sets up and solves a three-dimensional turbulent fluid flow
and heat transfer problem in a mixing elbow, which is common in piping
systems in power plants and process industries. Predicting the flow field
and temperature field in the area of the mixing region is important to
designing the junction properly.

This example uses settings objects.

**Problem description**

A cold fluid at 20 deg C flows into the pipe through a large inlet. It then mixes
with a warmer fluid at 40 deg C that enters through a smaller inlet located at
the elbow. The pipe dimensions are in inches, and the fluid properties and
boundary conditions are given in SI units. Because the Reynolds number for the
flow at the larger inlet is ``50, 800``, a turbulent flow model is required.
"""

###############################################################################
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Perform required imports, which includes downloading and importing
# the geometry file.

# sphinx_gallery_thumbnail_path = '_static/mixing_elbow_settings.png'
import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples

import_file_name = examples.download_file(
    "mixing_elbow.msh.h5", "pyfluent/mixing_elbow"
)

###############################################################################
# Launch Fluent
# ~~~~~~~~~~~~~
# Launch Fluent as a service in solver mode with double precision running on
# two processors.

solver = pyfluent.launch_fluent(precision="double", processor_count=2, mode="solver")

###############################################################################
# Import mesh and perform mesh check
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import the mesh and perform a mesh check, which lists the minimum and maximum
# x, y, and z values from the mesh in the default SI units of meters. The mesh
# check also reports a number of other mesh features that are checked. Any errors
# in the mesh are reported. Ensure that the minimum volume is not negative because
# Fluent cannot begin a calculation when this is the case.

solver.file.read(file_type="case", file_name=import_file_name)
solver.tui.mesh.check()

###############################################################################
# Set working units for mesh
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set the working units for the mesh to inches. Because the default SI units are
# used for everything except length, you do not have to change any other units
# in this example. If you want working units for length to be other than inches
# (for example, millimeters), make the appropriate change.

solver.tui.define.units("length", "in")

###############################################################################
# Enable heat transfer
# ~~~~~~~~~~~~~~~~~~~~
# Enable heat transfer by activating the energy equation.

solver.setup.models.energy.enabled = True

###############################################################################
# Create material
# ~~~~~~~~~~~~~~~
# Create a material named ``"water-liquid"``.

solver.setup.materials.database.copy_by_name(type="fluid", name="water-liquid")

###############################################################################
# Set up cell zone conditions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set up the cell zone conditions for the fluid zone (``elbow-fluid``). Set ``material``
# to ``"water-liquid"``.

solver.setup.cell_zone_conditions.fluid["elbow-fluid"].material = "water-liquid"

###############################################################################
# Set up boundary conditions for CFD analysis
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set up the boundary conditions for the inlets, outlet, and walls for CFD
# analysis.

# cold inlet (cold-inlet), Setting: Value:
# Velocity Specification Method: Magnitude, Normal to Boundary
# Velocity Magnitude: 0.4 [m/s]
# Specification Method: Intensity and Hydraulic Diameter
# Turbulent Intensity: 5 [%]
# Hydraulic Diameter: 4 [inch]
# Temperature: 293.15 [K]
cold_inlet = solver.setup.boundary_conditions.velocity_inlet["cold-inlet"]

cold_inlet.vmag = 0.4
cold_inlet.ke_spec = "Intensity and Hydraulic Diameter"
cold_inlet.turb_intensity = 0.05
cold_inlet.turb_hydraulic_diam = "4 [in]"
cold_inlet.t = 293.15

# hot inlet (hot-inlet), Setting: Value:
# Velocity Specification Method: Magnitude, Normal to Boundary
# Velocity Magnitude: 1.2 [m/s]
# Specification Method: Intensity and Hydraulic Diameter
# Turbulent Intensity: 5 [%]
# Hydraulic Diameter: 1 [inch]
# Temperature: 313.15 [K]
hot_inlet = solver.setup.boundary_conditions.velocity_inlet["hot-inlet"]

hot_inlet.vmag = 1.2
hot_inlet.ke_spec = "Intensity and Hydraulic Diameter"
hot_inlet.turb_hydraulic_diam = "1 [in]"
hot_inlet.t = 313.15

# pressure outlet (outlet), Setting: Value:
# Backflow Turbulent Intensity: 5 [%]
# Backflow Turbulent Viscosity Ratio: 4

solver.setup.boundary_conditions.pressure_outlet["outlet"].turb_viscosity_ratio = 4

###############################################################################
# Disable plotting of residuals during calculation
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Disable plotting of residuals during the calculation.

solver.tui.solve.monitors.residual.plot("no")

###############################################################################
# Initialize flow field
# ~~~~~~~~~~~~~~~~~~~~~
# Initialize the flow field using hybrid initialization.

solver.solution.initialization.hybrid_initialize()

###############################################################################
# Solve for 150 iterations
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Solve for 150 iterations.

solver.solution.run_calculation.iterate.argument_names
solver.solution.run_calculation.iterate(iter_count=150)

###############################################################################
# Create velocity vectors
# ~~~~~~~~~~~~~~~~~~~~~~~
# Create and display velocity vectors on the ``symmetry-xyplane`` plane
solver.results.graphics.vector["velocity_vector_symmetry"] = {}
velocity_symmetry = solver.results.graphics.vector["velocity_vector_symmetry"]
velocity_symmetry.print_state()
velocity_symmetry.field = "temperature"
velocity_symmetry.surfaces_list = [
    "symmetry-xyplane",
]
velocity_symmetry.scale.scale_f = 4
velocity_symmetry.style = "arrow"

###############################################################################
# .. image:: /_static/mixing_elbow_016.png
#   :width: 500pt
#   :align: center

###############################################################################
# Compute mass flow rate
# ~~~~~~~~~~~~~~~~~~~~~~
# Compute the mass flow rate.
solver.solution.report_definitions.flux["mass_flow_rate"] = {}

mass_flow_rate = solver.solution.report_definitions.flux["mass_flow_rate"]
mass_flow_rate.zone_names.get_attr("allowed-values")
mass_flow_rate.zone_names = [
    "cold-inlet",
    "hot-inlet",
    "outlet",
]
mass_flow_rate.print_state()
solver.solution.report_definitions.compute(report_defs=["mass_flow_rate"])

#########################################################################
# Close Fluent
# ~~~~~~~~~~~~
# Close Fluent.

solver.exit()
