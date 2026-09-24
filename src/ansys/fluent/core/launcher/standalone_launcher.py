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

"""Provides a module for launching Fluent in standalone mode.

Examples
--------

>>> from ansys.fluent.core.launcher.launcher import create_launcher
>>> from ansys.fluent.core.launcher.launch_options import LaunchMode, FluentMode

>>> standalone_meshing_launcher = create_launcher(LaunchMode.STANDALONE, mode=FluentMode.MESHING)
>>> standalone_meshing_session = standalone_meshing_launcher()

>>> standalone_solver_launcher = create_launcher(LaunchMode.STANDALONE)
>>> standalone_solver_session = standalone_solver_launcher()
"""

import logging
import math
import os
from pathlib import Path
import subprocess
from typing import TYPE_CHECKING, Any, TypedDict
import warnings

from typing_extensions import Unpack

from ansys.fluent.core._types import LauncherArgsBase
from ansys.fluent.core.exceptions import InvalidArgument
from ansys.fluent.core.launcher.error_handler import (
    LaunchFluentError,
)
from ansys.fluent.core.launcher.launch_options import (
    FluentMode,
    UIMode,
    _get_argvals_and_session,
    _get_standalone_launch_fluent_version,
)
from ansys.fluent.core.launcher.launcher_utils import (
    FluentLaunchCmdBuilder,
    _await_fluent_launch,
    _build_case_data_arguments,
    _build_journal_argument,
    _confirm_watchdog_start,
    _get_subprocess_kwargs_for_fluent,
    _validate_lightweight_with_case_data,
    _validate_lightweight_with_journal,
    is_windows,
)
from ansys.fluent.core.launcher.process_launch_string import (
    _generate_launch_command,
)
from ansys.fluent.core.launcher.server_info import (
    _get_server_info,
    _get_server_info_file_names,
)
import ansys.fluent.core.launcher.watchdog as watchdog
from ansys.fluent.core.utils.fluent_version import FluentVersion

if TYPE_CHECKING:
    from ansys.fluent.core.session.meshing import Meshing
    from ansys.fluent.core.session.pure_meshing import PureMeshing
    from ansys.fluent.core.session.solver import Solver
    from ansys.fluent.core.session.solver_aero import SolverAero
    from ansys.fluent.core.session.solver_icing import SolverIcing


class StandaloneArgsWithoutDryRunMode(
    LauncherArgsBase, TypedDict, total=False
):  # pylint: disable=missing-class-docstring
    journal_file_names: None | str | list[str]
    """Path(s) to a Fluent journal file(s) that Fluent will execute. Defaults to ``None``."""
    env: dict[str, Any] | None
    """A mapping for modifying environment variables in Fluent. Defaults to ``None``."""
    case_file_name: str | None
    """Name of the case file to read into the Fluent session. Defaults to None."""
    case_data_file_name: str | None
    """Name of the case data file. If both case and data files are provided, they are read into the session."""
    lightweight_mode: bool | None
    """If True, runs in lightweight mode where mesh settings are read into a background solver session,
    replacing it once complete. This parameter is only applicable when `case_file_name` is provided; defaults to False.
    """
    py: bool | None
    """If True, runs Fluent in Python mode. Defaults to None."""
    cwd: str | None
    """Working directory for the Fluent client."""
    fluent_path: str | None
    """User-specified path for Fluent installation."""
    topy: str | list[Any] | None
    """A flag indicating whether to write equivalent Python journals from provided journal files; can also specify
    a filename for the new Python journal.
    """


class StandaloneArgsWithoutDryRun(
    StandaloneArgsWithoutDryRunMode
):  # pylint: disable=missing-class-docstring
    mode: FluentMode
    """Specifies the launch mode of Fluent to target a specific session type."""


