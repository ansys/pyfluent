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

""".. _conjugate_heat_transfer:

Conjugate Heat Transfer
-----------------------
"""

#######################################################################################
# Objective
# =====================================================================================
#
# This tutorial demonstrates how to model forced convection in a louvered fin heat
# exchanger. This case solves equations for both Fluid and Solid domain.
# As a result, temperature field evolved together.
#
# This tutorial demonstrates how to perform the following tasks:
#
# * Calculate the fin heat transfer rate.
# * Use periodic boundaries to reduce the size of the computational domain.
# * Use a convective thermal boundary condition to represent heat transfer.
# * Examine and understand the relationship between flow and temperature.

# sphinx_gallery_thumbnail_path = '_static/cht_xy_pressure.png'

###################################
# Import required libraries/modules
# =================================

import csv
import os
from pathlib import Path
import platform

import matplotlib.pyplot as plt
import pyvista as pv

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.visualization import (
    Contour,
    GraphicsWindow,
    Mesh,
    Vector,
    XYPlot,
)

filenames = {
    "Windows": "cht_fin_htc_new.scdoc",
    "Other": "cht_fin_htc_new.scdoc.pmdb",
}

geom_filename = examples.download_file(
    filenames.get(platform.system(), filenames["Other"]),
    "pyfluent/examples/CHT",
    save_path=os.getcwd(),
)

#######################
# Fluent Solution Setup
# =====================

##################################################################
# Launch Fluent session with meshing mode and print Fluent version
# ================================================================

meshing_session = pyfluent.launch_fluent(
    mode="meshing",
    dimension=3,
    precision="double",
    processor_count=4,
)
print(meshing_session.get_fluent_version())

#############################################################################
# Start Watertight Geometry Meshing Workflow
# ==========================================

meshing_session.workflow.InitializeWorkflow(WorkflowType=r"Watertight Geometry")

meshing_session.workflow.TaskObject["Import Geometry"].Arguments = dict(
    FileName=geom_filename
)

meshing_session.workflow.TaskObject["Import Geometry"].Execute()

meshing_session.workflow.TaskObject["Add Local Sizing"].Execute()

meshing_session.workflow.TaskObject["Generate the Surface Mesh"].Arguments = dict(
    {
        "CFDSurfaceMeshControls": {
            "MinSize": 0.3,
            "MaxSize": 1,
            "ScopeProximityTo": "faces",
        },
    }
)
meshing_session.workflow.TaskObject["Generate the Surface Mesh"].Execute()

meshing_session.workflow.TaskObject["Describe Geometry"].UpdateChildTasks(
    SetupTypeChanged=True
)
meshing_session.workflow.TaskObject["Describe Geometry"].Arguments.setState(
    {
        r"CappingRequired": r"No",
        r"InvokeShareTopology": r"No",
        r"NonConformal": r"Yes",
        r"SetupType": r"The geometry consists of both fluid and solid regions and/or voids",
    }
)

meshing_session.workflow.TaskObject["Describe Geometry"].Execute()

#############################################################################
# Update Interface Boundaries; Create Region
# ==========================================

