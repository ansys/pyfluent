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

""".. _frozen_rotor_simulation:

Impeller-Volute simulation using the Frozen Rotor Approach
----------------------------------------------------------------------
"""

################################################################################################################
# Objective
# ==============================================================================================================
#
# This example demonstrates how to set up a CFD simulation of an impeller and volute using
# the frozen rotor approach. The frozen rotor approach is a technique used in computational
# fluid dynamics (CFD) to simulate the flow around rotating machinery, such as pumps,
# turbines, and compressors. In this approach, the rotor is treated as a stationary
# component, while the surrounding fluid is allowed to move. This allows for a more
# efficient simulation of the flow field, as the rotor's motion does not need to be
# explicitly modeled. The frozen rotor approach is particularly useful for simulating
# steady-state flows, where the rotor's motion is constant.
# By using this approach, engineers can obtain accurate predictions of the
# flow field and performance characteristics of rotating machinery without the need for
# complex and computationally expensive simulations.
#
#
# .. image:: ../../_static/pump-volute-geom.png
#    :align: center
#    :alt: Pump Volute Geometry View

################################################################################################################
# Outline
# ==============================================================================================================

# The example demonstrates the following:

# *Overview & Problem description
# *Launching Fluent in solver mode.
# *Downloading a mesh files from the examples repository.
# *Initial setup
# *Mesh configuration
# *Model selection & Material definition
# *Defining cell zone conditions & boundary conditions
# *Turbomachinery configuration
# *Solver settings
# *Report definitions
# *Initialization
# *Running the simulation
# *Post-processing the results
# *Visualizing the results
# *Saving the case file
# *Closing the solver


################################################################################################################
# Import required libraries/modules
# ==============================================================================================================
import math

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples

################################################################################################################
# Download the mesh file
# ==============================================================================================================

# Download the mesh file from the examples repository
# Impeller and volute mesh files
impeller_mesh = examples.download_file(
    "impeller.msh.h5",
    "pyfluent/examples/pump-volute",
)

volute_mesh = examples.download_file(
    "volute.msh.h5",
    "pyfluent/examples/pump-volute",
)

################################################################################################################
# Define Constants
# ==============================================================================================================

density_water = 998.2  # kg/m^3
viscosity_water = 0.001002  # kg/(m.s)
g = 9.81  # m/s^2
# Impeller speed
impeller_speed = 1450  # rpm
# Convert to rad/s
impeller_speed_rad = impeller_speed * 2 * math.pi / 60  # rad/s

################################################################################################################
# Launch Fluent with solver mode and print Fluent version
# ==============================================================================================================

solver = pyfluent.launch_fluent(
    mode="solver",
    ui_mode="gui",
    processor_count=4,
    cleanup_on_exit=True,
)
print(solver.get_fluent_version())


################################################################################################################
# Read, append the mesh files
# ==============================================================================================================

# Read Impeller mesh file
solver.settings.file.read_mesh(file_name=impeller_mesh)
# Append Volute mesh file
solver.settings.mesh.modify_zones.append_mesh(file_name=volute_mesh)

################################################################################################################
# Display the mesh
# ==============================================================================================================

# Access the graphics object
graphics = solver.settings.results.graphics

# Create a mesh object and configure its settings
mesh_object = solver.settings.results.graphics.mesh.create(name="mesh-1")
mesh_object.surfaces_list = [
    "inlet",
    "mass-flow-inlet-11",
    "interface-impeller-outlet",
    "interface-volute-inlet",
    "blade",
    "impeller-hub",
    "impeller-shroud",
    "inblock-hub",
    "inblock-shroud",
    "volute-inlet-wall",
    "volute-wall",
]
mesh_object.options.edges = True


# Set the hardcopy format for saving the image
graphics.picture.driver_options.hardcopy_format = "png"

graphics.views.restore_view(view_name="front")
mesh_object.display()
graphics.views.auto_scale()
graphics.picture.save_picture(
    file_name="pump-volute-mesh.png",
)


