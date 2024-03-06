from enum import Enum
import os
from pathlib import Path
import platform
import subprocess
import tempfile
from typing import Any, Dict, Optional, Union

from ansys.fluent.core.exceptions import DisallowedValuesError
from ansys.fluent.core.fluent_connection import FluentConnection, PortNotProvided
from ansys.fluent.core.launcher.custom_exceptions import (
    DockerContainerLaunchNotSupported,
    InvalidPassword,
    IpPortNotProvided,
    UnexpectedKeywordArgument,
)
from ansys.fluent.core.launcher.launcher_utils import logger
from ansys.fluent.core.session import _parse_server_info_file
from ansys.fluent.core.session_meshing import Meshing
from ansys.fluent.core.session_pure_meshing import PureMeshing
from ansys.fluent.core.session_solver import Solver
from ansys.fluent.core.session_solver_icing import SolverIcing
from ansys.fluent.core.utils.fluent_version import FluentVersion
from ansys.fluent.core.utils.networking import find_remoting_ip
import ansys.platform.instancemanagement as pypim


class LaunchMode(Enum):
    """An enumeration over supported Fluent launch modes."""

    STANDALONE = 1
    PIM = 2
    CONTAINER = 3
    SLURM = 4


class FluentMode(Enum):
    """An enumeration over supported Fluent modes."""

    MESHING_MODE = (Meshing, "meshing")
    PURE_MESHING_MODE = (PureMeshing, "pure-meshing")
    SOLVER = (Solver, "solver")
    SOLVER_ICING = (SolverIcing, "solver-icing")

    @staticmethod
    def get_mode(mode: str) -> "FluentMode":
        """Returns the FluentMode based on the provided mode string.

        Parameters
        ----------
        mode : str
            mode

        Returns
        -------
        FluentMode
            Fluent mode

        Raises
        ------
        DisallowedValuesError
            If an unknown mode is passed.
        """
        allowed_modes = []
        for m in FluentMode:
            allowed_modes.append(m.value[1])
            if mode == m.value[1]:
                return m
        raise DisallowedValuesError("mode", mode, allowed_modes)

    @staticmethod
    def is_meshing(mode: "FluentMode") -> bool:
        """Returns whether the current mode is meshing.

        Parameters
        ----------
        mode : FluentMode
            mode

        Returns
        -------
        True if mode is FluentMode.MESHING_MODE or FluentMode.PURE_MESHING_MODE else False
            bool
        """
        return mode in [FluentMode.MESHING_MODE, FluentMode.PURE_MESHING_MODE]


def get_fluent_exe_path(**launch_argvals) -> Path:
    """Get Fluent executable path. The path is searched in the following order.

    1. ``product_version`` parameter passed with ``launch_fluent``.
    2. The latest ANSYS version from ``AWP_ROOTnnn``` environment variables.

    Returns
    -------
    Path
        Fluent executable path
    """

    def get_fluent_root(version: FluentVersion) -> Path:
        awp_root = os.environ[version.awp_var]
        return Path(awp_root) / "fluent"

    def get_exe_path(fluent_root: Path) -> Path:
        if _is_windows():
            return fluent_root / "ntbin" / "win64" / "fluent.exe"
        else:
            return fluent_root / "bin" / "fluent"

    # (DEV) "PYFLUENT_FLUENT_ROOT" environment variable
    fluent_root = os.getenv("PYFLUENT_FLUENT_ROOT")
    if fluent_root:
        return get_exe_path(Path(fluent_root))

    # Look for Fluent exe path in the following order:
    # 1. product_version parameter passed with launch_fluent
    product_version = launch_argvals.get("product_version")
    if product_version:
        return get_exe_path(get_fluent_root(FluentVersion(product_version)))

    # 2. the latest ANSYS version from AWP_ROOT environment variables
    return get_exe_path(get_fluent_root(FluentVersion.get_latest_installed()))


def _is_windows():
    """Check if the current operating system is windows."""
    return platform.system() == "Windows"


def _get_mode(mode: Optional[Union[FluentMode, str, None]] = None):
    """Updates the session information."""
    if mode is None:
        mode = FluentMode.SOLVER

    if isinstance(mode, str):
        mode = FluentMode.get_mode(mode)

    return mode


def _get_running_session_mode(
    fluent_connection: FluentConnection, mode: Optional[FluentMode] = None
):
    """Get the mode of the running session if the mode has not been mentioned
    explicitly."""
    if mode:
        session_mode = mode
    else:
        try:
            session_mode = FluentMode.get_mode(
                "solver"
                if fluent_connection.scheme_eval.scheme_eval("(cx-solver-mode?)")
                else "meshing"
            )
        except Exception as ex:
            raise InvalidPassword() from ex
    return session_mode.value[0]


