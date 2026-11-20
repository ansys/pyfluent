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

""".. _mixing_tank_workflow:

Mixing Tank Workflow
-------------------------------------------
"""
#############################################################################################################
# Overeview
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
import os
import platform

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples

#############################################################################################################
# Launch Fluent session with meshing mode and print Fluent version
# ===========================================================================================================
session = pyfluent.launch_fluent(
    mode="meshing",
    cleanup_on_exit=True,
)
print(session.get_fluent_version())

#############################################################################################################
# Meshing Workflow
# ===========================================================================================================
workflow = session.workflow

filenames = {
    "Windows": "mixing_tank_geom.dsco",
    "Other": "StirredTank.scdoc.pmdb",
}

geometry_filename = examples.download_file(
    filenames.get(platform.system(), filenames["Other"]),
    "pyfluent/examples/MixingTank-WorkFlow",
    save_path=os.getcwd(),
)

workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
workflow.TaskObject["Import Geometry"].Arguments = dict(FileName=geometry_filename)
workflow.TaskObject["Import Geometry"].Execute()

workflow.TaskObject["Generate the Surface Mesh"].Execute()
workflow.TaskObject["Describe Geometry"].Arguments = dict(
    SetupType="The geometry consists of only fluid regions with no voids",
    wall_to_internal="Yes",
    InvokeShareTopology="Yes",
)
workflow.TaskObject["Describe Geometry"].Execute()
workflow.TaskObject["Apply Share Topology"].Execute()
workflow.TaskObject["Update Boundaries"].Execute()
workflow.TaskObject["Update Regions"].Execute()
workflow.TaskObject["Add Boundary Layers"].InsertCompoundChildTask()
workflow.TaskObject["smooth-transition_1"].Execute()
workflow.TaskObject["Generate the Volume Mesh"].Execute()

# Write a mesh file for reference
session.tui.file.write_mesh("mixing_tank.msh.h5")

#############################################################################################################
# Switch to the Solver Mode
# ===========================================================================================================
solver_session = session.switch_to_solver()


###############################################################################################################
# Display the mesh in solver mode
# ===========================================================================================================

# Create a middle plane to display the mesh
y_mid_plane = solver_session.settings.results.surfaces.plane_surface.create(
    name="mid_plane"
)
y_mid_plane.method = "zx-plane"
y_mid_plane.y = 0
y_mid_plane.display()


# Access the graphics object
graphics = solver_session.settings.results.graphics
# Set the hardcopy format for saving the image
graphics.picture.driver_options.hardcopy_format = "png"

# View settings
geom_view = graphics.views.display_states.create("geom_view")
geom_view.front_faces_transparent = "enable"
geom_view.view_name = "top"

# Get the list of all walls
all_walls = solver_session.settings.setup.boundary_conditions.wall.get_object_names()
filtered_walls_to_display = [wall for wall in all_walls if "mrf" not in wall]

# Create a mesh object and configure its settings
mesh_object = solver_session.settings.results.graphics.mesh.create(name="mesh-1")
mesh_object.surfaces_list = filtered_walls_to_display
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
g = 9.81  # m/s^2
water_density = 1000.0  # kg/m^3
water_viscosity = 0.001  # kg/m-s
agitation_speed = 10  # rad/s

#############################################################################################################
# Solver Setup and Solve Workflow
# ===========================================================================================================
solver_session.settings.setup.general.operating_conditions.gravity.enable = True
solver_session.settings.setup.general.operating_conditions.gravity.components = [
    0.0,
    0.0,
    -g,
]

#############################################################################################################
# Define Materials
# ===========================================================================================================
solver_session.settings.setup.materials.database.copy_by_name(
    type="fluid", name="water-liquid"
)
fluid_mat = solver_session.settings.setup.materials.fluid["water-liquid"]
fluid_mat.density.value = water_density
fluid_mat.viscosity.value = water_viscosity

#############################################################################################################
# Define Cell Zones, Wall Boundary Conditions
# ===========================================================================================================

