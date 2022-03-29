"""
This example demonstrates how to perform a design point study based on
Fluent Parametric Study Workflow.

In this example we do the following:

1) Parametric Study Workflow
- Read a case and data file.
- Create input and output parameters.
- Instantiate Design Point Study
- Access and Modify the input parameters of Base Design Point (DP).
- Update the current design point.
- Access output parameters of the Base DP
- Create, Update and Delete more design points.
- Create, Rename and Delete Parametric Studies

2) Project Based Workflow
- Instantiate a parametric study from a Fluent session
- Read the previously saved project - static_mixer_study.flprj
- Save the current Project
- Save the current Project as a different file name
- Export the current project
- Archive the current project
- Exit the Parametric Project Workflow

3) Parametric Session Workflow
- Launch Parametric Session using the Hopper/Mixer Case File
- Print the input parameters of the Current Parametric Session.
- Access the current study of the current parametric session
- Create a new study in a parametric session
- Rename this newly created study
- Create a new Parametric Session using the flprj saved earlier

"""
############################################################################
# Import the PyFluent module
import ansys.fluent.core as pyfluent

############################################################################

# Launch Fluent in 3-D and Double Precision
s = pyfluent.launch_fluent(precision="double", processor_count=4)

############################################################################

# Enable the settings API

root = s.get_settings_root()

############################################################################

# Read the Hopper/Mixer Case
s.tui.solver.file.read_case(case_file_name="Static_Mixer_main.cas.h5")

############################################################################

# Set Number of Iterations to 1000 to ensure convergence
s.tui.solver.solve.set.number_of_iterations("1000")
############################################################################

# Create Input Parameters after enabling parameter creation in the TUI:
# Parameter Values:
# Inlet1: Velocity (inlet1_vel) 5m/s and Temperature (inlet1_temp) at 300 K
# Inlet2: Velocity (inlet2_vel) 10 m/s and Temperature (inlet2_temp) at 350 K

s.tui.solver.define.parameters.enable_in_TUI("yes")

s.tui.solver.define.boundary_conditions.set.velocity_inlet(
    "inlet1", (), "vmag", "yes", "inlet1_vel", 5, "quit"
)
s.tui.solver.define.boundary_conditions.set.velocity_inlet(
    "inlet1", (), "temperature", "yes", "inlet1_temp", 300, "quit"
)

s.tui.solver.define.boundary_conditions.set.velocity_inlet(
    "inlet2", (), "vmag", "yes", "no", "inlet2_vel", 10, "quit"
)
s.tui.solver.define.boundary_conditions.set.velocity_inlet(
    "inlet2", (), "temperature", "yes", "no", "inlet2_temp", 350, "quit"
)

###########################################################################

# Create output parameters using report definitions

root.solution.report_definitions.surface["outlet-temp-avg"] = {}
root.solution.report_definitions.surface[
    "outlet-temp-avg"
].report_type = "surface-areaavg"
root.solution.report_definitions.surface[
    "outlet-temp-avg"
].field = "temperature"
root.solution.report_definitions.surface["outlet-temp-avg"].surface_names = [
    "outlet"
]

root.solution.report_definitions.surface["outlet-vel-avg"] = {}
root.solution.report_definitions.surface[
    "outlet-vel-avg"
].report_type = "surface-areaavg"
root.solution.report_definitions.surface[
    "outlet-vel-avg"
].field = "velocity-magnitude"
root.solution.report_definitions.surface["outlet-vel-avg"].surface_names = [
    "outlet"
]

s.tui.solver.define.parameters.enable_in_TUI("yes")
s.tui.solver.define.parameters.output_parameters.create(
    "report-definition", "outlet-temp-avg"
)
s.tui.solver.define.parameters.output_parameters.create(
    "report-definition", "outlet-vel-avg"
)

###########################################################################

# Enable convergence condition check

s.tui.solver.solve.monitors.residual.criterion_type("0")

###########################################################################

# Write Case with all the settings in place

s.tui.solver.file.write_case("Static_Mixer_Parameters.cas.h5")

###########################################################################
# 1) Parametric Study Workflow

# Import the Parametric Study Module

from ansys.fluent.parametric import ParametricStudy

###########################################################################

# Instantiate a parametric study from a Fluent session

study1 = ParametricStudy(root.parametric_studies).initialize()

