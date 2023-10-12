"""

Modeling Cavitation
-------------------
This example examines the pressure-driven cavitating flow of water through a
sharp-edged orifice. This is a typical configuration in fuel injectors, and
brings a challenge to the physics and numerics of cavitation models because of
the high pressure differentials involved and the high ratio of liquid to vapor
density.

This example uses the multiphase modeling capability of Ansys Fluent, and will
be able to predict the strong cavitation near the orifice after flow separation
at a sharp edge.

**Workflow tasks**

This example demonstrates how to do the following:

- Set boundary conditions for internal flow
- Use the mixture model with cavitation effects
- Calculate a solution using the pressure-based coupled solver

**Problem description**

The problem considers the cavitation caused by the flow separation after a
sharp-edged orifice. The flow is pressure driven, with an inlet pressure of 500
kPa and an outlet pressure of 95 kPa. The orifice diameter is 4 mm, and the
geometrical parameters of the orifice are D/d = 2.88 and L/d = 4, where D, d,
and L are the inlet diameter, orifice diameter, and orifice length respectively.
"""

###############################################################################
# Example Setup
# -------------
# Before you can begin, you must set up the example and initialize this
# workflow.
#
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Perform required imports, which includes downloading and importing
# the geometry file.

# sphinx_gallery_thumbnail_path = '_static/cavitation_model_thumb.png'
import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples

cav_file = examples.download_file(
    "cav.msh", "pyfluent/cavitation", save_path=pyfluent.EXAMPLES_PATH
)

###############################################################################
# Launch Fluent
# ~~~~~~~~~~~~~
# Launch Fluent as a service in 2d solution mode with double precision running
# on one processor.

solver = pyfluent.launch_fluent(
    precision="double",
    processor_count=4,
    mode="solver",
    version="2d",
)

###############################################################################
# Read and Check the Mesh
# ~~~~~~~~~~~~~~~~~~~~~~~
solver.read_case("cav.msh")

solver.mesh.check()

###############################################################################
# Specify an axisymmetric model
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

solver.setup.general.solver.two_dim_space = "axisymmetric"

###############################################################################
# Enable the multiphase mixture model
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

solver.setup.models.multiphase.models = "mixture"

solver.tui.define.models.multiphase.mixture_parameters("no", "implicit")

###############################################################################
# Select turbulence model
# ~~~~~~~~~~~~~~~~~~~~~~~
# Enable the k-ω SST turbulence model.

solver.setup.models.viscous = {"model": "k-omega", "k_omega_model": "sst"}

###############################################################################
# Define materials
# ~~~~~~~~~~~~~~~~
# Create a material named water, using 1000 kg/m3 for density and 0.001 kg/m–s
# for viscosity. Then, copy water vapor properties from the database and modify the copy by changing
# the density to 0.02558 kg/m3 and the viscosity to 1.26e-06 kg/m–s.

water = {
    "density": {"option": "constant", "value": 1000},
    "viscosity": {"option": "constant", "value": 0.001},
}

solver.setup.materials.fluid["water"] = water

solver.setup.materials.database.copy_by_name(type="fluid", name="water-vapor")

water_vapor = {"density": {"value": 0.02558}, "viscosity": {"value": 1.26e-06}}

solver.setup.materials.fluid["water-vapor"] = water_vapor

###############################################################################
# Phases
# ~~~~~~
# Change the name of the primary phase to "liquid" and the secondary phase to "water-vapor".
# Then, enable the cavitation model and set the number of mass
# transfer mechanisms to 1. Finally, specify cavitation as a mass transfer mechanism 
# occurring from the liquid to the vapor.

solver.tui.define.phases.set_domain_properties.change_phases_names("vapor", "liquid")

solver.tui.define.phases.set_domain_properties.phase_domains.liquid.material(
    "yes", "water"
)

solver.tui.define.phases.set_domain_properties.phase_domains.vapor.material(
    "yes", "water-vapor"
)

solver.tui.define.phases.set_domain_properties.interaction_domain.heat_mass_reactions.mass_transfer(
    1, "liquid", "vapor", "cavitation", "1", "no", "no", "no"
)

###############################################################################
# Boundary Conditions
# ~~~~~~~~~~~~~~~~~~~

# Set momentum and turbulence boundary conditions for the first inlet then copy
# to the second inlet. Set the direction specification method to 'normal to
# boundary', gauge total pressure as 500 kPa and supersonic or initial gauge
# pressure as 449 kPa. Set turbulent intensity as 0.05, turbulent specification
# to 'Intensity and Viscosity Ratio' and turbulent viscosity ratio as 10. Set
# the vapor phase volume fraction as 0. Apply the outlet boundary conditions.
# Set the gauge pressure as 95 kPa. Use the same turbulence and volume fraction
# settings as the inlets.

inlet_1 = solver.setup.boundary_conditions.pressure_inlet["inlet_1"].phase

