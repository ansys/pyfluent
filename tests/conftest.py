from collections import defaultdict
from contextlib import nullcontext
import functools
import operator
import os

from packaging.specifiers import SpecifierSet
from packaging.version import Version
import pytest

import ansys.fluent.core as pyfluent
from ansys.fluent.core.examples.downloads import download_file
from ansys.fluent.core.utils.file_transfer_service import RemoteFileTransferStrategy
from ansys.fluent.core.utils.fluent_version import FluentVersion

_fluent_release_version = FluentVersion.current_release().value


def pytest_addoption(parser):
    parser.addoption(
        "--fluent-version",
        action="store",
        metavar="VERSION",
        help="only run tests supported by Fluent version VERSION.",
    )
    parser.addoption(
        "--nightly", action="store_true", default=False, help="run nightly tests"
    )
    parser.addoption(
        "--solvermode", action="store_true", default=False, help="run solvermode tests"
    )


def pytest_runtest_setup(item):
    if (
        any(mark.name == "standalone" for mark in item.iter_markers())
        and os.getenv("PYFLUENT_LAUNCH_CONTAINER") == "1"
    ):
        pytest.skip()

    is_nightly = item.config.getoption("--nightly")
    if not is_nightly and any(mark.name == "nightly" for mark in item.iter_markers()):
        pytest.skip()

    is_solvermode_option = item.config.getoption("--solvermode")
    is_solvermode_path = "test_solvermode" in item.path.parts
    if is_solvermode_option ^ is_solvermode_path:
        pytest.skip()

    version_specs = []
    for mark in item.iter_markers(name="fluent_version"):
        spec = mark.args[0]
        # if a test is marked as fluent_version("latest")
        # run with dev and release Fluent versions in nightly
        # run with release Fluent versions in PRs
        if spec == "latest":
            spec = (
                f">={_fluent_release_version}"
                if is_nightly or is_solvermode_option
                else f"=={_fluent_release_version}"
            )
        version_specs.append(SpecifierSet(spec))
    if version_specs:
        combined_spec = functools.reduce(operator.and_, version_specs)
        version = item.config.getoption("--fluent-version")
        if version and Version(version) not in combined_spec:
            pytest.skip()


pytest_plugins = [
    "util.fixture_fluent",
    "util.meshing_workflow",
]


@pytest.fixture(autouse=True)
def run_before_each_test(
    monkeypatch: pytest.MonkeyPatch, request: pytest.FixtureRequest
) -> None:
    monkeypatch.setenv("PYFLUENT_TEST_NAME", request.node.name)
    pyfluent.CONTAINER_MOUNT_PATH = pyfluent.EXAMPLES_PATH


class Helpers:
    """Can be reused to provide helper methods to tests."""

    def __init__(self, monkeypatch: pytest.MonkeyPatch):
        self.monkeypatch = monkeypatch

    def mock_awp_vars(self, version=None):
        """Activates env vars for Fluent versions up to specified version, deactivates
        env vars for versions newer than specified."""
        if not version:
            version = FluentVersion.current_release()
        elif not isinstance(version, FluentVersion):
            version = FluentVersion(version)
        self.monkeypatch.delenv("PYFLUENT_FLUENT_ROOT", raising=False)
        for fv in FluentVersion:
            if fv <= version:
                self.monkeypatch.setenv(fv.awp_var, f"ansys_inc/{fv.name}")
            else:
                self.monkeypatch.delenv(fv.awp_var, raising=False)

    def delete_all_awp_vars(self):
        for fv in FluentVersion:
            self.monkeypatch.delenv(fv.awp_var, raising=False)


@pytest.fixture
def helpers(monkeypatch):
    return Helpers(monkeypatch)


pytest.wont_raise = nullcontext


def pytest_sessionfinish(session, exitstatus):
    if exitstatus == 5:
        session.exitstatus = 0


tests_by_fixture = defaultdict(list)


def pytest_collection_finish(session):
    for k, v in sorted(tests_by_fixture.items(), key=lambda t: len(t[1]), reverse=True):
        print(k, len(v))


def pytest_itemcollected(item):
    if not item.nodeid.startswith("tests/test_solvermode/"):
        for fixture in item.fixturenames:
            tests_by_fixture[fixture].append(item.nodeid)


def create_mesh_session():
    if pyfluent.USE_FILE_TRANSFER_SERVICE:
        container_dict = {"host_mount_path": pyfluent.USER_DATA_PATH}
        file_transfer_service = RemoteFileTransferStrategy()
        return pyfluent.launch_fluent(
            mode=pyfluent.FluentMode.MESHING,
            container_dict=container_dict,
            file_transfer_service=file_transfer_service,
        )
    else:
        return pyfluent.launch_fluent(mode=pyfluent.FluentMode.MESHING)


@pytest.fixture
def new_meshing_session():
    mesher = create_mesh_session()
    return mesher


def create_solver_session():
    if pyfluent.USE_FILE_TRANSFER_SERVICE:
        container_dict = {"host_mount_path": pyfluent.USER_DATA_PATH}
        file_transfer_service = RemoteFileTransferStrategy()
        return pyfluent.launch_fluent(
            container_dict=container_dict,
            file_transfer_service=file_transfer_service,
        )
    else:
        return pyfluent.launch_fluent()


@pytest.fixture
def new_solver_session():
    solver = create_solver_session()
    return solver


@pytest.fixture
def static_mixer_settings_only(new_solver_session):
    solver = new_solver_session
    case_path = download_file("Static_Mixer_main.cas.h5", "pyfluent/static_mixer")
    solver.file.read(
        file_type="case",
        file_name=case_path,
        lightweight_setup=True,
    )
    return solver
