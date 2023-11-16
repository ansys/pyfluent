import pytest
from util.meshing_workflow import new_mesh_session  # noqa: F401
from util.solver_workflow import new_solver_session  # noqa: F401

from ansys.fluent.core import examples
from ansys.fluent.core.utils.file_transfer_service import PyPIMConfigurationError

import_file_name = examples.download_file(
    "mixing_elbow.msh.h5", "pyfluent/mixing_elbow"
)


def test_meshing_session_upload(new_mesh_session):
    session = new_mesh_session
    with pytest.raises(PyPIMConfigurationError) as e_info:
        session.upload(import_file_name)
    session.exit()


def test_meshing_session_download(new_mesh_session):
    session = new_mesh_session
    with pytest.raises(PyPIMConfigurationError) as e_info:
        session.download(import_file_name)
    session.exit()


def test_solver_session_upload(new_solver_session):
    session = new_solver_session
    with pytest.raises(PyPIMConfigurationError) as e_info:
        session.upload(import_file_name)
    session.exit()


def test_solver_session_download(new_solver_session):
    session = new_solver_session
    with pytest.raises(PyPIMConfigurationError) as e_info:
        session.download(import_file_name)
    session.exit()
