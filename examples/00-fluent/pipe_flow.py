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

""".. _flow_through_pipe:

Flow of oil in a pipe through a lake
=====================================
"""

# %%
# Objective
# ---------
#
# The primary objective of this study is to simulate **thermal energy transport**
# in a circular pipe subjected to a constant wall temperature boundary condition.
# The simulation represents oil flowing through a horizontal pipeline submerged in
# icy lake water, where the surrounding cold environment maintains the pipe wall
# at a uniform temperature. The analysis focuses on predicting the oil temperature
# at the pipe exit after heat loss to the cold surroundings over the submerged
# pipe length.
#
# The numerical results are validated against the analytical solution, demonstrating
# the use of PyFluent as a verification and validation tool for classical
# internal-flow heat-transfer problems.
#
# Problem Description
# -------------------
#
# This simulation models the internal flow of oil through a horizontal circular
# pipeline exposed to icy lake conditions. A 200-m-long section of the pipe passes
# through lake water at 0°C. Due to the cold surroundings, measurements indicate
# that the outer and inner pipe wall temperatures are very nearly uniform at 0°C.
# The oil enters the lake section fully developed at a higher temperature and
# undergoes convective cooling as it flows downstream.
#
# **Configuration:**
#
# - **Pipe diameter:** 0.3 m
# - **Pipe length:** 200 m
# - **Inlet velocity:** 2 m/s
# - **Inlet temperature:** 20°C (293.15 K)
# - **Wall temperature:** 0°C (273.15 K)
#
# **Assumptions:**
#
# - Steady operating conditions
# - Thermal resistance of pipe material is negligible
# - Inner surfaces of pipeline are smooth
# - Flow is hydrodynamically developed when entering the lake section
#
# **Oil Properties at 20°C:**
#
# - Density (ρ): 888.1 kg/m³
# - Kinematic viscosity (ν): 0.0009429 m²/s
# - Specific heat (cp): 1880 J/kg·K
# - Thermal conductivity (k): 0.145 W/m·K
# - Prandtl number (Pr): 10863
#
# **Reynolds Number:**
#
# .. math::
#
#    Re = \frac{V D}{\nu} = \frac{(2 \text{ m/s})(0.3 \text{ m})}{9.429 \times 10^{-4} \text{ m}^2/\text{s}} = 636
#
# Since Re < 2300, the flow is laminar.
#
# .. image:: ../../_static/pipe_flow_1.png
#    :align: center
#    :alt: Schematic of pipe flow through lake

# %%
# Import modules
# --------------

import os

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.core.solver import (
    Energy,
    FluidMaterials,
    Initialization,
    LineSurfaces,
    RunCalculation,
    VelocityInlets,
    Viscous,
    WallBoundaries,
)
from ansys.fluent.visualization import GraphicsWindow, Monitor, XYPlot

# %%
# Launch Fluent in solver mode
# -----------------------------

solver = pyfluent.launch_fluent(
    precision=pyfluent.Precision.DOUBLE,
    mode=pyfluent.FluentMode.SOLVER,
    dimension=pyfluent.Dimension.TWO,
)

# %%
# Read mesh
# ---------

mesh_file = examples.download_file(
    "flow_through_pipe.msh",
    "pyfluent/flow_through_pipe",
    save_path=os.getcwd(),
)

solver.settings.file.read_mesh(file_name=mesh_file)

# %%
# Setup
# -----
#
# Configure the simulation settings including turbulence model, boundary conditions,
# and solution methods.
#
# Viscous Model
# ^^^^^^^^^^^^^

viscous = Viscous(solver)
viscous.model = viscous.model.LAMINAR

# %%
# Energy model
# ^^^^^^^^^^^^

energy_model = Energy(solver)
energy_model.enabled = True

# %%
# Materials
# ^^^^^^^^^

fluid_materials = FluidMaterials(solver)

fluid_materials.rename(new="oil", old="air")
fluid_materials["oil"] = {
    "density": 888.1,
    "viscosity": 0.0009429,
    "specific_heat": 1880,
    "thermal_conductivity": 0.145,
}

# %%
# Boundary Conditions
# ^^^^^^^^^^^^^^^^^^^
#
# Inlet velocity boundary
# ^^^^^^^^^^^^^^^^^^^^^^^

inlet_velocity_boundary = VelocityInlets(solver)

