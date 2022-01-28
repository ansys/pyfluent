import json
import os
import platform
import subprocess
import tempfile
import time
from pathlib import Path

from ansys.fluent.core import LOG
from ansys.fluent.session import Session

THIS_DIR = os.path.dirname(__file__)
OPTIONS_FILE = os.path.join(THIS_DIR, "fluent_launcher_options.json")
FLUENT_VERSION = "22.2"

def get_awp_path():
    if "AWP_ROOT" in os.environ:
        awp_path = os.environ["AWP_ROOT"]
    else:
        awp_path = os.environ["AWP_ROOT" + "".join(FLUENT_VERSION.split("."))]
    return Path(awp_path)

def get_fluent_exe_path():
    exe_path = get_awp_path() / "fluent"
    if platform.system() == "Windows":
        exe_path = exe_path / "ntbin" / "win64" / "fluent.exe"
    else:
        exe_path = exe_path / "bin" / "fluent"
    return str(exe_path)

def get_server_info_filepath():
    server_info_dir = os.getenv("SERVER_INFO_DIR")
    dir_ = Path(server_info_dir) if server_info_dir else tempfile.gettempdir()
    fd, filepath = tempfile.mkstemp(
        suffix=".txt", prefix="serverinfo-", dir=str(dir_)
    )
    os.close(fd)
    return filepath


def get_subprocess_kwargs_for_detached_process():
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
        kwargs.update(start_new_session=True)
    return kwargs


def launch_fluent(
    version=None,
    precision=None,
    processor_count=None,
    journal_filename=None,
    start_timeout=100,
):
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

    start_timeout : int, optional
        Maximum allowable time in seconds to connect to the Fluent
        server. Default is 100 seconds.

    Returns
    -------
    ansys.fluent.session.Session
        Fluent session.
    """
    exe_path = get_fluent_exe_path()
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
            fluent_values = v.get("fluent_values")
            if fluent_values:
                i = allowed_values.index(argval)
                argval = fluent_values[i]
            launch_string += v["fluent_format"].replace("{}", str(argval))
    server_info_filepath = get_server_info_filepath()
    try:
        launch_string += f' -sifile="{server_info_filepath}"'
        if not os.getenv("PYFLUENT_SHOW_SERVER_GUI"):
            launch_string += " -hidden"
        LOG.info("Launching Fluent with cmd: %s", launch_string)
        sifile_last_mtime = Path(server_info_filepath).stat().st_mtime
        kwargs = get_subprocess_kwargs_for_detached_process()
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
