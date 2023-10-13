import os
from pathlib import Path
import random
import string
import subprocess
import sys
import time
from typing import Optional

import ansys.fluent.core as pyfluent
from ansys.fluent.core.utils.execution import timeout_loop

IDLE_PERIOD = 2  # seconds
WATCHDOG_INIT_FILE = "watchdog_{}_init"


def launch(main_pid: int, sv_port: int, sv_password: str, sv_ip: Optional[str] = None):
    watchdog_id = "".join(
        random.choices(
            string.ascii_uppercase + string.ascii_lowercase + string.digits, k=6
        )
    )

    env_watchdog_debug = os.getenv("PYFLUENT_WATCHDOG_DEBUG", "off").upper()
    if env_watchdog_debug in ("1", "ON"):
        print(
            f"PYFLUENT_WATCHDOG_DEBUG environment variable found, "
            f"enabling debugging for watchdog ID {watchdog_id}..."
        )

    logger = pyfluent.logging.get_logger("pyfluent.launcher")

    watchdog_env = os.environ.copy()

    # No auto PyFluent logging to file on the watchdog
    if "PYFLUENT_LOGGING" in watchdog_env:
        watchdog_env.pop("PYFLUENT_LOGGING")

    # disable additional services/addons?

    # Path to the Python interpreter executable
    python_executable = sys.executable

    if not python_executable:
        logger.warning(
            "Python executable not found, please verify Python environment. "
            "Cancelling PyFluent Watchdog monitoring."
        )
        return

    logger.debug(f"Python sys.executable: {python_executable}")

    python_executable = Path(python_executable)

    if os.name == "nt":
        pythonw_executable = python_executable.parent / "pythonw.exe"
        if pythonw_executable.exists():
            python_executable = pythonw_executable
        else:
            logger.debug("Could not find Windows 'pythonw.exe' executable.")

    watchdog_exec = Path(__file__).parents[0] / "watchdog_exec.pyw"
    print(watchdog_exec)

    # Command to be executed by the new process
    command_list = [
        python_executable,
        watchdog_exec,
        str(main_pid),
        str(sv_ip),
        str(sv_port),
        sv_password,
        watchdog_id,
    ]

    if env_watchdog_debug in ("1", "ON"):
        logger.debug(f"Starting Watchdog logging to directory {os.getcwd()}")

    kwargs = {"env": watchdog_env, "stdin": subprocess.DEVNULL, "close_fds": True}

    if os.name == "nt":
        kwargs.update(shell=True)
        # https://learn.microsoft.com/en-us/windows/win32/procthread/process-creation-flags
        # https://docs.python.org/3/library/subprocess.html#windows-constants
        flags = 0
        flags |= subprocess.CREATE_NO_WINDOW
        flags |= subprocess.CREATE_NEW_PROCESS_GROUP
        flags |= subprocess.DETACHED_PROCESS
        flags |= subprocess.CREATE_BREAKAWAY_FROM_JOB
        flags |= subprocess.SW_HIDE
        kwargs.update(creationflags=flags)

    if os.name == "posix":
        kwargs.update(start_new_session=True)

    if env_watchdog_debug in ("1", "ON") and os.name != "nt":
        kwargs.update(
            stdout=open(f"pyfluent_watchdog_out_{watchdog_id}.log", mode="w"),
            stderr=open(f"pyfluent_watchdog_err_{watchdog_id}.log", mode="w"),
            bufsize=1,
        )
    else:
        kwargs.update(stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if os.name == "nt":
        # https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/start
        os_cmd = ["start"]
    else:
        os_cmd = []

    cmd_send = os_cmd + command_list
    logger.info(f"Watchdog command list: {cmd_send}")

    init_file = Path(WATCHDOG_INIT_FILE.format(watchdog_id))
    watchdog_err = Path("pyfluent_watchdog.err")

    if init_file.is_file():
        init_file.unlink()

    if watchdog_err.is_file():
        watchdog_err.unlink()

    subprocess.Popen(cmd_send, **kwargs)

    logger.info(f"Waiting for Watchdog to initialize, then proceeding...")
    file_exists = timeout_loop(
        lambda: init_file.is_file() or watchdog_err.is_file(), 10.0
    )

    if file_exists and init_file.is_file():
        time.sleep(0.1)
        init_file.unlink()
        logger.info("Watchdog initialized.")
    else:
        if watchdog_err.is_file():
            with open(watchdog_err) as f:
                err_content = f.read().replace("\n", "")
            watchdog_err.unlink()
            logger.error("Watchdog - %s" % err_content)
            if os.getenv("PYFLUENT_WATCHDOG_EXCEPTION_ON_ERROR"):
                raise RuntimeError(err_content)
        logger.warning(
            "PyFluent Watchdog did not initialize correctly, proceeding without it..."
        )
