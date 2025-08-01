# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Provides a module for server information."""

import os
from pathlib import Path
import tempfile

from ansys.fluent.core.fluent_connection import PortNotProvided
from ansys.fluent.core.launcher import launcher_utils
from ansys.fluent.core.launcher.error_handler import InvalidIpPort, IpPortNotProvided
from ansys.fluent.core.session import _parse_server_info_file


def _get_server_info_file_names(use_tmpdir=True) -> tuple[str, str]:
    """Returns a tuple containing server and client-side file names with the server connection information.
    When server and client are in a different machine, the environment variable SERVER_INFO_DIR
    can be set to a shared directory between the two machines and the server-info file will be
    created in that directory. The value of the environment variable SERVER_INFO_DIR can be
    different for the server and client machines. The relative path of the server-side server-info
    file is passed to Fluent launcher and PyFluent connects to the server using the absolute path
    of the client-side server-info file. A typical use case of the environment variable
    SERVER_INFO_DIR is as follows:
    - Server machine environment variable: SERVER_INFO_DIR=/mnt/shared
    - Client machine environment variable: SERVER_INFO_DIR=\\\\server\\shared
    - Server-side server-info file: /mnt/shared/serverinfo-xyz.txt
    - Client-side server-info file: \\\\server\\shared\\serverinfo-xyz.txt
    - Fluent launcher command: fluent ... -sifile=serverinfo-xyz.txt ...
    - From PyFluent: connect_to_fluent(server_info_file_name="\\\\server\\shared\\serverinfo-xyz.txt")

    When the environment variable SERVER_INFO_DIR is not set, the server-side and client-side
    file paths for the server-info file are identical. The server-info file is created in the
    temporary directory if ``use_tmpdir`` is True, otherwise it is created in the current working
    directory.
    """
    from ansys.fluent.core import config

    server_info_dir = config.fluent_server_info_dir
    dir_ = (
        Path(server_info_dir)
        if server_info_dir
        else tempfile.gettempdir() if use_tmpdir else Path.cwd()
    )
    fd, file_name = tempfile.mkstemp(suffix=".txt", prefix="serverinfo-", dir=str(dir_))
    os.close(fd)
    if server_info_dir:
        return Path(file_name).name, file_name
    else:
        return file_name, file_name


def _check_ip_port(ip: str, port: int):
    """Check if a port is open on a given IP address."""

    if not (ip and port):
        raise IpPortNotProvided()

    if not port:
        raise PortNotProvided()

    import socket

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    try:
        result = sock.connect_ex((ip, port))
        if result != 0:
            raise InvalidIpPort()
    finally:
        sock.close()


def _get_server_info(
    server_info_file_name: str,
    ip: str | None = None,
    port: int | None = None,
    password: str | None = None,
):
    """Get server connection information of an already running session."""
    from ansys.fluent.core import config

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
        ip = ip or config.launch_fluent_ip or "127.0.0.1"
        port = port or config.launch_fluent_port

    _check_ip_port(ip=ip, port=port)

    return ip, port, password