# Get the list of all Fluid Cell Zones,
fluid_cell_zones = (
    solver_session.settings.setup.cell_zone_conditions.fluid.get_object_names()
)
fluid_mrf_cell_zones = [zone for zone in fluid_cell_zones if "mrf" in zone]

for cell_zone in fluid_mrf_cell_zones:
    print(cell_zone)
    # Set the material for each cell zone
    fluid_cell_zone = solver_session.settings.setup.cell_zone_conditions.fluid[
        cell_zone
    ]
    fluid_cell_zone.general.material = "water-liquid"
    # Set the reference frame for each cell zone
    fluid_cell_zone.reference_frame.reference_frame_axis_origin = [0, 0, 0.4]
    fluid_cell_zone.reference_frame.reference_frame_axis_direction = [0, 0, -1]
    fluid_cell_zone.reference_frame.frame_motion = True
    # Set the rotation speed for each cell zone
    fluid_cell_zone.reference_frame.mrf_omega.value = agitation_speed

stationary_cell_zones = [zone for zone in fluid_cell_zones if "mrf" not in zone]
stationary_cell_zones = solver_session.settings.setup.cell_zone_conditions.fluid[
    stationary_cell_zones[0]
]
stationary_cell_zones.general.material = "water-liquid"

# Wall boundary conditions
wall_shaft = [wall for wall in all_walls if "shaft" in wall]

for wall in wall_shaft:
    print(wall)
    wall_boundary = solver_session.settings.setup.boundary_conditions.wall[wall]
    wall_boundary.momentum.wall_motion = "Moving Wall"
    wall_boundary.momentum.relative = False
    wall_boundary.momentum.rotating = True
    wall_boundary.momentum.rotation_axis_direction = [0, 0, -1]
    wall_boundary.momentum.rotation_speed = agitation_speed


liquid_level_bc = solver_session.settings.setup.boundary_conditions.wall[
    "wall_liquid_level"
]
liquid_level_bc.momentum.wall_motion = "Stationary Wall"
liquid_level_bc.momentum.shear_condition = "Specified Shear"

# Change the Zone type for internal walls to interior
solver_session.setup.boundary_conditions.set_zone_type(
    zone_list=["fluid_mrf_1-fluid_tank"], new_type="interior"
)

#############################################################################################################
# Solution Methods and Controls
# ===========================================================================================================
solver_session.settings.solution.methods.p_v_coupling.flow_scheme = "SIMPLE"
solver_session.settings.solution.methods.spatial_discretization.discretization_scheme[
    "pressure"
] = "presto!"
solver_session.settings.solution.controls.under_relaxation["pressure"] = 0.5
solver_session.settings.solution.controls.under_relaxation["mom"] = 0.3
solver_session.settings.solution.controls.under_relaxation["k"] = 0.6
solver_session.settings.solution.controls.under_relaxation["omega"] = 0.6
solver_session.settings.solution.controls.under_relaxation["turb-viscosity"] = 0.6

##############################################################################################################
#  Residuals Criteria & Initialization
# ===========================================================================================================

# Residuals criteria
residuals_options = solver_session.settings.solution.monitor.residual
residuals_options.equations["continuity"].absolute_criteria = 0.0001
residuals_options.equations["continuity"].monitor = True  # Enable continuity residuals
residuals_options.equations["x-velocity"].absolute_criteria = 0.0001
residuals_options.equations["y-velocity"].absolute_criteria = 0.0001
residuals_options.equations["z-velocity"].absolute_criteria = 0.0001
residuals_options.equations["k"].absolute_criteria = 0.0001
residuals_options.equations["omega"].absolute_criteria = 0.0001


# Initialize the solution
initialization = solver_session.settings.solution.initialization
initialization.reference_frame = "absolute"
initialization.initialization_type = "standard"
initialization.standard_initialize()


#############################################################################################################
# Define Report Definitions
# ===========================================================================================================

# Create a report definition for the volume average velocity magnitude
volume_avg_vmag_report_def = (
    solver_session.settings.solution.report_definitions.volume.create("volume-avg-vmag")
)
volume_avg_vmag_report_def.report_type.allowed_values()  # output the allowed values for report type
volume_avg_vmag_report_def.report_type = "volume-average"
volume_avg_vmag_report_def.field = "velocity-magnitude"
volume_avg_vmag_report_def.cell_zones = fluid_cell_zones

