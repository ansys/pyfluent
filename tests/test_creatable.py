import pytest


@pytest.mark.skip
def test_creatable(static_mixer_settings_session) -> None:
    setup = static_mixer_settings_session.setup
    has_not = (
        setup.boundary_conditions.velocity_inlet,
        setup.cell_zone_conditions.fluid,
    )
    results = static_mixer_settings_session.results
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