# %%
# .. image:: ../../_static/pump-volute-mesh.png
#    :align: center
#    :width: 650px
#    :height: 400px
#    :alt: Pump Volute Mesh

################################################################################################################
# Set the unit for angular velocity, rad/s to rev/min
# ==============================================================================================================

solver.settings.setup.general.units.set_units(
    quantity="angular-velocity", units_name="rev/min"
)

################################################################################################################
# Define the Viscous Model
# ==============================================================================================================

# Models setting
viscous = solver.settings.setup.models.viscous
viscous = solver.settings.setup.models.viscous
viscous.model = "k-omega"
viscous.k_omega_model = "sst"

################################################################################################################
# Define Materials
# ==============================================================================================================
solver.settings.setup.materials.database.copy_by_name(type="fluid", name="water-liquid")

################################################################################################################
# Define Cell Zone Conditions
# ==============================================================================================================

impeller_cell_zone = solver.settings.setup.cell_zone_conditions.fluid["impeller"]
impeller_cell_zone.general.material = "water-liquid"

impeller_cell_zone.reference_frame.reference_frame_axis_origin = [0, 0, 0]
impeller_cell_zone.reference_frame.reference_frame_axis_direction = [0, 0, 1]
impeller_cell_zone.reference_frame.frame_motion = True

# impeller rotation
impeller_cell_zone.reference_frame.mrf_omega.value = impeller_speed_rad


# Volute Cell Zone Conditions
volute_cell_zone = solver.settings.setup.cell_zone_conditions.fluid["volute"]
volute_cell_zone.general.material = "water-liquid"


# Boundary Conditions
# impeller hub
impeller_hub = solver.settings.setup.boundary_conditions.wall["impeller-hub"].momentum
impeller_hub.wall_motion = "Moving Wall"
impeller_hub.relative = True
impeller_hub.velocity_spec = "Rotational"

#  inblock-shroud

inblock_shroud = solver.settings.setup.boundary_conditions.wall[
    "inblock-shroud"
].momentum
inblock_shroud.wall_motion = "Moving Wall"
inblock_shroud.relative = False
inblock_shroud.velocity_spec = "Rotational"

################################################################################################################
# Define Boundary Conditions
# ==============================================================================================================

# Inlet Boundary Condition
pressure_inlet = solver.settings.setup.boundary_conditions.pressure_inlet["inlet"]
pressure_inlet.momentum.supersonic_or_initial_gauge_pressure.value = -100

# It seems, need to change the boundary condition to mass flow outlet
solver.settings.setup.boundary_conditions.set_zone_type(
    zone_list=["mass-flow-inlet-11"], new_type="mass-flow-outlet"
)
# Outlet Boundary Condition

mass_flow_outlet = solver.settings.setup.boundary_conditions.mass_flow_outlet[
    "mass-flow-inlet-11"
]
mass_flow_outlet.momentum.mass_flow_rate.value = 90  # kg/s


# Create a turbo interfaces
# enable the turbo models
solver.settings.setup.turbo_models.enabled = True

impeller_volute_interface = solver.settings.setup.mesh_interfaces.turbo_create.create(
    adjacent_cell_zone_1="impeller",
    adjacent_cell_zone_2="volute",
    mesh_interface_name="imp-volute-interface",
    turbo_choice="No-Pitch-Scale",
    zone1="interface-impeller-outlet",
    zone2="interface-volute-inlet",
)

################################################################################################################
# Define Solver Settings
# ==============================================================================================================
methods = solver.settings.solution.methods
methods.spatial_discretization.gradient_scheme = "green-gauss-node-based"
methods.high_order_term_relaxation.enable = True

################################################################################################################
# Define Named Expressions
# ==============================================================================================================

pump_head = solver.settings.setup.named_expressions.create("head")
pump_head.definition = "(({p-out} - {p-in}) / (998.2 [kg/m^3] * 9.81[m/s^2]))"
pump_head.output_parameter = True


################################################################################################################
# Define Report Definitions
# ==============================================================================================================

