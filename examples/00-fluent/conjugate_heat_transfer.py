# /// script
# dependencies = [
#   "ansys-fluent-core",
#   "ansys-fluent-visualization",
#   "matplotlib",
#   "pyvista",
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
from pathlib import Path
import platform

import matplotlib.pyplot as plt
import pyvista as pv

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
import ansys.fluent.core.meshing.meshing_workflow_new as mesh_wf_new
from ansys.fluent.core.solver import (
    BoundaryCondition,
    CellZoneCondition,
    Energy,
    FluidMaterial,
    Fluxes,
    General,
    Initialization,
    IsoSurface,
    Materials,
    MeshInterfaces,
    Monitor,
    PressureOutlet,
    ReportDefinitions,
    RunCalculation,
    SolidMaterial,
    VelocityInlet,
    Viscous,
    WallBoundary,
    write_case,
    write_case_data,
)
from ansys.fluent.visualization import (
    Contour,
    GraphicsWindow,
    Mesh,
    Vector,
    XYPlot,
)
from ansys.units import VariableCatalog
from ansys.units.common import J, K, Pa, W, kg, m, s

filenames = {
    "Windows": "cht_fin_htc_new.scdoc",
    "Other": "cht_fin_htc_new.scdoc.pmdb",
}

geom_filename = examples.download_file(
    filenames.get(platform.system(), filenames["Other"]),
    "pyfluent/examples/CHT",
    save_path=Path.cwd(),
)

#######################
# Fluent Solution Setup
# =====================

##################################################################
# Launch Fluent session with meshing mode and print Fluent version
# ================================================================

meshing = pyfluent.Meshing.from_install(
    precision=pyfluent.Precision.DOUBLE,
    processor_count=4,
)
print(meshing.get_fluent_version())

#############################################################################
# Start Watertight Geometry Meshing Workflow
# ==========================================

workflow: mesh_wf_new.WatertightMeshingWorkflow = meshing.watertight(legacy=False)
meshing.upload(geom_filename)
workflow.application.import_geometry(file_name=geom_filename)

#############################################################################
# Generate the Surface Mesh
# =========================

workflow.application.create_surface_mesh.cfd_surface_mesh_controls(
    min_size=0.3,
    max_size=1,
    scope_proximity_to="faces",
)

#############################################################################
# Describe Geometry
# =================

workflow.application.describe_geometry(
    capping_required=False,
    invoke_share_topology="No",  # Using a string as no enum is currently available
    non_conformal=True,
    setup_type="fluid_solid_voids",
)

#############################################################################
# Update Interface Boundaries; Create Region
# ==========================================

interface_labels = [
    "interface-out-solid-a",
    "interface-out-high-a",
    "interface-out-low-a",
    "interface-4-solid-sweep",
    "interface-4-high-sweep",
    "interface-4-low-sweep",
    "interface-3-solid-sweep",
    "interface-3-high-sweep",
    "interface-3-low-sweep",
    "interface-2-solid-sweep",
    "interface-2-high-sweep",
    "interface-2-low-sweep",
    "interface-1-solid-sweep",
    "interface-1-high-sweep",
    "interface-1-low-sweep",
    "interface-solid-in-a",
    "interface-in-high-a",
    "interface-in-low-a",
    "interface-tube-2-solid-a",
    "interface-tube-2-high-a",
    "interface-tube-2-low-a",
    "interface-tube-1-solid-a",
    "interface-tube-1-high-a",
    "interface-tube-1-low-a",
    "interface-4-fluid-high-tet",
    "interface-4-fluid-low-tet",
    "interface-3-fluid-low-tet",
    "interface-3-fluid-high-tet",
    "interface-2-fluid-high-tet",
    "interface-2-fluid-low-tet",
    "interface-1-fluid-high-tet",
    "interface-1-fluid-low-tet",
    "interface-1-solid-tet-4",
    "interface-1-solid-tet-3",
    "interface-1-solid-tet-2",
    "interface-1-solid-tet-1",
]

