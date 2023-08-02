import pytest
from util.fixture_fluent import load_static_mixer_case  # noqa: F401


@pytest.mark.fluent_version("latest")
def test_creatable(load_static_mixer_case) -> None:
    has_not = (
        load_static_mixer_case.setup.boundary_conditions.velocity_inlet,
        load_static_mixer_case.setup.cell_zone_conditions.fluid,
    )

    has = (
        load_static_mixer_case.results.graphics.contour,
        load_static_mixer_case.results.graphics.vector,
    )

    for obj in has_not:
        assert not hasattr(obj, "create")
        assert "create" not in dir(obj)

    for obj in has:
        assert hasattr(obj, "create")
        assert "create" in dir(obj)
