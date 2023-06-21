import multiprocessing.pool
import os
from pathlib import Path
import random
import string
import subprocess
import sys
import time

import ansys.fluent.core as pyfluent

IDLE_PERIOD = 2  # seconds
WATCHDOG_INIT_FILE = "watchdog_{}_init"


def launch(main_pid: int, sv_port: int, sv_password: str, sv_ip: str = None):
    watchdog_id = "".join(
        random.choices(
            string.ascii_uppercase + string.ascii_lowercase + string.digits, k=6
        )
    )

    env_watchdog_debug = os.getenv("PYFLUENT_WATCHDOG_DEBUG", "off").upper()
    if env_watchdog_debug in ("1", "ON"):
        print(f"Number of arguments: {len(sys.argv)} arguments.")
        print(f"Argument list: {sys.argv}")

        print(
            f"PYFLUENT_WATCHDOG_DEBUG environment variable found, "
            f"enabling debugging for watchdog id {watchdog_id}..."
        )

    logger = pyfluent.logging.get_logger("pyfluent.launcher")

    watchdog_env = os.environ.copy()

    # No auto PyFluent logging to file on the watchdog
    if "PYFLUENT_LOGGING" in watchdog_env:
        watchdog_env.pop("PYFLUENT_LOGGING")

    # disable additional services/addons?

    # Path to the Python interpreter executable
    python_executable = sys.executable
    if os.name == "nt":
        pythonw_executable = Path(sys.executable).parent / "pythonw.exe"
        if pythonw_executable.exists():
            python_executable = pythonw_executable

    # Command to be executed by the new process
    command_list = [
        Path(python_executable),
        Path(__file__),
        str(main_pid),
        str(sv_ip),
        str(sv_port),
        sv_password,
        watchdog_id,
    ]

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

    logger.debug(f"kwargs: {kwargs}")

    if os.name == "nt":
        # https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/start
        os_cmd = ["start"]
    else:
        os_cmd = []

    cmd_send = os_cmd + command_list
    logger.debug(f"Command list: {cmd_send}")

    init_file = Path(WATCHDOG_INIT_FILE.format(watchdog_id))
    if init_file.is_file():
        init_file.unlink()

    subprocess.Popen(cmd_send, **kwargs)

    logger.debug(f"Waiting for Watchdog to initialize, then proceeding...")
    i = 0.0
    success = False
    while i <= 10:
        if init_file.is_file():
            success = True
            init_file.unlink()
            break
        i += 0.5
        time.sleep(0.5)
    if not success:
        logger.warning(
            "PyFluent Watchdog did not initialize correctly, proceeding without it..."
        )


