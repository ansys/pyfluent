# /// script
# dependencies = [
#   "ansys-fluent-core",
#   "ansys-fluent-visualization",
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
#
# The example demonstrates the following:
#
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
from pathlib import Path

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.core.solver import (
    BoundaryConditions,
    FluidCellZone,
    General,
    Initialization,
    MassFlowOutlet,
    Materials,
    MeshInterfaces,
    Methods,
    Monitor,
    NamedExpression,
    PlaneSurface,
    PressureInlet,
    ReportDefinitions,
    ReportPlot,
    RunCalculation,
    Setup,
    Viscous,
    WallBoundary,
    write_case,
    write_case_data,
)
from ansys.fluent.visualization import Contour, Graphics
from ansys.units import VariableCatalog
from ansys.units.common import Pa, kg, m, s

################################################################################################################
# Download the mesh file
# ==============================================================================================================

# Download the mesh file from the examples repository
# Impeller and volute mesh files
impeller_mesh = examples.download_file(
    "impeller.msh.h5",
    "pyfluent/examples/pump-volute",
    save_path=Path.cwd(),
)

volute_mesh = examples.download_file(
    "volute.msh.h5",
    "pyfluent/examples/pump-volute",
    save_path=Path.cwd(),
)


################################################################################################################
# Define Constants
# ==============================================================================================================

density_water = 998.2 * kg / m**3
viscosity_water = 0.001002 * Pa * s
g = 9.81 * m / s**2
impeller_speed = 1450  # rpm
# Convert to rad/s
impeller_speed_rad = impeller_speed * 2 * math.pi / 60

################################################################################################################
# Launch Fluent with solver mode and print Fluent version
# ==============================================================================================================

solver = pyfluent.Solver.from_install(
    processor_count=4,
    cleanup_on_exit=True,
)
print(solver.get_fluent_version())

# upload mesh files to the solver
solver.upload(impeller_mesh)
solver.upload(volute_mesh)


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
graphics = Graphics(solver)

# Create a mesh object and configure its settings
mesh_object = graphics.mesh.create(name="mesh-1")
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

general = General(solver)
general.units.set_units(quantity="angular-velocity", units_name="rev/min")

################################################################################################################
# Define the Viscous Model
# ==============================================================================================================

# Models setting
viscous = Viscous(solver)
viscous.model = viscous.model.K_OMEGA
viscous.k_omega_model = viscous.k_omega_model.SST

################################################################################################################
# Define Materials
# ==============================================================================================================
Materials(solver).database.copy_by_name(type="fluid", name="water-liquid")

################################################################################################################
# Define Cell Zone Conditions
# ==============================================================================================================

impeller_cell_zone = FluidCellZone.get(solver, name="impeller")
impeller_cell_zone.general.material = "water-liquid"

impeller_cell_zone.reference_frame.reference_frame_axis_origin = (0, 0, 0)
impeller_cell_zone.reference_frame.reference_frame_axis_direction = (0, 0, 1)
impeller_cell_zone.reference_frame.frame_motion = True

impeller_cell_zone.reference_frame.mrf_omega = impeller_speed_rad


volute_cell_zone = FluidCellZone.get(solver, name="volute")
volute_cell_zone.general.material = "water-liquid"


# Boundary Conditions
impeller_hub = WallBoundary.get(solver, name="impeller-hub")
impeller_hub.momentum.wall_motion = impeller_hub.momentum.wall_motion.MOVING_WALL
impeller_hub.momentum.relative = True
impeller_hub.momentum.velocity_spec = impeller_hub.momentum.velocity_spec.ROTATIONAL

inblock_shroud = WallBoundary.get(solver, name="inblock-shroud")
inblock_shroud.momentum.wall_motion = inblock_shroud.momentum.wall_motion.MOVING_WALL
inblock_shroud.momentum.relative = False
inblock_shroud.momentum.velocity_spec = "Rotational"

################################################################################################################
# Define Boundary Conditions
# ==============================================================================================================

# Inlet Boundary Condition
pressure_inlet = PressureInlet.get(solver, name="inlet")
pressure_inlet.momentum.supersonic_or_initial_gauge_pressure = -100 * Pa

