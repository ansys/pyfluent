import json
import os

from ansys.fluent.core.launcher.launcher_utils import (
    _is_windows,
    get_fluent_exe_path,
    logger,
)
from ansys.fluent.core.launcher.pyfluent_enums import FluentMode
from ansys.fluent.core.scheduler import build_parallel_options, load_machines

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
                    logger.warning(
                        f"Specified value '{old_argval}' for argument '{k}' is not an allowed value ({allowed_values})."
                        f" Default value '{argval}' is going to be used instead."
                    )
                else:
                    logger.warning(
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
    addArgs = kwargs.get("additional_arguments")
    if addArgs and "-t" not in addArgs and "-cnf=" not in addArgs:
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
    ui = kwargs.get("ui")
    if ui and ui.value[0]:
        launch_args_string += f" -{ui.value[0]}"
    graphics_driver = kwargs.get("graphics_driver")
    if graphics_driver and graphics_driver.value[0]:
        launch_args_string += f" -driver {graphics_driver.value[0]}"
    return launch_args_string


def _generate_launch_string(
    argvals,
    mode: FluentMode,
    additional_arguments: str,
    server_info_file_name: str,
):
    """Generates the launch string to launch fluent."""
    if _is_windows():
        exe_path = str(get_fluent_exe_path(**argvals))
        if " " in exe_path:
            exe_path = '"' + exe_path + '"'
    else:
        exe_path = str(get_fluent_exe_path(**argvals))
    launch_string = exe_path
    if mode == FluentMode.SOLVER_ICING:
        argvals["fluent_icing"] = True
    launch_string += _build_fluent_launch_args_string(**argvals)
    if FluentMode.is_meshing(mode):
        launch_string += " -meshing"
    if additional_arguments:
        launch_string += f" {additional_arguments}"
    if " " in server_info_file_name:
        server_info_file_name = '"' + server_info_file_name + '"'
    launch_string += f" -sifile={server_info_file_name}"
    launch_string += " -nm"
    return launch_string
