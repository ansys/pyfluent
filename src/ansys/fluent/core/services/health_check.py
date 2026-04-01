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
import importlib
import logging
import sys

import grpc

from ansys.fluent.core.module_config import config
from ansys.fluent.core.services.grpc_compat import (
    GrpcApiVersion,
    get_grpc_api_version,
    import_fluent_api_module,
    resolve_attr_first,
)
from ansys.fluent.core.services.interceptors import (
    BatchInterceptor,
    ErrorStateInterceptor,
    GrpcErrorInterceptor,
    TracingInterceptor,
)

logger: logging.Logger = logging.getLogger("pyfluent.general")

HealthCheckModule = import_fluent_api_module("health_pb2", get_grpc_api_version(None))
HealthCheckGrpcModule = import_fluent_api_module(
    "health_pb2_grpc", get_grpc_api_version(None)
)


def _load_health_modules(grpc_api_version: GrpcApiVersion):
    """Load health proto/grpc modules for the selected API generation."""
    if grpc_api_version == GrpcApiVersion.V0:
        return (
            importlib.import_module("grpc_health.v1.health_pb2"),
            importlib.import_module("grpc_health.v1.health_pb2_grpc"),
        )
    return (
        import_fluent_api_module("health_pb2", grpc_api_version),
        import_fluent_api_module("health_pb2_grpc", grpc_api_version),
    )


class HealthCheckService:
    """Class wrapping the health check gRPC service of Fluent.

    Methods
    -------
    check_health()
        Check the health of the Fluent connection.
    """

    class Status(Enum):
        """Health check status."""

        UNSPECIFIED: int = 0
        SERVING: int = 1
        NOT_SERVING: int = 2
        SERVICE_UNKNOWN: int = 3

    @classmethod
    def _status_from_response(cls, response_status: int) -> "HealthCheckService.Status":
        """Convert a protobuf health status to local status enum."""
        serving_status_serving = resolve_attr_first(
            HealthCheckModule.HealthCheckResponse,
            "SERVING_STATUS_SERVING",
            "SERVING",
        )
        serving_status_not_serving = resolve_attr_first(
            HealthCheckModule.HealthCheckResponse,
            "SERVING_STATUS_NOT_SERVING",
            "NOT_SERVING",
        )
        serving_status_service_unknown = resolve_attr_first(
            HealthCheckModule.HealthCheckResponse,
            "SERVING_STATUS_SERVICE_UNKNOWN",
            "SERVICE_UNKNOWN",
        )
        if response_status == serving_status_serving:
            return cls.Status.SERVING
        if response_status == serving_status_not_serving:
            return cls.Status.NOT_SERVING
        if response_status == serving_status_service_unknown:
            return cls.Status.SERVICE_UNKNOWN
        return cls.Status.UNSPECIFIED

    def __init__(
        self,
        channel: grpc.Channel,
        metadata: list[tuple[str, str]],
        fluent_error_state,
        fluent_version: str | None = None,
    ) -> None:
        """__init__ method of HealthCheckService class."""
        global HealthCheckModule
        global HealthCheckGrpcModule

        self._grpc_api_version = get_grpc_api_version(fluent_version)
        HealthCheckModule, HealthCheckGrpcModule = _load_health_modules(
            self._grpc_api_version
        )

        intercept_channel = grpc.intercept_channel(
            channel,
            GrpcErrorInterceptor(),
            ErrorStateInterceptor(fluent_error_state),
            TracingInterceptor(),
            BatchInterceptor(),
        )
        self._stub = HealthCheckGrpcModule.HealthStub(intercept_channel)
        self._metadata = metadata
        self._channel = channel
        self._intercept_channel = intercept_channel

    def _switch_to_v0(self) -> None:
        """Switch proto/stub modules to v0 for older Fluent servers."""
        global HealthCheckModule
        global HealthCheckGrpcModule

        self._grpc_api_version = GrpcApiVersion.V0
        HealthCheckModule, HealthCheckGrpcModule = _load_health_modules(
            self._grpc_api_version
        )
        self._stub = HealthCheckGrpcModule.HealthStub(self._intercept_channel)

    def check_health(self) -> Status:
        """Check the health of the Fluent connection.

        Returns
        -------
        Status

        Raises
        ------
        RuntimeError
            If the gRPC call to check health fails.
        """
        request = HealthCheckModule.HealthCheckRequest()
        try:
            response = self._stub.Check(
                request,
                metadata=self._metadata,
                timeout=config.check_health_timeout,
            )
        except RuntimeError as ex:
            if (
                self._grpc_api_version == GrpcApiVersion.V1
                and "Method not found" in str(ex)
            ):
                self._switch_to_v0()
                request = HealthCheckModule.HealthCheckRequest()
                response = self._stub.Check(
                    request,
                    metadata=self._metadata,
                    timeout=config.check_health_timeout,
                )
            else:
                raise
        return self._status_from_response(response.status)

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
        request = HealthCheckModule.HealthCheckRequest()
        responses = self._stub.Watch(request, metadata=self._metadata, timeout=timeout)

        while True:
            try:
                response = next(responses)
                serving_status_serving = resolve_attr_first(
                    HealthCheckModule.HealthCheckResponse,
                    "SERVING_STATUS_SERVING",
                    "SERVING",
                )
                if response.status == serving_status_serving:
                    responses.cancel()
            except StopIteration:
                break
            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.CANCELLED:
                    break
                if e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                    raise TimeoutError(
                        f"The connection to the Fluent server could not be established within the configurable {timeout} second time limit."
                    )
                raise

    def status(self) -> Status:
        """Check health of Fluent connection."""
        if self._channel:
            try:
                return self.check_health()
            except Exception:
                ex_type, ex_value, _ = sys.exc_info()
                logger.info(
                    f"HealthCheckService.status() caught {ex_type.__name__}: {ex_value}"
                )
                return self.Status.NOT_SERVING
        else:
            return self.Status.NOT_SERVING

    @property
    def is_serving(self) -> bool:
        """Checks whether Fluent is serving."""
        return self.status() == self.Status.SERVING
