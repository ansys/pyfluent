"""Test the PyPIM integration."""
from concurrent import futures
import os
from unittest.mock import create_autospec

import grpc
from grpc_health.v1 import health_pb2_grpc
import pytest
from test_session import MockHealthServicer, MockSchemeEvalServicer
from util.solver_workflow import new_solver_session  # noqa: F401

from ansys.api.fluent.v0 import scheme_eval_pb2_grpc
from ansys.fluent.core.fluent_connection import (
    FluentConnection,
    UnsupportedRemoteFluentInstance,
)
from ansys.fluent.core.launcher import launcher
from ansys.fluent.core.session import BaseSession
import ansys.fluent.core.utils.fluent_version as docker_image_version
from ansys.fluent.core.utils.fluent_version import FluentVersion
from ansys.fluent.core.utils.networking import get_free_port
import ansys.platform.instancemanagement as pypim


def test_launch_remote_instance(monkeypatch, new_solver_session):
    fluent = new_solver_session
    # Create a mock pypim pretending it is configured and returning a channel to an already running Fluent
    mock_instance = pypim.Instance(
        definition_name="definitions/fake-fluent",
        name="instances/fake-fluent",
        ready=True,
        status_message=None,
        services={
            "grpc": pypim.Service(uri=fluent.fluent_connection._channel_str, headers={})
        },
    )
    pim_channel = grpc.insecure_channel(
        fluent.fluent_connection._channel_str,
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
            FluentVersion,
            "get_latest_installed",
            lambda: docker_image_version.get_version(),
        )

    # Start fluent with launch_fluent
    # Note: This is mocking to start Fluent, but actually reusing the common one
    # Thus cleanup_on_exit is set to false
    fluent = launcher.launch_fluent(cleanup_on_exit=False, mode="solver")

    # Assert: PyFluent went through the pypim workflow
    assert mock_is_configured.called
    assert mock_connect.called

    mock_client.create_instance.assert_called_with("fluent-3ddp", product_version=None)
    assert mock_instance.wait_for_ready.called
    mock_instance.build_grpc_channel.assert_called_with()

    # And it connected using the channel created by PyPIM
    assert fluent.fluent_connection._channel == pim_channel

    # and it kept track of the instance to be able to delete it
    assert fluent.fluent_connection._remote_instance == mock_instance

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    ip = "127.0.0.1"
    port = get_free_port()
    server.add_insecure_port(f"{ip}:{port}")
    health_pb2_grpc.add_HealthServicer_to_server(MockHealthServicer(), server)
    scheme_eval_pb2_grpc.add_SchemeEvalServicer_to_server(
        MockSchemeEvalServicer(), server
    )
    server.start()

    with pytest.raises(UnsupportedRemoteFluentInstance) as msg:
        session = BaseSession(
            FluentConnection(
                ip=ip,
                port=port,
                password="12345",
                remote_instance=mock_instance,
                cleanup_on_exit=False,
            )
        )
        session.exit(wait=60)
        session.fluent_connection.wait_process_finished(wait=60)
