"""Wrapper over the monitor grpc service of Fluent."""

from google.protobuf.json_format import MessageToDict
import grpc

from ansys.api.fluent.v0 import monitor_pb2 as MonitorModule
from ansys.api.fluent.v0 import monitor_pb2_grpc as MonitorGrpcModule
from ansys.fluent.core.services.streaming import StreamingService


class MonitorsService(StreamingService):
    """Class wrapping the monitor gRPC service of Fluent."""

    def __init__(self, channel: grpc.Channel, metadata):
        self._stub = MonitorGrpcModule.MonitorStub(channel)
        self._metadata = metadata
        super().__init__(
            stub=self._stub,
            request=MonitorModule.StreamingRequest(),
            metadata=self._metadata,
        )

    def get_monitors_info(self) -> dict:
        """Get monitors information.

        Parameters
        ----------
        None

        Returns
        -------
        dict
            Dictionary containing the monitors information.
        """
        monitors_info = {}
        request = MonitorModule.GetMonitorsRequest()
        response = self._stub.GetMonitors(request, metadata=self._metadata)
        for monitor_set in response.monitorset:
            monitor_info = MessageToDict(monitor_set)
            monitors_info[monitor_set.name] = monitor_info
        return monitors_info
