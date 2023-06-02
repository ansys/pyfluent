from ansys.api.fluent.v0 import otel_exporter_pb2 as OTelExporterProtoModule
from ansys.fluent.core.services.otel_outputs import OTelOutputsService
from ansys.fluent.core.streaming_services.streaming import StreamingService


class OTelOutputsStreaming(StreamingService):
    """Encapsulates otel output streaming service."""

    def __init__(self, channel, metadata):
        """__init__ method of OTelOutputsStreaming class."""
        super().__init__(
            stream_begin_method="BeginStreaming",
            target=OTelOutputsStreaming._process_streaming,
            streaming_service=OTelOutputsService(channel, metadata),
        )

    def _process_streaming(self, id, stream_begin_method, started_evt, *args, **kwargs):
        """Processes otel outputs."""
        request = OTelExporterProtoModule.OTelExporterRequest(*args, **kwargs)
        responses = self._streaming_service.begin_streaming(
            request, started_evt, id=id, stream_begin_method=stream_begin_method
        )
        while True:
            try:
                response: OTelExporterProtoModule.EventResponse = next(responses)
                self._streaming = True
                print(response.output)
            except StopIteration:
                break
