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

"""Provides a module for launching utilities."""

import logging
import os
from pathlib import Path
import platform
import shutil
import socket
import subprocess
import sys
import time
from typing import Any
import warnings

from ansys.fluent.core.exceptions import InvalidArgument
from ansys.fluent.core.pyfluent_warnings import PyFluentDeprecationWarning
from ansys.fluent.core.utils.networking import find_remoting_ip

logger = logging.getLogger("pyfluent.launcher")


class ComposeConfig:
    """Configuration for Docker or Podman Compose usage in PyFluent."""

    def __init__(
        self,
        use_docker_compose: bool | None = None,
        use_podman_compose: bool | None = None,
    ):
        from ansys.fluent.core.module_config import config

        self._env_docker = config.use_docker_compose
        self._env_podman = config.use_podman_compose

        self._use_docker = use_docker_compose
        self._use_podman = use_podman_compose

        if use_docker_compose is None and self._env_docker:
            self._warn_env_deprecated()
        if use_podman_compose is None and self._env_podman:
            self._warn_env_deprecated()

    def _warn_env_deprecated(self):
        warnings.warn(
            (
                "The environment variables 'PYFLUENT_USE_DOCKER_COMPOSE' and "
                "'PYFLUENT_USE_PODMAN_COMPOSE' are deprecated. "
                "Use the 'use_docker_compose' and 'use_podman_compose' parameters instead."
            ),
            category=PyFluentDeprecationWarning,
            stacklevel=3,
        )

    @property
    def use_docker_compose(self) -> bool:
        """Check if Docker Compose is configured to be used."""
        return self._use_docker if self._use_docker is not None else self._env_docker

    @property
    def use_podman_compose(self) -> bool:
        """Check if Podman Compose is configured to be used."""
        return self._use_podman if self._use_podman is not None else self._env_podman

    @property
    def is_compose(self) -> bool:
        """Check if either Docker Compose or Podman Compose is configured to be used."""
        return self.use_docker_compose or self.use_podman_compose


def is_windows():
    """Check if the current operating system is Windows."""
    return platform.system() == "Windows"


def _get_subprocess_kwargs_for_fluent(env: dict[str, Any], argvals) -> dict[str, Any]:
    import ansys.fluent.core as pyfluent

    scheduler_options = argvals.get("scheduler_options")
    is_slurm = scheduler_options and scheduler_options["scheduler"] == "slurm"
    kwargs: dict[str, Any] = {}
    if is_slurm:
        kwargs.update(stdout=subprocess.PIPE)
    else:
        kwargs.update(
            stdout=pyfluent.config.launch_fluent_stdout,
            stderr=pyfluent.config.launch_fluent_stderr,
        )
    if is_windows():
        kwargs.update(
            shell=True,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            | subprocess.CREATE_NO_WINDOW,
        )
    else:
        kwargs.update(shell=True, start_new_session=True)
    fluent_env = os.environ.copy()
    if env:
        fluent_env.update({k: str(v) for k, v in env.items()})
    fluent_env["REMOTING_THROW_LAST_TUI_ERROR"] = "1"
    fluent_env["REMOTING_THROW_LAST_SETTINGS_ERROR"] = "1"
    if pyfluent.config.clear_fluent_para_envs:
        fluent_env.pop("PARA_NPROCS", None)
        fluent_env.pop("PARA_MESH_NPROCS", None)

    if pyfluent.config.launch_fluent_ip:
        fluent_env["REMOTING_SERVER_ADDRESS"] = pyfluent.config.launch_fluent_ip

    if pyfluent.config.launch_fluent_port:
        fluent_env["REMOTING_PORTS"] = (
            f"{pyfluent.config.launch_fluent_port}/portspan=2"
        )

    if pyfluent.config.launch_fluent_skip_password_check:
        fluent_env["FLUENT_LAUNCHED_FROM_PYFLUENT"] = "1"

    if not is_slurm:
        if (
            pyfluent.config.infer_remoting_ip
            and "REMOTING_SERVER_ADDRESS" not in fluent_env
        ):
            remoting_ip = find_remoting_ip()
            if remoting_ip:
                fluent_env["REMOTING_SERVER_ADDRESS"] = remoting_ip

    if not pyfluent.config.fluent_automatic_transcript:
        fluent_env["FLUENT_NO_AUTOMATIC_TRANSCRIPT"] = "1"

    kwargs.update(env=fluent_env)
    return kwargs


