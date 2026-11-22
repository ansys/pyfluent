import pytest

from fvm import (
    BoundaryConditions,
    FixedValue,
    MovingWall,
    NoSlipWall,
    ZeroGradient,
)


def test_cavity_conditions_can_be_stored_by_field_and_boundary() -> None:
    conditions = BoundaryConditions()
    conditions.set("velocity", "north", MovingWall((1.0, 0.0)))
    conditions.set("velocity", "south", NoSlipWall())
    conditions.set("pressure", "north", ZeroGradient())
    conditions.set("pressure", "west", FixedValue(0.0))

    assert conditions.get("velocity", "north") == MovingWall((1.0, 0.0))
    assert conditions.get("velocity", "south") == NoSlipWall()
    assert conditions.get("pressure", "north") == ZeroGradient()
    assert len(conditions) == 4
    assert set(conditions.for_field("pressure")) == {"north", "west"}


def test_complete_cavity_boundary_assignment() -> None:
    conditions = BoundaryConditions()
    conditions.set("velocity", "north", MovingWall((1.0, 0.0)))
    for side in ("west", "east", "south"):
        conditions.set("velocity", side, NoSlipWall())
    for side in ("west", "east", "south", "north"):
        conditions.set("pressure", side, ZeroGradient())

    assert set(conditions.for_field("velocity")) == {"west", "east", "south", "north"}
    assert set(conditions.for_field("pressure")) == {"west", "east", "south", "north"}
    assert conditions.get("velocity", "north") == MovingWall((1.0, 0.0))


def test_boundary_conditions_can_replace_a_condition() -> None:
    conditions = BoundaryConditions()
    conditions.set("pressure", "east", ZeroGradient())
    conditions.set("pressure", "east", FixedValue(2.0))

    assert len(conditions) == 1
    assert conditions.get("pressure", "east") == FixedValue(2.0)


def test_boundary_conditions_validate_names_and_types() -> None:
    conditions = BoundaryConditions()

    with pytest.raises(ValueError, match="boundary"):
        conditions.set("pressure", "middle", ZeroGradient())
    with pytest.raises(ValueError, match="field_name"):
        conditions.set("", "north", ZeroGradient())
    with pytest.raises(TypeError, match="unsupported"):
        conditions.set("pressure", "north", object())  # type: ignore[arg-type]
    with pytest.raises(KeyError):
        conditions.get("pressure", "north")


def test_velocity_conditions_require_two_finite_components() -> None:
    with pytest.raises(ValueError, match="two components"):
        MovingWall((1.0,))  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="finite"):
        NoSlipWall((0.0, float("nan")))


def test_field_conditions_are_read_only() -> None:
    conditions = BoundaryConditions()
    conditions.set("pressure", "north", ZeroGradient())

    field_conditions = conditions.for_field("pressure")
    with pytest.raises(TypeError):
        field_conditions["south"] = ZeroGradient()  # type: ignore[index]