meshing_session.workflow.TaskObject["Update Boundaries"].Arguments.setState(
    {
        r"BoundaryLabelList": [
            r"interface-out-solid-a",
            r"interface-out-high-a",
            r"interface-out-low-a",
            r"interface-4-solid-sweep",
            r"interface-4-high-sweep",
            r"interface-4-low-sweep",
            r"interface-3-solid-sweep",
            r"interface-3-high-sweep",
            r"interface-3-low-sweep",
            r"interface-2-solid-sweep",
            r"interface-2-high-sweep",
            r"interface-2-low-sweep",
            r"interface-1-solid-sweep",
            r"interface-1-high-sweep",
            r"interface-1-low-sweep",
            r"interface-solid-in-a",
            r"interface-in-high-a",
            r"interface-in-low-a",
            r"interface-tube-2-solid-a",
            r"interface-tube-2-high-a",
            r"interface-tube-2-low-a",
            r"interface-tube-1-solid-a",
            r"interface-tube-1-high-a",
            r"interface-tube-1-low-a",
            r"interface-4-fluid-high-tet",
            r"interface-4-fluid-low-tet",
            r"interface-3-fluid-low-tet",
            r"interface-3-fluid-high-tet",
            r"interface-2-fluid-high-tet",
            r"interface-2-fluid-low-tet",
            r"interface-1-fluid-high-tet",
            r"interface-1-fluid-low-tet",
            r"interface-1-solid-tet-4",
            r"interface-1-solid-tet-3",
            r"interface-1-solid-tet-2",
            r"interface-1-solid-tet-1",
        ],
        r"BoundaryLabelTypeList": [
            r"interface",
            r"interface",
            r"interface",
            r"interface",
            r"interface",
            r"interface",
            r"interface",
            r"interface",
            r"interface",
            r"interface",
            r"interface",
            r"interface",
            r"interface",
            r"interface",
            r"interface",
            r"interface",
            r"interface",
            r"interface",
            r"interface",
            r"interface",
            r"interface",
            r"interface",
            r"interface",
            r"interface",
            r"interface",
            r"interface",
            r"interface",
            r"interface",
            r"interface",
            r"interface",
            r"interface",
            r"interface",
            r"interface",
            r"interface",
            r"interface",
            r"interface",
        ],
        r"OldBoundaryLabelList": [
            r"interface-out-solid-a",
            r"interface-out-high-a",
            r"interface-out-low-a",
            r"interface-4-solid-sweep",
            r"interface-4-high-sweep",
            r"interface-4-low-sweep",
            r"interface-3-solid-sweep",
            r"interface-3-high-sweep",
            r"interface-3-low-sweep",
            r"interface-2-solid-sweep",
            r"interface-2-high-sweep",
            r"interface-2-low-sweep",
            r"interface-1-solid-sweep",
            r"interface-1-high-sweep",
            r"interface-1-low-sweep",
            r"interface-solid-in-a",
            r"interface-in-high-a",
            r"interface-in-low-a",
            r"interface-tube-2-solid-a",
            r"interface-tube-2-high-a",
            r"interface-tube-2-low-a",
            r"interface-tube-1-solid-a",
            r"interface-tube-1-high-a",
            r"interface-tube-1-low-a",
            r"interface-4-fluid-high-tet",
            r"interface-4-fluid-low-tet",
            r"interface-3-fluid-low-tet",
            r"interface-3-fluid-high-tet",
            r"interface-2-fluid-high-tet",
            r"interface-2-fluid-low-tet",
            r"interface-1-fluid-high-tet",
            r"interface-1-fluid-low-tet",
            r"interface-1-solid-tet-4",
            r"interface-1-solid-tet-3",
            r"interface-1-solid-tet-2",
            r"interface-1-solid-tet-1",
        ],
        r"OldBoundaryLabelTypeList": [
            r"wall",
            r"wall",
            r"wall",
            r"wall",
            r"wall",
            r"wall",
            r"wall",
            r"wall",
            r"wall",
            r"wall",
            r"wall",
            r"wall",
            r"wall",
            r"wall",
            r"wall",
            r"wall",
            r"wall",
            r"wall",
            r"wall",
            r"wall",
            r"wall",
            r"wall",
            r"wall",
            r"wall",
            r"wall",
            r"wall",
            r"wall",
            r"wall",
            r"wall",
            r"wall",
            r"wall",
            r"wall",
            r"wall",
            r"wall",
            r"wall",
            r"wall",
        ],
        r"OldLabelZoneList": [
            r"interface-out-solid-a",
            r"interface-out-high-a",
            r"interface-out-low-a",
            r"interface-4-solid-sweep",
            r"interface-4-high-sweep",
            r"interface-4-low-sweep",
            r"interface-3-solid-sweep",
            r"interface-3-high-sweep",
            r"interface-3-low-sweep",
            r"interface-2-solid-sweep",
            r"interface-2-high-sweep",
            r"interface-2-low-sweep",
            r"interface-1-solid-sweep",
            r"interface-1-high-sweep",
            r"interface-1-low-sweep",
            r"interface-solid-in-a",
            r"interface-in-high-a",
            r"interface-in-low-a",
            r"interface-tube-2-solid-a.2",
            r"interface-tube-2-solid-a.1",
            r"interface-tube-2-solid-a",
            r"interface-tube-2-high-a.2",
            r"interface-tube-2-high-a.1",
            r"interface-tube-2-high-a",
            r"interface-tube-2-low-a.2",
            r"interface-tube-2-low-a.1",
            r"interface-tube-2-low-a",
            r"interface-tube-1-solid-a.2",
            r"interface-tube-1-solid-a.1",
            r"interface-tube-1-solid-a",
            r"interface-tube-1-high-a.2",
            r"interface-tube-1-high-a.1",
            r"interface-tube-1-high-a",
            r"interface-tube-1-low-a.2",
            r"interface-tube-1-low-a.1",
            r"interface-tube-1-low-a",
            r"interface-4-fluid-high-tet",
            r"interface-4-fluid-low-tet",
            r"interface-3-fluid-low-tet",
            r"interface-3-fluid-high-tet",
            r"interface-2-fluid-high-tet",
            r"interface-2-fluid-low-tet",
            r"interface-1-fluid-high-tet",
            r"interface-1-fluid-low-tet",
            r"interface-1-solid-tet-4",
            r"interface-1-solid-tet-3",
            r"interface-1-solid-tet-2",
            r"interface-1-solid-tet-1",
        ],
    }
)