class StandaloneArgsWithoutMode(
    StandaloneArgsWithoutDryRunMode, total=False
):  # pylint: disable=missing-class-docstring
    dry_run: bool | None
    """If True, does not launch Fluent but prints configuration information instead. The `call()` method
    returns a tuple containing the launch string and server info file name. Defaults to False.
    """


class StandaloneArgs(
    StandaloneArgsWithoutMode, StandaloneArgsWithoutDryRun, total=False
):
    """Arguments for launching Fluent in standalone mode."""


logger = logging.getLogger("pyfluent.launcher")


class StandaloneLauncher:
    """Instantiates Fluent session in standalone mode."""

    def __init__(
        self,
        **kwargs: Unpack[StandaloneArgs],
    ):
        """
        Launch a Fluent session in standalone mode.

        Parameters
        ----------
        mode : FluentMode
            Specifies the launch mode of Fluent to target a specific session type.
        ui_mode : UIMode or str, optional
            Defines the user interface mode for Fluent. Accepts either a ``UIMode`` value
            or a corresponding string such as ``"no_gui"``, ``"hidden_gui"``, or ``"gui"``.
        graphics_driver : FluentWindowsGraphicsDriver or FluentLinuxGraphicsDriver
            Specifies the graphics driver for Fluent. Options are from the ``FluentWindowsGraphicsDriver`` enum
            (for Windows) or the ``FluentLinuxGraphicsDriver`` enum (for Linux).
        product_version : FluentVersion or str or float or int, optional
            Indicates the version of Ansys Fluent to launch. For example, to use version 2025 R1, pass
            ``FluentVersion.v251``, ``"25.1.0"``, ``"25.1"``, ``25.1``, or ``251``. Defaults to ``None``,
            which uses the newest installed version.
        dimension : Dimension or int, optional
            Specifies the geometric dimensionality of the Fluent simulation. Defaults to ``None``,
            which corresponds to ``Dimension.THREE``. Acceptable values are from the ``Dimension`` enum
            (``Dimension.TWO`` or ``Dimension.THREE``) or integers ``2`` and ``3``.
        precision : Precision or str, optional
            Defines the floating point precision. Defaults to ``None``, which corresponds to
            ``Precision.DOUBLE``. Acceptable values are from the ``Precision`` enum (``Precision.SINGLE``
            or ``Precision.DOUBLE``) or strings ``"single"`` and ``"double"``.
        processor_count : int, optional
            Specifies the number of processors to use. Defaults to ``None``, which uses 1 processor.
            In job scheduler environments, this value limits the total number of allocated cores.
        journal_file_names : str or list of str, optional
            Path(s) to a Fluent journal file(s) that Fluent will execute. Defaults to ``None``.
        start_timeout : int, optional
            Maximum time in seconds allowed for connecting to the Fluent server. Defaults to 100 seconds.
        additional_arguments: str | list[str]
            Additional arguments to send to Fluent. When ``shell=True`` (default) this must
            be a string in the same format as arguments passed to Fluent on the command line.
            When ``shell=False`` this must be a list of individual command-line tokens.
        env : dict[str, str], optional
            A mapping for modifying environment variables in Fluent. Defaults to ``None``.
        cleanup_on_exit : bool, optional
            Determines whether to shut down the connected Fluent session when exiting PyFluent or calling
            the session's `exit()` method. Defaults to True.
        dry_run : bool, optional
            If True, does not launch Fluent but prints configuration information instead. The `call()` method
            returns a tuple containing the launch string and server info file name. Defaults to False.
        start_transcript : bool, optional
            Indicates whether to start streaming the Fluent transcript in the client. Defaults to True;
            streaming can be controlled via `transcript.start()` and `transcript.stop()` methods on the session object.
        case_file_name : :class:`os.PathLike` or str, optional
            Name of the case file to read into the Fluent session. Defaults to None.
        case_data_file_name : :class:`os.PathLike` or str, optional
            Name of the case data file. If both case and data files are provided, they are read into the session.
        lightweight_mode : bool, optional
            If True, runs in lightweight mode where mesh settings are read into a background solver session,
            replacing it once complete. This parameter is only applicable when `case_file_name` is provided; defaults to False.
        py : bool, optional
            If True, runs Fluent in Python mode. Defaults to None.
        gpu : bool, optional
            If True, starts Fluent with GPU Solver enabled.
        cwd : :class:`os.PathLike` or str, optional
            Working directory for the Fluent client.
        fluent_path: :class:`os.PathLike` or str, optional
            User-specified path for Fluent installation.
        topy :  bool or str, optional
            A flag indicating whether to write equivalent Python journals from provided journal files; can also specify
            a filename for the new Python journal.
        start_watchdog : bool, optional
            When `cleanup_on_exit` is True, defaults to True; an independent watchdog process ensures that any local
            GUI-less Fluent sessions started by PyFluent are properly closed when the current Python process ends.
        file_transfer_service : Any
            Service for uploading/downloading files to/from the server.
        shell: bool
            Whether to run the Fluent launch subprocess call with ``shell=True`` (default)
            or ``shell=False``. When ``shell=False``, the Fluent launch command is constructed
            as a list of arguments and ``additional_arguments`` must be a list of strings.

        Raises
        ------
        UnexpectedKeywordArgument
            If an unexpected keyword argument is provided.

        Notes
        -----
        In job scheduler environments (e.g., SLURM, LSF, PBS), resources and compute nodes are allocated,
        and core counts are queried from these environments before being passed to Fluent.
        """
        import ansys.fluent.core as pyfluent

        self.argvals, self.new_session = _get_argvals_and_session(kwargs)
        self.file_transfer_service = kwargs.get("file_transfer_service")

        self._configure_argvals(kwargs, pyfluent)
        self._validate_argvals()
        self._apply_version_dependent_defaults()
        if pyfluent.config.fluent_debug:
            self.argvals["fluent_debug"] = True

        server_info_file_name_for_server, self._server_info_file_name = (
            _get_server_info_file_names()
        )

        self._shell = self.argvals.get("shell", True)
        self._validate_shell_additional_arguments()

        self._cmd_builder = FluentLaunchCmdBuilder(self._shell)
        _generate_launch_command(
            self.argvals, server_info_file_name_for_server, self._cmd_builder
        )
        self._append_timeout_arg()

        self._sifile_last_mtime = Path(self._server_info_file_name).stat().st_mtime
        self._kwargs = _get_subprocess_kwargs_for_fluent(
            self.argvals.get("env") or {}, self.argvals
        )
        if self.argvals.get("cwd"):
            self._kwargs.update(cwd=self.argvals.get("cwd"))

        self._append_case_data_args()
        self._append_journal_args()
        self._launch_cmd = self._final_launch_cmd()

    def _configure_argvals(self, kwargs, pyfluent) -> None:
        """Apply the UI-mode override from config and defaults for ``lightweight_mode``."""
        if pyfluent.config.show_fluent_gui:
            kwargs["ui_mode"] = UIMode.GUI
        self.argvals["ui_mode"] = UIMode(kwargs.get("ui_mode"))
        if self.argvals.get("lightweight_mode") is None:
            self.argvals["lightweight_mode"] = False

    def _validate_argvals(self) -> None:
        """Validate mode combinations and downgrade ``lightweight_mode`` on conflict."""
        # case_data_file_name is not supported in meshing mode.
        if FluentMode.is_meshing(self.argvals.get("mode")) and self.argvals.get(
            "case_data_file_name"
        ):
            raise InvalidArgument("Case and data file cannot be read in meshing mode.")

        self._downgrade_lightweight_on_conflict(
            _validate_lightweight_with_journal,
            self.argvals.get("journal_file_names"),
        )
        self._downgrade_lightweight_on_conflict(
            _validate_lightweight_with_case_data,
            self.argvals.get("case_data_file_name"),
        )

    def _downgrade_lightweight_on_conflict(self, validator, conflicting_value) -> None:
        """Disable ``lightweight_mode`` with a warning when ``validator`` reports a conflict."""
        should_disable, warning_msg = validator(
            self.argvals.get("lightweight_mode"), conflicting_value
        )
        if should_disable:
            warnings.warn(warning_msg, UserWarning)
            self.argvals["lightweight_mode"] = False

    def _apply_version_dependent_defaults(self) -> None:
        """Enable ``py`` mode by default when running Fluent v25.1 or newer."""
        fluent_version = _get_standalone_launch_fluent_version(self.argvals)
        if (
            fluent_version
            and fluent_version >= FluentVersion.v251
            and self.argvals.get("py") is None
        ):
            self.argvals["py"] = True

    def _validate_shell_additional_arguments(self) -> None:
        """Reject a string ``additional_arguments`` when ``shell=False`` is in effect."""
        additional_arguments = self.argvals.get("additional_arguments")
        if (
            not self._shell
            and isinstance(additional_arguments, str)
            and additional_arguments
        ):
            raise InvalidArgument(
                "'additional_arguments' must be a list of strings when 'shell=False'."
            )

    def _append_timeout_arg(self) -> None:
        """Append the session-idle-timeout argument to the launch command."""
        if self.argvals.get("start_timeout") is None:
            self.argvals["start_timeout"] = 100
        start_timeout = self.argvals["start_timeout"]
        # Negative start_timeout values are treated as "no timeout".
        if start_timeout < 0:
            return
        self._cmd_builder.extend(
            self._construct_timeout(start_timeout, shell=self._shell)
        )

    def _append_case_data_args(self) -> None:
        """Append ``-case`` / ``-data`` CLI args unless lightweight_mode defers case reading."""
        if self.argvals.get("lightweight_mode") and self.argvals.get("case_file_name"):
            # Case reading is deferred to post-connection for lightweight_mode
            # to support background session orchestration.
            return
        _build_case_data_arguments(
            self.argvals.get("case_file_name"),
            self.argvals.get("case_data_file_name"),
            self._cmd_builder,
        )

    def _append_journal_args(self) -> None:
        """Append ``-i`` / ``-topy`` journal-file CLI args to the launch command."""
        _build_journal_argument(
            self.argvals.get("topy", []),
            self.argvals.get("journal_file_names"),
            self._cmd_builder,
        )

    def _final_launch_cmd(self) -> str | list[str]:
        """Return the command form that will be handed to ``subprocess.Popen``."""
        cmd = self._cmd_builder.get_cmd()
        if (
            self._shell
            and not is_windows()
            and self.argvals.get("ui_mode") not in (UIMode.GUI, UIMode.HIDDEN_GUI)
        ):
            # Linux + no visible GUI: nohup + '&' detaches Fluent from the current terminal.
            cmd = "nohup " + cmd + " &"
        return cmd

    @staticmethod
    def _construct_timeout(
        idle_timeout_seconds: int, shell: bool = True
    ) -> str | list[str]:
        """Return the session-idle-timeout CLI argument.

        The shell form is byte-identical to the historical hand-written
        fragment (``' -command="(...)"'``); the token form is a single
        ``-command=(...)`` element with the same effect after shell parsing.
        """
        # +1 ensures the minute-granularity timer never fires before start_timeout elapses.
        _idle_timeout_minutes = math.ceil(idle_timeout_seconds / 60) + 1
        if shell:
            return f' -command="(set-session-idle-timeoutPLF+{_idle_timeout_minutes})"'
        return [f"-command=(set-session-idle-timeoutPLF+{_idle_timeout_minutes})"]

    @staticmethod
    def _construct_timeout_arg(idle_timeout_seconds: int) -> str:
        """Compatibility wrapper returning the previous shell-formatted timeout arg."""
        return StandaloneLauncher._construct_timeout(idle_timeout_seconds, shell=True)

    @staticmethod
    def _construct_timeout_token(idle_timeout_seconds: int) -> str:
        """Compatibility wrapper returning the previous single-token timeout arg."""
        return StandaloneLauncher._construct_timeout(idle_timeout_seconds, shell=False)[
            0
        ]

    @staticmethod
    def _disable_idle_timeout_guard(session):
        try:
            default_idle_timeout = session.preferences.General.IdleTimeout()
        except RuntimeError:
            # This exception is raised only while running codegen locally before the preferences root is available.
            default_idle_timeout = 0
        try:
            session.application_runtime.set_idle_timeout(default_idle_timeout * 60)
        except Exception as ex:
            raise RuntimeError("Could not reset Idle Timeout") from ex

    def __call__(
        self,
    ) -> "Meshing | PureMeshing | Solver | SolverIcing | SolverAero | tuple[str, str]":
        if self.argvals.get("dry_run"):
            base_cmd = self._cmd_builder.get_cmd()
            label = "string" if self._shell else "command"
            print(f"Fluent launch {label}: {base_cmd}")
            return base_cmd, self._server_info_file_name
        try:
            logger.debug(f"Launching Fluent with command: {self._launch_cmd}")
            process = subprocess.Popen(self._launch_cmd, **self._kwargs)

            try:
                _await_fluent_launch(
                    self._server_info_file_name,
                    self.argvals.get("start_timeout", 100),
                    self._sifile_last_mtime,
                    process.pid,
                )
            except TimeoutError as ex:
                if is_windows() and self._shell:
                    logger.warning(f"Exception caught - {type(ex).__name__}: {ex}")
                    # Fall back to unquoted shell string so cmd.exe can locate the exe.
                    launch_cmd = self._cmd_builder.get_cmd().replace('"', "", 2)
                    self._kwargs.update(shell=False)
                    logger.warning(
                        f"Retrying Fluent launch with less robust command: {launch_cmd}"
                    )
                    process = subprocess.Popen(launch_cmd, **self._kwargs)
                    _await_fluent_launch(
                        self._server_info_file_name,
                        self.argvals.get("start_timeout", 100),
                        self._sifile_last_mtime,
                        process.pid,
                    )
                else:
                    raise ex

            session = self.new_session._create_from_server_info_file(
                server_info_file_name=self._server_info_file_name,
                file_transfer_service=self.file_transfer_service,
                cleanup_on_exit=self.argvals.get("cleanup_on_exit"),
                start_transcript=self.argvals.get("start_transcript"),
                launcher_args=self.argvals,
                inside_container=False,
            )
            session._process = process
            start_watchdog = _confirm_watchdog_start(
                self.argvals.get("start_watchdog"),
                self.argvals.get("cleanup_on_exit"),
                session._fluent_connection,
            )
            if start_watchdog:
                logger.info("Launching Watchdog for local Fluent client...")
                values = _get_server_info(self._server_info_file_name)
                if len(values) == 3:
                    ip, port, password = values
                    watchdog.launch(
                        os.getpid(),
                        port,
                        password,
                        ip,
                        inside_container=False,
                    )
            # PyFluent is now connected: disable the idle-timeout guard.
            self._disable_idle_timeout_guard(session)

            # For lightweight_mode with case file, read case post-connection
            # to support background session orchestration
            if self.argvals.get("lightweight_mode") and self.argvals.get(
                "case_file_name"
            ):
                session.read_case_lightweight(self.argvals.get("case_file_name"))

            return session
        except Exception as ex:
            logger.error(f"Exception caught - {type(ex).__name__}: {ex}")
            raise LaunchFluentError(self._launch_cmd) from ex
        finally:
            if self.argvals.get("cleanup_on_exit", True):
                Path(self._server_info_file_name).unlink(missing_ok=True)
