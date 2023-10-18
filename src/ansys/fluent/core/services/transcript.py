"""Wrapper over the transcript gRPC service of Fluent."""

from typing import List, Tuple

import grpc

from ansys.api.fluent.v0 import transcript_pb2_grpc as TranscriptGrpcModule
from ansys.fluent.core.services.streaming import StreamingService


class TranscriptService(StreamingService):
    """Class wrapping the transcript gRPC service of Fluent."""

    def __init__(self, channel: grpc.Channel, metadata: List[Tuple[str, str]]):
        """__init__ method of TranscriptService class."""
        super().__init__(
            stub=TranscriptGrpcModule.TranscriptStub(channel),
            metadata=metadata,
        )
