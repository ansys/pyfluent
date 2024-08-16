""".. _ref_parametric_static_mixer_1:

Parametric study workflow
-------------------------
This example shows how you can use the parametric study workflow to analyze a
static mixer.

"""

from pathlib import Path

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.parametric import ParametricProject, ParametricStudy

# sphinx_gallery_thumbnail_path = '_static/DP_table.png'
############################################################################
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Perform the required imports.


############################################################################
# Launch Fluent
# ~~~~~~~~~~~~~
# Launch Fluent in 3D and double precision.

solver_session = pyfluent.launch_fluent(
    precision="double", processor_count=2, mode="solver"
)

############################################################################
# Download and read files
# ~~~~~~~~~~~~~~~~~~~~~~~
# Download the files for this example and read the case for the static mixer.

import_filename = examples.download_file(
    "Static_Mixer_main.cas.h5", "pyfluent/static_mixer", return_without_path=False
)

solver_session.tui.file.read_case(import_filename)

############################################################################
# Set iterations
# ~~~~~~~~~~~~~~
# Set the number of iterations to 100.

solver_session.tui.solve.set.number_of_iterations("100")

############################################################################
# Create input parameters
# ~~~~~~~~~~~~~~~~~~~~~~~
# Enable parameter creation in the TUI and then create input parameters for
# the velocity and temperatures of inlets 1 and 2:
# Parameter values:
# Inlet1: velocity (inlet1_vel) 0.5 m/s and temperature (inlet1_temp) at 300 K
# Inlet2: velocity (inlet2_vel) 0.5 m/s and temperature (inlet2_temp) at 350 K

solver_session.tui.define.parameters.enable_in_TUI("yes")

solver_session.tui.define.boundary_conditions.set.velocity_inlet(
    "inlet1", (), "vmag", "yes", "inlet1_vel", 1, "quit"
)

solver_session.tui.define.boundary_conditions.set.velocity_inlet(
    "inlet1", (), "temperature", "yes", "inlet1_temp", 300, "quit"
)

solver_session.tui.define.boundary_conditions.set.velocity_inlet(
    "inlet2", (), "vmag", "yes", "no", "inlet2_vel", 1, "quit"
)

solver_session.tui.define.boundary_conditions.set.velocity_inlet(
    "inlet2", (), "temperature", "yes", "no", "inlet2_temp", 350, "quit"
)

###########################################################################
# Create output parameters
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Create output parameters named ``outlet-temp-avg`` and ``outlet-vel-avg``
# using report definitions.

solver_session.solution.report_definitions.surface["outlet-temp-avg"] = {}
solver_session.solution.report_definitions.surface["outlet-temp-avg"].report_type = (
    "surface-areaavg"
)
solver_session.solution.report_definitions.surface["outlet-temp-avg"].field = (
    "temperature"
)
solver_session.solution.report_definitions.surface["outlet-temp-avg"].surface_names = [
    "outlet"
]

solver_session.solution.report_definitions.surface["outlet-vel-avg"] = {}
solver_session.solution.report_definitions.surface["outlet-vel-avg"].report_type = (
    "surface-areaavg"
)
solver_session.solution.report_definitions.surface["outlet-vel-avg"].field = (
    "velocity-magnitude"
)
solver_session.solution.report_definitions.surface["outlet-vel-avg"].surface_names = [
    "outlet"
]

solver_session.tui.define.parameters.enable_in_TUI("yes")
solver_session.tui.define.parameters.output_parameters.create(
    "report-definition", "outlet-temp-avg"
)
solver_session.tui.define.parameters.output_parameters.create(
    "report-definition", "outlet-vel-avg"
)

###########################################################################
# Enable convergence condition check
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Enable the convergence condition check.

solver_session.tui.solve.monitors.residual.criterion_type("0")

###########################################################################
# Write case
# ~~~~~~~~~~
# Write the case with all settings in place.

case_path = str(Path(pyfluent.EXAMPLES_PATH) / "Static_Mixer_Parameters.cas.h5")
solver_session.tui.file.write_case(case_path)

