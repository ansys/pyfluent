"""

Modeling Cavitation
-------------------
This example examines the pressure-driven cavitating flow of water
through a sharp-edged orifice. This is a typical configuration in
fuel injectors, and brings a challenge to the physics and numerics
of cavitation models because of the high pressure differentials
involved and the high ratio of liquid to vapor density.

This example uses the multiphase modeling capability of Ansys
Fluent, and will be able to predict the strong cavitation near the
orifice after flow separation at a sharp edge.

**Workflow tasks**

This example demonstrates how to do the following:

- Set boundary conditions for internal flow
- Use the mixture model with cavitation effects
- Calculate a solution using the pressure-based coupled solver

**Problem description**

The problem considers the cavitation caused by the flow separation
after a sharp-edged orifice. The flow is pressure driven, with an
inlet pressure of 5 x 10^5 Pa and an outlet pressure of 9.5 x 10^4 Pa.
The orifice diameter is 4 x 10^-3 m, and the geometrical parameters
of the orifice are D/d = 2.88 and L/d = 4, where D, d, and L are the
inlet diameter, orifice diameter, and orifice length respectively.
"""

# sphinx_gallery_thumbnail_path = '_static/cavitation_model.png'

###############################################################################
# Example Setup
# -------------
# Before you can begin, you must set up the example and initialize this workflow.
#
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Perform required imports, which includes downloading and importing
# the geometry file.

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples

import_filename = examples.download_file(
    "cav.msh", "pyfluent/cavitation", save_path=pyfluent.EXAMPLES_PATH
)

###############################################################################
# Launch Fluent
# ~~~~~~~~~~~~~
# Launch Fluent as a service in 2d solution mode with double precision running
# on one processor.

solver = pyfluent.launch_fluent(
    precision="double",
    processor_count=1,
    mode="solver",
    version="2d",
    cwd=pyfluent.EXAMPLES_PATH,
    show_gui=True,
)

###############################################################################
# Reading and Checking the Mesh
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
solver.read_case("cav.msh")

solver.mesh.check()

###############################################################################
# Set units for length
# ~~~~~~~~~~~~~~~~~~~~
# Set the units for length.

solver.tui.define.units("length", "m")

###############################################################################
# Specify an axisymmetric model
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

solver.setup.general.solver.two_dim_space = "axisymmetric"

###############################################################################
# Enable the multiphase mixture model.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

solver.setup.models.multiphase.models = "mixture"
solver.tui.define.models.multiphase.mixture_parameters(False)

###############################################################################
# Select turbulence model
# ~~~~~~~~~~~~~~~~~~~~~~~

# model : k-omega
# k-omega model : sst

solver.setup.models.viscous = {"model": "k-omega", "k_omega_model": "sst"}

###############################################################################
# Define materials
# ~~~~~~~~~~~~~~~~
# Create the default material ``water``.

# name: water
# density : constant
# reference density : 1000 [kg/m^3]
# viscosity : constant
# viscosity method : constant
# reference viscosity : 0.001 [kg/(m s)]

water = {
    "density": {"option": "constant", "value": 1000},
    "name": "water",
    "viscosity": {"option": "constant", "value": 0.001},
}

solver.setup.materials.fluid["water"] = water

# Copy water vapor from the materials database and modify the properties of your local copy.

solver.setup.materials.database.copy_by_name(type="fluid", name="water-vapor")

# Set 0.02558 kg/m3 for Density and 1.26e-06 kg/m–s for Viscosity.

water_vapor = {"density": {"value": 0.02558}, "viscosity": {"value": 1.26e-06}}

solver.setup.materials.fluid["water-vapor"] = water_vapor

###############################################################################
# Phases
# ~~~~~~
# Change phase names to "liquid" and "water-vapor".

solver.tui.define.phases.set_domain_properties.change_phases_names("vapor", "liquid")

# Specify liquid water as the primary phase.

solver.tui.define.phases.set_domain_properties.phase_domains.liquid.material(
    "yes", "water"
)

# Specify water vapor as the secondary phase.

solver.tui.define.phases.set_domain_properties.phase_domains.vapor.material(
    "yes", "water-vapor"
)

