"""
This test file is provided for manual testing (a sample client).
1. Run the server - dummy
2. Run the test
"""
import grpc
from parsers._variant_value_convertor import (
    _convert_value_to_variant,
    _convert_variant_to_value,
)
import pytest

from ansys.api.fluent.v0 import state_engine_pb2, state_engine_pb2_grpc
from tests.run_stateengine_server import kill_server, run_server

BATCH_COMMAND = r"-----Batch-Script-Path----- dummy"


def test_dummy_static_info():
    run_server(BATCH_COMMAND)
    with grpc.insecure_channel("localhost:50055") as channel:
        stub = state_engine_pb2_grpc.StateEngineStub(channel)

        # Gets the static info
        static_info = stub.GetStaticInfo(
            state_engine_pb2.GetStaticInfoRequest(rules="dummy")
        )

        assert (
            static_info.info.singletons["Member_3"].commands["Command_1"].type
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


def test_dummy_update_dict():
    run_server(BATCH_COMMAND)
    with grpc.insecure_channel("localhost:50055") as channel:
        stub = state_engine_pb2_grpc.StateEngineStub(channel)

        # Gets the initial dictionary data
        org_dict = stub.GetState(
            state_engine_pb2.GetStateRequest(path="Member_1/Sample_Dict_1")
        )
        org_dict = _convert_variant_to_value(org_dict.state)

        stub.SetState(
            state_engine_pb2.SetStateRequest(path="Member_1/Sample_Dict_1", state=None)
        )

        request = state_engine_pb2.UpdateDictRequest()
        request.rules = "dummy"
        request.path = "Member_1/Sample_Dict_1"
        _convert_value_to_variant(
            {
                "Parent_1": {"child_1": True, "child_2": "Child of Parent_1"},
                "Parent_2": {"child_3": 3.0},
            },
            request.dicttomerge,
        )
        request.wait = True
        stub.UpdateDict(request)

        updated_dict = stub.GetState(
            state_engine_pb2.GetStateRequest(path="Member_1/Sample_Dict_1")
        )
        assert _convert_variant_to_value(updated_dict.state) == {
            "Parent_1": {"child_1": True, "child_2": "Child of Parent_1"},
            "Parent_2": {"child_3": 3.0},
        }

        _convert_value_to_variant(
            {"Parent_3": {"child_3_1": True}}, request.dicttomerge
        )
        stub.UpdateDict(request)
        updated_dict = stub.GetState(
            state_engine_pb2.GetStateRequest(path="Member_1/Sample_Dict_1")
        )
        assert _convert_variant_to_value(updated_dict.state) == {
            "Parent_1": {"child_1": True, "child_2": "Child of Parent_1"},
            "Parent_2": {"child_3": 3.0},
            "Parent_3": {"child_3_1": True},
        }

        set_org_state = state_engine_pb2.SetStateRequest()
        set_org_state.path = "Member_1/Sample_Dict_1"
        _convert_value_to_variant(org_dict, set_org_state.state)
        stub.SetState(set_org_state)
    kill_server()


@pytest.mark.skip
def test_dummy_object_operations():
    run_server(BATCH_COMMAND)
    with grpc.insecure_channel("localhost:50055") as channel:
        stub = state_engine_pb2_grpc.StateEngineStub(channel)

        # Gets list of creatable named objects from Member_3
        assert stub.GetCreatableObjectNames(
            state_engine_pb2.GetCreatableObjectNamesRequest(path="Member_3")
        ).result == ["Object_1", "Object_2", "Object_3"]
        # Gets list of creatable named objects from Member_1
        assert stub.GetCreatableObjectNames(
            state_engine_pb2.GetCreatableObjectNamesRequest(path="Member_1")
        ).result == ["Object_1"]
        assert (
            stub.GetChildObjectDisplayNames(
                state_engine_pb2.GetChildObjectDisplayNamesRequest(
                    path="Member_3", type="Object_2"
                )
            ).result
            == []
        )
        stub.CreateChildObject(
            state_engine_pb2.CreateChildObjectRequest(
                path="Member_3", parent="Object_2", child="Object_2_A"
            )
        )
        assert stub.GetChildObjectDisplayNames(
            state_engine_pb2.GetChildObjectDisplayNamesRequest(
                path="Member_3", type="Object_2"
            )
        ).result == ["Object_2_A"]
        stub.DeleteChildObject(
            state_engine_pb2.DeleteChildObjectRequest(
                path="Member_3", parent="Object_2", child="Object_2_A"
            )
        )
        assert (
            stub.GetChildObjectDisplayNames(
                state_engine_pb2.GetChildObjectDisplayNamesRequest(
                    path="Member_3", type="Object_2"
                )
            ).result
            == []
        )
    kill_server()
