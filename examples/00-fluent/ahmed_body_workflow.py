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

""".. _ahmed_body_simulation:

Ahmed Body External Aerodynamics Simulation
-------------------------------------------
"""

#######################################################################################
# Objective
# =====================================================================================
#
# Ahmed body is a simplified car model used for studying the flow around it and to
# predict the drag and lift forces. The model consists of a slanted back and a blunt
# front.
#
# In this example, PyFluent API is used to perform Ahmed Body external aerodynamics
# simulation. which includes typical workflow of CFD Simulation as follows:
#
# * Importing the geometry/CAD model.
# * Meshing the geometry.
# * Setting up the solver.
# * Running the solver.
# * Post-processing the results.
#
#
#
# .. image:: ../../_static/ahmed_body_model.png
#    :align: center
#    :alt: Ahmed Body Model


#######################################################################################
# Import required libraries/modules
# =====================================================================================

from pathlib import Path
import platform

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
import ansys.fluent.core.meshing.meshing_workflow_new as mesh_wf_new
from ansys.fluent.core.session_pure_meshing import PureMeshing
from ansys.fluent.core.solver import (
    FluidMaterial,
    Initialization,
    IsoSurface,
    Methods,
    Monitor,
    OutputParameters,
    PressureOutlet,
    ReferenceValues,
    ReportDefinitions,
    Residual,
    VelocityInlet,
    Viscous,
    iterate,
    write_case,
)
from ansys.fluent.visualization import Contour, GraphicsWindow
from ansys.units import VariableCatalog
from ansys.units.common import kg, m, s

#######################################################################################
# Launch Fluent session with meshing mode and print Fluent version
# =====================================================================================
meshing: PureMeshing = pyfluent.Meshing.from_install()
print(meshing.get_fluent_version())

#######################################################################################
# Meshing Workflow
# =====================================================================================

#######################################################################################
# Initialize the Meshing Workflow
# =====================================================================================

workflow: mesh_wf_new.WatertightMeshingWorkflow = meshing.watertight(legacy=False)

filenames = {
    "Windows": "ahmed_body_20_0degree_boi_half.scdoc",
    "Other": "ahmed_body_20_0degree_boi_half.scdoc.pmdb",
}

geometry_filename = examples.download_file(
    filenames.get(platform.system(), filenames["Other"]),
    "pyfluent/examples/Ahmed-Body-Simulation",
    save_path=Path.cwd(),
)
meshing.upload(geometry_filename)

workflow.application.import_geometry(file_name=geometry_filename)

#######################################################################################
# Add Local Face Sizing
# =====================================================================================

add_local_sizing = workflow.application.add_local_sizing_wtm(
    add_child=True,
    boi_control_name="facesize_front",
    boi_face_label_list=["wall_ahmed_body_front"],
    boi_growth_rate=1.15,
    boi_size=8,
)

workflow.application.add_local_sizing_wtm(
    add_child=True,
    boi_control_name="facesize_rear",
    boi_face_label_list=["wall_ahmed_body_rear"],
    boi_growth_rate=1.15,
    boi_size=5,
)


workflow.application.add_local_sizing_wtm(
    add_child=True,
    boi_control_name="facesize_main",
    boi_face_label_list=["wall_ahmed_body_main"],
    boi_growth_rate=1.15,
    boi_size=12,
)

#######################################################################################
# Add BOI (Body of Influence) Sizing
# =====================================================================================
workflow.application.add_local_sizing_wtm(
    add_child=True,
    boi_control_name="boi_1",
    boi_execution="Body Of Influence",  # Using a string as no enum is currently available
    boi_face_label_list=["ahmed_body_20_0degree_boi_half-boi"],
    boi_size=20,
)


#######################################################################################
# Add Surface Mesh Sizing
# =====================================================================================
workflow.application.create_surface_mesh.cfd_surface_mesh_controls(  # TODO double check this works (new_meshing_workflows.rst kinda implies it does)
    curvature_normal_angle=12,
    growth_rate=1.15,
    max_size=50,
    min_size=1,
    size_functions="curvature",  # Using a string as no enum is currently available
)

workflow.application.improve_surface_mesh(face_quality_limit=0.4)

#######################################################################################
# Describe Geometry, Update Boundaries, Update Regions
# =====================================================================================
workflow.application.describe_geometry(
    capping_required=True,
    setup_type="fluid",  # Using a string as no enum is currently available
)
update_boundaries = workflow.application.update_boundaries()
update_regions = workflow.application.update_regions()

#######################################################################################
# Add Boundary Layers
# =====================================================================================
workflow.application.add_boundary_layers(
    control_name="smooth-transition_1",
    number_of_layers=14,
    rate=1.15,
    transition_ratio=0.5,
)


#######################################################################################
# Generate the Volume Mesh
# =====================================================================================
workflow.application.create_volume_mesh_wtm(
    volume_fill="poly-hexcore"  # Using a string as no enum is currently available
)