meshing_session.workflow.TaskObject["Update Boundaries"].Execute()

meshing_session.workflow.TaskObject["Create Regions"].Execute()

#############################################################################
# Custom Journal for Creating Periodicity due to Non-Conformal Objects
# ====================================================================

meshing_session.workflow.TaskObject["Describe Geometry"].InsertNextTask(
    CommandName=r"RunCustomJournal"
)
meshing_session.workflow.TaskObject["Run Custom Journal"].Rename(
    NewName=r"set-periodicity"
)
meshing_session.workflow.TaskObject["set-periodicity"].Arguments = dict(
    {
        r"JournalString": r"""/bo rps translational semi-auto periodic-1-high periodic-2-high periodic-3-high periodic-4-high , 0 0 -2.3
/bo rps translational semi-auto periodic-5* , 0 0 -2.3
/bo rps translational semi-auto periodic-6-high , 0 0 -2.3
/bo rps translational semi-auto periodic-7-high , 0 0 -2.3
""",
    }
)

meshing_session.workflow.TaskObject["set-periodicity"].Execute()

#############################################################################
# Update Boundary Layer Task
# ==========================

meshing_session.workflow.TaskObject["Update Regions"].Execute()
meshing_session.workflow.TaskObject["Add Boundary Layers"].AddChildToTask()
meshing_session.workflow.TaskObject["Add Boundary Layers"].InsertCompoundChildTask()
meshing_session.workflow.TaskObject["smooth-transition_1"].Rename(
    NewName=r"aspect-ratio_1"
)

meshing_session.workflow.TaskObject["aspect-ratio_1"].Arguments.setState(
    {
        "BLControlName": r"aspect-ratio_1",
        "BLRegionList": [
            r"fluid-tet-4",
            r"fluid-tet-3",
            r"fluid-tet-2",
            r"fluid-tet-1",
            r"fluid-sweep-fin2",
            r"fluid-sweep-fin1",
            r"fluid-sweep-fin5",
            r"fluid-sweep-fin3",
            r"fluid-sweep-fin6",
            r"fluid-sweep-fin4",
            r"fluid-in",
            r"fluid-out",
        ],
        r"BLZoneList": [
            r"wall-fluid-tet-4-solid-tet-4",
            r"wall-fluid-tet-3-solid-tet-3",
            r"wall-fluid-tet-2-solid-tet-2",
            r"wall-fluid-tet-2-solid-tet-2-wall-fluid-tet-3-solid-tet-3-fluid-tet-2-solid-tet-2",
            r"wall-fluid-tet-1-solid-tet-1",
            r"wall-fluid-sweep-fin-solid-sweep-fin.1",
            r"wall-fluid-sweep-fin-solid-sweep-fin",
            r"wall-fluid-sweep-fin-solid-sweep-fin.5",
            r"wall-fluid-sweep-fin-solid-sweep-fin.4",
            r"wall-fluid-sweep-fin-solid-sweep-fin.3",
            r"wall-fluid-sweep-fin-solid-sweep-fin.2",
        ],
        r"BlLabelList": r"wall*",
        r"CompleteBlLabelList": [
            r"wall-fluid-sweep-fin-solid-sweep-fin",
            r"wall-fluid-tet-1-solid-tet-1",
            r"wall-fluid-tet-2-solid-tet-2",
            r"wall-fluid-tet-3-solid-tet-3",
            r"wall-fluid-tet-4-solid-tet-4",
        ],
        r"FaceScope": {
            r"GrowOn": r"selected-labels",
        },
        r"OffsetMethodType": r"aspect-ratio",
    }
)

