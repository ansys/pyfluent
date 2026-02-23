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

""".. _lid_driven_cavity_simulation:

Lid Driven Flow in a Cavity
---------------------------
"""
# %%
# Objective:
# ----------
#
# This PyFluent simulation investigates the classical lid-driven cavity flow,
# a benchmark problem in computational fluid dynamics. The domain consists of
# a square cavity filled with an incompressible fluid, where the top wall moves
# at a constant velocity while the remaining walls are stationary.
# The motion of the lid drives the flow inside the cavity, producing a
# primary vortex and secondary corner vortices due to viscous effects and no-slip
# boundary conditions. This problem is widely used to validate CFD solvers because
# it combines simple geometry with complex flow physics governed by the incompressible
# Navier–Stokes equations. Through this simulation, we analyze vortex formation and velocity distribution.
#
# Problem Description
# -------------------
#
# This simulation models a lid-driven cavity flow with the following
# configuration:
#
# - **Square cavity (1 m × 1 m)**: Completely filled with water
# - **Stationary walls**: Left, right, and bottom walls are fixed with no-slip conditions
# - **Moving top lid**: Translates horizontally at a constant velocity of **0.01 m/s**
#
# The PyFluent analysis focuses on:
#
# - Velocity vector distributions inside the cavity
# - Formation of the primary vortex at the cavity center
# - Development of secondary vortices near the bottom corners
# - Velocity variation along the horizontal centerline
#
# .. image:: ../../_static/lid_driven_cavity_1.png
#    :align: center
#    :alt: Schematic of lid-driven cavity geometry

# %%
# Import modules
# ^^^^^^^^^^^^^^

import os

import ansys.fluent.core as pyfluent
from ansys.fluent.core import Dimension, Precision, examples
from ansys.fluent.core.solver import (
    FluidCellZones,
    General,
    Graphics,
    Initialization,
    LineSurfaces,
    Materials,
    Methods,
    Residual,
    RunCalculation,
    Vector,
    Viscous,
    WallBoundaries,
)
from ansys.fluent.visualization import GraphicsWindow, XYPlot

# %%
# Launch Fluent
# ^^^^^^^^^^^^^

solver = pyfluent.launch_fluent(
    precision=Precision.DOUBLE,
    dimension=Dimension.TWO,
    mode=pyfluent.FluentMode.SOLVER,
)

# %%
# Read mesh
# ^^^^^^^^^

mesh_file = examples.download_file(
    "lid_driven_cavity.msh",
    "pyfluent/lid_driven_cavity",
    save_path=os.getcwd(),
)

solver.file.read(file_type="mesh", file_name=mesh_file)

# %%
# Viscous Model
# ^^^^^^^^^^^^^

viscous = Viscous(solver)

viscous.model = viscous.model.LAMINAR

# %%
# General settings
# ^^^^^^^^^^^^^^^^

g = 9.81  # m/s²
general_settings = General(solver)

general_settings.operating_conditions.gravity.enable = True
general_settings.operating_conditions.gravity.components = [0.0, -g, 0.0]

# %%
# Material definition
# ^^^^^^^^^^^^^^^^^^^

# %%
# Since the cavity is completely filled with water, the working fluid is defined
# as water liquid. The material properties are imported directly from the solver’s
# material database and applied to the fluid cell zone to ensure
# accurate density and viscosity representation.

# %%
materials = Materials(solver)
fluid = FluidCellZones(solver)

materials.database.copy_by_name(name="water-liquid", type="fluid")

fluid["surface_body"].general.material = "water-liquid"

# %%
# Boundary conditions
# ^^^^^^^^^^^^^^^^^^^
# Define the top wall as a moving lid with velocity 0.01 m/s
wall_boundary = WallBoundaries(solver)

wall_boundary["top_moving_wall"] = {
    "momentum": {"wall_motion": "Moving Wall", "speed": {"value": 0.01}}  # m/s
}
# Other walls remain stationary

# %%
# Solution methods
# ^^^^^^^^^^^^^^^^

solution_methods = Methods(solver)

solution_methods.p_v_coupling.flow_scheme = "SIMPLEC"
solution_methods.spatial_discretization = {
    "gradient_scheme": "green-gauss-cell-based",
}

