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

""".. _single_battery_cell_simulation:

Single Battery Cell Using MSMD Battery Model Simulation
----------------------------------------------------------------------------
"""

#######################################################################################
# Problem Description:
# =====================================================================================
# Simulate a 14.6 Ah lithium-ion battery with a LiMn₂O₄ cathode and graphite anode using
# the Multi-Scale Multi-Domain (MSMD) battery model in Ansys Fluent. Evaluate the battery's
# electrochemical and thermal performance under various discharge rates (e.g., 0.5C, 1C, 5C)
# and operating conditions, including normal operation, pulse discharge, and short-circuit
# scenarios. Key outputs include voltage, temperature, and state of charge.
#
# .. image:: ../../_static/Single_Battery_cell_model.png
#    :align: center
#    :alt: Single Battery Cell Model

#######################################################################################
# Import modules
# =====================================================================================
from pathlib import Path

import ansys.fluent.core as pyfluent
from ansys.fluent.core import Precision, examples
from ansys.fluent.core.solver import (
    CellRegister,
    Controls,
    General,
    Graphics,
    Initialization,
    Monitor,
    ReportDefinitions,
    SolidCellZone,
    SolidMaterial,
    SurfaceIntegrals,
    VolumeIntegrals,
    BoundaryCondition,
    Contour,
    Mesh,
    Vector,
    read_case,
    write_case_data,
    write_case,
    Battery,
    RunCalculation,
    WallBoundary,
)
from ansys.fluent.visualization import Contour as VizContour
from ansys.fluent.visualization import Vector as VizVector
from ansys.units import VariableCatalog
from ansys.units.common import J, K, W, kg, m, ohm, s

#######################################################################################
# Launch Fluent session
# =====================================================================================
# Launch a Fluent solver session with required parameters
solver = pyfluent.Solver.from_install(precision=Precision.DOUBLE, processor_count=4)

#######################################################################################
# Download the mesh file
# =====================================================================================
# Download the battery mesh file and save it to the current working directory.
unit_battery_mesh = examples.download_file(
    "unit_battery.msh.h5",
    "pyfluent/battery_thermal_simulation",
    save_path=Path.cwd(),
)

#######################################################################################
# Read and display mesh
# =====================================================================================
#
# .. note::
#   Graphics commands like restore_view and save_picture require GUI mode.
read_case(solver, file_name=unit_battery_mesh)

# Get all the available wall boundary surfaces
all_walls = BoundaryCondition(solver).wall.get_object_names()
mesh_object = Mesh.create(solver, name="mesh-1", surfaces_list=all_walls)
mesh_object.options.edges = True
mesh_object.display()

graphics = Graphics(solver)
graphics.picture.x_resolution = 650
graphics.picture.y_resolution = 450
graphics.views.restore_view(view_name="isometric")
graphics.picture.save_picture(file_name="Single_Battery_Cell_Mesh.png")

# %%
# .. image:: ../../_static/Single_Battery_Cell_Mesh.png
#    :align: center
#    :alt: Single Battery Cell Mesh

#######################################################################################
# Configure solver settings for battery model
# =====================================================================================
# Use an unsteady first-order time solver for transient behavior.
General(solver).solver.time = "unsteady-1st-order"

#######################################################################################
# Enable the battery model
# =====================================================================================
# Activate the NTGK/DCIR model with a nominal cell capacity of 14.6 Ah.
# Enable Joule heat in passive zones and define zones and terminals.
# For a detailed guide on setting up a single battery cell,refer to the Reference_ [3].

battery = Battery(solver)
battery.enabled = True
battery.echem_model = "ntgk/dcir"
battery.zone_assignment.active_zone = ["e_zone"]
battery.zone_assignment.passive_zone = ["tab_nzone", "tab_pzone"]
battery.zone_assignment.negative_tab = ["tab_n"]
battery.zone_assignment.positive_tab = ["tab_p"]

#######################################################################################
# Define materials for cell and tabs
# =====================================================================================
#
# .. note::
#   Chemical formula values are arbitrary identifiers for demonstration.
#
# Material definition for battery cell, positive tab and negative tab. User define
# scalars are defined for e-material and positive material to specify the
# electric conductivity with ``defined-per-uds`` and ``constant`` option respectively.
#
e_material = SolidMaterial.create(
    solver,
    name="e_material",
    chemical_formula="e",
    density=2092 * kg / m**3,
    specific_heat=678 * J / (kg * K),
    thermal_conductivity=18.2 * W / (m * K),
)
e_material.uds_diffusivity.option = "defined-per-uds"
e_material.uds_diffusivity.uds_diffusivities["uds-0"] = 1190000 * m**2 / s
e_material.uds_diffusivity.uds_diffusivities["uds-1"] = 983000 * m**2 / s

