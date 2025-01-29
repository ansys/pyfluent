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

import matplotlib.pyplot as plt
import pyvista as pv

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.visualization.matplotlib import Plots
from ansys.fluent.visualization.pyvista import Graphics, pyvista_windows_manager
from ansys.fluent.visualization.pyvista.pyvista_windows_manager import PyVistaWindow

###########################################################################
# Specifying save path
# ====================
# * save_path can be specified as Path("E:/", "pyfluent-examples-tests") or
# * Path("E:/pyfluent-examples-tests") in a Windows machine for example,  or
# * Path("~/pyfluent-examples-tests") in Linux.
save_path = Path(pyfluent.EXAMPLES_PATH)

geom_filename = examples.download_file(
    "cht_fin_htc_new.scdoc",
    "pyfluent/examples/CHT",
    save_path=save_path,
)

#######################
# Fluent Solution Setup
# =====================

##################################################################
# Launch Fluent session with meshing mode and print Fluent version
# ================================================================

meshing = pyfluent.launch_fluent(
    product_version="25.1.0",
    mode="meshing",
    dimension=3,
    precision="double",
    processor_count=4,
)
print(meshing.get_fluent_version())

#############################################################################
# Start Watertight Geometry Meshing Workflow
# ==========================================

meshing.workflow.InitializeWorkflow(WorkflowType=r"Watertight Geometry")

meshing.workflow.TaskObject["Import Geometry"].Arguments = dict(FileName=geom_filename)

meshing.workflow.TaskObject["Import Geometry"].Execute()

meshing.workflow.TaskObject["Add Local Sizing"].Execute()

meshing.workflow.TaskObject["Generate the Surface Mesh"].Arguments = dict(
    {
        "CFDSurfaceMeshControls": {
            "MinSize": 0.3,
            "MaxSize": 1,
            "ScopeProximityTo": "faces",
        },
    }
)
meshing.workflow.TaskObject["Generate the Surface Mesh"].Execute()

meshing.workflow.TaskObject["Describe Geometry"].UpdateChildTasks(SetupTypeChanged=True)
meshing.workflow.TaskObject["Describe Geometry"].Arguments.setState(
    {
        r"CappingRequired": r"No",
        r"InvokeShareTopology": r"No",
        r"NonConformal": r"Yes",
        r"SetupType": r"The geometry consists of both fluid and solid regions and/or voids",
    }
)

meshing.workflow.TaskObject["Describe Geometry"].Execute()

#############################################################################
# Update Interface Boundaries; Create Region
# ==========================================

