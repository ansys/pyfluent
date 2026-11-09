# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
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

"""Handle to a locally started Fluent server that is not yet connected."""

from __future__ import annotations

import subprocess
from typing import Any

from ansys.framework.process import Endpoint, LocalProcess


class FluentProcess(LocalProcess):
    """A local Fluent server started by :func:`start_fluent_process`.

    Pass it to :func:`connect_to_fluent` (``fluent_process=...``) to connect a
    session. It satisfies :class:`ansys.framework.process.ProcessHandle`.

    The process-level methods act on the launch command. Fluent itself detaches
    from that command, so once a session is connected, stop Fluent through the
    session's ``exit()`` or ``force_exit()``. :meth:`cleanup` deletes the
    server-info file.

    Attributes
    ----------
    process : subprocess.Popen
        The launch command.
    server_info_file_name : str
        File in which Fluent publishes its address and password.
    launcher_args : dict
        Resolved launch arguments.
    session_cls : type
        Session class for the launch mode.
    file_transfer_service : Any
        Service for uploading and downloading files to and from the server.
    """

    inside_container = False

    def __init__(
        self,
        process: subprocess.Popen,
        server_info_file_name: str,
        launcher_args: dict[str, Any],
        session_cls: type,
        file_transfer_service: Any = None,
    ) -> None:
        """Initialize the handle."""
        super().__init__(process, cleanup_paths=[server_info_file_name])
        self.server_info_file_name = server_info_file_name
        self.launcher_args = launcher_args
        self.session_cls = session_cls
        self.file_transfer_service = file_transfer_service

    def __repr__(self) -> str:
        """Represent the handle by its launch PID and server-info file."""
        return (
            f"FluentProcess(pid={self.pid}, "
            f"server_info_file_name={self.server_info_file_name!r})"
        )

    @property
    def endpoint(self) -> Endpoint:
        """Address and password read from the server-info file."""
        from ansys.fluent.core.execution.session.session import (
            _parse_server_info_file,
        )

        values = _parse_server_info_file(self.server_info_file_name)
        if len(values) == 2:
            address, password = values
            return Endpoint(address=address, password=password)
        host, port, password = values
        return Endpoint(host=host, port=port, password=password)

    def _on_connected(self, session) -> None:
        """Finish a launch once a session is connected."""
        from ansys.fluent.core.execution.launcher.standalone_launcher import (
            StandaloneLauncher,
        )

        session._process = self.process
        StandaloneLauncher._disable_idle_timeout_guard(session)
        if self.launcher_args.get("lightweight_mode") and self.launcher_args.get(
            "case_file_name"
        ):
            session.read_case_lightweight(self.launcher_args.get("case_file_name"))
