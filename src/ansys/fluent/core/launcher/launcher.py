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

"""Provides a module for launching Fluent.

This module supports both starting Fluent locally and connecting to a remote instance
with gRPC.
"""

import inspect
import logging
import os
from typing import Any, Literal, TypedDict, overload

from typing_extensions import Required, Unpack

import ansys.fluent.core as pyfluent
from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.launcher.container_launcher import DockerLauncher
from ansys.fluent.core.launcher.launch_options import (
    Dimension,
    FluentLinuxGraphicsDriver,
    FluentMode,
    FluentWindowsGraphicsDriver,
    LaunchMode,
    Precision,
    UIMode,
    _get_fluent_launch_mode,
    _get_running_session_mode,
)
from ansys.fluent.core.launcher.launcher_utils import (
    _confirm_watchdog_start,
    is_windows,
)
from ansys.fluent.core.launcher.pim_launcher import PIMLauncher
from ansys.fluent.core.launcher.server_info import _get_server_info
from ansys.fluent.core.launcher.slurm_launcher import SlurmFuture, SlurmLauncher
from ansys.fluent.core.launcher.standalone_launcher import StandaloneLauncher
import ansys.fluent.core.launcher.watchdog as watchdog
from ansys.fluent.core.session_meshing import Meshing
from ansys.fluent.core.session_pure_meshing import PureMeshing
from ansys.fluent.core.session_solver import Solver
from ansys.fluent.core.session_solver_aero import SolverAero
from ansys.fluent.core.session_solver_icing import SolverIcing
from ansys.fluent.core.utils.deprecate import all_deprecators
from ansys.fluent.core.utils.fluent_version import FluentVersion

_THIS_DIR = os.path.dirname(__file__)
_OPTIONS_FILE = os.path.join(_THIS_DIR, "fluent_launcher_options.json")
logger = logging.getLogger("pyfluent.launcher")


def create_launcher(fluent_launch_mode: LaunchMode, **kwargs):
    """Use the factory function to create a launcher for supported launch modes.

    Parameters
    ----------
    fluent_launch_mode: LaunchMode
        Supported Fluent launch modes. Options are ``"LaunchMode.CONTAINER"``,
        ``"LaunchMode.PIM"``, ``"LaunchMode.SLURM"``, and ``"LaunchMode.STANDALONE"``.
    kwargs : Any
        Keyword arguments.
    Returns
    -------
    launcher: DockerLauncher | PimLauncher | StandaloneLauncher
        Session launcher.
    Raises
    ------
    ValueError
        If an unknown Fluent launch mode is passed.
    """
    if fluent_launch_mode == LaunchMode.STANDALONE:
        return StandaloneLauncher(**kwargs)
    elif fluent_launch_mode == LaunchMode.CONTAINER:
        return DockerLauncher(**kwargs)
    elif fluent_launch_mode == LaunchMode.PIM:
        return PIMLauncher(**kwargs)
    elif fluent_launch_mode == LaunchMode.SLURM:
        return SlurmLauncher(**kwargs)
    raise ValueError(f"launch mode invalid: {fluent_launch_mode!r}")


def _show_gui_to_ui_mode(old_arg_val, **kwds):
    start_container = kwds.get("start_container")
    container_dict = kwds.get("container_dict")
    if old_arg_val is True:
        if start_container is True:
            return UIMode.NO_GUI
        elif container_dict:
            return UIMode.NO_GUI
        elif pyfluent.config.launch_fluent_container:
            return UIMode.NO_GUI
        else:
            return UIMode.GUI
    elif not old_arg_val:
        if is_windows():
            return UIMode.HIDDEN_GUI
        elif not is_windows():
            return UIMode.NO_GUI
        else:
            return None


def _version_to_dimension(old_arg_val):
    if old_arg_val == "2d":
        return Dimension.TWO
    elif old_arg_val == "3d":
        return Dimension.THREE
    else:
        return None


