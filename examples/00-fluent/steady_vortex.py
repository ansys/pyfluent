# /// script
# dependencies = [
#   "imageio",
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

""".. _steady_vortex:

Simulation of Steady Vortex in a Stirred Tank
==============================================
"""

# %%
#
# Introduction
# ------------
# This tutorial demonstrates simulating vortex dynamics within continuous stirred tank
# reactors (CSTRs), which are extensively utilized in industries such as chemical,
# petrochemical, and pharmaceuticals for applications like fluid blending, crystallization,
# and pharmaceutical manufacturing. This tutorial includes step-by-step instructions on
# setting up the simulation using the MRF method, and employing best
# practices to accelerate free-surface flow simulations. Understanding vortex formation is
# crucial, as it often leads to undesirable effects like air entrainment and improper solid
# mixing. Identifying operating conditions that lead to vortex formation can help minimize
# these issues and ensure optimal liquid blending.
#
# .. figure:: /_static/steady_vortex/steady_vortex_setup.png
#     :width: 500pt
#     :align: center
#
# Problem Description
# -------------------
# In this tutorial, we aim to model vortex formation in a stirred tank using a steady-state
# simulation. The setup involves an unbaffled cylindrical tank equipped with a Rushton
# turbine impeller, featuring the following specifications:
#
# Tank Diameter : 0.29 meters
# Impeller Diameter: 0.1 meters
# Liquid Level: 0.19 meters
# Agitation Speed: 240 [rev min^-1]
#
# The aim is to examine the vortex dynamics within the tank under given conditions.
#
# .. figure:: /_static/steady_vortex/steady_vortex_dimensions.png
#     :width: 500pt
#     :align: center
#
# Simulation Setup & Solution
# ---------------------------
# Import required modules and classes
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Import some direct settings classes which will be used in the following sections.
# These classes allow straightforward access to various settings without the need to
# navigate through the settings hierarchy.

# sphinx_gallery_capture_repr = ('_repr_html_', '__repr__')
# sphinx_gallery_thumbnail_path = '_static/steady_vortex/steady_vortex_setup.png'

from pathlib import Path

import imageio.v2 as imageio

import ansys.fluent.core as pyfluent
from ansys.fluent.core import Dimension, Precision
from ansys.fluent.core.examples import download_file
from ansys.fluent.core.solver import (  # noqa: E402
    LIC,
    CellRegister,
    CellZoneCondition,
    Contour,
    General,
    Graphics,
    FluidMaterial,
    Initialization,
    IsoClip,
    IsoSurface,
    Materials,
    Mesh,
    Methods,
    Models,
    Multiphase,
    NamedExpression,
    PlaneSurface,
    Scene,
    Viscous,
    WallBoundary,
    read_case,
    CalculationActivity,
    iterate,
    write_case_data,
)
from ansys.units.common import m, s

# %%
# Launch Fluent
# ^^^^^^^^^^^^^
#
# Launch Fluent in 3D double precision solver mode.

solver = pyfluent.Solver.from_install(
    dimension=Dimension.THREE,
    precision=Precision.DOUBLE,
    cleanup_on_exit=True,
    cwd=Path.cwd(),
)
print(solver.get_fluent_version())  # Print the Fluent version
pyfluent.set_console_logging_level("INFO")  # Set the console logging level

# %%
# Mesh
# ^^^^
#
# Download the mesh file and read it into the Fluent session.

vortex_mesh = download_file(
    "vortex-mixingtank.msh.h5",
    "pyfluent/examples/Steady-Vortex-VOF",
    save_path=Path.cwd(),
)

# %%
# Define Constants
# ^^^^^^^^^^^^^^^^
#
# Define constants.

g = 9.81 * m / s**2

# %%
#
# Read Mesh
# ^^^^^^^^^^^
#
# Import the mesh file into the Fluent session.

read_case(solver, file_name=vortex_mesh)

# %%
# Display the mesh in Fluent and save the image to a file to examine locally.

# Create a middle plane to display the mesh
y_mid_plane = PlaneSurface.create(solver, name="y_mid_plane", method="zx-plane", y=0)
y_mid_plane.display()

