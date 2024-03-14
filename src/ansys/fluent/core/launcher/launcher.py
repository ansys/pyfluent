"""Provides a module for launching Fluent.

This module supports both starting Fluent locally and connecting to a remote instance
with gRPC.
"""

import logging
import os
from typing import Any, Dict, Optional, Union
import warnings

from ansys.fluent.core.exceptions import DisallowedValuesError
from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.launcher.container_launcher import DockerLauncher
from ansys.fluent.core.launcher.error_handler import (
    GPUSolverSupportError,
    _process_invalid_args,
    _process_kwargs,
)
from ansys.fluent.core.launcher.launcher_utils import (
    _confirm_watchdog_start,
    is_windows,
)
from ansys.fluent.core.launcher.pim_launcher import PIMLauncher
from ansys.fluent.core.launcher.pyfluent_enums import (
    FluentLinuxGraphicsDriver,
    FluentMode,
    FluentWindowsGraphicsDriver,
    LaunchMode,
    UIMode,
    _get_fluent_launch_mode,
    _get_mode,
    _get_running_session_mode,
)
from ansys.fluent.core.launcher.server_info import _get_server_info
from ansys.fluent.core.launcher.slurm_launcher import SlurmFuture, SlurmLauncher
from ansys.fluent.core.launcher.standalone_launcher import StandaloneLauncher
import ansys.fluent.core.launcher.watchdog as watchdog
from ansys.fluent.core.session_meshing import Meshing
from ansys.fluent.core.session_pure_meshing import PureMeshing
from ansys.fluent.core.session_solver import Solver
from ansys.fluent.core.session_solver_icing import SolverIcing
from ansys.fluent.core.warnings import PyFluentDeprecationWarning

_THIS_DIR = os.path.dirname(__file__)
_OPTIONS_FILE = os.path.join(_THIS_DIR, "fluent_launcher_options.json")
logger = logging.getLogger("pyfluent.launcher")


def create_launcher(fluent_launch_mode: LaunchMode = None, **kwargs):
    """Factory function to create launcher for supported launch modes.

    Parameters
    ----------
    fluent_launch_mode: LaunchMode
        Supported Fluent launch modes. Options are ``"LaunchMode.CONTAINER"``,
        ``"LaunchMode.PIM"``, ``"LaunchMode.SLURM"``, and ``"LaunchMode.STANDALONE"``.
    kwargs : Any
        Keyword arguments.
    Returns
    -------
    launcher: Union[DockerLauncher, PimLauncher, StandaloneLauncher]
        Session launcher.
    Raises
    ------
    DisallowedValuesError
        If an unknown Fluent launch mode is passed.
    """
    allowed_options = [mode for mode in LaunchMode]
    if (
        not isinstance(fluent_launch_mode, LaunchMode)
        or fluent_launch_mode not in allowed_options
    ):
        raise DisallowedValuesError(
            "fluent_launch_mode",
            fluent_launch_mode,
            allowed_values=allowed_options,
        )
    if fluent_launch_mode == LaunchMode.STANDALONE:
        return StandaloneLauncher(**kwargs)
    elif fluent_launch_mode == LaunchMode.CONTAINER:
        return DockerLauncher(**kwargs)
    elif fluent_launch_mode == LaunchMode.PIM:
        return PIMLauncher(**kwargs)
    elif fluent_launch_mode == LaunchMode.SLURM:
        return SlurmLauncher(**kwargs)


