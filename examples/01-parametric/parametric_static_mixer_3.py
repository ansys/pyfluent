"""
.. _ref_parametric_static_mixer_3:

Parametric session workflow
----------------------------------------------
In this example we perform the following steps to
execute a parametric session workflow
- Launch parametric session using the hopper/mixer Case File
- Print the input parameters of the current parametric session.
- Access the current study of the current parametric session
- Create a new study in a parametric session
- Rename this newly created study
- Create a new parametric session using the flprj saved earlier

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

# Launch parametric session using the hopper/mixer Case File
# This case file contains pre-created input and output parameters
case_path = str(
    Path(pyfluent.EXAMPLES_PATH) / "Static_Mixer_Parameters.cas.h5"
)

s1 = ParametricSession(case_filepath=case_path)

#########################################################################

# Print the input parameters of the current parametric session.

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

# Access a new parametric session using the flprj saved earlier
proj_path_sa = str(
    Path(pyfluent.EXAMPLES_PATH) / "static_mixer_study_save_as.flprj"
)
s2 = ParametricSession(project_filepath=proj_path_sa)
