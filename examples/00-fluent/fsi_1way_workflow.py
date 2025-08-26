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

""".. _One_Way_FSI_Simulation:

Modeling One-Way Fluid-Structure Interaction
-------------------------------------------------------------
"""

#######################################################################################
# Objective
# =====================================================================================
#
# The Simulation focuses on simulating turbulent airflow through a cylindrical test chamber
# containing a steel probe, and analyzing the deformation of the probe due to
# aerodynamic forces. The deformation is assumed to be small enough that it
# does not influence the fluid flow, allowing for a one-way coupling approach.

#######################################################################################
# Problem Description:
# =====================================================================================
#
# The cylindrical test chamber is 20 cm long, with a diameter of 10 cm.
# Turbulent air enters the chamber at 100 m/s, flows around and through
# the steel probe, and exits through a pressure outlet.
#
#
# .. image:: ../../_static/fsi_1way_1.png
#    :align: center
#    :alt: One-Way Fluid-Structure Interaction Model

#######################################################################################
# Import modules
# =====================================================================================

import os

import ansys.fluent.core as pyfluent
from ansys.fluent.core import FluentMode, Precision, examples

#######################################################################################
# Launch Fluent session in solver mode
# =====================================================================================

solver = pyfluent.launch_fluent(
    precision=Precision.DOUBLE,
    mode=FluentMode.SOLVER,
)

#######################################################################################
# Download and Read the journal file
# =====================================================================================
#
# .. note::
#   Mesh file is required as input for the journal file.
#
# Journal file serves as a script that instructs Ansys Fluent on sequential operations

journal_file = examples.download_file(
    "fsi_1way.jou",
    "pyfluent/fsi_1way",
    save_path=os.getcwd(),
)

examples.download_file(
    "fsi_1way.msh.h5",
    "pyfluent/fsi_1way",
    save_path=os.getcwd(),
)

solver.tui.file.read_journal(journal_file)  # Read the journal file

graphics_object = solver.settings.results.graphics
graphics_object.picture.x_resolution = 650
graphics_object.picture.y_resolution = 450
graphics_object.views.restore_view(view_name="front")

solver.settings.results.graphics.contour["contour-vel"].display()
graphics_object.picture.save_picture(file_name="fsi_1way_2.png")

# %%
# .. image:: ../../_static/fsi_1way_2.png
#    :align: center
#    :alt: Velocity Contour

#######################################################################################
# Structural model and Material
# =====================================================================================
# To analyze the deformation of a steel probe under fluid flow,
# Linear Elasticity Structural model is chosen

solver.settings.setup.models.structure.model = "linear-elasticity"

# Copy materials from the database and assign to solid zone

solver.settings.setup.materials.database.copy_by_name(type="solid", name="steel")
solver.settings.setup.cell_zone_conditions.solid["solid"] = {
    "general": {"material": "steel"}
}

#######################################################################################
# Defining the boundary conditions
# =====================================================================================
# configure Fluent to define the steel probe's support and movement using
# structural boundary conditions

wall = solver.settings.setup.boundary_conditions.wall

# Configure solid-symmetry boundary
wall["solid-symmetry"] = {
    "structure": {
        "z_disp_boundary_value": 0,
        "z_disp_boundary_condition": "Node Z-Displacement",
    }
}

# Set solid-top boundary
wall["solid-top"] = {
    "structure": {
        "z_disp_boundary_value": 0,
        "z_disp_boundary_condition": "Node Z-Displacement",
        "y_disp_boundary_value": 0,
        "y_disp_boundary_condition": "Node Y-Displacement",
        "x_disp_boundary_value": 0,
        "x_disp_boundary_condition": "Node X-Displacement",
    }
}

# Copy boundary conditions from solid-symmetry to solid-symmetry:011
solver.settings.setup.boundary_conditions.copy(
    from_="solid-symmetry", to=["solid-symmetry:011"]
)

# Configure FSI surface
wall["fsisurface-solid"] = {
    "structure": {
        "z_disp_boundary_condition": "Intrinsic FSI",
        "y_disp_boundary_condition": "Intrinsic FSI",
        "x_disp_boundary_condition": "Intrinsic FSI",
    }
}

#######################################################################################
# Inclusion of Operating Pressure in Fluid-Structure Interaction Forces
# =====================================================================================
# Fluent uses gauge pressure for fluid-structure interaction force calculations.
# By setting  ``include_pop_in_fsi_force`` to  ``True``, Fluent uses absolute pressure.

solver.settings.setup.models.structure.expert.include_pop_in_fsi_force = True

#######################################################################################
# Configure flow settings
# =====================================================================================

solver.settings.solution.controls.equations["flow"] = False
solver.settings.solution.controls.equations["kw"] = False

#######################################################################################
# Run the simulation
# =====================================================================================

solver.settings.file.write_case(file_name="probe_fsi_1way.cas.h5")  # save the case file

solver.settings.solution.run_calculation.iter_count = 2
solver.settings.solution.run_calculation.calculate()

#######################################################################################
# Post-Processing
# =====================================================================================

displacement_contour = solver.settings.results.graphics.contour.create(
    "displacement_contour"
)
displacement_contour.field = "total-displacement"
displacement_contour.surfaces_list = ["fsisurface-solid"]
displacement_contour.range_options.compute()

graphics_object.views.restore_view(view_name="front")
displacement_contour.display()
graphics_object.picture.save_picture(file_name="fsi_1way_3.png")

# save the case and data file
solver.settings.file.write_case_data(file_name="probe_fsi_1way")

# %%
# .. image:: ../../_static/fsi_1way_3.png
#    :align: center
#    :alt: Structural Displacement Contour

#######################################################################################
# Close the solver
# =====================================================================================
solver.exit()

#######################################################################################
# References:
# =====================================================================================
# .. _Reference:
# [1] Modeling One-Way Fluid-Structure Interaction (FSI) Within Fluent, `Ansys Fluent documentation​ <https://ansyshelp.ansys.com/public/account/secured?returnurl=/Views/Secured/corp/v252/en/flu_tg/flu_tg_fsi_1way.html>`_.

# sphinx_gallery_thumbnail_path = '_static/fsi_1way_2.png'
