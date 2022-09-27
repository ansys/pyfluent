"""Wrapper over the monitor grpc service of Fluent."""

from google.protobuf.json_format import MessageToDict
import grpc

from ansys.api.fluent.v0 import monitor_pb2 as MonitorModule
from ansys.api.fluent.v0 import monitor_pb2_grpc as MonitorGrpcModule


class MonitorsService:
    """Class wrapping the monitor gRPC service of Fluent."""

    def __init__(self, channel: grpc.Channel, metadata):
        self.__stub = MonitorGrpcModule.MonitorStub(channel)
        self.__metadata = metadata
        self._streams = None

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
        response = self.__stub.GetMonitors(request, metadata=self.__metadata)
        for monitor_set in response.monitorset:
            monitor_info = MessageToDict(monitor_set)
            monitors_info[monitor_set.name] = monitor_info
        return monitors_info

    def begin_streaming(self, started_evt):
        """Begin monitor streaming from Fluent.

        Parameters
        ----------
        None

        Yields
        -------
        Monitor data
            Monitor data i.e monitor x and y values.
        """

        request = MonitorModule.StreamingRequest()
        self._streams = self.__stub.BeginStreaming(request, metadata=self.__metadata)
        started_evt.set()
        while True:
            try:
                yield next(self._streams)
            except Exception:
                break

    def end_streaming(self):
        """End monitor streaming from Fluent.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        if self._streams and not self._streams.cancelled():
            self._streams.cancel()
