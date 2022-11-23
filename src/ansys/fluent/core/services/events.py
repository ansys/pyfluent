"""Wrapper over the events gRPC service of Fluent."""

import grpc

from ansys.api.fluent.v0 import events_pb2 as EventsProtoModule
from ansys.api.fluent.v0 import events_pb2_grpc as EventsGrpcModule
from ansys.fluent.core.services.streaming import StreamingService


class EventsService(StreamingService):
    """Class wrapping the events gRPC service of Fluent."""

    def __init__(self, channel: grpc.Channel, metadata):
        super().__init__(
            stub=EventsGrpcModule.EventsStub(channel),
            request=EventsProtoModule.BeginStreamingRequest(),
            metadata=metadata,
        )
