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

""".. _ref_radiation_headlamp:

Modeling Radiation in a Headlamp Using the Monte Carlo Method
-------------------------------------------------------------
This example solves for the radiative and conductive heat transfer within a car
headlamp exposed to the sun's rays to determine the severity of any hotspots
that form. It uses a Monte Carlo radiation model and the  pressure-based
solver. This is based on the Fluent tutorial titled "Using the Monte Carlo
Radiation Model".

**Workflow tasks**

The Modeling Radiation Using the Monte Carlo Method example guides you through
these tasks:

- Creation of a mesh using the Watertight Geometry workflow.
- Setting up a Monte Carlo radiation model.
- Creation of materials with thermal and radiation properties.
- Setting boundary conditions for heat transfer and radiation calculations.
- Calculating a solution using the pressure-based solver.

**Problem description**

The problem considers the headlamp of a parked car exposed to sunlight. The
lens focuses incoming radiation onto the internal components of the headlamp,
producing thermal hotspots that could cause damage due to thermal stresses or
material degradation.
"""

###############################################################################
# .. image:: ../../_static/radiation_headlamp_geom.png
#   :width: 500pt
#   :align: center

###############################################################################
# Example Setup
# -------------
# Before you can use the watertight geometry meshing workflow, you must set up
# the example and initialize this workflow.
#
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Perform required imports, which includes downloading and importing the
# geometry files.

from pathlib import Path

from ansys.units import VariableCatalog

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.core.generated.solver.settings_builtin import CellZoneConditions
from ansys.fluent.core.generated.solver.settings_builtin_261 import BoundaryCondition, ReportPlot, initialize, iterate, write_case, write_case_data
from ansys.fluent.core.solver import (
    BoundaryConditions,
    Initialization,
    Models,
    Monitor,
    ReportDefinitions,
    RunCalculation,
    SolidCellZone,
    SolidMaterial,
    Solution,
    WallBoundary,
)
from ansys.units.common import J, K, W, kg, m

headlamp_spaceclaim_file, headlamp_pmdb_file = [
    examples.download_file(
        f,
        "pyfluent/radiation_headlamp",
        save_path=Path.cwd(),
    )
    for f in ["headlamp.scdoc", "headlamp.pmdb"]
]

###############################################################################
# Launch Fluent
# ~~~~~~~~~~~~~
# Launch Fluent as a service in meshing mode with single precision running on
# four processors and print Fluent version.

meshing = pyfluent.Meshing.from_install(
    precision="single",
    processor_count=4,
)
print(meshing.get_fluent_version())

# Upload downloaded example files to the meshing session
meshing.upload(headlamp_spaceclaim_file)
meshing.upload(headlamp_pmdb_file)

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
# Import the CAD geometry and set the length units to millimeters.

geo_import = meshing.workflow.TaskObject["Import Geometry"]
geo_import.Arguments.set_state(
    {
        "FileName": headlamp_pmdb_file,
        "LengthUnit": "mm",
    }
)

geo_import.Execute()

###############################################################################
# Add local sizing
# ~~~~~~~~~~~~~~~~
# Add local sizing controls to the geometry.

local_sizing = meshing.workflow.TaskObject["Add Local Sizing"]
local_sizing.Arguments.set_state(
    {
        "AddChild": "yes",
        "BOIControlName": "boi_lens",
        "BOIExecution": "Body Of Influence",
        "BOIFaceLabelList": ["boi"],
        "BOISize": 2,
    }
)

local_sizing.AddChildAndUpdate()

local_sizing.Arguments.set_state(
    {
        "AddChild": "yes",
        "BOIControlName": "bodysize_lens",
        "BOIExecution": "Body Size",
        "BOIFaceLabelList": ["lens"],
        "BOISize": 2,
    }
)

local_sizing.AddChildAndUpdate()

###############################################################################
# Generate surface mesh
# ~~~~~~~~~~~~~~~~~~~~~
# Generate the surface mesh.

surface_mesh_gen = meshing.workflow.TaskObject["Generate the Surface Mesh"]
surface_mesh_gen.Arguments.set_state(
    {
        "CFDSurfaceMeshControls": {
            "MinSize": 1,
            "MaxSize": 40,
        }
    }
)

surface_mesh_gen.Execute()

###############################################################################
# Improve surface mesh
# ~~~~~~~~~~~~~~~~~~~~
# Improve the surface mesh.

surface_mesh_gen.InsertNextTask(CommandName="ImproveSurfaceMesh")

meshing.workflow.TaskObject["Improve Surface Mesh"].Execute()

###############################################################################
# Describe geometry
# ~~~~~~~~~~~~~~~~~
# Describe geometry and define the fluid region.

