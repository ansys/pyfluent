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

""".. _Solidification_Simulation:

Modeling Solidification
-----------------------
"""

# %%
# Objective
# ---------
#
# This example models solidification in a Czochralski
# crystal growth process using PyFluent. The simulation involves setting
# up a two-dimensional axisymmetric swirl configuration with gravity and
# activating the Solidification and Melting model to capture phase change
# behavior. Pull velocities are applied to represent continuous casting,
# while Marangoni convection is incorporated through a surface tension
# gradient at the melt surface. The workflow begins with a steady state
# conduction solution to establish a realistic initial thermal field.
# Subsequently, transient flow and heat transfer are enabled to capture
# the combined effects of natural and Marangoni convection. To achieve
# this, custom field functions and patching techniques are employed for
# efficient definition of pull velocities and initialization of the
# simulation.

# %%
# Problem Description
# -------------------
#
# The problem involves simulating a two-dimensional axisymmetric bowl
# containing liquid metal. The liquid enters from the bottom at a
# temperature of 1300 K, while solidified material is continuously
# pulled from the top at a rate of 0.001 m/s. The crystal undergoes
# rotation at an angular velocity of 1 rad/s, which induces a
# swirling flow within the melt. Heat loss from the upper region
# of the crystal promotes solidification of the liquid metal.
# Additionally, Marangoni convection develops at the free surface
# due to temperature-dependent variations in surface tension.
# The solidification process is modeled with zero mushy zone width,
# where both the solidus and liquidus temperatures are 1150 K.
# The flow incorporates an axial pull velocity of 0.001 m/s and
# a swirl velocity defined by ω × r, with ω = 1 rad/s.
# The surface tension gradient responsible for Marangoni stress
# is given by dσ/dT = –0.00036 N/m·K, and gravity acts in the
# axial (X) direction with a magnitude of –9.81 m/s².
#
# .. image:: ../../_static/modeling_solidification.png
#    :align: center
#    :alt: Solidification in Czochralski Model

# %%
# Import modules
# --------------
#
# .. note::
#   Importing the following classes offer streamlined access to key solver settings,
#   eliminating the need to manually browse through the full settings structure.

from pathlib import Path

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.core.solver import (
    BoundaryCondition,
    Contour,
    Controls,
    FluidCellZone,
    write_case_data,
    FluidMaterial,
    General,
    Graphics,
    Initialization,
    Materials,
    Mesh,
    Methods,
    Results,
    RunCalculation,
    Setup,
    Solution,
    VelocityInlet,
    WallBoundary,
    Models,
)
from ansys.units import VariableCatalog
from ansys.units.common import J, K, N, Pa, W, kg, m, radian, s

# %%
# Launch Fluent session in solver mode
# ------------------------------------
solver = pyfluent.Solver.from_install(
    precision=pyfluent.Precision.DOUBLE,
    dimension=pyfluent.Dimension.TWO,
    fluent_path=r"C:\ANSYSDev\v261\fluent\ntbin\win64\fluent.exe",
)

# %%
# Download mesh file
# ------------------
mesh_file = examples.download_file(
    "solid.msh",
    "pyfluent/solidification",
    save_path=Path.cwd(),
)

solver.settings.file.read_mesh(file_name=mesh_file)

# %%
# Display mesh
# ------------
graphics = Graphics(solver)
mesh = Mesh.create(solver)

graphics.picture.x_resolution = 650  # Horizontal resolution for clear visualization
graphics.picture.y_resolution = 450  # Vertical resolution matching typical aspect ratio

all_walls = mesh.surfaces_list.allowed_values()

mesh.surfaces_list = all_walls
mesh.options.edges = True
mesh.display()

# graphics.picture.save_picture(file_name="modeling_solidification_1.png")

# %%
# .. image:: ../../_static/modeling_solidification_1.png
#    :align: center
#    :alt: Mesh

# %%
# Configure solver
# ----------------
general = General(solver)

general.solver.two_dim_space = "swirl"

general.operating_conditions.gravity.enable = True
general.operating_conditions.gravity.components = [-9.81 * m / s**2]

# %%
# Enable models
# -------------
#
# .. note::
#   Energy is auto-enabled with solidification

setup = Setup(solver)

setup.models.viscous.model = "laminar"

