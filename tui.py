import sys
from typing import Any

import grpc

from ansys.api.fluent.v0 import datamodel_tui_pb2, datamodel_tui_pb2_grpc
from ansys.api.fluent.v0.variant_pb2 import Variant


def parse_server_info_file(filename: str):
    with open(filename, encoding="utf-8") as f:
        lines = f.readlines()
    ip_and_port = lines[0].strip().split(":")
    ip = ip_and_port[0]
    port = int(ip_and_port[1])
    password = lines[1].strip()
    return ip, port, password


def convert_value_to_gvalue(val: Any, gval: Variant):
    """Convert Python datatype to Value type of
    google/protobuf/struct.proto."""
    if isinstance(val, bool):
        gval.bool_value = val
    elif isinstance(val, int) or isinstance(val, float):
        gval.number_value = val
    elif isinstance(val, str):
        gval.string_value = val
    elif isinstance(val, list) or isinstance(val, tuple):
        gval.list_value.SetInParent()
        for item in val:
            item_gval = gval.list_value.values.add()
            convert_value_to_gvalue(item, item_gval)
    elif isinstance(val, dict):
        gval.struct_value.SetInParent()
        for k, v in val.items():
            convert_value_to_gvalue(v, gval.struct_value.fields[k])


class CommandExecutor:
    def __init__(self, stub, metadata):
        self._stub = stub
        self._metadata = metadata

    def execute_tui(self, command: str, *args):
        request = datamodel_tui_pb2.ExecuteCommandRequest()
        request.path = command
        convert_value_to_gvalue(args, request.args.fields["tui_args"])
        self._stub.ExecuteCommand(request, metadata=self._metadata)


if __name__ == "__main__":
    ip, port, password = parse_server_info_file(sys.argv[1])
    with grpc.insecure_channel(f"{ip}:{port}") as channel:
        stub = datamodel_tui_pb2_grpc.DataModelStub(channel)
        metadata = [("password", password)]
        executor = CommandExecutor(stub, metadata)
        executor.execute_tui("/file/read_case", "elbow-transient.cas.h5")
        executor.execute_tui("/solve/initialize/hyb_initialization")
        executor.execute_tui("/solve/set/transient_controls/time_step_size", 0.1)
        executor.execute_tui("/solve/dual_time_iterate", 100)
