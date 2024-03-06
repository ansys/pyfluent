"""Provides a module for launching utilities."""

import logging
from pathlib import Path
import socket
import time
from typing import Union

from beartype import BeartypeConf, beartype

from ansys.fluent.core.exceptions import InvalidArgument

logger = logging.getLogger("pyfluent.launcher")


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


def check_docker_support():
    """Checks whether Python Docker SDK is supported by the current system."""
    import docker

    try:
        _ = docker.from_env()
    except docker.errors.DockerException:
        return False
    return True


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


@beartype(conf=BeartypeConf(violation_type=TypeError))
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
