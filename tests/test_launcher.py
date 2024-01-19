from pathlib import Path
import platform

from beartype.roar import BeartypeCallHintParamViolation
import pytest
from util.fixture_fluent import download_input_file

import ansys.fluent.core as pyfluent
from ansys.fluent.core.exceptions import DisallowedValuesError, InvalidArgument
from ansys.fluent.core.launcher import launcher_utils
from ansys.fluent.core.launcher.launcher import create_launcher
from ansys.fluent.core.launcher.launcher_utils import (
    DockerContainerLaunchNotSupported,
    LaunchFluentError,
    UnexpectedKeywordArgument,
    _build_journal_argument,
    check_docker_support,
    get_fluent_exe_path,
)
from ansys.fluent.core.utils.fluent_version import AnsysVersionNotFound, FluentVersion
import ansys.platform.instancemanagement as pypim


def test_mode():
    with pytest.raises(DisallowedValuesError) as msg:
        pyfluent.launch_fluent(
            mode="meshing-solver",
            start_container=False,
        )


@pytest.mark.standalone
def test_unsuccessful_fluent_connection():
    # start-timeout is intentionally provided to be 2s for the connection to fail
    with pytest.raises(TimeoutError) as msg:
        pyfluent.launch_fluent(mode="solver", start_timeout=2)


def test_additional_argument_g_gu():
    default_windows_flag = launcher_utils._is_windows()
    launcher_utils._is_windows = lambda: True
    try:
        with pytest.raises(InvalidArgument) as msg:
            pyfluent.launch_fluent(
                mode="solver",
                show_gui=True,
                additional_arguments="-g",
                start_container=False,
            )
        with pytest.raises(InvalidArgument) as msg:
            pyfluent.launch_fluent(
                mode="solver", additional_arguments="-gu", start_container=False
            )
    finally:
        launcher_utils._is_windows = lambda: default_windows_flag


def test_container_launcher():
    if not check_docker_support():
        with pytest.raises(DockerContainerLaunchNotSupported) as msg:
            container_dict_1 = pyfluent.launch_fluent(start_container=True)
            container_dict_2 = pyfluent.launch_fluent(
                start_container=True, dry_run=True
            )

    if check_docker_support():
        # test dry_run
        container_dict = pyfluent.launch_fluent(start_container=True, dry_run=True)
        assert isinstance(container_dict, dict)
        assert len(container_dict) > 1

        # test run with configuration dict
        session = pyfluent.launch_fluent(container_dict=container_dict)
        assert session.health_check_service.is_serving


@pytest.mark.standalone
def test_case_load():
    # Test that launch_fluent() works with a case file as an argument
    _, cas_path = download_input_file(
        "pyfluent/mixing_elbow",
        "mixing_elbow.cas.h5",
    )
    session = pyfluent.launch_fluent(case_file_name=cas_path)

    # Case loaded
    assert session.setup.boundary_conditions.is_active()
    # Mesh available because not lightweight
    fluent_version = float(session.get_fluent_version()[:-2])
    if not fluent_version < 23.1:
        assert session.mesh.quality.is_active()
    # Data not loaded
    assert not session.field_data.is_data_valid()

    session.exit()


@pytest.mark.standalone
@pytest.mark.fluent_version(">=23.2")
def test_case_lightweight_setup():
    # Test that launch_fluent() correctly performs lightweight setup
    _, cas_path = download_input_file(
        "pyfluent/mixing_elbow",
        "mixing_elbow.cas.h5",
    )
    session = pyfluent.launch_fluent(
        case_file_name=cas_path,
        lightweight_mode=True,
    )

    # Case loaded
    assert session.setup.boundary_conditions.is_active()
    # Mesh not available because lightweight
    assert not session.mesh.quality.is_active()
    # Data not loaded
    assert not session.field_data.is_data_valid()


@pytest.mark.standalone
def test_case_data_load():
    # Test that launch_fluent() works with a case+data file as an argument
    _, cas_dat_path = download_input_file(
        "pyfluent/mixing_elbow",
        "mixing_elbow.cas.h5",
        "mixing_elbow.dat.h5",
    )
    session = pyfluent.launch_fluent(case_data_file_name=cas_dat_path)

    # Case loaded
    assert session.setup.boundary_conditions.is_active()
    # Mesh available because not lightweight
    fluent_version = float(session.get_fluent_version()[:-2])
    if not fluent_version < 23.1:
        assert session.mesh.quality.is_active()
    # Data loaded
    assert session.field_data.is_data_valid()

    session.exit()


def test_gpu_launch_arg(helpers, monkeypatch):
    # The launch process is terminated intentionally to verify whether the fluent launch string
    # (which is available in the error message) is generated correctly.
    helpers.mock_awp_vars()
    monkeypatch.setenv("PYFLUENT_LAUNCH_CONTAINER", "0")
    with pytest.raises(LaunchFluentError) as error:
        pyfluent.launch_fluent(gpu=True, start_timeout=0)

    assert "-gpu" in str(error.value).split()


def test_gpu_launch_arg_additional_arg(helpers, monkeypatch):
    # The launch process is terminated intentionally to verify whether the fluent launch string
    # (which is available in the error message) is generated correctly.
    helpers.mock_awp_vars()
    monkeypatch.setenv("PYFLUENT_LAUNCH_CONTAINER", "0")
    with pytest.raises(LaunchFluentError) as error:
        pyfluent.launch_fluent(additional_arguments="-gpu", start_timeout=0)

    assert "-gpu" in str(error.value).split()


def test_kwargs():
    with pytest.raises(UnexpectedKeywordArgument):
        pyfluent.launch_fluent(abc=1, meshing_mode=True)
    with pytest.raises(UnexpectedKeywordArgument):
        pyfluent.launch_fluent(abc=1, xyz=2)


