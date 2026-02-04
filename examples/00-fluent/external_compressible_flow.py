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

""".. _ref_external_compressible_flow_settings_api:

Modeling External Compressible Flow
-----------------------------------
The purpose of this tutorial is to compute the turbulent flow past a transonic
wing at a nonzero angle of attack using the k-w SST turbulence model.

This example uses the guided workflow for watertight geometry meshing
because it is appropriate for geometries that can have no imperfections,
such as gaps and leakages.

**Workflow tasks**

The Modeling External Compressible Flow Using the Meshing Workflow guides you through these tasks:

- Creation of capsule mesh using Watertight Geometry workflow.
- Model compressible flow (using the ideal gas law for density).
- Set boundary conditions for external aerodynamics.
- Use the k-w SST turbulence model.
- Calculate a solution using the pressure-based coupled solver with global time step selected for the pseudo time method.
- Check the near-wall mesh resolution by plotting the distribution of .

**Problem description**

The problem considers the flow around a wing at an angle of attack a=3.06° and a free stream Mach
number of 0.8395 (M=0.8395). The flow is transonic, and has a shock near the mid-chord (x/c≃0.20)
on the upper (suction) side. The wing has a mean aerodynamic chord length of 0.64607 m, a span of 1.1963 m,
an aspect ratio of 3.8, and a taper ratio of 0.562.
"""

###############################################################################
# .. image:: /_static/external_compressible_flow_011.png
#   :width: 500pt
#   :align: center

###############################################################################
# Example Setup
# -------------
# Before you can use the meshing workflow, you must set up the
# example and initialize this workflow.
#
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Perform required imports, which includes downloading and importing
# the geometry files.

# sphinx_gallery_thumbnail_path = '_static/external_compressible_flow.png'
import shutil
import tempfile

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.core.generated.solver.settings_builtin import RunCalculation
from ansys.fluent.core.generated.solver.settings_builtin_261 import write_case
from ansys.fluent.core.solver import (
    FluidMaterial,
    General,
    Initialization,
    PressureFarFieldBoundary,
    Viscous,
)
from ansys.units.common import K, Pa, kg, m, s

wing_spaceclaim_file, wing_intermediary_file = [
    examples.download_file(CAD_file, "pyfluent/external_compressible")
    for CAD_file in ["wing.scdoc", "wing.pmdb"]
]

###############################################################################
# Launch Fluent
# ~~~~~~~~~~~~~
# Launch Fluent as a service in meshing mode with double precision running on
# four processors and print Fluent version.

meshing = pyfluent.Meshing.from_install(
    precision=pyfluent.Precision.DOUBLE,
    processor_count=4,
)
print(meshing.get_fluent_version())

tmpdir = tempfile.mkdtemp()
meshing.preferences.MeshingWorkflow.TempFolder = tmpdir

###############################################################################
# Initialize workflow
# ~~~~~~~~~~~~~~~~~~~
# Initialize the watertight geometry meshing workflow.

meshing.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")

###############################################################################
# Watertight geometry meshing workflow
# ------------------------------------
# The fault-tolerant meshing workflow guides you through the several tasks that
# follow.
#
# Import CAD and set length units
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import the CAD geometry and set the length units to inches.
geo_import = meshing.workflow.TaskObject["Import Geometry"]
geo_import.Arguments.set_state(
    {
        "FileName": wing_intermediary_file,
    }
)

geo_import.Execute()

###############################################################################
# Add local sizing
# ~~~~~~~~~~~~~~~~
# Add local sizing controls to the faceted geometry.
local_sizing = meshing.workflow.TaskObject["Add Local Sizing"]
local_sizing.Arguments.set_state(
    {
        "AddChild": "yes",
        "BOIControlName": "wing-facesize",
        "BOIFaceLabelList": ["wing_bottom", "wing_top"],
        "BOISize": 10,
    }
)

local_sizing.AddChildAndUpdate()

local_sizing.Arguments.set_state(
    {
        "AddChild": "yes",
        "BOIControlName": "wing-ege-facesize",
        "BOIFaceLabelList": ["wing_edge"],
        "BOISize": 2,
    }
)

local_sizing.AddChildAndUpdate()

local_sizing.Arguments.set_state(
    {
        "AddChild": "yes",
        "BOIControlName": "boi_1",
        "BOIExecution": "Body Of Influence",
        "BOIFaceLabelList": ["wing-boi"],
        "BOISize": 5,
    }
)

local_sizing.AddChildAndUpdate()

###############################################################################
# Generate surface mesh
# ~~~~~~~~~~~~~~~~~~~~~
# Generate the surface mash.
surface_mesh_gen = meshing.workflow.TaskObject["Generate the Surface Mesh"]
surface_mesh_gen.Arguments.set_state(
    {"CFDSurfaceMeshControls": {"MaxSize": 1000, "MinSize": 2}}
)

surface_mesh_gen.Execute()

###############################################################################
# Describe geometry
# ~~~~~~~~~~~~~~~~~
# Describe geometry and define the fluid region.
describe_geo = meshing.workflow.TaskObject["Describe Geometry"]
describe_geo.UpdateChildTasks(SetupTypeChanged=False)

describe_geo.Arguments.set_state(
    {"SetupType": "The geometry consists of only fluid regions with no voids"}
)

describe_geo.UpdateChildTasks(SetupTypeChanged=True)

describe_geo.Execute()

