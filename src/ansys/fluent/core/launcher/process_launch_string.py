# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Provides a module to process launch string."""

from collections.abc import Iterator
import json
import os
from pathlib import Path
from typing import Any

import ansys.fluent.core as pyfluent
from ansys.fluent.core.launcher import launcher_utils
from ansys.fluent.core.launcher.launch_options import (
    Dimension,
    FluentMode,
    Precision,
    UIMode,
)
from ansys.fluent.core.scheduler import build_parallel_options, load_machines
from ansys.fluent.core.utils.fluent_version import FluentVersion

_THIS_DIR = os.path.dirname(__file__)
_OPTIONS_FILE = os.path.join(_THIS_DIR, "fluent_launcher_options.json")


def _load_launcher_options() -> dict[str, dict[str, Any]]:
    """Load the JSON-defined Fluent launcher options."""
    with open(_OPTIONS_FILE, encoding="utf-8") as fp:
        return json.load(fp)


def _dimension_precision_flag(kwargs) -> str:
    """Return the combined dimension + precision Fluent flag (e.g. ``3ddp``)."""
    dimension = Dimension(kwargs.get("dimension"))
    precision = Precision(kwargs.get("precision"))
    return f"{dimension.get_fluent_value()[0]}{precision.get_fluent_value()[0]}"


def _resolve_option_argval(
    name: str, argval: Any, option_spec: dict[str, Any]
) -> Any | None:
    """Apply ``allowed_values`` / default fallback to an option value.

    Returns ``None`` when the option should be skipped entirely.
    """
    default = option_spec.get("default")
    if argval is None and option_spec.get("fluent_required") is True:
        argval = default
    if argval is None:
        return None
    allowed_values = option_spec.get("allowed_values")
    if allowed_values and argval not in allowed_values:
        if default is None:
            launcher_utils.logger.warning(
                f"{name} = {argval} is discarded as it is not an allowed value."
                f" Allowed values: {allowed_values}"
            )
            return None
        launcher_utils.logger.warning(
            f"Specified value '{argval}' for argument '{name}' is not an allowed"
            f" value ({allowed_values}). Default value '{default}' is going to"
            " be used instead."
        )
        argval = default
    return argval


def _apply_fluent_map(argval: Any, option_spec: dict[str, Any]) -> Any:
    """Translate ``argval`` through the option's ``fluent_map`` if present."""
    fluent_map = option_spec.get("fluent_map")
    if not fluent_map:
        return argval
    json_key = argval if isinstance(argval, str) else json.dumps(argval)
    return fluent_map[json_key]


def _iter_option_fragments(kwargs) -> Iterator[str]:
    """Yield the formatted fragment for each JSON-defined launcher option.

    The fragment preserves the leading space defined in ``fluent_format``
    (e.g. ``" -py"``). Callers can concatenate as-is for a shell string, or
    strip+split each fragment to produce individual tokens.
    """
    for name, spec in _load_launcher_options().items():
        argval = _resolve_option_argval(name, kwargs.get(name), spec)
        if argval is None:
            continue
        argval = _apply_fluent_map(argval, spec)
        yield spec["fluent_format"].replace("{}", str(argval))


def _gpu_tokens(gpu) -> list[str]:
    """Return the ``-gpu`` tokens (empty when the GPU solver is not requested)."""
    if gpu is True:
        return ["-gpu"]
    if isinstance(gpu, list):
        return [f"-gpu={','.join(map(str, gpu))}"]
    return []


def _ui_mode_tokens(ui_mode_arg) -> list[str]:
    """Return the UI-mode flag token (empty when no explicit flag is required)."""
    ui_mode = UIMode(ui_mode_arg)
    flag = ui_mode.get_fluent_value()[0] if ui_mode else None
    return [f"-{flag}"] if flag else []


def _graphics_driver_tokens(graphics_driver) -> list[str]:
    """Return the ``-driver <value>`` tokens (empty when the driver flag is empty)."""
    if not graphics_driver:
        return []
    value = graphics_driver.get_fluent_value()[0]
    return ["-driver", value] if value else []


def _validate_additional_arguments_list(additional_arguments) -> list[str]:
    """Validate and normalize ``additional_arguments`` for ``shell=False``."""
    if not additional_arguments:
        return []
    if isinstance(additional_arguments, str):
        raise TypeError(
            "'additional_arguments' must be a list of strings when 'shell=False'."
        )
    return list(additional_arguments)


