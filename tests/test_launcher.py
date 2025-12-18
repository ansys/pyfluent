# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
from pathlib import Path
import platform
import tempfile
from tempfile import TemporaryDirectory

import pytest

import ansys.fluent.core as pyfluent
from ansys.fluent.core import PyFluentDeprecationWarning, PyFluentUserWarning
from ansys.fluent.core.examples.downloads import download_file
from ansys.fluent.core.exceptions import DisallowedValuesError, InvalidArgument
from ansys.fluent.core.launcher import launcher_utils
from ansys.fluent.core.launcher.error_handler import (
    GPUSolverSupportError,
    InvalidIpPort,
    LaunchFluentError,
    _raise_non_gui_exception_in_windows,
)
from ansys.fluent.core.launcher.fluent_container import configure_container_dict
from ansys.fluent.core.launcher.launch_options import (
    FluentLinuxGraphicsDriver,
    FluentMode,
    FluentWindowsGraphicsDriver,
    LaunchMode,
    UIMode,
    _get_graphics_driver,
)
from ansys.fluent.core.launcher.launcher import create_launcher
from ansys.fluent.core.launcher.launcher_utils import (
    ComposeConfig,
    _build_journal_argument,
    is_windows,
)
from ansys.fluent.core.launcher.process_launch_string import (
    _build_fluent_launch_args_string,
    get_fluent_exe_path,
)
from ansys.fluent.core.utils.fluent_version import FluentVersion
import ansys.platform.instancemanagement as pypim


def test_gpu_version_error():
    with pytest.raises(GPUSolverSupportError):
        pyfluent.launch_fluent(
            mode="meshing",
            dimension=2,
            precision="single",
            processor_count=5,
            ui_mode="gui",
            gpu=True,
        )
        pyfluent.setup_for_fluent(
            mode="meshing",
            dimension=2,
            precision="single",
            processor_count=5,
            ui_mode="gui",
            gpu=True,
        )


def test_mode():
    with pytest.raises(DisallowedValuesError):
        pyfluent.launch_fluent(
            mode="meshing-solver",
            start_container=False,
        )


def test_unsuccessful_fluent_connection():
    # start-timeout is intentionally provided to be 1s for the connection to fail
    with pytest.raises(LaunchFluentError) as ex:
        pyfluent.launch_fluent(mode="solver", start_timeout=1)
    # TimeoutError -> LaunchFluentError
    assert isinstance(ex.value.__context__, TimeoutError)


def test_container_timeout_deprecation():
    with pytest.warns(PyFluentDeprecationWarning):
        configure_container_dict([], timeout=0)

    with pytest.warns(PyFluentDeprecationWarning):
        pyfluent.launch_fluent(
            start_container=True, container_dict=dict(timeout=0), dry_run=True
        )


def test_container_timeout_deprecation_override(caplog):
    # timeout should override start_timeout
    with pytest.raises(LaunchFluentError) as ex:
        with pytest.warns(PyFluentDeprecationWarning):
            pyfluent.launch_fluent(
                start_container=True, container_dict=dict(timeout=1), start_timeout=60
            )
    assert isinstance(ex.value.__context__, TimeoutError)
    assert "overridden" in caplog.text


@pytest.mark.fluent_version("<24.1")
def test_non_gui_in_windows_throws_exception():
    default_windows_flag = launcher_utils.is_windows()
    launcher_utils.is_windows = lambda: True
    try:
        with pytest.raises(InvalidArgument):
            _raise_non_gui_exception_in_windows(UIMode.NO_GUI, FluentVersion.v232)
        with pytest.raises(InvalidArgument):
            _raise_non_gui_exception_in_windows(UIMode.NO_GUI, FluentVersion.v231)
        with pytest.raises(InvalidArgument):
            _raise_non_gui_exception_in_windows(UIMode.NO_GUI, FluentVersion.v222)
        with pytest.raises(InvalidArgument):
            _raise_non_gui_exception_in_windows(
                UIMode.NO_GUI_OR_GRAPHICS, FluentVersion.v232
            )
        with pytest.raises(InvalidArgument):
            _raise_non_gui_exception_in_windows(
                UIMode.NO_GUI_OR_GRAPHICS, FluentVersion.v231
            )
        with pytest.raises(InvalidArgument):
            _raise_non_gui_exception_in_windows(
                UIMode.NO_GUI_OR_GRAPHICS, FluentVersion.v222
            )
    finally:
        launcher_utils.is_windows = lambda: default_windows_flag


