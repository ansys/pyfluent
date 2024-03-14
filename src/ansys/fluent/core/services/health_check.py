"""Wrapper over the health check gRPC service of Fluent."""

from enum import Enum
import logging
import sys

import grpc
from grpc_health.v1 import health_pb2 as HealthCheckModule
from grpc_health.v1 import health_pb2_grpc as HealthCheckGrpcModule

from ansys.fluent.core.services.interceptors import (
    BatchInterceptor,
    ErrorStateInterceptor,
    GrpcErrorInterceptor,
    TracingInterceptor,
)

logger: logging.Logger = logging.getLogger("pyfluent.general")


class HealthCheckService:
    """Class wrapping the health check gRPC service of Fluent.

    Methods
    -------
    check_health()
        Check the health of the Fluent connection.
    """

    class Status(Enum):
        """Health check status."""

        UNKNOWN: int = 0
        SERVING: int = 1
        NOT_SERVING: int = 2
        SERVICE_UNKNOWN: int = 3

    def __init__(
        self, channel: grpc.Channel, metadata: list[tuple[str, str]], fluent_error_state
    ) -> None:
        """__init__ method of HealthCheckService class."""
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

    def check_health(self) -> str:
        """Check the health of the Fluent connection.

        Returns
        -------
        str
            "SERVING" or "NOT_SERVING"
        """
        request = HealthCheckModule.HealthCheckRequest()
        response = self._stub.Check(request, metadata=self._metadata)
        return HealthCheckService.Status(response.status).name

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
                if response.status == 1:
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

    def status(self) -> str:
        """Check health of Fluent connection."""
        if self._channel:
            try:
                return self.check_health()
            except Exception:
                ex_type, ex_value, _ = sys.exc_info()
                logger.info(
                    f"HealthCheckService.status() caught {ex_type.__name__}: {ex_value}"
                )
                return self.Status.NOT_SERVING.name
        else:
            return self.Status.NOT_SERVING.name

    @property
    def is_serving(self) -> bool:
        """Checks whether Fluent is serving."""
        return True if self.status() == "SERVING" else False
