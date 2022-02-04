import json
import os
import platform
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any, Dict

from ansys.fluent.core import LOG
from ansys.fluent.session import Session

THIS_DIR = os.path.dirname(__file__)
OPTIONS_FILE = os.path.join(THIS_DIR, "fluent_launcher_options.json")
FLUENT_VERSION = "22.2"


def _get_awp_path():
    if "AWP_ROOT" in os.environ:
        awp_path = os.environ["AWP_ROOT"]
    else:
        awp_path = os.environ["AWP_ROOT" + "".join(FLUENT_VERSION.split("."))]
    return Path(awp_path)


def _get_fluent_exe_path():
    exe_path = _get_awp_path() / "fluent"
    if platform.system() == "Windows":
        exe_path = exe_path / "ntbin" / "win64" / "fluent.exe"
    else:
        exe_path = exe_path / "bin" / "fluent"
    return str(exe_path)


def _get_server_info_filepath():
    server_info_dir = os.getenv("SERVER_INFO_DIR")
    dir_ = Path(server_info_dir) if server_info_dir else tempfile.gettempdir()
    fd, filepath = tempfile.mkstemp(
        suffix=".txt", prefix="serverinfo-", dir=str(dir_)
    )
    os.close(fd)
    return filepath


def _get_subprocess_kwargs_for_fluent(env: Dict[str, Any]) -> Dict[str, Any]:
    kwargs = {}
    kwargs.update(
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
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
) -> Session:
    """Start Fluent locally in server mode.

    Parameters
    ----------
    version : str, optional
        Whether to use the ``"2d"`` or ``"3d"`` version of Fluent.
        Default is ``"3d"``.

    precision : str, optional
        Whether to use the ``"single"`` precision or ``"double"``
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

    Returns
    -------
    ansys.fluent.session.Session
        Fluent session.
    """
    exe_path = _get_fluent_exe_path()
    launch_string = exe_path
    argvals = locals()
    all_options = None
    with open(OPTIONS_FILE, encoding="utf-8") as fp:
        all_options = json.load(fp)
    for k, v in all_options.items():
        argval = argvals.get(k)
        default = v.get("default")
        if argval is None and v.get("required") is True:
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
                        "%s = %s is discarded as it is outside "
                        "allowed values %s.",
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
            launch_string += v["fluent_format"].replace("{}", str(argval))
    server_info_filepath = _get_server_info_filepath()
    try:
        launch_string += f" {additional_arguments}"
        launch_string += f' -sifile="{server_info_filepath}"'
        if not os.getenv("PYFLUENT_SHOW_SERVER_GUI"):
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
        return Session(server_info_filepath)
    finally:
        server_info_file = Path(server_info_filepath)
        if server_info_file.exists():
            server_info_file.unlink()
