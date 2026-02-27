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
# point. In this tutorial, Fluent ablation model is demonstrated for a reentry vehicle
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

from ansys.units import VariableCatalog

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.core.generated.solver.settings_builtin import (
    PlaneSurface,
    ReportFile,
    ReportPlot,
)
from ansys.fluent.core.generated.solver.settings_builtin_261 import read_case, write_case_data
from ansys.fluent.core.solver import (
    Controls,
    DynamicMesh,
    FluidMaterial,
    General,
    Initialization,
    Models,
    Monitor,
    PressureFarFieldBoundary,
    PressureOutlet,
    ReportDefinitions,
    Residual,
    Results,
    RunCalculation,
    Solution,
    WallBoundary,
)
from ansys.fluent.visualization import Contour, GraphicsWindow
from ansys.units.common import K, Pa, s

####################################################################################
# Download example file
# ==================================================================================
import_filename = examples.download_file(
    "ablation.msh.h5",
    "pyfluent/examples/Ablation-tutorial",
    save_path=Path.cwd(),
)

# upload mesh to the solver working directory
solver_upload_path = import_filename
# Note: solver.upload accepts a path-like or string
try:
    # solver may not be created yet; create it before upload below
    pass
except Exception:
    pass

####################################################################################
# Fluent Solution Setup
# ==================================================================================

####################################################################################
# Launch Fluent session with solver mode and print Fluent version
# ==================================================================================

solver = pyfluent.Solver.from_install(precision="double", processor_count=4)
print(solver.get_fluent_version())


####################################################################################
# Import mesh
# ==================================================================================

read_case(solver, file_name=import_filename)

####################################################################################
# Define models
# ==================================================================================

general = General(solver)
models = Models(solver)

general.solver.type = "density-based-implicit"
general.solver.time = "unsteady-1st-order"
general.operating_conditions.operating_pressure = 0.0 * Pa
models.energy.enabled = True
models.ablation.enabled = True

###################################################################
# Define material
# =================================================================

air = FluidMaterial.get(solver, name="air")
air.density.option = "ideal-gas"
air.molecular_weight = 28.966

############################
# Define boundary conditions
# ==========================

inlet = PressureFarFieldBoundary.get(solver, name="inlet")
inlet.momentum.gauge_pressure = 13500 * Pa
inlet.momentum.mach_number = 3
inlet.thermal.temperature = 4500 * K
inlet.turbulence.turbulent_intensity = 0.001

outlet = PressureOutlet.get(solver, name="outlet")
outlet.momentum.gauge_pressure = 13500 * Pa
outlet.momentum.prevent_reverse_flow = True

#############################################
# Ablation boundary condition (Vielles Model)
# ++++++++++++++++++++++++++++++++++++++++++++
# Once you have specified the ablation boundary conditions for the wall,
# Ansys Fluent automatically enables the Dynamic Mesh model with the Smoothing and
# Remeshing options, #creates the wall-ablation dynamic mesh zone, and configure
# appropriate dynamic mesh settings.

wall_ablation = WallBoundary.get(solver, name="wall_ablation")
wall_ablation.ablation.ablation_select_model = "Vielle's Model"
wall_ablation.ablation.ablation_vielle_a = 5
wall_ablation.ablation.ablation_vielle_n = 0.1

##############################
# Define dynamic mesh controls
# ============================

dynamic_mesh = DynamicMesh(solver)
dynamic_mesh.enabled = True

dz1 = dynamic_mesh.dynamic_zones.create(
    name="dynamic-zone-1", zone="interior--flow", type="deforming"
)
dz1.solver.stabilization.enabled = False
dz1.geometry.feature_detection.enabled = False
dz1.geometry.definition = "faceted"
dz1.meshing.smoothing.enabled = False
dz1.meshing.remeshing.parameters.global_settings = True
dz1.meshing.remeshing.enabled = True
dz1.motion.exclude_motion_bc = True

dz2 = dynamic_mesh.dynamic_zones.create(
    name="dynamic-zone-2", zone=outlet, type="deforming"
)
dz2.solver.stabilization.parameters.scale = 0.1
dz2.solver.stabilization.parameters.method = "coefficient-based"
dz2.solver.stabilization.enabled = True
dz2.geometry.feature_detection.enabled = False
dz2.geometry.definition = "faceted"
dz2.meshing.smoothing.enabled = True
dz2.meshing.remeshing.enabled = False
dz2.motion.exclude_motion_bc = True