meshing_session.workflow.TaskObject["aspect-ratio_1"].Execute()

#############################################################################
# Generate Mesh
# =============

meshing_session.workflow.TaskObject["Generate the Volume Mesh"].Execute()

#############################################################################
# Improve Volume Mesh
# ===================

meshing_session.workflow.TaskObject["Generate the Volume Mesh"].InsertNextTask(
    CommandName=r"ImproveVolumeMesh"
)

meshing_session.workflow.TaskObject["Improve Volume Mesh"].Arguments.setState(
    {
        r"CellQualityLimit": 0.05,
        r"VMImprovePreferences": {
            r"ShowVMImprovePreferences": False,
            r"VIQualityIterations": 5,
            r"VIQualityMinAngle": 0,
            r"VIgnoreFeature": r"yes",
        },
    }
)

meshing_session.workflow.TaskObject["Improve Volume Mesh"].Execute()

#############################################################################
# Save Mesh File
# ==============

save_mesh_as = str(Path(pyfluent.EXAMPLES_PATH) / "hx-fin-2mm.msh.h5")
meshing_session.tui.file.write_mesh(save_mesh_as)

#############################################################################
# Switch to Solution Mode
# =======================

solver_session = meshing_session.switch_to_solver()

#############################################################################
# Auto-create Mesh Interfaces
# ===========================

solver_session.tui.define.mesh_interfaces.create("int", "yes", "no")

#############################################################################
# Mesh Check; Review Fluent transcript for errors
# ===============================================

solver_session.mesh.check()

#############################################################################
# Create a few boundary list for display and post-processing
# ==========================================================

mesh1 = Mesh(solver=solver_session)

wall_list = []
periodic_list = []
symmetry_list = []

for item in mesh1.surfaces.allowed_values:
    if len(item.split("wall")) > 1:
        wall_list.append(item)
    if len(item.split("periodic")) > 1:
        periodic_list.append(item)
    if len(item.split("symmetry")) > 1:
        symmetry_list.append(item)

#############################################################################
# Display Mesh
# ============

mesh1.show_edges = True
mesh1.surfaces = wall_list

window1 = GraphicsWindow()
window1.add_graphics(mesh1)
window1.show()
p = window1.renderer
p.view_isometric()
p.add_axes()
p.add_floor(offset=1, show_edges=False)
light = pv.Light(light_type="headlight")
p.add_light(light)

###############################################################################
# Temperature, Energy, Laminar Viscous Model
# ==========================================
# * Set Temperature Unit
# * Enable Energy Equation
# * Enable Laminar Viscous Model

solver_session.setup.general.units.set_units(
    quantity="temperature", units_name="C", scale_factor=1.0, offset=273.15
)
solver_session.setup.models.energy.enabled = True
solver_session.setup.models.viscous.model.set_state("laminar")

#############################################################################
# Change a few material properties of default Air
# ===============================================

air_dict = solver_session.setup.materials.fluid["air"].get_state()
air_dict["density"]["value"] = 1.2
air_dict["viscosity"]["value"] = 1.5e-5
air_dict["thermal_conductivity"]["value"] = 0.026
air_dict["specific_heat"]["value"] = 1006.0
solver_session.setup.materials.fluid["air"].set_state(air_dict)

#############################################################################
# Change a few material properties of default Aluminum
# ====================================================

