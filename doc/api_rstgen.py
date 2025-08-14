"""Provides a module for generating PyFluent API RST files."""

import os
from pathlib import Path
import shutil

from ansys.fluent.core import FluentVersion

api_contents_path = (
    Path(__file__).parents[0].resolve() / "source" / "api" / "api_contents.rst"
)
fluent_version = FluentVersion.current_release()


def _write_rst_file(output_path: str, version: str):
    content = f""".. _ref_api:

API reference
=============

This API reference corresponds to {version}. PyFluent maintains strong backward compatibility guarantees, so scripts targeting older Ansys versions are expected to work without modification.

This is PyFluent's class and function reference. Please refer to the :ref:`ref_user_guide` for
full guidelines on their use.

All the public APIs for PyFluent are listed in the left hand margin. Some key APIs are mentioned below:

Meshing mode
------------

The following interfaces are specific to meshing mode.

* :ref:`meshing <ref_meshing_datamodel_meshing>`
* :ref:`PartManagement <ref_meshing_datamodel_part_management>`
* :ref:`PMFileManagement <ref_meshing_datamodel_pm_file_management>`
* :ref:`workflow <ref_meshing_datamodel_workflow>`
* :ref:`meshing utilities <ref_meshing_datamodel_meshing_utilities>`

Solution mode
-------------

The solver :ref:`settings API <ref_root>` is the main interface for controlling and running the solver.


.. toctree::
    :maxdepth: 2
    :hidden:
    :caption: ansys.fluent.core

    docker/docker_contents
    filereader/filereader_contents
    launcher/launcher_contents
    meshing/meshing_contents
    scheduler/scheduler_contents
    services/services_contents
    solver/solver_contents
    streaming_services/streaming_services_contents
    utils/utils_contents
    data_model_cache
    exceptions
    file_session
    field_data_interfaces
    fluent_connection
    journaling
    logger
    module_config
    parametric
    rpvars
    search
    session_base_meshing
    session_meshing
    session_pure_meshing
    session_solver_icing
    session_solver_lite
    session_solver
    session
    session_utilities
    system_coupling
    pyfluent_warnings
    workflow
    deprecated_apis
"""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)


def _get_folder_path(folder_name: str):
    """Get folder path.

    Parameters
    ----------
    folder_name: str
        Name of the folder.

    Returns
    -------
        Path of the folder.
    """
    return (Path(__file__) / ".." / "source" / "api" / folder_name).resolve()


def _get_file_path(folder_name: str, file_name: str):
    """Get file path.

    Parameters
    ----------
    folder_name: str
        Name of the folder.

    file_name: str
        Name of the file.

    Returns
    -------
        Path of the file.
    """
    return (
        Path(__file__) / ".." / "source" / "api" / folder_name / f"{file_name}.rst"
    ).resolve()


hierarchy = {
    "docker": ["docker_compose"],
    "filereader": ["case_file", "data_file", "lispy"],
    "launcher": [
        "container_launcher",
        "error_handler",
        "fluent_container",
        "launcher_utils",
        "launcher",
        "pim_launcher",
        "process_launch_string",
        "launch_options",
        "slurm_launcher",
        "standalone_launcher",
        "watchdog",
    ],
    "meshing": ["meshing_workflow", "datamodel/datamodel_contents", "tui/tui_contents"],
    "scheduler": ["load_machines", "machine_list"],
    "services": [
        "api_upgrade",
        "batch_ops",
        "datamodel_se",
        "datamodel_tui",
        "events",
        "field_data",
        "health_check",
        "interceptors",
        "monitor",
        "reduction",
        "scheme_eval",
        "settings",
        "solution_variables",
        "streaming",
        "transcript",
    ],
    "solver": [
        "error_message",
        "flobject",
        "datamodel/datamodel_contents",
        "settings_root",
        "tui/tui_contents",
    ],
    "streaming_services": [
        "datamodel_event_streaming",
        "datamodel_streaming",
        "events_streaming",
        "field_data_streaming",
        "monitor_streaming",
        "streaming",
        "transcript_streaming",
    ],
    "utils": [
        "data_transfer",
        "deprecate",
        "dictionary_operations",
        "dump_session_data",
        "event_loop",
        "execution",
        "file_transfer_service",
        "fix_doc",
        "fldoc",
        "fluent_version",
        "networking",
        "setup_for_fluent",
    ],
    "other": [
        "module_config",
        "exceptions",
        "file_session",
        "field_data_interfaces",
        "fluent_connection",
        "journaling",
        "logger",
        "parametric",
        "rpvars",
        "search",
        "session_base_meshing",
        "session_meshing",
        "session_pure_meshing",
        "session_solver_icing",
        "session_solver_lite",
        "session_solver",
        "session_utilities",
        "session",
        "system_coupling",
        "pyfluent_warnings",
        "workflow",
    ],
}


def _write_common_rst_members(rst_file):
    rst_file.write("    :members:\n")
    rst_file.write("    :show-inheritance:\n")
    rst_file.write("    :undoc-members:\n")
    rst_file.write("    :exclude-members: __weakref__, __dict__\n")
    rst_file.write("    :special-members: __init__\n")
    rst_file.write("    :autosummary:\n")


def _generate_api_source_rst_files(folder: str, files: list):
    for file in files:
        if file.endswith("_contents"):
            pass
        else:
            if folder:
                rst_file = _get_file_path(folder, file)
            else:
                rst_file = _get_file_path("", file)
            with open(rst_file, "w", encoding="utf8") as rst:
                rst.write(f".. _ref_{file}:\n\n")
                if folder:
                    if "root" in file:
                        rst.write("solver.settings\n")
                        rst.write(f'{"="*(len("solver.settings"))}\n\n')
                        rst.write(
                            "The :ref:`ref_root` is the top-level solver settings object. It contains all\n"
                        )
                        rst.write(
                            "other settings objects in a hierarchical structure.\n"
                        )
                    else:
                        rst.write(f"{file}\n")
                        rst.write(f'{"="*(len(f"{file}"))}\n\n')
                        rst.write(
                            f".. automodule:: ansys.fluent.core.{folder}.{file}\n"
                        )
                else:
                    rst.write(f"{file}\n")
                    rst.write(f'{"="*(len(f"{file}"))}\n\n')
                    rst.write(f".. automodule:: ansys.fluent.core.{file}\n")
                if "root" not in file:
                    _write_common_rst_members(rst_file=rst)


def _generate_api_index_rst_files():
    for folder, files in hierarchy.items():
        if Path(_get_folder_path(folder)).is_dir():
            shutil.rmtree(_get_folder_path(folder))
        if folder == "other":
            _generate_api_source_rst_files(None, files)
        else:
            Path(_get_folder_path(folder)).mkdir(parents=True, exist_ok=True)
            folder_index = _get_file_path(folder, f"{folder}_contents")
            with open(folder_index, "w", encoding="utf8") as index:
                index.write(f".. _ref_{folder}:\n\n")
                index.write(f"{folder}\n")
                index.write(f'{"="*(len(f"{folder}"))}\n\n')
                index.write(f".. automodule:: ansys.fluent.core.{folder}\n")
                _write_common_rst_members(rst_file=index)
                index.write(".. toctree::\n")
                index.write("    :maxdepth: 2\n")
                index.write("    :hidden:\n\n")
                for file in files:
                    index.write(f"    {file}\n")
                index.write("\n")
            _generate_api_source_rst_files(folder, files)


if __name__ == "__main__":
    _write_rst_file(api_contents_path, fluent_version)
    _generate_api_index_rst_files()
