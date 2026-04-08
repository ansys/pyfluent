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

"""Convenience launcher for a REST-backed solver session.

Provides :func:`launch_fluent_rest`, the REST counterpart of
:func:`ansys.fluent.core.launcher.launcher.launch_fluent`.

Usage
-----
::

    from ansys.fluent.core.rest.rest_launcher import launch_fluent_rest

    session = launch_fluent_rest("localhost", 8000, auth_token="secret")
    session.settings.setup.models.energy.enabled.set_state(False)
"""

from ansys.fluent.core.rest.rest_session import RestSolverSession

__all__ = ["launch_fluent_rest"]


def launch_fluent_rest(
    host: str = "localhost",
    port: int = 8000,
    *,
    auth_token: str | None = None,
    version: str = "",
    scheme: str = "http",
    timeout: float = 30.0,
) -> RestSolverSession:
    """Create a :class:`RestSolverSession` connected to a Fluent REST server.

    This is a thin convenience wrapper — it constructs the *base_url* from
    *host*, *port*, and *scheme* and delegates to :class:`RestSolverSession`.

    Parameters
    ----------
    host : str, optional
        Hostname or IP address.  Defaults to ``"localhost"``.
    port : int, optional
        TCP port.  Defaults to ``8000``.
    auth_token : str, optional
        Bearer token for authentication.
    version : str, optional
        Fluent version string (e.g. ``"261"``).
    scheme : str, optional
        URL scheme.  Defaults to ``"http"``.
    timeout : float, optional
        HTTP socket timeout in seconds.  Defaults to ``30.0``.

    Returns
    -------
    RestSolverSession
        A fully initialised solver session whose settings tree communicates
        over REST.

    Examples
    --------
    >>> from ansys.fluent.core.rest import FluentRestMockServer
    >>> from ansys.fluent.core.rest.rest_launcher import launch_fluent_rest
    >>> with FluentRestMockServer() as srv:
    ...     session = launch_fluent_rest("127.0.0.1", srv.port)
    ...     print(session.settings.setup.models.energy.enabled())
    True
    """
    base_url = f"{scheme}://{host}:{port}"
    return RestSolverSession(
        base_url, auth_token=auth_token, version=version, timeout=timeout
    )
