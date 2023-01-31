"""This test file is provided for manual testing (a sample client).

1. Run the server - preferences
2. Run the test
"""
import logging

import grpc
from parsers._variant_value_convertor import _convert_variant_to_value

from ansys.api.fluent.v0 import state_engine_pb2, state_engine_pb2_grpc
from tests.run_stateengine_server import kill_server, run_server

BATCH_COMMAND = r"-----Batch-Script-Path----- preferences"


def test_run_appearance_ansys_logo():
    run_server(BATCH_COMMAND)
    with grpc.insecure_channel("localhost:50055") as channel:
        stub = state_engine_pb2_grpc.StateEngineStub(channel)

        # Gets the default value -->> False
        default_val = stub.GetState(
            state_engine_pb2.GetStateRequest(path="Appearance/AnsysLogo/Visible")
        )
        default_val = _convert_variant_to_value(default_val.state)
        assert default_val is False

        # Updates the value -->> True
        stub.SetState(
            state_engine_pb2.SetStateRequest(
                path="Appearance/AnsysLogo/Visible", state={"bool_state": True}
            )
        )

        # Gets the updated value -->> True
        new_val = stub.GetState(
            state_engine_pb2.GetStateRequest(path="Appearance/AnsysLogo/Visible")
        )
        new_val = _convert_variant_to_value(new_val.state)
        assert new_val is True

        # Sets it back to the default value -->> False
        stub.SetState(
            state_engine_pb2.SetStateRequest(
                path="Appearance/AnsysLogo/Visible", state={"bool_state": default_val}
            )
        )
    kill_server()


def test_run_appearance_color_theme():
    run_server(BATCH_COMMAND)
    with grpc.insecure_channel("localhost:50055") as channel:
        stub = state_engine_pb2_grpc.StateEngineStub(channel)

        # Gets the default values
        default_val_color_theme = stub.GetState(
            state_engine_pb2.GetStateRequest(path="Appearance/ColorTheme")
        )
        default_val_color_theme = _convert_variant_to_value(
            default_val_color_theme.state
        )
        assert default_val_color_theme == "Default"

        default_val_graphics_color_theme = stub.GetState(
            state_engine_pb2.GetStateRequest(path="Appearance/GraphicsColorTheme")
        )
        default_val_graphics_color_theme = _convert_variant_to_value(
            default_val_graphics_color_theme.state
        )
        assert default_val_graphics_color_theme == "Gray Gradient"

        # Sets the current state to Dark mode
        stub.SetState(
            state_engine_pb2.SetStateRequest(
                path="Appearance/ColorTheme", state={"string_state": "Dark"}
            )
        )

        # Gets the updated values
        new_val_color_theme = stub.GetState(
            state_engine_pb2.GetStateRequest(path="Appearance/ColorTheme")
        )
        new_val_color_theme = _convert_variant_to_value(new_val_color_theme.state)
        assert new_val_color_theme == "Dark"

        new_val_graphics_color_theme = stub.GetState(
            state_engine_pb2.GetStateRequest(path="Appearance/GraphicsColorTheme")
        )
        new_val_graphics_color_theme = _convert_variant_to_value(
            new_val_graphics_color_theme.state
        )
        assert new_val_graphics_color_theme == "Dark"

        # Sets it back to the default value
        stub.SetState(
            state_engine_pb2.SetStateRequest(
                path="Appearance/ColorTheme",
                state={"string_state": default_val_color_theme},
            )
        )
        stub.SetState(
            state_engine_pb2.SetStateRequest(
                path="Appearance/GraphicsColorTheme",
                state={"string_state": default_val_graphics_color_theme},
            )
        )
    kill_server()


def test_preferences_static_info():
    run_server(BATCH_COMMAND)
    with grpc.insecure_channel("localhost:50055") as channel:
        stub = state_engine_pb2_grpc.StateEngineStub(channel)

        # Gets the static info
        static_info = stub.GetStaticInfo(
            state_engine_pb2.GetStaticInfoRequest(rules="preferences")
        )

        assert (
            static_info.info.singletons["Appearance"]
            .singletons["AnsysLogo"]
            .parameters["Visible"]
            .type
            == "Logical"
        )
        assert (
            static_info.info.singletons["Appearance"].parameters["DefaultView"].type
            == "String"
        )
    kill_server()


if __name__ == "__main__":
    logging.basicConfig()
    test_run_appearance_ansys_logo()
    test_run_appearance_color_theme()
