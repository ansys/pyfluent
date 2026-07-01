# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
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

"""Wrapper over the health check gRPC service of Fluent."""

from enum import Enum

from ansys.fluent.core.services.abstract_health_check import AbstractHealthCheck


class HealthCheck(AbstractHealthCheck):
    """Class wrapping the health check gRPC service of Fluent.

    Methods
    -------
    check_health()
        Check the health of the Fluent connection.
    """

    class Status(Enum):
        """Health check status."""

        SERVING: int = 1
        NOT_SERVING: int = 2

    def __init__(self, service):
        """Initialize ApplicationRuntime."""
        self.service = service

    def check_health(self) -> Status:
        """Check the health of the Fluent connection.

        Returns
        -------
        Status
        """
        return self.Status(self.service.check_health().value)

    def wait_for_server(self, timeout: int) -> None:
        """Keeps a watch on the health of the Fluent connection.

        Response changes only when the service's serving status changes.

        Parameters
        ----------
        timeout : int
            timeout in seconds

        Raises
        ------
        TimeoutError
            If the connection to the Fluent server could not be established within the timeout.
        """
        return self.service.wait_for_server(timeout=timeout)

    def status(self) -> Status:
        """Check health of Fluent connection."""
        return self.service.status()

    @property
    def is_serving(self) -> bool:
        """Checks whether Fluent is serving."""
        return self.service.is_serving
