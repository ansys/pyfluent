"""
.. _ref_parametric_static_mixer_2:

Parametric Project-Based Workflow
----------------------------------------------------
This example for executing a parametric project-based workflow performs these steps: 

- Instantiates a parametric study from a Fluent session
- Reads the previously saved project ``- static_mixer_study.flprj``
- Saves the current project
- Saves the current project to a different file name
- Exports the current project
- Archives the current project
- Exits the parametric project-based workflow


"""

#########################################################################

# Parametric project workflow

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
proj_path_read = str(Path(pyfluent.EXAMPLES_PATH) / "static_mixer_study.flprj")

proj = ParametricProject(
    root.file.parametric_project,
    root.parametric_studies,
    proj_path_read
)

#########################################################################

# Save the current project
proj.save()

#########################################################################

# Save the current project to a different file name

proj_path_sa = str(
    Path(pyfluent.EXAMPLES_PATH) / "static_mixer_study_save_as.flprj"
)
proj.save_as(project_filepath=proj_path_sa)

#########################################################################

# Export the current project
proj_path_exp = str(
    Path(pyfluent.EXAMPLES_PATH) / "static_mixer_study_export.flprj"
)
proj.export(project_filepath=proj_path_exp)
