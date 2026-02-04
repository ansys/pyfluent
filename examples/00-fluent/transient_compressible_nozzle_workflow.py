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

""".. _Compressible_Flow_Simulation:

Modeling Transient Compressible Flow
-------------------------------------------------------------
"""

# %%
# Objective
# ---------
#
# This example models transient, compressible airflow through a nozzle,
# mimicking jet engine or rocket propulsion systems.
# It starts with a steady-state solution to establish
# an accurate initial flow field. A time-varying outlet
# pressure, defined by a sinusoidal expression, simulates pulsating flow.
#
# The simulation uses a density-based solver to capture shock waves and
# automatic mesh adaptation to refine the grid in high-gradient regions,
# like shocks. This ensures numerical stability and accuracy in both steady
# and transient phases. The approach demonstrates steady-to-transient coupling,
# dynamic boundary conditions, and adaptive meshing for high-speed, time-dependent flows.

# %%
# Problem Description
# -------------------
#
# The nozzle has an inlet height of 0.2 meters and a smooth, sinusoidal contour
# that reduces the cross-sectional flow area by 20% at the throat, accelerating
# air to high Mach numbers. This design mimics jet engine nozzles,
# where flow compression drives thrust. Due to geometric and flow symmetry along
# the center plane, only half the domain is modeled, reducing computational cost
# while maintaining accurate flow field results, including shock formation and
# pressure dynamics.
#
# .. image:: ../../_static/transient_compressible_1.png
#    :align: center
#    :alt: Transient Compressible Flow Model

# %%
# Import modules
# --------------
#
# .. note::
#   Importing the following classes offer streamlined access to key solver settings,
#   eliminating the need to manually browse through the full settings structure.

from pathlib import Path
import platform

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.core.generated.solver.settings_builtin_261 import BoundaryCondition
from ansys.fluent.core.solver import (
    Contour,
    Controls,
    FluidMaterial,
    General,
    Graphics,
    Initialization,
    Mesh,
    PressureInlet,
    PressureOutlet,
    ReportDefinitions,
    RunCalculation,
    Setup,
    CellRegister,
    ReportFile,
    ReportPlot,
    calculate,
    iterate,
    write_case,
)
from ansys.fluent.visualization import GraphicsWindow, Monitor
from ansys.units import Quantity, VariableCatalog
from ansys.units.common import Pa, m, s

# %%
# Launch Fluent session in meshing mode
# -------------------------------------

meshing = pyfluent.Meshing.from_install()

# %%
# Meshing workflow
# ----------------

workflow = meshing.workflow

filenames = {
    "Windows": "nozzle.dsco",
    "Other": "nozzle.dsco.pmdb",
}

geometry_filename = examples.download_file(
    filenames.get(platform.system(), filenames["Other"]),
    "pyfluent/transient_compressible_simulation",
    save_path=Path.cwd(),
)

# Upload geometry to the Meshing session so tasks can operate on it
meshing.upload(geometry_filename)

workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
workflow.TaskObject["Import Geometry"].Arguments = {"FileName": geometry_filename}
workflow.TaskObject["Import Geometry"].Execute()

workflow.TaskObject["Add Local Sizing"].Execute()

# %%
# Generate surface mesh
# ---------------------

surface_mesh = {
    "CFDSurfaceMeshControls": {
        "MaxSize": 30,  # mm
        "MinSize": 2,  # mm
        "SizeFunctions": "Curvature",
    }
}
workflow.TaskObject["Generate the Surface Mesh"].Arguments.set_state(surface_mesh)
workflow.TaskObject["Generate the Surface Mesh"].Execute()

# %%
# Describe geometry
# -----------------

geometry_describe = {
    "SetupType": "The geometry consists of only fluid regions with no voids",
    "WallToInternal": "No",
    "InvokeShareTopology": "No",
    "Multizone": "No",
}
workflow.TaskObject["Describe Geometry"].Arguments.set_state(geometry_describe)
workflow.TaskObject["Describe Geometry"].Execute()

# %%
# Update boundaries and region
# ---------------------------

boundary_condition = {
    "BoundaryLabelList": ["inlet"],
    "BoundaryLabelTypeList": ["pressure-inlet"],
    "OldBoundaryLabelList": ["inlet"],
    "OldBoundaryLabelTypeList": ["velocity-inlet"],
}
workflow.TaskObject["Update Boundaries"].Arguments.set_state(boundary_condition)
workflow.TaskObject["Update Boundaries"].Execute()

