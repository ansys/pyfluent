from pathlib import Path
import platform

import pytest

import ansys.fluent.core as pyfluent
from ansys.fluent.core.launcher import launcher
from ansys.fluent.core.launcher.launcher import get_ansys_version, get_fluent_exe_path


def test_manual_fluent_version_setting():
    """Test case for setting up the Ansys / Fluent version via program"""

    old_ansys_version = launcher._ANSYS_VERSION_SET

    pyfluent.set_ansys_version("23.1.0")
    assert get_ansys_version() == "23.1.0"

    pyfluent.set_ansys_version(22.2)
    assert get_ansys_version() == "22.2.0"

    pyfluent.set_ansys_version(version=pyfluent.FluentVersion.version_23R1)
    assert get_ansys_version() == "23.1.0"

    # version does not exist
    with pytest.raises(RuntimeError):
        pyfluent.set_ansys_version(22.1)

    # Resets the global variable to its original state
    launcher._ANSYS_VERSION_SET = old_ansys_version


def test_manual_fluent_path_setting():
    """Test case for setting up the path to fluent.exe via program"""
    with pytest.raises(RuntimeError):
        pyfluent.set_fluent_exe_path("X:/dir_1/dir2/xxx.exe")

    with pytest.raises(RuntimeError):
        pyfluent.set_fluent_exe_path("X:/dir_1/dir2/fluent.bat")


@pytest.mark.skip(reason="Can be used only locally.")
def test_unsuccessful_fluent_connection(with_launching_container):
    # start-timeout is intentionally provided to be 2s for the connection to fail
    with pytest.raises(RuntimeError) as msg:
        pyfluent.launch_fluent(mode="solver", start_timeout=2)
    assert msg.value.args[0] == "The launch process has been timed out."


def test_additional_argument_g_gu(with_launching_container):

    default_windows_flag = launcher._is_windows()
    launcher._is_windows = lambda: True

    with pytest.raises(ValueError) as msg:
        pyfluent.launch_fluent(mode="solver", show_gui=True, additional_arguments="-g")
    assert msg.value.args[0] == "'-g' and '-gu' is not supported on windows platform."

    with pytest.raises(ValueError) as msg:
        pyfluent.launch_fluent(mode="solver", additional_arguments="-gu")
    assert msg.value.args[0] == "'-g' and '-gu' is not supported on windows platform."

    launcher._is_windows = lambda: default_windows_flag


def test_kwargs():
    with pytest.raises(RuntimeError):
        pyfluent.launch_fluent(abc=1, meshing_mode=True)
    with pytest.raises(TypeError):
        pyfluent.launch_fluent(abc=1, xyz=2)


def test_get_fluent_exe_path_when_nothing_is_set(monkeypatch):
    monkeypatch.delenv("PYFLUENT_FLUENT_ROOT", raising=False)
    monkeypatch.delenv("AWP_ROOT232", raising=False)
    monkeypatch.delenv("AWP_ROOT231", raising=False)
    monkeypatch.delenv("AWP_ROOT222", raising=False)
    with pytest.raises(RuntimeError):
        get_ansys_version()
    with pytest.raises(RuntimeError):
        get_fluent_exe_path()


def test_get_fluent_exe_path_from_awp_root_222(monkeypatch):
    monkeypatch.delenv("PYFLUENT_FLUENT_ROOT", raising=False)
    monkeypatch.delenv("AWP_ROOT232", raising=False)
    monkeypatch.delenv("AWP_ROOT231", raising=False)
    monkeypatch.setenv("AWP_ROOT222", "ansys_inc/v222")
    if platform.system() == "Windows":
        expected_path = Path("ansys_inc/v222/fluent") / "ntbin" / "win64" / "fluent.exe"
    else:
        expected_path = Path("ansys_inc/v222/fluent") / "bin" / "fluent"
    assert get_ansys_version() == "22.2.0"
    assert get_fluent_exe_path() == expected_path


def test_get_fluent_exe_path_from_awp_root_231(monkeypatch):
    monkeypatch.delenv("PYFLUENT_FLUENT_ROOT", raising=False)
    monkeypatch.delenv("AWP_ROOT232", raising=False)
    monkeypatch.setenv("AWP_ROOT231", "ansys_inc/v231")
    monkeypatch.setenv("AWP_ROOT222", "ansys_inc/v222")
    if platform.system() == "Windows":
        expected_path = Path("ansys_inc/v231/fluent") / "ntbin" / "win64" / "fluent.exe"
    else:
        expected_path = Path("ansys_inc/v231/fluent") / "bin" / "fluent"
    assert get_ansys_version() == "23.1.0"
    assert get_fluent_exe_path() == expected_path