###############################################################################
# Enable the cavitation model.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set the number of mass transfer mechanisms to 1, set liquid as the from phase,
# set vapor as the to phase and cavitation as the mechanism.

solver.tui.define.phases.set_domain_properties.interaction_domain.heat_mass_reactions.mass_transfer(
    1, "liquid", "vapor", "cavitation"
)

# Set the vaporization pressure to 3540 Pa and bubble number density to 1e+11

###############################################################################
# Set velocity and turbulence boundary conditions for first inlet
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set the velocity and turbulence boundary conditions for the first inlet
# (``inlet-1``).

solver.tui.define.boundary_conditions.set.velocity_inlet(
    "inlet-1", [], "vmag", "no", 1, "quit"
)

###############################################################################
# Set same boundary conditions for other velocity inlets
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set the same boundary conditions for the other velocity inlets (``inlet_2``
# and ``inlet_3``).

solver.tui.define.boundary_conditions.copy_bc("inlet-1", "inlet-2", "inlet-3", ())

###############################################################################
# Set boundary conditions at outlet
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set the boundary conditions at the outlet (``outlet-1``).

solver.tui.define.boundary_conditions.set.pressure_outlet(
    "outlet-1", [], "turb-intensity", 5, "quit"
)
solver.tui.solve.monitors.residual.plot("yes")

###############################################################################
# Initialize flow field
# ~~~~~~~~~~~~~~~~~~~~~
# Initialize the flow field using hybrid initialization.

solver.tui.solve.initialize.hyb_initialization()

###############################################################################
# Start calculation
# ~~~~~~~~~~~~~~~~~
# Start the calculation by requesting 100 iterations.

###############################################################################
# .. image:: /_static/exhaust_system_015.png
#   :width: 500pt
#   :align: center

solver.tui.solve.set.number_of_iterations(100)
solver.tui.solve.iterate()

# solver.tui.report.volume_integrals.volume("fluid-region-1","()","yes","volume.vrp")

###############################################################################
# Create path lines
# ~~~~~~~~~~~~~~~~~
# Create path lines highlighting the flow field.

###############################################################################
# .. image:: /_static/exhaust_system_016.png
#   :width: 500pt
#   :align: center

solver.tui.display.objects.create(
    "pathlines",
    "pathlines-1",
    "field",
    "time",
    "accuracy-control",
    "tolerance",
    "0.001",
    "skip",
    "5",
    "surfaces-list",
    "inlet-1",
    "inlet-2",
    "inlet-3",
    "()",
    "quit",
)

###############################################################################
# Create iso-surface
# ~~~~~~~~~~~~~~~~~~
# Create an iso-surface through the manifold geometry.

solver.tui.surface.iso_surface(
    "x-coordinate",
    "surf-x-coordinate",
    "()",
    "fluid-region-1",
    "()",
    "380",
    "()",
)

###############################################################################
# Create contours of velocity magnitude
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Create contours of the velocity magnitude throughout the manifold
# along with the mesh.

###############################################################################
# .. image:: /_static/exhaust_system_017.png
#   :width: 500pt
#   :align: center

solver.tui.display.objects.create(
    "contour",
    "contour-velocity",
    "field",
    "velocity-magnitude",
    "surfaces-list",
    "surf-x-coordinate",
    "()",
    "node-values?",
    "no",
    "range-option",
    "auto-range-on",
    "global-range?",
    "no",
    "quit",
    "quit",
)

solver.tui.display.objects.create("mesh", "mesh-1", "surfaces-list", "*", "()", "quit")

###############################################################################
# Create scene
# ~~~~~~~~~~~~
# Create a scene containing the mesh and the contours.

###############################################################################
# .. image:: /_static/exhaust_system_018.png
#   :width: 500pt
#   :align: center

solver.tui.display.objects.create(
    "scene",
    "scene-1",
    "graphics-objects",
    "add",
    "mesh-1",
    "transparency",
    "90",
    "quit",
    "add",
    "contour-velocity",
    "quit",
    "quit",
    "quit",
)

#########################################################################
# Close Fluent
# ~~~~~~~~~~~~
# Close Fluent.

solver.exit()
