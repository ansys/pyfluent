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

""".. _single_battery_cell_simulation:

Single Battery Cell Using MSMD Battery Model Simulation
----------------------------------------------------------------------------
"""

#######################################################################################
# Problem Description:
# =====================================================================================
# This example simulates a 14.6 Ah lithium-ion battery with a LiMn₂O₄ cathode and graphite
# anode using the Multi-Scale Multi-Domain (MSMD) battery model in Ansys Fluent.
# The simulation evaluates the battery's electrochemical and thermal performance
# under various discharge rates (e.g., 0.5C, 1C, 5C) and operating conditions, including
# normal operation, pulse discharge, and short-circuit scenarios. Key outputs include voltage,
# temperature, and state of charge, providing insights into battery behavior for
# design and analysis purposes.
#
# .. image:: ../../_static/Single_Battery_cell_model.png
#    :align: center
#    :alt: Single Battery Cell Model

#######################################################################################
# Import modules
# =====================================================================================
# The following Python modules are imported to interface with Ansys Fluent and manage file operations:
import os

import ansys.fluent.core as pyfluent
from ansys.fluent.core import FluentMode, Precision, UIMode, examples

#######################################################################################
# Launch Fluent session with solver mode and user interface
# =====================================================================================
# A Fluent solver session is launched in GUI mode with double precision and four
# processors to perform the simulation:

solver = pyfluent.launch_fluent(
    precision=Precision.DOUBLE,
    processor_count=4,
    mode=FluentMode.SOLVER,
    ui_mode=UIMode.GUI,
)

#######################################################################################
# Download the mesh file
# =====================================================================================
# The battery mesh file is downloaded from the Fluent examples repository and
# saved to the current working directory:
#
unit_battery_mesh = examples.download_file(
    "unit_battery.msh.h5",
    "pyfluent/battery_thermal_simulation",
    save_path=os.getcwd(),
)

#######################################################################################
# Load Mesh file and display it with surfaces
# =====================================================================================


solver.settings.file.read_case(file_name=unit_battery_mesh)  # Read the mesh file
# List of surfaces to display
surfaces = [
    "internal-18",
    "internal-18:20",
    "tab_n",
    "tab_p",
    "wall_active",
    "wall_n",
    "wall_p",
]

mesh = solver.settings.results.graphics.mesh
mesh.create("mesh-1")
mesh["mesh-1"].surfaces_list = surfaces
mesh["mesh-1"].options.edges = True
mesh["mesh-1"].display()

graphics = solver.settings.results.graphics

graphics.picture.x_resolution = 650
graphics.picture.y_resolution = 450

graphics.views.restore_view(view_name="isometric")

graphics.picture.save_picture(
    file_name="Single_Battery_Cell_Mesh.png",
)

# %%
# .. image:: ../../_static/Single_Battery_Cell_Mesh.png
#    :align: center
#    :alt: Single Battery Cell Mesh

#######################################################################################
# Battery Model Solver setup:
# =====================================================================================
#
# The simulation uses an unsteady first-order time solver to model the transient behavior
# of the battery, including voltage, temperature, and state of charge during discharge:

solver.settings.setup.general.solver.time = "unsteady-1st-order"

