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

"""Standalone REST-based solver session.

This module provides :class:`HttpSolver`, a lightweight solver session that
communicates with Fluent exclusively over the REST (HTTP) transport.  It is
completely independent of the gRPC infrastructure (``BaseSession``,
``FluentConnection``, ``ServiceFactory``, etc.).

Usage::

    >>> from ansys.fluent.core.session_http_solver import HttpSolver
    >>> from ansys.fluent.core.rest.client import FluentRestClient
    >>>
    >>> client = FluentRestClient.connect(
    ...     url="http://127.0.0.1:5000", auth_token="my-token"
    ... )
    >>> solver = HttpSolver(client)
    >>> solver.settings.setup.models.energy.enabled()
"""

from ansys.fluent.core.rest.client import FluentRestClient
from ansys.fluent.core.services.rest_settings import RestSettings
from ansys.fluent.core.solver import flobject


class HttpSolver:
    """Standalone solver session backed by the Fluent REST API.

    Unlike the gRPC-based :class:`~ansys.fluent.core.session_solver.Solver`,
    this class has **no** dependency on ``BaseSession``, ``FluentConnection``,
    or any gRPC service.  Settings classes are built at runtime from
    ``get_static_info()`` — no generated settings module is required.

    Parameters
    ----------
    rest_client : FluentRestClient
        A connected REST client instance (see
        :meth:`FluentRestClient.connect`).
    """

    def __init__(self, rest_client: FluentRestClient) -> None:
        self._rest_client = rest_client
        self._rest_settings_service = RestSettings(rest_client)
        self._settings = None

    @property
    def settings(self):
        """Root settings object (built at runtime via REST ``get_static_info()``)."""
        if self._settings is None:
            self._settings = flobject.get_root(
                flproxy=self._rest_settings_service,
                version="",
            )
        return self._settings

    def is_active(self) -> bool:
        """Whether the REST connection is still usable."""
        return self._rest_client is not None

    def exit(self) -> None:
        """Release the REST connection."""
        self._rest_client = None
        self._settings = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.exit()
        return False
