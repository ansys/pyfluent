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
        self.__stub = HealthCheckGrpcModule.HealthStub(channel)
        self.__metadata = metadata

    @catch_grpc_error
    def check_health(self) -> str:
        """Check the health of the Fluent connection.

        Returns
        -------
        str
            "SERVING" or "NOT_SERVING"
        """
        request = HealthCheckModule.HealthCheckRequest()
        response = self.__stub.Check(request, metadata=self.__metadata)
        return HealthCheckService.Status(response.status).name
