"""Provides a module for datamodel streaming."""

import logging

from google.protobuf.json_format import MessageToDict

from ansys.api.fluent.v0 import datamodel_se_pb2
import ansys.fluent.core as pyfluent
from ansys.fluent.core.streaming_services.streaming import StreamingService

network_logger: logging.Logger = logging.getLogger("pyfluent.networking")


class DatamodelStream(StreamingService):
    """Encapsulates a datamodel streaming service."""

    def __init__(self, service):
        """Initialize DatamodelStream."""
        super().__init__(
            stream_begin_method="BeginStreaming",
            target=DatamodelStream._process_streaming,
            streaming_service=service,
        )

    def _process_streaming(
        self,
        id,
        stream_begin_method,
        started_evt,
        rules,
        no_commands_diff_state,
        *args,
        **kwargs,
    ):
        """Processes datamodel events."""
        data_model_request = datamodel_se_pb2.DataModelRequest(*args, **kwargs)
        data_model_request.rules = rules
        data_model_request.returnstatechanges = pyfluent.DATAMODEL_RETURN_STATE_CHANGES
        if no_commands_diff_state:
            data_model_request.diffstate = datamodel_se_pb2.DIFFSTATE_NOCOMMANDS
        responses = self._streaming_service.begin_streaming(
            data_model_request,
            started_evt,
            id=id,
            stream_begin_method=stream_begin_method,
        )
        while True:
            try:
                response: datamodel_se_pb2.DataModelResponse = next(responses)
                network_logger.debug(
                    f"GRPC_TRACE: RPC = /grpcRemoting.DataModel/BeginStreaming, response = {MessageToDict(response)}"
                )
                with self._lock:
                    self._streaming = True
                    for _, cb_list in self._service_callbacks.items():
                        state = response.state if hasattr(response, "state") else None
                        deleted_paths = getattr(response, "deletedpaths", None)
                        cb_list[0](state=state, deleted_paths=deleted_paths)
            except StopIteration:
                break
