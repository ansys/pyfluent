"""Test the PyPIM integration."""
from unittest.mock import create_autospec

import grpc

# from ansys.fluent.core import launch_fluent
import ansys.platform.instancemanagement as pypim


def test_launch_remote_instance(monkeypatch, mapdl):
    # Create a mock pypim pretenting it is configured and returning a channel to an already running mapdl
    mock_instance = pypim.Instance(
        definition_name="definitions/fake-mapdl",
        name="instances/fake-mapdl",
        ready=True,
        status_message=None,
        services={"grpc": pypim.Service(uri=mapdl._channel_str, headers={})},
    )
    pim_channel = grpc.insecure_channel(
        mapdl._channel_str,
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

    # Start MAPDL with launch_mapdl
    # Note: This is mocking to start MAPDL, but actually reusing the common one
    # Thus cleanup_on_exit is set to false
    mapdl = launch_mapdl(cleanup_on_exit=False)

    # Assert: pymapdl went through the pypim workflow
    assert mock_is_configured.called
    assert mock_connect.called
    mock_client.create_instance.assert_called_with(
        product_name="mapdl", product_version=None
    )
    assert mock_instance.wait_for_ready.called
    mock_instance.build_grpc_channel.assert_called_with(
        options=[
            ("grpc.max_receive_message_length", MAX_MESSAGE_LENGTH),
        ]
    )

    # And it connected using the channel created by PyPIM
    assert mapdl._channel == pim_channel

    # and it kept track of the instance to be able to delete it
    assert mapdl._remote_instance == mock_instance
