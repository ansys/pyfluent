import pytest

pytest_plugins = [
    "util.fixture_fluent",
]


def pytest_collection_modifyitems(items, config):
    for item in items:
        if not any(item.iter_markers()):
            item.add_marker("unmarked")


@pytest.fixture
def with_launching_container(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PYFLUENT_LAUNCH_CONTAINER", "1")