# Report plot
volume_avg_vmag_report_plot = (
    solver_session.settings.solution.monitor.report_plots.create(
        "volume-avg-vmag-rplot"
    )
)
volume_avg_vmag_report_plot.report_defs = "volume-avg-vmag"
# Report file
volume_avg_vmag_report_file = (
    solver_session.settings.solution.monitor.report_files.create(
        "volume-avg-vmag-rfile"
    )
)
volume_avg_vmag_report_file.report_defs = "volume-avg-vmag"


# Create a report definition for the torque on the impeller walls
torque_report_def = solver_session.settings.solution.report_definitions.moment.create(
    "torque_imp_walls"
)
torque_report_def.report_output_type.allowed_values()  # output the allowed values for report output type
torque_report_def.report_output_type = "Moment"
filtered_walls = fnmatch.filter(all_walls, "wall_impeller*")
torque_report_def.zones = filtered_walls

# Report plot
torque_report_plot = solver_session.settings.solution.monitor.report_plots.create(
    "torque_imp_walls_rplot"
)
torque_report_plot.report_defs = "torque_imp_walls"
# Report file
torque_report_file = solver_session.settings.solution.monitor.report_files.create(
    "torque_imp_walls_rfile"
)
torque_report_file.report_defs = "torque_imp_walls"


# Average and maximum dissipation rate report definitions
average_dissipation_rate_report_def = (
    solver_session.settings.solution.report_definitions.volume.create(
        "average-dissipation-rate"
    )
)
average_dissipation_rate_report_def.report_type = "volume-average"
average_dissipation_rate_report_def.field = "turb-diss-rate"
average_dissipation_rate_report_def.cell_zones = fluid_cell_zones

maximum_dissipation_rate_report_def = (
    solver_session.settings.solution.report_definitions.volume.create(
        "maximum-dissipation-rate"
    )
)
maximum_dissipation_rate_report_def.report_type = "volume-max"
maximum_dissipation_rate_report_def.field = "turb-diss-rate"
maximum_dissipation_rate_report_def.cell_zones = fluid_cell_zones

# Average and maximum strain rate report definitions
average_strain_rate_report_def = (
    solver_session.settings.solution.report_definitions.volume.create(
        "average-strain-rate"
    )
)
average_strain_rate_report_def.report_type = "volume-average"
average_strain_rate_report_def.field = "strain-rate-mag"
average_strain_rate_report_def.cell_zones = fluid_cell_zones


maximum_strain_rate_report_def = (
    solver_session.settings.solution.report_definitions.volume.create(
        "maximum-strain-rate"
    )
)
maximum_strain_rate_report_def.report_type = "volume-max"
maximum_strain_rate_report_def.field = "strain-rate-mag"
maximum_strain_rate_report_def.cell_zones = fluid_cell_zones

#############################################################################################################
# Run Solver
# ===========================================================================================================

# Run the calculation
run_calculation = solver_session.settings.solution.run_calculation
run_calculation.iter_count = 500

# Write the case file
solver_session.settings.file.write(
    file_type="case", file_name="mixing_tank_final.cas.h5"
)
# Run the calculation
run_calculation.calculate()

#############################################################################################################
# Post-Processing Workflow
# ===========================================================================================================

# Set View
contour_view = graphics.views.display_states.create("contour_view")
contour_view.front_faces_transparent = "disable"
contour_view.view_name = "top"

# Define the contour for velocity magnitude
velocity_contour = solver_session.settings.results.graphics.contour.create(
    name="velocity-contour"
)
velocity_contour.field = "velocity-magnitude"
velocity_contour.surfaces_list = ["mid_plane"]
velocity_contour.display_state_name = contour_view.name()
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
solver_session.settings.file.write(
    file_type="case-data", file_name="mixing_tank_final.cas.h5"
)

#############################################################################################################
# Close the session
# ===========================================================================================================
session.exit()


# sphinx_gallery_thumbnail_path = '_static/mixing_tank_velocity_contour.png'
