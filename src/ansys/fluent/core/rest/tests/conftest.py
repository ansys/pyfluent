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

"""Shared pytest fixtures for the REST transport tests.

Real-server tests are marked with ``@pytest.mark.real_server``.
Run only real-server tests::

    pytest src/ansys/fluent/core/rest/tests/ -m real_server -v

Run only mock tests (default)::

    pytest src/ansys/fluent/core/rest/tests/ -m "not real_server" -v
"""

import urllib.request

import pytest

from ansys.fluent.core.rest import FluentRestClient, FluentRestMockServer

# ---------------------------------------------------------------------------
# Real server connection details
# ---------------------------------------------------------------------------

_REAL_SERVER_HOST = "10.18.44.175"
_REAL_SERVER_PORT = 5000
_REAL_SERVER_TOKEN = "5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5"
_REAL_SERVER_URL = f"http://{_REAL_SERVER_HOST}:{_REAL_SERVER_PORT}"


def _real_server_reachable() -> bool:
    """Return True if the real Fluent server responds on the connection endpoint."""
    try:
        urllib.request.urlopen(
            f"{_REAL_SERVER_URL}/api/connection/run_mode", timeout=3
        )
        return True
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Mock server fixtures (always available)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def rest_server():
    """Start a single mock-server instance shared across all tests in a module."""
    with FluentRestMockServer() as srv:
        yield srv


@pytest.fixture(scope="module")
def rest_client(rest_server):
    """Return a FluentRestClient pointed at the module-scoped mock server."""
    return FluentRestClient(rest_server.base_url)


# ---------------------------------------------------------------------------
# Real server fixture (skips if server not reachable)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def real_client():
    """Return a FluentRestClient connected to the real Fluent / SimBA server.

    Automatically skips the entire test module if the server is not reachable.
    This means real-server tests never fail your CI just because Fluent isn't
    running — they are simply skipped.
    """
    if not _real_server_reachable():
        pytest.skip(
            f"Real Fluent server not reachable at {_REAL_SERVER_URL}. "
            "Start Fluent with REST enabled to run these tests."
        )
    return FluentRestClient(
        _REAL_SERVER_URL,
        auth_token=_REAL_SERVER_TOKEN,
        component="fluent_1",
    )