#######################################################################################
# Enable the battery model:
# =====================================================================================
#
# By enabling the Battery Model, Fluent activates the physics and equations needed
# to simulate how the battery behaves electrically, chemically, and thermally.
#
# Select NTGK/DCIR Model:
# This is a simplified but accurate model (based on experimental data) for simulating
# how voltage and heat change during discharge.
# NTGK stands for Newman, Tiedemann, Gu, and Kim, who developed this model.
#
# Set Nominal Cell Capacity (14.6 Ah):
# Defines the total amount of charge the battery can store,
# based on the actual battery specs.
#
# Enable Joule Heat in Passive Zones:
# Includes heat generated in non-active parts like tabs and connectors. This makes the
# thermal results more accurate.
#
# Specify C-Rate (1C):
# Sets how fast the battery discharges. A 1C rate means the battery will fully discharge
# in 1 hour. Higher C-rates mean faster discharge.
#
# Minimum Stop Voltage (3 V):
# Fluent will stop the simulation if the battery voltage drops
# below this. It's a safety cutoff, just like in real batteries.
#
# Assign Zones under Conductive Zones:
# You're telling Fluent which parts are the active battery
# region (electrochemical zone) and which are conductive parts like tabs or connectors.
#
# Assign External Connectors:
# Defines where the current enters and leaves the battery. These are the positive and
# negative terminals.
#
# Print Battery System Connection Info:
# This checks if Fluent understood your setup and shows how everything is connected.
#
battery = solver.settings.setup.models.battery
battery.enabled = True
battery.echem_model = "ntgk/dcir"
battery.zone_assignment.active_zone = ["e_zone"]
battery.zone_assignment.passive_zone = ["tab_nzone", "tab_pzone"]
battery.zone_assignment.negative_tab = ["tab_n"]
battery.zone_assignment.positive_tab = ["tab_p"]
battery.zone_assignment.print_battery_connection()

# %%
# .. image:: ../../_static/battery_connection_info.png
#    :align: center
#    :alt: Battery Connection Information


#######################################################################################
#  Defining New Materials for Cell and Tabs
# =====================================================================================
# Material properties for the battery cell and tabs are defined to accurately
# model electrical and thermal behavior:
#
# what materials the battery is made of
#
# How well each material conducts electricity
#
# This helps fluent calculate voltage, current, and heat correctly during the simulation

materials = [
    {
        "name": "e_material",
        "chemical_formula": "e",
        "density": 2092,
        "specific_heat": 678,
        "thermal_conductivity": 18.2,
        "uds_diffusivity": {
            "option": "defined-per-uds",
            "uds-0": 1190000,
            "uds-1": 983000,
        },
    },
    {
        "name": "p_material",
        "chemical_formula": "pmat",
        "density": 8978,
        "specific_heat": 381,
        "thermal_conductivity": 387.6,
        "uds_diffusivity": {"option": "constant", "value": 10000000},
    },
    {
        "name": "n_material",
        "chemical_formula": "nmat",
        "density": 8978,
        "specific_heat": 381,
        "thermal_conductivity": 387.6,
    },
]

solids = solver.settings.setup.materials.solid
for mat in materials:
    solids.create(mat["name"])
    solids[mat["name"]].chemical_formula = mat["chemical_formula"]
    solids[mat["name"]].density.value = mat["density"]
    solids[mat["name"]].specific_heat.value = mat["specific_heat"]
    solids[mat["name"]].thermal_conductivity.value = mat["thermal_conductivity"]
    if "uds_diffusivity" in mat:
        solids[mat["name"]].uds_diffusivity = {
            "option": mat["uds_diffusivity"]["option"]
        }
        if mat["uds_diffusivity"]["option"] == "defined-per-uds":
            solids[mat["name"]].uds_diffusivity.uds_diffusivities["uds-0"].value = mat[
                "uds_diffusivity"
            ]["uds-0"]
            solids[mat["name"]].uds_diffusivity.uds_diffusivities["uds-1"].value = mat[
                "uds_diffusivity"
            ]["uds-1"]
        else:
            solids[mat["name"]].uds_diffusivity.value = mat["uds_diffusivity"]["value"]

#######################################################################################
#  Defining the cell zone conditions
# =====================================================================================
# Assign e_material to e_zone → The active part of the battery cell (where the reactions happen)
# is made of this material.
#
# Assign p_material to tab_pzone → The positive tab is made of the positive terminal material.
#
# Assign n_material to tab_nzone → The negative tab is made of the negative terminal material

cell_zones = [
    ("e_zone", "e_material"),
    ("tab_nzone", "n_material"),
    ("tab_pzone", "p_material"),
]

for zone, material in cell_zones:
    solver.settings.setup.cell_zone_conditions.solid[zone].general.material = material

#######################################################################################
#  Defining Boundary Conditions
# =====================================================================================
# Convective heat transfer is applied to the battery’s external surfaces to model heat
# loss to the environment, with a heat transfer coefficient of 5 W/m²·K:

