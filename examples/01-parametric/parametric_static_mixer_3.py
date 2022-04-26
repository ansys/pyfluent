""".. _ref_parametric_static_mixer_3:

Parametric Session Workflow
----------------------------------------------
This example for executing a parametric session workflow performs these steps:

- Launches a parametric session using the hopper/mixer case file
- Prints the input parameters of the current parametric session
- Accesses the current study of the current parametric session
- Creates a new study in a parametric session
- Renames this newly created study
- Creates a new parametric session using the flprj saved earlier
"""

#########################################################################
from pathlib import Path

import pandas as pd

import ansys.fluent.core as pyfluent
from ansys.fluent.parametric import ParametricSession

#########################################################################
# Launch parametric session using the hopper/mixer case File
# This case file contains pre-created input and output parameters

case_path = str(Path(pyfluent.EXAMPLES_PATH) / "Static_Mixer_Parameters.cas.h5")

session = ParametricSession(case_filepath=case_path)

#########################################################################
# Print the input parameters of the current parametric session.

session.studies["Static_Mixer_Parameters-Solve"].design_points[
    "Base DP"
].input_parameters

#########################################################################
# Access the current study of the current parametric session

study_1 = session.studies["Static_Mixer_Parameters-Solve"]

input_parameters_update = study_1.design_points["Base DP"].input_parameters
input_parameters_update["inlet1_vel"] = 15
study_1.design_points["Base DP"].input_parameters = input_parameters_update

design_point_1 = study_1.add_design_point()
design_point_1_input_parameters = study_1.design_points["DP1"].input_parameters
design_point_1_input_parameters["inlet1_temp"] = 323
design_point_1_input_parameters["inlet1_vel"] = 33
design_point_1_input_parameters["inlet2_vel"] = 25
study_1.design_points["DP1"].input_parameters = design_point_1_input_parameters

#########################################################################
# In this parametric project create a new study

study_2 = session.new_study()

#########################################################################
# Update all design points
study_2.update_all_design_points()

#########################################################################
# Export design point table as a CSV table

design_point_table_study_2 = str(
    Path(pyfluent.EXAMPLES_PATH) / "design_point_table_study_2.csv"
)
study_2.export_design_table(design_point_table_study_2)

#########################################################################
# Display CSV table as a pandas dataframe

data_frame = pd.read_csv(design_point_table_study_2)
print(data_frame)

#########################################################################
# Access a new parametric session using the flprj saved earlier

project_session_filepath = str(
    Path(pyfluent.EXAMPLES_PATH) / "static_mixer_study_save_as.flprj"
)
new_session = ParametricSession(project_filepath=project_session_filepath)
