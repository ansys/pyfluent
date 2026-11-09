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

"""gRPC transport for a Fluent connection.

:class:`GrpcTransport` owns everything backend-specific about talking to Fluent
over gRPC: the channel, the request metadata/authentication, the shared error
state, and the version-detected service factory (and hence the services). It
implements the backend-neutral
:class:`~ansys.solver.core.transport.Transport` protocol so that higher layers
can depend on the protocol rather than on gRPC directly.
"""

from __future__ import annotations

from typing import Any

from ansys.fluent.core.utils.networking import get_uds_path
from ansys.solver.core.connection import ErrorState


class GrpcTransport:
    """gRPC implementation of the platform ``Transport`` protocol.

    Parameters
    ----------
    ip, port, address, channel : optional
        Connection target. Pass an existing ``channel``, or an ``address``
        (``host:port`` or a UDS path), or an ``ip``/``port`` pair.
    password : str, optional
        Password sent as request metadata.
    allow_remote_host, certificates_folder, insecure_mode, inside_container :
        Channel security options, forwarded to the channel factory.
    """

    def __init__(
        self,
        *,
        ip: str | None = None,
        port: int | None = None,
        address: str | None = None,
        channel: Any | None = None,
        password: str | None = None,
        allow_remote_host: bool = False,
        certificates_folder: str | None = None,
        insecure_mode: bool = False,
        inside_container: bool | None = None,
    ) -> None:
        """Create the channel and the version-detected service factory."""
        from ansys.fluent.core._grpc_services import create_grpc_service_factory
        from ansys.fluent.core.connectivity.fluent_connection import (
            _get_channel,
            _get_ip_and_port,
        )
        from ansys.fluent.core.services import create_service_factory

        self._error_state = ErrorState()
        self.ip = ip
        self.port = port
        self._channel_str: str | None = None
        self._uds_fullpath: str | None = None

        if channel is not None:
            self._channel = channel
        else:
            if address is not None:
                self._channel_str = address
                self._uds_fullpath = get_uds_path(address)
                if self._uds_fullpath is None:
                    self.ip, self.port = address.rsplit(":", 1)
                    self.port = int(self.port)
            else:
                self.ip, self.port = _get_ip_and_port(ip, port)
                self._channel_str = f"{self.ip}:{self.port}"
            self._channel = _get_channel(
                ip=self.ip,
                port=self.port,
                uds_fullpath=self._uds_fullpath,
                allow_remote_host=allow_remote_host,
                certificates_folder=certificates_folder,
                insecure_mode=insecure_mode,
                inside_container=inside_container,
            )

        self._metadata: list[tuple[str, str]] = (
            [("password", password)] if password else []
        )

        self._service_factory = create_service_factory(
            service_factory=create_grpc_service_factory(
                channel=self._channel,
                metadata=self._metadata,
                error_state=self._error_state,
            ),
        )

        self._health_check = self._service_factory.health_check

    @property
    def metadata(self) -> list[tuple[str, str]]:
        """Per-request metadata/authentication headers."""
        return self._metadata

    @property
    def error_state(self) -> ErrorState:
        """Shared error state for this transport's services."""
        return self._error_state

    @property
    def is_serving(self) -> bool:
        """Whether the server is reachable and ready to serve requests."""
        return self._health_check.is_serving

    def connect(self) -> None:
        """No-op; the gRPC channel is established eagerly on construction."""

    def close(self) -> None:
        """Close the gRPC channel and release its resources."""
        if self._channel is not None:
            self._channel.close()
            self._channel = None

    def create_grpc_service(self, service: type, *args):
        """Instantiate a raw gRPC service bound to this channel and metadata."""
        return service(self._channel, self._metadata, *args)