#   pylint: disable=unused-argument
def launch_fluent(
    product_version: Optional[str] = None,
    version: Optional[str] = None,
    precision: Optional[str] = None,
    processor_count: Optional[int] = None,
    journal_file_names: Union[None, str, list[str]] = None,
    start_timeout: Optional[int] = None,
    additional_arguments: Optional[str] = "",
    env: Optional[Dict[str, Any]] = None,
    start_container: Optional[bool] = None,
    container_dict: Optional[dict] = None,
    dry_run: bool = False,
    cleanup_on_exit: bool = True,
    start_transcript: bool = True,
    ui_mode: Union[UIMode, str, None] = None,
    graphics_driver: Union[
        FluentWindowsGraphicsDriver, FluentLinuxGraphicsDriver, str, None
    ] = None,
    show_gui: Optional[bool] = None,
    case_file_name: Optional[str] = None,
    case_data_file_name: Optional[str] = None,
    lightweight_mode: Optional[bool] = None,
    mode: Optional[Union[FluentMode, str, None]] = None,
    py: Optional[bool] = None,
    gpu: Union[bool, list[int], None] = None,
    cwd: Optional[str] = None,
    topy: Optional[Union[str, list]] = None,
    start_watchdog: Optional[bool] = None,
    scheduler_options: Optional[dict] = None,
    file_transfer_service: Optional[Any] = None,
    **kwargs,
) -> Union[Meshing, PureMeshing, Solver, SolverIcing, SlurmFuture, dict]:
    """Launch Fluent locally in server mode or connect to a running Fluent server
    instance.

    Parameters
    ----------
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
        server. The default is ``60`` if Fluent is launched outside a Slurm environment,
        no timeout if Fluent is launched within a Slurm environment.
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
    ui_mode : UIMode or str, optional
        Fluent user interface mode. Options are either the values of the ``UIMode``
        enum or any of ``"no_gui_or_graphics"``, ``"no_gui"``, ``"hidden_gui"``,
        ``"no_graphics"`` or ``"gui"``. The default is ``UIMode.HIDDEN_GUI`` in
        Windows and ``UIMode.NO_GUI`` in Linux. ``"no_gui_or_graphics"`` and
        ``"no_gui"`` user interface modes are supported in Windows starting from Fluent
        version 2024 R1.
    graphics_driver : FluentWindowsGraphicsDriver or FluentLinuxGraphicsDriver or str, optional
        Graphics driver of Fluent. In Windows, options are either the values of the
        ``FluentWindowsGraphicsDriver`` enum or any of ``"null"``, ``"msw"``,
        ``"dx11"``, ``"opengl2"``, ``"opengl"`` or ``"auto"``. In Linux, options are
        either the values of the ``FluentLinuxGraphicsDriver`` enum or any of
       ``"null"``, ``"x11"``, ``"opengl2"``, ``"opengl"`` or ``"auto"``. The default is
       ``FluentWindowsGraphicsDriver.AUTO`` in Windows and
       ``FluentLinuxGraphicsDriver.AUTO`` in Linux.
    show_gui : bool, optional
        Whether to display the Fluent GUI. The default is ``None``, which does not
        cause the GUI to be shown. If a value of ``False`` is
        not explicitly provided, the GUI will also be shown if
        the environment variable ``PYFLUENT_SHOW_SERVER_GUI`` is set to 1.
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
    mode : str, optional
        Launch mode of Fluent to point to a specific session type.
        The default value is ``None``. Options are ``"meshing"``,
        ``"pure-meshing"`` and ``"solver"``.
    py : bool, optional
        If True, Fluent will run in Python mode. Default is None.
    gpu : bool or list, optional
        This option will start Fluent with the GPU Solver. A list of GPU IDs can be
        passed to use specific GPUs. If True is passed, the number of GPUs used will be
        clamped to the value of ``processor_count``. Please refer to
        *Starting the Fluent GPU Solver* section in *Fluent's User Guide* for more
        information like how to determine the GPU IDs.

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
    scheduler_options : dict, optional
        Dictionary containing scheduler options. Default is None.

        Currently only the Slurm scheduler is supported. The ``scheduler_options``
        dictionary must be of the form ``{"scheduler": "slurm",
        "scheduler_headnode": "<headnode>", "scheduler_queue": "<queue>",
        "scheduler_account": "<account>"}``. The keys ``scheduler_headnode``,
        ``scheduler_queue`` and ``scheduler_account`` are optional and should be
        specified in a similar manner to Fluent's scheduler options.
    file_transfer_service : optional
        File transfer service. Uploads/downloads files to/from the server.
    kwargs : Any
        Keyword arguments.

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
    if version != "3d" and gpu:
        raise GPUSolverSupportError()
    _process_kwargs(kwargs)
    del kwargs
    if show_gui is not None:
        warnings.warn(
            "'show_gui' is deprecated, use 'ui_mode' instead",
            PyFluentDeprecationWarning,
        )
    if show_gui or os.getenv("PYFLUENT_SHOW_SERVER_GUI") == "1":
        ui_mode = UIMode.GUI
    del show_gui
    if ui_mode is None:
        # Not using NO_GUI in windows as it opens a new cmd or
        # shows Fluent output in the current cmd if start <launch_string> is not used
        ui_mode = UIMode.HIDDEN_GUI if is_windows() else UIMode.NO_GUI
    if isinstance(ui_mode, str):
        ui_mode = UIMode(ui_mode)
    if graphics_driver is None:
        graphics_driver = "auto"
    graphics_driver = str(graphics_driver)
    graphics_driver = (
        FluentWindowsGraphicsDriver(graphics_driver)
        if is_windows()
        else FluentLinuxGraphicsDriver(graphics_driver)
    )
    fluent_launch_mode = _get_fluent_launch_mode(
        start_container=start_container,
        container_dict=container_dict,
        scheduler_options=scheduler_options,
    )
    del start_container
    mode = _get_mode(mode)
    argvals = locals().copy()
    _process_invalid_args(dry_run, fluent_launch_mode, argvals)
    fluent_launch_mode = argvals.pop("fluent_launch_mode")
    launcher = create_launcher(fluent_launch_mode, **argvals)
    return launcher()


def connect_to_fluent(
    ip: Optional[str] = None,
    port: Optional[int] = None,
    cleanup_on_exit: bool = False,
    start_transcript: bool = True,
    server_info_file_name: Optional[str] = None,
    password: Optional[str] = None,
    start_watchdog: Optional[bool] = None,
) -> Union[Meshing, PureMeshing, Solver, SolverIcing]:
    """Connect to an existing Fluent server instance.

    Parameters
    ----------
    ip : str, optional
        IP address for connecting to an existing Fluent instance. The
        IP address defaults to ``"127.0.0.1"``. You can also use the environment
        variable ``PYFLUENT_FLUENT_IP=<ip>`` to set this parameter.
        The explicit value of ``ip`` takes precedence over ``PYFLUENT_FLUENT_IP=<ip>``.
    port : int, optional
        Port to listen on for an existing Fluent instance. You can use the
        environment variable ``PYFLUENT_FLUENT_PORT=<port>`` to set a default
        value. The explicit value of ``port`` takes precedence over
        ``PYFLUENT_FLUENT_PORT=<port>``.
    cleanup_on_exit : bool, optional
        Whether to shut down the connected Fluent session when PyFluent is
        exited, or the ``exit()`` method is called on the session instance,
        or if the session instance becomes unreferenced. The default is ``False``.
    start_transcript : bool, optional
        Whether to start streaming the Fluent transcript in the client. The
        default is ``True``. You can stop and start the streaming of the
        Fluent transcript subsequently via the method calls, ``transcript.start()``
        and ``transcript.stop()`` on the session object.
    server_info_file_name: str
        Path to server-info file written out by Fluent server. The default is
        ``None``. PyFluent uses the connection information in the file to
        connect to a running Fluent session.
    password : str, optional
        Password to connect to existing Fluent instance.
    start_watchdog: bool, optional
        When ``cleanup_on_exit`` is True, ``start_watchdog`` defaults to True,
        which means an independent watchdog process is run to ensure
        that any local Fluent connections are properly closed (or terminated if frozen) when Python process ends.

    Returns
    -------
    :obj:`~typing.Union` [:class:`Meshing<ansys.fluent.core.session_meshing.Meshing>`, \
    :class:`~ansys.fluent.core.session_pure_meshing.PureMeshing`, \
    :class:`~ansys.fluent.core.session_solver.Solver`, \
    :class:`~ansys.fluent.core.session_solver_icing.SolverIcing`]
        Session object.
    """
    ip, port, password = _get_server_info(server_info_file_name, ip, port, password)
    fluent_connection = FluentConnection(
        ip=ip,
        port=port,
        password=password,
        cleanup_on_exit=cleanup_on_exit,
        start_transcript=start_transcript,
    )
    new_session = _get_running_session_mode(fluent_connection)

    start_watchdog = _confirm_watchdog_start(
        start_watchdog, cleanup_on_exit, fluent_connection
    )

    if start_watchdog:
        logger.info("Launching Watchdog for existing Fluent session...")
        ip, port, password = _get_server_info(server_info_file_name, ip, port, password)
        watchdog.launch(os.getpid(), port, password, ip)

    return new_session(
        fluent_connection=fluent_connection,
    )
