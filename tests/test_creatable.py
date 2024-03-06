import pytest
from util.fixture_fluent import (  # noqa: F401
    load_static_mixer_settings_only_scoped_session,
)


@pytest.mark.fluent_version("latest")
def test_creatable(load_static_mixer_settings_only_scoped_session) -> None:
    setup = load_static_mixer_settings_only_scoped_session.setup
    has_not = (
        setup.boundary_conditions.velocity_inlet,
        setup.cell_zone_conditions.fluid,
    )
    results = load_static_mixer_settings_only_scoped_session.results
    has = (
        results.graphics.contour,
        results.graphics.vector,
    )

    for obj in has_not:
        assert not hasattr(obj, "create")
        assert "create" not in dir(obj)

    for obj in has:
        assert hasattr(obj, "create")
        assert "create" in dir(obj)
