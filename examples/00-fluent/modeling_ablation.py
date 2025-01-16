""".. _modeling_ablation:

Modeling Ablation
-------------------------------------------
"""

#######################################################################################
# Objective
# =====================================================================================
#
# Ablation is an effective treatment used to protect an atmospheric reentry vehicle from
# the damaging effects of external high temperatures caused by shock wave and viscous
# heating. The ablative material is chipped away due to surface reactions that remove a
# significant amount of heat and keep the vehicle surface temperature below the melting
# point. In this tutorial, Fluent ablation model is demonstrated for a reendtry vehicle
# geometry simplified as a 3D wedge.
#
# This tutorial demonstrates how to do the following:
#
# * Define boundary conditions for a high-speed flow.
# * Set up the ablation model to model effects of a moving boundary due to ablation.
# * Initiate and solve the transient simulation using the density-based solver.
#
# Problem Description:
# ====================
#
# The geometry of the 3D wedge considered in this tutorial is shown in following figure.
# The air flow passes around a nose of a re-entry vehicle operating under high speed
# conditions. The inlet air has a temperature of 4500 K, a gauge pressure of 13500 Pa,
# and a Mach number of 3. The domain is bounded above and below by symmetry planes
# (displayed in yellow). As the ablative coating chips away, the surface of the wall
# moves. The moving of the surface is modeled using dynamic meshes. The surface moving
# rate is estimated by Vieille's empirical law:
#
# where r is the surface moving rate, p is the absolute pressure, and A and n are model
# parameters. In the considered case, A = 5 and n = 0.1.


####################################################################################
# .. math::
#
#    r = A \cdot p^n


# %%
# .. image:: ../../_static/ablation-problem-schematic.png
#    :align: center
#    :alt: Problem Schematic

# %%

####################################################################################
# Import required libraries/modules
# ==================================================================================
from pathlib import Path

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.visualization.pyvista import Graphics

###############################################################################
# Specifying save path
# ++++++++++++++++++++++
# save_path can be specified as Path("E:/", "pyfluent-examples-tests") or
# Path("E:/pyfluent-examples-tests") in a Windows machine for example,  or
# Path("~/pyfluent-examples-tests") in Linux.
save_path = Path(pyfluent.EXAMPLES_PATH)

####################################################################################
# Download example file
# ==================================================================================
import_filename = examples.download_file(
    "ablation.msh.h5", "pyfluent/examples/Ablation-tutorial", save_path=save_path
)

####################################################################################
# Fluent Solution Setup
# ==================================================================================

from ansys.fluent.visualization import set_config  # noqa: E402

set_config(blocking=True, set_view_on_display="isometric")

####################################################################################
# Launch Fluent session with solver mode and print Fluent version
# ==================================================================================

solver = pyfluent.launch_fluent(
    product_version="25.1.0",
    dimension=3,
    precision="double",
    processor_count=4,
)
print(solver.get_fluent_version())

####################################################################################
# Import mesh
# ==================================================================================

solver.file.read_case(file_name=import_filename)

####################################################################################
# Define models
# ==================================================================================

solver.setup.general.solver.type = "density-based-implicit"
solver.setup.general.solver.time = "unsteady-1st-order"
solver.setup.general.operating_conditions.operating_pressure = 0.0
solver.setup.models.energy = {"enabled": True}
solver.setup.models.ablation = {"enabled": True}

###################################################################
# Define material
# =================================================================

solver.setup.materials.fluid["air"] = {
    "density": {"option": "ideal-gas"},
    "molecular_weight": {"value": 28.966, "option": "constant"},
}
solver.setup.materials.fluid["air"] = {"density": {"option": "ideal-gas"}}

############################
# Define boundary conditions
# ==========================

solver.setup.boundary_conditions.set_zone_type(
    zone_list=["inlet"], new_type="pressure-far-field"
)
solver.setup.boundary_conditions.pressure_far_field["inlet"].momentum.gauge_pressure = (
    13500
)
solver.setup.boundary_conditions.pressure_far_field["inlet"].momentum.mach_number = 3
solver.setup.boundary_conditions.pressure_far_field["inlet"].thermal.temperature = 4500
solver.setup.boundary_conditions.pressure_far_field[
    "inlet"
].turbulence.turbulent_intensity = 0.001

