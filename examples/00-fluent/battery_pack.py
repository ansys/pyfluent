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

""".. _battery_pack:

Simulating a 1P3S Battery Pack Using the Battery Model
------------------------------------------------------
"""

# %%
# Objective
# ---------
#
# This example demonstrates a complete 1P3S battery pack simulation workflow comprising
# one parallel string and three cells in series using the NTGK
# (Newman-Tiedemann-Gu-Kim) electrochemical model utilizing PyFluent APIs.
# The goal is to model and analyze battery pack behavior under a constant
# 200 W discharge condition. This includes setting up active and passive zones,
# defining dual-path electrical conductivity using User-Defined Scalars (UDS),
# and applying convection cooling to simulate heat dissipation. The simulation
# aims to monitor key performance indicators such as pack voltage,
# maximum temperature, current flow, and heat generation over a 1500 second
# transient run, providing insights into thermal and electrical performance
# relevant to electric vehicle (EV) and energy storage system (ESS) design.

# %%
# Problem Description
# -------------------
#
# Simulation of a 1P3S lithium-ion battery pack, consisting of three cells
# connected in series and no parallel branches, undergoing a constant 200 W
# discharge to represent a high-load condition. Each cell has a
# nominal capacity of 14.6 Ah, resulting in a total pack capacity of 14.6 Ah
# and a nominal voltage range of 10.8–12.6 V, corresponding to an average cell
# voltage of approximately 3.9 V. The discharge C-rate equates to about 1.17C,
# and the total energy of roughly 171 Wh means the discharge would last around
# 51 minutes (3060 seconds). The simulation model includes active zones for the
# electrochemical cells and passive zones representing conductive components
# such as tabs and busbars, with defined electrical and thermal material properties.
# The model also incorporates natural convection cooling with a heat transfer coefficient
# of 5 W/m²·K and an ambient temperature of 300 K, allowing for realistic thermal
# management analysis.
#
# .. image:: ../../_static/battery_pack_schematic.png
#    :align: center
#    :alt: Battery Pack Schematic

# %%
# Import modules
# --------------
#
# .. note::
#   Importing the following classes offers streamlined access to key solver settings,
#   eliminating the need to manually browse through the full hierarchy of settings APIs structure.

from pathlib import Path

from ansys.units import VariableCatalog

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.core.solver import (
    Battery,
    Contour,
    Controls,
    General,
    Graphics,
    Initialization,
    Materials,
    Mesh,
    ReportDefinitions,
    RunCalculation,
    SolidMaterial,
    Solution,
    Vector,
    write_case_data,
    WallBoundary,
    SolidCellZone,
    ReportPlot,
    read_mesh,
)
from ansys.fluent.visualization import GraphicsWindow, Monitor
from ansys.units.common import K, W, m, ohm

# %%
# Define constants
# ----------------

S = 1 / ohm  # a Siemen


# %%
# Launch Fluent in solver mode
# ----------------------------

solver = pyfluent.Solver.from_install(
    precision=pyfluent.Precision.DOUBLE,
)

# %%
# Read mesh
# ---------

mesh_file = examples.download_file(
    "1P3S_battery_pack.msh",
    "pyfluent/battery_pack",
    save_path=Path.cwd(),
)

solver.setting.file.read_mesh(file_name=mesh_file)

# %%
# Display mesh
# ------------

graphics = Graphics(solver)
mesh = Mesh.create(solver, name="mesh-1")

graphics.picture.x_resolution = 650  # Horizontal resolution for clear visualization
graphics.picture.y_resolution = 450  # Vertical resolution matching typical aspect ratio

all_walls = mesh.surfaces_list.allowed_values()
mesh.surfaces_list = all_walls
mesh.options.edges = True
mesh.display()

graphics.picture.save_picture(file_name="battery_pack_1.png")

# %%
# .. image:: ../../_static/battery_pack_1.png
#    :align: center
#    :alt: Battery Pack Mesh

# %%
# Solver settings
# ---------------

general = General(solver)

general.solver.time = "unsteady-1st-order"