@pytest.mark.fluent_version(">=24.1")
def test_non_gui_in_windows_does_not_throw_exception():
    default_windows_flag = launcher_utils.is_windows()
    launcher_utils.is_windows = lambda: True
    try:
        _raise_non_gui_exception_in_windows(UIMode.NO_GUI, FluentVersion.v241)
        _raise_non_gui_exception_in_windows(
            UIMode.NO_GUI_OR_GRAPHICS, FluentVersion.v241
        )
        _raise_non_gui_exception_in_windows(UIMode.NO_GUI, FluentVersion.v242)
        _raise_non_gui_exception_in_windows(
            UIMode.NO_GUI_OR_GRAPHICS, FluentVersion.v242
        )
    finally:
        launcher_utils.is_windows = lambda: default_windows_flag


def test_container_launcher():
    # test dry_run
    container_dict = pyfluent.launch_fluent(start_container=True, dry_run=True)
    assert isinstance(container_dict, dict)
    assert len(container_dict) > 1

    # test run with configuration dict
    session = pyfluent.launch_fluent(container_dict=container_dict)
    assert session.is_server_healthy()


def test_container_working_dir():
    pyfluent.config.container_mount_source = None

    container_dict = pyfluent.launch_fluent(start_container=True, dry_run=True)
    assert container_dict["volumes"][0].startswith(os.getcwd())
    assert container_dict["volumes"][0].endswith(pyfluent.config.container_mount_target)
    assert container_dict["working_dir"] == pyfluent.config.container_mount_target
    server_info_matches = [
        arg
        for arg in container_dict["command"]
        if arg.startswith(
            f"-sifile={pyfluent.config.container_mount_target}/serverinfo"
        )
    ]
    assert len(server_info_matches) == 1, "Expected one server info file in command"

    target_mount1 = "/mnt/test1"
    container_dict.update(working_dir=target_mount1)
    container_dict2 = pyfluent.launch_fluent(
        container_dict=container_dict, dry_run=True
    )
    del container_dict
    assert container_dict2["volumes"][0].startswith(os.getcwd())
    assert container_dict2["volumes"][0].endswith(target_mount1)
    assert container_dict2["working_dir"] == target_mount1
    server_info_matches2 = [
        arg
        for arg in container_dict2["command"]
        if arg.startswith(f"-sifile={target_mount1}/serverinfo")
    ]
    assert len(server_info_matches2) == 1, "Expected one server info file in command"

    target_mount2 = "/mnt/test2"
    container_dict2.update(
        volumes=[f"{pyfluent.config.examples_path}:{target_mount2}"],
        working_dir=target_mount2,
    )
    container_dict3 = pyfluent.launch_fluent(
        container_dict=container_dict2, dry_run=True
    )
    del container_dict2
    assert container_dict3["volumes"][0].startswith(pyfluent.config.examples_path)
    assert container_dict3["volumes"][0].endswith(target_mount2)
    assert container_dict3["working_dir"] == target_mount2
    server_info_matches3 = [
        arg
        for arg in container_dict3["command"]
        if arg.startswith(f"-sifile={target_mount2}/serverinfo")
    ]
    assert len(server_info_matches3) == 1, "Expected one server info file in command"

    # after all these 'working_dir' changes, the container should still launch
    session = pyfluent.launch_fluent(container_dict=container_dict3)
    assert session.is_server_healthy()


@pytest.mark.standalone
def test_case_load():
    # Test that launch_fluent() works with a case file as an argument
    case_name = download_file(
        "mixing_elbow.cas.h5",
        "pyfluent/mixing_elbow",
    )
    session = pyfluent.launch_fluent(case_file_name=case_name)

    # Case loaded
    assert session.setup.boundary_conditions.is_active()
    # Mesh available because not lightweight
    if not session.get_fluent_version() < FluentVersion.v231:
        assert session.mesh.quality.is_active()
    # Data not loaded
    assert not session.fields.field_data.is_data_valid()

    session.exit()


@pytest.mark.standalone
@pytest.mark.fluent_version(">=23.2")
def test_case_lightweight_setup():
    # Test that launch_fluent() correctly performs lightweight setup
    case_name = download_file(
        "mixing_elbow.cas.h5",
        "pyfluent/mixing_elbow",
    )
    session = pyfluent.launch_fluent(
        case_file_name=case_name,
        lightweight_mode=True,
    )

    # Case loaded
    assert session.setup.boundary_conditions.is_active()
    # Mesh not available because lightweight
    assert not session.mesh.quality.is_active()
    # Data not loaded
    assert not session.fields.field_data.is_data_valid()