p_material = SolidMaterial.create(
    solver,
    name="p_material",
    chemical_formula="pmat",
    density=8978 * kg / m**3,
    specific_heat=381 * J / (kg * K),
    thermal_conductivity=387.6 * W / (m * K),
)
p_material.uds_diffusivity.option = "constant"
p_material.uds_diffusivity = 10000000 * m**2 / s

n_material = SolidMaterial.create(
    solver,
    name="n_material",
    chemical_formula="nmat",
    density=8978 * kg / m**3,
    specific_heat=381 * J / (kg * K),
    thermal_conductivity=387.6 * W / (m * K),
)

#######################################################################################
# Assign materials to cell zones
# =====================================================================================
# Map materials to respective zones.

SolidCellZone.get(solver, name="e_zone").general.material = e_material
SolidCellZone.get(solver, name="tab_nzone").general.material = n_material
SolidCellZone.get(solver, name="tab_pzone").general.material = p_material

#######################################################################################
# Define boundary conditions
# =====================================================================================
# Set convective heat transfer on external surfaces.

wall_active = WallBoundary.get(solver, name="wall_active")
wall_active.thermal.thermal_condition = "Convection"
wall_active.thermal.heat_transfer_coeff = 5 * W / (m**2 * K)

BoundaryCondition(solver).copy(from_="wall_active", to=["wall_n", "wall_p"])

#######################################################################################
# Configure solution settings
# =====================================================================================
# Disable flow and turbulence equations, since residual criteria are set to ``none``

controls = Controls(solver)
controls.equations["flow"] = False
controls.equations["kw"] = False

monitor = Monitor(solver)
monitor.residual.options.criterion_type = "none"

#######################################################################################
# Create report definitions
# =====================================================================================
# Monitor average voltage and maximum temperature.

report_definitions = ReportDefinitions(solver)
avg_surface_voltage_report_def = report_definitions.surface.create(
    "surface_voltage",
    report_type="surface-areaavg",
    field="passive-zone-potential",
    surface_names=["tab_p"],
)

max_temp_report_def = report_definitions.volume.create(
    "max_temperature",
    report_type="volume-max",
    field=VariableCatalog.TEMPERATURE,
    cell_zones=["e_zone", "tab_nzone", "tab_pzone"],
)

surf_voltage_report_files = monitor.report_files.create(
    "surface_voltage_file",
    report_defs=["flow-time", avg_surface_voltage_report_def],
    file_name="ntgk-1c.out",
    print=True,
)

max_temp_report_file = monitor.report_files.create(
    "max_temperature_file",
    report_defs=[max_temp_report_def],
    file_name="max-temp-1c.out",
    print=True,
)

report_plots = monitor.report_plots

voltage_plot = report_plots.create(
    "surface_voltage_plot", report_defs=[avg_surface_voltage_report_def], print=True
)
voltage_plot.axes.x.number_format.precision = 0
voltage_plot.axes.y.number_format.precision = 2

temp_plot = report_plots.create(
    "max_temperature_plot", report_defs=[max_temp_report_def], print=True
)
temp_plot.axes.x.number_format.precision = 0
temp_plot.axes.y.number_format.precision = 2

#######################################################################################
# Run the simulation
# =====================================================================================

run_calc = RunCalculation(solver)
initialization = Initialization(solver)
initialization.standard_initialize()
run_calc.transient_controls.time_step_size = 30
run_calc.transient_controls.time_step_count = 100
run_calc.calculate()

#######################################################################################
# Post-process results
# =====================================================================================
# Generate contour and vector plots.

contours = [
    Contour.create(
        solver, "contour-phi+", field="cathode-potential", surfaces_list=["wall_active"]
    ),
    Contour.create(
        solver, "contour-phi-", field="anode-potential", surfaces_list=["wall_active"]
    ),
    Contour.create(
        solver,
        "contour-phi-passive",
        field="passive-zone-potential",
        surfaces_list=["tab_n", "tab_p", "wall_n", "wall_p"],
    ),
    Contour.create(
        solver,
        "contour-temp",
        field=VariableCatalog.TEMPERATURE,
        surfaces_list=["wall_p", "wall_active", "tab_p", "tab_n", "wall_n"],
    ),
]

# Create, display, and save contour plots
for idx, contour in enumerate(contours):
    # Configure contour plot
    contour.range_options.compute()

    # Set the view
    graphics.views.restore_view(view_name="front")
    #  display the  current contour
    contour.display()
    # Save the contour plot as an image
    graphics.picture.save_picture(file_name=f"Single_Battery_Cell_{idx + 1}.png")

