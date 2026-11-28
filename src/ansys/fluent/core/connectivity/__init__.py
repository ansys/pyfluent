# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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

"""Connect to Ansys Fluent and transfer files and cases between sessions.

This package provides the gRPC connection to a running Fluent process
(:class:`~ansys.fluent.core.connectivity.fluent_connection.FluentConnection`),
file transfer strategies for standalone, containerized, and remote (PyPIM)
Fluent deployments, and helpers for transferring case/data files between
solver sessions.
"""

from ansys.fluent.core.connectivity.data_transfer import transfer_case  # noqa: F401
from ansys.fluent.core.connectivity.file_transfer_service import (  # noqa: F401
    ContainerFileTransferStrategy,
    FileTransferStrategy,
    PimFileTransferService,
    RemoteFileTransferStrategy,
    StandaloneFileTransferStrategy,
)
from ansys.fluent.core.connectivity.fluent_connection import (  # noqa: F401
    FluentConnection,
    PortNotProvided,
)

__all__ = [
    "transfer_case",
    "ContainerFileTransferStrategy",
    "FileTransferStrategy",
    "PimFileTransferService",
    "RemoteFileTransferStrategy",
    "StandaloneFileTransferStrategy",
    "FluentConnection",
    "PortNotProvided",
]
