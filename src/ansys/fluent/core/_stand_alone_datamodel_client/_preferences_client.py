"""Sample testing code (next)."""
from enum import Enum
from pathlib import Path
from typing import Dict, Union

import grpc

from ansys.fluent.core.services.datamodel_se import (
    DatamodelService,
    PyCommand,
    PyDictionary,
    PyMenu,
)
from tests.run_stateengine_server import kill_server, run_server


class StateType(Enum):
    string = (str, "string_state")
    boolean = (bool, "bool_state")


class _PreferencesClient:
    def __init__(self):
        self._channel = None
        self._data_model_service = None

    def run_preferences_server(self, batch_file_path: Union[str, Path]):
        run_command = str(batch_file_path) + " preferences"
        run_server(run_command)
        self._channel = grpc.insecure_channel("localhost:50055")
        self._data_model_service = DatamodelService(channel=self._channel, metadata=[])

    def set_state(self, path: str, state: str):
        py_menu = PyMenu(
            self._data_model_service, rules="preferences", path=[(path, "")]
        )
        return py_menu.set_state(state)

    def get_state(self, path: str):
        py_menu = PyMenu(
            self._data_model_service, rules="preferences", path=[(path, "")]
        )
        return py_menu.get_state()

    def get_static_info(self, rules: str):
        py_command = PyCommand(self._data_model_service, rules=rules, command="")
        return py_command._get_static_info()

    def update_dict(self, rules: str, path: str, dict_to_merge: Dict):
        py_dictionary = PyDictionary(
            self._data_model_service, rules=rules, path=[(path, "")]
        )
        return py_dictionary.update_dict(dict_to_merge)

    def get_attrib_value(self, path: str, attribute: str):
        py_menu = PyMenu(
            self._data_model_service, rules="preferences", path=[(path, "")]
        )
        return py_menu.get_attrib_value(attribute)

    def deleteObject(self):
        # TODO: to be implemented
        pass

    def executeCommand(self):
        # TODO: to be implemented
        pass

    def create_command_arguments(self):
        pass
        # self._stub.createCommandArguments(
        #     datamodel_se_pb2.CreateCommandArgumentsRequest()
        # )

    def delete_command_arguments(self):
        pass
        # self._stub.deleteCommandArguments(
        #     datamodel_se_pb2.DeleteCommandArgumentsRequest()
        # )

    def close_server(self):
        self._channel.close()
        try:
            kill_server()
            print("Server closed successfully.")
        except OSError:
            print(
                "WARNING: Attempt to kill server failed!!! \nPlease kill the server manually."
            )
