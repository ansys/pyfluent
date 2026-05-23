# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
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

"""REST-based PyFluent settings client and session.

Standalone HTTP transport layer for PyFluent, connecting to Fluent's
embedded web server via REST.  Pure HTTP/JSON — no gRPC, no protobuf,
no code-generated modules, no local settings tree.

* :class:`~ansys.fluent.core.rest.client.FluentRestClient` – pure-Python
  HTTP client using stdlib ``urllib`` only.  Each method makes one HTTP
  call and returns the server's JSON directly.

* :class:`~ansys.fluent.core.rest.rest_launcher.RestSolverSession` – a
  lightweight solver session holding a ``FluentRestClient`` and exposing
  thin pass-through convenience methods (``get_var``, ``set_var``,
  ``execute_command``, etc.).

* :func:`~ansys.fluent.core.rest.rest_launcher.launch_webserver` – **primary
  entry point**. Spawns a local Fluent process with ``-ws -ws-port={port}``,
  generates and configures the web server authentication token internally
  for the subprocess, and returns a connected session.

* :func:`~ansys.fluent.core.rest.rest_launcher.connect_to_webserver` –
  connects to an already-running web server using explicit ``ip``, ``port``,
  and ``auth_token``.

Example::

    from ansys.fluent.core.rest import launch_webserver

    session = launch_webserver()
    print(session.get_var("setup/models/energy/enabled"))
    session.set_var("setup/models/energy/enabled", False)
    session.execute_command("file/read-case", file_name="elbow.cas.h5")
    session.exit()
"""

from ansys.fluent.core.rest.client import FluentRestClient
from ansys.fluent.core.rest.rest_launcher import (
    RestSolverSession,
    connect_to_webserver,
    launch_webserver,
)

__all__ = [
    "FluentRestClient",
    "RestSolverSession",
    "connect_to_webserver",
    "launch_webserver",
]
