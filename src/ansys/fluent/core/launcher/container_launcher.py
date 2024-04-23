"""Provides a module for launching Fluent in container mode.

Examples
--------

>>> from ansys.fluent.core.launcher.launcher import create_launcher
>>> from ansys.fluent.core.launcher.pyfluent_enums import LaunchMode

>>> container_meshing_launcher = create_launcher(LaunchMode.CONTAINER, mode="meshing")
>>> container_meshing_session = container_meshing_launcher()

>>> container_solver_launcher = create_launcher(LaunchMode.CONTAINER)
>>> container_solver_session = container_solver_launcher()
"""

import logging
import os
from typing import Any, Optional, Union

from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.launcher.fluent_container import (
    configure_container_dict,
    start_fluent_container,
)
from ansys.fluent.core.launcher.process_launch_string import (
    _build_fluent_launch_args_string,
)
from ansys.fluent.core.launcher.pyfluent_enums import (
    FluentLinuxGraphicsDriver,
    FluentMode,
    FluentWindowsGraphicsDriver,
    UIMode,
)
import ansys.fluent.core.launcher.watchdog as watchdog
from ansys.fluent.core.utils.file_transfer_service import RemoteFileTransferStrategy
from ansys.fluent.core.utils.fluent_version import FluentVersion

_THIS_DIR = os.path.dirname(__file__)
_OPTIONS_FILE = os.path.join(_THIS_DIR, "fluent_launcher_options.json")
logger = logging.getLogger("pyfluent.launcher")


class DockerLauncher:
    """Instantiates Fluent session in container mode."""

    def __init__(
        self,
        mode: FluentMode,
        ui_mode: UIMode,
        graphics_driver: Union[FluentWindowsGraphicsDriver, FluentLinuxGraphicsDriver],
        product_version: Optional[FluentVersion] = None,
        version: Optional[str] = None,
        precision: Optional[str] = None,
        processor_count: Optional[int] = None,
        start_timeout: int = 60,
        additional_arguments: Optional[str] = "",
        container_dict: Optional[dict] = None,
        dry_run: bool = False,
        cleanup_on_exit: bool = True,
        start_transcript: bool = True,
        py: Optional[bool] = None,
        gpu: Optional[bool] = None,
        start_watchdog: Optional[bool] = None,
        file_transfer_service: Optional[Any] = None,
    ):
        """Launch Fluent session in container mode.

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
        product_version : FluentVersion, optional
            Version of Ansys Fluent to launch. Use ``FluentVersion.v241`` for 2024 R1.
            The default is ``None``, in which case the newest installed version is used.
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
        start_timeout : int, optional
            Maximum allowable time in seconds for connecting to the Fluent
            server. The default is ``60``.
        additional_arguments : str, optional
            Additional arguments to send to Fluent as a string in the same
            format they are normally passed to Fluent on the command line.
        container_dict : dict, optional
            Dictionary for Fluent Docker container configuration. The configuration settings specified in this
            dictionary are used to launch Fluent inside a Docker container.
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
        DockerContainerLaunchNotSupported
            If a Fluent Docker container launch is not supported.

        Notes
        -----
        Job scheduler environments such as SLURM, LSF, PBS, etc. allocates resources / compute nodes.
        The allocated machines and core counts are queried from the scheduler environment and
        passed to Fluent.
        """
        argvals = locals().copy()
        del argvals["self"]
        if argvals["start_timeout"] is None:
            argvals["start_timeout"] = 60
        for arg_name, arg_values in argvals.items():
            setattr(self, arg_name, arg_values)
        self.argvals = argvals
        self.new_session = self.mode.value[0]
        self.file_transfer_service = (
            file_transfer_service
            if file_transfer_service
            else RemoteFileTransferStrategy()
        )

    def __call__(self):
        if self.mode == FluentMode.SOLVER_ICING:
            self.argvals["fluent_icing"] = True
        args = _build_fluent_launch_args_string(**self.argvals).split()
        if FluentMode.is_meshing(self.mode):
            args.append(" -meshing")
        if self.container_dict is None:
            setattr(self, "container_dict", {})
        if self.product_version:
            self.container_dict["image_tag"] = f"v{self.product_version.value}"
        if self.dry_run:
            config_dict, *_ = configure_container_dict(args, **self.container_dict)
            from pprint import pprint

            print("\nDocker container run configuration:\n")
            print("config_dict = ")
            if os.getenv("PYFLUENT_HIDE_LOG_SECRETS") != "1":
                pprint(config_dict)
            else:
                config_dict_h = config_dict.copy()
                config_dict_h.pop("environment")
                pprint(config_dict_h)
                del config_dict_h
            return config_dict

        port, password = start_fluent_container(args, self.container_dict)

        fluent_connection = FluentConnection(
            port=port,
            password=password,
            cleanup_on_exit=self.cleanup_on_exit,
            slurm_job_id=self.argvals and self.argvals.get("slurm_job_id"),
            inside_container=True,
        )

        session = self.new_session(
            fluent_connection=fluent_connection,
            scheme_eval=fluent_connection._connection_interface.scheme_eval,
            file_transfer_service=self.file_transfer_service,
            start_transcript=self.start_transcript,
        )

        if self.start_watchdog is None and self.cleanup_on_exit:
            setattr(self, "start_watchdog", True)
        if self.start_watchdog:
            logger.debug("Launching Watchdog for Fluent container...")
            watchdog.launch(os.getpid(), port, password)

        return session