# %%
# Enable Battery Model (NTGK/DCIR)
# --------------------------------
#
# .. note::
#   Using wildcards (`*`, `?`, `|`, etc.) instead of explicit zone lists makes the setup
#   more flexible and scalable. For example:
#
#   - ``cell_*`` → selects all zones starting with ``cell_`` (e.g., ``cell_1``, ``cell_2``, ...)
#   - ``*bar*|*tabzone*`` → selects zones containing either ``bar`` or ``tabzone`` (e.g., ``bar1``, ``n_tabzone_1``,...)

battery_model = Battery(solver)

battery_model.enabled = True
battery_model.echem_model = "ntgk/dcir"
battery_model.eload_condition.eload_settings.eload_type = "specified-system-power"
battery_model.eload_condition.eload_settings.power_value = 200 * W  # Total pack power

# Conductive zones
battery_model.zone_assignment.active_zone = "cell_*"  # Active cells
battery_model.zone_assignment.passive_zone = "*bar*|*tabzone*"  # Bars zones + tab zones

# External electrical contacts
battery_model.zone_assignment.negative_tab = ["tab_n"]  # Negative terminal
battery_model.zone_assignment.positive_tab = ["tab_p"]  # Positive terminal

# %%
# Define materials
# ----------------

materials = Materials(solver)

# Active material (cells): conductivity via UDS-0 and UDS-1
e_material = SolidMaterial.create(solver, name="e_material", chemical_formula="e")
e_material.thermal_conductivity = 20 * W / (m * K)
e_material.uds_diffusivity.option = "defined-per-uds"
e_material.uds_diffusivity.uds_diffusivities["uds-0"] = (
    1e6 * S / m
)  # Electronic conductivity
e_material.uds_diffusivity.uds_diffusivities["uds-1"] = (
    1e6 * S / m
)  # Ionic conductivity

# Passive material (busbars & tabs): high constant conductivity
busbar_material = SolidMaterial.create(
    solver, name="busbar_material", chemical_formula="bus"
)
busbar_material.uds_diffusivity.option = "value"
busbar_material.uds_diffusivity.value = 3.541e7 * S / m  # Copper-like conductivity

# %%
# Assign materials to cell zones
# ------------------------------

# Assign e_material to cell_1 2 and 3 all at once
SolidCellZone.get(solver, name="cell_*").general.material = e_material

# Assign busbar_material to bar1 and all passive zones
SolidCellZone.get(solver, name="*bar*|*tabzone*").general.material = busbar_material

# %%
# Boundary conditions
# -------------------

# Convection on all walls (tabs, busbars, cells)
wall_bc = WallBoundary.get(solver, name="wall*")
wall_bc.thermal.thermal_condition = wall_bc.thermal.thermal_condition.CONVECTION
wall_bc.thermal.heat_transfer_coeff = 5 * W / (m**2 * K)

# %%
# Define solution controls and monitors
# ---------------------------------------
controls = Controls(solver)

# Disable flow and turbulence equations
controls.equations["flow"] = False
controls.equations["kw"] = False

solution = Solution(solver)

solution.monitor.residual.options.criterion_type = (
    "none"  # No automatic convergence check
)

# %%
# Define report definitions
# -------------------------
definitions = ReportDefinitions(solver)

# Surface report: voltage at positive tab (area-weighted average)
definitions.surface.create(
    name="voltage_surface_areaavg",
    report_type="surface-areaavg",
    field="passive-zone-potential",
    surface_names=["tab_p"],
    create_report_file=True,
    create_report_plot=True,
)

# Format plot axes
voltage_surface_areaavg = ReportPlot.get(solver, name="voltage_surface_areaavg-rplot")
voltage_surface_areaavg.axes.x.number_format.precision = 0  # Integer time steps
voltage_surface_areaavg.axes.y.number_format.precision = (
    2  # 2 decimal places for voltage
)

# Volume report: maximum temperature in all cell zones
vol_max = definitions.volume.create(
    name="volume_max_temp",
    report_type="volume-max",
    field=VariableCatalog.TEMPERATURE,
    cell_zones=["*cell|*bar*|*tabzone*"],
    create_report_file=True,
    create_report_plot=True,
)

volume_max_temp = ReportPlot.get(solver, name="volume_max_temp-rplot")
volume_max_temp.axes.x.number_format.precision = 0
volume_max_temp.axes.y.number_format.precision = 2

# %%
# Initialize solution
# -------------------
initialize = Initialization(solver)
initialize.standard_initialize()

