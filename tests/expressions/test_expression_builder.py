# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""Unit tests for the expression builder AST + registry.

These tests are pure-Python and do not require a live Fluent session.
"""

import pytest
from ansys.units import VariableCatalog as V

from ansys.fluent.core.expressions import ExpressionBuilder, ExpressionBuildError


@pytest.fixture
def b():
    return ExpressionBuilder()  # settings=None


# --------------------------------------------------------------------------- #
# Leaves                                                                      #
# --------------------------------------------------------------------------- #


def test_literal_renders(b):
    assert str(b.literal(1.5)) == "1.5"


def test_quantity_renders(b):
    assert str(b.quantity(5, "m/s")) == "5 [m/s]"


def test_variable_maps_via_naming_strategy(b):
    v = b.variable(V.ABSOLUTE_PRESSURE)
    assert str(v) == "AbsolutePressure"


def test_variable_unmapped_raises():
    from ansys.fluent.core.expressions._ast import Variable
    # Fabricate a descriptor unknown to FluentExprNamingStrategy.
    class _Fake:
        pass
    with pytest.raises(ExpressionBuildError):
        Variable(_Fake())  # type: ignore[arg-type]


def test_locations_render(b):
    locs = b.locations(["inlet1", "inlet2"])
    assert str(locs) == "['inlet1', 'inlet2']"


def test_locations_reject_bare_string(b):
    with pytest.raises(ExpressionBuildError):
        b.locations("inlet1")


# --------------------------------------------------------------------------- #
# Reductions                                                                  #
# --------------------------------------------------------------------------- #


def test_area_ave_renders_like_fluent(b):
    node = b.reductions.area_ave(
        expression=V.ABSOLUTE_PRESSURE, locations=["inlet1"]
    )
    assert str(node) == "AreaAve(AbsolutePressure,['inlet1'])"


def test_area_ave_positional(b):
    node = b.reductions.area_ave(V.ABSOLUTE_PRESSURE, ["inlet1", "inlet2"])
    assert str(node) == "AreaAve(AbsolutePressure,['inlet1', 'inlet2'])"


def test_count_no_expression(b):
    node = b.reductions.count(locations=["inlet1"])
    assert str(node) == "Count(['inlet1'])"


def test_missing_required_arg(b):
    with pytest.raises(ExpressionBuildError, match="missing required argument"):
        b.reductions.area_ave(expression=V.ABSOLUTE_PRESSURE)


def test_unknown_reduction(b):
    with pytest.raises(AttributeError):
        b.reductions.not_a_thing


def test_wrong_kind_for_location(b):
    with pytest.raises(ExpressionBuildError):
        # a scalar where a location list belongs
        b.reductions.area_ave(expression=V.ABSOLUTE_PRESSURE, locations=V.TEMPERATURE)


# --------------------------------------------------------------------------- #
# Operators / composition                                                     #
# --------------------------------------------------------------------------- #


def test_subtract_two_reductions(b):
    inlet = b.reductions.area_ave(
        expression=V.ABSOLUTE_PRESSURE, locations=["inlet1"]
    )
    outlet = b.reductions.area_ave(
        expression=V.ABSOLUTE_PRESSURE, locations=["outlet"]
    )
    dp = inlet - outlet
    assert str(dp) == (
        "(AreaAve(AbsolutePressure,['inlet1']) - "
        "AreaAve(AbsolutePressure,['outlet']))"
    )


def test_scalar_arithmetic_with_python_numbers(b):
    v = b.variable(V.VELOCITY_MAGNITUDE)
    node = 2 * v + 1
    assert str(node) == "((2 * VelocityMagnitude) + 1)"


def test_comparison_produces_boolean(b):
    from ansys.fluent.core.expressions import BooleanExpr
    v = b.variable(V.VELOCITY_MAGNITUDE)
    cond = v > 10
    assert isinstance(cond, BooleanExpr)
    assert str(cond) == "(VelocityMagnitude > 10)"


def test_equality_uses_compare_node_and_nodes_are_hashable(b):
    left = b.variable(V.VELOCITY_MAGNITUDE)
    right = b.variable(V.ABSOLUTE_PRESSURE)
    cond = left == right
    assert str(cond) == "(VelocityMagnitude == AbsolutePressure)"
    assert left in {left}


def test_negation(b):
    v = b.variable(V.VELOCITY_MAGNITUDE)
    assert str(-v) == "(-VelocityMagnitude)"


# --------------------------------------------------------------------------- #
# Introspection                                                               #
# --------------------------------------------------------------------------- #


def test_reductions_available(b):
    names = b.reductions.available()
    assert "area_ave" in names
    assert "count" in names


def test_signature_params(b):
    inv = b.reductions.area_ave
    assert inv.params() == ["expression", "locations"]