# Create a report definition
# p-out
outlet_pressure_report_def = solver.settings.solution.report_definitions.surface.create(
    "p-out"
)
outlet_pressure_report_def.report_type = "surface-massavg"
outlet_pressure_report_def.surface_names = ["mass-flow-inlet-11"]
outlet_pressure_report_def.field = "total-pressure"
outlet_pressure_report_def.per_surface = False

outlet_pressure_report_plot = solver.settings.solution.monitor.report_plots.create(
    "p-out-rplot"
)
outlet_pressure_report_plot.report_defs = "p-out"

outlet_pressure_report_file = solver.settings.solution.monitor.report_files.create(
    "p-out-rfile"
)
outlet_pressure_report_file.report_defs = "p-out"

# p-in
inlet_pressure_report_def = solver.settings.solution.report_definitions.surface.create(
    "p-in"
)
inlet_pressure_report_def.report_type = "surface-massavg"
inlet_pressure_report_def.surface_names = ["inlet"]
inlet_pressure_report_def.field = "total-pressure"
inlet_pressure_report_def.per_surface = False


# Pump Head
pump_head_report_def = (
    solver.settings.solution.report_definitions.single_valued_expression.create(
        "pump-head"
    )
)

pump_head_report_def.definition = "head"

# report plot
pump_head_report_plot = solver.settings.solution.monitor.report_plots.create(
    "pump-head-rplot"
)
pump_head_report_plot.report_defs = "pump-head"

# report file
pump_head_report_file = solver.settings.solution.monitor.report_files.create(
    "pump-head-rfile"
)
pump_head_report_file.report_defs = "pump-head"

# p-blade
blade_pressure_report_def = solver.settings.solution.report_definitions.surface.create(
    "p-blade"
)
blade_pressure_report_def.report_type = "surface-massavg"
blade_pressure_report_def.surface_names = ["blade"]
blade_pressure_report_def.field = "pressure"
blade_pressure_report_def.per_surface = False


################################################################################################################
# Initialization and run solver
# ==============================================================================================================
initialization = solver.settings.solution.initialization
initialization.reference_frame = "absolute"
initialization.hybrid_init_options.general_settings.initialization_options.initial_pressure = (
    True
)
initialization.hybrid_initialize()

# Run calculation settings
run_calculation = solver.settings.solution.run_calculation
run_calculation.pseudo_time_settings.time_step_method.time_step_size_scale_factor = 10
run_calculation.iter_count = 200

# Write the case file
solver.settings.file.write(file_type="case", file_name="pump_voulte_setup.cas.h5")
# Run the calculation
run_calculation.calculate()

################################################################################################################
# Post-Processing Workflow
# ==============================================================================================================

# Create a mid-plane surface at z = -0.015 m
z_mid_plane = solver.settings.results.surfaces.plane_surface.create(name="z_mid_plane")
z_mid_plane.method = "xy-plane"
z_mid_plane.z = -0.015
z_mid_plane.display()

# Define the contour for static pressure
pressure_contour = solver.settings.results.graphics.contour.create(
    name="static-pressure-contour"
)
pressure_contour.field = "pressure"
pressure_contour.surfaces_list = ["z_mid_plane"]

# Display the contour and save the image

graphics.views.restore_view(view_name="front")
pressure_contour.display()
graphics.views.auto_scale()
graphics.picture.save_picture(file_name="static-pressure-contour.png")


# %%
# .. image:: ../../_static/static-pressure-contour.png
#    :align: center
#    :alt: Static Pressure Contour

################################################################################################################
# Save the case file
# ==============================================================================================================
solver.settings.file.write(
    file_type="case-data", file_name="pump_volute_setup_solved.cas.h5"
)

################################################################################################################
# Close the session
# ==============================================================================================================
solver.exit()

################################################################################################################
# References
# ==============================================================================================================
#
# [1] Ansys Fluent User's Guide, Release 2025R1

# sphinx_gallery_thumbnail_path = '_static/static-pressure-contour.png'
