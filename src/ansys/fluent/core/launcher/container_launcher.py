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

"""Provides a module for launching Fluent in container mode.

Examples
--------

>>> from ansys.fluent.core.launcher.launcher import create_launcher
>>> from ansys.fluent.core.launcher.launch_options import LaunchMode, FluentMode

>>> container_meshing_launcher = create_launcher(LaunchMode.CONTAINER, mode=FluentMode.MESHING)
>>> container_meshing_session = container_meshing_launcher()

>>> container_solver_launcher = create_launcher(LaunchMode.CONTAINER)
>>> container_solver_session = container_solver_launcher()
"""

import logging
import os
import time
from typing import Any, TypedDict

from typing_extensions import Unpack

from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.launcher.fluent_container import (
    configure_container_dict,
    dict_to_str,
    start_fluent_container,
)
from ansys.fluent.core.launcher.launch_options import (
    Dimension,
    FluentLinuxGraphicsDriver,
    FluentMode,
    FluentWindowsGraphicsDriver,
    Precision,
    UIMode,
    _get_argvals_and_session,
)
from ansys.fluent.core.launcher.launcher_utils import ComposeConfig
from ansys.fluent.core.launcher.process_launch_string import (
    _build_fluent_launch_args_string,
)
import ansys.fluent.core.launcher.watchdog as watchdog
from ansys.fluent.core.session import _parse_server_info_file
from ansys.fluent.core.utils.fluent_version import FluentVersion


class ContainerArgsWithoutDryRun(
    TypedDict, total=False
):  # pylint: disable=missing-class-docstring
    ui_mode: UIMode | str | None
    graphics_driver: (
        FluentWindowsGraphicsDriver | FluentLinuxGraphicsDriver | str | None
    )
    product_version: FluentVersion | str | float | int | None
    dimension: Dimension | int | None
    precision: Precision | str | None
    processor_count: int | None
    start_timeout: int
    additional_arguments: str
    container_dict: dict[str, Any] | None
    cleanup_on_exit: bool
    start_transcript: bool
    py: bool | None
    gpu: bool | None
    start_watchdog: bool | None
    file_transfer_service: Any | None
    use_docker_compose: bool | None
    use_podman_compose: bool | None


class ContainerArgs(
    ContainerArgsWithoutDryRun, total=False
):  # pylint: disable=missing-class-docstring
    dry_run: bool


_THIS_DIR = os.path.dirname(__file__)
_OPTIONS_FILE = os.path.join(_THIS_DIR, "fluent_launcher_options.json")
logger = logging.getLogger("pyfluent.launcher")


def _get_server_info_from_container(config_dict):
    """Retrieve the server info from a specified file in a container."""

    host_server_info_file = config_dict["host_server_info_file"]

    time_limit = 0
    while not host_server_info_file.exists():
        time.sleep(2)
        time_limit += 2
        if time_limit > 60:
            raise FileNotFoundError(f"{host_server_info_file} not found.")

    return _parse_server_info_file(str(host_server_info_file))


