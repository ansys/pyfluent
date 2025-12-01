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

import os
import platform

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.visualization import Contour, GraphicsWindow

#######################################################################################
# Launch Fluent session with meshing mode and print Fluent version
# =====================================================================================
session = pyfluent.launch_fluent(mode="meshing", cleanup_on_exit=True)
print(session.get_fluent_version())

#######################################################################################
# Meshing Workflow
# =====================================================================================

#######################################################################################
# Initialize the Meshing Workflow
# =====================================================================================

workflow = session.workflow

filenames = {
    "Windows": "ahmed_body_20_0degree_boi_half.scdoc",
    "Other": "ahmed_body_20_0degree_boi_half.scdoc.pmdb",
}

geometry_filename = examples.download_file(
    filenames.get(platform.system(), filenames["Other"]),
    "pyfluent/examples/Ahmed-Body-Simulation",
    save_path=os.getcwd(),
)

workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
workflow.TaskObject["Import Geometry"].Arguments = dict(FileName=geometry_filename)
workflow.TaskObject["Import Geometry"].Execute()

#######################################################################################
# Add Local Face Sizing
# =====================================================================================
add_local_sizing = workflow.TaskObject["Add Local Sizing"]
add_local_sizing.Arguments = dict(
    {
        "AddChild": "yes",
        "BOIControlName": "facesize_front",
        "BOIFaceLabelList": ["wall_ahmed_body_front"],
        "BOIGrowthRate": 1.15,
        "BOISize": 8,
    }
)
add_local_sizing.Execute()

add_local_sizing.InsertCompoundChildTask()
workflow.TaskObject["Add Local Sizing"].Execute()
add_local_sizing = workflow.TaskObject["Add Local Sizing"]
add_local_sizing.Arguments = dict(
    {
        "AddChild": "yes",
        "BOIControlName": "facesize_rear",
        "BOIFaceLabelList": ["wall_ahmed_body_rear"],
        "BOIGrowthRate": 1.15,
        "BOISize": 5,
    }
)
add_local_sizing.Execute()

add_local_sizing.InsertCompoundChildTask()
workflow.TaskObject["Add Local Sizing"].Execute()
add_local_sizing = workflow.TaskObject["Add Local Sizing"]
add_local_sizing.Arguments = dict(
    {
        "AddChild": "yes",
        "BOIControlName": "facesize_main",
        "BOIFaceLabelList": ["wall_ahmed_body_main"],
        "BOIGrowthRate": 1.15,
        "BOISize": 12,
    }
)
add_local_sizing.Execute()

#######################################################################################
# Add BOI (Body of Influence) Sizing
# =====================================================================================
add_boi_sizing = workflow.TaskObject["Add Local Sizing"]
add_boi_sizing.InsertCompoundChildTask()
add_boi_sizing.Arguments = dict(
    {
        "AddChild": "yes",
        "BOIControlName": "boi_1",
        "BOIExecution": "Body Of Influence",
        "BOIFaceLabelList": ["ahmed_body_20_0degree_boi_half-boi"],
        "BOISize": 20,
    }
)
add_boi_sizing.Execute()
add_boi_sizing.InsertCompoundChildTask()


#######################################################################################
# Add Surface Mesh Sizing
# =====================================================================================
generate_surface_mesh = workflow.TaskObject["Generate the Surface Mesh"]
generate_surface_mesh.Arguments = dict(
    {
        "CFDSurfaceMeshControls": {
            "CurvatureNormalAngle": 12,
            "GrowthRate": 1.15,
            "MaxSize": 50,
            "MinSize": 1,
            "SizeFunctions": "Curvature",
        }
    }
)

generate_surface_mesh.Execute()
generate_surface_mesh.InsertNextTask(CommandName="ImproveSurfaceMesh")
improve_surface_mesh = workflow.TaskObject["Improve Surface Mesh"]
improve_surface_mesh.Arguments.update_dict({"FaceQualityLimit": 0.4})
improve_surface_mesh.Execute()

#######################################################################################
# Describe Geometry, Update Boundaries, Update Regions
# =====================================================================================
workflow.TaskObject["Describe Geometry"].Arguments = dict(
    CappingRequired="Yes",
    SetupType="The geometry consists of only fluid regions with no voids",
)
workflow.TaskObject["Describe Geometry"].Execute()
workflow.TaskObject["Update Boundaries"].Execute()
workflow.TaskObject["Update Regions"].Execute()

#######################################################################################
# Add Boundary Layers
# =====================================================================================
add_boundary_layers = workflow.TaskObject["Add Boundary Layers"]
add_boundary_layers.AddChildToTask()
add_boundary_layers.InsertCompoundChildTask()
workflow.TaskObject["smooth-transition_1"].Arguments.update_dict(
    {
        "BLControlName": "smooth-transition_1",
        "NumberOfLayers": 14,
        "Rate": 1.15,
        "TransitionRatio": 0.5,
    }
)
add_boundary_layers.Execute()