wall = solver.settings.setup.boundary_conditions.wall
wall["wall_active"].thermal.thermal_condition = "Convection"
wall["wall_active"].thermal.heat_transfer_coeff.value = 5

solver.settings.setup.boundary_conditions.copy(
    from_="wall_active", to=["wall_n", "wall_p"], verbosity=True
)

#######################################################################################
# Specifying solution settings
# =====================================================================================
# Since the simulation models a solid battery without fluid flow,
# flow and turbulence equations are disabled, and residual criteria are set to none:
#
# No flow = No need to solve equations for velocity or pressure.
#
# No turbulence = No air or liquid movement that could become chaotic.
#
solver.settings.solution.controls.equations["flow"] = False
solver.settings.solution.controls.equations["kw"] = False
solver.settings.solution.monitor.residual.options.criterion_type = "none"

#######################################################################################
# Creating Report Definitions
# =====================================================================================
# Report definitions are created to monitor the average voltage on the positive tab and
# the maximum temperature across the battery zones. Output files and plots are
# generated to track these quantities:

# Surface report for voltage
surface_reports = solver.settings.solution.report_definitions.surface
surface_reports.create("voltage_vp")
surface_reports["voltage_vp"] = {
    "report_type": "surface-areaavg",
    "field": "passive-zone-potential",
    "surface_names": ["tab_p"],
}

# Volume report for maximum temperature
volume_reports = solver.settings.solution.report_definitions.volume
volume_reports.create("max_temp")
volume_reports["max_temp"] = {
    "report_type": "volume-max",
    "field": "temperature",
    "cell_zones": ["e_zone", "tab_nzone", "tab_pzone"],
}

# Configure report files
report_files = solver.settings.solution.monitor.report_files

report_files.create("voltage_vp-rfile")
report_files["voltage_vp-rfile"].report_defs = ["flow-time", "voltage_vp"]
report_files["voltage_vp-rfile"].file_name = "ntgk-1c.out"
report_files["voltage_vp-rfile"].print = True

report_files.create("max_temp")
report_files["max_temp"].report_defs = ["max_temp"]
report_files["max_temp"].file_name = "max-temp-1c.out"
report_files["max_temp"].print = True

# Configure report plots
report_plots = solver.settings.solution.monitor.report_plots

report_plots.create("voltage_vp")
report_plots["voltage_vp"].report_defs = ["voltage_vp"]
report_plots["voltage_vp"].print = True
report_plots["voltage_vp"].axes.x.number_format.precision = 0
report_plots["voltage_vp"].axes.y.number_format.precision = 2

report_plots.create("max_temp")
report_plots["max_temp"].report_defs = ["max_temp"]
report_plots["max_temp"].print = True
report_plots["max_temp"].axes.x.number_format.precision = 0
report_plots["max_temp"].axes.y.number_format.precision = 2

#######################################################################################
# Obtaining the solution
# =====================================================================================

solver.settings.solution.initialization.standard_initialize()
solver.settings.solution.run_calculation.transient_controls.time_step_size = 30
solver.settings.solution.run_calculation.transient_controls.time_step_count = 100
solver.settings.solution.run_calculation.calculate()

#######################################################################################
# Post-processing  setup
# =====================================================================================
# Configure contours and vector plot for visualizing the results

# Configure graphics settings
graphics = solver.settings.results.graphics
graphics.picture.x_resolution = 650
graphics.picture.y_resolution = 450

# Define and create contour plots
contours = solver.settings.results.graphics.contour
contour_list = [
    {
        "name": "contour-phi+",
        "field": "cathode-potential",
        "surfaces": ["wall_active"],
        "file_name": "Single_Battery_Cell_1.png",
    },
    {
        "name": "contour-phi-",
        "field": "anode-potential",
        "surfaces": ["wall_active"],
        "file_name": "Single_Battery_Cell_2.png",
    },
    {
        "name": "contour-phi-passive",
        "field": "passive-zone-potential",
        "surfaces": ["tab_n", "tab_p", "wall_n", "wall_p"],
        "file_name": "Single_Battery_Cell_3.png",
    },
    {
        "name": "contour-temp",
        "field": "temperature",
        "surfaces": ["wall_p", "wall_active", "tab_p", "tab_n", "wall_n"],
        "file_name": "Single_Battery_Cell_4.png",
    },
]

