# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
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
import socket
import subprocess
import time
from typing import Any, Dict

from ansys.fluent.core.exceptions import InvalidArgument
from ansys.fluent.core.utils.networking import find_remoting_ip

logger = logging.getLogger("pyfluent.launcher")


def is_windows():
    """Check if the current operating system is Windows."""
    return platform.system() == "Windows"


def _get_subprocess_kwargs_for_fluent(env: Dict[str, Any], argvals) -> Dict[str, Any]:
    import ansys.fluent.core as pyfluent

    scheduler_options = argvals.get("scheduler_options")
    is_slurm = scheduler_options and scheduler_options["scheduler"] == "slurm"
    kwargs: Dict[str, Any] = {}
    if is_slurm:
        kwargs.update(stdout=subprocess.PIPE)
    else:
        kwargs.update(
            stdout=pyfluent.LAUNCH_FLUENT_STDOUT, stderr=pyfluent.LAUNCH_FLUENT_STDERR
        )
    if is_windows():
        kwargs.update(shell=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    else:
        kwargs.update(shell=True, start_new_session=True)
    fluent_env = os.environ.copy()
    fluent_env.update({k: str(v) for k, v in env.items()})
    fluent_env["REMOTING_THROW_LAST_TUI_ERROR"] = "1"
    fluent_env["REMOTING_THROW_LAST_SETTINGS_ERROR"] = "1"
    if pyfluent.CLEAR_FLUENT_PARA_ENVS:
        fluent_env.pop("PARA_NPROCS", None)
        fluent_env.pop("PARA_MESH_NPROCS", None)

    if pyfluent.LAUNCH_FLUENT_IP:
        fluent_env["REMOTING_SERVER_ADDRESS"] = pyfluent.LAUNCH_FLUENT_IP

    if pyfluent.LAUNCH_FLUENT_PORT:
        fluent_env["REMOTING_PORTS"] = f"{pyfluent.LAUNCH_FLUENT_PORT}/portspan=2"

    if pyfluent.LAUNCH_FLUENT_SKIP_PASSWORD_CHECK:
        fluent_env["FLUENT_LAUNCHED_FROM_PYFLUENT"] = "1"

    if not is_slurm:
        if pyfluent.INFER_REMOTING_IP and "REMOTING_SERVER_ADDRESS" not in fluent_env:
            remoting_ip = find_remoting_ip()
            if remoting_ip:
                fluent_env["REMOTING_SERVER_ADDRESS"] = remoting_ip

    if not pyfluent.FLUENT_AUTOMATIC_TRANSCRIPT:
        fluent_env["FLUENT_NO_AUTOMATIC_TRANSCRIPT"] = "1"

    kwargs.update(env=fluent_env)
    return kwargs


def _await_fluent_launch(
    server_info_file_name: str, start_timeout: int, sifile_last_mtime: float
):
    """Wait for successful fluent launch or raise an error."""
    while True:
        if Path(server_info_file_name).stat().st_mtime > sifile_last_mtime:
            time.sleep(1)
            logger.info("Fluent has been successfully launched.")
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
