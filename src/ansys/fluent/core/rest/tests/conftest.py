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

"""Shared pytest fixtures for REST transport tests.

Provides:
- ``real_client``: A :class:`FluentRestClient` connected to a real Fluent /
  SimBA server.  Auto-skips when the server is unreachable or when the
  required environment variables are not set.

Real-server connection parameters **must** be supplied via environment
variables.  No defaults are hard-coded so that credentials and internal
addresses never leak into source control.

Required environment variables
-------------------------------
``FLUENT_WEBSERVER_TOKEN``
    Bearer token (password) for the SimBA server.

``FLUENT_REST_PORT``
    TCP port the SimBA server is listening on.

Optional environment variables
-------------------------------
``FLUENT_REST_HOST``
    Hostname or IP (default: ``"127.0.0.1"``).
``FLUENT_REST_COMPONENT``
    DataModel component name (default: ``"fluent_1"``).
``FLUENT_REST_SCHEME``
    URL scheme (default: ``"http"``).

Setup instructions
------------------
Before running the real-server tests, set the variables in your shell::

    export FLUENT_WEBSERVER_TOKEN=<your-token>  # mandatory
    export FLUENT_REST_PORT=5000                # mandatory
    export FLUENT_REST_HOST=127.0.0.1           # optional
"""

import os
import urllib.request

import pytest

from ansys.fluent.core.rest.client import FluentRestClient

# ---------------------------------------------------------------------------
# Real-server connection — read from environment variables only.
# No hard-coded fallbacks: credentials must never appear in source control.
# ---------------------------------------------------------------------------
_REAL_SERVER_TOKEN = os.environ.get("FLUENT_WEBSERVER_TOKEN", "")
_REAL_SERVER_PORT_STR = os.environ.get("FLUENT_REST_PORT", "")
_REAL_SERVER_HOST = os.environ.get("FLUENT_REST_HOST", "127.0.0.1")
_REAL_SERVER_COMPONENT = os.environ.get("FLUENT_REST_COMPONENT", "fluent_1")
_REAL_SERVER_SCHEME = os.environ.get("FLUENT_REST_SCHEME", "http")


def _env_vars_present() -> bool:
    """Return ``True`` only when all mandatory env vars are set and non-empty."""
    return bool(_REAL_SERVER_TOKEN and _REAL_SERVER_PORT_STR)


def _real_server_reachable() -> bool:
    """Return ``True`` if the real server responds to a lightweight probe.

    Sends ``GET /api/connection/run_mode`` with the configured auth token.
    Returns ``False`` immediately if mandatory env vars are absent.
    """
    if not _env_vars_present():
        return False
    port = int(_REAL_SERVER_PORT_STR)
    url = (
        f"{_REAL_SERVER_SCHEME}://{_REAL_SERVER_HOST}:{port}"
        "/api/connection/run_mode"
    )
    req = urllib.request.Request(url, method="GET")
    req.add_header("Authorization", f"Bearer {_REAL_SERVER_TOKEN}")
    try:
        with urllib.request.urlopen(req, timeout=3):  # nosec B310
            return True
    except Exception:
        return False


@pytest.fixture(scope="module")
def real_client():
    """Provide a :class:`FluentRestClient` connected to the real SimBA server.

    Automatically **skips** the entire module when:

    * ``FLUENT_WEBSERVER_TOKEN`` or ``FLUENT_REST_PORT`` env vars are unset, or
    * the server is not reachable at the configured address.

    Set the following environment variables before running real-server tests::

        export FLUENT_WEBSERVER_TOKEN=<your-token>
        export FLUENT_REST_PORT=<port>
    """
    if not _env_vars_present():
        pytest.skip(
            "Mandatory environment variables are not set — "
            "set FLUENT_WEBSERVER_TOKEN and FLUENT_REST_PORT "
            "to run real-server tests."
        )
    if not _real_server_reachable():
        pytest.skip(
            f"Real Fluent server at {_REAL_SERVER_HOST}:{_REAL_SERVER_PORT_STR} "
            "is not reachable — skipping real-server tests."
        )
    port = int(_REAL_SERVER_PORT_STR)
    base_url = f"{_REAL_SERVER_SCHEME}://{_REAL_SERVER_HOST}:{port}"
    return FluentRestClient(
        base_url,
        auth_token=_REAL_SERVER_TOKEN,
        component=_REAL_SERVER_COMPONENT,
    )

