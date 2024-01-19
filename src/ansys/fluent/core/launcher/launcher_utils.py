"""Provides a module for launching utilities."""

from enum import Enum
import json
import logging
import os
from pathlib import Path
import platform
import socket
import subprocess
import tempfile
import time
from typing import Any, Dict, Optional, Union

from beartype import beartype

from ansys.fluent.core.exceptions import DisallowedValuesError, InvalidArgument
from ansys.fluent.core.fluent_connection import FluentConnection, PortNotProvided
from ansys.fluent.core.scheduler import build_parallel_options, load_machines
from ansys.fluent.core.session import _parse_server_info_file
from ansys.fluent.core.session_meshing import Meshing
from ansys.fluent.core.session_pure_meshing import PureMeshing
from ansys.fluent.core.session_solver import Solver
from ansys.fluent.core.session_solver_icing import SolverIcing
from ansys.fluent.core.utils.file_transfer_service import (
    PimFileTransferService,
    RemoteFileHandler,
)
from ansys.fluent.core.utils.fluent_version import FluentVersion
from ansys.fluent.core.utils.networking import find_remoting_ip
import ansys.platform.instancemanagement as pypim

_THIS_DIR = os.path.dirname(__file__)
_OPTIONS_FILE = os.path.join(_THIS_DIR, "fluent_launcher_options.json")
logger = logging.getLogger("pyfluent.launcher")


class InvalidPassword(ValueError):
    """Provides the error when password is invalid."""

    def __init__(self):
        super().__init__("Provide correct 'password'.")


class IpPortNotProvided(ValueError):
    """Provides the error when ip and port are not specified."""

    def __init__(self):
        super().__init__("Provide either 'ip' and 'port' or 'server_info_file_name'.")


class UnexpectedKeywordArgument(TypeError):
    """Provides the error when a valid keyword argument is not specified."""

    pass


class DockerContainerLaunchNotSupported(SystemError):
    """Provides the error when docker container launch is not supported."""

    def __init__(self):
        super().__init__("Python Docker SDK is unsupported on this system.")


def _is_windows():
    """Check if the current operating system is windows."""
    return platform.system() == "Windows"


class LaunchMode(Enum):
    """An enumeration over supported Fluent launch modes."""

    STANDALONE = 1
    PIM = 2
    CONTAINER = 3
    SLURM = 4


def check_docker_support():
    """Checks whether Python Docker SDK is supported by the current system."""
    import docker

    try:
        _ = docker.from_env()
    except docker.errors.DockerException:
        return False
    return True


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


class FluentMode(Enum):
    """An enumeration over supported Fluent modes."""

    # Tuple: Name, Solver object type, Meshing flag, Launcher options
    MESHING_MODE = ("meshing", Meshing, True, [])
    PURE_MESHING_MODE = ("pure-meshing", PureMeshing, True, [])
    SOLVER = ("solver", Solver, False, [])
    SOLVER_ICING = ("solver-icing", SolverIcing, False, [("fluent_icing", True)])

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
        for m in FluentMode:
            if mode == m.value[0]:
                return m
        else:
            raise DisallowedValuesError(
                "mode", mode, ["meshing", "pure-meshing", "solver", "solver-icing"]
            )


def _get_server_info_file_name(use_tmpdir=True):
    server_info_dir = os.getenv("SERVER_INFO_DIR")
    dir_ = (
        Path(server_info_dir)
        if server_info_dir
        else tempfile.gettempdir()
        if use_tmpdir
        else Path.cwd()
    )
    fd, file_name = tempfile.mkstemp(suffix=".txt", prefix="serverinfo-", dir=str(dir_))
    os.close(fd)
    return file_name


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


