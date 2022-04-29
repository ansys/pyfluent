"""Wrapper over the transcript grpc service of Fluent."""

import grpc

from ansys.api.fluent.v0 import monitor_pb2 as MonitorModule
from ansys.api.fluent.v0 import monitor_pb2_grpc as MonitorGrpcModule


class MonitorsService:
    """
    Class wrapping the transcript grpc service of Fluent.

    Methods
    -------
    begin_streaming
        Begin transcript streaming from Fluent

    """

    def __init__(self, channel: grpc.Channel, metadata):
        self.__stub = MonitorGrpcModule.MonitorStub(channel)
        self.__metadata = metadata
        self._streams = None 

    def get_monitors_info(self):
        monitors_info = {}
        request = MonitorModule.GetMonitorsRequest()
        response = self.__stub.GetMonitors(request, metadata=self.__metadata)
        for monitor_set in response.monitorset:
            monitor_info = {}
            monitor_info["title"] = monitor_set.title
            monitor_info["xlabel"] = monitor_set.xlabel
            monitor_info["ylabel"] = monitor_set.ylabel
            monitor_info["frequency"] = monitor_set.frequency
            monitor_info["type"] = monitor_set.type
            monitor_info["axis"] = monitor_set.axis
            monitor_info["monitors"] = monitor_set.monitors

            monitors_info[monitor_set.name] = monitor_info
        return monitors_info

    def begin_streaming(self):
        """
        Begin monitor streaming from Fluent

        Yields
        -------
        str
            A transcript line
        """
        request = MonitorModule.StreamingRequest()
        self._streams = self.__stub.BeginStreaming(
            request, metadata=self.__metadata
        )

        while True:
            try:
                yield next(self._streams)
            except Exception:
                break

    def end_streaming(self):
        if self._streams and not self._streams.cancelled():
            self._streams.cancel()
