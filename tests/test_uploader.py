import pytest
from util.meshing_workflow import new_mesh_session  # noqa: F401

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples


def test_base_session_upload(new_mesh_session):
    base_session = new_mesh_session
    with pytest.raises(AttributeError) as e_info:
        base_session._upload(
            examples.path("mixing_elbow.py"), "test_upload_download.py"
        )
    base_session.exit()


def test_base_session_download(new_mesh_session):
    base_session = new_mesh_session
    with pytest.raises(AttributeError) as e_info:
        base_session._download("test_upload_download.py", pyfluent.EXAMPLES_PATH)
    base_session.exit()


def test_session_upload(new_mesh_session):
    session = new_mesh_session
    with pytest.raises(AttributeError) as e_info:
        session._upload(examples.path("mixing_elbow.py"), "test_upload_download.py")
    session.exit()


def test_session_download(new_mesh_session):
    session = new_mesh_session
    with pytest.raises(AttributeError) as e_info:
        session._download("test_upload_download.py", pyfluent.EXAMPLES_PATH)
    session.exit()