workflow.application.update_boundaries(
    boundary_label_list=interface_labels,
    boundary_label_type_list=["interface"] * len(interface_labels),
    old_boundary_label_list=interface_labels,
    old_boundary_label_type_list=["wall"] * len(interface_labels),
    old_label_zone_list=[
        "interface-out-solid-a",
        "interface-out-high-a",
        "interface-out-low-a",
        "interface-4-solid-sweep",
        "interface-4-high-sweep",
        "interface-4-low-sweep",
        "interface-3-solid-sweep",
        "interface-3-high-sweep",
        "interface-3-low-sweep",
        "interface-2-solid-sweep",
        "interface-2-high-sweep",
        "interface-2-low-sweep",
        "interface-1-solid-sweep",
        "interface-1-high-sweep",
        "interface-1-low-sweep",
        "interface-solid-in-a",
        "interface-in-high-a",
        "interface-in-low-a",
        "interface-tube-2-solid-a.2",
        "interface-tube-2-solid-a.1",
        "interface-tube-2-solid-a",
        "interface-tube-2-high-a.2",
        "interface-tube-2-high-a.1",
        "interface-tube-2-high-a",
        "interface-tube-2-low-a.2",
        "interface-tube-2-low-a.1",
        "interface-tube-2-low-a",
        "interface-tube-1-solid-a.2",
        "interface-tube-1-solid-a.1",
        "interface-tube-1-solid-a",
        "interface-tube-1-high-a.2",
        "interface-tube-1-high-a.1",
        "interface-tube-1-high-a",
        "interface-tube-1-low-a.2",
        "interface-tube-1-low-a.1",
        "interface-tube-1-low-a",
        "interface-4-fluid-high-tet",
        "interface-4-fluid-low-tet",
        "interface-3-fluid-low-tet",
        "interface-3-fluid-high-tet",
        "interface-2-fluid-high-tet",
        "interface-2-fluid-low-tet",
        "interface-1-fluid-high-tet",
        "interface-1-fluid-low-tet",
        "interface-1-solid-tet-4",
        "interface-1-solid-tet-3",
        "interface-1-solid-tet-2",
        "interface-1-solid-tet-1",
    ],
)

workflow.application.create_regions()

#############################################################################
# Custom Journal for Creating Periodicity due to Non-Conformal Objects
# ====================================================================

workflow.application.custom_journal_task(
    journal_string=r"""/bo rps translational semi-auto periodic-1-high periodic-2-high periodic-3-high periodic-4-high , 0 0 -2.3
/bo rps translational semi-auto periodic-5* , 0 0 -2.3
/bo rps translational semi-auto periodic-6-high , 0 0 -2.3
/bo rps translational semi-auto periodic-7-high , 0 0 -2.3
""",
)

#############################################################################
# Update Regions; Add Boundary Layers
# ====================================

workflow.application.update_regions()

workflow.application.add_boundary_layers(
    add_child="yes",
    control_name="aspect-ratio_1",
    offset_method_type="aspect-ratio",
    region_scope=[
        "fluid-tet-4",
        "fluid-tet-3",
        "fluid-tet-2",
        "fluid-tet-1",
        "fluid-sweep-fin2",
        "fluid-sweep-fin1",
        "fluid-sweep-fin5",
        "fluid-sweep-fin3",
        "fluid-sweep-fin6",
        "fluid-sweep-fin4",
        "fluid-in",
        "fluid-out",
    ],
    zone_selection_list=[
        "wall-fluid-tet-4-solid-tet-4",
        "wall-fluid-tet-3-solid-tet-3",
        "wall-fluid-tet-2-solid-tet-2",
        "wall-fluid-tet-2-solid-tet-2-wall-fluid-tet-3-solid-tet-3-fluid-tet-2-solid-tet-2",
        "wall-fluid-tet-1-solid-tet-1",
        "wall-fluid-sweep-fin-solid-sweep-fin.1",
        "wall-fluid-sweep-fin-solid-sweep-fin",
        "wall-fluid-sweep-fin-solid-sweep-fin.5",
        "wall-fluid-sweep-fin-solid-sweep-fin.4",
        "wall-fluid-sweep-fin-solid-sweep-fin.3",
        "wall-fluid-sweep-fin-solid-sweep-fin.2",
    ],
    bl_label_list=["wall*"],
    face_scope={"grow_on": "selected-labels"},
    complete_bl_label_list=[
        "wall-fluid-sweep-fin-solid-sweep-fin",
        "wall-fluid-tet-1-solid-tet-1",
        "wall-fluid-tet-2-solid-tet-2",
        "wall-fluid-tet-3-solid-tet-3",
        "wall-fluid-tet-4-solid-tet-4",
    ],
)