# Define and display the mesh
mesh = Mesh.create(solver, name="mesh", surfaces_list=y_mid_plane.name())
mesh.options.edges = True
mesh.display()

# Create Graphics object to save the mesh image
graphics = Graphics(solver)
graphics.views.auto_scale()
if graphics.picture.use_window_resolution.is_active():
    graphics.picture.use_window_resolution = False

graphics.views.restore_view(view_name="top")
graphics.views.auto_scale()
graphics.picture.x_resolution = 600
graphics.picture.y_resolution = 600
graphics.picture.color_mode = "mono"
graphics.picture.save_picture(file_name="mesh.png")

# %%
# .. figure:: /_static/steady_vortex/mesh.png
#     :width: 500pt
#     :align: center
#
#     Polyhexcore Mesh for the Steady Vortex Simulation

# %%
# Define General Settings
# ^^^^^^^^^^^^^^^^^^^^^^^^
#
# Set gravity

general = General(solver)
general.operating_conditions.gravity.enable = True
general.operating_conditions.gravity.components = [0.0, 0.0, -g]

# %%
# Copy Materials from Fluent Database
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# Copy liquid water material from the Fluent database and get a reference to air material (it's predefined in Fluent).

water = Materials(solver).database.copy_by_name(type="fluid", name="water-liquid")
air = FluidMaterial.get(solver, name="air")

# %%
# Define Named Expression for Agitation Speed
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# Create a named expression for the agitation speed and specify as an input parameter.
stirring_speed = NamedExpression.create(
    solver, name="stirring_speed", definition="240 [rev min^-1]", input_parameter=True
)

# %%
# MRF zone parameters
# ^^^^^^^^^^^^^^^^^^^
#
# Define MRF zone parameters for the mrf cell zone.

reference_frame = CellZoneCondition(solver, name="mrf").reference_frame
reference_frame.frame_motion = True
reference_frame.reference_frame_axis_origin = (0, 0, 0)
reference_frame.reference_frame_axis_direction = (0, 0, 1)
reference_frame.mrf_omega.value = "stirring_speed"

# %%
# Rotating Wall BC parameters
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# Define the rotating wall boundary condition for the shaft.

wall_boundary = WallBoundary(solver, name="shaft_tank")
wall_boundary.momentum.wall_motion = "Moving Wall"
wall_boundary.momentum.relative = False
wall_boundary.momentum.rotating = True
wall_boundary.momentum.rotation_axis_direction = (0, 0, 1)
wall_boundary.momentum.rotation_speed = "stirring_speed"

# %%
# Physical Models: VOF
# ^^^^^^^^^^^^^^^^^^^^^^^
#
# Enable the VOF multiphase model and update the curvature correction setting for the viscous model.
model_setup = Models(solver)
multiphase = Multiphase(solver)
multiphase.model = "vof"
multiphase.vof_parameters.vof_formulation = "implicit"
multiphase.vof_parameters.vof_cutoff = 1e-06
multiphase.advanced_formulation.implicit_body_force = True
model_setup.multiphase = multiphase

viscous = Viscous(solver)
viscous.options.curvature_correction = True
model_setup.viscous = viscous

solution_methods = Methods(solver)
solution_methods.multiphase_numerics.solution_stabilization.execute_settings_optimization = True
solution_methods.multiphase_numerics.solution_stabilization.execute_advanced_stabilization = True

# Change phase names
# TODO check
primary_phase = multiphase.phases["phase-1"]
primary_phase.name = "water"
primary_phase.material = water
secondary_phase = multiphase.phases["phase-2"]
secondary_phase.name = "air"
secondary_phase.material = air
general.solver.time = "steady"  # steady solver

# %%
# Define Initial Conditions
# ^^^^^^^^^^^^^^^^^^^^^^^^^
#
# Define initial conditions for the simulation and set up cell registers to define the initial
# liquid region in the tank and initialize the solution and set multipase numerics settings.
#
# .. note::
#
#   Create a region of cells to patch the water volume fraction. Mark the cells from the bottom of
#   the tank up to the specified height. Create a cell register named "liquid_patch". Set Z-min to
#   the tank's minimum height coordinate and Z-max to 0.19 m. Utilize the minimum and maximum X & Y
#   values to ensure cells across the entire tank diameter are included.

