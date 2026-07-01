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

* :class:`~ansys.fluent.core.rest.client.FluentRestClient` – settings API
  client.  Use :meth:`~ansys.fluent.core.rest.client.FluentRestClient.connect`
  to create a production instance, or inject a fake
  :class:`~ansys.fluent.core.rest.transport.RequestStrategy` for unit tests.

* :class:`~ansys.fluent.core.rest.transport.HttpRequestStrategy` – real HTTP
  transport built on stdlib ``urllib``.

* :class:`~ansys.fluent.core.rest.transport.RequestStrategy` – protocol that
  test doubles must satisfy (structural — no inheritance required).

* :class:`~ansys.fluent.core.rest.errors.FluentRestError` – exception raised
  on HTTP failures.

Quick start::

    >>> from ansys.fluent.core.rest import FluentRestClient
    >>> client = FluentRestClient.connect("http://127.0.0.1:5000", auth_token="secret")
    >>> client.get_var("setup/models/energy/enabled")

"""

from ansys.fluent.core.rest.client import FluentRestClient
from ansys.fluent.core.rest.errors import FluentRestError
from ansys.fluent.core.rest.transport import HttpRequestStrategy, RequestStrategy

# Backwards-compatible alias — callers using connect_to_webserver() continue to work.
connect_to_webserver = FluentRestClient.connect

__all__ = [
    "FluentRestClient",
    "FluentRestError",
    "HttpRequestStrategy",
    "RequestStrategy",
    "connect_to_webserver",
]