# Create and configure vector plot
vector_plot = Vector.create(
    solver,
    name="vector-current_density",
    vector_field="current-density-j",
    field=VariableCatalog.CURRENT,
    surfaces_list=["wall_n", "wall_p", "wall_active", "tab_n", "tab_p"],
)
vector_plot.options.vector_style = "arrow"
vector_plot.range_options.compute()
# Set view, display, and save the vector plot image
graphics.views.restore_view(view_name="front")
vector_plot.display()
graphics.picture.save_picture(file_name="Single_Battery_Cell_5.png")
# Save case file for ROM simulation
write_case(solver, file_name="unit_battery.cas.h5")
# Save case and data for short circuit simulation
write_case_data(solver, file_name="ntgk")  # Save case data

# %%
# .. image:: ../../_static/Single_Battery_Cell_1.png
#    :align: center
#    :alt:  Anode Potential Contour(1C)
#
# .. image:: ../../_static/Single_Battery_Cell_2.png
#    :align: center
#    :alt:  Cathode Potential Contour(1C)
#
#
# .. image:: ../../_static/Single_Battery_Cell_3.png
#    :align: center
#    :alt:  Passive Zone Potential Contour(1C)
#
#
# .. image:: ../../_static/Single_Battery_Cell_4.png
#    :align: center
#    :alt:  Static Temperature Contour(1C)
#
#
# .. image:: ../../_static/Single_Battery_Cell_5.png
#    :align: center
#    :alt:  Current Density Vector(1C)
#


#######################################################################################
# Run simulations at different C-rates
# =====================================================================================
# Simulate at 0.5C and 5C discharge rates with adjusted time steps.

battery.eload_condition.eload_settings.crate_value = 0.5

# Get report files
report_files = monitor.report_files

# Update report file names for 0.5 c rate simulation for existing report files
report_files["surface_voltage_file"].file_name = "ntgk-0.5c.out"
report_files["max_temperature_file"].file_name = "max-temp-0.5c.out"
initialization.standard_initialize()
run_calc.transient_controls.time_step_count = 230
run_calc.calculate()

battery.eload_condition.eload_settings.crate_value = 5

# Update report file names for 5 c rate simulation for existing report files
report_files["surface_voltage_file"].file_name = "ntgk-5c.out"
report_files["max_temperature_file"].file_name = "max-temp-5c.out"
initialization.standard_initialize()
run_calc.transient_controls.time_step_count = 23
run_calc.calculate()

#######################################################################################
# Reduced Order Method (ROM) setup
# =====================================================================================
# Apply ROM for computational efficiency.

read_case(file_name="unit_battery.cas.h5")
initialization.standard_initialize()
run_calc.transient_controls.time_step_size = 30
run_calc.transient_controls.time_step_count = 3
run_calc.calculate()

battery.solution_method = "msmd-rom"
battery.solution_option.option_settings.number_substeps = 10
run_calc.transient_controls.time_step_size = 30
run_calc.transient_controls.time_step_count = 100
run_calc.calculate()

# Generate contour and vector plots for ROM results.
contours = [
    Contour.create(
        solver,
        "contour_cathode_potential",
        field="cathode-potential",
        surfaces_list=["wall_active"],
    ),
    Contour.create(
        solver,
        "contour_anode_potential",
        field="anode-potential",
        surfaces_list=["wall_active"],
    ),
    Contour.create(
        solver,
        "contour_passive_potential",
        field="passive-zone-potential",
        surfaces_list=["tab_n", "tab_p", "wall_n", "wall_p"],
    ),
    Contour.create(
        solver,
        "contour_temperature",
        field=VariableCatalog.TEMPERATURE,
        surfaces_list=["wall_p", "wall_active", "tab_p", "tab_n", "wall_n"],
    ),
]

for contour in contours:
    contour.range_options.compute()

vectors = Vector.create(
    solver,
    name="vector-current_density",
    vector_field="current-density-j",
    field="current-magnitude",
    surfaces_list=[
        "wall_n",
        "wall_p",
        "wall_active",
        "tab_n",
        "tab_p",
    ],
)
vectors.options.vector_style = "arrow"
vectors.range_options.compute()

# Set view, display, and save the vector plot image
graphics.views.restore_view(view_name="front")
vectors.display()
graphics.picture.save_picture(file_name="Single_Battery_Cell_6.png")

# %%
# .. image:: ../../_static/Single_Battery_Cell_6.png
#    :align: center
#    :alt: Current Magnitude (1C)
# Vector current density for ROM model (faster with identical results).

