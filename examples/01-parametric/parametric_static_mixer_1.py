"""
.. _ref_parametric_static_mixer_1:

Parametric Study Workflow
------------------------------
This example for executing a parametric study workflow performs these steps: 

- Reads a case file and data file
- Creates input and output parameters
- Instantiates a design point study
- Accesses and modifies the input parameters of the base design point (DP)
- Updates the current DP
- Accesses output parameters of the base DP
- Creates, updates, and deletes more DPs
- Creates, renames, and deletes parametric studies


"""

############################################################################
# Import the pyfluent module
import ansys.fluent.core as pyfluent

# Import the path module
from pathlib import Path

############################################################################

# Launch Fluent in 3D and double precision

s = pyfluent.launch_fluent(precision="double", processor_count=4)

############################################################################

# Enable the settings API

root = s.get_settings_root()

############################################################################

# Read the hopper/mixer Case

from ansys.fluent.core import examples


import_filename = examples.download_file(
    "Static_Mixer_main.cas.h5", "pyfluent/static_mixer"
)


s.tui.solver.file.read_case(case_file_name=import_filename)

############################################################################

# Set number of iterations to 1000 to ensure convergence
s.tui.solver.solve.set.number_of_iterations("1000")
############################################################################

# Create input parameters after enabling parameter creation in the TUI:
# Parameter values:
# Inlet1: velocity (inlet1_vel) 5 m/s and temperature (inlet1_temp) at 300 K
# Inlet2: velocity (inlet2_vel) 10 m/s and temperature (inlet2_temp) at 350 K

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

# Write case with all the settings in place
case_path = str(
    Path(pyfluent.EXAMPLES_PATH) / "Static_Mixer_Parameters.cas.h5"
)
s.tui.solver.file.write_case(case_path)

###########################################################################
# Parametric study workflow

# Import the parametric study module

from ansys.fluent.parametric import ParametricStudy

###########################################################################

# Instantiate a parametric study from a Fluent session

study1 = ParametricStudy(root.parametric_studies).initialize()

###########################################################################

# Access and modify input parameters of base DP
ip = study1.design_points["Base DP"].input_parameters
ip["inlet1_vel"] = 15
study1.design_points["Base DP"].input_parameters = ip

###########################################################################

# Update current design point
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

# Duplicate design points

dp3 = study1.duplicate_design_point(dp2)

#########################################################################

# Update all design points for study 1

study1.update_all_design_points()

#########################################################################

# Export design point table as a CSV table
dp_table = str(Path(pyfluent.EXAMPLES_PATH) / "dp_table_study1.csv")

study1.export_design_table(dp_table)

#########################################################################

# Display CSV table as pandas dataframe
# import pandas as pd
# df = pd.read_csv(dp_table)
# print(df)

##########################################################################

# Delete design points

study1.delete_design_points([dp1, dp2])

##########################################################################

# Create a new parametric study by duplicating the current one
study2 = study1.duplicate()

#########################################################################

# Rename the newly create parametric study

# study2.rename("New Study")

#########################################################################

# Delete the old parametric study

# study1.delete()

#########################################################################

# Save parametric project

proj_path = str(Path(pyfluent.EXAMPLES_PATH) / "static_mixer_study.flprj")

s.tui.solver.file.parametric_project.save_as(proj_path)
