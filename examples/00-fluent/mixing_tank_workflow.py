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

""".. _mixing_tank_workflow:

Mixing Tank Workflow
-------------------------------------------
"""
#############################################################################################################
# Overview
# ===========================================================================================================
#
# The mixing tank workflow demonstrates basic end to end comprehensive solution for simulating
# mixing tank with an single impeller. This workflow also demonstrates the use of the Python API's
# capabilities to setup complex workflows.
#
# Mixing tanks are commonly used in industries such as chemical processing, food and healthcare,
# pharmaceuticals etc. The mixing tank workflow in ANSYS Fluent allows engineers to analyze the
# performance of mixing tanks, optimize the design of impellers, and understand the flow
# patterns within the tank. By simulating the mixing process, engineers can gain insights
# into the efficiency of mixing, blend time, the distribution of shear forces, and the overall
# performance of the mixing system.
#
# This workflow can be extended to design and develop the vertical application for non-experts
# and seemingly expose the required functionality to democraticize the simulation process.
#
#
# The workflow includes:
#
#  * Importing a geometry file
#  * Generating the mesh
#  * Setting up the solver
#  * Defining the materials
#  * Defining the cell zones and wall boundary conditions
#  * Setting up the solution methods and controls
#  * Defining the report definitions
#  * Running the solver
#  * Post-processing the results
#  * Saving the case file
#  * Closing the session
#
# .. image:: ../../_static/mixing_tank_geom_view.png
#    :align: center
#    :scale: 60%
#    :alt: Mixing Tank Model


#############################################################################################################
# Import required libraries/modules
# ===========================================================================================================

import fnmatch
from pathlib import Path
import platform

from ansys.units import VariableCatalog

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.core.generated.solver.settings_builtin import (
    BoundaryCondition,
    Mesh,
    PlaneSurface,
    ReportFile,
    ReportPlot,
    Residual,
)
from ansys.fluent.core.generated.solver.settings_builtin_261 import write_case, write_case_data
from ansys.fluent.core.solver import (
    BoundaryConditions,
    Contour,
    FluidCellZone,
    FluidMaterial,
    General,
    Initialization,
    ReportDefinitions,
    RunCalculation,
    Solution,
    WallBoundary,
)
from ansys.fluent.core.solver import FluidCellZones, Graphics
from ansys.units.common import kg, m, s

#############################################################################################################
# Launch Fluent session with meshing mode and print Fluent version
# ===========================================================================================================
meshing = pyfluent.Meshing.from_install(
    cleanup_on_exit=True,
)
print(meshing.get_fluent_version())

#############################################################################################################
# Meshing Workflow
# ===========================================================================================================
workflow = meshing.workflow

filenames = {
    "Windows": "mixing_tank_geom.dsco",
    "Other": "StirredTank.scdoc.pmdb",
}

geometry_filename = examples.download_file(
    filenames.get(platform.system(), filenames["Other"]),
    "pyfluent/examples/MixingTank-WorkFlow",
    save_path=Path.cwd(),
)

# upload the geometry to the meshing session
meshing.upload(geometry_filename)

workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
workflow.TaskObject["Import Geometry"].Arguments = {"FileName": geometry_filename}
workflow.TaskObject["Import Geometry"].Execute()

workflow.TaskObject["Generate the Surface Mesh"].Execute()
workflow.TaskObject["Describe Geometry"].Arguments = {
    "SetupType": "The geometry consists of only fluid regions with no voids",
    "wall_to_internal": "Yes",
    "InvokeShareTopology": "Yes",
}
workflow.TaskObject["Describe Geometry"].Execute()
workflow.TaskObject["Apply Share Topology"].Execute()
workflow.TaskObject["Update Boundaries"].Execute()
workflow.TaskObject["Update Regions"].Execute()
workflow.TaskObject["Add Boundary Layers"].InsertCompoundChildTask()
workflow.TaskObject["smooth-transition_1"].Execute()
workflow.TaskObject["Generate the Volume Mesh"].Execute()

# Write a mesh file for reference
meshing.tui.file.write_mesh("mixing_tank.msh.h5")

#############################################################################################################
# Switch to the Solver Mode
# ===========================================================================================================
solver = meshing.switch_to_solver()


###############################################################################################################
# Display the mesh in solver mode
# ===========================================================================================================

