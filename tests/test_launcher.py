import pytest

import ansys.fluent.core as pyfluent
from ansys.fluent.core.launcher.launcher import FLUENT_EXE_PATH, FLUENT_VERSION


def test_manual_fluent_version_setting():
    """Test case for setting up the Ansys / Fluent version via program"""
    pyfluent.set_ansys_version("23.1")
    assert FLUENT_VERSION[0] == "23.1"

    pyfluent.set_ansys_version(22.2)
    assert FLUENT_VERSION[0] == "22.2"

    pyfluent.set_ansys_version(version=pyfluent.FluentVersion.version_23R1)
    assert FLUENT_VERSION[0] == "23.1"

    # version does not exist
    with pytest.raises(RuntimeError):
        pyfluent.set_ansys_version(22.1)


def test_manual_fluent_path_setting():
    """Test case for setting up the path to fluent.exe via program"""
    pyfluent.set_fluent_path("X:/dir_1/dir2/fluent.exe")
    assert FLUENT_EXE_PATH[0] == "X:/dir_1/dir2/fluent.exe"

    # fluent.exe does not exist
    with pytest.raises(RuntimeError):
        pyfluent.set_fluent_path("X:/dir_1/dir2/xxx.exe")

    with pytest.raises(RuntimeError):
        pyfluent.set_fluent_path("X:/dir_1/dir2/fluent.bat")