def test_get_fluent_exe_path_from_awp_root_232(monkeypatch):
    monkeypatch.delenv("PYFLUENT_FLUENT_ROOT", raising=False)
    monkeypatch.setenv("AWP_ROOT232", "ansys_inc/v232")
    monkeypatch.setenv("AWP_ROOT231", "ansys_inc/v231")
    monkeypatch.setenv("AWP_ROOT222", "ansys_inc/v222")
    if platform.system() == "Windows":
        expected_path = Path("ansys_inc/v232/fluent") / "ntbin" / "win64" / "fluent.exe"
    else:
        expected_path = Path("ansys_inc/v232/fluent") / "bin" / "fluent"
    assert get_ansys_version() == "23.2.0"
    assert get_fluent_exe_path() == expected_path


def test_get_fluent_exe_path_from_set_ansys_version(monkeypatch):
    monkeypatch.delenv("PYFLUENT_FLUENT_ROOT", raising=False)
    monkeypatch.setenv("AWP_ROOT232", "ansys_inc/v232")
    monkeypatch.setenv("AWP_ROOT231", "ansys_inc/v231")
    monkeypatch.setenv("AWP_ROOT222", "ansys_inc/v222")
    old_ansys_version = launcher._ANSYS_VERSION_SET
    pyfluent.set_ansys_version("22.2.0")
    if platform.system() == "Windows":
        expected_path = Path("ansys_inc/v222/fluent") / "ntbin" / "win64" / "fluent.exe"
    else:
        expected_path = Path("ansys_inc/v222/fluent") / "bin" / "fluent"
    assert get_ansys_version() == "22.2.0"
    assert get_fluent_exe_path() == expected_path
    launcher._ANSYS_VERSION_SET = old_ansys_version


def test_get_fluent_exe_path_from_set_fluent_exe_path(monkeypatch):
    monkeypatch.delenv("PYFLUENT_FLUENT_ROOT", raising=False)
    monkeypatch.setenv("AWP_ROOT232", "ansys_inc/v232")
    monkeypatch.setenv("AWP_ROOT231", "ansys_inc/v231")
    monkeypatch.setenv("AWP_ROOT222", "ansys_inc/v222")
    old_ansys_version = launcher._ANSYS_VERSION_SET
    pyfluent.set_ansys_version("22.2.0")
    old_fluent_exe_path = launcher._FLUENT_EXE_PATH_SET
    monkeypatch.setattr(Path, "exists", lambda self: True)
    pyfluent.set_fluent_exe_path("ansys_inc/vNNN/fluent/bin/fluent")
    expected_path = Path("ansys_inc/vNNN/fluent/bin/fluent")
    assert get_fluent_exe_path() == expected_path
    launcher._FLUENT_EXE_PATH_SET = old_fluent_exe_path
    launcher._ANSYS_VERSION_SET = old_ansys_version


def test_get_fluent_exe_path_from_product_version_launcher_arg(monkeypatch):
    monkeypatch.delenv("PYFLUENT_FLUENT_ROOT", raising=False)
    monkeypatch.setenv("AWP_ROOT232", "ansys_inc/v232")
    monkeypatch.setenv("AWP_ROOT231", "ansys_inc/v231")
    monkeypatch.setenv("AWP_ROOT222", "ansys_inc/v222")
    old_ansys_version = launcher._ANSYS_VERSION_SET
    pyfluent.set_ansys_version("22.2.0")
    old_fluent_exe_path = launcher._FLUENT_EXE_PATH_SET
    monkeypatch.setattr(Path, "exists", lambda self: True)
    pyfluent.set_fluent_exe_path("ansys_inc/vNNN/fluent/bin/fluent")
    if platform.system() == "Windows":
        expected_path = Path("ansys_inc/v231/fluent") / "ntbin" / "win64" / "fluent.exe"
    else:
        expected_path = Path("ansys_inc/v231/fluent") / "bin" / "fluent"
    assert get_fluent_exe_path(product_version="23.1.0") == expected_path
    launcher._FLUENT_EXE_PATH_SET = old_fluent_exe_path
    launcher._ANSYS_VERSION_SET = old_ansys_version


def test_get_fluent_exe_path_from_pyfluent_fluent_root(monkeypatch):
    monkeypatch.setenv("PYFLUENT_FLUENT_ROOT", "dev/vNNN/fluent")
    monkeypatch.setenv("AWP_ROOT232", "ansys_inc/v232")
    monkeypatch.setenv("AWP_ROOT231", "ansys_inc/v231")
    monkeypatch.setenv("AWP_ROOT222", "ansys_inc/v222")
    old_ansys_version = launcher._ANSYS_VERSION_SET
    pyfluent.set_ansys_version("22.2.0")
    old_fluent_exe_path = launcher._FLUENT_EXE_PATH_SET
    monkeypatch.setattr(Path, "exists", lambda self: True)
    pyfluent.set_fluent_exe_path("ansys_inc/vNNN/fluent/bin/fluent")
    if platform.system() == "Windows":
        expected_path = Path("dev/vNNN/fluent") / "ntbin" / "win64" / "fluent.exe"
    else:
        expected_path = Path("dev/vNNN/fluent") / "bin" / "fluent"
    assert get_fluent_exe_path(product_version="23.1.0") == expected_path
    launcher._FLUENT_EXE_PATH_SET = old_fluent_exe_path
    launcher._ANSYS_VERSION_SET = old_ansys_version
