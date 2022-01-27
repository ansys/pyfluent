"""Wrapper over the health check grpc service of Fluent."""

from enum import Enum

from ansys.api.fluent.v0 import health_pb2 as HealthCheckModule
from ansys.api.fluent.v0 import health_pb2_grpc as HealthCheckGrpcModule

import grpc


class HealthCheckService:
    """
    Class wrapping the health check grpc service of Fluent.

    Methods
    -------
    check_health
        Check health of Fluent connection

    """

    class Status(Enum):
        UNKNOWN = 0
        SERVING = 1
        NOT_SERVING = 2
        SERVICE_UNKNOWN = 3

    def __init__(self, channel: grpc.Channel, password: str):
        self.__stub = HealthCheckGrpcModule.HealthStub(channel)
        self.__metadata = [("password", password)]

    def check_health(self) -> str:
        """
        Check health of Fluent connection

        Returns
        -------
        str
            "SERVING" or "NOT_SERVING"
        """
        request = HealthCheckModule.HealthCheckRequest()
        response = self.__stub.Check(request, metadata=self.__metadata)
        return HealthCheckService.Status(response.status).name