@pytest.mark.standalone
def test_case_data_load():
    # Test that launch_fluent() works with a case+data file as an argument
    case_name = download_file(
        "mixing_elbow.cas.h5",
        "pyfluent/mixing_elbow",
    )
    download_file(
        "mixing_elbow.dat.h5",
        "pyfluent/mixing_elbow",
    )
    session = pyfluent.launch_fluent(case_data_file_name=case_name)

    # Case loaded
    assert session.setup.boundary_conditions.is_active()
    # Mesh available because not lightweight
    if not session.get_fluent_version() < FluentVersion.v231:
        assert session.mesh.quality.is_active()
    # Data loaded
    assert session.fields.field_data.is_data_valid()

    session.exit()


def test_gpu_launch_arg():
    assert (
        _build_fluent_launch_args_string(
            gpu=True, additional_arguments="", processor_count=None
        ).strip()
        == "3ddp -gpu -hidden"
        if is_windows()
        else "3ddp -gpu -gu"
    )
    assert (
        _build_fluent_launch_args_string(
            gpu=[1, 2, 4], additional_arguments="", processor_count=None
        ).strip()
        == "3ddp -gpu=1,2,4 -hidden"
        if is_windows()
        else "3ddp -gpu=1,2,4 -gu"
    )


def test_gpu_launch_arg_additional_arg():
    assert (
        _build_fluent_launch_args_string(
            additional_arguments="-gpu", processor_count=None
        ).strip()
        == "3ddp -gpu -hidden"
        if is_windows()
        else "3ddp -gpu -gu"
    )
    assert (
        _build_fluent_launch_args_string(
            additional_arguments="-gpu=1,2,4", processor_count=None
        ).strip()
        == "3ddp -gpu=1,2,4 -hidden"
        if is_windows()
        else "3ddp -gpu=1,2,4 -gu"
    )


def test_get_fluent_exe_path_when_nothing_is_set(helpers):
    helpers.delete_all_awp_vars()
    with pytest.raises(FileNotFoundError):
        get_fluent_exe_path()
    with pytest.raises(FileNotFoundError):
        FluentVersion.get_latest_installed()


@pytest.mark.parametrize(
    "fluent_version",
    [version for version in FluentVersion],
)
def test_get_fluent_exe_path_from_awp_root(fluent_version, helpers, fs):
    helpers.mock_awp_vars(version=str(fluent_version.number))
    fs.create_file(fluent_version.get_fluent_exe_path())
    if platform.system() == "Windows":
        expected_path = (
            Path(f"ansys_inc/v{fluent_version.number}/fluent")
            / "ntbin"
            / "win64"
            / "fluent.exe"
        )
    else:
        expected_path = (
            Path(f"ansys_inc/v{fluent_version.number}/fluent") / "bin" / "fluent"
        )
    assert FluentVersion.get_latest_installed() == fluent_version
    assert get_fluent_exe_path() == expected_path


def test_get_fluent_exe_path_from_product_version_launcher_arg(helpers):
    helpers.mock_awp_vars()
    if platform.system() == "Windows":
        expected_path = Path("ansys_inc/v231/fluent") / "ntbin" / "win64" / "fluent.exe"
    else:
        expected_path = Path("ansys_inc/v231/fluent") / "bin" / "fluent"
    assert get_fluent_exe_path(product_version=231) == expected_path


def test_get_fluent_exe_path_from_pyfluent_fluent_root(helpers, monkeypatch):
    helpers.mock_awp_vars()
    monkeypatch.setenv("PYFLUENT_FLUENT_ROOT", "dev/vNNN/fluent")
    if platform.system() == "Windows":
        expected_path = Path("dev/vNNN/fluent") / "ntbin" / "win64" / "fluent.exe"
    else:
        expected_path = Path("dev/vNNN/fluent") / "bin" / "fluent"
    assert get_fluent_exe_path() == expected_path


def test_watchdog_launch(monkeypatch):
    monkeypatch.setattr(pyfluent.config, "watchdog_exception_on_error", True)
    pyfluent.launch_fluent(start_watchdog=True)


