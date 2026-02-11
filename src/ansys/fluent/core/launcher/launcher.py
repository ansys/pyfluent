# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
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

import logging
import os
from typing import Any, Literal, TypedDict, cast, overload
from warnings import warn

from typing_extensions import Required, Unpack, assert_never

import ansys.fluent.core as pyfluent
from ansys.fluent.core._types import LauncherArgsBase, PathType
from ansys.fluent.core.exceptions import DisallowedValuesError
from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.launcher.container_launcher import DockerLauncher
from ansys.fluent.core.launcher.error_warning_messages import (
    ALLOW_REMOTE_HOST_NOT_PROVIDED_WITH_CERTIFICATES_FOLDER,
    ALLOW_REMOTE_HOST_NOT_PROVIDED_WITH_INSECURE_MODE,
    CERTIFICATES_FOLDER_NOT_PROVIDED_AT_CONNECT,
    CERTIFICATES_FOLDER_PROVIDED_IN_STANDALONE,
    INSECURE_MODE_PROVIDED_IN_STANDALONE,
)
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
    get_remote_grpc_options,
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
from ansys.fluent.core.session import BaseSession
from ansys.fluent.core.session_meshing import Meshing
from ansys.fluent.core.session_pure_meshing import PureMeshing
from ansys.fluent.core.session_solver import Solver
from ansys.fluent.core.session_solver_aero import SolverAero
from ansys.fluent.core.session_solver_icing import SolverIcing
from ansys.fluent.core.utils.deprecate import deprecate_arguments
from ansys.fluent.core.utils.fluent_version import FluentVersion

__all__ = (
    "create_launcher",
    "launch_fluent",
    "connect_to_fluent",
)

_THIS_DIR = os.path.dirname(__file__)
_OPTIONS_FILE = os.path.join(_THIS_DIR, "fluent_launcher_options.json")
logger = logging.getLogger("pyfluent.launcher")


def create_launcher(
    fluent_launch_mode: LaunchMode = LaunchMode.STANDALONE, **kwargs
) -> DockerLauncher | PIMLauncher | SlurmLauncher | StandaloneLauncher:
    """Use the factory function to create a launcher for supported launch modes.

    Parameters
    ----------
    fluent_launch_mode: LaunchMode
        Supported Fluent launch modes. Options are ``"LaunchMode.CONTAINER"``,
        ``"LaunchMode.PIM"``, ``"LaunchMode.SLURM"``, and ``"LaunchMode.STANDALONE"``.
        The default is ``"LaunchMode.STANDALONE"``.
    kwargs : Any
        Keyword arguments.
    Returns
    -------
    DockerLauncher | PIMLauncher | SlurmLauncher | StandaloneLauncher
        Session launcher.
    Raises
    ------
    ValueError
        If an unknown Fluent launch mode is passed.
    """
    launchers = {
        LaunchMode.STANDALONE: StandaloneLauncher,
        LaunchMode.CONTAINER: DockerLauncher,
        LaunchMode.PIM: PIMLauncher,
        LaunchMode.SLURM: SlurmLauncher,
    }

    if fluent_launch_mode in launchers:
        return launchers[fluent_launch_mode](**kwargs)
    else:
        raise DisallowedValuesError(
            "launch mode",
            fluent_launch_mode,
            [f"LaunchMode.{m.name}" for m in LaunchMode],
        )


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