workflow.TaskObject["Update Regions"].Execute()

# %%
# Add boundary layers
# -------------------
# Add boundary layers: 8 layers with 0.35 transition ratio for accurate near-wall resolution
boundary_layer = {
    "NumberOfLayers": 8,
    "TransitionRatio": 0.35,
}
workflow.TaskObject["Add Boundary Layers"].Arguments.update_dict(boundary_layer)
workflow.TaskObject["Add Boundary Layers"].Execute()

# %%
# Generate volume mesh
# --------------------

workflow.TaskObject["Generate the Volume Mesh"].Arguments.setState(
    {
        "VolumeFill": "poly-hexcore",
        # Poly-hexcore mesh combines polyhedral cells with hexahedral core for accuracy and computational efficiency.
        "VolumeFillControls": {
            "BufferLayers": 1,  # Thin buffer to avoid hex-to-poly abruptness
            "HexMaxCellLength": 20,  # mm
            "HexMinCellLength": 5,  # mm
            "PeelLayers": 0,
        },
        "VolumeMeshPreferences": {
            "Avoid1_8Transition": "yes",
            "MergeBodyLabels": "yes",
            "ShowVolumeMeshPreferences": True,
        },
    }
)
workflow.TaskObject["Generate the Volume Mesh"].Execute()

# %%
# Switch to solver
# ----------------

solver = meshing.switch_to_solver()

# %%
# Display mesh
# ------------

graphics = Graphics(solver)
mesh = Mesh.create(solver, name="mesh-1")
boundary_conditions = BoundaryCondition(solver)

graphics.picture.x_resolution = 650  # Horizontal resolution for clear visualization
graphics.picture.y_resolution = 450  # Vertical resolution matching typical aspect ratio

mesh.surfaces_list = mesh.surfaces_list.allowed_values()
mesh.options.edges = True
mesh.display()
graphics.views.restore_view(view_name="isometric")
graphics.picture.save_picture(file_name="transient_compressible_2.png")

# %%
# .. image:: ../../_static/transient_compressible_2.png
#    :align: center
#    :alt: Transient Compressible Flow Mesh

# %%
# Configure solver
# ----------------

solver_general_settings = General(solver)

solver_general_settings.units.set_units(
    quantity="pressure",
    units_name="atm",
)
# density-based solver for compressible flow to capture shock behavior accurately.
solver_general_settings.solver.type = "density-based-implicit"
solver_general_settings.operating_conditions.operating_pressure = 0

setup = Setup(solver)

setup.models.energy.enabled = True
air = FluidMaterial(solver, name="air")
air.density.option = "ideal-gas"

# %%
# Set boundary conditions
# -----------------------

inlet = PressureInlet.get(solver, name="inlet")
outlet = PressureOutlet.get(solver, name="outlet")

inlet.momentum.gauge_total_pressure = 91192.5 * Pa
inlet.momentum.supersonic_or_initial_gauge_pressure = 74666.3925 * Pa

# Low turbulent intensity of 1.5% for smooth inlet flow, typical for nozzle simulations.
inlet.turbulence.turbulent_intensity = 0.015

outlet.momentum.gauge_pressure = 74666.3925 * Pa
outlet.turbulence.backflow_turbulent_intensity = 0.015

# %%
# Set solution controls
# ---------------------
# Higher Courant number balances fast convergence and stability in density-based solver
controls = Controls(solver)
controls.courant_number = 25

# %%
# Define report definition
# ------------------------

mass_report = ReportDefinitions(solver).surface.create(
    name="mass-flow-rate",
    report_type="surface-massflowrate",
    surface_names=[outlet],
)

mass_rfile = ReportFile.create(
    solver,
    name="mass_flow_rate_out_rfile",
    report_defs=[mass_report],
    print=True,
    file_name="nozzle_ss.out",
)

mass_rplot = ReportPlot.create(
    solver, "mass_flow_rate_out_rplot", report_defs=[mass_report], print=True
)

# %%
# Steady-State Initialization and Mesh Adaptation
# -----------------------------------------------

write_case(solver, file_name="nozzle_steady.cas.h5")

initialize = Initialization(solver)
initialize.hybrid_initialize()

cell_register = CellRegister(solver)

# Refinement register: Mark cells where density gradient >50% of domain average
density_refn = CellRegister.create(solver, name="density_scaled_gradient_refn")
density_refn.type.option = "field-value"
density_refn.type.field_value.derivative = "gradient"
density_refn.type.field_value.scaling = "scale-by-global-average"
density_refn.type.field_value.option.option = "more-than"
density_refn.type.field_value.option.more_than = 0.5  # Threshold: >50% average
density_refn.type.field_value.field = "density"

