""".. _ref_parametric_static_mixer_2:

Parametric Project-Based Workflow
----------------------------------------------------
This example for executing a parametric project-based workflow
performs these steps:

- Instantiates a parametric study from a Fluent session
- Reads the previously saved project ``- static_mixer_study.flprj``
- Saves the current project
- Saves the current project to a different file name
- Exports the current project
- Archives the current project
- Exits the parametric project-based workflow
"""

#########################################################################
from pathlib import Path

import ansys.fluent.core as pyfluent
from ansys.fluent.parametric import ParametricProject

#########################################################################
# Launch Fluent and enable the settings API (Beta)

session = pyfluent.launch_fluent(precision="double", processor_count=2)
root = session.get_settings_root()

#########################################################################
# Read the previously saved project - static_mixer_study.flprj

project_filepath_read = str(Path(pyfluent.EXAMPLES_PATH) / "static_mixer_study.flprj")

proj = ParametricProject(
    root.file.parametric_project,
    root.parametric_studies,
    project_filepath_read,
)

#########################################################################
# Save the current project

proj.save()

#########################################################################
# Save the current project to a different file name

project_filepath_save_as = str(
    Path(pyfluent.EXAMPLES_PATH) / "static_mixer_study_save_as.flprj"
)
proj.save_as(project_filepath=project_filepath_save_as)

#########################################################################
# Export the current project

project_filepath_export = str(
    Path(pyfluent.EXAMPLES_PATH) / "static_mixer_study_export.flprj"
)
proj.export(project_filepath=project_filepath_export)

#########################################################################
# Archive the current project

proj.archive()
