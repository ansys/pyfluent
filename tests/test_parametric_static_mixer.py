""".. _ref_parametric_static_mixer_1:

Parametric Study Workflow
------------------------------
This example for executing a parametric study workflow
performs these steps:

- Reads a case file and data file
- Creates input and output parameters
- Instantiates a design point study
- Accesses and modifies the input parameters of
  the base design point (DP)
- Updates the current DP
- Accesses output parameters of the base DP
- Creates, updates, and deletes more DPs
- Creates, renames, and deletes parametric studies
"""

############################################################################
# Import the path module
from pathlib import Path

############################################################################
# Import the pyfluent module
import ansys.fluent.core as pyfluent

############################################################################
# Launch Fluent in 3D and double precision

session = pyfluent.launch_fluent(precision="double", processor_count=4)

############################################################################
# Enable the settings API (Beta)

root = session.get_settings_root()

############################################################################
# Read the hopper/mixer case

from ansys.fluent.core import examples

import_filename = examples.download_file(
    "Static_Mixer_main.cas.h5", "pyfluent/static_mixer"
)

session.tui.solver.file.read_case(case_file_name=import_filename)

############################################################################
# Set number of iterations to 1000 to ensure convergence

session.tui.solver.solve.set.number_of_iterations("1000")

############################################################################
# Create input parameters after enabling parameter creation in the TUI:
# Parameter values:
# Inlet1: velocity (inlet1_vel) 5 m/s and temperature (inlet1_temp) at 300 K
# Inlet2: velocity (inlet2_vel) 10 m/s and temperature (inlet2_temp) at 350 K

session.tui.solver.define.parameters.enable_in_TUI("yes")

session.tui.solver.define.boundary_conditions.set.velocity_inlet(
    "inlet1", (), "vmag", "yes", "inlet1_vel", 5, "quit"
)
session.tui.solver.define.boundary_conditions.set.velocity_inlet(
    "inlet1", (), "temperature", "yes", "inlet1_temp", 300, "quit"
)

session.tui.solver.define.boundary_conditions.set.velocity_inlet(
    "inlet2", (), "vmag", "yes", "no", "inlet2_vel", 10, "quit"
)
session.tui.solver.define.boundary_conditions.set.velocity_inlet(
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

session.tui.solver.define.parameters.enable_in_TUI("yes")
session.tui.solver.define.parameters.output_parameters.create(
    "report-definition", "outlet-temp-avg"
)
session.tui.solver.define.parameters.output_parameters.create(
    "report-definition", "outlet-vel-avg"
)

###########################################################################
# Enable convergence condition check

session.tui.solver.solve.monitors.residual.criterion_type("0")

###########################################################################
# Write case with all the settings in place
case_path = str(
    Path(pyfluent.EXAMPLES_PATH) / "Static_Mixer_Parameters.cas.h5"
)
session.tui.solver.file.write_case(case_path)

###########################################################################
# Parametric study workflow
# Import the parametric study module

from ansys.fluent.parametric import ParametricStudy

###########################################################################
# Instantiate a parametric study from a Fluent session

study_1 = ParametricStudy(root.parametric_studies).initialize()

###########################################################################
# Access and modify input parameters of base DP

input_parameters_update = study_1.design_points["Base DP"].input_parameters
input_parameters_update["inlet1_vel"] = 15
study_1.design_points["Base DP"].input_parameters = input_parameters_update

###########################################################################
# Update current design point

study_1.update_current_design_point()

###########################################################################
# Change value of specific design points

design_point_1 = study_1.add_design_point()
design_point_1_input_parameters = study_1.design_points["DP1"].input_parameters
design_point_1_input_parameters["inlet1_temp"] = 450
design_point_1_input_parameters["inlet1_vel"] = 30
design_point_1_input_parameters["inlet2_vel"] = 20
study_1.design_points["DP1"].input_parameters = design_point_1_input_parameters

###########################################################################
# Add another design point with different values of the input parameters

design_point_2 = study_1.add_design_point()
design_point_2_input_parameters = study_1.design_points["DP2"].input_parameters
design_point_2_input_parameters["inlet1_temp"] = 500
design_point_2_input_parameters["inlet1_vel"] = 45
design_point_2_input_parameters["inlet2_vel"] = 30
study_1.design_points["DP2"].input_parameters = design_point_2_input_parameters

##########################################################################
# Duplicate design points

design_point_3 = study_1.duplicate_design_point(design_point_2)

#########################################################################
# Update all design points for study 1

study_1.update_all_design_points()

#########################################################################
# Export design point table as a CSV table

design_point_table = str(
    Path(pyfluent.EXAMPLES_PATH) / "design_point_table_study_1.csv"
)
study_1.export_design_table(design_point_table)

#########################################################################
# Display CSV table as a pandas dataframe

import pandas as pd

data_frame = pd.read_csv(design_point_table)

from pytest import approx

def test_outlet_temp_design_point_1():
    assert float(data_frame['outlet-temp-avg-op'][2]) == approx(409.968, rel = 1e-2)

def test_outlet_vel_design_point_1():
    assert float(data_frame['outlet-vel-avg-op'][2]) == approx(61.46377, rel = 1e-2)

def test_outlet_temp_design_point_2():
    assert float(data_frame['outlet-temp-avg-op'][3]) == approx(439.978, rel = 1e-2)

def test_outlet_vel_design_point_2():
    assert float(data_frame['outlet-vel-avg-op'][3]) == approx(93.58455, rel = 1e-2)

##########################################################################
# Delete design points

study_1.delete_design_points([design_point_1, design_point_2])

##########################################################################
# Create a new parametric study by duplicating the current one

study_2 = study_1.duplicate()

#########################################################################
# Rename the newly created parametric study
# Currently affected by issue # 249, hence commented out

# study_2.rename("New Study")

#########################################################################
# Delete the old parametric study
# Currently affected by issue #249, hence commented out

# study_1.delete()

#########################################################################
# Save parametric project

project_filepath = str(
    Path(pyfluent.EXAMPLES_PATH) / "static_mixer_study.flprj"
)

session.tui.solver.file.parametric_project.save_as(project_filepath)