class LaunchFluentArgs(
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
    start_container: bool | None
    container_dict: dict[str, Any] | None
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
    topy: str | list | None
    start_watchdog: bool | None
    file_transfer_service: Any | None
    use_docker_compose: bool
    use_podman_compose: bool


class SlurmSchedulerOptions(
    TypedDict, total=False
):  # pylint: disable=missing-class-docstring
    scheduler: Required[Literal["slurm"]]
    scheduler_headnode: str
    scheduler_queue: str
    scheduler_account: str


@overload
def launch_fluent(
    *,
    dry_run: Literal[False] = False,
    mode: Literal[FluentMode.MESHING, "meshing"],
    **kwargs: Unpack[LaunchFluentArgs],
) -> Meshing: ...


@overload
def launch_fluent(
    *,
    dry_run: Literal[False] = False,
    mode: Literal[FluentMode.PURE_MESHING, "pure_meshing"],
    **kwargs: Unpack[LaunchFluentArgs],
) -> PureMeshing: ...


@overload
def launch_fluent(
    *,
    dry_run: Literal[False] = False,
    mode: Literal[FluentMode.SOLVER, "solver"] = FluentMode.SOLVER,
    **kwargs: Unpack[LaunchFluentArgs],
) -> Solver: ...


@overload
def launch_fluent(
    *,
    dry_run: Literal[False] = False,
    mode: Literal[FluentMode.SOLVER_ICING, "solver_icing"],
    **kwargs: Unpack[LaunchFluentArgs],
) -> SolverIcing: ...


@overload
def launch_fluent(
    *,
    dry_run: Literal[False] = False,
    mode: Literal[FluentMode.SOLVER_AERO, "solver_aero"] = ...,
    **kwargs: Unpack[LaunchFluentArgs],
) -> SolverAero: ...


@overload
def launch_fluent(
    *,
    dry_run: Literal[False] = False,
    scheduler_options: SlurmSchedulerOptions,
    mode: FluentMode | str = FluentMode.SOLVER,
    **kwargs: Unpack[LaunchFluentArgs],
) -> SlurmFuture: ...


@overload
def launch_fluent(
    *,
    dry_run: Literal[True],
    **kwargs: Unpack[LaunchFluentArgs],
) -> dict[str, Any]: ...


#   pylint: disable=unused-argument
@all_deprecators(
    deprecate_arg_mappings=[
        {
            "old_arg": "show_gui",
            "new_arg": "ui_mode",
            "converter": _show_gui_to_ui_mode,
        },
        {
            "old_arg": "version",
            "new_arg": "dimension",
            "converter": _version_to_dimension,
        },
    ],
    data_type_converter=None,
    deprecated_version="v0.22.dev0",
    deprecated_reason="'show_gui' and 'version' are deprecated. Use 'ui_mode' and 'dimension' instead.",
    warn_message="",
)
def launch_fluent(
    *,
    product_version: FluentVersion | str | float | int | None = None,
    dimension: Dimension | int = Dimension.THREE,
    precision: Precision | str = Precision.DOUBLE,
    processor_count: int | None = None,
    journal_file_names: None | str | list[str] = None,
    start_timeout: int | None = None,
    additional_arguments: str = "",
    env: dict[str, Any] | None = None,
    start_container: bool | None = None,
    container_dict: dict | None = None,
    dry_run: bool = False,
    cleanup_on_exit: bool = True,
    start_transcript: bool = True,
    ui_mode: UIMode | str | None = None,
    graphics_driver: (
        FluentWindowsGraphicsDriver | FluentLinuxGraphicsDriver | str | None
    ) = None,
    case_file_name: str | None = None,
    case_data_file_name: str | None = None,
    lightweight_mode: bool | None = None,
    mode: FluentMode | str = FluentMode.SOLVER,
    py: bool | None = None,
    gpu: bool | list[int] | None = None,
    cwd: str | None = None,
    fluent_path: str | None = None,
    topy: str | list | None = None,
    start_watchdog: bool | None = None,
    scheduler_options: SlurmSchedulerOptions | None = None,
    file_transfer_service: Any | None = None,
    use_docker_compose: bool = False,
    use_podman_compose: bool = False,
) -> (
    Meshing
    | PureMeshing
    | Solver
    | SolverIcing
    | SolverAero
    | SlurmFuture
    | dict[Any, Any]
):
    """Launch Fluent locally in server mode or connect to a running Fluent server
    instance.

    Parameters
    ----------
    product_version : FluentVersion or str or float or int, optional
        Version of Ansys Fluent to launch. To use Fluent version 2025 R1, pass
        any of  ``FluentVersion.v251``, ``"25.1.0"``, ``"25.1"``, ``25.1``or ``251``.
        The default is ``None``, in which case the newest installed version is used.
        PyFluent uses the ``AWP_ROOT<ver>`` environment variable to locate the Fluent
        installation, where ``<ver>`` is the Ansys release number such as ``251``.
        The ``AWP_ROOT<ver>`` environment variable is automatically configured on Windows
        system when Fluent is installed. On Linux systems, ``AWP_ROOT<ver>`` must be
        configured to point to the absolute path of an Ansys installation such as
        ``/apps/ansys_inc/v251``.
    dimension : Dimension or int, optional
        Geometric dimensionality of the Fluent simulation. The default is ``None``,
        in which case ``Dimension.THREE`` is used. Options are either the values of the
        ``Dimension`` enum (``Dimension.TWO`` or ``Dimension.THREE``) or any of ``2`` and ``3``.
    precision : Precision or str, optional
        Floating point precision. Options are either the values of the ``Precision`` enum (``Precision.SINGLE``
        or ``Precision.DOUBLE``) or any of ``"double"`` and ``"single"``.
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
        that would be used as if Fluent was being launched. If dry running a standalone start
        ``launch_fluent()`` will return a tuple containing Fluent launch string and the server info file name.
        If dry running a container start, ``launch_fluent()`` will return the configured ``container_dict``.
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
    mode : FluentMode or str or None, optional
        Launch mode of Fluent to point to a specific session type. Can be a
        ``FluentMode`` enum member or a string. The default value is ``SOLVER``.
        Valid string options include ``"meshing"``, ``"pure-meshing"``, and
        ``"solver"``.
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
    fluent_path: str, Optional
        User provided Fluent installation path.
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
    use_docker_compose: bool
        Whether to use Docker Compose to launch Fluent.
    use_podman_compose: bool
        Whether to use Podman Compose to launch Fluent.

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
    ValueError
        If both ``use_docker_compose`` and ``use_podman_compose`` are set to ``True``.

    Notes
    -----
    Job scheduler environments such as SLURM, LSF, PBS, etc. allocates resources / compute nodes.
    The allocated machines and core counts are queried from the scheduler environment and
    passed to Fluent.
    """
    if env is None:
        env = {}

    if use_docker_compose and use_podman_compose:
        raise ValueError(
            "Cannot use both 'use_docker_compose' and 'use_podman_compose' at the same time."
        )

    if start_timeout is None:
        start_timeout = pyfluent.config.launch_fluent_timeout

    def _mode_to_launcher_type(fluent_launch_mode: LaunchMode):
        launcher_mode_type = {
            LaunchMode.CONTAINER: DockerLauncher,
            LaunchMode.PIM: PIMLauncher,
            LaunchMode.SLURM: SlurmLauncher,
            LaunchMode.STANDALONE: StandaloneLauncher,
        }
        return launcher_mode_type[fluent_launch_mode]

    argvals = inspect.getargvalues(inspect.currentframe()).locals

    fluent_launch_mode = _get_fluent_launch_mode(
        start_container=start_container,
        container_dict=container_dict,
        scheduler_options=scheduler_options,
    )

    launcher_type = _mode_to_launcher_type(fluent_launch_mode)
    launch_fluent_args = set(inspect.signature(launch_fluent).parameters.keys())
    launcher_type_args = set(
        inspect.signature(launcher_type.__init__).parameters.keys()
    )
    common_args = launch_fluent_args.intersection(launcher_type_args)
    launcher_argvals = {arg: val for arg, val in argvals.items() if arg in common_args}
    if pyfluent.config.start_watchdog is False:
        launcher_argvals["start_watchdog"] = False
    launcher = launcher_type(**launcher_argvals)
    return launcher()


def connect_to_fluent(
    *,
    ip: str | None = None,
    port: int | None = None,
    cleanup_on_exit: bool = False,
    start_transcript: bool = True,
    server_info_file_name: str | None = None,
    password: str | None = None,
    start_watchdog: bool | None = None,
    file_transfer_service: Any | None = None,
) -> Meshing | PureMeshing | Solver | SolverIcing | SolverAero:
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
    file_transfer_service : optional
        File transfer service. Uploads/downloads files to/from the server.

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
        scheme_eval=fluent_connection._connection_interface.scheme_eval,
        start_transcript=start_transcript,
        file_transfer_service=file_transfer_service,
    )
