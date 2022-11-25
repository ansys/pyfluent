"""Wrapper over the health check grpc service of Fluent."""

from enum import Enum
from typing import List, Tuple

import grpc

from ansys.api.fluent.v0 import health_pb2 as HealthCheckModule
from ansys.api.fluent.v0 import health_pb2_grpc as HealthCheckGrpcModule
from ansys.fluent.core.services.error_handler import catch_grpc_error


class HealthCheckService:
    """Class wrapping the health check gRPC service of Fluent.

    Methods
    -------
    check_health
        Check the health of the Fluent connection.
    """

    class Status(Enum):
        UNKNOWN = 0
        SERVING = 1
        NOT_SERVING = 2
        SERVICE_UNKNOWN = 3

    def __init__(self, channel: grpc.Channel, metadata: List[Tuple[str, str]]):
        self._stub = HealthCheckGrpcModule.HealthStub(channel)
        self._metadata = metadata
        self._channel = channel

    @catch_grpc_error
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

    @catch_grpc_error
    def wait_for_server(self, timeout) -> None:
        """Keeps a watch on the health of the Fluent connection.

        Response changes only when the service's serving status changes.
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
            except Exception as e:
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
                return self.Status.NOT_SERVING.name
        else:
            return self.Status.NOT_SERVING.name

    @property
    def is_serving(self) -> bool:
        return True if self.status() == "SERVING" else False