solver.setup.boundary_conditions.pressure_outlet["outlet"].momentum.gauge_pressure = (
    13500
)
solver.setup.boundary_conditions.pressure_outlet[
    "outlet"
].momentum.prevent_reverse_flow = True

#############################################
# Ablation boundary condition (Vielles Model)
# ++++++++++++++++++++++++++++++++++++++++++++
# Once you have specified the ablation boundary conditions for the wall,
# Ansys Fluent automatically enables the Dynamic Mesh model with the Smoothing and
# Remeshing options, #creates the wall-ablation dynamic mesh zone, and configure
# appropriate dynamic mesh settings.

solver.setup.boundary_conditions.wall[
    "wall_ablation"
].ablation.ablation_select_model = "Vielle's Model"
solver.setup.boundary_conditions.wall["wall_ablation"].ablation.ablation_vielle_a = 5
solver.setup.boundary_conditions.wall["wall_ablation"].ablation.ablation_vielle_n = 0.1

##############################
# Define dynamic mesh controls
# ============================

solver.tui.define.dynamic_mesh.dynamic_mesh("yes")
solver.tui.define.dynamic_mesh.zones.create(
    "interior--flow",
    "deforming",
    "faceted",
    "no",
    "no",
    "yes",
    "no",
    "yes",
    "yes",
    "no",
    "yes",
)
solver.tui.define.dynamic_mesh.zones.create(
    "outlet",
    "deforming",
    "faceted",
    "no",
    "yes",
    "no",
    "yes",
    "yes",
    "coefficient-based",
    "0.1",
    "yes",
)
solver.tui.define.dynamic_mesh.zones.create(
    "symm1",
    "deforming",
    "plane",
    "0",
    "-0.04",
    "0",
    "0",
    "-1",
    "0",
    "no",
    "yes",
    "no",
    "yes",
    "yes",
    "coefficient-based",
    "0.1",
    "yes",
)
solver.tui.define.dynamic_mesh.zones.create(
    "symm2",
    "deforming",
    "plane",
    "0",
    "0.04",
    "0",
    "0",
    "1",
    "0",
    "no",
    "yes",
    "no",
    "yes",
    "yes",
    "coefficient-based",
    "0.1",
    "yes",
)
solver.tui.define.dynamic_mesh.zones.create(
    "wall_ablation",
    "user-defined",
    "**ablation**",
    "no",
    "no",
    "189",
    "constant",
    "0",
    "yes",
    "yes",
    "0.7",
    "no",
    "no",
)

############################################
# Define solver settings
# =======================

solver.setup.general.solver.time = "unsteady-2nd-order"
solver.solution.controls.limits = {"max_temperature": 25000}
solver.solution.monitor.residual.equations["energy"].absolute_criteria = 1e-06

############################################
# Create report definitions
# ==========================

solver.solution.report_definitions.drag["drag_force_x"] = {}
solver.solution.report_definitions.drag["drag_force_x"].zones = ["wall_ablation"]

solver.solution.monitor.report_plots.create(name="drag_force_x")
solver.solution.monitor.report_plots["drag_force_x"].report_defs = "drag_force_x"
solver.tui.solve.report_plots.axes(
    "drag_force_x", "numbers", "float", "4", "exponential", "2", "q"
)

solver.solution.monitor.report_files.create(name="drag_force_x")
solver.solution.monitor.report_files["drag_force_x"] = {
    "report_defs": ["drag_force_x"],
    "file_name": r"drag_force_x.out",
}

solver.solution.report_definitions.surface["pressure_avg_abl_wall"] = {}
solver.solution.report_definitions.surface["pressure_avg_abl_wall"].report_type = (
    "surface-areaavg"
)
solver.solution.report_definitions.surface["pressure_avg_abl_wall"].field = "pressure"
solver.solution.report_definitions.surface["pressure_avg_abl_wall"].surface_names = [
    "wall_ablation"
]

solver.solution.monitor.report_plots.create(name="pressure_avg_abl_wall")
solver.solution.monitor.report_plots["pressure_avg_abl_wall"].report_defs = (
    "pressure_avg_abl_wall"
)
solver.tui.solve.report_plots.axes(
    "pressure_avg_abl_wall", "numbers", "float", "4", "exponential", "2", "q"
)

solver.solution.monitor.report_files.create(name="pressure_avg_abl_wall")
solver.solution.monitor.report_files["pressure_avg_abl_wall"] = {
    "report_defs": ["pressure_avg_abl_wall"],
    "file_name": r"pressure_avg_abl_wall.out",
}