def _build_fluent_launch_args_string(**kwargs) -> str:
    """Build Fluent's launch arguments string from keyword arguments.

    Returns
    -------
    str
        Fluent's launch arguments string.
    """
    all_options = None
    with open(_OPTIONS_FILE, encoding="utf-8") as fp:
        all_options = json.load(fp)
    launch_args_string = ""
    for k, v in all_options.items():
        argval = kwargs.get(k)
        default = v.get("default")
        if argval is None and v.get("fluent_required") is True:
            argval = default
        if argval is not None:
            allowed_values = v.get("allowed_values")
            if allowed_values and argval not in allowed_values:
                if default is not None:
                    old_argval = argval
                    argval = default
                    logger.warning(
                        f"Specified value '{old_argval}' for argument '{k}' is not an allowed value ({allowed_values}), default value '{argval}' is going to be used instead."
                    )
                else:
                    logger.warning(
                        f"{k} = {argval} is discarded as it is not an allowed value. Allowed values: {allowed_values}"
                    )
                    continue
            fluent_map = v.get("fluent_map")
            if fluent_map:
                if isinstance(argval, str):
                    json_key = argval
                else:
                    json_key = json.dumps(argval)
                argval = fluent_map[json_key]
            launch_args_string += v["fluent_format"].replace("{}", str(argval))
    addArgs = kwargs["additional_arguments"]
    if "-t" not in addArgs and "-cnf=" not in addArgs:
        parallel_options = build_parallel_options(
            load_machines(ncores=kwargs["processor_count"])
        )
        if parallel_options:
            launch_args_string += " " + parallel_options
    return launch_args_string


def _get_session_info(argvals, mode: Optional[Union[FluentMode, str, None]] = None):
    """Updates the session information."""
    if mode is None:
        mode = FluentMode.SOLVER

    if isinstance(mode, str):
        mode = FluentMode.get_mode(mode)
    new_session = mode.value[1]
    meshing_mode = mode.value[2]
    for k, v in mode.value[3]:
        argvals[k] = v

    return new_session, meshing_mode, argvals, mode


def _raise_exception_g_gu_in_windows_os(additional_arguments: str) -> None:
    """If -g or -gu is passed in Windows OS, the exception should be raised."""
    additional_arg_list = additional_arguments.split()
    if _is_windows() and (
        ("-g" in additional_arg_list) or ("-gu" in additional_arg_list)
    ):
        raise InvalidArgument("Unsupported '-g' and '-gu' on windows platform.")


def _update_launch_string_wrt_gui_options(
    launch_string: str, show_gui: Optional[bool] = None, additional_arguments: str = ""
) -> str:
    """Checks for all gui options in additional arguments and updates the launch string
    with hidden, if none of the options are met."""

    if (show_gui is False) or (
        show_gui is None and (os.getenv("PYFLUENT_SHOW_SERVER_GUI") != "1")
    ):
        if not {"-g", "-gu"} & set(additional_arguments.split()):
            launch_string += " -hidden"

    return launch_string


def _await_fluent_launch(
    server_info_file_name: str, start_timeout: int, sifile_last_mtime: float
):
    """Wait for successful fluent launch or raise an error."""
    while True:
        if Path(server_info_file_name).stat().st_mtime > sifile_last_mtime:
            time.sleep(1)
            logger.info("Fluent has been successfully launched.")
            break
        if start_timeout == 0:
            raise TimeoutError("The launch process has timed out.")
        time.sleep(1)
        start_timeout -= 1
        logger.info(f"Waiting for Fluent to launch...")
        if start_timeout >= 0:
            logger.info(f"...{start_timeout} seconds remaining")


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
    return session_mode.value[1]


def _generate_launch_string(
    argvals,
    meshing_mode: bool,
    show_gui: bool,
    additional_arguments: str,
    server_info_file_name: str,
):
    """Generates the launch string to launch fluent."""
    if _is_windows():
        exe_path = str(get_fluent_exe_path(**argvals))
        if " " in exe_path:
            exe_path = '"' + exe_path + '"'
    else:
        exe_path = str(get_fluent_exe_path(**argvals))
    launch_string = exe_path
    launch_string += _build_fluent_launch_args_string(**argvals)
    if meshing_mode:
        launch_string += " -meshing"
    if additional_arguments:
        launch_string += f" {additional_arguments}"
    if " " in server_info_file_name:
        server_info_file_name = '"' + server_info_file_name + '"'
    launch_string += f" -sifile={server_info_file_name}"
    launch_string += " -nm"
    launch_string = _update_launch_string_wrt_gui_options(
        launch_string, show_gui, additional_arguments
    )
    return launch_string