#######################################################################################
# Switch to the Solver Mode
# =====================================================================================
solver = meshing.switch_to_solver()

#######################################################################################
# Mesh Visualization
# =====================================================================================

# %%
# .. image:: ../../_static/ahmed_body_mesh_1.png
#    :align: center
#    :alt: Ahmed Body Mesh

# %%
# .. image:: ../../_static/ahmed_body_mesh_2.png
#    :align: center
#    :alt: Ahmed Body Mesh

#######################################################################################
# Solver Setup and Solve Workflow
# =====================================================================================

#######################################################################################
# Define Constants
# =====================================================================================
density = 1.225 * kg / m**3
inlet_velocity = 30 * m / s
inlet_area = 0.11203202 * m**2

#######################################################################################
# Define Materials
# =====================================================================================
air = FluidMaterial(solver).get("air")
air.density = density

viscous = Viscous(solver=solver)
viscous.model = viscous.model.K_EPSILON
viscous.k_epsilon_model = viscous.k_epsilon_model.REALIZABLE
viscous.options.curvature_correction = True

#######################################################################################
# Define Boundary Conditions
# =====================================================================================
inlet = VelocityInlet(solver).get(name="inlet")
inlet.turbulence.turb_intensity = 0.05
inlet.momentum.velocity.value = inlet_velocity
inlet.turbulence.turb_viscosity_ratio = 5

outlet = PressureOutlet.get(solver, name="outlet")
outlet.turbulence.turb_intensity = 0.05

#######################################################################################
# Define Reference Values
# =====================================================================================
ref_values = ReferenceValues(solver)
ref_values.area = inlet_area
ref_values.density = density
ref_values.velocity = inlet_velocity

#######################################################################################
# Define Solver Settings
# =====================================================================================
methods = Methods(solver)
methods.p_v_coupling.flow_scheme = "Coupled"

discretization_scheme = methods.spatial_discretization.discretization_scheme
discretization_scheme["pressure"] = "second-order"
discretization_scheme["k"] = "second-order-upwind"
discretization_scheme["epsilon"] = "second-order-upwind"
initialization = Initialization(solver)
initialization.defaults.k = 1e-6

residual = Residual(solver)
for monitor in (
    "continuity",
    "x-velocity",
    "y-velocity",
    "z-velocity",
    "k",
    "epsilon",
):
    residual.equations[monitor].absolute_criteria = 1e-4

#######################################################################################
# Define Report Definitions
# =====================================================================================

drag = ReportDefinitions(solver).drag.create(
    name="cd-mon1",
    zones=[
        "wall_ahmed_body_main",
        "wall_ahmed_body_front",
        "wall_ahmed_body_rear",
    ],
    force_vector=(0, 0, 1),
)

params_report_defs = OutputParameters(solver).report_definitions
param_1 = params_report_defs.create(report_def_name=drag)

monitor = Monitor(solver)
plot_mon = monitor.report_plots.create(name=drag, print=True, report_defs=[drag])

#######################################################################################
# Initialize and Run Solver
# =====================================================================================

init = Initialization(solver)
init.initialization_type = "standard"
init.standard_initialize()
iterate(solver, iter_count=5)

#######################################################################################
# Post-Processing Workflow
# =====================================================================================
iso = IsoSurface(solver).create(name="xmid", field="x-coordinate", iso_values=[0 * m])

velocity_mag = Contour(
    solver=solver, field=VariableCatalog.VELOCITY_MAGNITUDE, surfaces=["xmid"]
)
disp1 = GraphicsWindow()
disp1.add_graphics(velocity_mag)
disp1.show()

pressure_coeff = Contour(
    solver=solver, field=VariableCatalog.PRESSURE_COEFFICIENT, surfaces=["xmid"]
)
disp2 = GraphicsWindow()
disp2.add_graphics(pressure_coeff)
disp2.show()

#######################################################################################
# Simulation Results Visualization
# =====================================================================================

# %%
# .. image:: ../../_static/ahmed_body_model_velocity_mag.png
#    :align: center
#    :alt: Velocity Magnitude

# %%
#    Velocity Magnitude Contour

# %%
# .. image:: ../../_static/ahmed_body_model_pressure_coeff.png
#    :align: center
#    :alt: Peressure Coefficient

# %%
#    Pressure Coefficient Contour

#######################################################################################
# Save the case file
# =====================================================================================
write_case(solver, file_name="ahmed_body_final.cas.h5")

#######################################################################################
# Close the session
# =====================================================================================
solver.exit()


#######################################################################################
# References
# =====================================================================================
#
# [1] S.R. Ahmed, G. Ramm, Some Salient Features of the Time-Averaged Ground Vehicle
# Wake,SAE-Paper 840300,1984

# sphinx_gallery_thumbnail_path = '_static/ahmed_body_model_pressure_coeff.png'