# Create a middle plane to display the mesh
y_mid_plane = PlaneSurface.create(method="zx-plane", y=0 * m)
y_mid_plane.display()


# Access the graphics object
graphics = Graphics(solver)
# Set the hardcopy format for saving the image
graphics.picture.driver_options.hardcopy_format = "png"

# View settings
geom_view = graphics.views.display_states.create(
    "geom_view", front_faces_transparent="enable", view_name="top"
)

# Get the list of all walls
all_walls = BoundaryConditions(solver).wall.get_object_names()
filtered_walls_to_display = [wall for wall in all_walls if "mrf" not in wall]

# Create a mesh object and configure its settings
mesh_object = Mesh.create(solver, surfaces_list=filtered_walls_to_display)
mesh_object.options.edges = False

mesh_object.display_state_name = geom_view.name()
mesh_object.coloring.option = "manual"
mesh_object.display()
graphics.views.auto_scale()


graphics.picture.save_picture(
    file_name="mixing_tank_geom_view.png",
)


mesh_object.surfaces_list = y_mid_plane.name()
mesh_object.options.edges = True
mesh_object.display()
graphics.views.auto_scale()

graphics.picture.save_picture(
    file_name="mixing_tank_mesh.png",
)

geom_view.front_faces_transparent = "disable"

# %%
# .. image:: ../../_static/mixing_tank_mesh.png
#    :align: center
#    :scale: 60%
#    :alt: Mixing Tank Mesh
#############################################################################################################
# Define Constants
# ===========================================================================================================
g = 9.81 * m / s**2
water_density = 1000.0 * kg / m**3
water_viscosity = 0.001 * kg / (m * s)
agitation_speed = 10 / s

#############################################################################################################
# Solver Setup and Solve Workflow
# ===========================================================================================================
general = General(solver)
general.operating_conditions.gravity.enable = True
general.operating_conditions.gravity.components = [0.0, 0.0, -g]

#############################################################################################################
# Define Materials
# ===========================================================================================================
Materials(solver).database.copy_by_name(type="fluid", name="water-liquid")
fluid_mat = FluidMaterial.get(
    solver, name="water-liquid", density=water_density, viscosity=water_viscosity
)

#############################################################################################################
# Define Cell Zones, Wall Boundary Conditions
# ===========================================================================================================

# Get the list of all Fluid Cell Zones
fluid_cell_zones = FluidCellZones(solver).get_object_names()
fluid_mrf_cell_zones = [zone for zone in fluid_cell_zones if "mrf" in zone]

for cell_zone in fluid_mrf_cell_zones:
    print(cell_zone)
    fluid_cell_zone = FluidCellZone.get(solver, name=cell_zone)
    fluid_cell_zone.general.material = "water-liquid"
    fluid_cell_zone.reference_frame.reference_frame_axis_origin = (0, 0, 0.4 * m)
    fluid_cell_zone.reference_frame.reference_frame_axis_direction = (0, 0, -1)
    fluid_cell_zone.reference_frame.frame_motion = True
    fluid_cell_zone.reference_frame.mrf_omega.value = agitation_speed

stationary_names = [zone for zone in fluid_cell_zones if "mrf" not in zone]
if stationary_names:
    stationary_zone = FluidCellZone(solver, name=stationary_names[0])
    stationary_zone.general.material = "water-liquid"

# Wall boundary conditions
wall_shaft = [wall for wall in all_walls if "shaft" in wall]

for wall in wall_shaft:
    print(wall)
    wall_boundary = WallBoundary.get(solver, name=wall)
    wall_boundary.momentum.wall_motion = "Moving Wall"
    wall_boundary.momentum.relative = False
    wall_boundary.momentum.rotating = True
    wall_boundary.momentum.rotation_axis_direction = (0, 0, -1)
    wall_boundary.momentum.rotation_speed = agitation_speed


liquid_level_bc = WallBoundary.get(solver, name="wall_liquid_level")
liquid_level_bc.momentum.wall_motion = "Stationary Wall"
liquid_level_bc.momentum.shear_condition = "Specified Shear"

# Change the Zone type for internal walls to interior
BoundaryConditions(solver).set_zone_type(
    zone_list=["fluid_mrf_1-fluid_tank"], new_type="interior"
)

