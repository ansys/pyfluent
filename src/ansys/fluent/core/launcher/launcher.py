"""Provide a module for launching Fluent.

This module supports both starting Fluent locally or connecting to a
remote instance with gRPC.
"""

import json
import os
from pathlib import Path
import platform
import subprocess
import tempfile
import time
from typing import Any, Dict

from ansys.fluent.core.launcher.fluent_container import start_fluent_container
from ansys.fluent.core.session import Session
from ansys.fluent.core.utils.logging import LOG

_THIS_DIR = os.path.dirname(__file__)
_OPTIONS_FILE = os.path.join(_THIS_DIR, "fluent_launcher_options.json")
FLUENT_VERSION = "22.2"


def _get_fluent_path():
    if "PYFLUENT_FLUENT_ROOT" in os.environ:
        path = os.environ["PYFLUENT_FLUENT_ROOT"]
        return Path(path)
    else:
        path = os.environ["AWP_ROOT" + "".join(FLUENT_VERSION.split("."))]
        return Path(path) / "fluent"


def _get_fluent_exe_path():
    exe_path = _get_fluent_path()
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
        Fluent's launch arguments string
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


#   pylint: disable=unused-argument
def launch_fluent(
    version: str = None,
    precision: str = None,
    processor_count: int = None,
    journal_filename: str = None,
    meshing_mode: bool = None,
    start_timeout: int = 100,
    additional_arguments: str = "",
    env: Dict[str, Any] = None,
    start_instance: bool = None,
    ip: str = None,
    port: int = None,
    cleanup_on_exit: bool = True,
    show_gui: bool = None,
) -> Session:
    """Start Fluent locally in server mode or connect to a running Fluent
    server instance.

    Parameters
    ----------
    version : str, optional
        Selects either the ``"2d"`` or ``"3d"`` version of Fluent.
        Default is ``"3d"``.

    precision : str, optional
        Selects either the ``"single"`` precision or ``"double"``
        precision version of Fluent. Default is ``"double"`` precision.

    processor_count : int, optional
        Specify number of processors. Default is 1.

    journal_filename : str, optional
        Read the specified journal file.

    meshing_mode : bool, optional
        Launch Fluent in meshing mode

    start_timeout : int, optional
        Maximum allowable time in seconds to connect to the Fluent
        server. Default is 100 seconds.

    additional_arguments : str, optional
        Additional arguments in string format which will be sent to
        Fluent launcher as is.

    env : Dict[str, str], optional
        Mapping to modify environment variables in Fluent

    start_instance : bool, optional
        When False, connect to an existing Fluent instance at ``ip``
        and ``port``. Otherwise, launch a local instance of Fluent.
        Defaults to True and can also be set by the environment variable
        ``PYFLUENT_START_INSTANCE=<0 or 1>``.

    ip : str, optional
        IP address to connect to existing Fluent instance. Used only
        when ``start_instance`` is ``False``.  Defaults to
        ``"127.0.0.1"`` and can also be set by the environment variable
        ``PYFLUENT_FLUENT_IP=<ip>``.

    port : int, optional
        Port to connect to existing Fluent instance. Used only when
        ``start_instance`` is ``False``. Default value can be set
        by the environment variable ``PYFLUENT_FLUENT_PORT=<port>``.

    cleanup_on_exit : bool, optional
        When True, the connected Fluent session will be shut down when
        PyFluent is exited or exit() is called on the session instance,
        by default True.

    show_gui : bool, optional
        When True, the Fluent GUI will be displayed as long as start_instance
        is also True, which can also be set by the environment
        variable PYFLUENT_SHOW_SERVER_GUI=<0 or 1>``. The show-gui argument has
        the effect of overriding the PYFLUENT_SHOW_SERVER_GUI. E.g., if
        PYFLUENT_SHOW_SERVER_GUI is set to 1, the gui is hidden if show-gui is
        set to False. The default is None so that explicit False settings can
        be detected.

    Returns
    -------
    ansys.fluent.session.Session
        Fluent session.
    """
    argvals = locals()
    if start_instance is None:
        start_instance = bool(int(os.getenv("PYFLUENT_START_INSTANCE", "1")))
    if start_instance:
        exe_path = _get_fluent_exe_path()
        launch_string = exe_path
        launch_string += _build_fluent_launch_args_string(**argvals)
        server_info_filepath = _get_server_info_filepath()
        try:
            launch_string += f" {additional_arguments}"
            launch_string += f' -sifile="{server_info_filepath}"'
            launch_string += " -nm"
            if (show_gui == False) or (
                show_gui == None and (os.getenv("PYFLUENT_SHOW_SERVER_GUI") != "1")
            ):
                launch_string += " -hidden"
            LOG.info("Launching Fluent with cmd: %s", launch_string)
            sifile_last_mtime = Path(server_info_filepath).stat().st_mtime
            if env is None:
                env = {}
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
            return Session.create_from_server_info_file(
                server_info_filepath, cleanup_on_exit
            )
        finally:
            server_info_file = Path(server_info_filepath)
            if server_info_file.exists():
                server_info_file.unlink()
    else:
        import ansys.fluent.core as pyfluent

        if pyfluent.BUILDING_GALLERY or os.getenv("PYFLUENT_LAUNCH_CONTAINER") == "1":
            args = _build_fluent_launch_args_string(**argvals).split()
            # Assumes the container OS will be able to create the
            # EXAMPLES_PATH of host OS. With the Fluent docker
            # container, the following currently works only in linux.
            port = start_fluent_container(
                pyfluent.EXAMPLES_PATH, pyfluent.EXAMPLES_PATH, args
            )
            return Session(port=port, cleanup_on_exit=cleanup_on_exit)
        else:
            ip = argvals.get("ip", None)
            port = argvals.get("port", None)
            return Session(ip=ip, port=port, cleanup_on_exit=cleanup_on_exit)