@pytest.mark.standalone
def test_create_standalone_launcher():
    kwargs = dict(
        ui_mode=UIMode.NO_GUI,
        graphics_driver=(
            FluentWindowsGraphicsDriver.AUTO
            if is_windows()
            else FluentLinuxGraphicsDriver.AUTO
        ),
        env={},
    )

    standalone_meshing_launcher = create_launcher(
        LaunchMode.STANDALONE, mode=FluentMode.MESHING, **kwargs
    )
    standalone_meshing_session = standalone_meshing_launcher()
    assert standalone_meshing_session
    standalone_meshing_session.exit()

    standalone_solver_launcher = create_launcher(
        LaunchMode.STANDALONE, mode=FluentMode.SOLVER, **kwargs
    )
    standalone_solver_session = standalone_solver_launcher()
    assert standalone_solver_session
    standalone_solver_session.exit()


def test_fluent_launchers():
    kwargs = dict(
        ui_mode=UIMode.NO_GUI,
        graphics_driver=(
            FluentWindowsGraphicsDriver.AUTO
            if is_windows()
            else FluentLinuxGraphicsDriver.AUTO
        ),
    )
    kargs = dict(
        ui_mode=kwargs["ui_mode"],
        graphics_driver=kwargs["graphics_driver"],
        product_version=None,
        precision=None,
        processor_count=None,
        start_timeout=None,
        additional_arguments="",
        container_dict=None,
        dry_run=None,
        cleanup_on_exit=None,
        start_transcript=None,
        py=None,
        gpu=None,
        start_watchdog=None,
        file_transfer_service=None,
    )
    container_meshing_launcher = create_launcher(
        LaunchMode.CONTAINER,
        mode=FluentMode.MESHING,
        **kargs,
    )
    container_meshing_session = container_meshing_launcher()
    assert container_meshing_session
    container_meshing_session.exit()

    container_solver_launcher = create_launcher(
        LaunchMode.CONTAINER,
        mode=FluentMode.SOLVER,
        **kargs,
    )
    container_solver_session = container_solver_launcher()
    assert container_solver_session
    container_solver_session.exit()

    if pypim.is_configured():
        pim_meshing_launcher = create_launcher(
            LaunchMode.PIM, mode=FluentMode.MESHING, **kwargs
        )
        pim_meshing_session = pim_meshing_launcher()
        assert pim_meshing_session
        pim_meshing_session.exit()

        pim_solver_launcher = create_launcher(
            LaunchMode.PIM, mode=FluentMode.SOLVER, **kwargs
        )
        pim_solver_session = pim_solver_launcher()
        assert pim_solver_session
        pim_solver_session.exit()


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
        (None, 5, None, pytest.raises(TypeError)),
        (True, None, None, pytest.raises(InvalidArgument)),
    ],
)
def test_build_journal_argument(topy, journal_file_names, result, raises):
    with raises:
        assert _build_journal_argument(topy, journal_file_names) == result


def test_show_gui_raises_warning():
    with pytest.warns(PyFluentDeprecationWarning):
        solver = pyfluent.launch_fluent(show_gui=True)
        solver.exit()


def test_fluent_enums():
    assert UIMode.GUI.value == "gui"
    assert UIMode("gui") == UIMode.GUI
    with pytest.raises(ValueError):
        UIMode("")
    with pytest.raises(TypeError):
        assert UIMode.NO_GUI < FluentWindowsGraphicsDriver.AUTO


def test_exposure_and_graphics_driver_arguments():
    with pytest.raises(ValueError):
        pyfluent.launch_fluent(ui_mode="gu")
    with pytest.raises(ValueError):
        pyfluent.launch_fluent(graphics_driver="x11" if is_windows() else "dx11")
    for m in UIMode:
        string1 = _build_fluent_launch_args_string(
            ui_mode=m, additional_arguments="", processor_count=None
        ).strip()
        string2 = (
            f"3ddp -{m.get_fluent_value()[0]}" if m.get_fluent_value()[0] else "3ddp"
        )
        assert string1 == string2
    for e in (FluentWindowsGraphicsDriver, FluentLinuxGraphicsDriver):
        for m in e:
            msg = _build_fluent_launch_args_string(
                graphics_driver=m, additional_arguments="", processor_count=None
            ).strip()
            if is_windows():
                assert (
                    msg == f"3ddp -hidden -driver {m.get_fluent_value()[0]}"
                    if m.get_fluent_value()[0]
                    else " 3ddp -hidden"
                )
            else:
                assert (
                    msg == f"3ddp -gu -driver {m.get_fluent_value()[0]}"
                    if m.get_fluent_value()[0]
                    else " 3ddp -gu"
                )


