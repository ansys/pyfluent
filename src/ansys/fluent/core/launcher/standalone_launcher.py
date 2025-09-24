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
import os
from pathlib import Path
import subprocess
from typing import Any, TypedDict

from typing_extensions import Unpack

from ansys.fluent.core.launcher.error_handler import (
    LaunchFluentError,
    _raise_non_gui_exception_in_windows,
)
from ansys.fluent.core.launcher.launch_options import (
    Dimension,
    FluentLinuxGraphicsDriver,
    FluentMode,
    FluentWindowsGraphicsDriver,
    Precision,
    UIMode,
    _get_argvals_and_session,
    _get_standalone_launch_fluent_version,
)
from ansys.fluent.core.launcher.launcher import LaunchFluentArgs
from ansys.fluent.core.launcher.launcher_utils import (
    _await_fluent_launch,
    _build_journal_argument,
    _confirm_watchdog_start,
    _get_subprocess_kwargs_for_fluent,
    is_windows,
)
from ansys.fluent.core.launcher.process_launch_string import _generate_launch_string
from ansys.fluent.core.launcher.server_info import (
    _get_server_info,
    _get_server_info_file_names,
)
import ansys.fluent.core.launcher.watchdog as watchdog
from ansys.fluent.core.session import BaseSession
from ansys.fluent.core.utils.fluent_version import FluentVersion


class StandaloneArgsWithoutDryRun(
    TypedDict, total=False
):  # pylint: disable=missing-class-docstring
    product_version: FluentVersion | str | float | int | None
    dimension: Dimension | int
    precision: Precision | str
    processor_count: int | None
    journal_file_names: None | str | list[str]
    start_timeout: int
    additional_arguments: str
    env: dict[str, Any] | None
    cleanup_on_exit: bool
    start_transcript: bool
    ui_mode: UIMode | str | None
    graphics_driver: (
        FluentWindowsGraphicsDriver | FluentLinuxGraphicsDriver | str | None
    )
    case_file_name: str | None
    case_data_file_name: str | None
    lightweight_mode: bool | None
    py: bool | None
    gpu: bool | list[int] | None
    cwd: str | None
    fluent_path: str | None
    topy: str | list[Any] | None
    start_watchdog: bool | None
    file_transfer_service: Any | None


class StandaloneArgs(
    StandaloneArgsWithoutDryRun, total=False
):  # pylint: disable=missing-class-docstring
    dry_run: bool | None


logger = logging.getLogger("pyfluent.launcher")


