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

    Each fragment preserves the leading space defined in ``fluent_format``
    (e.g. ``" -py"``). Callers can concatenate as-is for the shell string
    form, or split each fragment to produce individual list tokens.
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


def _normalize_additional_arguments(
    additional_arguments, shell: bool
) -> str | list[str]:
    """Validate and normalise the ``additional_arguments`` argument.

    When ``shell=True`` the value is returned as a string (defaults to
    ``""``). When ``shell=False`` a list of tokens is required and returned.
    """
    if not additional_arguments:
        return "" if shell else []
    if isinstance(additional_arguments, list):
        return additional_arguments
    if isinstance(additional_arguments, str):
        if not shell:
            raise TypeError(
                "'additional_arguments' must be a list of strings when 'shell=False'."
            )
        return additional_arguments
    raise TypeError("'additional_arguments' must be a string or a list of strings.")


def _parallel_options_string(kwargs) -> str:
    """Return Fluent's ``-t`` / ``-cnf=`` parallel options (may be empty)."""
    return build_parallel_options(load_machines(ncores=kwargs.get("processor_count")))


def _build_fluent_launch_args(shell: bool = True, **kwargs) -> str | list[str]:
    """Build Fluent's launch arguments in either shell string or token list form.

    The two branches share every helper that resolves option values; they
    differ only in whether they emit leading-space-prefixed fragments (shell
    string form) or standalone tokens (list form).
    """
    additional_arguments = _normalize_additional_arguments(
        kwargs.get("additional_arguments"), shell
    )
    dp_flag = _dimension_precision_flag(kwargs)
    gpu_tokens = _gpu_tokens(kwargs.get("gpu"))
    ui_tokens = _ui_mode_tokens(kwargs.get("ui_mode"))
    driver_tokens = _graphics_driver_tokens(kwargs.get("graphics_driver"))
    joined_additional = (
        additional_arguments
        if isinstance(additional_arguments, str)
        else " ".join(additional_arguments)
    )
    need_parallel = "-t" not in joined_additional and "-cnf=" not in joined_additional
    parallel_options = _parallel_options_string(kwargs) if need_parallel else ""

    if shell:
        # Byte-identical to the historical hand-written string form. Every
        # fragment already carries its own leading space.
        launch_args = f" {dp_flag}"
        for fragment in _iter_option_fragments(kwargs):
            launch_args += fragment
        if additional_arguments:
            launch_args += " " + additional_arguments
        if parallel_options:
            launch_args += " " + parallel_options
        for token in gpu_tokens + ui_tokens:
            launch_args += f" {token}"
        if driver_tokens:
            launch_args += " " + " ".join(driver_tokens)
        return launch_args

    tokens: list[str] = [dp_flag]
    # Each JSON-defined option formats to a whitespace-separated fragment;
    # split so every CLI flag is its own token.
    for fragment in _iter_option_fragments(kwargs):
        tokens.extend(fragment.split())
    tokens.extend(additional_arguments)
    if parallel_options:
        tokens.extend(parallel_options.strip().split())
    tokens.extend(gpu_tokens)
    tokens.extend(ui_tokens)
    tokens.extend(driver_tokens)
    return tokens


def _build_fluent_launch_args_string(**kwargs) -> str:
    """Build Fluent's launch arguments as a shell string (compatibility wrapper)."""
    return _build_fluent_launch_args(shell=True, **kwargs)


def _build_fluent_launch_args_list(**kwargs) -> list[str]:
    """Build Fluent's launch arguments as a list of tokens (compatibility wrapper)."""
    return _build_fluent_launch_args(shell=False, **kwargs)


def _mode_extra_args(mode, shell: bool) -> str | list[str]:
    """Return the mode-specific CLI flags for ``mode`` (may be empty)."""
    if mode == FluentMode.SOLVER_ICING:
        return (
            " -flicing -license=enterprise"
            if shell
            else ["-flicing", "-license=enterprise"]
        )
    if mode == FluentMode.SOLVER_AERO:
        return (
            " -flaero_server -license=enterprise"
            if shell
            else ["-flaero_server", "-license=enterprise"]
        )
    if mode == FluentMode.PRE_POST:
        return " -post" if shell else ["-post"]
    if FluentMode.is_meshing(mode):
        return " -meshing" if shell else ["-meshing"]
    return "" if shell else []


def _generate_launch_command(
    argvals, server_info_file_name: str, shell: bool = True
) -> str | list[str]:
    """Generate the Fluent launch command as either a shell string or token list.

    The shell-string form is byte-identical to the original hand-crafted
    string (including the exe/``-sifile`` path quoting rules), so callers
    that construct shell commands continue to see the exact same output.
    """
    exe_path = str(get_fluent_exe_path(**argvals))
    # ``argvals`` already carries a ``shell`` key that we control here;
    # drop it so the explicit ``shell=`` isn't a duplicate keyword.
    args_kwargs = {k: v for k, v in argvals.items() if k != "shell"}
    args = _build_fluent_launch_args(shell=shell, **args_kwargs)
    mode_extra = _mode_extra_args(argvals["mode"], shell)

    if shell:
        # On Windows, quote the exe path only if it contains a space; the
        # ``-sifile`` path is quoted under the same rule.
        if launcher_utils.is_windows() and " " in exe_path:
            exe_path = f'"{exe_path}"'
        sifile = server_info_file_name
        if " " in sifile:
            sifile = f'"{sifile}"'
        launch_string = exe_path + args + mode_extra + f" -sifile={sifile}"
        if not pyfluent.config.fluent_show_mesh_after_case_read:
            launch_string += " -nm"
        return launch_string

    tokens: list[str] = [exe_path]
    tokens.extend(args)
    tokens.extend(mode_extra)
    tokens.append(f"-sifile={server_info_file_name}")
    if not pyfluent.config.fluent_show_mesh_after_case_read:
        tokens.append("-nm")
    return tokens


def _generate_launch_string(argvals, server_info_file_name: str) -> str:
    """Generate the Fluent launch command as a shell string (compatibility wrapper)."""
    return _generate_launch_command(argvals, server_info_file_name, shell=True)


def _generate_launch_command_list(argvals, server_info_file_name: str) -> list[str]:
    """Generate the Fluent launch command as a token list (compatibility wrapper)."""
    return _generate_launch_command(argvals, server_info_file_name, shell=False)


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
