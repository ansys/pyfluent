import os
from pathlib import Path
import random
import string
import subprocess
import sys
import time

import ansys.fluent.core as pyfluent
from ansys.fluent.core.utils.execution import timeout_exec, timeout_loop

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

    if not python_executable:
        logger.warning(
            "Python executable not found, please verify Python environment. "
            "Cancelling PyFluent Watchdog monitoring."
        )
        return

    logger.debug(f"sys.executable: {python_executable}")

    python_executable = Path(python_executable)

    if os.name == "nt":
        pythonw_executable = python_executable.parent / "pythonw.exe"
        if pythonw_executable.exists():
            python_executable = pythonw_executable
        else:
            logger.debug("Could not find Windows 'pythonw.exe' executable.")

    # Command to be executed by the new process
    command_list = [
        python_executable,
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
                err_content = f.read()
            watchdog_err.unlink()
            logger.error("Watchdog - %s" % err_content.replace("\n", ""))
        logger.warning(
            "PyFluent Watchdog did not initialize correctly, proceeding without it..."
        )


if __name__ == "__main__":
    try:
        import signal

        import psutil

        from ansys.fluent.core.fluent_connection import FluentConnection, get_container

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

        logger.info("Attempting to connect to existing Fluent session...")

        kwargs = {
            "ip": ip,
            "port": int(port),
            "password": password,
            "launcher_args": None,
            "start_transcript": False,
            "cleanup_on_exit": True,
        }

        fluent = timeout_exec(FluentConnection, timeout=IDLE_PERIOD * 5, kwargs=kwargs)
        if not fluent:
            logger.error("Fluent connection timeout.")
            sys.exit()

        if fluent._remote_instance:
            logger.error("PyFluentWatchdog does not work with remote Fluent instances.")
            sys.exit()

        logger.info("Fluent connection successful")

        open(WATCHDOG_INIT_FILE.format(watchdog_id), "w").close()

        fluent_host_pid = fluent.connection_properties.fluent_host_pid
        cortex_pid = fluent.connection_properties.cortex_pid
        cortex_host = fluent.connection_properties.cortex_host

        logger.debug(f"fluent_host_pid: {fluent_host_pid}")
        logger.debug(f"cortex_pid: {cortex_pid}")
        logger.debug(f"cortex_host: {cortex_host}")

        down = []
        while True:
            if not psutil.pid_exists(launcher_pid):
                logger.debug("Python launcher down")
                down.append("Python")
            if not fluent.connection_properties.inside_container:
                if not psutil.pid_exists(cortex_pid):
                    logger.debug("Cortex down")
                    down.append("Cortex")
                if not psutil.pid_exists(fluent_host_pid):
                    logger.debug("Fluent down")
                    down.append("Fluent")
            else:
                if not get_container(cortex_host):
                    logger.debug("Fluent container down")
                    down.append("Fluent container")
            if down:
                break
            logger.info("Waiting...")
            time.sleep(IDLE_PERIOD)

        logger.info(", ".join(down) + " not running anymore")

        def check_fluent_processes():
            logger.info("Checking if Fluent processes are still alive...")
            if fluent.connection_properties.inside_container:
                _response = timeout_loop(
                    get_container,
                    IDLE_PERIOD * 5,
                    args=(cortex_host,),
                    expected="falsy",
                )
            else:
                _response = timeout_loop(
                    lambda: psutil.pid_exists(fluent_host_pid)
                    or psutil.pid_exists(cortex_pid),
                    IDLE_PERIOD * 5,
                    expected="falsy",
                )
            return _response

        alive = check_fluent_processes()

        if alive:
            logger.info(
                "Fluent processes remain. Checking if Fluent gRPC service is healthy..."
            )
            is_serving = timeout_exec(
                fluent.health_check_service.is_serving, timeout=IDLE_PERIOD * 3
            )

            if is_serving:
                logger.info("Fluent client healthy, trying soft exit with timeout...")
                fluent.exit(timeout=IDLE_PERIOD * 2, timeout_force=False)
                response = check_fluent_processes()
                if response:
                    logger.info("Fluent client or container remains...")
                else:
                    logger.info("Exit call succeeded.")
            else:
                logger.info("Fluent client not healthy.")

        if fluent.connection_properties.inside_container:
            logger.info(
                "Running Fluent cleanup scripts inside container if they are still available..."
            )
            fluent.force_exit_container()
            response = timeout_loop(
                get_container,
                IDLE_PERIOD * 3,
                args=(cortex_host,),
                expected="falsy",
            )
            if response:
                logger.info(
                    "Fluent container still alive somehow, directly terminating it..."
                )
                subprocess.run(["docker", "kill", cortex_host])
            else:
                logger.info("Fluent container successfully shut down.")
        else:
            logger.info(
                "Running local Fluent cleanup scripts if they are still available..."
            )
            fluent.force_exit()

        logger.info("Done.")

    except Exception as exc:
        with open("pyfluent_watchdog.err", "w") as file:
            file.write(f"{type(exc).__name__}: {exc}")
        raise
