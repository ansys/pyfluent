import pytest

import ansys.fluent.core as pyfluent
from ansys.fluent.core import launch_fluent


def test_base_session():
    base_session = launch_fluent(cleanup_on_exit=False, mode="meshing")
    with pytest.raises(Exception) as e_info:
        base_session._upload(
            pyfluent.EXAMPLES_PATH + "/mixing_elbow.py", "test_upload_download.py"
        )
        base_session._download("test_upload_download.py", pyfluent.EXAMPLES_PATH)
    base_session.exit()


def test_session():
    session = launch_fluent(cleanup_on_exit=False, meshing_mode=True)
    with pytest.raises(Exception) as e_info:
        session._upload(
            pyfluent.EXAMPLES_PATH + "/mixing_elbow.py", "test_upload_download.py"
        )
        session._download("test_upload_download.py", pyfluent.EXAMPLES_PATH)
    session.exit()
