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

""".. _ref_parametric_static_mixer_1:

Parametric study workflow
-------------------------
This example shows how you can use the parametric study workflow to analyze a
static mixer.
"""

from pathlib import Path

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.core.solver import (
    Monitor,
    NamedExpression,
    OutputParameters,
    ParametricStudies,
    ReportDefinitions,
    RunCalculation,
    VelocityInlet,read_case, write_case
)
from ansys.units import VariableCatalog
from ansys.units.common import K, m, s

# sphinx_gallery_thumbnail_path = '_static/DP_table.png'
############################################################################
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Perform the required imports.


############################################################################
# Launch Fluent
# ~~~~~~~~~~~~~
# Launch Fluent in 3D and double precision and print Fluent version.

solver = pyfluent.Solver.from_install(
    precision=pyfluent.Precision.DOUBLE, processor_count=2
)
print(solver.get_fluent_version())

############################################################################
# Download and read files
# ~~~~~~~~~~~~~~~~~~~~~~~
# Download the files for this example and read the case for the static mixer.

import_filename = examples.download_file(
    "Static_Mixer_main.cas.h5",
    "pyfluent/static_mixer",
    save_path=Path.cwd(),
)

read_case(solver, file_name=import_filename)

############################################################################
# Set iterations
# ~~~~~~~~~~~~~~
# Set the number of iterations to 100.

run_calc = RunCalculation(solver)
run_calc.iter_count = 100

############################################################################
# Create input parameters
# ~~~~~~~~~~~~~~~~~~~~~~~
# Enable parameter creation in the TUI and then create input parameters for
# the velocity and temperatures of inlets 1 and 2:
# Parameter values:
# Inlet1: velocity (inlet1_vel) 0.5 m/s and temperature (inlet1_temp) at 300 K
# Inlet2: velocity (inlet2_vel) 0.5 m/s and temperature (inlet2_temp) at 350 K

solver.settings.parameters.enable_in_tui = True

# Create named expressions using typed helper and units
inlet1_vel = NamedExpression.create(
    solver,
    name="inlet1_vel",
    output_parameter=False,
    input_parameter=True,
    unit="velocity",
    parametername="inlet1_vel",
    parameterid="real-1",
    definition=1 * m / s,
)

inlet1_temp = NamedExpression.create(
    solver,
    name="inlet1_temp",
    output_parameter=False,
    input_parameter=True,
    unit="temperature",
    parametername="inlet1_temp",
    parameterid="real-2",
    definition=300 * K,
)

inlet2_vel = NamedExpression.create(
    solver,
    name="inlet2_vel",
    output_parameter=False,
    input_parameter=True,
    unit="velocity",
    parametername="inlet2_vel",
    parameterid="real-3",
    definition=1 * m / s,
)

inlet2_temp = NamedExpression.create(
    solver,
    name="inlet2_temp",
    output_parameter=False,
    input_parameter=True,
    unit="temperature",
    parametername="inlet2_temp",
    parameterid="real-4",
    definition=350 * K,
)

inlet1 = VelocityInlet(solver, "inlet1")
inlet1.momentum.velocity = inlet1_vel.name
inlet1.thermal.temperature = inlet1_temp.name

inlet2 = VelocityInlet(solver, "inlet2")
inlet2.momentum.velocity = inlet2_vel.name
inlet2.thermal.temperature = inlet2_temp.name

###########################################################################
# Create output parameters
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Create output parameters named ``outlet-temp-avg`` and ``outlet-vel-avg``
# using report definitions.

report_defs = ReportDefinitions(solver)
outlet_temp_avg = report_defs.surface.create(
    "outlet-temp-avg",
    report_type="surface-areaavg",
    field=VariableCatalog.TEMPERATURE,
    surface_names=["outlet"],
)

outlet_vel_avg = report_defs.surface.create(
    "outlet-vel-avg",
    report_type="surface-areaavg",
    field=VariableCatalog.VELOCITY_MAGNITUDE,
    surface_names=[outlet.name()],
)

params = OutputParameters(solver)
param5 = params.report_definitions.create(
    "parameter-5", report_def_name=outlet_temp_avg
)

param6 = params.report_definitions.create(
    "parameter-6", report_def_name=outlet_vel_avg
)

###########################################################################
# Enable convergence condition check
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Enable the convergence condition check.

