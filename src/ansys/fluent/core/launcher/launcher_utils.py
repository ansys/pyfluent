"""Provides a module for launching utilities."""

from enum import Enum
from functools import total_ordering
import logging
from pathlib import Path
import socket
import time
from typing import Union

from beartype import BeartypeConf, beartype

from ansys.fluent.core.exceptions import InvalidArgument

logger = logging.getLogger("pyfluent.launcher")


def check_docker_support():
    """Checks whether Python Docker SDK is supported by the current system."""
    import docker

    try:
        _ = docker.from_env()
    except docker.errors.DockerException:
        return False
    return True


@total_ordering
class FluentEnum(Enum):
    """Provides the base class for Fluent-related enums.

    Accepts lowercase member names as values and supports comparison operators.
    """

    @classmethod
    def _missing_(cls, value: str):
        for member in cls:
            if str(member) == value:
                return member
        raise ValueError(
            f"The specified value '{value}' is a supported value of {cls.__name__}."
            f""" The supported values are: '{", '".join(str(member) for member in cls)}'."""
        )

    def __str__(self):
        return self.name.lower()

    def __lt__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError(
                f"Cannot compare between {type(self).__name__} and {type(other).__name__}"
            )
        if self == other:
            return False
        for member in type(self):
            if self == member:
                return True
            if other == member:
                return False


class FluentUI(FluentEnum):
    """Provides supported user interface mode of Fluent."""

    NO_GUI_OR_GRAPHICS = ("g",)
    NO_GRAPHICS = ("gr",)
    NO_GUI = ("gu",)
    HIDDEN_GUI = ("hidden",)
    GUI = ("",)


class FluentWindowsGraphicsDriver(FluentEnum):
    """Provides supported graphics driver of Fluent in Windows."""

    NULL = ("null",)
    MSW = ("msw",)
    DX11 = ("dx11",)
    OPENGL2 = ("opengl2",)
    OPENGL = ("opengl",)
    AUTO = ("",)


class FluentLinuxGraphicsDriver(FluentEnum):
    """Provides supported graphics driver of Fluent in Linux."""

    NULL = ("null",)
    X11 = ("x11",)
    OPENGL2 = ("opengl2",)
    OPENGL = ("opengl",)
    AUTO = ("",)


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