#############################################################################
# Generate Mesh
# =============

workflow.application.create_volume_mesh_wtm()

#############################################################################
# Improve Volume Mesh
# ===================

workflow.application.improve_volume_mesh(
    cell_quality_limit=0.05,
    improve_volume_mesh_preferences={
        "show_in_gui": False,
        "iterations": 5,
        "min_angle": 0,
        "smooth_remaining_bad_cells": True,
    },
)

#############################################################################
# Save Mesh File
# ==============

save_mesh_as = str(Path(pyfluent.config.examples_path) / "hx-fin-2mm.msh.h5")
meshing.tui.file.write_mesh(save_mesh_as)

#############################################################################
# Switch to Solution Mode
# =======================

solver = meshing.switch_to_solver()

#############################################################################
# Auto-create Mesh Interfaces
# ===========================

MeshInterfaces(solver).create(si_name="int", all_bnd=True)

#############################################################################
# Mesh Check; Review Fluent transcript for errors
# ===============================================

solver.settings.mesh.check()

#############################################################################
# Create boundary lists for display and post-processing
# =====================================================

mesh1 = Mesh(solver=solver, surfaces=[])

wall_list = [
    boundary_name
    for boundary_name in mesh1.surfaces.allowed_values
    if "wall" in boundary_name
]

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

General(solver).units.set_units(
    quantity="temperature", units_name="C", scale_factor=1.0, offset=273.15
)
Energy(solver).enabled = True
viscous = Viscous(solver)
viscous.model = viscous.model.LAMINAR

#############################################################################
# Change a few material properties of default Air
# ===============================================

# Air
air = FluidMaterial.get(solver, name="air")
air.density = 1.2 * kg / m**3
air.viscosity = 1.5e-5 * Pa * s
air.thermal_conductivity = 0.026 * W / (m * K)
air.specific_heat = 1006.0 * J / (kg * K)

# Aluminum
al = SolidMaterial.create(solver, name="aluminum")
al.density = 2719.0 * kg / m**3
al.thermal_conductivity = 200.0 * W / (m * K)
al.specific_heat = 871.0 * J / (kg * K)

# Copy Copper and set properties
materials = Materials(solver)
materials.database.copy_by_name(type="solid", name="copper")
cu = SolidMaterial.create(solver, name="copper")
cu.density = 8978.0 * kg / m**3
cu.thermal_conductivity = 340.0 * W / (m * K)
cu.specific_heat = 381.0 * J / (kg * K)

# Set Tube Cell Zone Material as Copper
cell_zones = CellZoneCondition(solver, name="solid-tube-*")
cell_zones.general.material = "copper"

# Boundary conditions
inlet = VelocityInlet.get(solver, name="inlet")
inlet.momentum.velocity = 4.0 * m / s
inlet.thermal.temperature = 293.15 * K

outlet = PressureOutlet.get(solver, name="outlet")
outlet.thermal.backflow_total_temperature = 293.15 * K

# Wall thermal BC
walls_inner = WallBoundary.get(solver, name="wall-inner-tube-*")
walls_inner.thermal.thermal_condition = walls_inner.thermal.thermal_condition.CONVECTION
walls_inner.thermal.heat_transfer_coeff = 1050.0 * W / (m**2 * K)
walls_inner.thermal.free_stream_temp = 353.15 * K

# Enable HOTR
solver.settings.solution.methods.high_order_term_relaxation.enable = True

# Define Report Definitions using typed API
rdefs = ReportDefinitions(solver)
out_ent = rdefs.surface.create(
    name="outlet-enthalpy-flow",
    report_type="surface-flowrate",
    field=VariableCatalog.ENTHALPY,
    surface_names=["outlet"],
)