Monitor(solver).residual.options.criterion_type = "absolute"

###########################################################################
# Write case
# ~~~~~~~~~~
# Write the case with all settings in place.

write_case(file_name="Static_Mixer_Parameters.cas.h5")

###########################################################################
# Initialize parametric study
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Initialize a parametric design point study from a Fluent session.

parametric_studies = ParametricStudies(solver)
parametric_studies.initialize(project_filename="project_1")

###############################################################################
# .. image:: /_static/DP_table_011.png
#   :width: 500pt
#   :align: center

###########################################################################
# Access and modify input parameters
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Access and modify the input parameters of the base design point.


study = parametric_studies["Static_Mixer_main-Solve"]
dp_base = study.design_points["Base DP"]
dp_base.input_parameters.create(inlet1_temp.name, value=300 * K)
dp_base.input_parameters.create(inlet2_temp.name, value=350 * K)
dp_base.input_parameters.create(inlet2_vel.name, value=1 * m / s)
dp_base.input_parameters.create(inlet1_vel.name, value=0.5 * m / s)

###########################################################################
# Update current design point
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Update the current design point.

study.design_points.update_current()

###########################################################################
# Add design point (DP)
# ~~~~~~~~~~~~~~~~~~~~~
# Add a design point.

dp_table = study.design_points.create(
    write_data=False, capture_simulation_report_data=True
)

dp1 = dp_table["DP1"]
dp1.input_parameters.create(inlet1_vel.name, value=1 * m / s)
dp1.input_parameters.create(inlet2_vel.name, value=1 * m / s)
dp1.input_parameters.create(inlet1_temp.name, value=500 * K)
dp1.input_parameters.create(inlet2_temp.name, value=350 * K)

##########################################################################
# Duplicate design point
# ~~~~~~~~~~~~~~~~~~~~~~~
# Duplicate design point 1 to create design point 2.

study.design_points.duplicate(design_point="DP1")

#########################################################################
# Update all design points
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Update all design points.

study.design_points.update_all()

###############################################################################
# .. image:: /_static/DP_table_012.png
#   :width: 500pt
#   :align: center

###############################################################################
# Export design point table
# ~~~~~~~~~~~~~~~~~~~~~~~~~
# Export the design point table to a CSV file.

parametric_studies.export_design_table(filepath="design_point_table_study_1.csv")

##########################################################################
# Delete design point
# ~~~~~~~~~~~~~~~~~~~
# Delete design point 1.

study.design_points.delete_design_points(design_points=["DP1"])

##########################################################################
# Create parametric study
# ~~~~~~~~~~~~~~~~~~~~~~~
# Create another parametric study by duplicating the current one.

parametric_studies.duplicate(copy_design_points=True)

#########################################################################
# Rename new parametric study
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Rename the newly created parametric study.

parametric_studies.rename(new="New Study", old="Static_Mixer_main-1-Solve")

#########################################################################
# Delete old parametric study
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Delete the old parametric study.

parametric_studies.delete(name_list="Static_Mixer_main-Solve")

#########################################################################
# Save parametric project and close Fluent
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Save the parametric project and close Fluent.

solver.settings.file.parametric_project.save_as(
    project_filename="static_mixer_study_save.flprj"
)

#########################################################################
# Read saved project
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Read the previously saved project.

solver.settings.file.parametric_project.open(
    project_filename=Path.cwd() / "static_mixer_study_save.flprj",
    load_case=True,
)

#########################################################################
# Save current project
# ~~~~~~~~~~~~~~~~~~~~
# Save the current project.

solver.settings.file.parametric_project.save()

#########################################################################
# Save current project as a different project
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Save the current project as a different project.

solver.settings.file.parametric_project.save_as(
    project_filename="static_mixer_study_save_as.flprj"
)

#########################################################################
# Export current project
# ~~~~~~~~~~~~~~~~~~~~~~
# Export the current project.

solver.settings.file.parametric_project.save_as_copy(
    project_filename="static_mixer_study_export.flprj", convert_to_managed=False
)

#########################################################################
# Archive current project
# ~~~~~~~~~~~~~~~~~~~~~~~
# Archive the current project.

solver.settings.file.parametric_project.archive(
    archive_name="static_mixer_study_archive.flprj"
)

#########################################################################
# Close Fluent
# ~~~~~~~~~~~~
# Close Fluent.

solver.exit()
