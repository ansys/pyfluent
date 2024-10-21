import pytest

from ansys.fluent.core.utils.fluent_version import FluentVersion


@pytest.mark.fluent_version("latest")
def test_creatable(mixing_elbow_case_data_session) -> None:
    solver = mixing_elbow_case_data_session
    fluent_version = solver.get_fluent_version()
    has_not = (
        solver.setup.boundary_conditions.velocity_inlet,
        solver.setup.cell_zone_conditions.fluid,
    )
    has = (
        solver.results.graphics.contour,
        solver.results.graphics.vector,
    )

    for obj in has_not:
        # creatability condition is dynamic since 25.1
        if fluent_version >= FluentVersion.v251:
            assert not getattr(obj, "create").is_active()
        else:
            assert not hasattr(obj, "create")
            assert "create" not in dir(obj)

    for obj in has:
        assert hasattr(obj, "create")
        assert "create" in dir(obj)
        if fluent_version >= FluentVersion.v251:
            assert getattr(obj, "create").is_active()
