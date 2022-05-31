""".. _ref_parametric_static_mixer_1:

Parametric Study Workflow
------------------------------
This parametric study workflow example performs these steps:

- Reads a case file and data file
- Creates input and output parameters
- Instantiates a design point study
- Accesses and modifies the input parameters of
  the base design point (DP)
- Updates design points
- Creates, updates, and deletes more DPs
- Creates, renames, duplicates and deletes parametric studies
"""

############################################################################
from pathlib import Path

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.parametric import ParametricProject, ParametricStudy
from ansys.fluent.post import set_config
from ansys.fluent.post.pyvista import Graphics

set_config(blocking=True, set_view_on_display="isometric")

############################################################################
# Launch Fluent in 3D and double precision

session = pyfluent.launch_fluent(precision="double", processor_count=2)

############################################################################
# Read the hopper/mixer case

import_filename = examples.download_file(
    "Static_Mixer_main.cas.h5", "pyfluent/static_mixer"
)

session.solver.tui.file.read_case(case_file_name=import_filename)

############################################################################
# Set number of iterations to 100

session.solver.tui.solve.set.number_of_iterations("100")

############################################################################
# Create input parameters after enabling parameter creation in the TUI:
# Parameter values:
# Inlet1: velocity (inlet1_vel) 0.5 m/s and temperature (inlet1_temp) at 300 K
# Inlet2: velocity (inlet2_vel) 0.5 m/s and temperature (inlet2_temp) at 350 K

session.solver.tui.define.parameters.enable_in_TUI("yes")

session.solver.tui.define.boundary_conditions.set.velocity_inlet(
    "inlet1", (), "vmag", "yes", "inlet1_vel", 1, "quit"
)
session.solver.tui.define.boundary_conditions.set.velocity_inlet(
    "inlet1", (), "temperature", "yes", "inlet1_temp", 300, "quit"
)

session.solver.tui.define.boundary_conditions.set.velocity_inlet(
    "inlet2", (), "vmag", "yes", "no", "inlet2_vel", 1, "quit"
)
session.solver.tui.define.boundary_conditions.set.velocity_inlet(
    "inlet2", (), "temperature", "yes", "no", "inlet2_temp", 350, "quit"
)

###########################################################################
# Create output parameters using report definitions

session.solver.root.solution.report_definitions.surface["outlet-temp-avg"] = {}
session.solver.root.solution.report_definitions.surface[
    "outlet-temp-avg"
].report_type = "surface-areaavg"
session.solver.root.solution.report_definitions.surface[
    "outlet-temp-avg"
].field = "temperature"
session.solver.root.solution.report_definitions.surface[
    "outlet-temp-avg"
].surface_names = ["outlet"]

session.solver.root.solution.report_definitions.surface["outlet-vel-avg"] = {}
session.solver.root.solution.report_definitions.surface[
    "outlet-vel-avg"
].report_type = "surface-areaavg"
session.solver.root.solution.report_definitions.surface[
    "outlet-vel-avg"
].field = "velocity-magnitude"
session.solver.root.solution.report_definitions.surface[
    "outlet-vel-avg"
].surface_names = ["outlet"]

session.solver.tui.define.parameters.enable_in_TUI("yes")
session.solver.tui.define.parameters.output_parameters.create(
    "report-definition", "outlet-temp-avg"
)
session.solver.tui.define.parameters.output_parameters.create(
    "report-definition", "outlet-vel-avg"
)

###########################################################################
# Enable convergence condition check

session.solver.tui.solve.monitors.residual.criterion_type("0")

###########################################################################
# Write case with all the settings in place
case_path = str(Path(pyfluent.EXAMPLES_PATH) / "Static_Mixer_Parameters.cas.h5")
session.solver.tui.file.write_case(case_path)

###########################################################################
# Instantiate a parametric study from a Fluent session

study_1 = ParametricStudy(session.solver.root.parametric_studies).initialize()

###########################################################################
# Access and modify input parameters of base DP

input_parameters_update = study_1.design_points["Base DP"].input_parameters
input_parameters_update["inlet1_vel"] = 0.5
study_1.design_points["Base DP"].input_parameters = input_parameters_update

###########################################################################
# Update current design point

study_1.update_current_design_point()

###########################################################################
# Add a new design point

design_point_1 = study_1.add_design_point()
design_point_1_input_parameters = study_1.design_points["DP1"].input_parameters
design_point_1_input_parameters["inlet1_temp"] = 500
design_point_1_input_parameters["inlet1_vel"] = 1
design_point_1_input_parameters["inlet2_vel"] = 1
study_1.design_points["DP1"].input_parameters = design_point_1_input_parameters

##########################################################################
# Duplicate design points

design_point_2 = study_1.duplicate_design_point(design_point_1)

#########################################################################
# Update all design points for study 1

study_1.update_all_design_points()

#########################################################################
# Mesh display using PyVista

graphics_session = Graphics(session)
mesh_1 = graphics_session.Meshes["mesh-1"]
mesh_1.show_edges = True
mesh_1.surfaces_list = [
    "inlet1",
    "inlet2",
    "wall",
    "outlet",
]

mesh_1.display()

###############################################################################
# Export design point table as a CSV table

design_point_table = str(
    Path(pyfluent.EXAMPLES_PATH) / "design_point_table_study_1.csv"
)
study_1.export_design_table(design_point_table)

##########################################################################
# Delete design points

study_1.delete_design_points([design_point_1])

##########################################################################
# Create a new parametric study by duplicating the current one

study_2 = study_1.duplicate()

#########################################################################
# Rename the newly created parametric study

study_2.rename("New Study")

#########################################################################
# Delete the old parametric study

study_1.delete()

#########################################################################
# Save parametric project and close Fluent

project_filepath = str(Path(pyfluent.EXAMPLES_PATH) / "static_mixer_study.flprj")

session.solver.tui.file.parametric_project.save_as(project_filepath)

session.exit()

#########################################################################
# Launch Fluent again and read the previously saved project

session = pyfluent.launch_fluent(precision="double", processor_count=2)
project_filepath_read = str(Path(pyfluent.EXAMPLES_PATH) / "static_mixer_study.flprj")

proj = ParametricProject(
    session.solver.root.file.parametric_project,
    session.solver.root.parametric_studies,
    project_filepath_read,
)

#########################################################################
# Save the current project

proj.save()

#########################################################################
# Save the current project to a different file name

project_filepath_save_as = str(
    Path(pyfluent.EXAMPLES_PATH) / "static_mixer_study_save_as.flprj"
)
proj.save_as(project_filepath=project_filepath_save_as)

#########################################################################
# Export the current project

project_filepath_export = str(
    Path(pyfluent.EXAMPLES_PATH) / "static_mixer_study_export.flprj"
)
proj.export(project_filepath=project_filepath_export)

#########################################################################
# Archive the current project

proj.archive()

#########################################################################
# Close Fluent

session.exit()
