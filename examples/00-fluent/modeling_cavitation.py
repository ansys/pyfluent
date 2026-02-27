# /// script
# dependencies = [
#   "ansys-fluent-core",
# ]
# ///

# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
# Launch Fluent
# ~~~~~~~~~~~~~
# Perform required imports, which includes downloading and importing
# the geometry file.

# sphinx_gallery_thumbnail_path = '_static/cavitation_model_thumb.png'

from pathlib import Path

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.core.solver import (
    Contour,
    Controls,
    FluidMaterial,
    General,
    Graphics,
    Initialization,
    Methods,
    Models,
    PressureInlet,
    PressureOutlet,
    Residual,
    RunCalculation,    git apply --check -p1 C:\ANSYSDev\pyfluent\the-patch.utf8.diff    git apply --check -p1 C:\ANSYSDev\pyfluent\the-patch.utf8.diff    Get-Content C:\ANSYSDev\pyfluent\patch.patch -TotalCount 60    Get-Content C:\ANSYSDev\pyfluent\patch.patch -TotalCount 60write_case_data
)
from ansys.units import VariableCatalog
from ansys.units.common import Pa, kg, m, s

cav_file = examples.download_file(
    "cav.msh.gz", "pyfluent/cavitation", save_path=Path.cwd()
)


###############################################################################
# Launch a Fluent session in the 2d solution mode with double precision running
# on four processors and print Fluent version.

solver = pyfluent.Solver.from_install(
    precision=pyfluent.Precision.DOUBLE,
    processor_count=4,
    dimension=2,
)
print(solver.get_fluent_version())

###############################################################################
# Read the mesh that was downloaded.

# Upload the downloaded mesh to the solver session so it's available
solver.settings.file.read_mesh(file_name=cav_file)

solver.settings.mesh.check()

###############################################################################
# Specify an axisymmetric model.

solver.settings.setup.general.solver.two_dim_space = "axisymmetric"

###############################################################################
# Enable the multiphase mixture model.

models = Models(solver)
models.multiphase.models = "mixture"

models.multiphase.mixture_parameters.slip_velocity_on = False
models.multiphase.vof_parameters.vof_formulation = "implicit"

###############################################################################
# Enable the k-ω SST turbulence model.

models.viscous.model = "k-omega"
models.viscous.k_omega_model = "sst"

###############################################################################
# Define materials
# ~~~~~~~~~~~~~~~~
# Create a material named water, using 1000 kg/m3 for density and 0.001 kg/m–s
# for viscosity. Then, copy water vapor properties from the database and modify
# the copy by changing the density to 0.02558 kg/m3 and the viscosity to
# 1.26e-06 kg/m–s.

water = FluidMaterial.create(solver, name="water")
water.density = 1000 * kg / m**3
water.viscosity = 0.001 * kg / (m * s)

# copy vapor from database then override properties
solver.settings.setup.materials.database.copy_by_name(type="fluid", name="water-vapor")
water_vapor = FluidMaterial.get(solver, name="water-vapor")
water_vapor.density = 0.02558 * kg / m**3
water_vapor.viscosity = 1.26e-06 * kg / (m * s)

###############################################################################
# Phases
# ~~~~~~
# Change the name of the primary phase to "liquid" and the secondary phase to
# "water-vapor". Then, enable the cavitation model and set the number of mass
# transfer mechanisms to 1. Finally, specify cavitation as a mass transfer
# mechanism occurring from the liquid to the vapor.

# TODO fix
primary_phase = solver.setup.models.multiphase.phases["phase-1"]
primary_phase.name = "liquid"
primary_phase.material = water.name
secondary_phase = solver.setup.models.multiphase.phases["phase-2"]
secondary_phase.name = "vapor"
secondary_phase.material = water_vapor.name

# solver.settings.setup.models.multiphase.phase_interaction.mass_transfer_list.
solver.tui.define.phases.set_domain_properties.interaction_domain.heat_mass_reactions.mass_transfer(
    1, "liquid", "vapor", "cavitation", "1", "no", "no", "no"
)

###############################################################################
# Boundary Conditions
# ~~~~~~~~~~~~~~~~~~~
# For the first inlet momentum boundary conditions set the direction
# specification method to 'normal to boundary', gauge total pressure as 500 kPa
# and supersonic or initial gauge pressure as 449 kPa.
#
# For the turbulence settings choose 'Intensity and Viscosity Ratio' for
# turbulent specification. Set turbulent intensity and turbulent viscosity
# ratio to 0.05 and 10 respectively.

inlets = PressureInlet.get(solver, name="inlet_*")
inlets.momentum.gauge_total_pressure = 500_000 * Pa
inlets.momentum.supersonic_or_initial_gauge_pressure = 449_000 * Pa
inlets.momentum.direction_specification_method = "Normal to Boundary"
inlets.turbulence.turbulent_specification = "Intensity and Viscosity Ratio"
inlets.turbulence.turbulent_intensity = 0.05
inlets.turbulence.turbulent_viscosity_ratio = 10
# Set volume fraction of vapor phase to 0 for the inlets
inlets.multiphase.volume_fraction = 0

###############################################################################
# For the outlet boundary conditions, set the gauge pressure as 95 kPa. Use
# the same turbulence and volume fraction settings as the inlets.