# It seems, need to change the boundary condition to mass flow outlet
BoundaryConditions(solver).set_zone_type(
    zone_list=["mass-flow-inlet-11"], new_type="mass-flow-outlet"
)
# Outlet Boundary Condition

mass_flow_outlet = MassFlowOutlet.get(solver, name="mass-flow-inlet-11")
mass_flow_outlet.momentum.mass_flow_rate.value = 90 * kg / s


# Create a turbo interfaces
# enable the turbo models
turbo_models = Setup(solver).turbo_models
turbo_models.enabled = True

impeller_volute_interface = MeshInterfaces(solver).turbo_create.create(
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
methods = Methods(solver)
methods.spatial_discretization.gradient_scheme = "green-gauss-node-based"
methods.high_order_term_relaxation.enable = True

################################################################################################################
# Define Named Expressions
# ==============================================================================================================

pump_head = NamedExpression.create(
    solver,
    name="head",
    definition="(({p-out} - {p-in}) / (998.2 [kg/m^3] * 9.81[m/s^2]))",
    output_parameter=True,
)


################################################################################################################
# Define Report Definitions
# ==============================================================================================================

monitor = Monitor(solver)
report_definitions = ReportDefinitions(solver)

# Create a report definition
# p-out
outlet_pressure_report_def = report_definitions.surface.create(
    "p-out",
    report_type="surface-massavg",
    surface_names=["mass-flow-inlet-11"],
    field="total-pressure",
    per_surface=False,
)

outlet_pressure_report_plot = ReportPlot(
    solver, name="p-out-rplot", report_defs="p-out"
)

outlet_pressure_report_file = ReportPlot(
    solver, name="p-out-rfile", report_defs="p-out"
)

# p-in
inlet_pressure_report_def = report_definitions.surface.create(
    "p-in",
    report_type="surface-massavg",
    surface_names=["inlet"],
    field="total-pressure",
    per_surface=False,
)


# Pump Head
pump_head_report_def = report_definitions.single_valued_expression.create("pump-head")

pump_head_report_def.definition = "head"

# report plot
pump_head_report_plot = monitor.report_plots.create(
    "pump-head-rplot", report_defs=pump_head_report_def
)

# report file
pump_head_report_file = monitor.report_files.create(
    "pump-head-rfile", report_defs=pump_head_report_def
)

# p-blade
blade_pressure_report_def = report_definitions.surface.create(
    "p-blade",
    report_type="surface-massavg",
    surface_names=["blade"],
    field="pressure",
    per_surface=False,
)

################################################################################################################
# Initialization and run solver
# ==============================================================================================================
initialization = Initialization(solver)
initialization.reference_frame = "absolute"
initialization.hybrid_init_options.general_settings.initialization_options.initial_pressure = (
    True
)
initialization.hybrid_initialize()

# Run calculation settings
run_calculation = RunCalculation(solver)
run_calculation.pseudo_time_settings.time_step_method.time_step_size_scale_factor = 10
run_calculation.iter_count = 200

# Write the case file
write_case(solver, file_name="pump_volute_setup.cas.h5")
# Run the calculation
run_calculation.calculate()

################################################################################################################
# Post-Processing Workflow
# ==============================================================================================================

# Create a mid-plane surface at z = -0.015 m
z_mid_plane = PlaneSurface.create(
    solver, name="z_mid_plane", method="xy-plane", z=-0.015
)
z_mid_plane.display()

# Define and display the contour for static pressure using typed API
graphics = Graphics(solver)
pressure_contour = Contour.create(
    solver=solver, field=VariableCatalog.PRESSURE, surfaces=["z_mid_plane"]
)
pressure_contour.display()
graphics.views.restore_view(view_name="front")
graphics.views.auto_scale()
graphics.picture.save_picture(file_name="static-pressure-contour.png")


# %%
# .. image:: ../../_static/static-pressure-contour.png
#    :align: center
#    :alt: Static Pressure Contour

################################################################################################################
# Save the case file
# ==============================================================================================================
write_case_data(solver, file_name="pump_volute_setup_solved.cas.h5")

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
