from contextlib import nullcontext
import os

from packaging.specifiers import SpecifierSet
from packaging.version import Version
import pytest

from ansys.fluent.core.data_model_cache import DataModelCache
from ansys.fluent.core.utils.fluent_version import FluentVersion

_fluent_release_version = FluentVersion.current_release().value
_fluent_develop_version = next(iter(FluentVersion)).value


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

    fluent_version_spec = None
    fluent_version_markers = list(item.iter_markers(name="fluent_version"))
    if fluent_version_markers:
        spec = fluent_version_markers[0].args[0]
        # Tests which depend on the current development Fluent version or tracking
        # Fluent API change are marked as fluent_version("latest"). They are run only
        # with the development Fluent version.
        if spec == "latest":
            fluent_version_spec = f"=={_fluent_develop_version}"
        # Tests which depend on a specific released Fluent version are marked as
        # fluent_version("==<version>"). They are run only with that specific Fluent
        # version.
        else:
            fluent_version_spec = spec
    else:
        # Tests which do not require to run Fluent at all or can be run with any stable
        # Fluent version are not marked. They are run only with the latest released
        # Fluent version during PRs and with the latest released and the current
        # development Fluent versions during nightly.
        fluent_version_spec = (
            f">={_fluent_release_version}"
            if is_nightly
            else f"=={_fluent_release_version}"
        )
    fluent_version = item.config.getoption("--fluent-version")
    if fluent_version and Version(fluent_version) not in SpecifierSet(
        fluent_version_spec
    ):
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
