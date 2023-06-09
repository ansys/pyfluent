import pytest

pytest_plugins = [
    "util.fixture_fluent",
    "util.meshing_workflow",
]


def pytest_collection_modifyitems(items, config):
    version_markers = ["fluent_222", "fluent_231", "fluent_232", "fluent_241"]
    for item in items:
        markers = [x.name for x in item.iter_markers()]
        # If no markers are defined add "dev" marker
        if not any(markers):
            item.add_marker("dev")
        # If no version markers are defined, run it for all versions
        if not any(x for x in version_markers if x in markers):
            for m in version_markers:
                item.add_marker(m)


@pytest.fixture
def with_launching_container(
    monkeypatch: pytest.MonkeyPatch, request: pytest.FixtureRequest
) -> None:
    monkeypatch.setenv("PYFLUENT_LAUNCH_CONTAINER", "1")
    monkeypatch.setenv("PYFLUENT_TIMEOUT_FORCE_EXIT", "5")
    monkeypatch.setenv("PYFLUENT_TEST_NAME", request.node.name)
