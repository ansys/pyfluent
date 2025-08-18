"""
Script to write field-level help info for Fluent meshing datamodels
Field-level help info will be written to field_level_help.csv in the current directory from Fluent
"""

from pathlib import Path

from ansys.fluent.core import FluentMode, launch_fluent

if __name__ == "__main__":
    Path("field_level_help.csv").unlink(missing_ok=True)
    meshing = launch_fluent(
        mode=FluentMode.MESHING, env={"FLUENT_GENERATE_FIELD_LEVEL_HELP_CSV": "1"}
    )
    for rules in ("workflow", "meshing", "PartManagement", "PMFileManagement"):
        meshing._datamodel_service_se.get_static_info(rules)
