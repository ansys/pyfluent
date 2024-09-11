"""Provides a module for server information."""

import os
from pathlib import Path
import tempfile

from ansys.fluent.core.fluent_connection import PortNotProvided
from ansys.fluent.core.launcher import launcher_utils
from ansys.fluent.core.launcher.error_handler import IpPortNotProvided
from ansys.fluent.core.session import _parse_server_info_file


def _get_server_info_file_name(use_tmpdir=True):
    server_info_dir = os.getenv("SERVER_INFO_DIR")
    dir_ = (
        Path(server_info_dir)
        if server_info_dir
        else tempfile.gettempdir() if use_tmpdir else Path.cwd()
    )
    fd, file_name = tempfile.mkstemp(suffix=".txt", prefix="serverinfo-", dir=str(dir_))
    os.close(fd)
    return file_name


def _get_server_info(
    server_info_file_name: str,
    ip: str | None = None,
    port: int | None = None,
    password: str | None = None,
):
    """Get server connection information of an already running session."""
    if not (ip and port) and not server_info_file_name:
        raise IpPortNotProvided()
    if (ip or port) and server_info_file_name:
        launcher_utils.logger.warning(
            "The IP address and port are extracted from the server-info file "
            "and their explicitly specified values are ignored."
        )
    else:
        if server_info_file_name:
            ip, port, password = _parse_server_info_file(server_info_file_name)
        ip = ip or os.getenv("PYFLUENT_FLUENT_IP", "127.0.0.1")
        port = port or os.getenv("PYFLUENT_FLUENT_PORT")

    if not port:
        raise PortNotProvided()

    return ip, port, password
