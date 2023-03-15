from ansys.api.fluent.v0 import datamodel_se_pb2
from ansys.fluent.core.services.datamodel_se import _convert_variant_to_value
from ansys.fluent.core.streaming_services.streaming import StreamingService


class DatamodelStream(StreamingService):
    """Encapsulates a datamodel streaming service."""

    def __init__(self, service):
        """Instantiate DatamodelStream."""
        super().__init__(
            target=DatamodelStream._process_streaming,
            streaming_service=service,
        )

    def _process_streaming(self, started_evt):
        """Processes datamodel events."""
        responses = self._streaming_service.begin_streaming(started_evt)
        while True:
            try:
                response: datamodel_se_pb2.DataModelResponse = next(responses)
                print(response)
                with self._lock:
                    self._streaming = True
                    for _, cb_list in self._service_callbacks.items():
                        state = (
                            _convert_variant_to_value(response.state)
                            if hasattr(response, "state")
                            else None
                        )
                        deleted_paths = getattr(response, "deletedpaths", None)
                        events = getattr(response, "events", None)
                        cb_list[0](
                            state=state, deleted_paths=deleted_paths, events=events
                        )
            except StopIteration:
                break