class LaunchFluentArgs(LauncherArgsBase, TypedDict, total=False):
    """Arguments for launch_fluent()."""

    journal_file_names: None | str | list[str]
    """The string path to a Fluent journal file, or a list of such paths. Fluent will execute the
    journal(s). The default is ``None``.
    """
    env: dict[str, Any] | None
    """Mapping to modify environment variables in Fluent. The default
    is ``None``.
    """
    start_container: bool | None
    """Specifies whether to launch a Fluent Docker container image. For more details about containers, see
    :mod:`~ansys.fluent.core.launcher.fluent_container`.
    """
    container_dict: dict[str, Any] | None
    """Dictionary for Fluent Docker container configuration. If specified,
    setting ``start_container = True`` as well is redundant.
    Will launch Fluent inside a Docker container using the configuration changes specified.
    See also :mod:`~ansys.fluent.core.launcher.fluent_container`.
    """
    case_file_name: str | None
    """If provided, the case file at ``case_file_name`` is read into the Fluent session."""
    case_data_file_name: str | None
    """If provided, the case and data files at ``case_data_file_name`` are read into the Fluent session."""
    lightweight_mode: bool | None
    """Whether to run in lightweight mode. In lightweight mode, the lightweight settings are read into the
    current Fluent solver session. The mesh is read into a background Fluent solver session which will
    replace the current Fluent solver session once the mesh read is complete and the lightweight settings
    made by the user in the current Fluent solver session have been applied in the background Fluent
    solver session. This is all orchestrated by PyFluent and requires no special usage.
    This parameter is used only when ``case_file_name`` is provided. The default is ``False``.
    """
    py: bool | None
    """If True, Fluent will run in Python mode. Default is None."""
    cwd: str | None
    """Working directory for the Fluent client."""
    fluent_path: str | None
    """User provided Fluent installation path."""
    topy: str | list[Any] | None
    """A boolean flag to write the equivalent Python journal(s) from the journal(s) passed.
    Can optionally take the file name of the new python journal file.
    """
    use_docker_compose: bool
    """Whether to use Docker Compose to launch Fluent."""
    use_podman_compose: bool
    """Whether to use Podman Compose to launch Fluent."""


class SlurmSchedulerOptions(
    TypedDict, total=False
):  # pylint: disable=missing-class-docstring
    scheduler: Required[Literal["slurm"]]
    """Currently only the Slurm scheduler is supported."""
    scheduler_headnode: str
    """The keys ``scheduler_headnode``, ``scheduler_queue`` and ``scheduler_account`` are optional and should be
    specified in a similar manner to Fluent's scheduler options.
    """
    scheduler_queue: str
    """The keys ``scheduler_headnode``, ``scheduler_queue`` and ``scheduler_account`` are optional and should be
    specified in a similar manner to Fluent's scheduler options.
    """
    scheduler_account: str
    """The keys ``scheduler_headnode``, ``scheduler_queue`` and ``scheduler_account`` are optional and should be
    specified in a similar manner to Fluent's scheduler options.
    """


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
    mode: Literal[FluentMode.SOLVER_AERO, "solver_aero"],
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
) -> tuple[str, str]: ...


def _custom_converter_gui(kwargs):
    old_val = kwargs.pop("show_gui", None)
    kwargs["ui_mode"] = _show_gui_to_ui_mode(old_val, **kwargs)
    return kwargs


def _custom_converter_dimension(kwargs):
    old_val = kwargs.pop("version", None)
    kwargs["dimension"] = _version_to_dimension(old_val)
    return kwargs


