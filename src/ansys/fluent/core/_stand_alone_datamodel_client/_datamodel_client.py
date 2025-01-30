# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Client side implementation of the stand-alone datamodel server."""

from pathlib import Path

import grpc

from ansys.fluent.core.services.datamodel_se import (
    DatamodelService,
    PySimpleMenuGeneric,
)
from tests.run_stateengine_server import kill_server, run_server


def run_datamodel_server(batch_file_name: str | Path, rules):
    """Run the datamodel server."""
    run_command = str(batch_file_name) + " " + rules
    run_server(run_command)
    _channel = grpc.insecure_channel("localhost:50055")
    _data_model_service = DatamodelService(channel=_channel, metadata=[])

    return PySimpleMenuGeneric(_data_model_service, rules)


def close_server():
    """Close the server."""
    grpc.insecure_channel("localhost:50055").close()
    try:
        kill_server()
        print("Server closed successfully.")
    except OSError:
        print(
            "WARNING: Attempt to kill server failed!!! \nPlease kill the server manually."
        )