###############################################################################
# Update boundaries
# ~~~~~~~~~~~~~~~~~
# Update the boundaries.

meshing.workflow.TaskObject["Update Boundaries"].Execute()

###############################################################################
# Update regions
# ~~~~~~~~~~~~~~
# Update the regions.

meshing.workflow.TaskObject["Update Regions"].Execute()

###############################################################################
# Add boundary layers
# ~~~~~~~~~~~~~~~~~~~
# Add boundary layers, which consist of setting properties for the
# boundary layer mesh.
add_boundary_layer = meshing.workflow.TaskObject["Add Boundary Layers"]
add_boundary_layer.Arguments.set_state({"NumberOfLayers": 12})

add_boundary_layer.AddChildAndUpdate()

###############################################################################
# Generate volume mesh
# ~~~~~~~~~~~~~~~~~~~~
# Generate the volume mesh, which consists of setting properties for the
# volume mesh.
volume_mesh_gen = meshing.workflow.TaskObject["Generate the Volume Mesh"]
volume_mesh_gen.Arguments.set_state(
    {
        "VolumeFill": "poly-hexcore",
        "VolumeFillControls": {"HexMaxCellLength": 512},
        "VolumeMeshPreferences": {
            "CheckSelfProximity": "yes",
            "ShowVolumeMeshPreferences": True,
        },
    }
)

volume_mesh_gen.Execute()

###############################################################################
# Check mesh in meshing mode
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# Check the mesh in meshing mode.

meshing.tui.mesh.check_mesh()

###############################################################################
# Save mesh file
# ~~~~~~~~~~~~~~
# Save the mesh file (``wing.msh.h5``).

meshing.meshing.File.WriteMesh(FileName="wing.msh.h5")

###############################################################################
# Solve and postprocess
# ---------------------
# Once you have completed the watertight geometry meshing workflow, you can
# solve and postprocess the results.
#
# Switch to solution mode
# ~~~~~~~~~~~~~~~~~~~~~~~
# Switch to solution mode. Now that a high-quality mesh has been generated
# using Fluent in meshing mode, you can switch to solver mode to complete the
# setup of the simulation.

solver = meshing.switch_to_solver()

###############################################################################
# Check mesh in solver mode
# ~~~~~~~~~~~~~~~~~~~~~~~~~
# Check the mesh in solver mode. The mesh check lists the minimum and maximum
# x, y, and z values from the mesh in the default SI units of meters. It also
# reports a number of other mesh features that are checked. Any errors in the
# mesh are reported.

solver.settings.mesh.check()

###############################################################################
# Define model
# ~~~~~~~~~~~~
# Set the k-w sst turbulence model.

# model : k-omega
# k-omega model : sst

viscous = Viscous(solver)

viscous.model = viscous.model.K_OMEGA
viscous.k_omega_model = viscous.k_omega_model.SST

###############################################################################
# Define materials
# ~~~~~~~~~~~~~~~~
# Modify the default material ``air`` to account for compressibility and variations of the thermophysical properties with temperature.

air = FluidMaterial.get(solver, name="air")

air.density.option = "ideal-gas"

air.viscosity.option = "sutherland"

air.viscosity.sutherland.option = "three-coefficient-method"

air.viscosity.sutherland.reference_viscosity = 1.716e-05 * kg / (m * s)

air.viscosity.sutherland.reference_temperature = 273.11 * K

air.viscosity.sutherland.effective_temperature = 110.56 * K

###############################################################################
# Boundary Conditions
# ~~~~~~~~~~~~~~~~~~~
# Set the boundary conditions for ``pressure_farfield``.

pressure_far_field = PressureFarFieldBoundary.get(solver, name="pressure_farfield")

pressure_far_field.momentum.gauge_pressure = 0 * Pa

pressure_far_field.momentum.mach_number = 0.8395

pressure_far_field.thermal.temperature = 255.56 * K

pressure_far_field.momentum.flow_direction[0] = 0.998574  # x-component

pressure_far_field.momentum.flow_direction[2] = 0.053382  # z-component

pressure_far_field.turbulence.turbulent_intensity = 0.05

pressure_far_field.turbulence.turbulent_viscosity_ratio = 10

###############################################################################
# Operating Conditions
# ~~~~~~~~~~~~~~~~~~~~
# Set the operating conditions.

general = General(solver)
general.operating_conditions.operating_pressure = 80_600 * Pa

###############################################################################
# Initialize flow field
# ~~~~~~~~~~~~~~~~~~~~~
# Initialize the flow field using hybrid initialization.

initialize = Initialization(solver)
initialize.hybrid_initialize()

###############################################################################
# Save case file
# ~~~~~~~~~~~~~~
# Save the case file ``external_compressible1.cas.h5``.

write_case(
    solver,
    file_name="external_compressible.cas.h5"
)

###############################################################################
# Solve for 25 iterations
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Solve for 25 iterations (100 iterations is recommended, however for this example 25 is sufficient).

RunCalculation(solver).iterate(iter_count=25)

###############################################################################
# Write final case file and data
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Write the final case file and the data.

write_case(
    solver,
    file_name="external_compressible1.cas.h5"
)

###############################################################################
# Close Fluent
# ~~~~~~~~~~~~
# Close Fluent.

solver.exit()

shutil.rmtree(tmpdir, ignore_errors=True)
shutil.rmtree("wing_workflow_files", ignore_errors=True)

###############################################################################
