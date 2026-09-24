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

from collections.abc import Iterable
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

from ansys.fluent.core.exceptions import InvalidArgument, PyFluentDeprecationWarning
from ansys.fluent.core.launcher.error_warning_messages import (
    LIGHTWEIGHT_MODE_IGNORED_WITH_CASE_DATA,
    LIGHTWEIGHT_MODE_IGNORED_WITH_JOURNAL,
)
from ansys.fluent.core.utils.networking import find_remoting_ip

logger = logging.getLogger("pyfluent.launcher")


class FluentLaunchCmdBuilder:
    """Build a Fluent launch command for a Python ``subprocess`` call.

    Accumulates command-line elements into either a shell string
    (``shell=True``) or a list of tokens (``shell=False``). The class does
    not add any quoting or spacing beyond what the caller supplies; each
    call site is expected to pass fragments that are already correctly
    formatted for the currently-selected mode.

    Functions that build a piece of the launch command (journal args, case/data
    args, ...) accept either a ``bool`` (to create a fresh builder) or an
    existing ``FluentLaunchCmdBuilder`` instance (to append onto a command
    that is already being assembled), and return ``builder.get_cmd()``::

        builder = FluentLaunchCmdBuilder(shell=True)
        _build_journal_argument(topy, journals, builder=builder)
        _build_case_data_arguments(case, data, builder=builder)
        cmd = builder.get_cmd()
    """

    def __init__(self, shell: bool) -> None:
        self._shell = shell
        # For shell mode we accumulate a single string. For list mode we
        # accumulate a list of tokens that will be passed as-is to
        # ``subprocess.Popen``.
        self._cmd: str | list[str] = "" if shell else []

    @property
    def shell(self) -> bool:
        """Whether this builder targets a shell string (True) or a token list (False)."""
        return self._shell

    def append(self, elem: str) -> "FluentLaunchCmdBuilder":
        """Append a single element.

        In shell mode ``elem`` is concatenated verbatim (the caller supplies
        any needed leading whitespace and quoting). In list mode ``elem``
        becomes a single token.
        """
        if self._shell:
            self._cmd += elem
        else:
            self._cmd.append(elem)
        return self

    def extend(self, elems: str | Iterable[str] | None) -> "FluentLaunchCmdBuilder":
        """Append multiple elements.

        - In shell mode: a ``str`` is concatenated verbatim; a non-string
          iterable has its items joined with a single space and concatenated
          (with a leading space).
        - In list mode: a ``str`` is added as a single token; a non-string
          iterable is extended token-by-token.

        ``None`` and empty inputs are no-ops.
        """
        if not elems:
            return self
        if self._shell:
            if isinstance(elems, str):
                self._cmd += elems
            else:
                self._cmd += " " + " ".join(elems)
        else:
            if isinstance(elems, str):
                self._cmd.append(elems)
            else:
                self._cmd.extend(elems)
        return self

    def get_cmd(self) -> str | list[str]:
        """Return the accumulated command in the form matching ``shell``."""
        return self._cmd if self._shell else list(self._cmd)

    @staticmethod
    def as_builder(
        builder: "FluentLaunchCmdBuilder | bool",
    ) -> "FluentLaunchCmdBuilder":
        """Return ``builder`` unchanged, or wrap a bare ``shell`` bool in a new instance."""
        if isinstance(builder, FluentLaunchCmdBuilder):
            return builder
        return FluentLaunchCmdBuilder(builder)


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
    shell = argvals.get("shell", True)
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
            shell=shell,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            | subprocess.CREATE_NO_WINDOW,
        )
    else:
        kwargs.update(shell=shell, start_new_session=True)
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
    topy: None | bool | str,
    journal_file_names: None | str | list[str],
    builder: "FluentLaunchCmdBuilder | bool" = True,
) -> str | list[str]:
    """Build Fluent's commandline journal argument.

    ``builder`` may be an existing :class:`FluentLaunchCmdBuilder` to append
    onto, or a bool selecting shell-string (``True``, default) vs token-list
    (``False``) output. Returns ``builder.get_cmd()``.
    """
    builder = FluentLaunchCmdBuilder.as_builder(builder)
    if journal_file_names and not isinstance(journal_file_names, (str, list)):
        raise TypeError(
            "Use 'journal_file_names' to specify and convert journal files."
        )
    if topy and not journal_file_names:
        raise InvalidArgument(
            "Use 'journal_file_names' to specify and convert journal files."
        )
    if isinstance(journal_file_names, str):
        journal_file_names = [journal_file_names]
    for journal in journal_file_names or []:
        if builder.shell:
            builder.append(f' -i "{journal}"')
        else:
            builder.extend(["-i", str(journal)])
    if topy:
        if builder.shell:
            builder.append(f' -topy="{topy}"' if isinstance(topy, str) else " -topy")
        else:
            builder.append(f"-topy={topy}" if isinstance(topy, str) else "-topy")
    return builder.get_cmd()


def _validate_lightweight_with_journal(
    lightweight_mode: bool | None, journal_file_names: None | str | list[str]
) -> tuple[bool, str | None]:
    """Validate that lightweight_mode and journal_file_names are not both provided.

    Parameters
    ----------
    lightweight_mode : bool | None
        Lightweight mode flag.
    journal_file_names : None | str | list[str]
        Journal file names.

    Returns
    -------
    tuple[bool, str | None]
        A tuple where:
        - First element (bool): True if lightweight_mode should be disabled, False otherwise.
        - Second element (str | None): Warning message if lightweight_mode should be disabled, None otherwise.
    """
    if lightweight_mode and journal_file_names:
        return (True, LIGHTWEIGHT_MODE_IGNORED_WITH_JOURNAL)
    return (False, None)


def _validate_lightweight_with_case_data(
    lightweight_mode: bool | None, case_data_file_name: None | str
) -> tuple[bool, str | None]:
    """Validate that lightweight_mode and case_data_file_name are not both provided.

    Parameters
    ----------
    lightweight_mode : bool | None
        Lightweight mode flag.
    case_data_file_name : None | str
        Case-data file name.

    Returns
    -------
    tuple[bool, str | None]
        A tuple where:
        - First element (bool): True if lightweight_mode should be disabled, False otherwise.
        - Second element (str | None): Warning message if lightweight_mode should be disabled, None otherwise.
    """
    if lightweight_mode and case_data_file_name:
        return (True, LIGHTWEIGHT_MODE_IGNORED_WITH_CASE_DATA)
    return (False, None)


def _build_case_data_arguments(
    case_file_name: None | str,
    case_data_file_name: None | str,
    builder: "FluentLaunchCmdBuilder | bool" = True,
) -> str | list[str]:
    """Build Fluent's commandline case and data file arguments.

    ``builder`` may be an existing :class:`FluentLaunchCmdBuilder` to append
    onto, or a bool selecting shell-string (``True``, default) vs token-list
    (``False``) output. Returns ``builder.get_cmd()``.

    Raises
    ------
    InvalidArgument
        If ``case_data_file_name`` is provided without ``case_file_name``.
    """
    builder = FluentLaunchCmdBuilder.as_builder(builder)
    if case_data_file_name and not case_file_name:
        raise InvalidArgument(
            "'case_data_file_name' requires 'case_file_name' to also be provided."
        )
    if case_file_name:
        if builder.shell:
            builder.append(f' -case "{str(case_file_name)}"')
        else:
            builder.extend(["-case", str(case_file_name)])
    if case_data_file_name:
        if builder.shell:
            builder.append(f' -data "{str(case_data_file_name)}"')
        else:
            builder.extend(["-data", str(case_data_file_name)])
    return builder.get_cmd()