# Create, display, and save contour plots
for contour in contour_list:
    # Create the contour
    contours.create(contour["name"])
    current = contours[contour["name"]]
    current.field = contour["field"]
    current.surfaces_list = contour["surfaces"]
    current.range_options.compute()

    # Set the  view
    graphics.views.restore_view(view_name="front")

    #  display the  current contour
    current.display()

    # Save the contour plot as an image
    graphics.picture.save_picture(file_name=contour["file_name"])

# Create and configure vector plot
vectors = solver.settings.results.graphics.vector
vectors.create("vector-current_density")
vector_plot = vectors["vector-current_density"]
vector_plot.vector_field = "current-density-j"
vector_plot.field = "current-magnitude"
vector_plot.surfaces_list = ["wall_n", "wall_p", "wall_active", "tab_n", "tab_p"]
vector_plot.options.vector_style = "arrow"
vector_plot.range_options.compute()

# Set view, display, and save the vector plot image
graphics.views.restore_view(view_name="front")
vector_plot.display()
graphics.picture.save_picture(file_name="Single_Battery_Cell_5.png")

# Save case file
solver.settings.file.write(file_name="unit_battery.cas.h5", file_type="case")

# %%
# .. image:: ../../_static/Single_Battery_Cell_1.png
#    :align: center
#    :alt:  Anode Potential Contour(c=1)
#
# .. image:: ../../_static/Single_Battery_Cell_2.png
#    :align: center
#    :alt:  Cathode Potential Contour(c=1)
#
#
# .. image:: ../../_static/Single_Battery_Cell_3.png
#    :align: center
#    :alt:  Passive Zone Potential Contour(c=1)
#
#
# .. image:: ../../_static/Single_Battery_Cell_4.png
#    :align: center
#    :alt:  Static Temperature Contour(c=1)
#
#
# .. image:: ../../_static/Single_Battery_Cell_5.png
#    :align: center
#    :alt:  Current Density Vector(c=1)
#


#######################################################################################
# Running the simulation at different C-Rates and time steps
# =====================================================================================
# The simulation is repeated at 0.5C and 5C discharge rates to analyze performance
# under varying loads. Different time step counts are used to account for faster or slower discharge:
#

solver.settings.setup.models.battery.eload_condition.eload_settings.crate_value = (
    0.5  # C-Rate=0.5
)

report_files["voltage_vp-rfile"].file_name = "ntgk-0.5c.out"
report_files["max_temp"].file_name = "max-temp-0.5c.out"

solver.settings.solution.initialization.standard_initialize()
solver.settings.solution.run_calculation.transient_controls.time_step_count = 230
solver.settings.solution.run_calculation.calculate()

# C-Rate=5 simulation
solver.settings.setup.models.battery.eload_condition.eload_settings.crate_value = (
    5  # C-Rate=5
)

report_files["voltage_vp-rfile"].file_name = "ntgk-5c.out"
report_files["max_temp"].file_name = "max-temp-5c.out"

solver.settings.solution.initialization.standard_initialize()
solver.settings.solution.run_calculation.transient_controls.time_step_count = 23
solver.settings.solution.run_calculation.calculate()

#######################################################################################
# Reduced Order Method (ROM) Battery Model Setup
# =====================================================================================
# The Reduced Order Method (ROM) is applied to improve computational efficiency.

solver.settings.file.read_case(file_name="unit_battery.cas.h5")  # Read the case file

# Initialize the problem
solver.settings.solution.initialization.standard_initialize()
solver.settings.solution.run_calculation.transient_controls.time_step_size = 30
solver.settings.solution.run_calculation.transient_controls.time_step_count = 3
solver.settings.solution.run_calculation.calculate()