avg_pressure = rdefs.surface.create(
    name="avg-pressure-inlet",
    report_type="surface-areaavg",
    field=VariableCatalog.PRESSURE,
    surface_names=["inlet"],
)

vol_max = rdefs.volume.create(
    name="max-vel-louvers4",
    report_type="volume-max",
    field=VariableCatalog.VELOCITY_MAGNITUDE,
    cell_zones=["fluid-sweep-fin4"],
)


wall_shear = rdefs.surface.create(
    name="wall-shear-int",
    report_type="surface-integral",
    field=VariableCatalog.WALL_SHEAR,
    surface_names=[
        "wall-fluid-sweep-fin-solid-sweep-fin-shadow",
        "wall-fluid-tet-1-solid-tet-1",
        "wall-fluid-tet-2-solid-tet-2",
        "wall-fluid-tet-3-solid-tet-3",
        "wall-fluid-tet-4-solid-tet-4",
    ],
)

monitor = Monitor(solver)
monitor.report_plots.create(report_defs=[out_ent])
monitor.report_files.create(report_defs=[out_ent], file_name="outlet-enthalpy-flow.out")
monitor.report_plots.create(report_defs=[avg_pressure])
monitor.report_files.create(
    report_defs=[avg_pressure], file_name="avg-pressure-inlet.out"
)
monitor.report_plots.create(report_defs=[vol_max])
monitor.report_files.create(report_defs=[vol_max], file_name="max-vel-louvers4.out")
monitor.report_plots.create(report_defs=[wall_shear])
monitor.report_files.create(report_defs=[wall_shear], file_name="wall-shear-int.out")

#############################################################################
# Hybrid Initialization; Slit Interior between Solid Zones; Save Case
# ===================================================================

initialization = Initialization(solver)
initialization.initialization_type = "hybrid"
initialization.hybrid_initialize()

BoundaryCondition(solver).slit_interior_between_diff_solids()
write_case(solver, file_name="hx-fin-2mm.cas.h5")

#############################################################################
# Set Aggressive Length Scale Method; Run Calculation & Save Data
# ===============================================================

run_calc = RunCalculation(solver)
run_calc.pseudo_time_settings.time_step_method.time_step_method = "automatic"
run_calc.pseudo_time_settings.time_step_method.length_scale_methods = "aggressive"

run_calc.iterate(iter_count=250)

write_case_data(solver, file_name="hx-fin-2mm.dat.h5")

#############################################################################
# Post-Processing Mass Balance Report
# ===================================

fluxes = Fluxes(solver)
inlet_mfr = fluxes.get_mass_flow(zones=["inlet"])
outlet_mfr = fluxes.get_mass_flow(zones=["outlet"])
net_mfr = inlet_mfr - outlet_mfr

print("Mass Balance Report\n")
print("Inlet (kg/s): ", inlet_mfr)
print("Outlet (kg/s): ", outlet_mfr)
print("Net (kg/s): ", net_mfr)

#############################################################################
# Heat Balance Report
# ===================

htr = fluxes.get_heat_transfer()

print("Heat Balance Report\n")
print("Net Imbalance (Watt): ", htr)

#############################################################################
# Plot Monitors
# =============

fig, axs = plt.subplots(2, 2, figsize=(10, 8))
fig.suptitle("Monitor Plots")

out_files = sorted(Path.cwd().glob("*.out"))
index = 0
for ax, file in zip(axs.flat, out_files):
    X = []
    Y = []
    i = -1
    with file.open() as fp:
        for rows in csv.reader(fp, delimiter=" "):
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

contour1 = Contour(solver=solver, field="temperature", surfaces=wall_list)
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

IsoSurface.create(
    solver,
    name="x=0.012826",
    field="x-coordinate",
    iso_values=[0.012826 * m],
)

#############################################################################
# Vector Plot
# ===========

vector1 = Vector(
    solver=solver,
    field="velocity",
    color_by="x-velocity",
    surfaces=[iso_x.name],
    scale=2.0,
    skip=5,
)
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
    solver=solver,
    surfaces=[iso_x.name],
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
solver.exit()