def _get_app_data_root() -> Path:
    if sys.platform == "win32":
        return Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support"
    if sys.platform.startswith(("linux", "freebsd", "openbsd")):
        return Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return Path.home() / ".config"


def _update_server_info_file(server_info_file_name: str, pid: int | None = None):
    try:
        servers_dir = _get_app_data_root() / "pyfluent" / "servers"
        servers_dir.mkdir(parents=True, exist_ok=True)
        si_file = servers_dir / Path(server_info_file_name).name
        shutil.copy2(server_info_file_name, si_file)
        if pid is not None:
            with open(si_file, "a", encoding="utf-8") as f:
                f.write(f"\n{pid}")
    except PermissionError:
        logger.warning("Insufficient permissions to update server info file. Skipping.")


def _await_fluent_launch(
    server_info_file_name: str,
    start_timeout: int,
    sifile_last_mtime: float,
    pid: int | None = None,
):
    """Wait for successful fluent launch or raise an error."""
    while True:
        if Path(server_info_file_name).stat().st_mtime > sifile_last_mtime:
            time.sleep(1)
            logger.info("Fluent has been successfully launched.")
            _update_server_info_file(server_info_file_name, pid)
            break
        if start_timeout == 0:
            raise TimeoutError("The launch process has timed out.")
        time.sleep(1)
        start_timeout -= 1
        logger.info("Waiting for Fluent to launch...")
        if start_timeout >= 0:
            logger.info(f"...{start_timeout} seconds remaining")


def _confirm_watchdog_start(start_watchdog, cleanup_on_exit, fluent_connection):
    """Confirm whether Fluent is running locally, and whether the Watchdog should be
    started."""
    if start_watchdog is None and cleanup_on_exit:
        host = fluent_connection.connection_properties.cortex_host
        if host == socket.gethostname():
            logger.debug(
                "Fluent running on the host machine and 'cleanup_on_exit' activated, will launch Watchdog."
            )
            start_watchdog = True
    return start_watchdog


def _build_journal_argument(
    topy: None | bool | str, journal_file_names: None | str | list[str]
) -> str:
    """Build Fluent commandline journal argument."""

    def _impl(
        topy: None | bool | str, journal_file_names: None | str | list[str]
    ) -> str:
        if journal_file_names and not isinstance(journal_file_names, (str, list)):
            raise TypeError(
                "Use 'journal_file_names' to specify and convert journal files."
            )
        if topy and not journal_file_names:
            raise InvalidArgument(
                "Use 'journal_file_names' to specify and convert journal files."
            )
        fluent_jou_arg = ""
        if isinstance(journal_file_names, str):
            journal_file_names = [journal_file_names]
        if journal_file_names:
            fluent_jou_arg += "".join(
                [f' -i "{journal}"' for journal in journal_file_names]
            )
        if topy:
            if isinstance(topy, str):
                fluent_jou_arg += f' -topy="{topy}"'
            else:
                fluent_jou_arg += " -topy"
        return fluent_jou_arg

    return _impl(topy, journal_file_names)


def _read_journals(session, journal_file_names: None | str | list[str]) -> None:
    """Read one or more journal files into an already-connected session.

    This is used instead of the startup ``-i`` argument when a case file is
    also being read, so that the case is processed before the journal
    (see issue #4265).
    """
    if not journal_file_names:
        return
    if isinstance(journal_file_names, str):
        journal_file_names = [journal_file_names]
    for journal in journal_file_names:
        session.execute_tui(f'/file/read-journal "{journal}"')


