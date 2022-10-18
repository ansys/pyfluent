"""Client side implementation of the stand-alone datamodel server."""
from pathlib import Path
from typing import Union

import grpc

from ansys.fluent.core.services.datamodel_se import (
    DatamodelService,
    PySimpleMenuGeneric,
)
from tests.run_stateengine_server import kill_server, run_server


def run_datamodel_server(batch_file_path: Union[str, Path], rules):
    run_command = str(batch_file_path) + " " + rules
    run_server(run_command)
    _channel = grpc.insecure_channel("localhost:50055")
    _data_model_service = DatamodelService(channel=_channel, metadata=[])

    return PySimpleMenuGeneric(_data_model_service, rules)


def close_server():
    grpc.insecure_channel("localhost:50055").close()
    try:
        kill_server()
        print("Server closed successfully.")
    except OSError:
        print(
            "WARNING: Attempt to kill server failed!!! \nPlease kill the server manually."
        )
