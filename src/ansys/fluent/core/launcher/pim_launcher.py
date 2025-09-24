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

"""Provides a module for launching Fluent in pim mode.

Examples
--------

>>> from ansys.fluent.core.launcher.launcher import create_launcher
>>> from ansys.fluent.core.launcher.launch_options import LaunchMode, FluentMode

>>> pim_meshing_launcher = create_launcher(LaunchMode.PIM, mode=FluentMode.MESHING)
>>> pim_meshing_session = pim_meshing_launcher()

>>> pim_solver_launcher = create_launcher(LaunchMode.PIM)
>>> pim_solver_session = pim_solver_launcher()
"""

import logging
import os
from typing import Any, Dict, TypedDict

from typing_extensions import Unpack

from ansys.fluent.core.fluent_connection import FluentConnection, _get_max_c_int_limit
from ansys.fluent.core.launcher.launch_options import (
    Dimension,
    FluentLinuxGraphicsDriver,
    FluentMode,
    FluentWindowsGraphicsDriver,
    Precision,
    UIMode,
    _get_argvals_and_session,
)
from ansys.fluent.core.session_meshing import Meshing
from ansys.fluent.core.session_pure_meshing import PureMeshing
from ansys.fluent.core.session_solver import Solver
from ansys.fluent.core.session_solver_icing import SolverIcing
from ansys.fluent.core.utils.file_transfer_service import PimFileTransferService
from ansys.fluent.core.utils.fluent_version import FluentVersion
import ansys.platform.instancemanagement as pypim


