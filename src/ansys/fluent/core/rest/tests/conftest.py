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
- ``real_client``: A :class:`FluentRestClient` connected to the real Fluent /
  SimBA server.  Auto-skips when the server is unreachable.

Real-server connection parameters can be supplied via:
- Environment variables: ``FLUENT_REST_HOST``, ``FLUENT_REST_PORT``,
  ``FLUENT_REST_TOKEN``
- Defaults hard-coded below (development convenience).
"""

import os
import urllib.request

import pytest

from ansys.fluent.core.rest.client import FluentRestClient

# ---------------------------------------------------------------------------
# Real-server connection defaults (overridable via env vars)
# ---------------------------------------------------------------------------
_REAL_SERVER_HOST = os.environ.get("FLUENT_REST_HOST", "10.18.44.175")
_REAL_SERVER_PORT = int(os.environ.get("FLUENT_REST_PORT", "5000"))
_REAL_SERVER_TOKEN = os.environ.get(
    "FLUENT_REST_TOKEN",
    "5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5",
)
_REAL_SERVER_COMPONENT = os.environ.get("FLUENT_REST_COMPONENT", "fluent_1")


def _real_server_reachable() -> bool:
    """Return True if the real server responds to a lightweight probe."""
    url = f"http://{_REAL_SERVER_HOST}:{_REAL_SERVER_PORT}/api/connection/run_mode"
    req = urllib.request.Request(url, method="GET")
    req.add_header("token", _REAL_SERVER_TOKEN)
    try:
        with urllib.request.urlopen(req, timeout=3):
            return True
    except Exception:
        return False


@pytest.fixture(scope="module")
def real_client():
    """Provide a :class:`FluentRestClient` connected to the real server.

    Automatically **skips** the entire module when the server is not reachable.
    """
    if not _real_server_reachable():
        pytest.skip(
            f"Real Fluent server at {_REAL_SERVER_HOST}:{_REAL_SERVER_PORT} "
            "is not reachable — skipping real-server tests."
        )
    base_url = f"http://{_REAL_SERVER_HOST}:{_REAL_SERVER_PORT}"
    return FluentRestClient(
        base_url,
        auth_token=_REAL_SERVER_TOKEN,
        component=_REAL_SERVER_COMPONENT,
    )


# ---------------------------------------------------------------------------
# Mock-server fixtures (used by test_rest_client.py)
# ---------------------------------------------------------------------------

from ansys.fluent.core.rest.mock_server import FluentRestMockServer  # noqa: E402


@pytest.fixture(scope="module")
def rest_server():
    """Provide a shared mock server for the test module."""
    with FluentRestMockServer() as srv:
        yield srv


@pytest.fixture()
def rest_client(rest_server):
    """Return a FluentRestClient pointed at the shared mock server."""
    return FluentRestClient(rest_server.base_url)