al_dict = solver_session.setup.materials.solid["aluminum"].get_state()
al_dict["density"]["value"] = 2719.0
al_dict["thermal_conductivity"]["value"] = 200.0
al_dict["specific_heat"]["value"] = 871.0
solver_session.setup.materials.solid["aluminum"].set_state(al_dict)

#############################################################################
# Copy Copper and change a few material properties of default Copper
# ==================================================================

solver_session.setup.materials.database.copy_by_name(type="solid", name="copper")
cu_dict = solver_session.setup.materials.solid["copper"].get_state()
cu_dict["density"]["value"] = 8978.0
cu_dict["thermal_conductivity"]["value"] = 340.0
cu_dict["specific_heat"]["value"] = 381.0
solver_session.setup.materials.solid["copper"].set_state(cu_dict)

#############################################################################
# Set Tube Cell Zone Material as Copper
# =====================================

tube_dict = solver_session.setup.cell_zone_conditions.solid["solid-tube-1"].get_state()
tube_dict["material"] = "copper"
solver_session.setup.cell_zone_conditions.solid["solid-tube-1"].set_state(tube_dict)

tube_dict = solver_session.setup.cell_zone_conditions.solid["solid-tube-2"].get_state()
tube_dict["material"] = "copper"
solver_session.setup.cell_zone_conditions.solid["solid-tube-2"].set_state(tube_dict)

#############################################################################
# Set Boundary Condition for Inlet and Outlet
# ===========================================

solver_session.setup.boundary_conditions.velocity_inlet["inlet"].momentum.velocity = 4.0
solver_session.setup.boundary_conditions.velocity_inlet["inlet"].thermal.temperature = (
    293.15  # Need to specify in Kelvin
)

solver_session.setup.boundary_conditions.pressure_outlet[
    "outlet"
].thermal.backflow_total_temperature = 293.15

#############################################################################
# Set Thermal Boundary Condition for Wall Inner Tube
# ==================================================

solver_session.setup.boundary_conditions.wall[
    "wall-inner-tube-1"
].thermal.thermal_condition = "Convection"
solver_session.setup.boundary_conditions.wall[
    "wall-inner-tube-1"
].thermal.heat_transfer_coeff = 1050.0
solver_session.setup.boundary_conditions.wall[
    "wall-inner-tube-1"
].thermal.free_stream_temp = 353.15

solver_session.setup.boundary_conditions.copy(
    from_="wall-inner-tube-1", to="wall-inner-tube-2"
)

#############################################################################
# Enable HOTR
# ===========

solver_session.solution.methods.high_order_term_relaxation.enable = True

#############################################################################
# Define Report Definitions
# =========================

solver_session.solution.report_definitions.surface["outlet-enthalpy-flow"] = {}
solver_session.solution.report_definitions.surface[
    "outlet-enthalpy-flow"
].report_type = "surface-flowrate"
solver_session.solution.report_definitions.surface["outlet-enthalpy-flow"].field = (
    "enthalpy"
)
solver_session.solution.report_definitions.surface[
    "outlet-enthalpy-flow"
].surface_names = ["outlet"]

solver_session.solution.report_definitions.surface["avg-pressure-inlet"] = {}
solver_session.solution.report_definitions.surface["avg-pressure-inlet"].report_type = (
    "surface-areaavg"
)
solver_session.solution.report_definitions.surface["avg-pressure-inlet"].field = (
    "pressure"
)
solver_session.solution.report_definitions.surface[
    "avg-pressure-inlet"
].surface_names = ["inlet"]

solver_session.solution.report_definitions.volume["max-vel-louvers4"] = {}
solver_session.solution.report_definitions.volume["max-vel-louvers4"].report_type = (
    "volume-max"
)
solver_session.solution.report_definitions.volume["max-vel-louvers4"].field = (
    "velocity-magnitude"
)
solver_session.solution.report_definitions.volume["max-vel-louvers4"].cell_zones = [
    "fluid-tet-4"
]