inlet_velocity_boundary["inlet"] = {
    "momentum": {"velocity_magnitude": 2},
    "thermal": {"temperature": 293.15},
}

# %%
# Wall boundary
# ^^^^^^^^^^^^^

wall_boundary = WallBoundaries(solver)

wall_boundary["wall"] = {
    "thermal": {"thermal_condition": "Temperature", "temperature": 273.15}
}

# %%
# Initialize and run
# ^^^^^^^^^^^^^^^^^^

solution_initialization = Initialization(solver)
solution_initialization.initialization_type = "hybrid"
solution_initialization.initialize()

calculation = RunCalculation(solver)
calculation.iterate(iter_count=300)

# %%
# The solver was allowed to run for up to 300 iterations.
# The solution converged after 146 iterations, as residuals
# stabilized and key flow variables no longer changed so the solution terminated automatically.

# %%
# Results
# -------
#
# Create line surface for temperature profile
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

line_surface = LineSurfaces(solver)

line_surface["line"] = {"p0": [0, 0.15, 0], "p1": [200, 0.15, 0]}

# %%
# Plot temperature distribution along the pipe
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

plot_window = GraphicsWindow()

xy_plot_object = XYPlot(
    solver=solver,
    surfaces=["line"],
    y_axis_function="temperature",
)
plot_window.add_plot(
    xy_plot_object, position=(0, 0), title="Temperature along the pipe"
)

residual = Monitor(solver=solver, monitor_set_name="residual")
plot_window.add_plot(residual, position=(0, 1))

plot_window.show()

# %%
# .. image:: ../../_static/pipe_flow_2.png
#    :align: center
#    :alt: temperature profile along center line

# %%
# Close session
# -------------

solver.exit()


# %%
# Numerical Validation
# ====================
#
# Analytical Solution
# -------------------
#
# The problem can be validated against analytical solutions for thermally developing
# laminar flow in pipes with constant wall temperature.
#
#
# **Thermal Entry Length:**
#
# For laminar flow with high Prandtl number:
#
# .. math::
#
#    L_t \approx 0.05 \, Re \, Pr \, D = 0.05 \times 636 \times 10863 \times 0.3 \approx 103{,}600 \text{ m}
#
# This is much greater than the pipe length (200 m), confirming thermally developing flow.
#
# **Nusselt Number:**
#
# For thermally developing laminar flow:
#
# .. math::
#
#    Nu = 3.66 + \frac{0.065 (D/L) Re \, Pr}{1 + 0.04 [(D/L) Re \, Pr]^{2/3}}
#
# .. math::
#
#    Nu = 3.66 + \frac{0.065(0.3/200) \times 636 \times 10{,}863}{1 + 0.04[(0.3/200) \times 636 \times 10{,}863]^{2/3}} = 33.7
#
# **Heat Transfer Coefficient:**
#
# .. math::
#
#    h = \frac{k \, Nu}{D} = \frac{0.145 \times 33.7}{0.3} = 16.3 \text{ W/m}^2\text{·K}
#
# **Exit Temperature:**
#
# Using energy balance for constant wall temperature:
#
# .. math::
#
#    T_e = T_s - (T_s - T_i) \exp\left(-\frac{h A_s}{\dot{m} c_p}\right)
#
# Where:
#
# - :math:`A_s = \pi D L = \pi (0.3)(200) = 188.5 \text{ m}^2`
# - :math:`\dot{m} = \rho A_c V = 888 \times \frac{\pi}{4}(0.3)^2 \times 2 = 125.6 \text{ kg/s}`
#
# .. math::
#
#    T_e = 273.15 - (273.15 - 293.15) \exp\left(-\frac{16.3 \times 188.5}{125.6 \times 1880}\right) = 292.89 \text{ K} \, (19.74°\text{C})
#
# Discussion
# ----------
#
# This example validates PyFluent's capability to accurately simulate conjugate heat transfer
# problems involving high-Prandtl-number fluids in thermally developing flow regimes.
# The PyFluent simulation was compared with the analytical solution for thermally developing laminar flow in a pipe with constant wall temperature.
#
# Analytical outlet temperature: :T_e = 292.74 K
#
# PyFluent outlet temperature: :T_e = 291.79 K
#
# Both approaches show only a small temperature drop over the 200-m pipe, consistent with the very long thermal entry length.

# sphinx_gallery_thumbnail_path = '_static/pipe_flow_1.png'