describe_geo = meshing.workflow.TaskObject["Describe Geometry"]
describe_geo.Arguments.set_state(
    {
        "SetupType": "The geometry consists of both fluid and solid regions and/or voids",
        "CappingRequired": "No",
        "WallToInternal": "No",
        "InvokeShareTopology": "No",
        "Multizone": "No",
    }
)

describe_geo.Execute()

###############################################################################
# Update boundaries
# ~~~~~~~~~~~~~~~~~
# Update the boundaries.

update_bc = meshing.workflow.TaskObject["Update Boundaries"]
update_bc.Arguments.set_state(
    {
        "BoundaryLabelList": ["rad-input"],
        "BoundaryLabelTypeList": ["wall"],
    }
)

update_bc.Execute()

###############################################################################
# Create fluid region
# ~~~~~~~~~~~~~~~~~~~
# Create the fluid region.

create_regions = meshing.workflow.TaskObject["Create Regions"]
create_regions.Arguments.set_state({"NumberOfFlowVolumes": 1})

create_regions.Execute()

###############################################################################
# Update regions
# ~~~~~~~~~~~~~~
# Update the regions.

meshing.workflow.TaskObject["Update Regions"].Execute()

###############################################################################
# Boundary layers
# ~~~~~~~~~~~~~~~~~~~
# Do not add boundary layers and proceed to the next task.

add_boundary_layers = meshing.workflow.TaskObject["Add Boundary Layers"]
add_boundary_layers.Arguments.set_state({"AddChild": "no"})

add_boundary_layers.Execute()

###############################################################################
# Generate volume mesh
# ~~~~~~~~~~~~~~~~~~~~
# Generate the volume mesh, which consists of setting properties for the
# volume mesh.

