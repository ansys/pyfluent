"""Provides a module for launching Fluent in container mode.

Examples
--------

>>> from ansys.fluent.core.launcher.launcher import create_launcher
>>> from ansys.fluent.core.launcher.pyfluent_enums import LaunchMode, FluentMode

>>> container_meshing_launcher = create_launcher(LaunchMode.CONTAINER, mode=FluentMode.MESHING)
>>> container_meshing_session = container_meshing_launcher()

>>> container_solver_launcher = create_launcher(LaunchMode.CONTAINER)
>>> container_solver_session = container_solver_launcher()
"""

import logging
import os
from typing import Any

from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.launcher.fluent_container import (
    configure_container_dict,
    start_fluent_container,
)
from ansys.fluent.core.launcher.process_launch_string import (
    _build_fluent_launch_args_string,
)
from ansys.fluent.core.launcher.pyfluent_enums import (
    Dimension,
    FluentLinuxGraphicsDriver,
    FluentMode,
    FluentWindowsGraphicsDriver,
    Precision,
    UIMode,
    _get_argvals_and_session,
)
import ansys.fluent.core.launcher.watchdog as watchdog
from ansys.fluent.core.utils.fluent_version import FluentVersion

_THIS_DIR = os.path.dirname(__file__)
_OPTIONS_FILE = os.path.join(_THIS_DIR, "fluent_launcher_options.json")
logger = logging.getLogger("pyfluent.launcher")


class DockerLauncher:
    """Instantiates Fluent session in container mode."""

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
        container_dict: dict | None = None,
        dry_run: bool = False,
        cleanup_on_exit: bool = True,
        start_transcript: bool = True,
        py: bool | None = None,
        gpu: bool | None = None,
        start_watchdog: bool | None = None,
        file_transfer_service: Any | None = None,
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
        product_version : FluentVersion or str or float or int, optional
            Version of Ansys Fluent to launch. To use Fluent version 2025 R1, pass
            any of ``FluentVersion.v251``, ``"25.1.0"``, ``"25.1"``, ``25.1``, or ``251``.
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

        Notes
        -----
        Job scheduler environments such as SLURM, LSF, PBS, etc. allocates resources / compute nodes.
        The allocated machines and core counts are queried from the scheduler environment and
        passed to Fluent.
        """
        self.argvals, self.new_session = _get_argvals_and_session(locals().copy())
        if self.argvals["start_timeout"] is None:
            self.argvals["start_timeout"] = 60
        self.file_transfer_service = file_transfer_service
        if self.argvals["mode"] == FluentMode.SOLVER_ICING:
            self.argvals["fluent_icing"] = True
        if self.argvals["container_dict"] is None:
            self.argvals["container_dict"] = {}
        if self.argvals["product_version"]:
            self.argvals["container_dict"][
                "image_tag"
            ] = f"v{FluentVersion(self.argvals['product_version']).value}"

        self._args = _build_fluent_launch_args_string(**self.argvals).split()
        if FluentMode.is_meshing(self.argvals["mode"]):
            self._args.append(" -meshing")

    def __call__(self):
        if self.argvals["dry_run"]:
            config_dict, *_ = configure_container_dict(
                self._args, **self.argvals["container_dict"]
            )
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

        port, password, container = start_fluent_container(
            self._args, self.argvals["container_dict"]
        )

        fluent_connection = FluentConnection(
            port=port,
            password=password,
            file_transfer_service=self.file_transfer_service,
            cleanup_on_exit=self.argvals["cleanup_on_exit"],
            slurm_job_id=self.argvals and self.argvals.get("slurm_job_id"),
            inside_container=True,
        )

        session = self.new_session(
            fluent_connection=fluent_connection,
            scheme_eval=fluent_connection._connection_interface.scheme_eval,
            file_transfer_service=self.file_transfer_service,
            start_transcript=self.argvals["start_transcript"],
        )
        session._container = container

        if self.argvals["start_watchdog"] is None and self.argvals["cleanup_on_exit"]:
            self.argvals["start_watchdog"] = True
        if self.argvals["start_watchdog"]:
            logger.debug("Launching Watchdog for Fluent container...")
            watchdog.launch(os.getpid(), port, password)

        return session
