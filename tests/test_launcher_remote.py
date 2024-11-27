"""Test the PyPIM integration."""

from concurrent import futures
import os
from pathlib import Path
import shutil
from unittest.mock import create_autospec
import uuid

import grpc
from grpc_health.v1 import health_pb2_grpc
import pytest
from test_session import MockHealthServicer, MockSchemeEvalServicer

from ansys.api.fluent.v0 import scheme_eval_pb2_grpc
import ansys.fluent.core as pyfluent
from ansys.fluent.core import EXAMPLES_PATH, examples
from ansys.fluent.core.fluent_connection import (
    FluentConnection,
    UnsupportedRemoteFluentInstance,
)
from ansys.fluent.core.launcher import launcher
from ansys.fluent.core.session import BaseSession
from ansys.fluent.core.session_pure_meshing import PureMeshing
from ansys.fluent.core.session_solver import Solver
from ansys.fluent.core.utils.file_transfer_service import PimFileTransferService
import ansys.fluent.core.utils.fluent_version as docker_image_version
from ansys.fluent.core.utils.fluent_version import FluentVersion
from ansys.fluent.core.utils.networking import get_free_port
import ansys.platform.instancemanagement as pypim


def test_launch_remote_instance(monkeypatch, new_solver_session):
    monkeypatch.setattr(pyfluent, "CHECK_HEALTH", False)
    fluent = new_solver_session
    # Create a mock pypim pretending it is configured and returning a channel to an already running Fluent
    mock_instance = pypim.Instance(
        definition_name="definitions/fake-fluent",
        name="instances/fake-fluent",
        ready=True,
        status_message=None,
        services={
            "grpc": pypim.Service(
                uri=fluent._fluent_connection._channel_str, headers={}
            )
        },
    )
    pim_channel = grpc.insecure_channel(
        fluent._fluent_connection._channel_str,
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
    assert fluent._fluent_connection._channel == pim_channel

    # and it kept track of the instance to be able to delete it
    assert fluent._fluent_connection._remote_instance == mock_instance

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    ip = "127.0.0.1"
    port = get_free_port()
    server.add_insecure_port(f"{ip}:{port}")
    health_pb2_grpc.add_HealthServicer_to_server(MockHealthServicer(), server)
    scheme_eval_pb2_grpc.add_SchemeEvalServicer_to_server(
        MockSchemeEvalServicer(), server
    )
    server.start()

    with pytest.raises(UnsupportedRemoteFluentInstance):
        fluent_connection = FluentConnection(
            ip=ip,
            port=port,
            password="12345",
            remote_instance=mock_instance,
            cleanup_on_exit=False,
        )
        session = BaseSession(
            fluent_connection=fluent_connection,
            scheme_eval=fluent_connection._connection_interface.scheme_eval,
        )

        file_transfer_service = PimFileTransferService(pim_instance=mock_instance)
        assert not file_transfer_service.file_service
        assert file_transfer_service.is_configured()
        assert file_transfer_service.pim_instance
        assert file_transfer_service.upload_server

        session.exit(wait=60)
        session._fluent_connection.wait_process_finished(wait=60)


class TransferRequestRecorder:
    def __init__(self):
        self.uploaded_files = list()
        self.downloaded_files = list()

    def uploads(self):
        return self.uploaded_files

    def downloads(self):
        return self.downloaded_files

    def upload(self, file_name: str):
        self.uploaded_files.append(file_name)

    def download(self, file_name: str):
        self.downloaded_files.append(file_name)

    def is_configured(self):
        return True


def rename_downloaded_file(file_path: str, suffix: str) -> str:
    """Rename downloaded file by appending a suffix to the file name.

    Parameters
    ----------
    file_path : str
        Downloaded file path. Can be absolute or relative.
    suffix : str
        Suffix to append to the file name.

    Returns:
    --------
    str
        New file path with the suffix appended to the file name.
    """
    ext = "".join(Path(file_path).suffixes)
    orig_path = Path(file_path)
    file_path = file_path.removesuffix(ext)
    file_path = Path(file_path)
    if file_path.is_absolute():
        new_stem = f"{file_path.stem}{suffix}"
        new_path = file_path.with_stem(new_stem)
        new_path = new_path.with_suffix(ext)
        orig_path.rename(new_path)
        return str(new_path)
    else:
        orig_abs_path = Path(EXAMPLES_PATH) / orig_path
        abs_path = Path(EXAMPLES_PATH) / file_path
        new_stem = f"{file_path.stem}{suffix}"
        new_path = abs_path.with_stem(new_stem)
        new_path = new_path.with_suffix(ext)
        orig_abs_path.rename(new_path)
        return str(file_path.with_stem(new_stem).with_suffix(ext))


@pytest.mark.parametrize(
    "ext,a,b,c,d",
    [(".cas", "a1", "b1", "c1", "d1"), (".cas.gz", "a2", "b2", "c2", "d2")],
)
def test_rename_downloaded_file(ext, a, b, c, d):
    try:
        file_path = Path(EXAMPLES_PATH) / f"{a}{ext}"
        file_path.touch()
        file_path = str(file_path)
        new_file_path = rename_downloaded_file(file_path, "_1")
        assert new_file_path == str(Path(EXAMPLES_PATH) / f"{a}_1{ext}")
    except Exception:
        raise
    finally:
        Path(new_file_path).unlink(missing_ok=True)

    try:
        file_path = f"{b}{ext}"
        (Path(EXAMPLES_PATH) / file_path).touch()
        new_file_path = rename_downloaded_file(file_path, "_1")
        assert new_file_path == f"{b}_1{ext}"
    except Exception:
        raise
    finally:
        (Path(EXAMPLES_PATH) / new_file_path).unlink(missing_ok=True)

    try:
        dir_path = Path(EXAMPLES_PATH) / c
        dir_path.mkdir()
        file_path = dir_path / f"{d}{ext}"
        file_path.touch()
        file_path = str(Path(c) / f"{d}{ext}")
        new_file_path = rename_downloaded_file(file_path, "_1")
        assert new_file_path == str(Path(c) / f"{d}_1{ext}")
    except Exception:
        raise
    finally:
        shutil.rmtree(dir_path, ignore_errors=True)


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=24.2")
def test_file_purpose_on_remote_instance(
    monkeypatch, new_solver_session, new_meshing_session
):
    solver = new_solver_session

    file_service = TransferRequestRecorder()

    solver_session = Solver(
        fluent_connection=solver._fluent_connection,
        scheme_eval=solver._fluent_connection._connection_interface.scheme_eval,
        file_transfer_service=file_service,
    )

    import_file_name = examples.download_file(
        "mixing_elbow.msh.h5", "pyfluent/mixing_elbow"
    )
    suffix = uuid.uuid4().hex
    import_file_name = rename_downloaded_file(import_file_name, f"_{suffix}")

    solver_session.file.read_case(file_name=import_file_name)
    assert file_service.is_configured()
    assert file_service.uploads()
    assert len(file_service.uploads()) == 1
    assert file_service.uploads()[0] == import_file_name

    solver_session.file.write_case(file_name=import_file_name)
    assert file_service.downloads()
    assert len(file_service.downloads()) == 1
    assert file_service.downloads()[0] == import_file_name

    solver_session.exit()

    meshing = new_meshing_session

    meshing_session = PureMeshing(
        fluent_connection=meshing._fluent_connection,
        scheme_eval=meshing._fluent_connection._connection_interface.scheme_eval,
        file_transfer_service=file_service,
    )

    meshing_session.meshing.File.ReadMesh(FileName=import_file_name)
    assert len(file_service.uploads()) == 2
    assert file_service.uploads()[1] == import_file_name

    meshing_session.meshing.File.WriteMesh(FileName=import_file_name)
    assert len(file_service.downloads()) == 2
    assert file_service.downloads()[1] == import_file_name

    meshing_session.exit()