solver_session.solution.report_definitions.surface["wall-shear-int"] = {}
solver_session.solution.report_definitions.surface["wall-shear-int"].report_type = (
    "surface-integral"
)
solver_session.solution.report_definitions.surface["wall-shear-int"].field = (
    "wall-shear"
)
solver_session.solution.report_definitions.surface["wall-shear-int"].surface_names = [
    "wall-fluid-sweep-fin-solid-sweep-fin-shadow",
    "wall-fluid-tet-1-solid-tet-1",
    "wall-fluid-tet-2-solid-tet-2",
    "wall-fluid-tet-3-solid-tet-3",
    "wall-fluid-tet-4-solid-tet-4",
]

solver_session.solution.monitor.report_plots.create(name="outlet-enthalpy-flow-plot")
solver_session.solution.monitor.report_plots[
    "outlet-enthalpy-flow-plot"
].report_defs = "outlet-enthalpy-flow"

solver_session.solution.monitor.report_files["outlet-enthalpy-flow-file"] = {}
solver_session.solution.monitor.report_files["outlet-enthalpy-flow-file"] = {
    "report_defs": ["outlet-enthalpy-flow"],
    "file_name": r"outlet-enthalpy-flow.out",
}

solver_session.solution.monitor.report_plots["avg-pressure-inlet-plot"] = {}
solver_session.solution.monitor.report_plots["avg-pressure-inlet-plot"] = {
    "report_defs": ["avg-pressure-inlet"]
}

solver_session.solution.monitor.report_files["avg-pressure-inlet-file"] = {}
solver_session.solution.monitor.report_files["avg-pressure-inlet-file"] = {
    "report_defs": ["avg-pressure-inlet"],
    "file_name": r"avg-pressure-inlet.out",
}

solver_session.solution.monitor.report_plots["max-vel-louvers4-plot"] = {}
solver_session.solution.monitor.report_plots["max-vel-louvers4-plot"] = {
    "report_defs": ["max-vel-louvers4"]
}

solver_session.solution.monitor.report_files["max-vel-louvers4-file"] = {}
solver_session.solution.monitor.report_files["max-vel-louvers4-file"] = {
    "report_defs": ["max-vel-louvers4"],
    "file_name": r"max-vel-louvers4.out",
}

solver_session.solution.monitor.report_plots["wall-shear-int-plot"] = {}
solver_session.solution.monitor.report_plots["wall-shear-int-plot"] = {
    "report_defs": ["wall-shear-int"]
}

solver_session.solution.monitor.report_files["wall-shear-int-file"] = {}
solver_session.solution.monitor.report_files["wall-shear-int-file"] = {
    "report_defs": ["wall-shear-int"],
    "file_name": r"wall-shear-int.out",
}

#############################################################################
# Hybrid Initialization; Slit Interior between Solid Zones; Save Case
# ===================================================================

solver_session.solution.initialization.initialization_type = "hybrid"
solver_session.solution.initialization.hybrid_initialize()

solver_session.setup.boundary_conditions.slit_interior_between_diff_solids()
solver_session.file.write(file_type="case", file_name="hx-fin-2mm.cas.h5")

#############################################################################
# Set Aggressive Length Scale Method; Run Calculation & Save Data
# ===============================================================

solver_session.solution.run_calculation.pseudo_time_settings.time_step_method.time_step_method = (
    "automatic"
)
solver_session.solution.run_calculation.pseudo_time_settings.time_step_method.length_scale_methods = (
    "aggressive"
)

solver_session.solution.run_calculation.iterate(iter_count=250)

solver_session.file.write(file_type="case-data", file_name="hx-fin-2mm.dat.h5")

#############################################################################
# Post-Processing Mass Balance Report
# ===================================

inlet_mfr = solver_session.scheme.exec(
    ('(ti-menu-load-string "/report/fluxes/mass-flow no inlet () no")',)
).split(" ")[-1]
outlet_mfr = solver_session.scheme.exec(
    ('(ti-menu-load-string "/report/fluxes/mass-flow no outlet () no")',)
).split(" ")[-1]
net_mfr = solver_session.scheme.exec(
    ('(ti-menu-load-string "/report/fluxes/mass-flow no inlet outlet () no")',)
).split(" ")[-1]
print("Mass Balance Report\n")
print("Inlet (kg/s): ", inlet_mfr)
print("Outlet (kg/s): ", outlet_mfr)
print("Net (kg/s): ", net_mfr)