solver.solution.report_definitions.surface["recede_point"] = {}
solver.solution.report_definitions.surface["recede_point"].report_type = (
    "surface-vertexmax"
)
solver.solution.report_definitions.surface["recede_point"].field = "z-coordinate"
solver.solution.report_definitions.surface["recede_point"].surface_names = [
    "wall_ablation"
]

solver.solution.monitor.report_plots.create(name="recede_point")
solver.solution.monitor.report_plots["recede_point"].report_defs = "recede_point"
solver.tui.solve.report_plots.axes(
    "recede_point", "numbers", "float", "4", "exponential", "2", "q"
)
solver.solution.monitor.report_files.create(name="recede_point")
solver.solution.monitor.report_files["recede_point"] = {
    "report_defs": ["recede_point"],
    "file_name": r"recede_point.out",
}

############################################
# Initialize and Save case
# ========================

solver.tui.solve.initialize.compute_defaults.pressure_far_field("inlet")
solver.solution.initialization.initialization_type = "standard"
solver.solution.initialization.standard_initialize()
solver.solution.run_calculation.transient_controls.time_step_size = 1e-06

save_case_data_as = Path(save_path) / "ablation.cas.h5"
solver.file.write(file_type="case", file_name=save_case_data_as)

############################################
# Run the calculation
# ===================
# Note: It may take about half an hour to finish the calculation.

solver.solution.run_calculation.dual_time_iterate(
    time_step_count=100, max_iter_per_step=20
)

###############################################
# Save simulation data
# ====================
# Write case and data files
save_case_data_as = Path(save_path) / "ablation_Solved.cas.h5"
solver.file.write(file_type="case-data", file_name=str(save_case_data_as))

####################################################################################
# Post Processing
# ==================================================================================

###############################################
# Display plots
# =============

# %%
# .. image:: ../../_static/ablation-residual.png
#    :align: center
#    :alt: residual

# %%
#    Scaled residual plot

# %%
# .. image:: ../../_static/ablation-drag_force_x.png
#    :align: center
#    :alt: Drag force in x direction

# %%
#    History of the drag force on the ablation wall

# %%
# .. image:: ../../_static/ablation-avg_pressure.png
#    :align: center
#    :alt: Average pressure on the ablation wall

# %%
#    History of the averaged pressure on the ablation wall

# %%
# .. image:: ../../_static/ablation-recede_point.png
#    :align: center
#    :alt: Recede point (albation)

# %%
#    Recede point (deformation due to ablation)

###############################################
# Display contour
# ================
# Following contours are displayed in the Fluent GUI:

solver.results.surfaces.plane_surface.create(name="mid_plane")
solver.results.surfaces.plane_surface["mid_plane"].method = "zx-plane"

solver.results.graphics.contour.create(name="contour_pressure")
solver.results.graphics.contour["contour_pressure"] = {
    "field": "pressure",
    "surfaces_list": ["mid_plane"],
}
solver.results.graphics.contour.display(object_name="contour_pressure")

solver.results.graphics.contour.create(name="contour_mach")
solver.results.graphics.contour["contour_mach"] = {
    "field": "mach-number",
    "surfaces_list": ["mid_plane"],
}
solver.results.graphics.contour.display(object_name="contour_mach")

###############################################
# Post processing with PyVista (3D visualization)
# ===============================================
# Following graphics is displayed in the a new window/notebook

graphics_session1 = Graphics(solver)
contour1 = graphics_session1.Contours["contour-1"]
contour1.field = "pressure"
contour1.surfaces_list = ["mid_plane"]
contour1.display()
# %%
# .. image:: ../../_static/ablation-pressure.png
#    :align: center
#    :alt: Static Pressure Contour

# %%
#    Static Pressure Contour

contour1.field = "mach-number"
contour1.range.option = "auto-range-off"
contour1.range.auto_range_off.minimum = 0.5
contour1.range.auto_range_off.maximum = 3.0
contour1.display()

# %%
# .. image:: ../../_static/ablation-mach-number.png
#    :align: center
#    :alt: Mach Number Contour

# %%
#    Mach Number Contour

####################################################################################
# Close the session
# ==================================================================================

solver.exit()

# sphinx_gallery_thumbnail_path = '_static/ablation-mach-number-thumbnail.png'
