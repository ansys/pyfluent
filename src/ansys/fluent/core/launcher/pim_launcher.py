"""Provides a module for launching Fluent in pim mode.

Examples
--------

>>> from ansys.fluent.core.launcher.launcher import create_launcher
>>> from ansys.fluent.core.launcher.pyfluent_enums import LaunchMode

>>> pim_meshing_launcher = create_launcher(LaunchMode.PIM, mode="meshing")
>>> pim_meshing_session = pim_meshing_launcher()

>>> pim_solver_launcher = create_launcher(LaunchMode.PIM)
>>> pim_solver_session = pim_solver_launcher()
"""

import logging
import os
from typing import Any, Dict, Optional, Union

from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.launcher.error_handler import _process_invalid_args
from ansys.fluent.core.launcher.pyfluent_enums import (
    FluentLinuxGraphicsDriver,
    FluentMode,
    FluentWindowsGraphicsDriver,
    UIMode,
)
from ansys.fluent.core.session_meshing import Meshing
from ansys.fluent.core.session_pure_meshing import PureMeshing
from ansys.fluent.core.session_solver import Solver
from ansys.fluent.core.session_solver_icing import SolverIcing
from ansys.fluent.core.utils.file_transfer_service import PimFileTransferService
import ansys.platform.instancemanagement as pypim

_THIS_DIR = os.path.dirname(__file__)
_OPTIONS_FILE = os.path.join(_THIS_DIR, "fluent_launcher_options.json")
logger = logging.getLogger("pyfluent.launcher")