in_mixture = {
    "direction_spec": "Normal to Boundary",
    "gauge_total_pressure": {"value": 500000},
    "gauge_pressure": {"value": 449000},
    "turb_intensity": 0.05,
    "ke_spec": "Intensity and Viscosity Ratio",
    "turb_viscosity_ratio": 10,
}
inlet_1["mixture"] = in_mixture

inlet_1["vapor"] = {"volume_fraction": {"value": 0}}

solver.setup.boundary_conditions.copy(from_="inlet_1", to="inlet_2")

outlet = solver.setup.boundary_conditions.pressure_outlet["outlet"].phase

out_mixture = {
    "gauge_pressure": {"value": 95000},
    "turb_intensity": 0.05,
    "ke_spec": "Intensity and Viscosity Ratio",
    "turb_viscosity_ratio": 10,
}

outlet["mixture"] = out_mixture

outlet["vapor"] = {"volume_fraction": {"value": 0}}

###############################################################################
# Operating Conditions
# ~~~~~~~~~~~~~~~~~~~~
# Set the operating pressure as 0.

solver.setup.general.operating_conditions.operating_pressure = 0

###############################################################################
# Solution
# ~~~~~~~~
# Apply the methods parameters. For the discretization scheme, set 'first order
# upwind' for turbulent kinetic energy and turbulent dissipation rate, 'quick'
# for the momentum and volume fraction and 'presto!' for pressure. Set the
# pseudo time method to 'global time step' then Enable 'High Order Term
# Relaxation'. Set the pseudo time explicit relaxation factor for 'Volume
# Fraction' to 0.3. Enable plotting of residuals and set the convergence
# criteria to 1e-05 for x-velocity, y-velocity, k, omega, and vf-vapor. Enable
# the specified initial pressure and initialize the solution with hybrid
# initialization.

methods = solver.solution.methods

discretization_scheme = {
    "k": "first-order-upwind",
    "mom": "quick",
    "mp": "quick",
    "omega": "first-order-upwind",
    "pressure": "presto!",
}

methods.discretization_scheme = discretization_scheme

methods.p_v_coupling.flow_scheme = "Coupled"

methods.pseudo_time_method.formulation.coupled_solver = "global-time-step"

methods.high_order_term_relaxation.enable = True

solver.solution.controls.pseudo_time_explicit_relaxation_factor.global_dt_pseudo_relax[
    "mp"
] = 0.3

solver.tui.solve.monitors.residual.plot("yes")

solver.tui.solve.monitors.residual.convergence_criteria(
    1e-05, 1e-05, 1e-05, 1e-05, 1e-05, 1e-05
)

solver.solution.initialization.hybrid_init_options.general_settings.initial_pressure = (
    True
)

solver.solution.initialization.hybrid_initialize()

###############################################################################
# Save and Run
# ~~~~~~~~~~~~
# Save the case file 'cav.cas.h5'. Then start the calculation by requesting
# 500 iterations. Save the final case file and the data.

solver.file.write(file_name="cav", file_type="case")

solver.solution.run_calculation.iterate(iter_count=500)

solver.file.write(file_name="cav", file_type="case-data")

###############################################################################
# Post Processing
# ~~~~~~~~~~~~~~~
# Create a contour plot for static pressure, turbulent kinetic energy and the
# volume fraction of water vapor. for each plot enable banded coloring and
# filled. Mirror the display around the symmetry plane to show the full model.

solver.results.graphics.contour.create("contour_static_pressure")

contour_static_pressure = {
    "coloring": {"option": "banded", "smooth": False},
    "field": "pressure",
    "filled": True,
}

solver.results.graphics.contour["contour_static_pressure"] = contour_static_pressure

solver.tui.display.set.mirror_zones(["symm_2", "symm_1"])

###############################################################################
# .. image:: /_static/cavitation_model_012.png
#   :width: 500pt
#   :align: center

solver.results.graphics.contour.create("contour_tke")

contour_tke = {
    "coloring": {"option": "banded", "smooth": False},
    "field": "turb-kinetic-energy",
    "filled": True,
}

solver.results.graphics.contour["contour_tke"] = contour_tke

###############################################################################
# .. image:: /_static/cavitation_model_011.png
#   :width: 500pt
#   :align: center

solver.results.graphics.contour.create("contour_vf_vapor")

contour_vf_vapor = {
    "coloring": {"option": "banded", "smooth": False},
    "field": "vapor-vof",
    "filled": True,
}

solver.results.graphics.contour["contour_vf_vapor"] = contour_vf_vapor

###############################################################################
# .. image:: /_static/cavitation_model.png
#   :width: 500pt
#   :align: center

###############################################################################
# Save and Exit
# ~~~~~~~~~~~~~

solver.file.write(file_name="cav", file_type="case")

solver.exit()
