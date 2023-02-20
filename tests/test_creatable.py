import pytest
from util.solver_workflow import new_solver_session  # noqa: F401


@pytest.mark.fluent_231
def test_creatable(new_solver_session) -> None:
    has_not = (
        new_solver_session.setup.boundary_conditions.velocity_inlet,
        new_solver_session.setup.cell_zone_conditions.fluid,
    )

    has = (
        new_solver_session.results.graphics.contour,
        new_solver_session.results.graphics.vector,
    )

    for obj in has_not:
        assert not hasattr(obj, "create")
        assert "create" not in dir(obj)

    for obj in has:
        assert hasattr(obj, "create")
        assert "create" in dir(obj)