class PIMArgsWithoutDryRun(
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
    cleanup_on_exit: bool
    start_transcript: bool
    gpu: bool | None
    start_watchdog: bool | None
    file_transfer_service: Any | None


class PIMArgs(
    PIMArgsWithoutDryRun, total=False
):  # pylint: disable=missing-class-docstring
    dry_run: bool


class PIMArgsWithMode(PIMArgs, total=False):  # pylint: disable=missing-class-docstring
    mode: FluentMode | str | None


_THIS_DIR = os.path.dirname(__file__)
_OPTIONS_FILE = os.path.join(_THIS_DIR, "fluent_launcher_options.json")
logger = logging.getLogger("pyfluent.launcher")


class PIMLauncher:
    """Instantiates Fluent session in `PIM <https://pypim.docs.pyansys.com/version/stable/>`_ mode."""

    def __init__(
        self,
        **kwargs: Unpack[PIMArgsWithMode],
    ):
        """
        Launch a Fluent session in `PIM <https://pypim.docs.pyansys.com/version/stable/>`_ mode.

        Parameters
        ----------
        mode : FluentMode
            Specifies the launch mode of Fluent for targeting a specific session type.
        ui_mode : UIMode
            Defines the user interface mode for Fluent. Options correspond to values in the ``UIMode`` enum.
        graphics_driver : FluentWindowsGraphicsDriver or FluentLinuxGraphicsDriver
            Specifies the graphics driver for Fluent. Options are from the ``FluentWindowsGraphicsDriver`` enum
            (for Windows) or the ``FluentLinuxGraphicsDriver`` enum (for Linux).
        product_version : FluentVersion or str or float or int, optional
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
        cleanup_on_exit : bool
            Determines whether to shut down the connected Fluent session upon exit or when calling
            the session's `exit()` method. Defaults to True.
        dry_run : bool, optional
            If True, returns a configuration dictionary instead of starting a Fluent session.
        start_transcript : bool
            Indicates whether to start streaming the Fluent transcript in the client. Defaults to True;
            streaming can be controlled via `transcript.start()` and `transcript.stop()` methods on the session object.
        gpu : bool, optional
            If True, starts Fluent with GPU Solver enabled.
        start_watchdog : bool, optional
            If True and `cleanup_on_exit` is True, an independent watchdog process is run to ensure that any local
            GUI-less Fluent sessions started by PyFluent are properly closed when the current Python process ends.
        file_transfer_service : Any, optional
            Service for uploading/downloading files to/from the server.

        Returns
        -------
        Union[Meshing, PureMeshing, Solver, SolverIcing, dict]
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
        additional_arguments = kwargs.get("additional_arguments", "")
        start_watchdog = kwargs.get("start_watchdog")
        file_transfer_service = kwargs.get("file_transfer_service")

        if additional_arguments:
            logger.warning(
                "'additional_arguments' option for 'launch_fluent()' method is not supported "
                "when starting a remote Fluent PyPIM client."
            )

        if start_watchdog:
            logger.warning(
                "'start_watchdog' argument for 'launch_fluent()' method is not supported "
                "when starting a remote Fluent PyPIM client."
            )
        self.argvals, self.new_session = _get_argvals_and_session(kwargs)
        self.file_transfer_service = file_transfer_service
        if self.argvals.get("start_timeout") is None:
            self.argvals["start_timeout"] = 60

    def __call__(self):
        logger.info("Starting Fluent remotely. The startup configuration is ignored.")
        if self.argvals["product_version"]:
            fluent_product_version = str(
                FluentVersion(self.argvals["product_version"]).number
            )
        else:
            fluent_product_version = str(
                FluentVersion(FluentVersion.current_release()).number
            )

        return launch_remote_fluent(
            session_cls=self.new_session,
            start_transcript=self.argvals["start_transcript"],
            product_version=fluent_product_version,
            cleanup_on_exit=self.argvals["cleanup_on_exit"],
            mode=self.argvals["mode"],
            dimensionality=self.argvals["dimension"],
            launcher_args=self.argvals,
            file_transfer_service=self.file_transfer_service,
        )


def launch_remote_fluent(
    session_cls,
    start_transcript: bool,
    product_version: str | None = None,
    cleanup_on_exit: bool = True,
    mode: FluentMode = FluentMode.SOLVER,
    dimensionality: str | None = None,
    launcher_args: Dict[str, Any] | None = None,
    file_transfer_service: Any | None = None,
) -> Meshing | PureMeshing | Solver | SolverIcing:
    """Launch Fluent remotely using `PyPIM <https://pypim.docs.pyansys.com>`.

    Ensure that you are in an environment where PyPIM is configured.
    Use the :func:`pypim.is_configured <ansys.platform.instancemanagement.is_configured>`
    method to verify that PyPIM is configured.

    Parameters
    ----------
    session_cls: type(Meshing) | type(PureMeshing) | type(Solver) | type(SolverIcing)
        Session type.
    start_transcript: bool
        Whether to start streaming the Fluent transcript in the client.
    product_version : str, optional
        Version of Ansys Fluent to launch. Default is ``None`` for the newest version.
    cleanup_on_exit : bool, optional
        Whether to clean up and exit Fluent when Python exits. Default is ``True``.
    mode : FluentMode, optional
        Launch Fluent in meshing mode. Default is ``FluentMode.SOLVER``.
    dimensionality : str, optional
        Geometric dimensionality of the Fluent simulation. Default is ``None`` (3D).
    file_transfer_service : optional
        Service for uploading/downloading files to/from the server.
    launcher_args : Any
        Launcher arguments.

    Returns
    -------
    Meshing | PureMeshing | Solver | SolverIcing
        Session object.
    """

    pim = pypim.connect()

    instance = create_fluent_instance(
        pim=pim,
        mode=mode,
        dimensionality=dimensionality,
        product_version=product_version,
    )

    instance.wait_for_ready()

    channel = instance.build_grpc_channel(
        options=[
            ("grpc.max_send_message_length", _get_max_c_int_limit()),
            ("grpc.max_receive_message_length", _get_max_c_int_limit()),
        ],
    )

    fluent_connection = create_fluent_connection(
        channel=channel,
        cleanup_on_exit=cleanup_on_exit,
        instance=instance,
        launcher_args=launcher_args,
    )

    file_transfer_service = get_file_transfer_service(
        file_transfer_service, fluent_connection
    )

    return session_cls(
        fluent_connection=fluent_connection,
        scheme_eval=fluent_connection._connection_interface.scheme_eval,
        file_transfer_service=file_transfer_service,
        start_transcript=start_transcript,
    )


def create_fluent_instance(
    pim, mode: FluentMode, dimensionality: str | None, product_version: str | None
):
    """Create a Fluent instance based on mode and dimensionality."""

    product_name = (
        "fluent-meshing"
        if FluentMode.is_meshing(mode)
        else "fluent-2ddp" if dimensionality == Dimension.TWO else "fluent-3ddp"
    )

    return pim.create_instance(
        product_name=product_name, product_version=product_version
    )


def create_fluent_connection(
    channel, cleanup_on_exit: bool, instance, launcher_args: Dict[str, Any] | None
):
    """Create a Fluent connection."""

    return FluentConnection(
        channel=channel,
        cleanup_on_exit=cleanup_on_exit,
        remote_instance=instance,
        slurm_job_id=launcher_args.get("slurm_job_id") if launcher_args else None,
    )


def get_file_transfer_service(
    file_transfer_service: Any | None, fluent_connection
) -> Any:
    """Get the file transfer service."""

    return (
        file_transfer_service
        if file_transfer_service
        else PimFileTransferService(pim_instance=fluent_connection._remote_instance)
    )
