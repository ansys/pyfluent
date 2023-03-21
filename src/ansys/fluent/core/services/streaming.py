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

    def __init__(self, stub, metadata: List[Tuple[str, str]]):
        """__init__ method of StreamingService class."""
        self._stub = stub
        self._metadata = metadata
        self._streams = None

    def begin_streaming(self, request, started_evt) -> Generator:
        """Begin streaming from Fluent."""
        self._streams = self._stub.BeginStreaming(request, metadata=self._metadata)
        started_evt.set()
        while True:
            try:
                yield next(self._streams)
            except Exception:
                break

    def end_streaming(self) -> None:
        """End streaming from Fluent."""
        if self._streams and not self._streams.cancelled():
            self._streams.cancel()
