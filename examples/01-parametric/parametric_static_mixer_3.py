"""
.. _ref_parametric_static_mixer_3:

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
# Parametric session workflow
# Import the parametric session workflow

from ansys.fluent.parametric import ParametricSession

############################################################################
# Import the pyfluent module and path

import ansys.fluent.core as pyfluent
from pathlib import Path

#########################################################################
# Launch parametric session using the hopper/mixer case File
# This case file contains pre-created input and output parameters

case_path = str(
    Path(pyfluent.EXAMPLES_PATH) / "Static_Mixer_Parameters.cas.h5"
)

session = ParametricSession(case_filepath=case_path)

#########################################################################
# Print the input parameters of the current parametric session.

session.studies["Static_Mixer_Parameters-Solve"].design_points[
    "Base DP"
].input_parameters

#########################################################################
# Access the current study of the current parametric session

study1 = session.studies["Static_Mixer_Parameters-Solve"]

ip = study1.design_points["Base DP"].input_parameters
ip["inlet1_vel"] = 15
study1.design_points["Base DP"].input_parameters = ip

design_point_1 = study1.add_design_point()
design_point_1_input_parameters = study1.design_points["DP1"].input_parameters
design_point_1_input_parameters["inlet1_temp"] = 323
design_point_1_input_parameters["inlet1_vel"] = 33
design_point_1_input_parameters["inlet2_vel"] = 25
study1.design_points["DP1"].input_parameters = design_point_1_input_parameters

#########################################################################
# In this parametric project create a new study

study2 = session.new_study()

#########################################################################
# Update all design points
study2.update_all_design_points()

#########################################################################
# Access a new parametric session using the flprj saved earlier

project_filepath_session = str(
    Path(pyfluent.EXAMPLES_PATH) / "static_mixer_study_save_as.flprj"
)
session_new = ParametricSession(project_filepath=project_filepath_session)
