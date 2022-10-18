import platform

import pytest

import ansys.fluent.core as pyfluent
from ansys.fluent.core.launcher.launcher import FLUENT_VERSION


def test_manual_fluent_version_setting():
    """Test case for setting up the Ansys / Fluent version via program"""

    initial_version_info = FLUENT_VERSION[0]

    pyfluent.set_ansys_version("23.1")
    assert FLUENT_VERSION[0] == "23.1"

    pyfluent.set_ansys_version(22.2)
    assert FLUENT_VERSION[0] == "22.2"

    pyfluent.set_ansys_version(version=pyfluent.FluentVersion.version_23R1)
    assert FLUENT_VERSION[0] == "23.1"

    # version does not exist
    with pytest.raises(RuntimeError):
        pyfluent.set_ansys_version(22.1)

    # Resets the global variable to its original state
    pyfluent.set_ansys_version(initial_version_info)


def test_manual_fluent_path_setting():
    """Test case for setting up the path to fluent.exe via program"""
    with pytest.raises(RuntimeError):
        pyfluent.set_fluent_path("X:/dir_1/dir2/xxx.exe")

    with pytest.raises(RuntimeError):
        pyfluent.set_fluent_path("X:/dir_1/dir2/fluent.bat")


@pytest.mark.skip(reason="Can be used only locally.")
def test_unsuccessful_fluent_connection(with_launching_container):
    # start-timeout is intentionally provided to be 2s for the connection to fail
    with pytest.raises(RuntimeError) as msg:
        pyfluent.launch_fluent(mode="solver", start_timeout=2)
    assert msg.value.args[0] == "The launch process has been timed out."


def test_additional_argument_g_gu(with_launching_container):
    if platform.system() == "Windows":
        with pytest.raises(ValueError) as msg:
            pyfluent.launch_fluent(
                mode="solver", show_gui=True, additional_arguments="-g"
            )
        assert (
            msg.value.args[0] == "'-g' and '-gu' is not supported on windows platform."
        )

        with pytest.raises(ValueError) as msg:
            pyfluent.launch_fluent(mode="solver", additional_arguments="-gu")
        assert (
            msg.value.args[0] == "'-g' and '-gu' is not supported on windows platform."
        )