class PIMLauncher:
    """Instantiates Fluent session in `PIM <https://pypim.docs.pyansys.com/version/stable/>`_ mode."""

    def __init__(
        self,
        mode: FluentMode,
        ui_mode: UIMode,
        graphics_driver: Union[FluentWindowsGraphicsDriver, FluentLinuxGraphicsDriver],
        product_version: Optional[str] = None,
        version: Optional[str] = None,
        precision: Optional[str] = None,
        processor_count: Optional[int] = None,
        journal_file_names: Union[None, str, list[str]] = None,
        start_timeout: int = 60,
        additional_arguments: Optional[str] = "",
        env: Optional[Dict[str, Any]] = None,
        start_container: Optional[bool] = None,
        container_dict: Optional[dict] = None,
        dry_run: bool = False,
        cleanup_on_exit: bool = True,
        start_transcript: bool = True,
        case_file_name: Optional[str] = None,
        case_data_file_name: Optional[str] = None,
        lightweight_mode: Optional[bool] = None,
        py: Optional[bool] = None,
        gpu: Optional[bool] = None,
        cwd: Optional[str] = None,
        topy: Optional[Union[str, list]] = None,
        start_watchdog: Optional[bool] = None,
        scheduler_options: Optional[dict] = None,
        file_transfer_service: Optional[Any] = None,
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
        product_version : str, optional
            Version of Ansys Fluent to launch. The string must be in a format like
            ``"23.2.0"`` (for 2023 R2), matching the documented version format in the
            FluentVersion class. The default is ``None``, in which case the newest installed
            version is used.
        version : str, optional
            Geometric dimensionality of the Fluent simulation. The default is ``None``,
            in which case ``"3d"`` is used. Options are ``"3d"`` and ``"2d"``.
        precision : str, optional
            Floating point precision. The default is ``None``, in which case ``"double"``
            is used. Options are ``"double"`` and ``"single"``.
        processor_count : int, optional
            Number of processors. The default is ``None``, in which case ``1``
            processor is used.  In job scheduler environments the total number of
            allocated cores is clamped to value of ``processor_count``.
        journal_file_names : str or list of str, optional
            The string path to a Fluent journal file, or a list of such paths. Fluent will execute the
            journal(s). The default is ``None``.
        start_timeout : int, optional
            Maximum allowable time in seconds for connecting to the Fluent
            server. The default is ``60``.
        additional_arguments : str, optional
            Additional arguments to send to Fluent as a string in the same
            format they are normally passed to Fluent on the command line.
        env : dict[str, str], optional
            Mapping to modify environment variables in Fluent. The default
            is ``None``.
        start_container : bool, optional
            Specifies whether to launch a Fluent Docker container image. For more details about containers, see
            :mod:`~ansys.fluent.core.launcher.fluent_container`.
        container_dict : dict, optional
            Dictionary for Fluent Docker container configuration. If specified,
            setting ``start_container = True`` as well is redundant.
            Will launch Fluent inside a Docker container using the configuration changes specified.
            See also :mod:`~ansys.fluent.core.launcher.fluent_container`.
        dry_run : bool, optional
            Defaults to False. If True, will not launch Fluent, and will instead print configuration information
            that would be used as if Fluent was being launched. If dry running a container start,
            ``launch_fluent()`` will return the configured ``container_dict``.
        cleanup_on_exit : bool, optional
            Whether to shut down the connected Fluent session when PyFluent is
            exited, or the ``exit()`` method is called on the session instance,
            or if the session instance becomes unreferenced. The default is ``True``.
        start_transcript : bool, optional
            Whether to start streaming the Fluent transcript in the client. The
            default is ``True``. You can stop and start the streaming of the
            Fluent transcript subsequently via the method calls, ``transcript.start()``
            and ``transcript.stop()`` on the session object.
        case_file_name : str, optional
            If provided, the case file at ``case_file_name`` is read into the Fluent session.
        case_data_file_name : str, optional
            If provided, the case and data files at ``case_data_file_name`` are read into the Fluent session.
        lightweight_mode : bool, optional
            Whether to run in lightweight mode. In lightweight mode, the lightweight settings are read into the
            current Fluent solver session. The mesh is read into a background Fluent solver session which will
            replace the current Fluent solver session once the mesh read is complete and the lightweight settings
            made by the user in the current Fluent solver session have been applied in the background Fluent
            solver session. This is all orchestrated by PyFluent and requires no special usage.
            This parameter is used only when ``case_file_name`` is provided. The default is ``False``.
        py : bool, optional
            If True, Fluent will run in Python mode. Default is None.
        gpu : bool, optional
            If True, Fluent will start with GPU Solver.
        cwd : str, Optional
            Working directory for the Fluent client.
        topy : bool or str, optional
            A boolean flag to write the equivalent Python journal(s) from the journal(s) passed.
            Can optionally take the file name of the new python journal file.
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
        DockerContainerLaunchNotSupported
            If a Fluent Docker container launch is not supported.

        Notes
        -----
        Job scheduler environments such as SLURM, LSF, PBS, etc. allocates resources / compute nodes.
        The allocated machines and core counts are queried from the scheduler environment and
        passed to Fluent.
        """
        del start_container
        argvals = locals().copy()
        del argvals["self"]
        _process_invalid_args(dry_run, "pim", argvals)
        if argvals["start_timeout"] is None:
            argvals["start_timeout"] = 60
        for arg_name, arg_values in argvals.items():
            setattr(self, arg_name, arg_values)
        self.argvals = argvals
        self.new_session = self.mode.value[0]

        if self.additional_arguments:
            logger.warning(
                "'additional_arguments' option for 'launch_fluent' is currently not supported "
                "when starting a remote Fluent PyPIM client."
            )

        if self.start_watchdog:
            logger.warning(
                "'start_watchdog' argument for 'launch_fluent' is currently not supported "
                "when starting a remote Fluent PyPIM client."
            )
        self.file_transfer_service = (
            file_transfer_service if file_transfer_service else PimFileTransferService()
        )

    def __call__(self):
        logger.info(
            "Starting Fluent remotely. The startup configuration will be ignored."
        )
        if self.product_version:
            fluent_product_version = "".join(self.product_version.split("."))[:-1]
        else:
            fluent_product_version = None

        return launch_remote_fluent(
            session_cls=self.new_session,
            start_transcript=self.start_transcript,
            product_version=fluent_product_version,
            cleanup_on_exit=self.cleanup_on_exit,
            mode=self.mode,
            dimensionality=self.version,
            launcher_args=self.argvals,
            file_transfer_service=self.file_transfer_service,
        )


def launch_remote_fluent(
    session_cls,
    start_transcript: bool,
    product_version: Optional[str] = None,
    cleanup_on_exit: bool = True,
    mode: FluentMode = FluentMode.SOLVER,
    dimensionality: Optional[str] = None,
    launcher_args: Optional[Dict[str, Any]] = None,
    file_transfer_service: Optional[Any] = None,
) -> Union[Meshing, PureMeshing, Solver, SolverIcing]:
    """Launch Fluent remotely using `PyPIM <https://pypim.docs.pyansys.com>`.

    When calling this method, you must ensure that you are in an
    environment where PyPIM is configured. You can use the :func:
    `pypim.is_configured <ansys.platform.instancemanagement.is_configured>`
    method to verify that PyPIM is configured.

    Parameters
    ----------
    session_cls: Union[type(Meshing), type(PureMeshing), type(Solver), type(SolverIcing)]
        Session type.
    start_transcript: bool
        Whether to start streaming the Fluent transcript in the client. The
        default is ``True``. You can stop and start the streaming of the
        Fluent transcript subsequently via method calls on the session object.
    product_version : str, optional
        Ansys version to use. The string must be in a format like
        ``"23.2.0"`` (for 2023 R2), matching the documented version format in the
        FluentVersion class. The default is ``None``, in which case the newest installed
        version is used.
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
        start_transcript=start_transcript,
        launcher_args=launcher_args,
    )

    file_transfer_service = (
        file_transfer_service
        if file_transfer_service
        else PimFileTransferService(pim_instance=fluent_connection._remote_instance)
    )

    return session_cls(
        fluent_connection=fluent_connection, file_transfer_service=file_transfer_service
    )