@deprecate_arguments(
    old_args="show_gui",
    new_args="ui_mode",
    version="v0.22.0",
    converter=_custom_converter_gui,
)
@deprecate_arguments(
    old_args="version",
    new_args="dimension",
    version="v0.22.0",
    converter=_custom_converter_dimension,
)
def launch_fluent(
    *,
    product_version: FluentVersion | str | float | int | None = None,
    dimension: Dimension | Literal[2, 3] = Dimension.THREE,
    precision: Precision | Literal["single", "double"] = Precision.DOUBLE,
    processor_count: int = 1,
    journal_file_names: None | str | list[str] = None,
    start_timeout: int | None = None,
    additional_arguments: str = "",
    env: dict[str, Any] | None = None,
    start_container: bool | None = None,
    container_dict: dict[str, Any] | None = None,
    dry_run: bool = False,
    cleanup_on_exit: bool = True,
    start_transcript: bool = True,
    ui_mode: UIMode | str | None = None,
    graphics_driver: (
        FluentWindowsGraphicsDriver | FluentLinuxGraphicsDriver | str | None
    ) = None,
    case_file_name: "PathType | None" = None,
    case_data_file_name: "PathType | None" = None,
    lightweight_mode: bool | None = None,
    mode: FluentMode | str = FluentMode.SOLVER,
    py: bool | None = None,
    gpu: bool | list[int] | None = None,
    cwd: "PathType | None" = None,
    fluent_path: "PathType | None" = None,
    topy: str | list[Any] | None = None,
    start_watchdog: bool | None = None,
    scheduler_options: SlurmSchedulerOptions | None = None,
    file_transfer_service: Any | None = None,
    use_docker_compose: bool = False,
    use_podman_compose: bool = False,
    certificates_folder: str | None = None,
    insecure_mode: bool = False,
) -> (
    Meshing
    | PureMeshing
    | Solver
    | SolverIcing
    | SolverAero
    | SlurmFuture
    | tuple[str, str]
):
    """Launch Fluent locally in server mode or connect to a running Fluent server
    instance.

    Returns
    -------
    :obj:`~typing.Union` [:class:`Meshing<ansys.fluent.core.session_meshing.Meshing>`, \
    :class:`~ansys.fluent.core.session_pure_meshing.PureMeshing`, \
    :class:`~ansys.fluent.core.session_solver.Solver`, \
    :class:`~ansys.fluent.core.session_solver_icing.SolverIcing`, tuple[str, str]]
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

    start_timeout_val = (
        start_timeout
        if start_timeout is not None
        else pyfluent.config.launch_fluent_timeout
    )

    def _normalize_path(value: "PathType | None") -> str | None:
        if value is None or isinstance(value, str):
            return value
        return os.fspath(value)

    case_file_name_val = _normalize_path(case_file_name)
    case_data_file_name_val = _normalize_path(case_data_file_name)
    cwd_val = _normalize_path(cwd)
    fluent_path_val = _normalize_path(fluent_path)

    fluent_launch_mode = _get_fluent_launch_mode(
        start_container=start_container,
        container_dict=container_dict,
        scheduler_options=scheduler_options,
    )

    if fluent_launch_mode == LaunchMode.STANDALONE and certificates_folder is not None:
        warn(
            CERTIFICATES_FOLDER_PROVIDED_IN_STANDALONE,
            UserWarning,
        )

    if fluent_launch_mode == LaunchMode.STANDALONE and insecure_mode:
        warn(
            INSECURE_MODE_PROVIDED_IN_STANDALONE,
            UserWarning,
        )

    if pyfluent.config.start_watchdog is False:
        start_watchdog = False

    match fluent_launch_mode:
        case LaunchMode.CONTAINER:
            launcher = DockerLauncher(
                mode=mode,
                ui_mode=ui_mode,
                graphics_driver=graphics_driver,
                product_version=product_version,
                dimension=dimension,
                precision=precision,
                processor_count=processor_count,
                start_timeout=start_timeout_val,
                additional_arguments=additional_arguments,
                container_dict=container_dict,
                dry_run=dry_run,
                cleanup_on_exit=cleanup_on_exit,
                start_transcript=start_transcript,
                py=py,
                gpu=gpu,
                start_watchdog=start_watchdog,
                file_transfer_service=file_transfer_service,
                use_docker_compose=use_docker_compose,
                use_podman_compose=use_podman_compose,
                certificates_folder=certificates_folder,
                insecure_mode=insecure_mode,
            )
        case LaunchMode.PIM:
            launcher = PIMLauncher(
                mode=mode,
                ui_mode=ui_mode,
                graphics_driver=graphics_driver,
                product_version=product_version,
                dimension=dimension,
                precision=precision,
                processor_count=processor_count,
                start_timeout=start_timeout_val,
                additional_arguments=additional_arguments,
                cleanup_on_exit=cleanup_on_exit,
                start_transcript=start_transcript,
                gpu=gpu,
                start_watchdog=start_watchdog,
                file_transfer_service=file_transfer_service,
            )
        case LaunchMode.SLURM:
            launcher = SlurmLauncher(
                mode=mode,
                ui_mode=ui_mode,
                graphics_driver=graphics_driver,
                product_version=product_version,
                dimension=dimension,
                precision=precision,
                processor_count=processor_count,
                journal_file_names=journal_file_names,
                start_timeout=start_timeout_val,
                additional_arguments=additional_arguments,
                env=env,
                cleanup_on_exit=cleanup_on_exit,
                start_transcript=start_transcript,
                case_file_name=case_file_name_val,
                case_data_file_name=case_data_file_name_val,
                lightweight_mode=lightweight_mode,
                py=py,
                gpu=gpu,
                cwd=cwd_val,
                fluent_path=fluent_path_val,
                topy=topy,
                start_watchdog=start_watchdog,
                scheduler_options=(
                    dict(scheduler_options) if scheduler_options is not None else None
                ),
                file_transfer_service=file_transfer_service,
                certificates_folder=certificates_folder,
                insecure_mode=insecure_mode,
            )
        case LaunchMode.STANDALONE:
            launcher = StandaloneLauncher(
                mode=FluentMode(mode),
                dry_run=dry_run,
                product_version=product_version,
                dimension=dimension,
                precision=precision,
                processor_count=processor_count,
                journal_file_names=journal_file_names,
                start_timeout=start_timeout_val,
                additional_arguments=additional_arguments,
                env=env,
                cleanup_on_exit=cleanup_on_exit,
                start_transcript=start_transcript,
                ui_mode=ui_mode,
                graphics_driver=graphics_driver,
                case_file_name=case_file_name_val,
                case_data_file_name=case_data_file_name_val,
                lightweight_mode=lightweight_mode,
                py=py,
                gpu=gpu,
                cwd=cwd_val,
                fluent_path=fluent_path_val,
                topy=topy,
                start_watchdog=start_watchdog,
                file_transfer_service=file_transfer_service,
            )
        case _:
            assert_never(fluent_launch_mode)

    return cast(
        Meshing | PureMeshing | Solver | SolverIcing | SolverAero | tuple[str, str],
        launcher(),
    )


def connect_to_fluent(
    *,
    ip: str | None = None,
    port: int | None = None,
    address: str | None = None,
    cleanup_on_exit: bool = False,
    start_transcript: bool = True,
    server_info_file_name: str | None = None,
    password: str | None = None,
    allow_remote_host: bool = False,
    certificates_folder: str | None = None,
    insecure_mode: bool = False,
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
    address : str, optional
        Address for connecting to an existing Fluent instance. The address
        can be a TCP address of the form ``<ip>:<port>`` or a Unix domain
        socket of the form ``unix:/<path>``. The default is ``None``.
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
    allow_remote_host : bool, optional
        Whether to allow connecting to a remote Fluent instance.
    certificates_folder : str, optional
        Path to the folder containing TLS certificates for Fluent's gRPC server.
    insecure_mode : bool, optional
        If True, Fluent's gRPC server will be connected in insecure mode without TLS.
        This mode is not recommended. For more details on the implications
        and usage of insecure mode, refer to the Fluent documentation.
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

    Raises
    -------
    ValueError
        Raised when neither `certificates_folder` nor `insecure_mode` are set while `allow_remote_host` is True.
        Raised when both `certificates_folder` and `insecure_mode` are set simultaneously.
        Raised when `certificates_folder` is set but `allow_remote_host` is False.
        Raised when `insecure_mode` is set but `allow_remote_host` is False.
    """
    if allow_remote_host:
        certificates_folder, insecure_mode = get_remote_grpc_options(
            certificates_folder, insecure_mode
        )
        if certificates_folder is None and not insecure_mode:
            raise ValueError(CERTIFICATES_FOLDER_NOT_PROVIDED_AT_CONNECT)
    else:
        if certificates_folder is not None:
            raise ValueError(ALLOW_REMOTE_HOST_NOT_PROVIDED_WITH_CERTIFICATES_FOLDER)
        if insecure_mode:
            raise ValueError(ALLOW_REMOTE_HOST_NOT_PROVIDED_WITH_INSECURE_MODE)

    if address is None:
        values = _get_server_info(server_info_file_name, ip, port, password)
        if len(values) == 2:
            address, password = values
            ip, port = None, None
        else:
            ip, port, password = values

    fluent_connection = FluentConnection(
        ip=ip,
        port=port,
        password=password,
        address=address,
        allow_remote_host=allow_remote_host,
        certificates_folder=certificates_folder,
        insecure_mode=insecure_mode,
        cleanup_on_exit=cleanup_on_exit,
    )
    new_session = _get_running_session_mode(fluent_connection)

    start_watchdog = _confirm_watchdog_start(
        start_watchdog, cleanup_on_exit, fluent_connection
    )

    if start_watchdog:
        logger.info("Launching Watchdog for existing Fluent session...")
        if ip is not None and port is not None and password is not None:
            watchdog.launch(
                os.getpid(),
                port,
                password,
                ip,
                allow_remote_host=allow_remote_host,
                certificates_folder=certificates_folder,
                insecure_mode=insecure_mode,
            )

    return new_session(
        fluent_connection=fluent_connection,
        scheme_eval=fluent_connection._connection_interface.scheme_eval,
        start_transcript=start_transcript,
        file_transfer_service=file_transfer_service,
    )
