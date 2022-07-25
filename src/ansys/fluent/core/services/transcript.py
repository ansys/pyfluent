"""Wrapper over the transcript grpc service of Fluent."""

from typing import Generator, List, Tuple

import grpc

from ansys.api.fluent.v0 import transcript_pb2 as TranscriptModule
from ansys.api.fluent.v0 import transcript_pb2_grpc as TranscriptGrpcModule


class TranscriptService:
    """Class wrapping the transcript gRPC service of Fluent.

    Methods
    -------
    begin_streaming
        Begin transcript streaming from Fluent.
    """

    def __init__(self, channel: grpc.Channel, metadata: List[Tuple[str, str]]):
        self.__stub = TranscriptGrpcModule.TranscriptStub(channel)
        self.__metadata = metadata
        self.__streams = None

    def begin_streaming(
        self,
    ) -> Generator[TranscriptModule.TranscriptResponse, None, None]:
        """Begin transcript streaming from Fluent.

        Yields
        ------
        str
            A transcript line
        """
        request = TranscriptModule.TranscriptRequest()
        self.__streams = self.__stub.BeginStreaming(request, metadata=self.__metadata)

        while True:
            try:
                yield next(self.__streams)
            except Exception:
                break

    def end_streaming(self) -> None:
        if self.__streams and not self.__streams.cancelled():
            self.__streams.cancel()
