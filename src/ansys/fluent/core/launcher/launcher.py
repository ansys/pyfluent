"""Provides a module for launching Fluent.

This module supports both starting Fluent locally and connecting to a
remote instance with gRPC.
"""
from enum import Enum
import json
import os
from pathlib import Path
import platform
import subprocess
import tempfile
import time
from typing import Any, Dict, Union
import warnings

from ansys.fluent.core.fluent_connection import _FluentConnection
from ansys.fluent.core.launcher.fluent_container import start_fluent_container
from ansys.fluent.core.session import Session, _BaseSession, parse_server_info_file
from ansys.fluent.core.session_meshing import Meshing
from ansys.fluent.core.session_pure_meshing import PureMeshing
from ansys.fluent.core.session_solver import Solver
from ansys.fluent.core.session_solver_icing import SolverIcing
from ansys.fluent.core.session_solver_lite import SolverLite
from ansys.fluent.core.utils.logging import LOG
import ansys.platform.instancemanagement as pypim

_THIS_DIR = os.path.dirname(__file__)
_OPTIONS_FILE = os.path.join(_THIS_DIR, "fluent_launcher_options.json")
FLUENT_VERSION = ["22.2"]
PIM_FLUENT_PRODUCT_VERSION = [FLUENT_VERSION[0].replace(".", "")]
FLUENT_EXE_PATH = []


class FluentVersion(Enum):
    """Contains the standard Ansys Fluent release."""

    version_22R2 = "22.2"
    version_23R1 = "23.1"

    @staticmethod
    def get_version(version: str) -> "FluentVersion":
        """Get the available versions based on the version in string format."""
        for v in FluentVersion:
            if version == v.value:
                return v
        else:
            raise RuntimeError(f"The passed version '{version}' does not exist.")


def set_fluent_path(fluent_exe_path: Union[str, Path]) -> None:
    """Set the Fluent installation path manually.

    This supersedes the Fluent path set in the environment variable.
    """
    if Path(fluent_exe_path).exists() and Path(fluent_exe_path).name == "fluent.exe":
        FLUENT_EXE_PATH.append(str(fluent_exe_path))
    else:
        raise RuntimeError(
            f"The passed path '{fluent_exe_path}' does not contain a valid Fluent executable file."
        )


def set_ansys_version(version: Union[str, float, FluentVersion]) -> None:
    """Set the Fluent version manually.

    This method only works if the provided Fluent version is installed
    and the environment variables are updated properly. This supersedes
    the Fluent path set in the environment variable.
    """
    if type(version) in [float, str]:
        version = FluentVersion.get_version(str(version))
    if version in FluentVersion or str(version) in FluentVersion.value:
        FLUENT_VERSION[0] = version.value
        PIM_FLUENT_PRODUCT_VERSION[0] = FLUENT_VERSION[0].replace(".", "")


class LaunchModes(Enum):
    """Provides the standard Fluent launch modes."""

    # Tuple:   Name, Solver object type, Meshing flag, Launcher options
    MESHING_MODE = ("meshing", Meshing, True, [])
    PURE_MESHING_MODE = ("pure-meshing", PureMeshing, True, [])
    SOLVER = ("solver", Solver, False, [])
    SOLVER_LITE = ("solver-lite", SolverLite, False, [])
    SOLVER_ICING = ("solver-icing", SolverIcing, False, [("fluent_icing", True)])

    @staticmethod
    def get_mode(mode: str) -> "LaunchModes":
        """Returns the LaunchMode based on the mode in string format."""
        for m in LaunchModes:
            if mode == m.value[0]:
                return m
        else:
            raise RuntimeError(
                f"The passed mode '{mode}' matches none of the allowed modes."
            )


def get_fluent_path() -> Path:
    """Get the local Fluent installation path specified by PYFLUENT_FLUENT_ROOT
    or AWP_ROOTXXX environment variable.

    Returns
    -------
    str
        Local Fluent installation path.
    """
    if "PYFLUENT_FLUENT_ROOT" in os.environ:
        path = os.environ["PYFLUENT_FLUENT_ROOT"]
        return Path(path)
    else:
        path = os.environ["AWP_ROOT" + "".join(FLUENT_VERSION[0].split("."))]
        return Path(path) / "fluent"


