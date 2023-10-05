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
solver.tui.define.models.multiphase.mixture_parameters("no", "implicit")

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
    1, "liquid", "vapor", "cavitation", "1", "no", "no", "no"
)

# Set the vaporization pressure to 3540 Pa and bubble number density to 1e+11

solver.setup.models.multiphase.vaporization_pressure = 3540

solver.setup.models.multiphase.bubble_number_density = 1e11

###############################################################################
# Set momentum and turbulence boundary conditions for first inlet
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

inlet_1 = solver.setup.boundary_conditions.pressure_inlet["inlet_1"].phase

# Set direction specification method to ``Normal to Boundary``.
# Set gauge total pressure as 500000 Pa.
# Set supersonic or initial gauge pressure as 449000 Pa.

momentum = {
    "direction_specification_method": "Normal to Boundary",
    "gauge_total_pressure": {"value": 500000},
    "supersonic_or_initial_gauge_pressure": {"value": 449000},
}
inlet_1["mixture"].momentum = momentum

# Set turbulent intensity as 0.05.
# Set turbulent specification to ``Intensity and Viscosity Ratio``.
# Set turbulent viscosity ratio as 10.

in_turbulence = {
    "turbulent_intensity": 0.05,
    "turbulent_specification": "Intensity and Viscosity Ratio",
    "turbulent_viscosity_ratio_real": 10,
}
inlet_1["mixture"].turbulence = in_turbulence

# Set the vapor phase volume fraction as 0.

inlet_1["vapor"].multiphase.volume_fraction.value = 0

# Copy ``inlet_1`` conditions to ``inlet_2``.

solver.setup.boundary_conditions.copy(from_="inlet_1", to="inlet_2")

###############################################################################
# Set boundary conditions at outlet
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set the boundary conditions at the outlet (``outlet``).

outlet = solver.setup.boundary_conditions.pressure_outlet["outlet"].phase

# Set the gauge pressure as 95000

outlet["mixture"].momentum.gauge_pressure.value = 95000

# Set turbulent intensity as 0.05.
# Set turbulent specification to ``Intensity and Viscosity Ratio``.
# Set turbulent viscosity ratio as 10.

out_turbulence = {
    "turbulent_intensity": 0.05,
    "turbulent_specification": "Intensity and Viscosity Ratio",
    "turbulent_viscosity_ratio_real": 10,
}

outlet["mixture"].turbulence = out_turbulence

# Set the vapor phase volume fraction as 0.

outlet["vapor"].multiphase.volume_fraction.value = 0

###############################################################################
# Operating Conditions
# ~~~~~~~~~~~~~~~~~~~~
# Set the operating pressure as 0

solver.setup.general.operating_conditions.operating_pressure = 0

###############################################################################
# Solution
# ~~~~~~~~
# Set the methods parameters.

methods = solver.solution.methods

# Set Coupled from pressure-velocity coupling.

methods.p_v_coupling.flow_scheme = "Coupled"

# Set of presto! for spatial discretization.

methods.discretization_scheme["pressure"] = "presto!"

# Set quick for momentum and volume fraction.

methods.discretization_scheme["mom"] = "quick"
methods.discretization_scheme["mp"] = "quick"

# Set first order upwind for turbulent kinetic energy and turbulent dissipation rate.

methods.discretization_scheme["k"] = "first-order-upwind"
methods.discretization_scheme["omega"] = "first-order-upwind"

# Set global time step from pseudo time method.

methods.pseudo_time_method.formulation.coupled_solver = "global-time-step"

# Enable High Order Term Relaxation.

methods.high_order_term_relaxation.enable = True

# Set the methods parameters.

# Set the pseudo time explicit relaxation factor for volume fraction to 0.3.

solver.solution.controls.pseudo_time_explicit_relaxation_factor.global_dt_pseudo_relax[
    "mp"
] = 0.3

# Enable the plotting of residuals during the calculation.

residual = solver.solution.monitor.residual

residual.options.plot = True

# Set the absolute criteria of continuity, x-velocity, y-velocity, k, omega, and vf-vapor to 1e-05

equations = {
    "continuity": {"convergence_criteria": 1e-05},
    "x-velocity": {"convergence_criteria": 1e-05},
    "y-velocity": {"convergence_criteria": 1e-05},
    "k": {"convergence_criteria": 1e-05},
    "omega": {"convergence_criteria": 1e-05},
    "vf-vapor": {"convergence_criteria": 1e-05},
}
residual.equations = equations

# Enable use specified initial pressure on inlets.

solver.solution.initialization.hybrid_init_options.general_settings.initial_pressure = (
    True
)

# Initialize the solution with hybrid initialization.

solver.solution.initialization.hybrid_initialize()

# Save case file
# ~~~~~~~~~~~~~~
# Solve the case file (``cavitation_model.cas.h5``).

solver.file.write(file_name="cavitation_model.cas.h5", file_type="case")

# Start the calculation by requesting 500 iterations.

solver.solution.run_calculation.iterate(iter_count=500)

# Write the final case file and the data.

solver.file.write(file_name="cavitation_model.cas.h5", file_type="case")

###############################################################################
# Post Processing
# ~~~~~~~~~~~~~~~
