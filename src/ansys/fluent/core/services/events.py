"""Wrapper over the events gRPC service of Fluent."""

from typing import List, Tuple

import grpc

from ansys.api.fluent.v0 import events_pb2_grpc as EventsGrpcModule
from ansys.fluent.core.services.streaming import StreamingService


class EventsService(StreamingService):
    """Class wrapping the events gRPC service of Fluent."""

    def __init__(self, channel: grpc.Channel, metadata: List[Tuple[str, str]]):
        """__init__ method of EventsService class."""
        super().__init__(
            stub=EventsGrpcModule.EventsStub(channel),
            metadata=metadata,
        )