def _get_fluent_exe_path():
    exe_path = get_fluent_path()
    if platform.system() == "Windows":
        exe_path = exe_path / "ntbin" / "win64" / "fluent.exe"
    else:
        exe_path = exe_path / "bin" / "fluent"
    return str(exe_path)


def _get_server_info_filepath():
    server_info_dir = os.getenv("SERVER_INFO_DIR")
    dir_ = Path(server_info_dir) if server_info_dir else tempfile.gettempdir()
    fd, filepath = tempfile.mkstemp(suffix=".txt", prefix="serverinfo-", dir=str(dir_))
    os.close(fd)
    return filepath


def _get_subprocess_kwargs_for_fluent(env: Dict[str, Any]) -> Dict[str, Any]:
    kwargs: Dict[str, Any] = {}
    kwargs.update(stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if platform.system() == "Windows":
        kwargs.update(
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            | subprocess.DETACHED_PROCESS
        )
    else:
        kwargs.update(shell=True, start_new_session=True)
    fluent_env = os.environ.copy()
    fluent_env.update({k: str(v) for k, v in env.items()})
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
                    LOG.warning(
                        "Default value %s is chosen for %s as the passed "
                        "value  %s is outside allowed values %s.",
                        argval,
                        k,
                        old_argval,
                        allowed_values,
                    )
                else:
                    LOG.warning(
                        "%s = %s is discarded as it is outside " "allowed values %s.",
                        k,
                        argval,
                        allowed_values,
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
    return launch_args_string


def launch_remote_fluent(
    session_cls,
    product_version: str = None,
    cleanup_on_exit: bool = True,
    meshing_mode: bool = False,
    dimensionality: str = None,
):

    """Launch Fluent remotely using the PIM (Product Instance Management) API.

    When calling this method, you must ensure that you are in an
    environment where PyPIM is configured. You can use the :func:
    `pypim.is_configured <ansys.platform.instancemanagement.is_configured>`
    method to verify that PYPIM is configured.

    Parameters
    ----------
    product_version : str, optional
        Version of Fluent to use in the three-digit format (such as ``"212"``
        for 2021 R2). The default is ``None``, in which case the active version
        or latest installed version is used.
    cleanup_on_exit : bool, optional
        Whether to clean up and exit Fluent when Python exits or when garbage
        is collected for the Fluent Python instance. The default is ``True``.
    meshing_mode : bool, optional
        Whether to launch Fluent remotely in meshing mode. The default is
        ``False``.
    dimensionality : str, optional
        Number of dimensions for modeling. The default is ``None``, in which
        case ``"3s"`` is used. Options are ``"3d"`` and ``"2d"``.

    Returns
    -------
    ansys.fluent.core.session.Session
        Instance of the session.
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
    return session_cls(
        fluent_connection=_FluentConnection(
            channel=channel, cleanup_on_exit=cleanup_on_exit, remote_instance=instance
        )
    )


#   pylint: disable=unused-argument
def launch_fluent(
    version: str = None,
    precision: str = None,
    processor_count: int = None,
    journal_filename: str = None,
    start_timeout: int = 100,
    additional_arguments: str = "",
    env: Dict[str, Any] = None,
    start_instance: bool = None,
    ip: str = None,
    port: int = None,
    cleanup_on_exit: bool = True,
    start_transcript: bool = True,
    show_gui: bool = None,
    case_filepath: str = None,
    meshing_mode: bool = None,
    mode: Union[LaunchModes, str, None] = None,
    server_info_filepath: str = None,
    password: str = None,
) -> Union[_BaseSession, Session]:
    """Launch Fluent locally in server mode or connect to a running Fluent
    server instance.

    Parameters
    ----------
    version : str, optional
        Dimensions for modeling. The default is ``None``, in which case ``"3d"``
        is used. Options are ``"3d"`` and ``"2d"``.
    precision : str, optional
        Floating point precision. The default is ``None``, in which case ``"double"``
        is used. Options are ``"double"`` and ``"single"``.
    processor_count : int, optional
        Number of processors. The default is ``None``, in which case ``1``
        is used.
    journal_filename : str, optional
        Name of the journal file to read. The default is ``None``.
    start_timeout : int, optional
        Maximum allowable time in seconds for connecting to the Fluent
        server. The default is ``100``.
    additional_arguments : str, optional
        Additional arguments to send to Fluent. The default is ``""``.
    env : dict[str, str], optional
        Mapping to modify environment variables in Fluent. The default
        is ``None``.
    start_instance : bool, optional
        Whether to connect to an existing Fluent instance at a specified IP
        address on a specified port. The default is ``None``, in which
        case a local instance of Fluent is started. When ``False``, use
        the next two parameters to specify the IP address and port. You
        can also use the environment variable ``PYFLUENT_START_INSTANCE=<0 or 1>``
        to set this parameter.
    ip : str, optional
        IP address for connecting to an existing Fluent instance. This parameter
        is used only when ``start_instance`` is ``False``. Otherwise, the
        IP address defaults to ``"127.0.0.1"``. You can also use the environment
        variable ``PYFLUENT_FLUENT_IP=<ip>`` to set this parameter.
    port : int, optional
        Port to listen on for an existing Fluent instance. This parameter is
        used only when ``start_instance`` is ``False``. You can use the
        environment variable ``PYFLUENT_FLUENT_PORT=<port>`` to set a default
        value.
    cleanup_on_exit : bool, optional
        Whether to shut down the connected Fluent session when PyFluent is
        exited or the ``exit()`` method is called on the session instance.
        The default is ``True``.
    start_transcript : bool, optional
        Whether to start streaming the Fluent transcript in the client. The
        default is ``True``. You can stop and start the streaming of the
        Fluent transcript subsequently via method calls on the session object.
    show_gui : bool, optional
        Whether to display the Fluent GUI when ``start_instance``
        is set to ''True``. The default is ``None`` so that explicit
        ``False`` settings can be detected. This is because you can use
        also use the environment variable ``PYFLUENT_SHOW_SERVER_GUI=<0 or 1>``
        to set this parameter. The ``show-gui`` parameter overrides the
        PYFLUENT_SHOW_SERVER_GUI environment variable. For example, if
        PYFLUENT_SHOW_SERVER_GUI is set to ``1`` and the ``show-gui``
        parameter is set to ``False``, the GUI is hidden.
    case_filepath : str, optional
        If provided, reads a fluent case file and sets the required settings
        in the fluent session
    meshing_mode : bool, optional
        Whether to launch Fluent in meshing mode. The default is ``None``,
        in which case Fluent is launched in meshing mode.
    mode : str, optional
        Launch mode of Fluent to point to a specific session type.
        The default value is ``None``. Options are ``"meshing"``,
        ``"pure-meshing"``, ``"solver"``, and ``"solver-lite"``.
    server_info_filepath: str
        Path to server-info file written out by Fluent server. The default is ``None``.
    password : str, optional
            Password to connect to existing Fluent instance.

    Returns
    -------
    ansys.fluent.session.Session
        Fluent session.
    """
    argvals = locals()

    if mode is None:
        new_session = Session
    elif mode and meshing_mode:
        raise RuntimeError(
            "Please select either of the 2 ways of running ('mode' or 'meshing_mode')"
        )
    else:
        if type(mode) == str:
            mode = LaunchModes.get_mode(mode)
        new_session = mode.value[1]
        meshing_mode = mode.value[2]
        for k, v in mode.value[3]:
            argvals[k] = v

    if start_instance is None:
        start_instance = bool(
            int(
                os.getenv(
                    "PYFLUENT_START_INSTANCE", "0" if pypim.is_configured() else "1"
                )
            )
        )
    if start_instance:
        if FLUENT_EXE_PATH:
            exe_path = FLUENT_EXE_PATH[0]
        else:
            exe_path = _get_fluent_exe_path()
        launch_string = exe_path
        launch_string += _build_fluent_launch_args_string(**argvals)
        if meshing_mode:
            launch_string += " -meshing"

        server_info_filepath = _get_server_info_filepath()
        try:
            launch_string += f" {additional_arguments}"
            launch_string += f' -sifile="{server_info_filepath}"'
            launch_string += " -nm"
            if (show_gui is False) or (
                show_gui is None and (os.getenv("PYFLUENT_SHOW_SERVER_GUI") != "1")
            ):
                launch_string += " -hidden"
            LOG.info("Launching Fluent with cmd: %s", launch_string)
            sifile_last_mtime = Path(server_info_filepath).stat().st_mtime
            if env is None:
                env = {}
            if mode != LaunchModes.SOLVER_ICING:
                env["APP_LAUNCHED_FROM_CLIENT"] = "1"  # disables flserver datamodel
            kwargs = _get_subprocess_kwargs_for_fluent(env)
            subprocess.Popen(launch_string, **kwargs)
            while True:
                if Path(server_info_filepath).stat().st_mtime > sifile_last_mtime:
                    time.sleep(1)
                    LOG.info("Fluent process is successfully launched.")
                    break
                if start_timeout == 0:
                    LOG.error("The launch process has been timed out.")
                    break
                time.sleep(1)
                start_timeout -= 1
                LOG.info(
                    "Waiting for Fluent to launch...%02d seconds remaining",
                    start_timeout,
                )
            return new_session.create_from_server_info_file(
                server_info_filepath, cleanup_on_exit, start_transcript
            )
        finally:
            server_info_file = Path(server_info_filepath)
            if server_info_file.exists():
                server_info_file.unlink()
    else:
        if pypim.is_configured():
            LOG.info(
                "Starting Fluent remotely. The startup configuration will be ignored."
            )
            return launch_remote_fluent(
                session_cls=new_session,
                product_version=PIM_FLUENT_PRODUCT_VERSION[0],
                cleanup_on_exit=cleanup_on_exit,
                meshing_mode=meshing_mode,
                dimensionality=version,
            )
        import ansys.fluent.core as pyfluent

        if pyfluent.BUILDING_GALLERY or os.getenv("PYFLUENT_LAUNCH_CONTAINER") == "1":
            args = _build_fluent_launch_args_string(**argvals).split()
            if meshing_mode:
                args.append(" -meshing")
            # Assumes the container OS will be able to create the
            # EXAMPLES_PATH of host OS. With the Fluent docker
            # container, the following currently works only in linux.
            port = start_fluent_container(
                pyfluent.EXAMPLES_PATH, pyfluent.EXAMPLES_PATH, args
            )
            return new_session(
                fluent_connection=_FluentConnection(
                    port=port,
                    cleanup_on_exit=cleanup_on_exit,
                    start_transcript=start_transcript,
                )
            )
        else:
            ip = argvals.get("ip", None)
            port = argvals.get("port", None)
            if ip and port:
                warnings.warn(
                    "The server-info file was not parsed because ip and port were provided explicitly."
                )
            elif server_info_filepath:
                ip, port, password = parse_server_info_file(server_info_filepath)
            elif os.getenv("PYFLUENT_FLUENT_IP") and os.getenv("PYFLUENT_FLUENT_PORT"):
                pass
            else:
                raise RuntimeError(
                    "Please provide either ip and port data or server-info file."
                )

            fluent_connection = _FluentConnection(
                ip=ip,
                port=port,
                password=password,
                cleanup_on_exit=cleanup_on_exit,
                start_transcript=start_transcript,
            )
            if mode:
                session_mode = mode
            else:
                try:
                    session_mode = LaunchModes.get_mode(
                        fluent_connection.get_current_fluent_mode()
                    )
                except BaseException:
                    raise RuntimeError("Fluent session password mismatch")

            new_session = session_mode.value[1]
            return new_session(fluent_connection=fluent_connection)
