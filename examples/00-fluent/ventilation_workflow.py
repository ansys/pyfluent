# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
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

""".. _ventilation_flow_simulation:

Wind Flow Through A Mechanically Ventilated Poultry House
-------------------------------------------------------------
"""
# %%
# Objective
# ---------
#
# The primary objective of this PyFluent study is to investigate airflow patterns, air distribution,
# and ventilation effectiveness inside a mechanically ventilated poultry house.
# The simulation represents a typical poultry housing configuration with
# 32 side inlet windows and six exhaust fans installed on one end wall, capturing the
# interaction between inlet air jets and exhaust driven flow.
#
# The study analyzes velocity fields, airflow distribution, and mixing characteristics
# to evaluate the uniformity of fresh air delivery, particularly within bird occupied zones,
# and to identify regions of stagnant airflow.
#
# Ventilation performance is assessed based on its ability to supply adequate fresh air.
# In addition, the influence of inlet and fan configuration on airflow direction is examined
# to provide insights for ventilation system optimization.
#
#
# Problem Description
# -------------------
#
# This simulation models a mechanically ventilated broiler house with the following
# configuration:
#
# - **32 side inlet windows**: Located along the sidewalls to allow fresh air intake
# - **6 exhaust fans**: Installed on one end wall to remove stale air
#
# The analysis focuses on:
#
# - Velocity field distribution throughout the poultry house
# - Airflow pathlines from inlets to exhaust fans
# - Uniformity of exhaust velocities across the six fans
#
# .. image:: ../../_static/wind_flow_1.png
#    :align: center
#    :alt: Schematic of mechanically ventilated poultry house

# %%
# Import modules
# ^^^^^^^^^^^^^^

import os

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.core.solver import (
    BoundaryConditions,
    Contour,
    Graphics,
    Initialization,
    Methods,
    Pathlines,
    PlaneSurfaces,
    PressureOutlets,
    Residual,
    RunCalculation,
    SurfaceIntegrals,
    Viscous,
)

# %%
# Launch Fluent in solver mode
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# .. note::
#   Fluent supports multiple launch modes and options. For a full description of the
#   available launch methods and how to configure them, refer to the:
#   `PyFluent documentation <https://fluent.docs.pyansys.com/version/stable/api/launcher/launcher.html>`_.

solver = pyfluent.launch_fluent(
    precision=pyfluent.Precision.DOUBLE,
    mode=pyfluent.FluentMode.SOLVER,
)

# %%
# Read mesh
# ^^^^^^^^^
mesh_file = examples.download_file(
    "poultry_farm_ventilation.msh",
    "pyfluent/poultry_ventilation",
    save_path=os.getcwd(),
)

solver.file.read(file_type="mesh", file_name=mesh_file)

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
viscous.model = viscous.model.K_EPSILON

# %%
# Boundary conditions
# ^^^^^^^^^^^^^^^^^^^

boundary_conditions = BoundaryConditions(solver)
boundary_conditions.set_zone_type(new_type="inlet-vent", zone_list=["*inlet_vent_*"])

pressure_outlets = PressureOutlets(solver)
# %%
# The target mass flow rate option is enabled to ensure that each exhaust outlet
# (fan) removes a specified and controlled amount of air.

pressure_outlets["outlet_*"] = {
    "momentum": {
        "target_mass_flow_rate": True,
        "target_mass_flow": {
            "value": 12.25  # kg/ s; Represents the design airflow capacity of one exhaust fan
        },
    }
}

# %%
# Solution methods and controls
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

solution_methods = Methods(solver)

solution_methods.p_v_coupling.flow_scheme = "SIMPLEC"
# %%
# SIMPLEC: Faster convergence and better pressure–velocity coupling for steady, incompressible indoor airflow

# %%
solution_methods.spatial_discretization = {
    "gradient_scheme": "green-gauss-cell-based",
    "discretization_scheme": {
        "epsilon": "second-order-upwind",
        "k": "second-order-upwind",
        "mom": "second-order-upwind",
        "pressure": "second-order",
    },
}
# %%
# The cell-based Green–Gauss method calculates gradients using cell centered values and face fluxes,
# making it less sensitive to mesh irregularities and more stable than node-based methods

# %%
monitor_residuals = Residual(solver)

equations = (
    "continuity",
    "x-velocity",
    "y-velocity",
    "z-velocity",
    "k",
    "epsilon",
)

