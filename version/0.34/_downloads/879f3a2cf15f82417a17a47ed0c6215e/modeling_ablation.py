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
import os

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.visualization import Contour, GraphicsWindow

####################################################################################
# Download example file
# ==================================================================================
import_filename = examples.download_file(
    "ablation.msh.h5",
    "pyfluent/examples/Ablation-tutorial",
    save_path=os.getcwd(),
)

####################################################################################
# Fluent Solution Setup
# ==================================================================================

####################################################################################
# Launch Fluent session with solver mode and print Fluent version
# ==================================================================================

solver_session = pyfluent.launch_fluent(
    dimension=3,
    precision="double",
    processor_count=4,
)
print(solver_session.get_fluent_version())

####################################################################################
# Import mesh
# ==================================================================================

solver_session.file.read_case(file_name=import_filename)

####################################################################################
# Define models
# ==================================================================================

solver_session.setup.general.solver.type = "density-based-implicit"
solver_session.setup.general.solver.time = "unsteady-1st-order"
solver_session.setup.general.operating_conditions.operating_pressure = 0.0
solver_session.setup.models.energy = {"enabled": True}
solver_session.setup.models.ablation = {"enabled": True}

###################################################################
# Define material
# =================================================================

solver_session.setup.materials.fluid["air"] = {
    "density": {"option": "ideal-gas"},
    "molecular_weight": {"value": 28.966, "option": "constant"},
}
solver_session.setup.materials.fluid["air"] = {"density": {"option": "ideal-gas"}}

############################
# Define boundary conditions
# ==========================

solver_session.setup.boundary_conditions.set_zone_type(
    zone_list=["inlet"], new_type="pressure-far-field"
)
solver_session.setup.boundary_conditions.pressure_far_field[
    "inlet"
].momentum.gauge_pressure = 13500
solver_session.setup.boundary_conditions.pressure_far_field[
    "inlet"
].momentum.mach_number = 3
solver_session.setup.boundary_conditions.pressure_far_field[
    "inlet"
].thermal.temperature = 4500
solver_session.setup.boundary_conditions.pressure_far_field[
    "inlet"
].turbulence.turbulent_intensity = 0.001

solver_session.setup.boundary_conditions.pressure_outlet[
    "outlet"
].momentum.gauge_pressure = 13500
solver_session.setup.boundary_conditions.pressure_outlet[
    "outlet"
].momentum.prevent_reverse_flow = True

#############################################
# Ablation boundary condition (Vielles Model)
# ++++++++++++++++++++++++++++++++++++++++++++
# Once you have specified the ablation boundary conditions for the wall,
# Ansys Fluent automatically enables the Dynamic Mesh model with the Smoothing and
# Remeshing options, #creates the wall-ablation dynamic mesh zone, and configure
# appropriate dynamic mesh settings.

solver_session.setup.boundary_conditions.wall[
    "wall_ablation"
].ablation.ablation_select_model = "Vielle's Model"
solver_session.setup.boundary_conditions.wall[
    "wall_ablation"
].ablation.ablation_vielle_a = 5
solver_session.setup.boundary_conditions.wall[
    "wall_ablation"
].ablation.ablation_vielle_n = 0.1

##############################
# Define dynamic mesh controls
# ============================

solver_session.settings.setup.dynamic_mesh = {"enabled": True}

solver_session.settings.setup.dynamic_mesh.dynamic_zones = {
    "dynamic-zone-1": {
        "solver": {"stabilization": {"enabled": False}},
        "geometry": {"feature_detection": {"enabled": False}, "definition": "faceted"},
        "meshing": {
            "smoothing": {"enabled": False},
            "remeshing": {"parameters": {"global_settings": True}, "enabled": True},
        },
        "motion": {"exclude_motion_bc": True},
        "type": "deforming",
        "zone": "interior--flow",
        "name": "dynamic-zone-1",
    }
}

solver_session.settings.setup.dynamic_mesh.dynamic_zones = {
    "dynamic-zone-2": {
        "solver": {
            "stabilization": {
                "parameters": {"scale": 0.1, "method": "coefficient-based"},
                "enabled": True,
            }
        },
        "geometry": {"feature_detection": {"enabled": False}, "definition": "faceted"},
        "meshing": {"smoothing": {"enabled": True}, "remeshing": {"enabled": False}},
        "motion": {"exclude_motion_bc": True},
        "type": "deforming",
        "zone": "outlet",
        "name": "dynamic-zone-2",
    }
}

solver_session.settings.setup.dynamic_mesh.dynamic_zones = {
    "dynamic-zone-3": {
        "solver": {
            "stabilization": {
                "parameters": {"scale": 0.1, "method": "coefficient-based"},
                "enabled": True,
            }
        },
        "geometry": {
            "feature_detection": {"enabled": False},
            "plane_def": {"normal": [0, -1, 0], "point": [0.0, -0.04, 0.0]},
            "definition": "plane",
        },
        "meshing": {"smoothing": {"enabled": True}, "remeshing": {"enabled": False}},
        "motion": {"exclude_motion_bc": True},
        "type": "deforming",
        "zone": "symm1",
        "name": "dynamic-zone-3",
    }
}

solver_session.settings.setup.dynamic_mesh.dynamic_zones = {
    "dynamic-zone-4": {
        "solver": {
            "stabilization": {
                "parameters": {"scale": 0.1, "method": "coefficient-based"},
                "enabled": True,
            }
        },
        "geometry": {
            "feature_detection": {"enabled": False},
            "plane_def": {"normal": [0, 1, 0], "point": [0.0, 0.04, 0.0]},
            "definition": "plane",
        },
        "meshing": {"smoothing": {"enabled": True}, "remeshing": {"enabled": False}},
        "motion": {"exclude_motion_bc": True},
        "type": "deforming",
        "zone": "symm2",
        "name": "dynamic-zone-4",
    }
}