class StandaloneLauncher:
    """Instantiates Fluent session in standalone mode."""

    def __init__(
        self,
        *,
        mode: FluentMode,
        dry_run: bool = False,
        **kwargs: Unpack[LaunchFluentArgs],
    ):
        """
        Launch a Fluent session in standalone mode.

        Parameters
        ----------
        mode : FluentMode
            Specifies the launch mode of Fluent to target a specific session type.
        ui_mode : UIMode
            Defines the user interface mode for Fluent. Options correspond to values in the ``UIMode`` enum.
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
            Maximum time in seconds allowed for connecting to the Fluent server. Defaults to 60 seconds.
        additional_arguments : str, optional
            Additional command-line arguments for Fluent, formatted as they would be on the command line.
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
        case_file_name : str, optional
            Name of the case file to read into the Fluent session. Defaults to None.
        case_data_file_name : str, optional
            Name of the case data file. If both case and data files are provided, they are read into the session.
        lightweight_mode : bool, optional
            If True, runs in lightweight mode where mesh settings are read into a background solver session,
            replacing it once complete. This parameter is only applicable when `case_file_name` is provided; defaults to False.
        py : bool, optional
            If True, runs Fluent in Python mode. Defaults to None.
        gpu : bool, optional
            If True, starts Fluent with GPU Solver enabled.
        cwd : str, optional
            Working directory for the Fluent client.
        fluent_path: str, optional
            User-specified path for Fluent installation.
        topy :  bool or str, optional
            A flag indicating whether to write equivalent Python journals from provided journal files; can also specify
            a filename for the new Python journal.
        start_watchdog : bool, optional
            When `cleanup_on_exit` is True, defaults to True; an independent watchdog process ensures that any local
            GUI-less Fluent sessions started by PyFluent are properly closed when the current Python process ends.
        file_transfer_service : Any
            Service for uploading/downloading files to/from the server.

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
        if pyfluent.config.show_fluent_gui:
            kwargs["ui_mode"] = UIMode.GUI
        self.argvals["ui_mode"] = UIMode(kwargs.get("ui_mode"))
        if self.argvals.get("start_timeout") is None:
            self.argvals["start_timeout"] = 60
        if self.argvals.get("lightweight_mode") is None:
            self.argvals["lightweight_mode"] = False
        fluent_version = _get_standalone_launch_fluent_version(self.argvals)
        if fluent_version:
            _raise_non_gui_exception_in_windows(self.argvals["ui_mode"], fluent_version)

        if (
            fluent_version
            and fluent_version >= FluentVersion.v251
            and self.argvals.get("py") is None
        ):
            self.argvals["py"] = True

        if pyfluent.config.fluent_debug:
            self.argvals["fluent_debug"] = True

        server_info_file_name_for_server, server_info_file_name_for_client = (
            _get_server_info_file_names()
        )
        self._server_info_file_name = server_info_file_name_for_client
        self._launch_string = _generate_launch_string(
            self.argvals,
            server_info_file_name_for_server,
        )

        self._sifile_last_mtime = Path(self._server_info_file_name).stat().st_mtime
        self._kwargs = _get_subprocess_kwargs_for_fluent(
            self.argvals.get("env", {}), self.argvals
        )
        if "cwd" in self.argvals:
            self._kwargs.update(cwd=self.argvals.get("cwd"))
        self._launch_string += _build_journal_argument(
            self.argvals.get("topy", []), self.argvals.get("journal_file_names")
        )

        if is_windows():
            if (
                pyfluent.config.launch_fluent_stdout
                or pyfluent.config.launch_fluent_stderr
            ):
                self._launch_cmd = self._launch_string
            else:
                # Using 'start.exe' is better; otherwise Fluent is more susceptible to bad termination attempts.
                self._launch_cmd = 'start "" ' + self._launch_string
        else:
            if self.argvals.get("ui_mode") not in [UIMode.GUI, UIMode.HIDDEN_GUI]:
                # Using nohup to hide Fluent output from the current terminal
                self._launch_cmd = "nohup " + self._launch_string + " &"
            else:
                self._launch_cmd = self._launch_string

    def __call__(self) -> tuple[str, str] | BaseSession:
        if self.argvals.get("dry_run"):
            print(f"Fluent launch string: {self._launch_string}")
            return self._launch_string, self._server_info_file_name
        try:
            logger.debug(f"Launching Fluent with command: {self._launch_cmd}")

            process = subprocess.Popen(self._launch_cmd, **self._kwargs)

            try:
                _await_fluent_launch(
                    self._server_info_file_name,
                    self.argvals.get("start_timeout", 60),
                    self._sifile_last_mtime,
                )
            except TimeoutError as ex:
                if is_windows():
                    logger.warning(f"Exception caught - {type(ex).__name__}: {ex}")
                    launch_cmd = self._launch_string.replace('"', "", 2)
                    self._kwargs.update(shell=False)
                    logger.warning(
                        f"Retrying Fluent launch with less robust command: {launch_cmd}"
                    )
                    process = subprocess.Popen(launch_cmd, **self._kwargs)
                    _await_fluent_launch(
                        self._server_info_file_name,
                        self.argvals.get("start_timeout", 60),
                        self._sifile_last_mtime,
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
                ip, port, password = _get_server_info(self._server_info_file_name)
                watchdog.launch(os.getpid(), port, password, ip)
            if self.argvals.get("case_file_name"):
                if FluentMode.is_meshing(self.argvals.get("mode")):
                    session.tui.file.read_case(self.argvals.get("case_file_name"))
                elif self.argvals.get("lightweight_mode"):
                    session.read_case_lightweight(self.argvals.get("case_file_name"))
                else:
                    session.file.read(
                        file_type="case",
                        file_name=self.argvals.get("case_file_name"),
                    )
            if self.argvals.get("case_data_file_name"):
                if not FluentMode.is_meshing(self.argvals.get("mode")):
                    session.file.read(
                        file_type="case-data",
                        file_name=self.argvals.get("case_data_file_name"),
                    )
                else:
                    raise RuntimeError(
                        "Case and data file cannot be read in meshing mode."
                    )

            return session
        except Exception as ex:
            logger.error(f"Exception caught - {type(ex).__name__}: {ex}")
            raise LaunchFluentError(self._launch_cmd) from ex
        finally:
            server_info_file = Path(self._server_info_file_name)
            if server_info_file.exists():
                server_info_file.unlink()