#######################################################################################
# Simulate short-circuit
# =====================================================================================
# Apply low external resistance and define a short-circuit region.

read_case(file_name="ntgk.cas.h5")

battery.eload_condition.eload_settings.eload_type = "specified-resistance"
battery.eload_condition.eload_settings.external_resistance = 0.5 * ohm

# Create a new cell register named "register_patch"
patch = CellRegister.create(solver, name="register_patch")
patch.type.option = "hexahedron"

# Configure the hexahedron box
patch.type.hexahedron.inside = True
patch.type.hexahedron.min_point = (-0.01, -0.01, -1.0)
patch.type.hexahedron.max_point = (0.01, 0.02, 1.0)

initialization.standard_initialize()

# Patch initialization
initialization.patch.calculate_patch(
    registers=["register_patch"],
    variable="battery-short-resistance",
    reference_frame="Relative to Cell Zone",
    use_custom_field_function=False,
    value=5e-07,
)

run_calc.transient_controls.time_step_size = 1
run_calc.transient_controls.time_step_count = 5
run_calc.calculate()

write_case_data(file_name="ntgk_short_circuit.cas.h5")


SurfaceIntegrals(solver).area_weighted_avg(
    report_of="passive-zone-potential", surface_names=["tab_p"], write_to_file=False
)
VolumeIntegrals(solver).volume_integral(
    cell_function="total-current-source", cell_zones=["e_zone"], write_to_file=False
)

vector_negative = Vector.create(
    solver,
    name="vector_negative_current",
    vector_field="current-density-jn",
    field=VariableCatalog.CURRENT,
    surfaces_list=[
        "wall_n",
        "wall_p",
        "wall_active",
    ],
)
vector_negative.options.vector_style = "arrow"
vector_negative.range_options.compute()
graphics.views.restore_view(view_name="front")
vector_negative.display()
graphics.picture.save_picture(file_name="Single_Battery_Cell_9.png")


# %%
# .. image:: ../../_static/Single_Battery_Cell_9.png
#    :align: center
#    :alt: Negative Current Vector Plot
# Negative current vector plot after short circuit.

vector_positive = Vector.create(
    solver,
    name="vector_positive_current",
    vector_field="current-density-jp",
    field=VariableCatalog.CURRENT,
    surfaces_list=[
        "wall_n",
        "wall_p",
        "wall_active",
    ],
)
vector_positive.options.vector_style = "arrow"
vector_positive.range_options.compute()

graphics.views.restore_view(view_name="front")
vector_positive.display()
graphics.picture.save_picture(file_name="Single_Battery_Cell_10.png")

# %%
# .. image:: ../../_static/Single_Battery_Cell_10.png
#    :align: center
#    :alt: Positive Current Vector Plot
# Positive current vector plot after short circuit.

temp_contour = Contour.create(
    solver, name="temperature-contour", field=VariableCatalog.TEMPERATURE
)
temp_contour.surfaces_list = all_walls
temp_contour.range_options.compute()

graphics.views.restore_view(view_name="front")
temp_contour.display()
graphics.picture.save_picture(file_name="Single_Battery_Cell_11.png")

# %%
# .. image:: ../../_static/Single_Battery_Cell_11.png
#    :align: center
#    :alt: Temperature Contour
# Temperature contour plot after short circuit.

#######################################################################################
# Close the solver
# =====================================================================================
solver.exit()

#######################################################################################
# References:
# =====================================================================================
# [1] U. S. Kim et al, "Effect of electrode configuration on the thermal behavior of
# a lithium-polymer battery", Journal of Power Sources, Volume 180 (2), pages 909-916, 2008.
#
# [2] U. S. Kim, et al., "Modeling the Dependence of the Discharge Behavior of a Lithium-Ion Battery
# on the Environmental Temperature", J. of Electrochemical Soc., Volume 158 (5), pages A611-A618, 2011.
#
# .. _Reference:
# [3] Simulating a Single Battery Cell Using the MSMD Battery Model, `Ansys Fluent documentation​ <https://ansyshelp.ansys.com/public/account/secured?returnurl=/Views/Secured/corp/v252/en/flu_tg/flu_bat_tutorial_cell.html>`_.

# sphinx_gallery_thumbnail_path = '_static/Single_Battery_Cell_4.png'
#
# .. _Reference:
# [3] Simulating a Single Battery Cell Using the MSMD Battery Model, `Ansys Fluent documentation​ <https://ansyshelp.ansys.com/public/account/secured?returnurl=/Views/Secured/corp/v252/en/flu_tg/flu_bat_tutorial_cell.html>`_.

# sphinx_gallery_thumbnail_path = '_static/Single_Battery_Cell_4.png'