if __name__ == "__main__":
    from multiprocessing.context import TimeoutError
    import signal

    import psutil

    from ansys.fluent.core.fluent_connection import FluentConnection, get_container_ids

    print(
        "Starting PyFluent Watchdog process, do not manually close or terminate this process, "
        "it will automatically exit once finished.".upper()
    )

    watchdog_id = sys.argv[5]

    launcher_pid = int(sys.argv[1])

    # Configure logger for Watchdog process
    log_config = pyfluent.logging.get_default_config()
    log_config["handlers"]["pyfluent_file"][
        "filename"
    ] = f"pyfluent_watchdog_{watchdog_id}.log"

    logger = pyfluent.logging.get_logger("pyfluent.watchdog")

    if os.getenv("PYFLUENT_WATCHDOG_DEBUG", "OFF").upper() in ("1", "ON"):
        pyfluent.logging.enable(custom_config=log_config)
        logger.setLevel("DEBUG")
        logger.handlers = pyfluent.logging.get_logger(
            "pyfluent.general"
        ).handlers  # using same handlers as already defined

    def got_sig(signum, _):
        logger.warning(f"Received {signal.Signals(signum).name}, ignoring it")

    signals = signal.valid_signals()
    if os.name == "posix":
        try:
            signals.remove(signal.SIGCHLD)
        except AttributeError:
            pass

    for sig in signals:
        try:
            logger.debug(f"Handling signal {sig}")
            signal.signal(sig, got_sig)
        except OSError:
            logger.debug(f"Unable to handle signal {sig}")

    logger.debug(f"Number of arguments: {len(sys.argv)} arguments.")
    logger.debug(f"Argument list: {sys.argv}")
    logger.debug(f"Watchdog pid: {os.getpid()}")
    logger.debug(f"Python launcher pid: {launcher_pid}")

    ip, port, password = sys.argv[2:5]

    logger.debug(f"ip:{ip} port:{port} pass:{password}")

    if ip == "None":
        ip = None

    logger.debug("Attempting to connect to existing Fluent session...")

    kwargs = {
        "ip": ip,
        "port": int(port),
        "password": password,
        "launcher_args": None,
        "start_transcript": False,
        "cleanup_on_exit": False,
    }

    def _start_connection(**connection_kwargs):
        return FluentConnection(**connection_kwargs)

    pool = multiprocessing.pool.ThreadPool(processes=1)
    async_result = pool.apply_async(_start_connection, kwds=kwargs)
    try:
        fluent = async_result.get(timeout=IDLE_PERIOD * 5)
        pool.close()
    except TimeoutError:
        logger.debug("Fluent connection timeout")
        pool.terminate()
        sys.exit("Unable to connect to Fluent client")

    logger.debug("Fluent connection successful")

    open(WATCHDOG_INIT_FILE.format(watchdog_id), "w").close()

    fluent_host_pid = fluent.connection_properties.fluent_host_pid
    cortex_pid = fluent.connection_properties.cortex_pid
    cortex_host = fluent.connection_properties.cortex_host

    logger.debug(f"fluent_host_pid: {fluent_host_pid}")
    logger.debug(f"cortex_pid: {cortex_pid}")
    logger.debug(f"cortex_host: {cortex_host}")

    while True:
        if not psutil.pid_exists(launcher_pid):
            logger.debug("Python launcher down")
            break
        if not fluent._remote_instance:
            if fluent.connection_properties.inside_container is False:
                if not psutil.pid_exists(cortex_pid):
                    logger.debug("Cortex down")
                    break
                if not psutil.pid_exists(fluent_host_pid):
                    logger.debug("Fluent down")
                    break
            elif fluent.connection_properties.inside_container is True:
                if not cortex_host in get_container_ids():
                    logger.debug("Fluent container down")
                    break
                # additional wait due to expensive get_container_ids() call
                time.sleep(IDLE_PERIOD * 2)
            else:
                logger.debug(
                    "Undefined whether Fluent is inside a container or not, "
                    "monitoring only the Python process..."
                )
        logger.debug("Waiting...")
        time.sleep(IDLE_PERIOD)

    down = []
    if not psutil.pid_exists(launcher_pid):
        down.append("Python")
    if fluent.connection_properties.inside_container:
        if cortex_host not in get_container_ids():
            down.append("Fluent container")

    if (
        fluent.connection_properties.inside_container is False
        and not fluent._remote_instance
    ):
        if not psutil.pid_exists(fluent_host_pid):
            down.append("Fluent")
        if not psutil.pid_exists(cortex_pid):
            down.append("Cortex")

    logger.debug(", ".join(down) + " not running anymore")
    # wait a bit as processes may be currently closing down
    time.sleep(IDLE_PERIOD * 2)

    def _check_serving(fl):
        return fl.health_check_service.is_serving

    pool = multiprocessing.pool.ThreadPool(processes=1)
    async_result = pool.apply_async(_check_serving, args=(fluent,))
    try:
        is_serving = async_result.get(timeout=IDLE_PERIOD * 3)
        pool.close()
    except TimeoutError:
        is_serving = False
        pool.terminate()

    force = False
    if is_serving:
        logger.debug("Fluent client healthy, trying soft exit with timeout...")
        fluent.exit(timeout=IDLE_PERIOD * 3, timeout_force=False)
        logger.debug("Waiting...")
        time.sleep(IDLE_PERIOD * 2)
        if (
            fluent.connection_properties.inside_container
            and cortex_host in get_container_ids()
        ):
            logger.debug("Exit call passed, but Fluent container remains...")
            force = True
        elif psutil.pid_exists(fluent_host_pid) or psutil.pid_exists(cortex_pid):
            logger.debug("Exit call passed, but Fluent client remains...")
            force = True
        else:
            logger.debug("Exit call succeeded.")
        logger.debug("Continuing...")
    else:
        logger.debug("Fluent client not healthy")
        force = True

    if force:
        logger.debug("Forcing cleanup...")
        if fluent._remote_instance:
            logger.error("Cannot terminate remote Fluent client.")
        elif fluent.connection_properties.inside_container:
            logger.debug("Terminating Fluent container...")
            fluent.force_exit_container()
        else:
            logger.debug("Terminating local Fluent client...")
            fluent.force_exit()

    logger.debug("Done.")
