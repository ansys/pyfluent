"""Provides a module for launching Fluent in pim mode.

Examples
--------

>>> from ansys.fluent.core.launcher.launcher import create_launcher
>>> from ansys.fluent.core.launcher.pyfluent_enums import LaunchMode, FluentMode

>>> pim_meshing_launcher = create_launcher(LaunchMode.PIM, mode=FluentMode.MESHING)
>>> pim_meshing_session = pim_meshing_launcher()

>>> pim_solver_launcher = create_launcher(LaunchMode.PIM)
>>> pim_solver_session = pim_solver_launcher()
"""

import logging
import os
from typing import Any, Dict

from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.launcher.pyfluent_enums import (
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

_THIS_DIR = os.path.dirname(__file__)
_OPTIONS_FILE = os.path.join(_THIS_DIR, "fluent_launcher_options.json")
logger = logging.getLogger("pyfluent.launcher")


class PIMLauncher:
    """Instantiates Fluent session in `PIM <https://pypim.docs.pyansys.com/version/stable/>`_ mode."""

    def __init__(
        self,
        mode: FluentMode | str | None = None,
        ui_mode: UIMode | str | None = None,
        graphics_driver: (
            FluentWindowsGraphicsDriver | FluentLinuxGraphicsDriver | str | None
        ) = None,
        product_version: FluentVersion | str | float | int | None = None,
        dimension: Dimension | int | None = None,
        precision: Precision | str | None = None,
        processor_count: int | None = None,
        start_timeout: int = 60,
        additional_arguments: str | None = "",
        cleanup_on_exit: bool = True,
        start_transcript: bool = True,
        py: bool | None = None,
        gpu: bool | None = None,
        start_watchdog: bool | None = None,
        file_transfer_service: Any | None = None,
    ):
        """Launch Fluent session in `PIM <https://pypim.docs.pyansys.com/version/stable/>`_ mode.

        Parameters
        ----------
        mode : FluentMode
            Launch mode of Fluent to point to a specific session type.
        ui_mode : UIMode
            Fluent user interface mode. Options are the values of the ``UIMode`` enum.
        graphics_driver : FluentWindowsGraphicsDriver or FluentLinuxGraphicsDriver
            Graphics driver of Fluent. Options are the values of the
            ``FluentWindowsGraphicsDriver`` enum in Windows or the values of the
            ``FluentLinuxGraphicsDriver`` enum in Linux.
        product_version : FluentVersion or str or float or int, optional
            Version of Ansys Fluent to launch. To use Fluent version 2025 R1, pass
           ``FluentVersion.v251``, ``"25.1.0"``, ``"25.1"``, ``25.1``, or ``251``.
            The default is ``None``, in which case the newest installed version is used.
        dimension : Dimension or int, optional
            Geometric dimensionality of the Fluent simulation. The default is ``None``,
            in which case ``Dimension.THREE`` is used. Options are either the values of the
            ``Dimension`` enum (``Dimension.TWO`` or ``Dimension.THREE``) or any of ``2`` and ``3``.
        precision : Precision or str, optional
            Floating point precision. The default is ``None``, in which case ``Precision.DOUBLE``
            is used. Options are either the values of the ``Precision`` enum (``Precision.SINGLE``
            or ``Precision.DOUBLE``) or any of ``"double"`` and ``"single"``.
        processor_count : int, optional
            Number of processors. The default is ``None``, in which case ``1``
            processor is used.  In job scheduler environments the total number of
            allocated cores is clamped to value of ``processor_count``.
        start_timeout : int, optional
            Maximum allowable time in seconds for connecting to the Fluent
            server. The default is ``60``.
        additional_arguments : str, optional
            Additional arguments to send to Fluent as a string in the same
            format they are normally passed to Fluent on the command line.
        cleanup_on_exit : bool, optional
            Whether to shut down the connected Fluent session when PyFluent is
            exited, or the ``exit()`` method is called on the session instance,
            or if the session instance becomes unreferenced. The default is ``True``.
        start_transcript : bool, optional
            Whether to start streaming the Fluent transcript in the client. The
            default is ``True``. You can stop and start the streaming of the
            Fluent transcript subsequently via the method calls, ``transcript.start()``
            and ``transcript.stop()`` on the session object.
        py : bool, optional
            If True, Fluent will run in Python mode. Default is None.
        gpu : bool, optional
            If True, Fluent will start with GPU Solver.
        start_watchdog : bool, optional
            When ``cleanup_on_exit`` is True, ``start_watchdog`` defaults to True,
            which means an independent watchdog process is run to ensure
            that any local GUI-less Fluent sessions started by PyFluent are properly closed (or killed if frozen)
            when the current Python process ends.
        file_transfer_service : optional
            File transfer service. Uploads/downloads files to/from the server.

        Returns
        -------
        :obj:`~typing.Union` [:class:`Meshing<ansys.fluent.core.session_meshing.Meshing>`, \
        :class:`~ansys.fluent.core.session_pure_meshing.PureMeshing`, \
        :class:`~ansys.fluent.core.session_solver.Solver`, \
        :class:`~ansys.fluent.core.session_solver_icing.SolverIcing`, dict]
            Session object or configuration dictionary if ``dry_run = True``.

        Raises
        ------
        UnexpectedKeywordArgument
            If an unexpected keyword argument is provided.

        Notes
        -----
        Job scheduler environments such as SLURM, LSF, PBS, etc. allocates resources / compute nodes.
        The allocated machines and core counts are queried from the scheduler environment and
        passed to Fluent.
        """
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
        self.argvals, self.new_session = _get_argvals_and_session(locals().copy())
        self.file_transfer_service = file_transfer_service
        if self.argvals["start_timeout"] is None:
            self.argvals["start_timeout"] = 60

    def __call__(self):
        logger.info("Starting Fluent remotely. The startup configuration is ignored.")
        if self.argvals["product_version"]:
            fluent_product_version = str(
                FluentVersion(self.argvals["product_version"]).number
            )
        else:
            fluent_product_version = None

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

    When calling this method, you must ensure that you are in an
    environment where PyPIM is configured. You can use the :func:
    `pypim.is_configured <ansys.platform.instancemanagement.is_configured>`
    method to verify that PyPIM is configured.

    Parameters
    ----------
    session_cls: type(Meshing) | type(PureMeshing) | type(Solver) | type(SolverIcing)
        Session type.
    start_transcript: bool
        Whether to start streaming the Fluent transcript in the client. The
        default is ``True``. You can stop and start the streaming of the
        Fluent transcript subsequently via method calls on the session object.
    product_version : str, optional
        Version of Ansys Fluent to launch. Use ``"242"`` for 2024 R2.
        The default is ``None``, in which case the newest installed version is used.
    cleanup_on_exit : bool, optional
        Whether to clean up and exit Fluent when Python exits or when garbage
        is collected for the Fluent Python instance. The default is ``True``.
    mode : FluentMode, optional
        Whether to launch Fluent remotely in meshing mode. The default is
        ``FluentMode.SOLVER``.
    dimensionality : str, optional
        Geometric dimensionality of the Fluent simulation. The default is ``None``,
        in which case ``"3d"`` is used. Options are ``"3d"`` and ``"2d"``.
    file_transfer_service : optional
        File transfer service for uploading or downloading files to or from the server.
    launcher_args : Any
        Launcher arguments.

    Returns
    -------
    :obj:`~typing.Union` [:class:`Meshing<ansys.fluent.core.session_meshing.Meshing>`, \
    :class:`~ansys.fluent.core.session_pure_meshing.PureMeshing`, \
    :class:`~ansys.fluent.core.session_solver.Solver`, \
    :class:`~ansys.fluent.core.session_solver_icing.SolverIcing`]
        Session object.
    """
    pim = pypim.connect()
    instance = pim.create_instance(
        product_name=(
            "fluent-meshing"
            if FluentMode.is_meshing(mode)
            else "fluent-2ddp" if dimensionality == "2d" else "fluent-3ddp"
        ),
        product_version=product_version,
    )
    instance.wait_for_ready()
    # nb pymapdl sets max msg len here:
    channel = instance.build_grpc_channel()

    fluent_connection = FluentConnection(
        channel=channel,
        cleanup_on_exit=cleanup_on_exit,
        remote_instance=instance,
        slurm_job_id=launcher_args and launcher_args.get("slurm_job_id"),
    )

    file_transfer_service = (
        file_transfer_service
        if file_transfer_service
        else PimFileTransferService(pim_instance=fluent_connection._remote_instance)
    )

    return session_cls(
        fluent_connection=fluent_connection,
        scheme_eval=fluent_connection._connection_interface.scheme_eval,
        file_transfer_service=file_transfer_service,
        start_transcript=start_transcript,
    )