class DockerLauncher:
    """Instantiates Fluent session in container mode."""

    def __init__(
        self,
        mode: FluentMode | str,
        **kwargs: Unpack[ContainerArgs],
    ):
        """
        Launch a Fluent session in container mode.

        Parameters
        ----------
        mode : FluentMode
            Specifies the launch mode of Fluent to target a specific session type.
        ui_mode : UIMode
            Defines the user interface mode for Fluent. Options correspond to values in the ``UIMode`` enum.
        graphics_driver : FluentWindowsGraphicsDriver or FluentLinuxGraphicsDriver
            Specifies the graphics driver for Fluent. Options are from the ``FluentWindowsGraphicsDriver`` enum
            (for Windows) or the ``FluentLinuxGraphicsDriver`` enum (for Linux).
        product_version :  FluentVersion or str or float or int, optional
            Indicates the version of Ansys Fluent to launch. For example, to use version 2025 R1, pass
            any of ``FluentVersion.v251``, ``"25.1.0"``, ``"25.1"``, ``25.1``, or ``251``. Defaults to ``None``,
            which uses the newest installed version.
        dimension : Dimension or int, optional
            Specifies the geometric dimensionality of the Fluent simulation. Defaults to ``None``,
            which corresponds to ``Dimension.THREE``. Acceptable values include ``Dimension.TWO``,
            ``Dimension.THREE``, or integers ``2`` and ``3``.
        precision : Precision or str, optional
            Defines the floating point precision. Defaults to ``None``, which corresponds to
            ``Precision.DOUBLE``. Acceptable values include ``Precision.SINGLE``,
            ``Precision.DOUBLE``, or strings ``"single"`` and ``"double"``.
        processor_count : int, optional
            Specifies the number of processors to use. Defaults to ``None``, which uses 1 processor.
            In job scheduler environments, this value limits the total number of allocated cores.
        start_timeout : int, optional
            Maximum allowable time in seconds for connecting to the Fluent server. Defaults to 60 seconds.
        additional_arguments : str, optional
            Additional command-line arguments for Fluent, formatted as they would be on the command line.
        container_dict : dict, optional
            Configuration dictionary for launching Fluent inside a Docker container. See also
            :mod:`~ansys.fluent.core.launcher.fluent_container`.
        dry_run : bool, optional
            If True, does not launch Fluent but prints configuration information instead. If dry running a
            container start, this method will return the configured ``container_dict``. Defaults to False.
        cleanup_on_exit : bool
            Determines whether to shut down the connected Fluent session upon exit or when calling
            the session's `exit()` method. Defaults to True.
        start_transcript : bool
            Indicates whether to start streaming the Fluent transcript in the client. Defaults to True;
            streaming can be controlled via `transcript.start()` and `transcript.stop()` methods on the session object.
        py : bool, optional
            If True, runs Fluent in Python mode. Defaults to None.
        gpu : bool, optional
            If True, starts Fluent with GPU Solver enabled.
        start_watchdog : bool, optional
            If True and `cleanup_on_exit` is True, an independent watchdog process is run to ensure that any local
            GUI-less Fluent sessions started by PyFluent are properly closed when the current Python process ends.
        file_transfer_service : Any, optional
            Service for uploading/downloading files to/from the server.
        use_docker_compose: bool
            Whether to use Docker Compose to launch Fluent.
        use_podman_compose: bool
            Whether to use Podman Compose to launch Fluent.

        Returns
        -------
        Meshing | PureMeshing | Solver | SolverIcing | dict
            Session object or configuration dictionary if ``dry_run`` is True.

        Raises
        ------
        UnexpectedKeywordArgument
            If an unexpected keyword argument is provided.

        Notes
        -----
        In job scheduler environments (e.g., SLURM, LSF, PBS), resources and compute nodes are allocated,
        and core counts are queried from these environments before being passed to Fluent.
        """
        self.argvals, self.new_session = _get_argvals_and_session(
            {**kwargs, mode: mode}
        )
        if self.argvals.get("start_timeout") is None:
            self.argvals["start_timeout"] = 60
        self.file_transfer_service = kwargs.get("file_transfer_service")
        if self.argvals["mode"] == FluentMode.SOLVER_ICING:
            self.argvals["fluent_icing"] = True
        if self.argvals.get("container_dict") is None:
            self.argvals["container_dict"] = {}
        if "product_version" in self.argvals:
            self.argvals["container_dict"][
                "image_tag"
            ] = f"v{FluentVersion(self.argvals['product_version']).value}"

        self._args = _build_fluent_launch_args_string(**self.argvals).split()
        if FluentMode.is_meshing(self.argvals["mode"]):
            self._args.append(" -meshing")

        use_docker_compose = kwargs.get("use_docker_compose")
        use_podman_compose = kwargs.get("use_podman_compose")
        self._compose_config = ComposeConfig(use_docker_compose, use_podman_compose)

    def __call__(self):
        if self.argvals["dry_run"]:
            config_dict, *_ = configure_container_dict(
                self._args,
                compose_config=self._compose_config,
                **self.argvals["container_dict"],
            )
            dict_str = dict_to_str(config_dict)
            print("\nDocker container run configuration:\n")
            print("config_dict = ")
            print(dict_str)
            return config_dict

        logger.debug(f"Fluent container launcher args: {self._args}")
        logger.debug(f"Fluent container launcher argvals:\n{dict_to_str(self.argvals)}")

        if self._compose_config.is_compose:
            port, config_dict, container = start_fluent_container(
                self._args,
                self.argvals["container_dict"],
                self.argvals["start_timeout"],
                compose_config=self._compose_config,
            )

            _, _, password = _get_server_info_from_container(config_dict=config_dict)
        else:
            port, password, container = start_fluent_container(
                self._args,
                self.argvals["container_dict"],
                self.argvals["start_timeout"],
                compose_config=self._compose_config,
            )

        fluent_connection = FluentConnection(
            port=port,
            password=password,
            file_transfer_service=self.file_transfer_service,
            cleanup_on_exit=self.argvals["cleanup_on_exit"],
            slurm_job_id=self.argvals and self.argvals.get("slurm_job_id"),
            inside_container=True,
            container=container,
            compose_config=self._compose_config,
        )

        self.argvals["compose_config"] = self._compose_config

        session = self.new_session(
            fluent_connection=fluent_connection,
            scheme_eval=fluent_connection._connection_interface.scheme_eval,
            file_transfer_service=self.file_transfer_service,
            start_transcript=self.argvals["start_transcript"],
            launcher_args=self.argvals,
        )

        session._container = container

        if not self._compose_config.is_compose:
            if (
                self.argvals["start_watchdog"] is None
                and self.argvals["cleanup_on_exit"]
            ):
                self.argvals["start_watchdog"] = True
            if self.argvals["start_watchdog"]:
                logger.debug("Launching Watchdog for Fluent container...")
                watchdog.launch(os.getpid(), port, password)

        return session
