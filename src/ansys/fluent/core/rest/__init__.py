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

HTTP transport layer for PyFluent, connecting to Fluent's embedded web
server via REST instead of gRPC.  It contains:

* :class:`~ansys.fluent.core.rest.client.FluentRestClient` – pure-Python
  HTTP client implementing the 14-method proxy interface expected by
  :mod:`~ansys.fluent.core.solver.flobject`.  Uses stdlib ``urllib`` only.

* :class:`~ansys.fluent.core.rest.rest_launcher.RestSolverSession` – a
  lightweight solver session that wires ``FluentRestClient`` into
  ``flobject.get_root`` so the full settings tree works over HTTP.

* :func:`~ansys.fluent.core.rest.rest_launcher.launch_webserver` – **primary
  entry point**.  Spawns a local Fluent process with ``-ws -ws-port={port}``,
  reads the mandatory ``FLUENT_WEBSERVER_TOKEN`` env var, and returns a
  connected session.

* :func:`~ansys.fluent.core.rest.rest_launcher.connect_to_webserver` –
  connects to an already-running web server using explicit ``ip``, ``port``,
  and ``auth_token``.
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
