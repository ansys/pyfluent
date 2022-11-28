"""Wrapper over the transcript grpc service of Fluent."""

from typing import List, Tuple

import grpc

from ansys.api.fluent.v0 import transcript_pb2 as TranscriptModule
from ansys.api.fluent.v0 import transcript_pb2_grpc as TranscriptGrpcModule
from ansys.fluent.core.services.streaming import StreamingService


class TranscriptService(StreamingService):
    """Class wrapping the transcript gRPC service of Fluent."""

    def __init__(self, channel: grpc.Channel, metadata: List[Tuple[str, str]]):
        super().__init__(
            stub=TranscriptGrpcModule.TranscriptStub(channel),
            request=TranscriptModule.TranscriptRequest(),
            metadata=metadata,
        )
