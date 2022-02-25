"""Wrapper over the transcript grpc service of Fluent."""

import grpc

from ansys.api.fluent.v0 import transcript_pb2 as TranscriptModule
from ansys.api.fluent.v0 import transcript_pb2_grpc as TranscriptGrpcModule


class TranscriptService:
    """
    Class wrapping the transcript grpc service of Fluent.

    Methods
    -------
    begin_streaming
        Begin transcript streaming from Fluent

    """

    def __init__(self, channel: grpc.Channel, metadata):
        self.__stub = TranscriptGrpcModule.TranscriptStub(channel)
        self.__metadata = metadata

    def begin_streaming(self):
        """
        Begin transcript streaming from Fluent

        Yields
        -------
        str
            A transcript line
        """
        request = TranscriptModule.TranscriptRequest()
        self.__streams = self.__stub.BeginStreaming(
            request, metadata=self.__metadata
        )

        while True:
            try:
                yield next(self.__streams)
            except Exception:
                break

    def end_streaming(self):
        if not self.__streams.cancelled():
            self.__streams.cancel()