def _validate_lightweight_with_journal(
    lightweight_mode: bool | None, journal_file_names: None | str | list[str]
) -> tuple[bool, str | None]:
    """Validate lightweight_mode and journal_file_names compatibility.

    Parameters
    ----------
    lightweight_mode : bool | None
        Whether lightweight mode is requested.
    journal_file_names : str | list[str] | None
        Path(s) to journal file(s).

    Returns
    -------
    tuple[bool, str | None]
        A tuple of (should_disable_lightweight, warning_message).
        - should_disable_lightweight: True if lightweight_mode should be disabled
        - warning_message: Warning message if incompatible combination detected, else None

    Notes
    -----
    lightweight_mode with journal_file_names is not supported because there is no
    consistent ordering for journals (run in foreground) vs. mesh loading (background).
    See issue #4265.
    """
    if lightweight_mode and journal_file_names:
        from ansys.fluent.core.launcher.error_warning_messages import (
            LIGHTWEIGHT_MODE_IGNORED_WITH_JOURNAL,
        )

        return True, LIGHTWEIGHT_MODE_IGNORED_WITH_JOURNAL
    return False, None


def _resolve_file_processing_strategy(
    case_file_name: str | None,
    journal_file_names: None | str | list[str],
    lightweight_mode: bool | None,
) -> dict[str, Any]:
    """Resolve file processing strategy based on case/journal/lightweight_mode combination.

    Implements the truth table for deciding which files are passed via CLI flags vs.
    post-connection processing, and whether lightweight mode is compatible.

    Parameters
    ----------
    case_file_name : str | None
        Case file name or path.
    journal_file_names : str | list[str] | None
        Journal file name(s) or path(s).
    lightweight_mode : bool | None
        Whether lightweight mode was requested.

    Returns
    -------
    dict[str, Any]
        Strategy dictionary with keys:
        - 'use_cli_case': bool - Pass -case/-data to Fluent CLI
        - 'use_cli_journal': bool - Pass -i to Fluent CLI
        - 'enable_lightweight': bool - Launch background session for lightweight mode
        - 'warning': str | None - Warning message for user, if any

    Truth Table (case | journal | lightweight):
    - F | F | F → No-op
    - F | F | T → Warn & disable, no-op
    - F | T | F → Pass -i to Fluent
    - F | T | T → Warn & disable, pass -i
    - T | F | F → Pass -case/-data to Fluent
    - T | F | T → Keep fg/bg session (lightweight works without journal)
    - T | T | F → Pass -case/-data -i to Fluent
    - T | T | T → Warn & disable, pass -case/-data -i

    Notes
    -----
    The only case where post-connection processing is needed is T|F|T (lightweight mode
    with case file), which requires a background session launch that only happens
    post-connection in the standalone launcher.
    """
    has_case = bool(case_file_name)
    has_journal = bool(journal_file_names)

    strategy: dict[str, Any] = {
        "use_cli_case": False,
        "use_cli_journal": False,
        "enable_lightweight": False,
        "warning": None,
    }

    # Check for incompatible lightweight_mode + journal combination
    should_disable, warning_msg = _validate_lightweight_with_journal(
        lightweight_mode, journal_file_names
    )

    if should_disable:
        strategy["warning"] = warning_msg
        lightweight_mode = False

    # Apply truth table logic
    if not has_case and not has_journal:
        # F|F|* → No-op
        pass
    elif not has_case and has_journal:
        # F|T|* → Pass -i to Fluent
        strategy["use_cli_journal"] = True
    elif has_case and not has_journal:
        if lightweight_mode:
            # T|F|T → Keep fg/bg session (post-connection processing needed)
            strategy["enable_lightweight"] = True
        else:
            # T|F|F → Pass -case/-data to Fluent
            strategy["use_cli_case"] = True
    else:  # has_case and has_journal
        # T|T|* → Pass both -case/-data and -i to Fluent
        strategy["use_cli_case"] = True
        strategy["use_cli_journal"] = True

    return strategy


def _build_case_data_arguments(
    case_file_name: str | None = None,
    case_data_file_name: str | None = None,
) -> str:
    """Build Fluent command-line arguments for case and data files.

    Parameters
    ----------
    case_file_name : str | None
        Name of the case file to pass via -case flag.
    case_data_file_name : str | None
        Name of the case data file to pass via -data flag.

    Returns
    -------
    str
        Formatted command-line arguments.
        Examples:
        - '' (empty string if neither provided)
        - '-case "x.cas.h5"'
        - '-case "x.cas.h5" -data "x.dat"'
        - '-data "x.dat"'

    """
    args = ""
    if case_file_name:
        args += f' -case "{case_file_name}"'
    if case_data_file_name:
        args += f' -data "{case_data_file_name}"'
    return args
