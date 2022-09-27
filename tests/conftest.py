import pytest

pytest_plugins = [
    "util.fixture_fluent",
    "util.meshing_workflow",
]


def pytest_collection_modifyitems(items, config):
    for item in items:
        if not any(item.iter_markers()):
            item.add_marker("dev")


@pytest.fixture
def with_launching_container(
    monkeypatch: pytest.MonkeyPatch, request: pytest.FixtureRequest
) -> None:
    monkeypatch.setenv("PYFLUENT_LAUNCH_CONTAINER", "1")
    monkeypatch.setenv("PYFLUENT_TEST_NAME", request.node.name)
