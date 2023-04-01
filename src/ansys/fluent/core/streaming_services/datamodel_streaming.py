from ansys.api.fluent.v0 import datamodel_se_pb2
from ansys.fluent.core.streaming_services.streaming import StreamingService


class DatamodelStream(StreamingService):
    """Encapsulates a datamodel streaming service."""

    def __init__(self, service):
        """Instantiate DatamodelStream."""
        super().__init__(
            target=DatamodelStream._process_streaming,
            streaming_service=service(),
        )

    def _process_streaming(
        self, started_evt, rules, no_commands_diff_state, *args, **kwargs
    ):
        """Processes datamodel events."""
        data_model_request = datamodel_se_pb2.DataModelRequest(*args, **kwargs)
        data_model_request.rules = rules
        if no_commands_diff_state:
            data_model_request.diffstate = datamodel_se_pb2.DIFFSTATE_NOCOMMANDS
        responses = self._streaming_service.begin_streaming(
            data_model_request, started_evt
        )
        while True:
            try:
                response: datamodel_se_pb2.DataModelResponse = next(responses)
                with self._lock:
                    self._streaming = True
                    for _, cb_list in self._service_callbacks.items():
                        state = response.state if hasattr(response, "state") else None
                        deleted_paths = getattr(response, "deletedpaths", None)
                        cb_list[0](state=state, deleted_paths=deleted_paths)
            except StopIteration:
                break