# %%
# Residual convergence criteria
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# %%
# Reason for choosing 1e-6:
#
# - Ensures that the numerical solution satisfies the governing equations to a high degree of accuracy.
# - Reduces numerical errors in velocity and pressure fields.
# - Helps capture delicate flow features, such as primary and secondary vortices in the cavity.

# %%
monitor_residuals = Residual(solver)

monitor_residuals.equations = {
    eqn: {"absolute_criteria": 1e-6}
    for eqn in (
        "continuity",
        "x-velocity",
        "y-velocity",
    )
}

# %%
# Initialize and solve
# --------------------

solution_initialization = Initialization(solver)

solution_initialization.initialization_type = "hybrid"
solution_initialization.initialize()

# %%
# For this simulation, the prescribed convergence criterion of **1e-6**,
# the residuals stabilize after approximately **1000 iterations**,
# indicating that the governing equations are satisfied to the desired level of accuracy.
# Continuing the calculation up to **1500 iterations** provides an additional safety margin,
# ensuring that numerical errors in the velocity and pressure fields are minimized

# %%
calculation = RunCalculation(solver)
calculation.iterate(iter_count=1500)

# %%
# Post-processing
# ---------------

vector = Vector(solver, new_instance_name="velocity-magnitude-vector")
graphics = Graphics(solver)

# Define image resolution as named constants to improve maintainability.
# Updating these values will automatically apply to all image save operations.
image_width = 650
image_height = 450

graphics.picture.x_resolution = image_width
graphics.picture.y_resolution = image_height

vector.vector_field = "velocity"
vector.surfaces_list = [
    "bottom_wall",
    "top_moving_wall",
    "interior-surface_body",
    "stationary_side_wall",
]
vector.options.vector_style = "arrow"
vector.options.scale = 0.02  # Scale factor for visibility
vector.vector_opt.fixed_length = True  # Uniform arrow length
vector.display()

graphics.picture.save_picture(file_name="lid_driven_cavity_2.png")

# %%
# .. image:: ../../_static/lid_driven_cavity_2.png
#    :align: center
#    :alt: velocity vector

# %%
# Create horizontal centerline
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^

line_surfaces = LineSurfaces(solver)

line_surfaces.create()
line_surfaces["line-1"] = {
    "p0": [0, 0.5, 0],
    "p1": [1, 0.5, 0],
}

# %%
# Plot velocity magnitude along centerline
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

xy_plot = XYPlot(
    solver=solver,
    surfaces=["line-1"],
    y_axis_function="velocity-magnitude",
)
plot_window = GraphicsWindow()
plot_window.add_plot(xy_plot, position=(0, 0), title="velocity along center line")
plot_window.show()

# %%
# .. image:: ../../_static/lid_driven_cavity_3.png
#    :align: center
#    :alt: velocity magnitude at centerline

# %%
# Save case and data
# ------------------

solver.settings.file.write_case_data(file_name="lid_driven_cavity_case_data")

# %%
# Close session
# -------------

solver.exit()

# %%
# Discussion
# ----------
#
# The lid-driven cavity simulation successfully captures the fundamental
# flow physics associated with shear-driven recirculating flows.
# The motion of the top lid induces shear at the fluid–wall interface,
# transferring momentum into the cavity and generating a dominant recirculating motion within the fluid domain.
#
# The velocity vector plot shows a dominant **primary vortex** at the center of the
# cavity, driven by the motion of the top lid. Fluid moves in the direction of the
# lid near the top boundary and recirculates downward along the sidewalls, which is
# characteristic of lid-driven cavity flow at low Reynolds numbers. Reduced velocity
# magnitudes are observed near the stationary walls due to the **no-slip boundary condition**,
# where the fluid velocity approaches zero. The vector field also reveals **secondary vortices**
# near the bottom corners, formed due to viscous effects and local pressure gradients caused by
# interaction with the stationary walls. Overall, the flow remains smooth,
# symmetric, and indicative of a steady laminar regime.
#
# The velocity variation along the horizontal centerline provides quantitative
# insight into the internal flow structure. The velocity component along this
# line shows both positive and negative values, indicating upward and downward
# motions associated with the recirculating flow within the cavity.

# sphinx_gallery_thumbnail_path = '_static/lid_driven_cavity_1.png'