###########################################################################
# Initialize parametric study
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Initialize a parametric design point study from a Fluent session.

study_1 = ParametricStudy(solver_session.parametric_studies)

###############################################################################
# .. image:: /_static/DP_table_011.png
#   :width: 500pt
#   :align: center

###########################################################################
# Access and modify input parameters
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Access and modify the input parameters of the base design point.

input_parameters_update = study_1.design_points["Base DP"].input_parameters
input_parameters_update["inlet1_vel"] = 0.5
study_1.design_points["Base DP"].input_parameters = input_parameters_update

###########################################################################
# Update current design point
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Update the current design point.

study_1.update_current_design_point()

###########################################################################
# Add design point
# ~~~~~~~~~~~~~~~~
# Add a design point.

design_point_1 = study_1.add_design_point()
design_point_1_input_parameters = study_1.design_points["DP1"].input_parameters
design_point_1_input_parameters["inlet1_temp"] = 500
design_point_1_input_parameters["inlet1_vel"] = 1
design_point_1_input_parameters["inlet2_vel"] = 1
study_1.design_points["DP1"].input_parameters = design_point_1_input_parameters

##########################################################################
# Duplicate design point
# ~~~~~~~~~~~~~~~~~~~~~~~
# Duplicate design point 1 to create design point 2.

design_point_2 = study_1.duplicate_design_point(design_point_1)

#########################################################################
# Update all design points
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Update all design points for study 1.

study_1.update_all_design_points()

###############################################################################
# .. image:: /_static/DP_table_012.png
#   :width: 500pt
#   :align: center

###############################################################################
# Export design point table
# ~~~~~~~~~~~~~~~~~~~~~~~~~
# Export the design point table to a CSV file.

design_point_table = str(
    Path(pyfluent.EXAMPLES_PATH) / "design_point_table_study_1.csv"
)
study_1.export_design_table(design_point_table)

##########################################################################
# Delete design point
# ~~~~~~~~~~~~~~~~~~~
# Delete design point 1.

study_1.delete_design_points([design_point_1])

##########################################################################
# Create parametric study
# ~~~~~~~~~~~~~~~~~~~~~~~
# Create another parametric study by duplicating the current one.

study_2 = study_1.duplicate()

#########################################################################
# Rename new parametric study
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Rename the newly created parametric study.

study_2.rename("New Study")

#########################################################################
# Delete old parametric study
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Delete the old parametric study.

study_1.delete()

#########################################################################
# Save parametric project and close Fluent
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Save the parametric project and close Fluent.

project_filepath = str(Path(pyfluent.EXAMPLES_PATH) / "static_mixer_study.flprj")

solver_session.tui.file.parametric_project.save_as(project_filepath)

solver_session.exit()

#########################################################################
# Launch Fluent and read saved project
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Launch Fluent once again and read the previously saved project.

solver_session = pyfluent.launch_fluent(
    precision="double", processor_count=2, mode="solver"
)
project_filepath_read = str(Path(pyfluent.EXAMPLES_PATH) / "static_mixer_study.flprj")

proj = ParametricProject(
    solver_session.file.parametric_project,
    solver_session.parametric_studies,
    project_filepath_read,
)

#########################################################################
# Save current project
# ~~~~~~~~~~~~~~~~~~~~
# Save the current project.

proj.save()

#########################################################################
# Save current project as a different project
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Save the current project as a different project.

project_filepath_save_as = str(
    Path(pyfluent.EXAMPLES_PATH) / "static_mixer_study_save_as.flprj"
)
proj.save_as(project_filepath=project_filepath_save_as)

#########################################################################
# Export current project
# ~~~~~~~~~~~~~~~~~~~~~~
# Export the current project.

project_filepath_export = str(
    Path(pyfluent.EXAMPLES_PATH) / "static_mixer_study_export.flprj"
)
proj.export(project_filepath=project_filepath_export)

#########################################################################
# Archive current project
# ~~~~~~~~~~~~~~~~~~~~~~~
# Archive the current project.

proj.archive()

#########################################################################
# Close Fluent
# ~~~~~~~~~~~~
# Close Fluent.

solver_session.exit()
