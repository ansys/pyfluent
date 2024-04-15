"""Test file transfer service."""

import pytest

from ansys.fluent.core import examples

import_case_file_name = examples.download_file(
    "mixing_elbow.cas.h5", "pyfluent/mixing_elbow"
)
import_mesh_file_name = examples.download_file(
    "mixing_elbow.msh.h5", "pyfluent/mixing_elbow"
)


@pytest.mark.codegen_required
@pytest.mark.fluent_version(">=24.2")
def test_remote_grpc_fts_container(monkeypatch, new_solver_session, new_mesh_session):
    solver = new_solver_session
    solver.file.read_case(file_name=import_case_file_name)
    solver.file.write_case(file_name="downloaded_solver_mixing_elbow.cas.h5")
    assert solver.file_exists_on_remote("downloaded_solver_mixing_elbow.cas.h5")

    meshing = new_mesh_session
    meshing.meshing.File.ReadMesh(FileName=import_mesh_file_name)
    meshing.meshing.File.WriteMesh(FileName="downloaded_meshing_mixing_elbow.msh.h5")
    assert meshing.file_exists_on_remote("downloaded_meshing_mixing_elbow.msh.h5")
