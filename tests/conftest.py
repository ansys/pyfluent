import pytest


@pytest.fixture
def with_launching_container(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PYFLUENT_LAUNCH_CONTAINER", "1")
