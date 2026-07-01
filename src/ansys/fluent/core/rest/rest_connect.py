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

"""Simple REST connection for the Fluent web server.

This module provides a lightweight connection function to an already-running
Fluent REST server. Users pass the full URL and bearer token directly.

Public API
----------
* :func:`connect_to_webserver` — connect to a Fluent REST server, returning
  a :class:`FluentRestClient`.

Examples
--------
Connect to a Fluent web server and interact via the REST client::

    >>> from ansys.fluent.core.rest import connect_to_webserver
    >>> client = connect_to_webserver(
    ...     url="http://127.0.0.1:5000",
    ...     auth_token="my-secret-token",
    ... )
    >>> result = client.get_var("setup/models/energy/enabled")
"""

from __future__ import annotations

import logging

from ansys.fluent.core.rest.client import FluentRestClient

__all__ = ["connect_to_webserver"]

logger = logging.getLogger(__name__)


def connect_to_webserver(url: str, auth_token: str) -> FluentRestClient:
    """Connect to an already-running Fluent REST server.

    Parameters
    ----------
    url : str
        Full URL of the Fluent REST server, e.g., ``"http://127.0.0.1:5000"``.
    auth_token : str
        Bearer token (password) for authentication. It will be SHA-256 hashed
        before being sent in the Authorization header.

    Returns
    -------
    FluentRestClient
        A client instance ready for REST operations.

    """
    logger.info("Connecting to Fluent REST server at %s", url)
    return FluentRestClient(url, auth_token=auth_token)
