#########################################################################

# 2. Parametric project workflow

#########################################################################

# Import the parametric project module and the parametric study module
from ansys.fluent.parametric import ParametricProject

#########################################################################

# Launch Fluent and enable the settings API
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

# Save the current project
proj.save()

#########################################################################

# Save the current project as a different file name
proj.save_as(project_filepath="static_mixer_study_save_as.flprj")

#########################################################################

# Export the current project
proj.export(project_filepath="static_mixer_study_export.flprj")

#########################################################################

# Archive the current project
proj.archive()

#########################################################################

# Exit the parametric project workflow

s.exit()