import pytest
from util.fixture_fluent import (  # load_static_mixer_case_2; noqa: F401
    load_static_mixer_case,
)

load_static_mixer_case_2 = load_static_mixer_case


def _test_minimum():
    pass


@pytest.mark.fluent_231
def test_reductions(load_static_mixer_case, load_static_mixer_case_2) -> None:
    solver = load_static_mixer_case
    solver2 = load_static_mixer_case_2