#######################################################################################
# Generate the Volume Mesh
# =====================================================================================
generate_volume_mesh = workflow.TaskObject["Generate the Volume Mesh"]
generate_volume_mesh.Arguments.update_dict({"VolumeFill": "poly-hexcore"})
generate_volume_mesh.Execute()

#######################################################################################
# Switch to the Solver Mode
# =====================================================================================
session = session.switch_to_solver()

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
density = 1.225
inlet_velocity = 30
inlet_area = 0.11203202

#######################################################################################
# Define Materials
# =====================================================================================
session.tui.define.materials.change_create("air", "air", "yes", "constant", density)
session.settings.setup.models.viscous.model = "k-epsilon"
session.settings.setup.models.viscous.k_epsilon_model = "realizable"
session.settings.setup.models.viscous.options.curvature_correction = True

#######################################################################################
# Define Boundary Conditions
# =====================================================================================
inlet = session.settings.setup.boundary_conditions.velocity_inlet["inlet"]
inlet.turbulence.turb_intensity = 0.05
inlet.momentum.velocity.value = inlet_velocity
inlet.turbulence.turb_viscosity_ratio = 5

outlet = session.settings.setup.boundary_conditions.pressure_outlet["outlet"]
outlet.turbulence.turb_intensity = 0.05

#######################################################################################
# Define Reference Values
# =====================================================================================
session.settings.setup.reference_values.area = inlet_area
session.settings.setup.reference_values.density = density
session.settings.setup.reference_values.velocity = inlet_velocity

#######################################################################################
# Define Solver Settings
# =====================================================================================
session.tui.solve.set.p_v_coupling(24)

session.tui.solve.set.discretization_scheme("pressure", 12)
session.tui.solve.set.discretization_scheme("k", 1)
session.tui.solve.set.discretization_scheme("epsilon", 1)
session.tui.solve.initialize.set_defaults("k", 0.000001)

session.settings.solution.monitor.residual.equations["continuity"].absolute_criteria = (
    0.0001
)
session.settings.solution.monitor.residual.equations["x-velocity"].absolute_criteria = (
    0.0001
)
session.settings.solution.monitor.residual.equations["y-velocity"].absolute_criteria = (
    0.0001
)
session.settings.solution.monitor.residual.equations["z-velocity"].absolute_criteria = (
    0.0001
)
session.settings.solution.monitor.residual.equations["k"].absolute_criteria = 0.0001
session.settings.solution.monitor.residual.equations["epsilon"].absolute_criteria = (
    0.0001
)

#######################################################################################
# Define Report Definitions
# =====================================================================================

session.settings.solution.report_definitions.drag["cd-mon1"] = {}
session.settings.solution.report_definitions.drag["cd-mon1"] = {
    "zones": ["wall_ahmed_body_main", "wall_ahmed_body_front", "wall_ahmed_body_rear"],
    "force_vector": [0, 0, 1],
}
session.parameters.output_parameters.report_definitions.create(name="parameter-1")
session.parameters.output_parameters.report_definitions["parameter-1"] = {
    "report_definition": "cd-mon1"
}

session.settings.solution.monitor.report_plots.create(name="cd-mon1")
session.settings.solution.monitor.report_plots["cd-mon1"] = {"report_defs": ["cd-mon1"]}

#######################################################################################
# Initialize and Run Solver
# =====================================================================================

session.settings.solution.run_calculation.iter_count = 5
session.settings.solution.initialization.initialization_type = "standard"
session.settings.solution.initialization.standard_initialize()
session.settings.solution.run_calculation.iterate(iter_count=5)

#######################################################################################
# Post-Processing Workflow
# =====================================================================================
session.results.surfaces.iso_surface.create(name="xmid")
session.results.surfaces.iso_surface["xmid"].field = "x-coordinate"
session.results.surfaces.iso_surface["xmid"] = {"iso_values": [0]}

contour1 = Contour(solver=session, field="velocity-magnitude", surfaces=["xmid"])
disp1 = GraphicsWindow()
disp1.add_graphics(contour1)
disp1.show()

contour2 = Contour(solver=session, surfaces=["xmid"])
contour2.field.allowed_values
contour2.field = "pressure-coefficient"
disp2 = GraphicsWindow()
disp2.add_graphics(contour2)
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
session.settings.file.write(file_type="case-data", file_name="ahmed_body_final.cas.h5")

#######################################################################################
# Close the session
# =====================================================================================
session.exit()


#######################################################################################
# References
# =====================================================================================
#
# [1] S.R. Ahmed, G. Ramm, Some Salient Features of the Time-Averaged Ground Vehicle
# Wake,SAE-Paper 840300,1984

# sphinx_gallery_thumbnail_path = '_static/ahmed_body_model_pressure_coeff.png'