solver.tui.define.models.solidification_melting(
    "yes",  # Enable Solidification/Melting model
    "constant",  # Mushy Zone Parameter
    "100000",  # Mushy Zone Constant
    "yes",  # Include Pull Velocities
    "no",  # Compute Pull Velocities
)

Models(solver)

# %%
# Define material
# ---------------
Materials(solver).database.copy_by_name(type="fluid", name="air", new_name="liquid-metal")

liquid_metal = FluidMaterial(
    solver,
    name="liquid-metal",
    viscosity=0.00553 * Pa * s,
    specific_heat=680.0 * J / kg / K,
    thermal_conductivity=30.0 * W / m / K,
    melting_heat=100000.0 * J / kg,
    tsolidus=1150.0 * K,
    tliqidus=1150.0 * K,
)
liquid_metal.density.option = "polynomial"
liquid_metal.density.polynomial.coefficients = [
    8000,
    -0.1,
]  # [Density (kg/m³), Linear temp coefficient (kg/(m³·K))]

# Assign material to fluid zone using a typed cell-zone object
fluid_zone = FluidCellZone.get(solver, name="fluid")
fluid_zone.general.material = liquid_metal

# %%
# Boundary conditions
# -------------------

# Inlet: liquid injection
inlet = VelocityInlet.get(solver, name="inlet")

inlet.momentum.velocity_magnitude = 0.00101 * m / s
inlet.thermal.temperature = 1300 * K

# Outlet: solid pull-out (velocity inlet with axial + swirl)
outlet = VelocityInlet.get(solver, name="outlet")

outlet.momentum.velocity_specification_method = "Components"
outlet.momentum.swirl_angular_velocity = 1 * radian / s
outlet.momentum.velocity_components = (0.001, 0, 0) * m / s  # axial, radial, tangential
outlet.thermal.temperature.value = 500 * K

# Bottom wall: fixed temperature
bottom_wall = WallBoundary.get(solver, name="bottom-wall")
bottom_wall.thermal.thermal_condition = (
    bottom_wall.thermal.thermal_condition.TEMPERATURE
)
bottom_wall.thermal.temperature = 1300 * K

# Free surface: Marangoni stress + convection
free_surface = WallBoundary.get(solver, name="free-surface")
free_surface.momentum.shear_condition = (
    free_surface.momentum.shear_condition.MARANGONI_STRESS
)
free_surface.momentum.surface_tension_gradient = -0.00036 * N / (m * K)
free_surface.thermal.thermal_condition = (
    free_surface.thermal.thermal_condition.CONVECTION
)
free_surface.thermal.convection.free_stream_temperature = 1500 * K
free_surface.thermal.convection.convective_heat_transfer_coefficient = (
    100 * W / (m**2 * K)
)

# Side wall: fixed temperature
side_wall = WallBoundary.get(solver, name="side-wall")
side_wall.thermal.thermal_condition = side_wall.thermal.thermal_condition.TEMPERATURE
side_wall.thermal.temperature = 1400 * K

# Solid wall: rotating + cold
solid_wall = WallBoundary.get(solver, name="solid-wall")
solid_wall.momentum.wall_motion = "Moving Wall"
solid_wall.momentum.velocity_spec = "Rotational"
solid_wall.momentum.rotation_speed = 1 * radian / s
solid_wall.thermal.thermal_condition = solid_wall.thermal.thermal_condition.TEMPERATURE
solid_wall.thermal.temperature = 500 * K

# %%
# Solution methods
# ----------------
methods = Methods(solver)

methods.p_v_coupling.flow_scheme = "Coupled"
methods.spatial_discretization.discretization_scheme["pressure"] = "presto!"
methods.pseudo_time_method.formulation.coupled_solver = "global-time-step"

# %%
# Disable flow equations
# ----------------------
controls = Controls(solver)

controls.equations["flow"] = False
controls.equations["w-swirl"] = False


# %%
# Initialize flow field
# ---------------------
initialize = Initialization(solver)
initialize.hybrid_initialize()

# %%
# Define custom field function
# ----------------------------
results = Results(solver)

omega_r = results.custom_field_functions.create(
    name="omegar",
    custom_field_function="1 * radial_coordinate",  # ω = 1 rad/s
)

# %%
# Patch pull velocities
# ---------------------

# Axial pull velocity = 0.001 m/s
initialize.patch.calculate_patch(
    cell_zones=["fluid"],
    variable="x-pull-velocity",
    reference_frame="Relative to Cell Zone",
    use_custom_field_function=True,
    custom_field_function_name=omega_r.name(),
    value=0.001,
)

