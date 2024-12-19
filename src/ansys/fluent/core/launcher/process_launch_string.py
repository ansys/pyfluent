"""Provides a module to process launch string."""

import json
import os
from pathlib import Path

import ansys.fluent.core as pyfluent
from ansys.fluent.core.launcher import launcher_utils
from ansys.fluent.core.launcher.pyfluent_enums import (
    Dimension,
    FluentMode,
    Precision,
    UIMode,
)
from ansys.fluent.core.scheduler import build_parallel_options, load_machines
from ansys.fluent.core.utils.fluent_version import FluentVersion

_THIS_DIR = os.path.dirname(__file__)
_OPTIONS_FILE = os.path.join(_THIS_DIR, "fluent_launcher_options.json")


def _build_fluent_launch_args_string(**kwargs) -> str:
    """Build Fluent's launch arguments string from keyword arguments.

    Returns
    -------
    str
        Fluent's launch arguments string.
    """
    all_options = None
    with open(_OPTIONS_FILE, encoding="utf-8") as fp:
        all_options = json.load(fp)
    launch_args_string = ""
    dimension = Dimension(kwargs.get("dimension"))
    launch_args_string += f" {dimension.get_fluent_value()[0]}"
    precision = Precision(kwargs.get("precision"))
    launch_args_string += f"{precision.get_fluent_value()[0]}"
    for k, v in all_options.items():
        argval = kwargs.get(k)
        default = v.get("default")
        if argval is None and v.get("fluent_required") is True:
            argval = default
        if argval is not None:
            allowed_values = v.get("allowed_values")
            if allowed_values and argval not in allowed_values:
                if default is not None:
                    old_argval = argval
                    argval = default
                    launcher_utils.logger.warning(
                        f"Specified value '{old_argval}' for argument '{k}' is not an allowed value ({allowed_values})."
                        f" Default value '{argval}' is going to be used instead."
                    )
                else:
                    launcher_utils.logger.warning(
                        f"{k} = {argval} is discarded as it is not an allowed value. Allowed values: {allowed_values}"
                    )
                    continue
            fluent_map = v.get("fluent_map")
            if fluent_map:
                if isinstance(argval, str):
                    json_key = argval
                else:
                    json_key = json.dumps(argval)
                argval = fluent_map[json_key]
            launch_args_string += v["fluent_format"].replace("{}", str(argval))
    additional_arguments = kwargs["additional_arguments"]
    if additional_arguments:
        launch_args_string += " " + additional_arguments
    if "-t" not in additional_arguments and "-cnf=" not in additional_arguments:
        parallel_options = build_parallel_options(
            load_machines(ncores=kwargs["processor_count"])
        )
        if parallel_options:
            launch_args_string += " " + parallel_options
    gpu = kwargs.get("gpu")
    if gpu is True:
        launch_args_string += " -gpu"
    elif isinstance(gpu, list):
        launch_args_string += f" -gpu={','.join(map(str, gpu))}"
    ui_mode = UIMode(kwargs.get("ui_mode"))
    if ui_mode and ui_mode.get_fluent_value()[0]:
        launch_args_string += f" -{ui_mode.get_fluent_value()[0]}"
    graphics_driver = kwargs.get("graphics_driver")
    if graphics_driver and graphics_driver.get_fluent_value()[0]:
        launch_args_string += f" -driver {graphics_driver.get_fluent_value()[0]}"
    return launch_args_string


def _generate_launch_string(
    argvals,
    server_info_file_name: str,
):
    """Generates the launch string to launch fluent."""
    if launcher_utils.is_windows():
        exe_path = str(get_fluent_exe_path(**argvals))
        if " " in exe_path:
            exe_path = '"' + exe_path + '"'
    else:
        exe_path = str(get_fluent_exe_path(**argvals))
    launch_string = exe_path
    launch_string += _build_fluent_launch_args_string(**argvals)
    if argvals["mode"] == FluentMode.SOLVER_ICING:
        launch_string += " -flicing -license=enterprise"
    if argvals["mode"] == FluentMode.SOLVER_AERO:
        launch_string += " -flaero_server -license=enterprise"
    if FluentMode.is_meshing(argvals["mode"]):
        launch_string += " -meshing"
    if " " in server_info_file_name:
        server_info_file_name = '"' + server_info_file_name + '"'
    launch_string += f" -sifile={server_info_file_name}"
    if not pyfluent.FLUENT_SHOW_MESH_AFTER_CASE_READ:
        launch_string += " -nm"
    return launch_string


def get_fluent_exe_path(**launch_argvals) -> Path:
    """Get the path for the Fluent executable file. The search for the path is performed
    in the following order.

    1. ``product_version`` parameter passed with the ``launch_fluent`` method.
    2. The latest Ansys version from ``AWP_ROOTnnn``` environment variables.

    Returns
    -------
    Path
        Fluent executable path
    """

    def get_fluent_root(version: FluentVersion) -> Path:
        awp_root = os.environ[version.awp_var]
        return Path(awp_root) / "fluent"

    def get_exe_path(fluent_root: Path) -> Path:
        if launcher_utils.is_windows():
            return fluent_root / "ntbin" / "win64" / "fluent.exe"
        else:
            return fluent_root / "bin" / "fluent"

    # Look for Fluent exe path in the following order:
    # 1. Custom Path provided by the user in launch_fluent
    fluent_path = launch_argvals.get("fluent_path")
    if fluent_path:
        # Return the fluent_path string verbatim. The path may not even exist
        # in the current machine if user wants to launch fluent externally (dry_run use case).
        return fluent_path

    # 2. product_version parameter passed with launch_fluent
    product_version = launch_argvals.get("product_version")
    if product_version:
        return get_exe_path(get_fluent_root(FluentVersion(product_version)))

    # (DEV) "PYFLUENT_FLUENT_ROOT" environment variable
    fluent_root = os.getenv("PYFLUENT_FLUENT_ROOT")
    if fluent_root:
        return get_exe_path(Path(fluent_root))

    # 3. the latest ANSYS version from AWP_ROOT environment variables
    return get_exe_path(get_fluent_root(FluentVersion.get_latest_installed()))
