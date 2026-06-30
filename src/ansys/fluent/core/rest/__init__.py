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

"""REST-based PyFluent client for Fluent web server.

Standalone HTTP transport layer for PyFluent, connecting to Fluent's
embedded web server via REST.  Pure HTTP/JSON — no gRPC, no protobuf,
no code-generated modules, no local settings tree.

* :class:`~ansys.fluent.core.rest.client.FluentRestClient` – pure-Python
  HTTP client using stdlib ``urllib`` only.  Each method makes one HTTP
  call and returns the server's JSON directly.

* :func:`~ansys.fluent.core.rest.rest_connect.connect_to_webserver` – connect
  to an already-running Fluent web server and return a FluentRestClient.

* :class:`~ansys.fluent.core.rest.client.FluentRestError` – exception raised
  on HTTP failures.

"""

from ansys.fluent.core.rest.client import FluentRestClient, FluentRestError
from ansys.fluent.core.rest.rest_connect import connect_to_webserver

__all__ = [
    "FluentRestClient",
    "connect_to_webserver",
    "FluentRestError",
]
