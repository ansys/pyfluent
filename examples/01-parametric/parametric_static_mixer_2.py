#########################################################################

# 2. Parametric project workflow

#########################################################################

# Import the parametric project module and the parametric study module
from ansys.fluent.parametric import ParametricProject

############################################################################
# Import the pyfluent module and path
import ansys.fluent.core as pyfluent
from pathlib import Path

#########################################################################

# Launch Fluent and enable the settings API
s = pyfluent.launch_fluent(precision="double", processor_count=4)
root = s.get_settings_root()

#########################################################################

# Read the previously saved project - static_mixer_study.flprj
proj_path = str(Path(pyfluent.EXAMPLES_PATH) / "static_mixer_study.flprj")

proj = ParametricProject(
    root.file.parametric_project,
    root.parametric_studies,
    proj_path,
)

#########################################################################

# Save the current project
proj.save()

#########################################################################

# Save the current project as a different file name
proj_path_sa = str(Path(pyfluent.EXAMPLES_PATH) / "static_mixer_study_save_as.flprj")
proj.save_as(project_filepath=proj_path_sa)

#########################################################################

# Export the current project
proj_path_exp = str(Path(pyfluent.EXAMPLES_PATH) / "static_mixer_study_export.flprj")
proj.export(project_filepath=proj_path_exp)

#########################################################################

# Archive the current project
proj.archive()
