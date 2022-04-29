import pytest

import ansys.fluent.core as pyfluent


@pytest.fixture
def with_running_pytest(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(pyfluent, "RUNNING_PYTEST", True)