def test_additional_arguments_fluent_launch_args_string():
    additional_arguments = "-ws -ws-port=5000 -i test.jou"
    assert additional_arguments in _build_fluent_launch_args_string(
        additional_arguments=additional_arguments,
        processor_count=4,
    )


def test_processor_count():
    def get_processor_count(solver):
        return int(solver.rp_vars("parallel/nprocs_string").strip('"'))

    with pyfluent.launch_fluent(processor_count=2) as solver:
        assert get_processor_count(solver) == 2
    # The following check is not yet supported for container launch
    # https://github.com/ansys/pyfluent/issues/2624
    # with pyfluent.launch_fluent(additional_arguments="-t2") as solver:
    #     assert get_processor_count(solver) == 2


def test_container_mount_source_target(caplog):
    container_dict = {
        "mount_source": os.getcwd(),
        "mount_target": "/mnt/pyfluent/tests",
    }
    session = pyfluent.launch_fluent(container_dict=container_dict)
    assert session.is_server_healthy()
    assert container_dict["mount_source"] in caplog.text
    assert container_dict["mount_target"] in caplog.text


def test_fluent_automatic_transcript(monkeypatch):
    with TemporaryDirectory(dir=pyfluent.config.examples_path) as tmp_dir:
        with pyfluent.launch_fluent(container_dict=dict(mount_source=tmp_dir)):
            assert list(Path(tmp_dir).glob("*.trn"))
    with monkeypatch.context() as m:
        m.setattr(pyfluent.config, "fluent_automatic_transcript", False)
        with TemporaryDirectory(dir=pyfluent.config.examples_path) as tmp_dir:
            with pyfluent.launch_fluent(container_dict=dict(mount_source=tmp_dir)):
                assert not list(Path(tmp_dir).glob("*.trn"))


def test_standalone_launcher_dry_run(monkeypatch):
    monkeypatch.setattr(pyfluent.config, "launch_fluent_container", False)
    fluent_path = r"\x\y\z\fluent.exe"
    fluent_launch_string, server_info_file_name = pyfluent.launch_fluent(
        fluent_path=fluent_path, dry_run=True, ui_mode="no_gui"
    )
    assert str(Path(server_info_file_name).parent) == tempfile.gettempdir()
    assert (
        fluent_launch_string
        == f"{fluent_path} 3ddp -gu -driver null -sifile={server_info_file_name} -nm"
    )


def test_standalone_launcher_dry_run_with_server_info_dir(monkeypatch):
    monkeypatch.setattr(pyfluent.config, "launch_fluent_container", False)
    with tempfile.TemporaryDirectory() as tmp_dir:
        monkeypatch.setattr(pyfluent.config, "fluent_server_info_dir", tmp_dir)
        fluent_path = r"\x\y\z\fluent.exe"
        fluent_launch_string, server_info_file_name = pyfluent.launch_fluent(
            fluent_path=fluent_path, dry_run=True, ui_mode="no_gui"
        )
        assert str(Path(server_info_file_name).parent) == tmp_dir
        assert (
            fluent_launch_string
            == f"{fluent_path} 3ddp -gu -driver null -sifile={Path(server_info_file_name).name} -nm"
        )


def test_container_ports():
    container_dict = {"ports": {"5000": 5000, "5001": 5001}}
    with pyfluent.launch_fluent(container_dict=container_dict) as session:
        session._container.reload()
        assert len(session._container.ports) == 2


def test_correct_ip_port():
    with pytest.raises(InvalidIpPort):
        pyfluent.connect_to_fluent(ip="1.2.3.4", port=5555)


def test_container_launcher_args():
    container_dict = pyfluent.launch_fluent(start_container=True, dry_run=True)
    commands = container_dict["command"]
    graphics_args = ["-gu", "-hidden", "-g", "-gr"]
    graphics_arg_count = 0
    for arg in graphics_args:
        graphics_arg_count += commands.count(arg)
    assert graphics_arg_count == 1, "Too many graphics arguments"


def test_report():
    from ansys.fluent.core.report import ANSYS_ENV_VARS, dependencies
    from ansys.tools.report import Report

    rep = Report(ansys_libs=dependencies, ansys_vars=ANSYS_ENV_VARS)
    assert "PyAnsys Software and Environment Report" in str(rep)
    assert str(rep).count("pandas") == 1