# %%
# Transient controls
# ------------------
calculation = RunCalculation(solver)

transient_controls = calculation.transient_controls
# Use typed quantities for time step settings
transient_controls.time_step_count = 50  # Number of time steps
transient_controls.time_step_size = 30  # 30s per step

# Run transient simulation
calculation.calculate()

# %%
# Post-processing
# ---------------

# Current density vector plot
vector = Vector.create(
    solver,
    name="current-magnitude-vector",
    vector_field="current-density-j",  # A/m²  (Current density vector)
    field="current-magnitude",  # A/m²  (Magnitude for coloring)
    surfaces_list=["tab_n", "tab_p", "wall*"],
)
vector.options.vector_style = "arrow"
vector.options.scale = 0.03  # Scale factor for visibility
vector.vector_opt.fixed_length = True  # Uniform arrow length
vector.display()

graphics.views.restore_view(view_name="isometric")
graphics.picture.save_picture(file_name="battery_pack_2.png")

# %%
# .. image:: ../../_static/battery_pack_2.png
#    :align: center
#    :alt: Current density vector plot

# Temperature contour
temp_contour = Contour.create(
    solver,
    name="temp_contour",
    field=VariableCatalog.TEMPERATURE,  # K
    surfaces_list=["tab_n", "tab_p", "wall*"],
)
temp_contour.colorings.banded = True
temp_contour.display()

graphics.views.restore_view(view_name="isometric")
graphics.picture.save_picture(file_name="battery_pack_3.png")

# %%
# .. image:: ../../_static/battery_pack_3.png
#    :align: center
#    :alt: Temperature contour

# Joule heat source contour
joule_contour = Contour.create(
    solver,
    field="battery-joule-heat-source",  # W/m³
    surfaces_list=["tab_n", "tab_p", "wall*"],
)
joule_contour.colorings.banded = True
joule_contour.display()

graphics.views.restore_view(view_name="isometric")
graphics.picture.save_picture(file_name="battery_pack_4.png")

# %%
# .. image:: ../../_static/battery_pack_4.png
#    :align: center
#    :alt: Joule heat source contour

# Total heat source contour
total_heat_contour = Contour.create(
    solver,
    name="total_heating_contour",
    field="total-heat-source",  # W/m³  (Joule + reaction heat)
    surfaces_list=["tab_n", "tab_p", "wall*"],
)
total_heat_contour.colorings.banded = True
total_heat_contour.display()

graphics.views.restore_view(view_name="isometric")
graphics.picture.save_picture(file_name="battery_pack_5.png")

# %%
# .. image:: ../../_static/battery_pack_5.png
#    :align: center
#    :alt: Total heat source contour

# %%
# Display monitor plots
# ---------------------

plot_window = GraphicsWindow()

voltage_rplot = Monitor(solver=solver, monitor_set_name="voltage_surface_areaavg-rplot")
plot_window.add_plot(voltage_rplot, position=(0, 0))

temp_rplot = Monitor(solver=solver, monitor_set_name="volume_max_temp-rplot")
plot_window.add_plot(temp_rplot, position=(1, 1))

plot_window.show()

# %%
# .. image:: ../../_static/battery_pack_8.png
#    :align: center
#    :alt: Temperature and voltage Monitor Plot

# %%
# Save case and data
# ------------------------
write_case_data(solver, file_name="1P3S_Battery_Pack")

# %%
# Close Fluent
# -------------

solver.exit()

# %%
# Summary
# -------
#
# This example provides a complete and reproducible PyFluent workflow
# for simulating a multi-cell battery pack using the Battery Model with
# the NTGK sub-model. It demonstrates how to set up active and passive
# zones, apply constant power discharge, use UDS-based dual-path
# conductivity, and monitor voltage and temperature behavior during
# operation. It serves as a template for battery pack analysis,
# applicable to designs ranging from small modules to full EV packs.

# %%
# References:
# -----------
# [1] Simulating a 1P3S Battery Pack Using the Battery Model, `Ansys Fluent documentation​ <https://ansyshelp.ansys.com/public/account/secured?returnurl=/Views/Secured/corp/v252/en/flu_tg/flu_bat_tutorial_pack.html>`_.

# sphinx_gallery_thumbnail_path = '_static/battery_pack_2.png'