# Once the calculatuion is done, we enable ROM
solver.settings.setup.models.battery.solution_method = "msmd-rom"
solver.settings.setup.models.battery.solution_option.option_settings.number_substeps = (
    10
)
solver.settings.solution.run_calculation.transient_controls.time_step_size = 30
solver.settings.solution.run_calculation.transient_controls.time_step_count = 100
solver.settings.solution.run_calculation.calculate()

# contour and vector plots for ROM results

graphics = solver.settings.results.graphics
graphics.picture.x_resolution = 650
graphics.picture.y_resolution = 450

contours = solver.settings.results.graphics.contour
contour_list = [
    {"name": "contour-phi+", "field": "cathode-potential", "surfaces": ["wall_active"]},
    {"name": "contour-phi-", "field": "anode-potential", "surfaces": ["wall_active"]},
    {
        "name": "contour-phi-passive",
        "field": "passive-zone-potential",
        "surfaces": ["tab_n", "tab_p", "wall_n", "wall_p"],
    },
    {
        "name": "contour-temp",
        "field": "temperature",
        "surfaces": ["wall_p", "wall_active", "tab_p", "tab_n", "wall_n"],
    },
]

for contour in contour_list:
    contours.create(contour["name"])
    contours[contour["name"]].field = contour["field"]
    contours[contour["name"]].surfaces_list = contour["surfaces"]
    contours[contour["name"]].range_options.compute()

vectors = solver.settings.results.graphics.vector
vectors.create("vector-current_density")
vectors["vector-current_density"].vector_field = "current-density-j"
vectors["vector-current_density"].field = "current-magnitude"
vectors["vector-current_density"].surfaces_list = [
    "wall_n",
    "wall_p",
    "wall_active",
    "tab_n",
    "tab_p",
]
vectors["vector-current_density"].options.vector_style = "arrow"
vectors["vector-current_density"].range_options.compute()

# Set view, display, and save the vector plot image
graphics.views.restore_view(view_name="front")
vector_plot.display()
graphics.picture.save_picture(file_name="Single_Battery_Cell_6.png")

# %%
# .. image:: ../../_static/Single_Battery_Cell_6.png
#    :align: center
#    :alt:  current magnitude(c=1)
# Vector current density for ROM model
#
# The solution of the simulation using the ROM is significantly faster than
# when using the direct method without any changes in results.

#######################################################################################
# External and Internal Short-Circuit Treatment :
# =====================================================================================

#######################################################################################
# Setting up and Solving a Short-Circuit Problem
# =====================================================================================
# A short-circuit scenario is simulated by applying a low external resistance and defining
# a short-circuit region within the battery:

solver.settings.file.read_case(
    file_name=unit_battery_mesh
)  # Read the original case file again

# Configure battery model settings
solver.settings.setup.models.battery.eload_condition.eload_settings.set_state(
    {"eload_type": "specified-resistance", "external_resistance": 0.5}
)

# Create and configure cell register
solver.settings.solution.cell_registers.create(name="register_patch")
solver.settings.solution.cell_registers["register_patch"] = {
    "type": {
        "option": "hexahedron",
        "hexahedron": {
            "inside": True,
            "max_point": [0.01, 0.02, 1.0],
            "min_point": [-0.01, -0.01, -1.0],
        },
    }
}

# Initialize solution
solver.settings.solution.initialization.standard_initialize()
#
# Patch initialization
solver.settings.solution.initialization.patch.calculate_patch(
    domain="",
    cell_zones=[],
    registers=["register_patch"],
    variable="battery-short-resistance",
    reference_frame="Relative to Cell Zone",
    use_custom_field_function=False,
    custom_field_function_name="",
    value=5e-07,
)

# Set up transient calculation parameters
solver.settings.solution.run_calculation.transient_controls.set_state(
    {"time_step_size": 1, "time_step_count": 5}
)

# Run the simulation
solver.settings.solution.run_calculation.calculate()

# Save the case and data file
solver.settings.file.write(file_type="case-data", file_name="ntgk_short_circuit.cas.h5")

