import functools
import operator

from packaging.specifiers import SpecifierSet
from packaging.version import Version
import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--fluent-version",
        action="store",
        metavar="VERSION",
        help="only run tests supported by Fluent version VERSION.",
    )


def pytest_runtest_setup(item):
    version_specs = [
        SpecifierSet(mark.args[0]) for mark in item.iter_markers(name="fluent_version")
    ]
    if version_specs:
        combined_spec = functools.reduce(operator.and_, version_specs)
        version = item.config.getoption("--fluent-version")
        if version:
            if Version(version) not in combined_spec:
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