def _parallel_tokens(joined_additional: str, kwargs) -> list[str]:
    """Return parallel (``-t`` / ``-cnf=``) tokens when not already supplied."""
    if "-t" in joined_additional or "-cnf=" in joined_additional:
        return []
    parallel_options = build_parallel_options(
        load_machines(ncores=kwargs.get("processor_count"))
    )
    return parallel_options.strip().split() if parallel_options else []


def _build_fluent_launch_args_string(**kwargs) -> str:
    """Build Fluent's launch arguments string from keyword arguments.

    Returns
    -------
    str
        Fluent's launch arguments string.
    """
    launch_args_string = f" {_dimension_precision_flag(kwargs)}"
    for fragment in _iter_option_fragments(kwargs):
        launch_args_string += fragment
    additional_arguments = kwargs.get("additional_arguments", "")
    if additional_arguments:
        launch_args_string += " " + additional_arguments
    if "-t" not in additional_arguments and "-cnf=" not in additional_arguments:
        parallel_options = build_parallel_options(
            load_machines(ncores=kwargs.get("processor_count"))
        )
        if parallel_options:
            launch_args_string += " " + parallel_options
    for token in _gpu_tokens(kwargs.get("gpu")):
        launch_args_string += f" {token}"
    for token in _ui_mode_tokens(kwargs.get("ui_mode")):
        launch_args_string += f" {token}"
    driver_tokens = _graphics_driver_tokens(kwargs.get("graphics_driver"))
    if driver_tokens:
        launch_args_string += " " + " ".join(driver_tokens)
    return launch_args_string


def _build_fluent_launch_args_list(**kwargs) -> list[str]:
    """Build Fluent's launch arguments as a list of tokens (for ``shell=False``).

    ``additional_arguments`` must be a list of individual command-line tokens
    (never a single space-separated string) so that ``subprocess.Popen`` can
    forward them verbatim without shell parsing.

    Returns
    -------
    list[str]
        Fluent's launch arguments as a list of tokens.
    """
    additional_arguments = _validate_additional_arguments_list(
        kwargs.get("additional_arguments")
    )
    tokens: list[str] = [_dimension_precision_flag(kwargs)]
    # Each JSON-defined option formats to a whitespace-separated fragment;
    # split it so every CLI flag is its own token.
    for fragment in _iter_option_fragments(kwargs):
        tokens.extend(fragment.split())
    tokens.extend(additional_arguments)
    tokens.extend(_parallel_tokens(" ".join(additional_arguments), kwargs))
    tokens.extend(_gpu_tokens(kwargs.get("gpu")))
    tokens.extend(_ui_mode_tokens(kwargs.get("ui_mode")))
    tokens.extend(_graphics_driver_tokens(kwargs.get("graphics_driver")))
    return tokens


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
    if argvals["mode"] == FluentMode.PRE_POST:
        launch_string += " -post"
    if FluentMode.is_meshing(argvals["mode"]):
        launch_string += " -meshing"
    if " " in server_info_file_name:
        server_info_file_name = '"' + server_info_file_name + '"'
    launch_string += f" -sifile={server_info_file_name}"
    if not pyfluent.config.fluent_show_mesh_after_case_read:
        launch_string += " -nm"
    return launch_string


def _generate_launch_command_list(
    argvals,
    server_info_file_name: str,
) -> list[str]:
    """Generate the launch command as a list of tokens (for ``shell=False``)."""
    exe_path = str(get_fluent_exe_path(**argvals))
    tokens: list[str] = [exe_path]
    tokens.extend(_build_fluent_launch_args_list(**argvals))
    if argvals["mode"] == FluentMode.SOLVER_ICING:
        tokens.extend(["-flicing", "-license=enterprise"])
    if argvals["mode"] == FluentMode.SOLVER_AERO:
        tokens.extend(["-flaero_server", "-license=enterprise"])
    if argvals["mode"] == FluentMode.PRE_POST:
        tokens.append("-post")
    if FluentMode.is_meshing(argvals["mode"]):
        tokens.append("-meshing")
    tokens.append(f"-sifile={server_info_file_name}")
    if not pyfluent.config.fluent_show_mesh_after_case_read:
        tokens.append("-nm")
    return tokens


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
        return FluentVersion(product_version)._get_fluent_exe_path()

    # (DEV) "PYFLUENT_FLUENT_ROOT" environment variable
    fluent_root = os.getenv("PYFLUENT_FLUENT_ROOT")
    if fluent_root:
        return get_exe_path(Path(fluent_root))

    # 3. the latest ANSYS version from AWP_ROOT environment variables
    return FluentVersion.get_latest_installed().get_fluent_exe_path()
