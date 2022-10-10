"""
This test file is provided for manual testing (a sample client).
1. Run the server -> 'models'
2. Run the test
"""
import logging

import grpc
from parsers._variant_value_convertor import (
    _convert_value_to_variant,
    _convert_variant_to_value,
)

from ansys.api.fluent.v0 import state_engine_pb2, state_engine_pb2_grpc


def test_run_models_energy():
    with grpc.insecure_channel("localhost:50055") as channel:
        stub = state_engine_pb2_grpc.StateEngineStub(channel)

        # Gets the default value -->> False
        default_val = stub.GetState(
            state_engine_pb2.GetStateRequest(path="Models/Energy")
        )
        default_val = _convert_variant_to_value(default_val.state)
        assert default_val is False

        # Updates the value -->> True
        stub.SetState(
            state_engine_pb2.SetStateRequest(
                path="Models/Energy", state={"bool_state": True}
            )
        )

        # Gets the updated value -->> True
        new_val = stub.GetState(state_engine_pb2.GetStateRequest(path="Models/Energy"))
        new_val = _convert_variant_to_value(new_val.state)
        assert new_val is True

        # Sets it back to the default value -->> False
        stub.SetState(
            state_engine_pb2.SetStateRequest(
                path="Models/Energy", state={"bool_state": default_val}
            )
        )


def test_run_models_input_data():
    with grpc.insecure_channel("localhost:50055") as channel:
        stub = state_engine_pb2_grpc.StateEngineStub(channel)
        request = state_engine_pb2.SetStateRequest()
        request.path = "ModelsInputData"
        _convert_value_to_variant(
            {"ConfigVars": {"rp-kw?": True}, "RpVars": {"kw-std-on?": True}},
            request.state,
        )
        stub.SetState(request)

        turbulence_model = stub.GetState(
            state_engine_pb2.GetStateRequest(path="Models/Viscous/TurbulenceModel")
        )
        assert _convert_variant_to_value(turbulence_model.state) == "k-omega Standard"

        model_constants = stub.GetState(
            state_engine_pb2.GetStateRequest(path="Models/Viscous/ModelConstants")
        )
        assert _convert_variant_to_value(model_constants.state) == {
            "kw_sig_k": 2.0,
            "kw_beta_i": 0.072,
            "kw_sig_w": 2.0,
            "kw_alpha_star_inf": 1.0,
            "kw_alpha_inf": 0.52,
            "sst_pk_factor": 10.0,
            "kw_beta_star_inf": 0.09,
        }

        # Sets it back to default
        _convert_value_to_variant(
            {"ConfigVars": {"rp-kw?": False}, "RpVars": {"kw-std-on?": False}},
            request.state,
        )
        stub.SetState(request)


if __name__ == "__main__":
    logging.basicConfig()
    test_run_models_energy()
