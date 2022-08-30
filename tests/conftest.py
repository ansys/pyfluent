import os
import shutil

import pytest

import ansys.fluent.core as pyfluent

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


@pytest.fixture(autouse=True)
def clean_examples():
    if os.path.exists(pyfluent.EXAMPLES_PATH):
        shutil.rmtree(pyfluent.EXAMPLES_PATH)
    os.mkdir(pyfluent.EXAMPLES_PATH)