# Calculate surface integral
solver.settings.results.report.surface_integrals.area_weighted_avg(
    report_of="passive-zone-potential", surface_names=["tab_p"], write_to_file=False
)
# %%
# .. image:: ../../_static/Single_Battery_Cell_7.png
#    :align: center
#    :alt:  area weighted average
# Surface integral of passive zone potential after short circuit

# Calculate volume integral
solver.settings.results.report.volume_integrals.volume_integral(
    cell_function="total-current-source", cell_zones=["e_zone"], write_to_file=False
)
# %%
# .. image:: ../../_static/Single_Battery_Cell_8.png
#    :align: center
#    :alt:  total volume integral
# Total Volume Integral of total current source after short circuit

graphics = solver.settings.results.graphics
graphics.picture.x_resolution = 650
graphics.picture.y_resolution = 450

# Create and configure negative current vector plot
solver.settings.results.graphics.vector.create()
solver.settings.results.graphics.vector.rename(new="vector-current-", old="vector-1")
solver.settings.results.graphics.vector["vector-current-"].set_state(
    {
        "vector_field": "current-density-jn",
        "field": "current-magnitude",
        "surfaces_list": ["wall_n", "wall_p", "wall_active"],
        "options": {"vector_style": "arrow"},
    }
)
solver.settings.results.graphics.vector["vector-current-"].range_options.compute()

# Set view, display, and save the vector plot image
graphics.views.restore_view(view_name="front")
solver.settings.results.graphics.vector["vector-current-"].display()
graphics.picture.save_picture(file_name="Single_Battery_Cell_9.png")

# %%
# .. image:: ../../_static/Single_Battery_Cell_9.png
#    :align: center
#    :alt:  negative vector plot
# Negative Current vector plot after short circuit

# Create and configure positive current vector plot
solver.settings.results.graphics.vector.create()
solver.settings.results.graphics.vector.rename(new="vector-current+", old="vector-1")
solver.settings.results.graphics.vector["vector-current+"].set_state(
    {
        "vector_field": "current-density-jp",
        "field": "current-magnitude",
        "surfaces_list": ["wall_n", "wall_p", "wall_active"],
        "options": {"vector_style": "arrow"},
    }
)
solver.settings.results.graphics.vector["vector-current+"].range_options.compute()

# Set view, display, and save the vector plot image
graphics.views.restore_view(view_name="front")
solver.settings.results.graphics.vector["vector-current+"].display()
graphics.picture.save_picture(file_name="Single_Battery_Cell_10.png")

# %%
# .. image:: ../../_static/Single_Battery_Cell_10.png
#    :align: center
#    :alt:  positive plot
# Positive Current vector plot after short circuit

# Create and configure temperature contour plot
solver.settings.results.graphics.contour.create()
solver.settings.results.graphics.contour["contour-1"].set_state(
    {
        "field": "temperature",
        "surfaces_list": ["wall_p", "wall_active", "tab_p", "tab_n", "wall_n"],
    }
)
solver.settings.results.graphics.contour["contour-1"].range_options.compute()

# Set view, display, and save the vector plot image
graphics.views.restore_view(view_name="front")
solver.settings.results.graphics.contour["contour-1"].display()
graphics.picture.save_picture(file_name="Single_Battery_Cell_11.png")
# %%
# .. image:: ../../_static/Single_Battery_Cell_11.png
#    :align: center
#    :alt:  temperature contour
# Temperature contour plot after short circuit

#######################################################################################
# Close the solver
# =====================================================================================
solver.exit()

#######################################################################################
# References:
# =====================================================================================
#
# [1]  U. S. Kim et al, "Effect of electrode configuration on the thermal behavior of
# a lithium-polymer battery", Journal of Power Sources, Volume 180 (2), pages 909-916, 2008.
#
# [2]  U. S. Kim, et al., "Modeling the Dependence of the Discharge Behavior of a Lithium-Ion Battery
# on the Environmental Temperature", J. of Electrochemical Soc., Volume 158 (5), pages A611-A618, 2011.


# sphinx_gallery_thumbnail_path = '_static/Single_Battery_Cell_4.png'