# Swirl pull velocity = ω × r
initialize.patch.calculate_patch(
    cell_zones=["fluid"],
    variable="z-pull-velocity",
    reference_frame="Relative to Cell Zone",
    use_custom_field_function=True,
    custom_field_function_name=omega_r.name(),
)

# %%
# Pseudo-transient settings
# -------------------------
calculation = RunCalculation(solver)

calculation.pseudo_time_settings.time_step_method.time_step_method = "user-specified"
calculation.pseudo_time_settings.time_step_method.auto_time_size_calc_solid_zone = False


calculation.iterate(iter_count=20)

# %%
# Post-processing
# ---------------
temp_contour = Contour.create(
    solver, name="temperature_contour", field=VariableCatalog.TEMPERATURE
)
temp_contour.coloring.option = "banded"
temp_contour.display()

graphics.views.restore_view(view_name="front")
graphics.picture.save_picture(file_name="modeling_solidification_2.png")

# %%
# .. image:: ../../_static/modeling_solidification_2.png
#    :align: center
#    :alt: Temperature Contours


mushy_temp = Contour.create(
    solver, name="temperature-mushy", field=VariableCatalog.TEMPERATURE
)
mushy_temp.coloring.option = "banded"
# set explicit contour range
mushy_temp.range.option = "auto-range-off"
mushy_temp.range.auto_range_off.clip_to_range = True
mushy_temp.range.auto_range_off.minimum = 1100 * K
mushy_temp.range.auto_range_off.maximum = 1200 * K
mushy_temp.display()

graphics.views.restore_view(view_name="front")
graphics.picture.save_picture(file_name="modeling_solidification_3.png")

# %%
# .. image:: ../../_static/modeling_solidification_3.png
#    :align: center
#    :alt: Mushy Zone


# Save steady state case
write_case_data(file_name="steady_state")


# %%
# Enable transient flow and heat transfer
# ---------------------------------------
general.solver.time = "unsteady-1st-order"  # First-order implicit

controls.equations["flow"] = True
controls.equations["w-swirl"] = True

controls.under_relaxation["delh"] = 0.1

# %%
# Transient controls
# ------------------
solutions = Solution(solver)

solutions.run_calculation.transient_controls.time_step_count = 2
solutions.run_calculation.transient_controls.time_step_size = 0.1  # s
solutions.run_calculation.calculate()

# Liquid fraction at t = 0.2 s
liquid_fraction_contour = Contour.create(
    solver, name="liquid-fraction", field="liquid-fraction"
)
liquid_fraction_contour.display()

graphics.picture.save_picture(file_name="modeling_solidification_4.png")

# %%
# .. image:: ../../_static/modeling_solidification_4.png
#    :align: center
#    :alt: Liquid Fraction at t = 0.2 s

# Continue to t = 5.0 s (48 more steps)
solutions.run_calculation.transient_controls.time_step_count = 48

solutions.run_calculation.calculate()

# Liquid fraction at t = 5.0 s
liquid_fraction_contour_t_5_sec = Contour.create(
    solver, name="liquid-fraction", field="liquid-fraction"
)
liquid_fraction_contour_t_5_sec.display()

graphics.picture.save_picture(file_name="modeling_solidification_5.png")

# %%
# .. image:: ../../_static/modeling_solidification_5.png
#    :align: center
#    :alt: Liquid Fraction at t = 5 s

# Save transient case
write_case_data(file_name="unsteady_state")

# %%
# Close session
# -------------
solver.exit()

# %%
# Summary
# -------
#
# In this example, we used PyFluent to model solidification
# in a Czochralski crystal growth process. The workflow begins
# with a steady conduction solution to establish the initial
# thermal field, followed by transient flow to capture natural
# and Marangoni-driven convection. Pull velocities are applied
# through a custom field function (ω × r), and surface tension
# gradients define Marangoni effects. This approach is efficient,
# fully scriptable, and easily adaptable to other casting or
# crystal growth simulations.


# %%
# References:
# -----------
# [1] Modeling Solidification, `Ansys Fluent documentation​ <https://ansyshelp.ansys.com/public/account/secured?returnurl=/Views/Secured/corp/v252/en/flu_tg/x1-37700023.html>`_.

# sphinx_gallery_thumbnail_path = '_static/modeling_solidification_2.png'