# Coarsening register: Mark cells where density gradient <45% of domain average
density_crsn = CellRegister.create(solver, name="density_scaled_gradient_crsn")
density_crsn.type.option = "field-value"
density_crsn.type.field_value.derivative = "gradient"
density_crsn.type.field_value.scaling = "scale-by-global-average"
density_crsn.type.field_value.option.option = "less-than"
density_crsn.type.field_value.option.less_than = 0.45  # Threshold: <45% average
density_crsn.type.field_value.field = "density"

# Define adaptation criteria: Refine if gradient is high and refinement level <2; coarsen if low
mesh.adapt.manual_refinement_criteria = (
    "AND(density_scaled_gradient_refn, CellRefineLevel < 2)"
)
mesh.adapt.manual_coarsening_criteria = "density_scaled_gradient_crsn"

mesh.adapt.manage_criteria.add("F")

iterate(solver, iter_count=400)

# %%
# Post-processing
# ---------------

# Create pressure contour
pressure_contour = Contour.create(
    solver, name="pressure_contour", surfaces_list=["symmetry"]
)
pressure_contour.display()

graphics.views.restore_view(view_name="front")
graphics.picture.save_picture(file_name="transient_compressible_3.png")

# %%
# .. image:: ../../_static/transient_compressible_3.png
#    :align: center
#    :alt: Transient Compressible Flow Pressure Contour

# Create velocity contour
velocity_contour = Contour.create(
    solver,
    name="velocity_contour",
    field=VariableCatalog.VELOCITY_MAGNITUDE,
    surfaces_list=["symmetry"],
)
velocity_contour.display()

graphics.views.restore_view(view_name="front")
graphics.picture.save_picture(file_name="transient_compressible_4.jpg")

# save the case and data file
write_case(solver, file_name="steady_state_nozzle.cas.h5")

# %%
# .. image:: ../../_static/transient_compressible_4.jpg
#    :align: center
#    :alt: Transient Compressible Flow Velocity Contour

# %%
# Enabling time dependence and setting transient conditions
# ---------------------------------------------------------

solver_general_settings.solver.time = "unsteady-1st-order"

# Sinusoidal pressure variation at 2200 Hz simulates pulsating flow, with mean pressure of 0.737 atm.
outlet.momentum.gauge_pressure = "(0.12*sin(2200[Hz]*t)+0.737)*101325.0[Pa]"

# Configure mesh adaptation: Refine every 25 iterations
mesh.adapt.manage_criteria.edit("adaption_criteria_0", "frequency", "25")

mass_rfile.file_name = "trans-nozzle-rfile.out"

mass_rplot.x_label = "time-step"

write_case(solver, file_name="nozzle_unsteady.cas.h5")

transient_controls = RunCalculation(solver).transient_controls
transient_controls.time_step_count = 100
transient_controls.time_step_size = 2.85596e-05 * s
transient_controls.max_iter_per_time_step = 10

calculate(solver)

mass_bal_rplot = Monitor(solver=solver, monitor_set_name="mass_flow_rate_out_rplot")
plot_window = GraphicsWindow()
plot_window.add_plot(mass_bal_rplot)
plot_window.show()

# %%
# .. image:: ../../_static/transient_compressible_5.jpg
#    :align: center
#    :alt: Transient Compressible Flow mass flow rate plot

# %%
# Close Fluent
# ^^^^^^^^^^^^

solver.exit()

# %%
# Summary
# -------
#
# In this example, we used PyFluent to model transient
# compressible flow in a nozzle with a sinusoidal pressure
# variation, simulating a realistic engineering scenario
# such as a jet engine or rocket propulsion system.
# The workflow demonstrated the use of the modern Watertight
# Geometry meshing, density-based solver setup, and
# post-processing with pressure and velocity contours.
# These procedures can be adapted to other compressible
# flow simulations,
# ensuring accurate modeling of shock waves and
# transient flow behavior.

# %%
# References:
# -----------
# [1] Modeling Transient Compressible Flow, `Ansys Fluent documentation​ <https://ansyshelp.ansys.com/public/account/secured?returnurl=/Views/Secured/corp/v252/en/flu_tg/flu_tg_transient_compressible.html>`_.

# sphinx_gallery_thumbnail_path = '_static/transient_compressible_2.png'