monitor_residuals.equations = {eqn: {"absolute_criteria": 1e-6} for eqn in equations}

# %%
# Residual convergence: to ensure a high level of numerical accuracy and solution stability in the simulation

# %%
# Initialize and run
# ^^^^^^^^^^^^^^^^^^
solution_initialization = Initialization(solver)
solution_initialization.initialization_type = "hybrid"
solution_initialization.initialize()

calculation = RunCalculation(solver)
calculation.iterate(iter_count=1000)
# %%
# The objective of running 1000 iterations is to obtain a physically reasonable
# flow field and to demonstrate typical convergence behavior. Increasing the number
# of iterations generally helps reduce residuals and stabilize key monitored quantities
# such as mass flow, average velocity, and recirculation patterns. For faster
# demonstration runs, the iteration count can be reduced once the residuals no longer change significantly.

# %%
# Results
# ^^^^^^^

# %%
# Define image resolution as named constants to improve maintainability.
# Updating these values will automatically apply to all image save operations.

graphics = Graphics(solver)

image_width = 650
image_height = 450

graphics.picture.x_resolution = image_width
graphics.picture.y_resolution = image_height
# %%

plane_surfaces = PlaneSurfaces(solver)

# Create ZX plane at the center of the domain
plane_surfaces.create()
plane_surfaces.rename(new="zx-plane", old="plane-1")
plane_surfaces["zx-plane"].method = "zx-plane"

# Create pathlines
velocity_pathline = Pathlines(solver)

velocity_pathline["pathlines-1"] = {
    "field": "velocity-magnitude",
    "release_from_surfaces": ["*inlet_vent_*"],
}
velocity_pathline["pathlines-1"].display()

graphics.picture.save_picture(file_name="wind_flow_2.png")


# %%
# .. image:: ../../_static/wind_flow_2.png
#    :align: center
#    :alt: Pathlines showing airflow from inlets to outlets


# Create velocity contour
velocity_contour = Contour(solver, new_instance_name="velocity_contour")

velocity_contour.field = "velocity-magnitude"
velocity_contour.surfaces_list = ["zx-plane"]
velocity_contour.display()

graphics.picture.save_picture(file_name="wind_flow_3.png")

# %%
# .. image:: ../../_static/wind_flow_3.png
#    :align: center
#    :alt: Velocity contour showing airflow distribution


surface_integrals_reports = SurfaceIntegrals(solver)

surface_integrals_reports.area_weighted_avg(
    file_name="velocity_area_avg_of_outlets",
    report_of="velocity-magnitude",
    surface_names=["*outlet_*"],
    write_to_file=True,
)
# %%
# Computes the area-weighted average of velocity magnitude over all outlet surfaces and writes the results to a
# "Surface Integral Report" file, listing the velocity values for each outlet.


solver.settings.file.write_case_data(file_name="poultry_ventilation")
# %%
# Save case and data

# %%
# Close session
# ^^^^^^^^^^^^^
solver.exit()

# %%
# Discussion
# ^^^^^^^^^^
#
# The airflow behavior inside the mechanically ventilated house was analyzed using
# velocity contour, pathlines, and surface integral reports obtained from the PyFluent simulation.
#
# Pathline visualizations illustrated the trajectories of air entering through the side inlets and
# exiting through the exhaust fans. These pathlines confirmed the effective transport of fresh air
# across the poultry house and demonstrated the interaction between inlet air jets and the exhaust-driven flow.
#
# Quantitative assessment of ventilation performance was conducted using area-weighted average velocity values
# at the exhaust outlets. The outlet velocities ranged from approximately 7.99 m/s to 8.94 m/s, with a
# net area-weighted average velocity of 8.36 m/s. The relatively small variation in velocity among the
# six outlets indicates a balanced and uniform exhaust performance, suggesting that the ventilation
# system effectively distributes airflow across the outlets without significant flow imbalance.
#
# Overall, the combined analysis of pathlines, velocity contours, and outlet velocity averages
# demonstrates that the simulated ventilation system provides effective airflow transport and
# reasonably uniform exhaust performance. These results validate the use of PyFluent for evaluating
# ventilation effectiveness and offer valuable insights for optimizing inlet and fan configurations
# to further improve airflow distribution and indoor air quality in mechanically ventilated poultry housing.

# sphinx_gallery_thumbnail_path = '_static/wind_flow_2.png'