def _get_fluent_launch_mode(start_container, container_dict, scheduler_options):
    """Get Fluent launch mode.

    Parameters
    ----------
    start_container: bool
        Specifies whether to launch a Fluent Docker container image.
    container_dict: dict
        Dictionary for Fluent Docker container configuration.

    Returns
    -------
    fluent_launch_mode: str
        Fluent launch mode.
    """
    if pypim.is_configured():
        fluent_launch_mode = "pim"
    elif start_container is True or (
        start_container is None
        and (container_dict or os.getenv("PYFLUENT_LAUNCH_CONTAINER") == "1")
    ):
        if check_docker_support():
            fluent_launch_mode = "container"
        else:
            raise DockerContainerLaunchNotSupported()
    elif scheduler_options and scheduler_options["scheduler"] == "slurm":
        fluent_launch_mode = "slurm"
    else:
        fluent_launch_mode = "standalone"
    return fluent_launch_mode


def _get_server_info_file_name(use_tmpdir=True):
    server_info_dir = os.getenv("SERVER_INFO_DIR")
    dir_ = (
        Path(server_info_dir)
        if server_info_dir
        else tempfile.gettempdir() if use_tmpdir else Path.cwd()
    )
    fd, file_name = tempfile.mkstemp(suffix=".txt", prefix="serverinfo-", dir=str(dir_))
    os.close(fd)
    return file_name


def _get_server_info(
    server_info_file_name: str,
    ip: Optional[str] = None,
    port: Optional[int] = None,
    password: Optional[str] = None,
):
    """Get server connection information of an already running session."""
    if not (ip and port) and not server_info_file_name:
        raise IpPortNotProvided()
    if (ip or port) and server_info_file_name:
        logger.warning(
            "The ip and port will be extracted from the server-info file and their explicitly specified values will be ignored."
        )
    else:
        if server_info_file_name:
            ip, port, password = _parse_server_info_file(server_info_file_name)
        ip = ip or os.getenv("PYFLUENT_FLUENT_IP", "127.0.0.1")
        port = port or os.getenv("PYFLUENT_FLUENT_PORT")

    if not port:
        raise PortNotProvided()

    return ip, port, password


def _get_subprocess_kwargs_for_fluent(env: Dict[str, Any], argvals) -> Dict[str, Any]:
    scheduler_options = argvals.get("scheduler_options")
    is_slurm = scheduler_options and scheduler_options["scheduler"] == "slurm"
    kwargs: Dict[str, Any] = {}
    if is_slurm:
        kwargs.update(stdout=subprocess.PIPE)
    if _is_windows():
        kwargs.update(shell=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    else:
        kwargs.update(shell=True, start_new_session=True)
    fluent_env = os.environ.copy()
    fluent_env.update({k: str(v) for k, v in env.items()})
    fluent_env["REMOTING_THROW_LAST_TUI_ERROR"] = "1"

    if not is_slurm:
        from ansys.fluent.core import INFER_REMOTING_IP

        if INFER_REMOTING_IP and not "REMOTING_SERVER_ADDRESS" in fluent_env:
            remoting_ip = find_remoting_ip()
            if remoting_ip:
                fluent_env["REMOTING_SERVER_ADDRESS"] = remoting_ip

    kwargs.update(env=fluent_env)
    return kwargs


def _process_kwargs(kwargs):
    """Verify whether keyword arguments are valid or not.

    Parameters
    ----------
    kwargs: Any
        Provided keyword arguments.

    Raises
    ------
    UnexpectedKeywordArgument
        If an unexpected keyword argument is provided.
    """
    if kwargs:
        if "meshing_mode" in kwargs:
            raise UnexpectedKeywordArgument(
                "Use 'launch_fluent(mode='meshing')' to launch Fluent in meshing mode."
            )
        else:
            raise UnexpectedKeywordArgument(
                f"launch_fluent() got an unexpected keyword argument {next(iter(kwargs))}"
            )


def _process_invalid_args(dry_run, fluent_launch_mode, argvals):
    """Get invalid arguments.

    Parameters
    ----------
    dry_run: bool
        If dry running a container start,
        ``launch_fluent()`` will return the configured ``container_dict``.
    fluent_launch_mode: str
        Fluent launch mode.
    argvals: dict
        Local arguments.
    """
    if dry_run and fluent_launch_mode != "container":
        logger.warning(
            "'dry_run' argument for 'launch_fluent' currently is only "
            "supported when starting containers."
        )
    if fluent_launch_mode != "standalone":
        arg_names = [
            "env",
            "cwd",
            "topy",
            "case_file_name",
            "lightweight_mode",
            "journal_file_names",
            "case_data_file_name",
        ]
        invalid_arg_names = list(
            filter(lambda arg_name: argvals[arg_name] is not None, arg_names)
        )
        if len(invalid_arg_names) != 0:
            invalid_str_names = ", ".join(invalid_arg_names)
            logger.warning(
                f"These specified arguments are only supported when starting "
                f"local standalone Fluent clients: {invalid_str_names}."
            )
