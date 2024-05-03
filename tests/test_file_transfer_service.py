"""Test file transfer service."""

import os
import pathlib

import pytest
from util.meshing_workflow import new_mesh_session  # noqa: F401
from util.solver_workflow import new_solver_session  # noqa: F401

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples

if pyfluent.REMOTE_GRPC_FILE_TRANSFER_SERVICE:
    import_case_file_name = examples.download_file(
        "mixing_elbow.cas.h5", "pyfluent/mixing_elbow", return_without_path=False
    )
    import_mesh_file_name = examples.download_file(
        "mixing_elbow.msh.h5", "pyfluent/mixing_elbow", return_without_path=False
    )
else:
    import_case_file_name = examples.download_file(
        "mixing_elbow.cas.h5", "pyfluent/mixing_elbow"
    )
    import_mesh_file_name = examples.download_file(
        "mixing_elbow.msh.h5", "pyfluent/mixing_elbow"
    )


def file_downloaded_to_the_client(file_name: str) -> bool:
    """Check if client file exists.

    Parameters
    ----------
    file_name: str
        File name.

    Returns
    -------
        Whether file exists.
    """
    full_file_name = pathlib.Path(
        "/home/runner/.local/share/ansys_fluent_core/examples"
    ) / os.path.basename(file_name)
    return full_file_name.is_file()


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=24.2")
def test_remote_grpc_fts_container(monkeypatch, new_solver_session, new_mesh_session):
    solver = new_solver_session
    solver.file.read_case(file_name=import_case_file_name)
    solver.file.write_case(file_name="downloaded_solver_mixing_elbow.cas.h5")
    assert solver.file_exists_on_remote("downloaded_solver_mixing_elbow.cas.h5")
    assert file_downloaded_to_the_client("downloaded_solver_mixing_elbow.cas.h5")

    meshing = new_mesh_session
    meshing.meshing.File.ReadMesh(FileName=import_mesh_file_name)
    meshing.meshing.File.WriteMesh(FileName="downloaded_meshing_mixing_elbow.msh.h5")
    assert meshing.file_exists_on_remote("downloaded_meshing_mixing_elbow.msh.h5")
    assert file_downloaded_to_the_client("downloaded_meshing_mixing_elbow.msh.h5")