###########################################################################

# Access and Modify Input Parameters of Base DP
ip = study1.design_points["Base DP"].input_parameters
ip["inlet1_vel"] = 15
study1.design_points["Base DP"].input_parameters = ip

###########################################################################

# Update Current Design Point
study1.update_current_design_point()

###########################################################################

# Change value of specific design points

dp1 = study1.add_design_point()
dp1_ip = study1.design_points["DP1"].input_parameters
dp1_ip["inlet1_temp"] = 450
dp1_ip["inlet1_vel"] = 30
dp1_ip["inlet2_vel"] = 20
study1.design_points["DP1"].input_parameters = dp1_ip

###########################################################################

# Add another design point with different values of the input parameters

dp2 = study1.add_design_point()
dp2_ip = study1.design_points["DP2"].input_parameters
dp2_ip["inlet1_temp"] = 500
dp2_ip["inlet1_vel"] = 45
dp2_ip["inlet2_vel"] = 30
study1.design_points["DP2"].input_parameters = dp2_ip

##########################################################################

# Duplicate Design Points

dp3 = study1.duplicate_design_point(dp2)

#########################################################################

# Update all Design Points for Study 1

study1.update_all_design_points()

##########################################################################

# Delete Design Points

study1.delete_design_points([dp1, dp2])

##########################################################################

# Create a new parametric study by duplicating the current one
study2 = study1.duplicate()

#########################################################################

# Rename the newly create parametric study

study2.rename("New Study")

#########################################################################

# Delete the old parametric study

study1.delete()

#########################################################################

# Export design point table as a CSV table

# study2.export_design_table("dp_table_study2.csv")

#########################################################################

# Save Parametric Project

s.tui.solver.file.parametric_project.save_as("static_mixer_study.flprj")

#########################################################################

# Exit the parametric study session

s.exit()

#########################################################################

# 2. Parametric Project Workflow

#########################################################################

# Import the Parametric Project Module and the Parametric Study Module
from ansys.fluent.parametric import ParametricProject

#########################################################################

# Launch Fluent and Enable the Settings Object API
s = pyfluent.launch_fluent(precision="double", processor_count=4)
root = s.get_settings_root()

#########################################################################

# Read the previously saved project - static_mixer_study.flprj
proj = ParametricProject(
    root.file.parametric_project,
    root.parametric_studies,
    "static_mixer_study.flprj",
)

#########################################################################

# Save the current Project
proj.save()

#########################################################################

# Save the current Project as a different file name
proj.save_as(project_filepath="static_mixer_study_save_as.flprj")

#########################################################################

# Export the current project
proj.export(project_filepath="static_mixer_study_export.flprj")

#########################################################################

# Archive the current project
proj.archive()

#########################################################################

# Exit the Parametric Project Workflow

s.exit()

#########################################################################

# 3. Parametric Session Workflow
# Import the Parametric Session workflow

from ansys.fluent.parametric import ParametricSession

#########################################################################

# Launch Parametric Session using the Static mixer Case File
# This case file contains pre-created input and output parameters

s1 = ParametricSession(case_filepath="Static_Mixer_Parameters.cas.h5")

#########################################################################

# Print the input parameters of the Current Parametric Session.

s1.studies["Static_Mixer_Parameters-Solve"].design_points[
    "Base DP"
].input_parameters

#########################################################################

# Access the current study of the current parametric session

study1_session = s1.studies["Static_Mixer_Parameters-Solve"]

ip = study1_session.design_points["Base DP"].input_parameters
ip["inlet1_vel"] = 15
study1_session.design_points["Base DP"].input_parameters = ip

dp1 = study1_session.add_design_point()
dp1_ip = study1_session.design_points["DP1"].input_parameters
dp1_ip["inlet1_temp"] = 323
dp1_ip["inlet1_vel"] = 33
dp1_ip["inlet2_vel"] = 25
study1_session.design_points["DP1"].input_parameters = dp1_ip

#########################################################################

# In this parametric project create a new study
study2_session = s1.new_study()

#########################################################################

# Update all design points
study2_session.update_all_design_points()

#########################################################################

# Access a new Parametric Session using the flprj saved earlier
s2 = ParametricSession(project_filepath="static_mixer_study_save_as.flprj")

#########################################################################

# Delete the 2 Parametric Sessions
del s1
del s2
