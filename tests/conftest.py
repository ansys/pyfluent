from collections import defaultdict
from contextlib import nullcontext
import functools
import operator
import os

from packaging.specifiers import SpecifierSet
from packaging.version import Version
import pytest

from ansys.fluent.core.data_model_cache import DataModelCache
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


@pytest.fixture(autouse=True)
def clear_datamodel_cache():
    yield
    DataModelCache.rules_str_to_cache.clear()


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


fixtures = [
    "sample_solver_session",
    "launch_fluent_pure_meshing",
    "launch_fluent_solver_3ddp_t2",
    "launch_fluent_solver_2ddp",
    "launch_fluent_solver_2ddp_t2",
    "exhaust_system_geometry",
    "load_mixing_elbow_mesh",
    "load_mixing_elbow_case_dat",
    "load_mixing_elbow_settings_only",
    "load_static_mixer_case",
    "load_static_mixer_settings_only",
    "load_mixing_elbow_param_case_dat",
    "load_mixing_elbow_pure_meshing",
    "load_mixing_elbow_meshing",
    "load_periodic_rot_cas",
    "load_periodic_rot_settings_only",
    "load_disk_mesh",
    "load_disk_settings_only",
    "new_mesh_session",
    "new_watertight_workflow_session",
    "new_watertight_workflow",
    "shared_mesh_session",
    "shared_watertight_workflow_session",
    "shared_watertight_workflow",
    "mixing_elbow_geometry",
    "new_fault_tolerant_workflow_session",
    "new_fault_tolerant_workflow",
    "shared_fault_tolerant_workflow_session",
    "shared_fault_tolerant_workflow",
    "exhaust_system_geometry",
    "new_solver_session",
    "make_new_session",
    "new_solver_session_single_precision",
    "new_solver_session_no_transcript",
]
tests_by_fixture = defaultdict(list)


def pytest_collection_finish(session):
    for k, v in sorted(tests_by_fixture.items(), key=lambda t: len(t[1]), reverse=True):
        print(k, len(v))


def pytest_itemcollected(item):
    if not item.nodeid.startswith("tests/test_solvermode/"):
        for fixture in item.fixturenames:
            if fixture in fixtures:
                tests_by_fixture[fixture].append(item.nodeid)