def test_get_fluent_exe_path_when_nothing_is_set(helpers):
    helpers.delete_all_awp_vars()
    with pytest.raises(AnsysVersionNotFound):
        get_fluent_exe_path()
    with pytest.raises(AnsysVersionNotFound):
        FluentVersion.get_latest_installed()


def test_get_fluent_exe_path_from_awp_root_222(helpers):
    helpers.mock_awp_vars(version="222")
    if platform.system() == "Windows":
        expected_path = Path("ansys_inc/v222/fluent") / "ntbin" / "win64" / "fluent.exe"
    else:
        expected_path = Path("ansys_inc/v222/fluent") / "bin" / "fluent"
    assert FluentVersion.get_latest_installed() == FluentVersion.v222
    assert get_fluent_exe_path() == expected_path


def test_get_fluent_exe_path_from_awp_root_231(helpers):
    helpers.mock_awp_vars(version="231")
    if platform.system() == "Windows":
        expected_path = Path("ansys_inc/v231/fluent") / "ntbin" / "win64" / "fluent.exe"
    else:
        expected_path = Path("ansys_inc/v231/fluent") / "bin" / "fluent"
    assert FluentVersion.get_latest_installed() == FluentVersion.v231
    assert get_fluent_exe_path() == expected_path


def test_get_fluent_exe_path_from_awp_root_232(helpers):
    helpers.mock_awp_vars(version="232")
    if platform.system() == "Windows":
        expected_path = Path("ansys_inc/v232/fluent") / "ntbin" / "win64" / "fluent.exe"
    else:
        expected_path = Path("ansys_inc/v232/fluent") / "bin" / "fluent"
    assert FluentVersion.get_latest_installed() == FluentVersion.v232
    assert get_fluent_exe_path() == expected_path


def test_get_fluent_exe_path_from_awp_root_241(helpers):
    helpers.mock_awp_vars(version="241")
    if platform.system() == "Windows":
        expected_path = Path("ansys_inc/v241/fluent") / "ntbin" / "win64" / "fluent.exe"
    else:
        expected_path = Path("ansys_inc/v241/fluent") / "bin" / "fluent"
    assert FluentVersion.get_latest_installed() == FluentVersion.v241
    assert get_fluent_exe_path() == expected_path


def test_get_fluent_exe_path_from_product_version_launcher_arg(helpers):
    helpers.mock_awp_vars()
    if platform.system() == "Windows":
        expected_path = Path("ansys_inc/v231/fluent") / "ntbin" / "win64" / "fluent.exe"
    else:
        expected_path = Path("ansys_inc/v231/fluent") / "bin" / "fluent"
    assert get_fluent_exe_path(product_version="23.1.0") == expected_path


def test_get_fluent_exe_path_from_pyfluent_fluent_root(helpers, monkeypatch):
    helpers.mock_awp_vars()
    monkeypatch.setenv("PYFLUENT_FLUENT_ROOT", "dev/vNNN/fluent")
    if platform.system() == "Windows":
        expected_path = Path("dev/vNNN/fluent") / "ntbin" / "win64" / "fluent.exe"
    else:
        expected_path = Path("dev/vNNN/fluent") / "bin" / "fluent"
    assert get_fluent_exe_path(product_version="23.1.0") == expected_path


def test_watchdog_launch(monkeypatch):
    monkeypatch.setenv("PYFLUENT_WATCHDOG_EXCEPTION_ON_ERROR", "1")
    pyfluent.launch_fluent(start_watchdog=True)


def test_fluent_launchers():
    if not check_docker_support() and not pypim.is_configured():
        standalone_meshing_launcher = create_launcher("standalone", mode="meshing")
        standalone_meshing_session = standalone_meshing_launcher()
        assert standalone_meshing_session

        standalone_solver_launcher = create_launcher("standalone")
        standalone_solver_session = standalone_solver_launcher()
        assert standalone_solver_session

    if check_docker_support():
        container_meshing_launcher = create_launcher("container", mode="meshing")
        container_meshing_session = container_meshing_launcher()
        assert container_meshing_session

        container_solver_launcher = create_launcher("container")
        container_solver_session = container_solver_launcher()
        assert container_solver_session

    if pypim.is_configured():
        pim_meshing_launcher = create_launcher("pim", mode="meshing")
        pim_meshing_session = pim_meshing_launcher()
        assert pim_meshing_session

        pim_solver_launcher = create_launcher("pim")
        pim_solver_session = pim_solver_launcher()
        assert pim_solver_session


@pytest.mark.parametrize(
    "topy,journal_file_names,result,raises",
    [
        (None, "a.jou", ' -i "a.jou"', pytest.wont_raise()),
        (None, ["a.jou", "b.jou"], ' -i "a.jou" -i "b.jou"', pytest.wont_raise()),
        (True, "a.jou", ' -i "a.jou" -topy', pytest.wont_raise()),
        (True, ["a.jou", "b.jou"], ' -i "a.jou" -i "b.jou" -topy', pytest.wont_raise()),
        ("c.py", "a.jou", ' -i "a.jou" -topy="c.py"', pytest.wont_raise()),
        (
            "c.py",
            ["a.jou", "b.jou"],
            ' -i "a.jou" -i "b.jou" -topy="c.py"',
            pytest.wont_raise(),
        ),
        (None, 5, None, pytest.raises(BeartypeCallHintParamViolation)),
        (True, None, None, pytest.raises(InvalidArgument)),
    ],
)
def test_build_journal_argument(topy, journal_file_names, result, raises):
    with raises:
        assert _build_journal_argument(topy, journal_file_names) == result