def _confirm_watchdog_start(start_watchdog, cleanup_on_exit, fluent_connection):
    """Confirm whether Fluent is running locally, and whether the Watchdog should be
    started."""
    if start_watchdog is None and cleanup_on_exit:
        host = fluent_connection.connection_properties.cortex_host
        if host == socket.gethostname():
            logger.debug(
                "Fluent running on the host machine and 'cleanup_on_exit' activated, will launch Watchdog."
            )
            start_watchdog = True
    return start_watchdog


@beartype
def _build_journal_argument(
    topy: Union[None, bool, str], journal_file_names: Union[None, str, list[str]]
) -> str:
    """Build Fluent commandline journal argument."""
    if topy and not journal_file_names:
        raise InvalidArgument(
            "Use 'journal_file_names' to specify and convert journal files."
        )
    fluent_jou_arg = ""
    if isinstance(journal_file_names, str):
        journal_file_names = [journal_file_names]
    if journal_file_names:
        fluent_jou_arg += "".join(
            [f' -i "{journal}"' for journal in journal_file_names]
        )
    if topy:
        if isinstance(topy, str):
            fluent_jou_arg += f' -topy="{topy}"'
        else:
            fluent_jou_arg += " -topy"
    return fluent_jou_arg


# pylint: disable=missing-raises-doc
class LaunchFluentError(Exception):
    """Exception class representing launch errors."""

    def __init__(self, launch_string):
        """__init__ method of LaunchFluentError class."""
        details = "\n" + "Fluent Launch string: " + launch_string
        super().__init__(details)


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


def _get_argvals(argvals, mode):
    """Update local arguments.

    Parameters
    ----------
    argvals: dict
        Local arguments.
    mode : str
        Launch mode of Fluent to point to a specific session type.
        Options are ``"meshing"``, ``"pure-meshing"`` and ``"solver"``.

    Returns
    -------
    argvals: dict
        Updated local arguments.
    """
    new_session, meshing_mode, argvals, mode = _get_session_info(argvals, mode)
    argvals = locals().copy()
    return argvals


def launch_remote_fluent(
    session_cls,
    start_transcript: bool,
    product_version: Optional[str] = None,
    cleanup_on_exit: bool = True,
    meshing_mode: bool = False,
    dimensionality: Optional[str] = None,
    launcher_args: Optional[Dict[str, Any]] = None,
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
        Select an installed version of ANSYS. The string must be in a format like
        ``"23.2.0"`` (for 2023 R2) matching the documented version format in the
        FluentVersion class. The default is ``None``, in which case the newest installed
        version is used.
    cleanup_on_exit : bool, optional
        Whether to clean up and exit Fluent when Python exits or when garbage
        is collected for the Fluent Python instance. The default is ``True``.
    meshing_mode : bool, optional
        Whether to launch Fluent remotely in meshing mode. The default is
        ``False``.
    dimensionality : str, optional
        Geometric dimensionality of the Fluent simulation. The default is ``None``,
        in which case ``"3d"`` is used. Options are ``"3d"`` and ``"2d"``.

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
        product_name="fluent-meshing"
        if meshing_mode
        else "fluent-2ddp"
        if dimensionality == "2d"
        else "fluent-3ddp",
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

    remote_file_handler = RemoteFileHandler(
        transfer_service=PimFileTransferService(
            pim_instance=fluent_connection._remote_instance
        )
    )

    return session_cls(
        fluent_connection=fluent_connection, remote_file_handler=remote_file_handler
    )
