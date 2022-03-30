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