initialization = Initialization(solver)
initialization.reference_frame = "absolute"
initialization.defaults["k"] = 0.001
initialization.localized_turb_init.enabled = False

cell_register = CellRegister(solver, new_instance_name="liquid_patch")
cell_register.type.option = "hexahedron"
cell_register.type.hexahedron.inside = True
cell_register.type.hexahedron.max_point = (100.0, 100.0, 0.19)
cell_register.type.hexahedron.min_point = (-100.0, -100.0, -100.0)

initialization.initialize()

# Patch the water volume fraction in the defined cell register to set the initial
# liquid region in the tank.
# "mp" refers to the volume fraction of the primary phase (here water).
# Setting value=1 fills the patch region entirely with water.
initialization.patch.calculate_patch(
    domain="water",
    cell_zones=[],
    registers=["liquid_patch"],
    variable="mp",
    reference_frame="Relative to Cell Zone",
    use_custom_field_function=False,
    value=1,
)

# %%
# Postprocessing Setup
# ^^^^^^^^^^^^^^^^^^^^
#
# Define surfaces, meshes and scenes for postprocessing and visualization.
# e.g., to visualize the free surface and wetted walls and dry walls.

# Free surface iso-surface
free_surface = IsoSurface.create(
    solver, name="freesurface", field="water-vof", iso_values=[0.5] * m
)

# Wetted wall and dry wall iso-clips
wet_wall = IsoClip.create(
    solver, name="wet_wall", field="water-vof", surfaces=["wall_tank"]
)
wet_wall.range.minimum = 0.5
wet_wall.range.maximum = 1.0


dry_wall = IsoClip.create(
    solver, name="dry_wall", field="water-vof", surfaces=["wall_tank"]
)
dry_wall.range.minimum = 0.0
dry_wall.range.maximum = 0.499

# Meshes
internal_comp_mesh = Mesh.create(
    solver,
    name="internals",
    surfaces_list=[
        "wall_impeller",
        "shaft_mrf",
        "shaft_tank",
    ],
)
internal_comp_mesh.surfaces_list()

# dry wall
dry_wall_comp_mesh = Mesh.create(solver, name="drywall", surfaces_list=[dry_wall])
dry_wall_comp_mesh.surfaces_list()

# wet wall
wet_wall_comp_mesh = Mesh.create(solver, name="wetwall", surfaces_list=[wet_wall])
wet_wall_comp_mesh.surfaces_list()
wet_wall_comp_mesh.coloring.option = "manual"
wet_wall_comp_mesh.coloring.manual.faces = "pastel cyan"

# liquid level
liquidlevel_comp_mesh = Mesh.create(
    solver, name="liquidlevel", surfaces_list=[freesurface]
)
liquidlevel_comp_mesh.surfaces_list()
liquidlevel_comp_mesh.coloring.option = "manual"
liquidlevel_comp_mesh.coloring.manual.faces = "pastel cyan"


# Scenes
vortex_scene = Scene.create(solver, name="scene-1")
liquid_gobj = vortex_scene.graphics_objects.add(name=liquidlevel_comp_mesh.name())
liquid_gobj.transparency = 50
liquid_gobj.color_map.position = 0
liquid_gobj.color_map.left = 0.0
liquid_gobj.color_map.bottom = 0.0
liquid_gobj.color_map.width = 0.0
liquid_gobj.color_map.height = 0.0

internal_gobj = vortex_scene.graphics_objects.add(name=internal_comp_mesh.name())
internal_gobj.transparency = 35
internal_gobj.color_map.position = 0
internal_gobj.color_map.left = 0.0
internal_gobj.color_map.bottom = 0.0
internal_gobj.color_map.width = 0.0
internal_gobj.color_map.height = 0.0

dry_gobj = vortex_scene.graphics_objects.add(name=dry_wall_comp_mesh.name())
dry_gobj.transparency = 75
dry_gobj.color_map.position = 0
dry_gobj.color_map.left = 0.0
dry_gobj.color_map.bottom = 0.0
dry_gobj.color_map.width = 0.0
dry_gobj.color_map.height = 0.0