#############################################################################
# Heat Balance Report
# ===================

htr = solver_session.scheme.exec(
    ('(ti-menu-load-string "/report/fluxes/heat-transfer yes no")',)
).split(" ")[-1]
print("Heat Balance Report\n")
print("Net Imbalance (Watt): ", htr)

#############################################################################
# Plot Monitors
# =============

fig, axs = plt.subplots(2, 2, figsize=(10, 8))
fig.suptitle("Monitor Plots")

outFilesList = []
fileList = os.listdir(os.getcwd())
for tempFile in fileList:
    fName, ext = os.path.splitext(tempFile)
    if ext == ".out":
        outFilesList.append(tempFile)
outFilesList.sort()

index = 0
for ax in axs.flat:
    X = []
    Y = []
    i = -1
    with open(outFilesList[index], "r") as datafile:
        plotting = csv.reader(datafile, delimiter=" ")
        for rows in plotting:
            i += 1
            if i == 1:
                var = rows[1]
            if i > 2:
                X.append(int(rows[0]))
                Y.append(float(rows[1]))

    ax.plot(X, Y)
    ax.set(xlabel="Iteration", ylabel=var, title=var)
    index += 1

plt.tight_layout()

#############################################################################
# Show graph
# ==========

plt.show()

# %%
# .. image:: ../../_static/cht_avg_pressure.png
#    :align: center
#    :alt: Average Pressure

# %%
#    Average Pressure

#############################################################################
# Contour Plot
# ============

contour1 = Contour(solver=solver_session, field="temperature", surfaces=wall_list)
window2 = GraphicsWindow()
window2.add_graphics(contour1)
window2.show()

p = window2.renderer
p.view_isometric()
p.add_axes()
p.add_floor(offset=1, show_edges=False)
# known vtk issue in rendering the below
# p.add_text(
#     "Contour of Temperature on Walls", font="courier", color="grey", font_size=10
# )
light = pv.Light(light_type="headlight")
p.add_light(light)

p.scalar_bar.SetVisibility(False)
p.add_scalar_bar(
    "Temperature [K]",
    interactive=True,
    vertical=False,
    title_font_size=20,
    label_font_size=15,
    outline=False,
    position_x=0.5,
    fmt="%10.1f",
)

#############################################################################
# Create Iso-Surface of X=0.012826 m
# ==================================

solver_session.results.surfaces.iso_surface["x=0.012826"] = {}
solver_session.results.surfaces.iso_surface["x=0.012826"].field = "x-coordinate"
solver_session.results.surfaces.iso_surface["x=0.012826"] = {"iso_values": [0.012826]}

#############################################################################
# Vecotor Plot
# ============

vector1 = Vector(solver=solver_session, surfaces=["x=0.012826"], scale=2.0, skip=5)
window3 = GraphicsWindow()
window3.add_graphics(vector1)
window3.show()

p = window3.renderer
p.view_isometric()
p.add_axes()
# known vtk issues in rendering the below
# p.add_floor( offset=1, show_edges=False)
# p.add_text("Vector Plot", font="courier", color="grey", font_size=10)
light = pv.Light(light_type="headlight")
p.add_light(light)

p.scalar_bar.SetVisibility(False)
p.add_scalar_bar(
    "Velocity [m/s]",
    interactive=True,
    vertical=False,
    title_font_size=20,
    label_font_size=15,
    outline=False,
    position_x=0.5,
    fmt="%10.1f",
)

#############################################################################
# XY Plot of Pressure
# ===================

p1 = XYPlot(
    solver=solver_session,
    surfaces=["x=0.012826"],
    y_axis_function="pressure",
    x_axis_function="direction-vector",
    direction_vector=[0, 1, 0],
)

#############################################################################
# Show graph
# ==========

plot_window = GraphicsWindow()
plot_window.add_plot(p1)
plot_window.show()

# %%
# .. image:: ../../_static/cht_xy_pressure.png
#    :align: center
#    :alt: XY Plot of Pressure

# %%
#    XY Plot of Pressure

#############################################################################
# Exit Fluent Session
# ===================
solver_session.exit()