volume_mesh_gen = meshing.workflow.TaskObject["Generate the Volume Mesh"]
volume_mesh_gen.Arguments.set_state(
    {
        "VolumeMeshPreferences": {
            "PolyFeatureAngle": 40,
        },
    },
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
# Save the mesh file (``headlamp.msh.h5``).

meshing.meshing.File.WriteMesh(FileName="headlamp.msh.h5")
watertight.application.file.write_mesh
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
# Enable energy and viscosity models
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set up the energy and viscosity models.

models = Models(solver)
models.energy.enabled = True
models.viscous.model = models.viscous.model.LAMINAR

###############################################################################
# Set up radiation model
# ~~~~~~~~~~~~~~~~~~~~~~
# Set up the Monte Carlo radiation model. The number of histories is set to 10
# million in order to reduce computation time, but this may need to be
# increased to obtain accurate results.

radiation = models.radiation
radiation.model = models.radiation.model.MONTE_CARLO
radiation.monte_carlo.number_of_histories = 1e7
radiation.solve_frequency.iteration_interval = 20

###############################################################################
# Define materials
# ~~~~~~~~~~~~~~~~
# Create materials to represent the glass and plastic parts of the headlamp.
# To demonstrate two different methods of creating materials through the
# settings API, we will create glass using a dictionary and plastic using dot
# syntax.

# --- Properties of glass ---
glass = SolidMaterial.create(
    solver,
    name="glass",
    density=2650 * kg / m**3,
    specific_heat=1887 * J / (kg * K),
    thermal_conductivity=7.6 * W / (m * K),
    absorption_coefficient=5.302,
    refractive_index=1.4714,
)

# --- Properties of plastic ---
plastic = SolidMaterial.create(
    solver,
    name="plastic",
    density=1545.3 * kg / m**3,
    specific_heat=2302 * J / (kg * K),
    thermal_conductivity=0.316 * W / (m * K),
    absorption_coefficient=0,
    refractive_index=1,
)

###############################################################################
# Cell Zone Conditions
# ~~~~~~~~~~~~~~~~~~~~
# Set the cell zone conditions for the bezel and the lens.

SolidCellZone(solver, name="bezel").general.material = plastic
CellZoneConditions(solver).copy(
    from_="bezel",
    to=[
        "holder",
        "housing",
        "inner-bezel",
        "reflector",
        "rim-bezel",
        "seating-steel-rim",
    ],
)

lens_cellzone_conds = SolidCellZone.get(solver, name="lens")
lens_cellzone_conds.general.material = glass
lens_cellzone_conds.general.participates_in_radiation = True

###########################################################################################################
# Boundary Conditions
# ~~~~~~~~~~~~~~~~~~~
# Set the boundary conditions.

# --- Set up bezel-enclosure BC ---
bezel_enc_bc = WallBoundary.get(solver, name="bezel-enclosure")
bezel_enc_bc.thermal.material = plastic
bezel_enc_bc.radiation.bc_type = "Opaque"
bezel_enc_bc.radiation.internal_emissivity = 1
bezel_enc_bc.radiation.diffuse_irradiation_settings.diffuse_fraction_band = {"s-": 1}

# Get list of wall zones
bc = BoundaryCondition(solver)
zones_to_copy = bc()["wall"].keys() - {"bezel-enclosure", "enclosure:1", "rad-input"}

# Copy bezel-enclosure BC to all other BCs
bc.copy(from_="bezel-enclosure", to=list(zones_to_copy))

# --- Set up enclosure-lens BC ---
enc_lens_bc = WallBoundary.get(solver, name="enclosure-lens")
enc_lens_bc.thermal.material = glass
enc_lens_bc.radiation.bc_type = "Semi Transparent"
enc_lens_bc.radiation.diffuse_irradiation_settings.diffuse_fraction_band = {"s-": 0}

# Copy enclosure-lens BC to other lens boundary
bc.copy(from_="enclosure-lens", to=["enclosure-lens-shadow"])

# --- Set up enclosure-rim-bezel BC ---
enc_rim_bezel_bc = WallBoundary.get(solver, name="enclosure-rim-bezel")
enc_rim_bezel_bc.thermal.material = plastic
enc_rim_bezel_bc.radiation.bc_type = "Opaque"
enc_rim_bezel_bc.radiation.internal_emissivity = 0.16
enc_rim_bezel_bc.radiation.diffuse_irradiation_settings.diffuse_fraction_band = {
    "s-": 0.1
}

# Copy enclosure-rim-bezel BC to other rim bezel boundaries
bc.copy(
    from_="enclosure-rim-bezel",
    to=[
        "enclosure-rim-bezel-shadow",
        "holder-rim-bezel",
        "holder-rim-bezel-shadow",
        "housing-rim-bezel",
        "housing-rim-bezel-shadow",
    ],
)

# --- Set up enclosure:1 (domain boundaries) BC ---
enc1_bc = WallBoundary.get(solver, name="enclosure:1")
enc1_bc.thermal.thermal_condition = "Temperature"
enc1_bc.thermal.temperature.value = 298.15 * K

# --- Set up radiation input BC ---
rad_input_bc = WallBoundary.get(solver, name="rad-input")
rad_input_bc.thermal.thermal_condition = "Temperature"
rad_input_bc.thermal.temperature.value = 298.15 * K
rad_input_bc.radiation.boundary_source = True
rad_input_bc.radiation.direct_irradiation_settings.direct_irradiation[
    "Full-spectrum"
] = 1200 * W / m**2
rad_input_bc.radiation.direct_irradiation_settings.beam_direction = (
    -0.848,
    0,
    -0.53,
)

###########################################################################################################
# Set convergence criteria
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Enable residual plots and set the convergence criteria to 'none'.

Solution(solver).monitor.residual.options.criterion_type = "none"

###########################################################################################################
# Define surface reports
# ~~~~~~~~~~~~~~~~~~~~~~
# Define a surface report to find the maximum temperature of the inner bezel,
# then print the state of the report object.

report_defs = ReportDefinitions(solver)
max_temp_surf_report = report_defs.surface.create(
    "max-temp",
    surface_names=["enclosure-inner-bezel"],
    report_type="surface-facetmax",
    field=VariableCatalog.TEMPERATURE,
)

monitor = Monitor(solver)
max_temp_surf_report_plot = ReportPlot.create(name="max-temp-rplot", report_defs = [max_temp_surf_report], print = True)

max_temp_rplot = ReportPlot.create(name="max-temp-rplot", report_defs = [max_temp_surf_report], print = True)

###############################################################################
# Save case file
# ~~~~~~~~~~~~~~
# Save the case file (``headlamp.cas.h5``).

write_case(solver, file_name="headlamp.cas.h5")

###############################################################################
# Initialize flow field
# ~~~~~~~~~~~~~~~~~~~~~
# Initialize the solution.

initialize(solver)

###############################################################################
# Solve for 19 iterations
# ~~~~~~~~~~~~~~~~~~~~~~~
# Solve for 19 iterations. 99 iterations is recommended by the tutorial, but is
# reduced to 19 for this example for demonstration purposes.

iterate(solver, iter_count=19)

###############################################################################
# Write final case file and data
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Enable overwrite so that the original case file will be overwritten. Write
# the final case file and the data.

solver.settings.file.batch_options.confirm_overwrite = True
write_case_data(solver, file_name="headlamp.cas.h5")

###############################################################################
# Close Fluent
# ~~~~~~~~~~~~
# Close Fluent.

solver.exit()

###############################################################################
