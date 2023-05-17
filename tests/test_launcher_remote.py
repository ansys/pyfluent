"""Test the PyPIM integration."""
import os
from unittest.mock import create_autospec

import grpc
from util.solver_workflow import new_solver_session  # noqa: F401

from ansys.fluent.core.launcher import launcher
import ansys.fluent.core.utils.fluent_version as docker_image_version
import ansys.platform.instancemanagement as pypim


def test_launch_remote_instance(monkeypatch, new_solver_session):
    fluent = new_solver_session
    # Create a mock pypim pretenting it is configured and returning a channel to an already running Fluent
    mock_instance = pypim.Instance(
        definition_name="definitions/fake-fluent",
        name="instances/fake-fluent",
        ready=True,
        status_message=None,
        services={"grpc": pypim.Service(uri=fluent._channel_str, headers={})},
    )
    pim_channel = grpc.insecure_channel(
        fluent._channel_str,
    )
    mock_instance.wait_for_ready = create_autospec(mock_instance.wait_for_ready)
    mock_instance.build_grpc_channel = create_autospec(
        mock_instance.build_grpc_channel, return_value=pim_channel
    )
    mock_instance.delete = create_autospec(mock_instance.delete)

    mock_client = pypim.Client(channel=grpc.insecure_channel("localhost:12345"))
    mock_client.create_instance = create_autospec(
        mock_client.create_instance, return_value=mock_instance
    )

    mock_connect = create_autospec(pypim.connect, return_value=mock_client)
    mock_is_configured = create_autospec(pypim.is_configured, return_value=True)
    monkeypatch.setattr(pypim, "connect", mock_connect)
    monkeypatch.setattr(pypim, "is_configured", mock_is_configured)

    if os.getenv("FLUENT_IMAGE_TAG"):
        monkeypatch.setattr(
            launcher, "get_ansys_version", lambda: docker_image_version.get_version()
        )

    # Start fluent with launch_fluent
    # Note: This is mocking to start Fluent, but actually reusing the common one
    # Thus cleanup_on_exit is set to false
    fluent = launcher.launch_fluent(cleanup_on_exit=False, mode="solver")

    # Assert: PyFluent went through the pypim workflow
    assert mock_is_configured.called
    assert mock_connect.called

    mock_client.create_instance.assert_called_with(
        "fluent-3ddp", product_version="latest"
    )
    assert mock_instance.wait_for_ready.called
    mock_instance.build_grpc_channel.assert_called_with()

    # And it connected using the channel created by PyPIM
    assert fluent._channel == pim_channel

    # and it kept track of the instance to be able to delete it
    assert fluent._remote_instance == mock_instance