solver_session.settings.setup.dynamic_mesh.dynamic_zones = {
    "dynamic-zone-5": {
        "solver": {"stabilization": {"enabled": False}},
        "geometry": {"feature_detection": {"enabled": False}},
        "meshing": {
            "udf_deform": {"max_skew": 0.7, "enabled": True},
            "adjacent_zones": {"t0": {"height": 0.0, "type": "constant"}},
        },
        "motion": {
            "relative_motion": {"enabled": False},
            "exclude_motion_bc": False,
            "motion_def": "**ablation**",
        },
        "type": "user-defined",
        "zone": "wall_ablation",
        "name": "dynamic-zone-5",
    }
}

############################################
# Define solver settings
# =======================

solver_session.setup.general.solver.time = "unsteady-2nd-order"
solver_session.solution.controls.limits = {"max_temperature": 25000}
solver_session.solution.monitor.residual.equations["energy"].absolute_criteria = 1e-06

############################################
# Create report definitions
# ==========================

solver_session.settings.solution.report_definitions.drag.create(name="drag_force_x")
solver_session.settings.solution.report_definitions.drag["drag_force_x"].zones = [
    "wall_ablation"
]
solver_session.settings.solution.monitor.report_plots.create(name="drag_force_x")
solver_session.settings.solution.monitor.report_plots["drag_force_x"].report_defs = (
    "drag_force_x"
)
solver_session.settings.solution.monitor.report_files.create(name="drag_force_x")
solver_session.settings.solution.monitor.report_files["drag_force_x"] = {
    "file_name": "drag_force_x.out",
    "report_defs": ["drag_force_x"],
}

solver_session.settings.solution.report_definitions.surface.create(
    name="pressure_avg_abl_wall"
)
solver_session.settings.solution.report_definitions.surface[
    "pressure_avg_abl_wall"
].report_type = "surface-areaavg"
solver_session.settings.solution.report_definitions.surface[
    "pressure_avg_abl_wall"
].field = "pressure"
solver_session.settings.solution.report_definitions.surface[
    "pressure_avg_abl_wall"
].surface_names = ["wall_ablation"]
solver_session.settings.solution.monitor.report_plots.create(
    name="pressure_avg_abl_wall"
)
solver_session.settings.solution.monitor.report_plots[
    "pressure_avg_abl_wall"
].report_defs = "pressure_avg_abl_wall"
solver_session.settings.solution.monitor.report_files.create(
    name="pressure_avg_abl_wall"
)
solver_session.settings.solution.monitor.report_files["pressure_avg_abl_wall"] = {
    "report_defs": ["pressure_avg_abl_wall"],
    "file_name": "pressure_avg_abl_wall.out",
}

solver_session.settings.solution.report_definitions.surface.create(name="recede_point")
solver_session.settings.solution.report_definitions.surface[
    "recede_point"
].report_type = "surface-vertexmax"
solver_session.settings.solution.report_definitions.surface["recede_point"].field = (
    "z-coordinate"
)
solver_session.settings.solution.report_definitions.surface[
    "recede_point"
].surface_names = ["wall_ablation"]
solver_session.settings.solution.monitor.report_plots.create(name="recede_point")
solver_session.settings.solution.monitor.report_plots["recede_point"].report_defs = (
    "recede_point"
)
solver_session.settings.solution.monitor.report_files.create(name="recede_point")
solver_session.settings.solution.monitor.report_files["recede_point"] = {
    "file_name": "recede_point.out",
    "report_defs": ["recede_point"],
}

############################################
# Initialize and Save case
# ========================

solver_session.solution.initialization.compute_defaults(
    from_zone_type="pressure-far-field", from_zone_name="inlet", phase="mixture"
)
solver_session.solution.initialization.initialization_type = "standard"
solver_session.solution.initialization.standard_initialize()
solver_session.solution.run_calculation.transient_controls.time_step_size = 1e-06

solver_session.file.write(file_type="case", file_name="ablation.cas.h5")

############################################
# Run the calculation
# ===================
# Note: It may take about half an hour to finish the calculation.

solver_session.solution.run_calculation.dual_time_iterate(
    time_step_count=100, max_iter_per_step=20
)

###############################################
# Save simulation data
# ====================
# Write case and data files
solver_session.file.write(file_type="case-data", file_name="ablation_Solved.cas.h5")

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

solver_session.results.surfaces.plane_surface.create(name="mid_plane")
solver_session.results.surfaces.plane_surface["mid_plane"].method = "zx-plane"

solver_session.results.graphics.contour.create(name="contour_pressure")
solver_session.results.graphics.contour["contour_pressure"] = {
    "field": "pressure",
    "surfaces_list": ["mid_plane"],
}
solver_session.results.graphics.contour.display(object_name="contour_pressure")

solver_session.results.graphics.contour.create(name="contour_mach")
solver_session.results.graphics.contour["contour_mach"] = {
    "field": "mach-number",
    "surfaces_list": ["mid_plane"],
}
solver_session.results.graphics.contour.display(object_name="contour_mach")

###############################################
# Post processing with PyVista (3D visualization)
# ===============================================
# Following graphics is displayed in the a new window/notebook


contour1 = Contour(solver=solver_session, field="pressure", surfaces=["mid_plane"])

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

solver_session.exit()

# sphinx_gallery_thumbnail_path = '_static/ablation-mach-number-thumbnail.png'