outlet = PressureOutlet.get(solver, name="outlet")
outlet.momentum.gauge_pressure = 95_000 * Pa
outlet.turbulence.turbulent_specification = "Intensity and Viscosity Ratio"
outlet.turbulence.turbulent_intensity = 0.04
outlet.turbulence.turbulent_viscosity_ratio = 10
outlet.multiphase.volume_fraction = 0


###############################################################################
# Operating Conditions
# ~~~~~~~~~~~~~~~~~~~~
# Set the operating pressure to 0.

general = General(solver)
general.operating_conditions.operating_pressure = 0 * Pa

###############################################################################
# Solution
# ~~~~~~~~
# To configure the discretization scheme, set 'first order
# upwind' method for turbulent kinetic energy and turbulent dissipation rate, 'quick'
# for the momentum and volume fraction, and 'presto!' for pressure.

methods = Methods(solver)
discretization_scheme = methods.spatial_discretization.discretization_scheme
discretization_scheme["k"] = "first-order-upwind"
discretization_scheme["mom"] = "quick"
discretization_scheme["mp"] = "quick"
discretization_scheme["omega"] = "first-order-upwind"
discretization_scheme["pressure"] = "presto!"

# Pressure-velocity coupling and pseudo-time settings
methods.p_v_coupling.flow_scheme = "Coupled"
methods.pseudo_time_method.formulation.coupled_solver = "global-time-step"
methods.high_order_term_relaxation.enable = True
controls = Controls(solver)
controls.pseudo_time_explicit_relaxation_factor.global_dt_pseudo_relax["mp"] = 0.3

###############################################################################
# To plot the residuals, enable plotting and set the convergence criteria to
# 1e-05 for x-velocity, y-velocity, k, omega, and vf-vapor. Enable the specified
# initial pressure then initialize the solution with hybrid initialization.

equations = Residual(solver).equations
equations["continuity"].absolute_criteria = 1e-5
equations["x-velocity"].absolute_criteria = 1e-5
equations["y-velocity"].absolute_criteria = 1e-5
equations["k"].absolute_criteria = 1e-5
equations["omega"].absolute_criteria = 1e-5
equations["vf-vapor"].absolute_criteria = 1e-5

initialization = Initialization(solver)
initialization.initialization_type = "hybrid"
initialization.hybrid_init_options.general_settings.initial_pressure = True
initialization.hybrid_initialize()

###############################################################################
# Save and Run
# ~~~~~~~~~~~~
# Save the case file 'cav.cas.h5'. Then, start the calculation by requesting
# 500 iterations. Save the final case file and the data.

# Write the initial case file
write_case(file_name="cav.cas.h5")

# Run calculation using typed RunCalculation
RunCalculation(solver).iterate(iter_count=500)

# Write final case and data (file API retained)
write_case_data(file_name="cav.cas.h5")

###############################################################################
# Post Processing
# ~~~~~~~~~~~~~~~
# Since Fluent is being run without the GUI, we will need to export plots as
# picture files. Edit the picture settings to use a custom resolution so that
# the images are large enough.

graphics = Graphics(solver)
# use_window_resolution option not active inside containers or Ansys Lab environment
if graphics.picture.use_window_resolution.is_active():
    graphics.picture.use_window_resolution = False

graphics.picture.x_resolution = 1920
graphics.picture.y_resolution = 1440

###############################################################################
# Create contour plots
# ~~~~~~~~~~~~~~~~~~~~
# Create a contour plot for static pressure, turbulent kinetic energy and the
# volume fraction of water vapor. For each plot enable banded coloring and
# filled option.

cont_static = Contour.create(
    solver, name="contour_static_pressure", field=VariableCatalog.PRESSURE, filled=True
)
cont_static.coloring.option = "banded"
cont_static.coloring.smooth = False


###############################################################################
# Mirror the display around the symmetry plane to show the full model.

Graphics(solver).views.mirror_zones = ["symm_2", "symm_1"]

cont_static.display()

graphics.picture.save_picture(file_name="contour_static_pressure.png")

###############################################################################
# .. image:: /_static/cavitation_model_012.png
#   :width: 500pt
#   :align: center

cont_tke = Contour.create(
    solver,
    name="contour_tke",
    field=VariableCatalog.TURBULENT_KINETIC_ENERGY,
    filled=True,
)
cont_tke.coloring.option = "banded"
cont_tke.coloring.smooth = False
cont_tke.display()

graphics.picture.save_picture(file_name="contour_tke.png")

###############################################################################
# .. image:: /_static/cavitation_model_011.png
#   :width: 500pt
#   :align: center

cont_vf = Contour.create(
    solver,
    name="contour_vf_vapor",
    field=VariableCatalog.fluent.VOLUME_FRACTION_SECONDARY_PHASE,
    filled=True,
)
cont_vf.coloring.option = "banded"
cont_vf.coloring.smooth = False
cont_vf.display()

graphics.picture.save_picture(file_name="contour_vf_vapor.png")

###############################################################################
# .. image:: /_static/cavitation_model.png
#   :width: 500pt
#   :align: center

# Save case to 'cav.cas.h5' and exit

write_case(file_name="cav.cas.h5")  # noqa: F821

solver.exit()
