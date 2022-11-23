"""Wrapper over the streaming grpc services of Fluent."""

from typing import Generator, List, Tuple


class StreamingService:
    """Class wrapping the streaming gRPC services of Fluent.

    Methods
    -------
    begin_streaming
        Begin streaming from Fluent.

    end_streaming
        End streaming
    """

    def __init__(self, stub, request, metadata: List[Tuple[str, str]]):
        self.__stub = stub
        self.__metadata = metadata
        self.request = request
        self.__streams = None

    def begin_streaming(self, started_evt) -> Generator:
        """Begin streaming from Fluent."""
        request = self.request
        self.__streams = self.__stub.BeginStreaming(request, metadata=self.__metadata)
        started_evt.set()
        while True:
            try:
                yield next(self.__streams)
            except Exception:
                break

    def end_streaming(self) -> None:
        """End streaming from Fluent."""
        if self.__streams and not self.__streams.cancelled():
            self.__streams.cancel()
