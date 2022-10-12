"""
This test file is provided for manual testing (a sample client).
1. Run the server - dummy
2. Run the test
"""
import grpc

from ansys.api.fluent.v0 import state_engine_pb2, state_engine_pb2_grpc
from tests.run_stateengine_server import kill_server, run_server

BATCH_COMMAND = r"-----Batch-Script-Path----- dummy"


def test_models_static_info():
    run_server(BATCH_COMMAND)
    with grpc.insecure_channel("localhost:50055") as channel:
        stub = state_engine_pb2_grpc.StateEngineStub(channel)

        # Gets the static info
        static_info = stub.GetStaticInfo(
            state_engine_pb2.GetStaticInfoRequest(rules="dummy")
        )

        assert (
            static_info.info.namedobjects["Member_3"].commands["Command_1"].type
            == "Command"
        )
        assert (
            static_info.info.singletons["Member_1"]
            .singletons["Child_Singleton_member_1"]
            .singletons["member_1"]
            .parameters["member_2"]
            .type
            == "Real"
        )
        assert (
            static_info.info.singletons["Member_1"].commands["Delete"].type == "Command"
        )
        assert (
            static_info.info.singletons["Member_1"]
            .commands["Delete"]
            .commandinfo.returntype
            == "Logical"
        )
        assert static_info.info.commands["Member_2"].type == "Command"
    kill_server()
