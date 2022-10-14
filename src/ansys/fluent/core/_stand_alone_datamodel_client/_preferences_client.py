"""Sample testing code (next)."""
from enum import Enum
from pathlib import Path
from typing import Dict, Union

import grpc
from parsers._variant_value_convertor import (
    _convert_value_to_variant,
    _convert_variant_to_value,
)

from ansys.api.fluent.v0 import datamodel_se_pb2, datamodel_se_pb2_grpc
from tests.run_stateengine_server import kill_server, run_server


class StateType(Enum):
    string = (str, "string_state")
    boolean = (bool, "bool_state")


class _PreferencesClient:
    def __init__(self):
        self._channel = None
        self._stub = None

    def run_preferences_server(self, batch_file_path: Union[str, Path]):
        run_command = str(batch_file_path) + " preferences"
        run_server(run_command)
        self._channel = grpc.insecure_channel("localhost:50055")
        self._stub = datamodel_se_pb2_grpc.DataModelStub(self._channel)

    def set_state(self, path: str, state: str):
        state_type = None
        # TODO: Later use the Enum class StateType.
        if type(state) == str:
            state_type = "string_state"
        if type(state) == bool:
            state_type = "bool_state"
        # Sets the color theme to be dark.
        self._stub.setState(
            datamodel_se_pb2.SetStateRequest(path=path, state={state_type: state})
        )

    def get_state(self, path: str):
        updated_preferences_dict = self._stub.getState(
            datamodel_se_pb2.GetStateRequest(path=path)
        )
        return _convert_variant_to_value(updated_preferences_dict.state)

    def get_static_info(self, rules: str):
        return self._stub.getStaticInfo(
            datamodel_se_pb2.GetStaticInfoRequest(rules=rules)
        )

    def update_dict(self, rules: str, path: str, dict_to_merge: Dict):
        request = datamodel_se_pb2.UpdateDictRequest()
        request.rules = rules
        request.path = path
        _convert_value_to_variant(dict_to_merge, request.dicttomerge)
        request.wait = True
        self._stub.updateDict(request)

    def getAttributeValue(self):
        # TODO: to be implemented
        pass

    def deleteObject(self):
        # TODO: to be implemented
        pass

    def executeCommand(self):
        # TODO: to be implemented
        pass

    def create_command_arguments(self):
        self._stub.createCommandArguments(
            datamodel_se_pb2.CreateCommandArgumentsRequest()
        )

    def delete_command_arguments(self):
        self._stub.deleteCommandArguments(
            datamodel_se_pb2.DeleteCommandArgumentsRequest()
        )

    def close_server(self):
        self._channel.close()
        try:
            kill_server()
            print("Server closed successfully.")
        except OSError:
            print(
                "WARNING: Attempt to kill server failed!!! \nPlease kill the server manually."
            )
