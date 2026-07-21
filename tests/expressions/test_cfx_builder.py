# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""Tests for the CFX (CEL) expression builder.

The CFX builder shares the generic AST / registry machinery with the
Fluent builder but emits CEL-shaped strings: reductions use a
``@location`` postfix instead of Fluent's list-argument form, and
variable / function names follow CFX conventions.
"""

import pytest

from ansys.fluent.core.expressions import CfxExpressionBuilder, ExpressionBuildError
from ansys.fluent.core.expressions.cfx_builder import CfxCall, CfxSignature
from ansys.units import VariableCatalog as V

# --------------------------------------------------------------------------- #
# Reductions                                                                  #
# --------------------------------------------------------------------------- #


def test_area_ave_renders_with_location_postfix():
    b = CfxExpressionBuilder()
    expr = b.reductions.area_ave(expression=V.ABSOLUTE_PRESSURE, location="inlet1")
    assert isinstance(expr, CfxCall)
    assert str(expr) == "areaAve(Absolute Pressure)@inlet1"


def test_reduction_requires_location():
    b = CfxExpressionBuilder()
    with pytest.raises(ExpressionBuildError):
        b.reductions.area_ave(expression=V.ABSOLUTE_PRESSURE)


def test_reduction_location_must_be_string():
    b = CfxExpressionBuilder()
    with pytest.raises(ExpressionBuildError):
        b.reductions.area_ave(expression=V.ABSOLUTE_PRESSURE, location=["inlet1"])


def test_extent_reduction_no_expression():
    b = CfxExpressionBuilder()
    expr = b.reductions.area(location="outlet")
    assert str(expr) == "area()@outlet"


def test_extent_reduction_rejects_expression():
    b = CfxExpressionBuilder()
    with pytest.raises(ExpressionBuildError):
        b.reductions.area(V.ABSOLUTE_PRESSURE, location="outlet")


def test_mass_flow_ave_positional_expression():
    b = CfxExpressionBuilder()
    expr = b.reductions.mass_flow_ave(V.TEMPERATURE, location="inlet1")
    assert str(expr) == "massFlowAve(Temperature)@inlet1"


# --------------------------------------------------------------------------- #
# Math                                                                        #
# --------------------------------------------------------------------------- #


def test_math_without_location():
    b = CfxExpressionBuilder()
    expr = b.math.sqrt(b.literal(2))
    assert str(expr) == "sqrt(2)"


def test_math_rejects_location():
    b = CfxExpressionBuilder()
    with pytest.raises(ExpressionBuildError):
        b.math.sqrt(b.literal(2), location="inlet1")


def test_binary_math():
    b = CfxExpressionBuilder()
    expr = b.math.pow(b.literal(2), b.literal(3))
    assert str(expr) == "pow(2, 3)"


# --------------------------------------------------------------------------- #
# Composition via operator overloading (reuses generic AST)                   #
# --------------------------------------------------------------------------- #


def test_arithmetic_composition():
    b = CfxExpressionBuilder()
    dp = b.reductions.area_ave(
        expression=V.ABSOLUTE_PRESSURE, location="inlet1"
    ) - b.reductions.area_ave(expression=V.ABSOLUTE_PRESSURE, location="outlet")
    assert str(dp) == (
        "(areaAve(Absolute Pressure)@inlet1" " - areaAve(Absolute Pressure)@outlet)"
    )


def test_call_composes_with_literal_and_quantity():
    b = CfxExpressionBuilder()
    expr = b.reductions.area_ave(
        expression=V.TEMPERATURE, location="inlet"
    ) + b.quantity(1, "K")
    assert str(expr) == "(areaAve(Temperature)@inlet + 1 [K])"


def test_comparison_produces_boolean_expr():
    from ansys.fluent.core.expressions import BooleanExpr

    b = CfxExpressionBuilder()
    cmp = b.reductions.area_ave(
        expression=V.ABSOLUTE_PRESSURE, location="inlet"
    ) > b.literal(0)
    assert isinstance(cmp, BooleanExpr)
    assert str(cmp) == "(areaAve(Absolute Pressure)@inlet > 0)"


# --------------------------------------------------------------------------- #
# Leaves                                                                      #
# --------------------------------------------------------------------------- #


def test_literal_and_quantity():
    b = CfxExpressionBuilder()
    assert str(b.literal(3.14)) == "3.14"
    assert str(b.quantity(5, "m s^-1")) == "5 [m s^-1]"


def test_variable_uses_cfx_naming():
    b = CfxExpressionBuilder()
    assert str(b.variable(V.ABSOLUTE_PRESSURE)) == "Absolute Pressure"
    assert str(b.variable(V.TEMPERATURE)) == "Temperature"


def test_unknown_variable_rejected():
    b = CfxExpressionBuilder()

    class _Bogus:  # not registered in the CFX naming map
        pass

    with pytest.raises(ExpressionBuildError):
        b.variable(_Bogus())


def test_raw_escape_hatch():
    b = CfxExpressionBuilder()
    assert str(b.raw("MyNamedExpr")) == "MyNamedExpr"


# --------------------------------------------------------------------------- #
# Facade UX                                                                   #
# --------------------------------------------------------------------------- #


def test_group_available_lists_signatures():
    b = CfxExpressionBuilder()
    reductions = b.reductions.available()
    assert "area_ave" in reductions
    assert "mass_flow_ave" in reductions
    assert "area" in reductions
    math = b.math.available()
    assert "sqrt" in math and "pow" in math


def test_unknown_reduction_raises_attribute_error():
    b = CfxExpressionBuilder()
    with pytest.raises(AttributeError):
        b.reductions.does_not_exist


def test_invoker_exposes_signature_and_params():
    b = CfxExpressionBuilder()
    inv = b.reductions.area_ave
    assert isinstance(inv.signature, CfxSignature)
    assert inv.params() == ["expression"]
    assert "area_ave" in repr(inv)
    assert "cfx=" in repr(inv)


def test_render_matches_str():
    b = CfxExpressionBuilder()
    expr = b.reductions.area_ave(expression=V.TEMPERATURE, location="inlet")
    assert CfxExpressionBuilder.render(expr) == str(expr)
