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