@pytest.mark.fluent_version(">=23.1")
def test_docker_compose(monkeypatch):
    import ansys.fluent.core as pyfluent
    from ansys.fluent.core import examples
    from ansys.fluent.core.utils.networking import get_free_port

    port_1 = get_free_port()
    port_2 = get_free_port()
    container_dict = {"ports": {f"{port_1}": port_1, f"{port_2}": port_2}}
    solver = pyfluent.launch_fluent(
        container_dict=container_dict, use_docker_compose=True
    )
    assert len(solver._container.ports) == 2
    case_file_name = examples.download_file(
        "mixing_elbow.cas.h5", "pyfluent/mixing_elbow"
    )
    solver.file.read_case(file_name=case_file_name)
    solver.exit()


@pytest.mark.standalone
def test_respect_driver_is_not_null_in_windows():
    driver = _get_graphics_driver(
        graphics_driver=FluentWindowsGraphicsDriver.DX11, ui_mode=UIMode.GUI
    )
    assert driver == FluentWindowsGraphicsDriver.DX11

    driver = _get_graphics_driver(
        graphics_driver=FluentWindowsGraphicsDriver.OPENGL, ui_mode=UIMode.HIDDEN_GUI
    )
    assert driver == FluentWindowsGraphicsDriver.OPENGL


def test_respect_driver_is_not_null_in_linux():
    driver = _get_graphics_driver(
        graphics_driver=FluentLinuxGraphicsDriver.X11, ui_mode=UIMode.GUI
    )
    assert driver == FluentLinuxGraphicsDriver.X11

    driver = _get_graphics_driver(
        graphics_driver=FluentLinuxGraphicsDriver.OPENGL, ui_mode=UIMode.HIDDEN_GUI
    )
    assert driver == FluentLinuxGraphicsDriver.OPENGL


@pytest.mark.standalone
def test_warning_in_windows():
    with pytest.warns(PyFluentUserWarning):
        driver = _get_graphics_driver(
            graphics_driver=FluentWindowsGraphicsDriver.DX11, ui_mode=UIMode.NO_GUI
        )
        assert driver == FluentWindowsGraphicsDriver.NULL

    with pytest.warns(PyFluentUserWarning):
        driver = _get_graphics_driver(
            graphics_driver=FluentWindowsGraphicsDriver.AUTO, ui_mode=UIMode.NO_GRAPHICS
        )
        assert driver == FluentWindowsGraphicsDriver.NULL

    with pytest.warns(PyFluentUserWarning):
        driver = _get_graphics_driver(
            graphics_driver=FluentWindowsGraphicsDriver.AUTO,
            ui_mode=UIMode.NO_GUI_OR_GRAPHICS,
        )
        assert driver == FluentWindowsGraphicsDriver.NULL


def test_warning_in_linux():
    with pytest.warns(PyFluentUserWarning):
        driver = _get_graphics_driver(
            graphics_driver=FluentLinuxGraphicsDriver.X11, ui_mode=UIMode.NO_GUI
        )
        assert driver == FluentLinuxGraphicsDriver.NULL

    with pytest.warns(PyFluentUserWarning):
        driver = _get_graphics_driver(
            graphics_driver=FluentLinuxGraphicsDriver.AUTO, ui_mode=UIMode.NO_GRAPHICS
        )
        assert driver == FluentLinuxGraphicsDriver.NULL

    with pytest.warns(PyFluentUserWarning):
        driver = _get_graphics_driver(
            graphics_driver=FluentLinuxGraphicsDriver.AUTO,
            ui_mode=UIMode.NO_GUI_OR_GRAPHICS,
        )
        assert driver == FluentLinuxGraphicsDriver.NULL


def test_no_warning_for_none_values(caplog):
    driver = _get_graphics_driver(graphics_driver=None, ui_mode=None)  # noqa: F841
    assert "PyFluentUserWarning" not in caplog.text
    caplog.clear()


def test_error_for_selecting_both_compose_sources():
    with pytest.raises(ValueError):
        pyfluent.launch_fluent(use_docker_compose=True, use_podman_compose=True)


def test_warning_for_deprecated_compose_env_vars(monkeypatch):
    monkeypatch.setattr(pyfluent.config, "use_docker_compose", True)
    with pytest.warns(PyFluentDeprecationWarning):
        ComposeConfig()

    monkeypatch.setattr(pyfluent.config, "use_podman_compose", True)
    with pytest.warns(PyFluentDeprecationWarning):
        ComposeConfig()
