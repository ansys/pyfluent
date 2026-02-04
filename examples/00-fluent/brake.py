# /// script
# dependencies = [
#   "ansys-fluent-core",
#   "ansys-fluent-visualization",
#   "matplotlib",
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
#################################
Automotive Brake Thermal Analysis
#################################

Objective:
==========

Braking surfaces get heated due to frictional heating during braking.
High temperature affects the braking performance and life of the braking system.
This example demonstrates:

* Fluent setup and simulation using PyFluent
* Post processing using PyVista (3D Viewer) and Matplotlib (2D graphs)

"""

####################################################################################
# Import required libraries/modules
# ==================================================================================

import csv
import itertools
from pathlib import Path

from ansys.units import VariableCatalog
import matplotlib.pyplot as plt

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.core.generated.solver.settings_242 import report_type
from ansys.fluent.core.generated.solver.settings_builtin_261 import read_case, write_case_data
from ansys.fluent.visualization import Contour, GraphicsWindow
from ansys.fluent.core.generated.solver.settings_builtin import Controls, Graphics
from ansys.fluent.core.solver import (
    Energy,
    General,
    SolidCellZone,
    WallBoundary,
    ReportDefinitions,
    Monitor,
    Initialization,
    RunCalculation,
)
from ansys.units.common import K, m, W, radian, s

import_filename = examples.download_file(
    "brake.msh.h5",
    "pyfluent/examples/Brake-Thermal-PyVista-Matplotlib",
    save_path=Path.cwd(),
)

####################################################################################
# Fluent Solution Setup
# ==================================================================================

####################################################################################
# Launch Fluent session with solver mode and print Fluent version
# ---------------------------------------------------------------

solver = pyfluent.Solver.from_install(precision="double", processor_count=2, dimension=3)
print(solver.get_fluent_version())

####################################################################################
# Import mesh
# ------------

read_case(solver, file_name=import_filename)

############################
# Define models and material
# --------------------------
energy = Energy(solver)
energy.enabled = True

general = General(solver)
general.solver.time = "unsteady-2nd-order-bounded"

Materials(solver).database.copy_by_name(type="solid", name="steel")

#########################################
# Solve only energy equation (conduction)
# ---------------------------------------
controls = Controls(solver)
controls.equations["kw"] = False  # Turbulence
controls.equations["flow"] = False  # Flow
controls.equations["temperature"] = True  # Energy

##########################################################################################
# Define disc rotation
# --------------------
discs = SolidCellZone.get(solver, name="disc*")
discs.solid_motion.enable = True
discs.solid_motion.solid_motion_zone_motion_function = "none"
discs.solid_motion.solid_motion_axis_direction = [0, 1, 0]
discs.solid_motion.solid_motion_axis_origin = [-0.035, -0.821, 0.045] * m
discs.solid_motion.solid_motion_velocity = [0, 0, 0] * m / s
discs.solid_motion.solid_omega = (
    -15.79 * radian / s
)  # 100 km/h car speed with 0.28 m of axis height from ground
discs.solid_motion.solid_relative_to_thread = "absolute"

##########################################################################################
# Apply frictional heating on pad-disc surfaces
# ----------------------------------------------
# Wall thickness 0f 2 mm has been assumed and 2e9 w/m3 is the heat generation which
# has been calculated from kinetic energy change due to braking.
wall_pad_discs = WallBoundary.get(solver, name="wall-pad-disc*")
wall_pad_discs.thermal.q_dot = 2e9 * W / m**3
wall_pad_discs.thermal.wall_thickness = 0.002 * m

##########################################################################################
# Apply convection cooling on outer surfaces due to air flow
# -----------------------------------------------------------
# Outer surfaces are applied a constant htc of 100 W/(m2 K)
# and 300 K free stream temperature

walls = WallBoundary.get(solver, name="wall-disc*|wall-geom*")
walls.thermal.thermal_condition = walls.thermal.thermal_condition.CONVECTION
walls.thermal.convection.convective_heat_transfer_coefficient = 100 * W / (m**2 * K)
walls.thermal.convection.free_stream_temperature = 300 * K

##########################################################################################
# Initialize
# ----------
# Initialize with 300 K temperature
initialization = Initialization(solver)
initialization.initialization_type = "standard"
initialization.standard_initialize()

###############################################################################################
# Post processing setup
# ---------------------
# * Report definitions and monitor plots
# * Set contour plot properties
# * Set views and camera
# * Set animation object

report_defs = ReportDefinitions(solver)

max_pad_temp = report_defs.volume.create(name="max-pad-temperature", report_type="volume-max", field=VariableCatalog.TEMPERATURE, cell_zones=["geom-1-innerpad", "geom-1-outerpad"])


max_disc_temp = report_defs.volume.create(name="max-disc-temperature",
report_type = "volume-max",
field = "temperature",
cell_zones = ["disc1", "disc2"],)

monitor = Monitor(solver)
temp_plot = monitor.report_plots.create(name="max-temperature")
temp_plot.report_defs = [max_pad_temp, max_disc_temp]

temp_file = monitor.report_files.create(name="max-temperature",
report_defs = [max_pad_temp, max_disc_temp, "flow-time"],
file_name = "max-temperature.out")


graphics = Graphics(solver)
temp_contour = graphics.contour.create(name="temperature",
field = VariableCatalog.TEMPERATURE,
surfaces_list = "wall*")

temp_contour.color_map.visible = True
temp_contour.color_map.size = 100
temp_contour.color_map.color = "field-velocity"
temp_contour.color_map.log_scale = False
temp_contour.color_map.format = "%0.1f"
temp_contour.color_map.user_skip = 9
temp_contour.color_map.show_all = True
temp_contour.color_map.position = 1
temp_contour.color_map.font_name = "Helvetica"
temp_contour.color_map.font_automatic = True
temp_contour.color_map.font_size = 0.032
temp_contour.color_map.length = 0.54
temp_contour.color_map.width = 6
temp_contour.color_map.bground_transparent = True
temp_contour.color_map.bground_color = "#CCD3E2"
temp_contour.color_map.title_elements = "Variable and Object Name"

# range configuration
temp_contour.range.option = "auto-range-off"
temp_contour.range.auto_range_off.minimum = 300.0
temp_contour.range.auto_range_off.maximum = 400.0
temp_contour.range.auto_range_off.clip_to_range = False

# views / camera
graphics.restore_view(view_name="top")
graphics.views.camera.zoom(factor=2)
graphics.views.save_view(view_name="animation-view")

solver.solution.calculation_activity.solution_animations.create(
    name="animate-temperature",
animate_on = "temperature",
frequency_of = "flow-time",
flow_time_frequency = 0.05,
view = "animation-view",)

##################################################################################################
# Run simulation
# ---------------
# * Run simulation for 2 seconds flow time
# * Set time step size
# * Set number of time steps and maximum number of iterations per time step
run_calc = RunCalculation(solver)
run_calc.transient_controls.time_step_size = 0.01
run_calc.dual_time_iterate(time_step_count=200, max_iter_per_step=5)

##################################################################################################
# Save simulation data
# --------------------
# Write case and data files
write_case_data(solver, file_name="brake-final.cas.h5")

###############################################
# Post processing with PyVista (3D visualization)
# ===============================================

###############################################
# Temperature contour object
# --------------------------
contour1_surfaces = [
    "wall-disc1",
    "wall-disc2",
    "wall-pad-disc2",
    "wall_pad-disc1",
    "wall-geom-1-bp_inner",
    "wall-geom-1-bp_outer",
    "wall-geom-1-innerpad",
    "wall-geom-1-outerpad",
]
contour1 = Contour(solver=solver, field="temperature", surfaces=contour1_surfaces)

###############################################
# Set contour properties
# ----------------------

contour1.range.option = "auto-range-off"
contour1.range.auto_range_off.minimum = 300
contour1.range.auto_range_off.maximum = 400

###############################################
# Display contour
# ---------------

window = GraphicsWindow()
window.add_graphics(contour1)
window.show()

# %%
# .. image:: ../../_static/brake_surface_temperature.png
#    :align: center
#    :alt: Brake Surface Temperature Contour

# %%
#    Brake Surface Temperature

###############################################
# Post processing with Matplotlib (2D graph)
# ===============================================

###############################################
# Read monitor file
# -----------------

X = []
Y = []
Z = []

with (Path.cwd() / "max-temperature.out").open() as datafile:
    for rows in csv.reader(
        itertools.islice(datafile, 3, -1),  # skip header lines
        delimiter=" ",
    ):
        X.append(float(rows[3]))
        Y.append(float(rows[2]))
        Z.append(float(rows[1]))

###############################################
# Plot graph
# ----------


plt.title("Maximum Temperature", fontdict={"color": "darkred", "size": 20})
plt.plot(X, Z, label="Max. Pad Temperature", color="red")
plt.plot(X, Y, label="Max. Disc Temperature", color="blue")
plt.xlabel("Time (sec)")
plt.ylabel("Max Temperature (K)")
plt.legend(loc="lower right", shadow=True, fontsize="x-large")

###############################################
# Show graph
# ----------

plt.show()

# %%
# .. image:: ../../_static/brake_maximum_temperature.png
#    :align: center
#    :alt: Brake Maximum Temperature

# %%
#    Brake Maximum Temperature

####################################################################################
# Close the session
# ==================================================================================

solver.exit()

# sphinx_gallery_thumbnail_path = '_static/brake_surface_temperature-thumbnail.png'