#############################################################################################################
# Solution Methods and Controls
# ===========================================================================================================
solution = Solution(solver)
solution.methods.p_v_coupling.flow_scheme = "SIMPLE"
solution.methods.spatial_discretization.discretization_scheme["pressure"] = "presto!"
solution.controls.under_relaxation["pressure"] = 0.5
solution.controls.under_relaxation["mom"] = 0.3
solution.controls.under_relaxation["k"] = 0.6
solution.controls.under_relaxation["omega"] = 0.6
solution.controls.under_relaxation["turb-viscosity"] = 0.6

##############################################################################################################
#  Residuals Criteria & Initialization
# ===========================================================================================================

equations = Residual(solver).equations
equations.continuity.absolute_criteria = 1e-4
equations.continuity.monitor = True
equations.x_velocity.absolute_criteria = 1e-4
equations.y_velocity.absolute_criteria = 1e-4
equations.z_velocity.absolute_criteria = 1e-4
equations.k.absolute_criteria = 1e-4
equations.omega.absolute_criteria = 1e-4


initialization = Initialization(solver)
initialization.reference_frame = "absolute"
initialization.initialization_type = "standard"
initialization.standard_initialize()


#############################################################################################################
# Define Report Definitions
# ===========================================================================================================

report_defs = ReportDefinitions(solver)
volume_avg_vmag_report_def = report_defs.volume.create(
    "volume-avg-vmag",
    report_type="volume-average",
    field="velocity-magnitude",
    cell_zones=fluid_cell_zones,
)

volume_avg_vmag_report_plot = ReportPlot.create(
    "volume-avg-vmag-rplot", report_defs="volume-avg-vmag"
)
volume_avg_vmag_report_file = ReportFile.create(
    "volume-avg-vmag-rfile", report_defs="volume-avg-vmag"
)

torque_report_def = report_defs.moment.create(
    "torque_imp_walls",
    report_output_type="Moment",
    zones=BoundaryCondition.get(solver, name="wall_impeller*"),
)

ReportPlot.create(
    solver, name="torque_imp_walls_rplot", report_defs=[torque_report_def]
)
ReportFile.create("torque_imp_walls_rfile", report_defs=[torque_report_def])


average_dissipation_rate_report_def = report_defs.volume.create(
    "average-dissipation-rate",
    report_type="volume-average",
    field=VariableCatalog.TURBULENT_DISSIPATION_RATE,
    cell_zones=fluid_cell_zones,
)


maximum_dissipation_rate_report_def = report_defs.volume.create(
    "maximum-dissipation-rate",
    report_type="volume-max",
    field="turb-diss-rate",
    cell_zones=fluid_cell_zones,
)

average_strain_rate_report_def = report_defs.volume.create(
    "average-strain-rate",
    report_type="volume-average",
    field=VariableCatalog.STRAIN_RATE,
    cell_zones=fluid_cell_zones,
)

maximum_strain_rate_report_def = report_defs.volume.create(
    "maximum-strain-rate",
    report_type="volume-max",
    field=VariableCatalog.STRAIN_RATE,
    cell_zones=fluid_cell_zones,
)

#############################################################################################################
# Run Solver
# ===========================================================================================================

run_calculation = RunCalculation(solver)
run_calculation.iter_count = 500

# Write the case file
write_case(solver, file_name="mixing_tank_final.cas.h5")
# Run the calculation
run_calculation.calculate()

#############################################################################################################
# Post-Processing Workflow
# ===========================================================================================================

# Set View
contour_view = graphics.views.display_states.create(
    "contour_view",
    front_faces_transparent="disable",
    view_name="top",
)

# Define the contour for velocity magnitude
velocity_contour = Contour.create(
    solver,
    name="velocity-contour",
    field="velocity-magnitude",
    surfaces_list=["mid_plane"],
    display_state_name=contour_view.name(),
)
velocity_contour.display()

graphics.views.auto_scale()
graphics.picture.save_picture(file_name="mixing_tank_velocity_contour.png")

# %%
# .. image:: ../../_static/mixing_tank_velocity_contour.png
#    :align: center
#    :scale: 60%
#    :alt: Mixing Tank Model Velocity Contour


#############################################################################################################
# Save the case file
# ===========================================================================================================
write_case_data(solver, file_name="mixing_tank_final.cas.h5")

#############################################################################################################
# Close the session
# ===========================================================================================================
meshing.exit()


# sphinx_gallery_thumbnail_path = '_static/mixing_tank_velocity_contour.png'
