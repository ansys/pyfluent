"""Wrapper over the otel exporter grpc service of Fluent."""

from typing import List, Tuple

import grpc

from ansys.api.fluent.v0 import otel_exporter_pb2_grpc as OTelExporterGrpcModule
from ansys.fluent.core.services.streaming import StreamingService


class OTelOutputsService(StreamingService):
    """Class wrapping the otel exporter gRPC service of Fluent."""

    def __init__(self, channel: grpc.Channel, metadata: List[Tuple[str, str]]):
        """__init__ method of OTelOutputsService class."""
        super().__init__(
            stub=OTelExporterGrpcModule.OTelExporterStub(channel),
            metadata=metadata,
        )
