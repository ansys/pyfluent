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

"""REST-based PyFluent settings client (Step 1 exploration).

This package provides a transport-agnostic alternative to the gRPC
``SettingsService``.  It contains:

* :class:`~ansys.fluent.core.rest.client.FluentRestClient` – a pure-Python
  HTTP client whose public interface is identical to the duck-typed proxy
  expected by :mod:`~ansys.fluent.core.solver.flobject`.  Written against a
  provisional REST API contract; the contract is documented in ``client.py``
  and can be adjusted to match the real Fluent REST API when it becomes
  available.

* :class:`~ansys.fluent.core.rest.mock_server.FluentRestMockServer` – a
  lightweight in-process HTTP server (stdlib only, no Flask) that implements
  the same provisional REST contract backed by an in-memory settings store.
  Useful for local development, unit-tests, and demos without a running Fluent
  instance.
"""

from ansys.fluent.core.rest.client import FluentRestClient
from ansys.fluent.core.rest.mock_server import FluentRestMockServer

__all__ = ["FluentRestClient", "FluentRestMockServer"]