dz3 = dynamic_mesh.dynamic_zones.create(
    name="dynamic-zone-3", zone="symm1", type="deforming"
)
dz3.solver.stabilization.parameters.scale = 0.1
dz3.solver.stabilization.parameters.method = "coefficient-based"
dz3.solver.stabilization.enabled = True
dz3.geometry.feature_detection.enabled = False
dz3.geometry.plane_def.normal = [0, -1, 0]
dz3.geometry.plane_def.point = [0.0, -0.04, 0.0]
dz3.geometry.definition = "plane"
dz3.meshing.smoothing.enabled = True
dz3.meshing.remeshing.enabled = False
dz3.motion.exclude_motion_bc = True

dz4 = dynamic_mesh.dynamic_zones.create(
    name="dynamic-zone-4", zone="symm2", type="deforming"
)
dz4.solver.stabilization.parameters.scale = 0.1
dz4.solver.stabilization.parameters.method = "coefficient-based"
dz4.solver.stabilization.enabled = True
dz4.geometry.feature_detection.enabled = False
dz4.geometry.plane_def.normal = [0, 1, 0]
dz4.geometry.plane_def.point = [0.0, 0.04, 0.0]
dz4.geometry.definition = "plane"
dz4.meshing.smoothing.enabled = True
dz4.meshing.remeshing.enabled = False
dz4.motion.exclude_motion_bc = True

dz5 = dynamic_mesh.dynamic_zones.create(name="dynamic-zone-5")
dz5.zone = wall_ablation.name
dz5.type = "user-defined"
dz5.solver.stabilization.enabled = False
dz5.geometry.feature_detection.enabled = False
dz5.meshing.udf_deform.max_skew = 0.7
dz5.meshing.udf_deform.enabled = True
dz5.meshing.adjacent_zones.t0.height = 0.0
dz5.meshing.adjacent_zones.t0.type = "constant"
dz5.motion.relative_motion.enabled = False
dz5.motion.exclude_motion_bc = False
dz5.motion.motion_def = "**ablation**"

############################################
# Define solver settings
# =======================

general.solver.time = "unsteady-2nd-order"
controls = Controls(solver)
controls.limits.max_temperature = 25_000 * K
Residual(solver).equations["energy"].absolute_criteria = 1e-06

############################################
# Create report definitions
# ==========================

solution = Solution(solver)
monitor = Monitor(solver)
report_definitions = ReportDefinitions(solver)

drag_def = report_definitions.drag.create(name="drag_force_x", zones=[wall_ablation])
ReportPlot.create(solver, name="drag_force_x", report_defs=[drag_def])
ReportFile.create(
    solver, name="drag_force_x", file_name="drag_force_x.out", report_defs=[drag_def]
)

pressure_avg = report_definitions.surface.create(
    name="pressure_avg_abl_wall",
    report_type="surface-areaavg",
    field=VariableCatalog.PRESSURE,
    surface_names=[wall_ablation],
)
ReportPlot.create(solver, name="pressure_avg_abl_wall", report_defs=[pressure_avg])
pressure_avg_file = ReportFile.create(
    solver,
    name="pressure_avg_abl_wall",
    report_defs=[pressure_avg],
    file_name="pressure_avg_abl_wall.out",
)

recede = report_definitions.surface.create(name="recede_point")
recede.report_type = "surface-vertexmax"
recede.field = "z-coordinate"
recede.surface_names = [wall_ablation.name]
recede_plot = ReportPlot(solver, new_instance_name="recede_point")
recede_plot.report_defs = recede.name
recede_file = ReportFile(solver, new_instance_name="recede_point")
recede_file.file_name = "recede_point.out"
recede_file.report_defs = [recede.name]

############################################
# Initialize and Save case
# ========================

init = Initialization(solver)
init.compute_defaults(
    from_zone_type="pressure-far-field", from_zone_name=inlet.name(), phase="mixture"
)
init.initialization_type = "standard"
init.standard_initialize()
run_calc = RunCalculation(solver)
run_calc.transient_controls.time_step_size = 1e-06 * s

write_case(solver, file_name="ablation.cas.h5")

############################################
# Run the calculation
# ===================
# Note: It may take about half an hour to finish the calculation.

run_calc.dual_time_iterate(time_step_count=100, max_iter_per_step=20)

###############################################
# Save simulation data
# ====================
# Write case and data files
write_case_data(solver, file_name="ablation_Solved.cas.h5")

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

mid_plane = PlaneSurface.create(name="mid_plane", method="zx-plane")
# Create mid plane surface for contouring

###############################################
# Post processing with PyVista (3D visualization)
# ===============================================
# Following graphics is displayed in the a new window/notebook


contour1 = Contour(solver=solver, field="pressure", surfaces=["mid_plane"])

window = GraphicsWindow()
window.add_graphics(contour1)
window.show()
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
window = GraphicsWindow()
window.add_graphics(contour1)
window.show()

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