wet_gobj = vortex_scene.graphics_objects.add(name=wet_wall_comp_mesh.name())
wet_gobj.transparency = 75
wet_gobj.color_map.position = 0
wet_gobj.color_map.left = 0.0
wet_gobj.color_map.bottom = 0.0
wet_gobj.color_map.width = 0.0
wet_gobj.color_map.height = 0.0

# Contour plot on Y-Mid plane
y_mid_iso_surface = IsoSurface.create(
    solver, name="ymid", field="y-coordinate", iso_values=[0] * m
)

volume_fraction_contour = Contour.create(
    solver,
    name="contour-1",
    surfaces_list=y_mid_iso_surface.name(),
    field="water-vof",
)
volume_fraction_contour.surfaces_list()
volume_fraction_contour.display()

graphics.views.restore_view(view_name="top")
graphics.views.auto_scale()
graphics.picture.color_mode = "color"
graphics.picture.use_window_resolution = False
graphics.picture.x_resolution = 600
graphics.picture.y_resolution = 600
graphics.picture.save_picture(file_name="contour.png")

# %%
# .. figure:: /_static/steady_vortex/contour.png
#     :width: 500pt
#     :align: center
#
#     Velocity Vectors
#
# *The velocity vectors illustrate the flow patterns within the tank, highlighting the
#  complex interactions between the liquid and gas phases.*


# Animation Setup
CalculationActivity(solver).solution_animations.create(
    name="animation-2",
    animate_on="scene-1",
    frequency=10,
    storage_type="png",
    view="top",
)

# %%
# Save Initial Files & Run Calculation
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# Save the initial case file and run the calculation for 500 iterations.
write_case_data(solver, file_name="vortex_init.cas.h5")

iterate(solver, iter_count=50)  # Iteration count keep it 50 for demo only purpose

# %%
# LIC Visualization
# ^^^^^^^^^^^^^^^^^
#
# Set up the LIC (Line Integral Convolution) visualization for the midplane.

lic_visualization = LIC.create(
    solver,
    name="lic-1",
    surfaces_list=y_mid_plane.name(),
    field="velocity-magnitude",
    lic_image_filter="Strong Sharpen",
    lic_intensity_factor=10,
    texture_size=10,
)
lic_visualization.display()

graphics.views.restore_view(view_name="top")
graphics.views.auto_scale()
graphics.picture.use_window_resolution = False
graphics.picture.x_resolution = 600
graphics.picture.y_resolution = 600
graphics.picture.save_picture(file_name="lic-1.png")

# %%
# .. figure:: /_static/steady_vortex/lic-1.png
#     :width: 500pt
#     :align: center
#
#     LIC Visualization
#
# *The LIC visualization provides a detailed view of the flow patterns within the tank.*

# %%
# Save Visualization of Final Vortex Shape & Write Simulation Files
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# Save the final vortex shape visualization and write the final case and data files.

vortex_scene.display()
graphics.views.restore_view(view_name="top")
graphics.views.auto_scale()

graphics.picture.use_window_resolution = False
graphics.picture.x_resolution = 600
graphics.picture.y_resolution = 600
graphics.picture.save_picture(file_name="vortex.png")

# %%
# .. figure:: /_static/steady_vortex/vortex.png
#     :width: 500pt
#     :align: center
#
#     Vortex Shape Visualization
#
# *Steady vortex shape in the stirred tank.*

# Save final case and data files
write_case_data(solver, file_name="vortex_final.cas.h5")

# %%
# Close Fluent
# ^^^^^^^^^^^^
#
# Exit the Fluent session.
solver.exit()

# %%
# Generate GIF Animation: Vortex Formation
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# Create a GIF animation from the saved PNG images of the vortex formation using third-party library `imageio`.
#
# .. note::
#
#   Install imageio package if not already installed. You can install it via pip:
#   `pip install imageio`

images = list(map(imageio.imread, sorted(Path.cwd().glob("animation*.png"))))

imageio.mimsave(uri="vortex.gif", ims=images, duration=0.2)

# %%
# .. figure:: /_static/steady_vortex/vortex.gif
#     :width: 500pt
#     :align: center
#
#     Vortex Formation
#
# *The GIF animation illustrates the dynamic process of vortex formation within the stirred tank.*
