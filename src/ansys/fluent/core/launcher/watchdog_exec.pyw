"""Watchdog execution script, should not be executed directly or imported as a module.
PyFluent will handle the Watchdog process, see the ``launch_fluent`` documentation.
"""

if __name__ == "__main__":
    try:
        import os
        import subprocess
        import sys
        import time

        import ansys.fluent.core as pyfluent
        from ansys.fluent.core.utils.execution import timeout_exec, timeout_loop
        from watchdog import IDLE_PERIOD, WATCHDOG_INIT_FILE

        import signal

        import psutil

        from ansys.fluent.core.fluent_connection import FluentConnection, get_container

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

        if not fluent.wait_process_finished(wait=IDLE_PERIOD * 5):
            logger.info(
                "Fluent processes remain. Checking if Fluent gRPC service is healthy..."
            )
            is_serving = timeout_exec(
                fluent.health_check_service.is_serving, timeout=IDLE_PERIOD * 3
            )

            if is_serving:
                logger.info("Fluent client healthy, trying soft exit with timeout...")
                fluent.exit(timeout=IDLE_PERIOD * 2, timeout_force=False)
                if not fluent.wait_process_finished(wait=IDLE_PERIOD * 5):
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
