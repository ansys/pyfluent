"""Wrapper over the transcript grpc service of Fluent."""

from typing import Generator, List, Tuple
import grpc

from ansys.api.fluent.v0 import field_data_pb2 as FieldDataProtoModule
from ansys.api.fluent.v0 import field_data_pb2_grpc as FieldGrpcModule
from ansys.fluent.core.services.streaming import StreamingService


class FieldDataStreamingService(StreamingService):
    """Class wrapping the transcript gRPC service of Fluent."""

    def __init__(self, channel: grpc.Channel, metadata: List[Tuple[str, str]]):
        super().__init__(
            stub=FieldGrpcModule.FieldDataStub(channel),
            metadata=metadata
        )

    def begin_streaming(self, request, started_evt) -> Generator:
        """Begin streaming from Fluent."""      
        self._streams = self._stub.BeginFieldsStreaming(request, metadata=self._metadata)
        started_evt.set()
        while True:
            try:
                yield next(self._streams)
            except Exception:
                break