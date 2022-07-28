"""Wrapper over the events gRPC service of Fluent."""

import grpc

from ansys.api.fluent.v0 import events_pb2 as EventsProtoModule
from ansys.api.fluent.v0 import events_pb2_grpc as EventsGrpcModule


class EventsService:
    """Class wrapping the events gRPC service of Fluent."""

    def __init__(self, channel: grpc.Channel, metadata):
        self.__stub = EventsGrpcModule.EventsStub(channel)
        self.__metadata = metadata
        self.__streams = None

    def begin_streaming(self, started_evt):
        """Begin events streaming from Fluent.

        Yields
        ------
        Event
        """
        request = EventsProtoModule.BeginStreamingRequest()
        self.__streams = self.__stub.BeginStreaming(request, metadata=self.__metadata)
        started_evt.set()
        while True:
            try:
                yield next(self.__streams)
            except Exception:
                break

    def end_streaming(self):
        """End events streaming from Fluent."""

        if self.__streams and not self.__streams.cancelled():
            self.__streams.cancel()
