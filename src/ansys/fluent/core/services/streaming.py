"""Wrapper over the streaming gRPC services of Fluent."""

from typing import Generator, List, Tuple


class _StreamingServiceHelper:
    """Helper Class providing API to start/stop gRPC streaming services of Fluent.

    Methods
    -------
    begin_streaming(request, started_evt)
        Begin streaming from Fluent.
    end_streaming()
        End streaming
    """

    def __init__(self, stub, metadata: List[Tuple[str, str]], stream_begin_method):
        """__init__ method of StreamingService class."""
        self._stub = stub
        self._metadata = metadata
        self._stream_begin_method = stream_begin_method
        self._streams = None

    def begin_streaming(self, request, started_evt) -> Generator:
        """Begin streaming from Fluent."""
        self._streams = getattr(self._stub, self._stream_begin_method)(
            request, metadata=self._metadata
        )
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


class StreamingService:
    """Class wrapping the streaming gRPC services of Fluent.

    Methods
    -------
    begin_streaming(request, started_evt, ID, stream_begin_method)
        Begin streaming from Fluent.
    end_streaming(ID, stream_begin_method)
        End streaming
    """

    def __init__(self, stub, metadata: List[Tuple[str, str]]):
        """__init__ method of StreamingService class."""
        self._stub = stub
        self._metadata = metadata
        self._streamHelper = {}

    def begin_streaming(
        self, request, started_evt, id, stream_begin_method
    ) -> Generator:
        """Begin streaming from Fluent."""
        if id in self._streamHelper:
            return
        self._streamHelper[id + stream_begin_method] = _StreamingServiceHelper(
            self._stub, self._metadata, stream_begin_method
        )
        return self._streamHelper[id + stream_begin_method].begin_streaming(
            request, started_evt
        )

    def end_streaming(self, id, stream_begin_method) -> None:
        """End streaming from Fluent."""
        self._streamHelper[id + stream_begin_method].end_streaming()
        del self._streamHelper[id + stream_begin_method]
