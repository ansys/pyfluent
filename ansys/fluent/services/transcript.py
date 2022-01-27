"""Wrapper over the transcript grpc service of Fluent."""

from ansys.api.fluent.v0 import transcript_pb2 as TranscriptModule
from ansys.api.fluent.v0 import transcript_pb2_grpc as TranscriptGrpcModule

import grpc


class TranscriptService:
    """
    Class wrapping the transcript grpc service of Fluent.

    Methods
    -------
    begin_streaming
        Begin transcript streaming from Fluent

    """

    def __init__(self, channel: grpc.Channel, password: str):
        self.__stub = TranscriptGrpcModule.TranscriptStub(channel)
        self.__metadata = [("password", password)]

    def begin_streaming(self):
        """
        Begin transcript streaming from Fluent

        Yields
        -------
        str
            A transcript line
        """
        request = TranscriptModule.TranscriptRequest()
        yield from self.__stub.BeginStreaming(
            request, metadata=self.__metadata
        )