meshing.workflow.TaskObject["Update Boundaries"].Arguments.setState(
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

meshing.workflow.TaskObject["Update Boundaries"].Execute()

meshing.workflow.TaskObject["Create Regions"].Execute()

#############################################################################
# Custom Journal for Creating Periodicity due to Non-Conformal Objects
# ====================================================================

meshing.workflow.TaskObject["Describe Geometry"].InsertNextTask(
    CommandName=r"RunCustomJournal"
)
meshing.workflow.TaskObject["Run Custom Journal"].Rename(NewName=r"set-periodicity")
meshing.workflow.TaskObject["set-periodicity"].Arguments = dict(
    {
        r"JournalString": r"""/bo rps translational semi-auto periodic-1-high periodic-2-high periodic-3-high periodic-4-high , 0 0 -2.3
/bo rps translational semi-auto periodic-5* , 0 0 -2.3
/bo rps translational semi-auto periodic-6-high , 0 0 -2.3
/bo rps translational semi-auto periodic-7-high , 0 0 -2.3
""",
    }
)

meshing.workflow.TaskObject["set-periodicity"].Execute()

#############################################################################
# Update Boundary Layer Task
# ==========================

meshing.workflow.TaskObject["Update Regions"].Execute()
meshing.workflow.TaskObject["Add Boundary Layers"].AddChildToTask()
meshing.workflow.TaskObject["Add Boundary Layers"].InsertCompoundChildTask()
meshing.workflow.TaskObject["smooth-transition_1"].Rename(NewName=r"aspect-ratio_1")

meshing.workflow.TaskObject["aspect-ratio_1"].Arguments.setState(
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

meshing.workflow.TaskObject["aspect-ratio_1"].Execute()

#############################################################################
# Generate Mesh
# =============

meshing.workflow.TaskObject["Generate the Volume Mesh"].Execute()

#############################################################################
# Improve Volume Mesh
# ===================

meshing.workflow.TaskObject["Generate the Volume Mesh"].InsertNextTask(
    CommandName=r"ImproveVolumeMesh"
)

meshing.workflow.TaskObject["Improve Volume Mesh"].Arguments.setState(
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

meshing.workflow.TaskObject["Improve Volume Mesh"].Execute()

#############################################################################
# Save Mesh File
# ==============

save_mesh_as = str(Path(pyfluent.EXAMPLES_PATH) / "hx-fin-2mm.msh.h5")
meshing.tui.file.write_mesh(save_mesh_as)

#############################################################################
# Switch to Solution Mode
# =======================

solver = meshing.switch_to_solver()

#############################################################################
# Auto-create Mesh Interfaces
# ===========================

solver.tui.define.mesh_interfaces.create("int", "yes", "no")

#############################################################################
# Mesh Check; Review Fluent transcript for errors
# ===============================================

solver.mesh.check()

#############################################################################
# Create a few boundary list for display and post-processing
# ==========================================================

graphics_session1 = Graphics(solver)
mesh1 = graphics_session1.Meshes["mesh-1"]

wall_list = []
periodic_list = []
symmetry_list = []

for item in mesh1.surfaces_list.allowed_values:
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
mesh1.surfaces_list = wall_list
mesh1.display("window-1")
p = pyvista_windows_manager.get_plotter("window-1")
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

solver.setup.general.units.set_units(
    quantity="temperature", units_name="c", scale_factor=1.0, offset=0.0
)
solver.setup.models.energy.enabled = True
solver.setup.models.viscous.model.set_state("laminar")

#############################################################################
# Change a few material properties of default Air
# ===============================================

air_dict = solver.setup.materials.fluid["air"].get_state()
air_dict["density"]["value"] = 1.2
air_dict["viscosity"]["value"] = 1.5e-5
air_dict["thermal_conductivity"]["value"] = 0.026
air_dict["specific_heat"]["value"] = 1006.0
solver.setup.materials.fluid["air"].set_state(air_dict)

#############################################################################
# Change a few material properties of default Aluminum
# ====================================================

al_dict = solver.setup.materials.solid["aluminum"].get_state()
al_dict["density"]["value"] = 2719.0
al_dict["thermal_conductivity"]["value"] = 200.0
al_dict["specific_heat"]["value"] = 871.0
solver.setup.materials.solid["aluminum"].set_state(al_dict)

#############################################################################
# Copy Copper and change a few material properties of default Copper
# ==================================================================

solver.setup.materials.database.copy_by_name(type="solid", name="copper")
cu_dict = solver.setup.materials.solid["copper"].get_state()
cu_dict["density"]["value"] = 8978.0
cu_dict["thermal_conductivity"]["value"] = 340.0
cu_dict["specific_heat"]["value"] = 381.0
solver.setup.materials.solid["copper"].set_state(cu_dict)

#############################################################################
# Set Tube Cell Zone Material as Copper
# =====================================

tube_dict = solver.setup.cell_zone_conditions.solid["solid-tube-1"].get_state()
tube_dict["material"] = "copper"
solver.setup.cell_zone_conditions.solid["solid-tube-1"].set_state(tube_dict)

tube_dict = solver.setup.cell_zone_conditions.solid["solid-tube-2"].get_state()
tube_dict["material"] = "copper"
solver.setup.cell_zone_conditions.solid["solid-tube-2"].set_state(tube_dict)

#############################################################################
# Set Boundary Condition for Inlet and Outlet
# ===========================================

solver.setup.boundary_conditions.velocity_inlet["inlet"].momentum.velocity = 4.0
solver.setup.boundary_conditions.velocity_inlet["inlet"].thermal.temperature = (
    293.15  # Need to specify in Kelvin
)

solver.setup.boundary_conditions.pressure_outlet[
    "outlet"
].thermal.backflow_total_temperature = 293.15

#############################################################################
# Set Thermal Boundary Condition for Wall Inner Tube
# ==================================================

solver.setup.boundary_conditions.wall["wall-inner-tube-1"].thermal.thermal_condition = (
    "Convection"
)
solver.setup.boundary_conditions.wall[
    "wall-inner-tube-1"
].thermal.heat_transfer_coeff = 1050.0
solver.setup.boundary_conditions.wall["wall-inner-tube-1"].thermal.free_stream_temp = (
    353.15
)

solver.setup.boundary_conditions.copy(from_="wall-inner-tube-1", to="wall-inner-tube-2")

#############################################################################
# Enable HOTR
# ===========

solver.solution.methods.high_order_term_relaxation.enable = True

#############################################################################
# Define Report Definitions
# =========================

solver.solution.report_definitions.surface["outlet-enthalpy-flow"] = {}
solver.solution.report_definitions.surface["outlet-enthalpy-flow"].report_type = (
    "surface-flowrate"
)
solver.solution.report_definitions.surface["outlet-enthalpy-flow"].field = "enthalpy"
solver.solution.report_definitions.surface["outlet-enthalpy-flow"].surface_names = [
    "outlet"
]

solver.solution.report_definitions.surface["avg-pressure-inlet"] = {}
solver.solution.report_definitions.surface["avg-pressure-inlet"].report_type = (
    "surface-areaavg"
)
solver.solution.report_definitions.surface["avg-pressure-inlet"].field = "pressure"
solver.solution.report_definitions.surface["avg-pressure-inlet"].surface_names = [
    "inlet"
]

solver.solution.report_definitions.volume["max-vel-louvers4"] = {}
solver.solution.report_definitions.volume["max-vel-louvers4"].report_type = "volume-max"
solver.solution.report_definitions.volume["max-vel-louvers4"].field = (
    "velocity-magnitude"
)
solver.solution.report_definitions.volume["max-vel-louvers4"].cell_zones = [
    "fluid-tet-4"
]

solver.solution.report_definitions.surface["wall-shear-int"] = {}
solver.solution.report_definitions.surface["wall-shear-int"].report_type = (
    "surface-integral"
)
solver.solution.report_definitions.surface["wall-shear-int"].field = "wall-shear"
solver.solution.report_definitions.surface["wall-shear-int"].surface_names = [
    "wall-fluid-sweep-fin-solid-sweep-fin-shadow",
    "wall-fluid-tet-1-solid-tet-1",
    "wall-fluid-tet-2-solid-tet-2",
    "wall-fluid-tet-3-solid-tet-3",
    "wall-fluid-tet-4-solid-tet-4",
]

solver.solution.monitor.report_plots.create(name="outlet-enthalpy-flow-plot")
solver.solution.monitor.report_plots["outlet-enthalpy-flow-plot"].report_defs = (
    "outlet-enthalpy-flow"
)

solver.solution.monitor.report_files["outlet-enthalpy-flow-file"] = {}
solver.solution.monitor.report_files["outlet-enthalpy-flow-file"] = {
    "report_defs": ["outlet-enthalpy-flow"],
    "file_name": r"outlet-enthalpy-flow.out",
}

solver.solution.monitor.report_plots["avg-pressure-inlet-plot"] = {}
solver.solution.monitor.report_plots["avg-pressure-inlet-plot"] = {
    "report_defs": ["avg-pressure-inlet"]
}

solver.solution.monitor.report_files["avg-pressure-inlet-file"] = {}
solver.solution.monitor.report_files["avg-pressure-inlet-file"] = {
    "report_defs": ["avg-pressure-inlet"],
    "file_name": r"avg-pressure-inlet.out",
}

solver.solution.monitor.report_plots["max-vel-louvers4-plot"] = {}
solver.solution.monitor.report_plots["max-vel-louvers4-plot"] = {
    "report_defs": ["max-vel-louvers4"]
}

solver.solution.monitor.report_files["max-vel-louvers4-file"] = {}
solver.solution.monitor.report_files["max-vel-louvers4-file"] = {
    "report_defs": ["max-vel-louvers4"],
    "file_name": r"max-vel-louvers4.out",
}

solver.solution.monitor.report_plots["wall-shear-int-plot"] = {}
solver.solution.monitor.report_plots["wall-shear-int-plot"] = {
    "report_defs": ["wall-shear-int"]
}

solver.solution.monitor.report_files["wall-shear-int-file"] = {}
solver.solution.monitor.report_files["wall-shear-int-file"] = {
    "report_defs": ["wall-shear-int"],
    "file_name": r"wall-shear-int.out",
}

#############################################################################
# Hybrid Initialization; Slit Interior between Solid Zones; Save Case
# ===================================================================

solver.solution.initialization.initialization_type = "hybrid"
solver.solution.initialization.hybrid_initialize()

solver.setup.boundary_conditions.slit_interior_between_diff_solids()
save_case_as = str(Path(pyfluent.EXAMPLES_PATH) / "hx-fin-2mm.cas.h5")
solver.file.write(file_type="case", file_name=save_case_as)

#############################################################################
# Set Aggressive Length Scale Method; Run Calculation & Save Data
# ===============================================================

solver.solution.run_calculation.pseudo_time_settings.time_step_method.time_step_method = (
    "automatic"
)
solver.solution.run_calculation.pseudo_time_settings.time_step_method.length_scale_methods = (
    "aggressive"
)

solver.solution.run_calculation.iterate(iter_count=250)

save_case_data_as = str(Path(pyfluent.EXAMPLES_PATH) / "hx-fin-2mm.dat.h5")
solver.file.write(file_type="case-data", file_name=save_case_data_as)

#############################################################################
# Post-Processing Mass Balance Report
# ===================================

inlet_mfr = solver.scheme_eval.exec(
    ('(ti-menu-load-string "/report/fluxes/mass-flow no inlet () no")',)
).split(" ")[-1]
outlet_mfr = solver.scheme_eval.exec(
    ('(ti-menu-load-string "/report/fluxes/mass-flow no outlet () no")',)
).split(" ")[-1]
net_mfr = solver.scheme_eval.exec(
    ('(ti-menu-load-string "/report/fluxes/mass-flow no inlet outlet () no")',)
).split(" ")[-1]
print("Mass Balance Report\n")
print("Inlet (kg/s): ", inlet_mfr)
print("Outlet (kg/s): ", outlet_mfr)
print("Net (kg/s): ", net_mfr)

#############################################################################
# Heat Balance Report
# ===================

htr = solver.scheme_eval.exec(
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

graphics_session1 = Graphics(solver)
contour1 = graphics_session1.Contours["contour-1"]
contour1.field = "temperature"
contour1.surfaces_list = wall_list
contour1.display("window-2")

p = pyvista_windows_manager.get_plotter("window-2")
p.view_isometric()
p.add_axes()
p.add_floor(offset=1, show_edges=False)
p.add_title(
    "Contour of Temperature on Walls", font="courier", color="grey", font_size=10
)
light = pv.Light(light_type="headlight")
p.add_light(light)

p.remove_scalar_bar()
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

solver.results.surfaces.iso_surface["x=0.012826"] = {}
solver.results.surfaces.iso_surface["x=0.012826"].field = "x-coordinate"
solver.results.surfaces.iso_surface["x=0.012826"] = {"iso_values": [0.012826]}

#############################################################################
# Vecotor Plot
# ============

graphics_session1 = Graphics(solver)
vector1 = graphics_session1.Vectors["vector-1"]
vector1.surfaces_list = ["x=0.012826"]
vector1.scale = 2.0
vector1.skip = 5
vector1.display("window-3")

p = pyvista_windows_manager.get_plotter("window-3")
p.view_isometric()
p.add_axes()
# p.add_floor( offset=1, show_edges=False)
p.add_title("Vector Plot", font="courier", color="grey", font_size=10)
light = pv.Light(light_type="headlight")
p.add_light(light)

p.remove_scalar_bar()
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

o = PyVistaWindow(None, None)
o._fetch_mesh(mesh1)
o._display_mesh(mesh1, p)

#############################################################################
# XY Plot of Pressure
# ===================

plots_session1 = Plots(solver)
p1 = plots_session1.XYPlots["p1"]
p1.surfaces_list = ["x=0.012826"]
p1.y_axis_function = "pressure"
p1.x_axis_function = "direction-vector"
p1.direction_vector.set_state([0, 1, 0])

#############################################################################
# Show graph
# ==========

p1.plot("p1")

# %%
# .. image:: ../../_static/cht_xy_pressure.png
#    :align: center
#    :alt: XY Plot of Pressure

# %%
#    XY Plot of Pressure

#############################################################################
# Exit Fluent Session
# ===================
solver.exit()
