# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""Tests for the Fluent expression parser and round-tripping."""

import pytest

from ansys.fluent.core.expressions import (
    ExpressionBuilder,
    ExpressionBuildError,
    Kind,
    Weight,
    parse,
)
from ansys.fluent.core.expressions._ast import (
    BinOp,
    Call,
    Compare,
    KeywordArg,
    Literal,
    LocationList,
    Quantity,
    RawName,
    UnaryOp,
    Variable,
)
from ansys.units import VariableCatalog as V


@pytest.fixture
def b():
    return ExpressionBuilder()


# --------------------------------------------------------------------------- #
# Atoms                                                                       #
# --------------------------------------------------------------------------- #


def test_parse_int_literal():
    node = parse("42")
    assert isinstance(node, Literal) and node.value == 42


def test_parse_float_literal():
    node = parse("3.14")
    assert isinstance(node, Literal) and node.value == 3.14


def test_parse_scientific_literal():
    node = parse("1.5e-3")
    assert isinstance(node, Literal) and node.value == 1.5e-3


def test_parse_quantity():
    node = parse("5 [m/s]")
    assert isinstance(node, Quantity)
    assert node.value == 5.0
    assert node.units == "m/s"


def test_parse_variable_by_name():
    node = parse("AbsolutePressure")
    assert isinstance(node, Variable)
    assert node.descriptor is V.ABSOLUTE_PRESSURE


def test_parse_dotted_variable():
    node = parse("Velocity.x")
    assert isinstance(node, Variable)
    assert node.descriptor is V.VELOCITY_X


def test_parse_unknown_identifier_is_rawname():
    node = parse("MyNamedExpression")
    assert isinstance(node, RawName)
    assert node.name == "MyNamedExpression"


def test_parse_location_list():
    node = parse("['inlet1', 'inlet2']")
    assert isinstance(node, LocationList)
    assert node.names == ("inlet1", "inlet2")


def test_parse_empty_location_list():
    node = parse("[]")
    assert isinstance(node, LocationList) and node.names == ()


# --------------------------------------------------------------------------- #
# Operators                                                                   #
# --------------------------------------------------------------------------- #


def test_parse_addition_precedence():
    node = parse("1 + 2 * 3")
    assert isinstance(node, BinOp) and node.op == "+"
    assert isinstance(node.right, BinOp) and node.right.op == "*"


def test_parse_parens_override_precedence():
    node = parse("(1 + 2) * 3")
    assert isinstance(node, BinOp) and node.op == "*"
    assert isinstance(node.left, BinOp) and node.left.op == "+"


def test_parse_unary_minus():
    node = parse("-5")
    assert isinstance(node, UnaryOp) and node.op == "-"
    assert isinstance(node.operand, Literal)


def test_parse_power_right_associative():
    node = parse("2 ** 3 ** 2")
    assert isinstance(node, BinOp) and node.op == "**"
    assert isinstance(node.right, BinOp) and node.right.op == "**"


def test_parse_comparison():
    node = parse("VelocityMagnitude > 10")
    assert isinstance(node, Compare) and node.op == ">"


# --------------------------------------------------------------------------- #
# Calls                                                                       #
# --------------------------------------------------------------------------- #


def test_parse_area_ave():
    node = parse("AreaAve(AbsolutePressure,['inlet1'])")
    assert isinstance(node, Call) and node.name == "AreaAve"
    assert isinstance(node.args[0], Variable)
    assert isinstance(node.args[1], LocationList)


def test_parse_sum_with_weight():
    node = parse("Sum(AbsolutePressure,['inlet1'],Weight=Area)")
    assert isinstance(node, Call) and node.name == "Sum"
    assert isinstance(node.args[2], KeywordArg)
    assert node.args[2].keyword == "Weight"


def test_parse_nested_calls():
    node = parse("Magnitude(MakeVec(1,2,3))")
    assert isinstance(node, Call) and node.name == "Magnitude"
    assert isinstance(node.args[0], Call) and node.args[0].name == "MakeVec"


def test_parse_return_kind_from_registry():
    node = parse("Centroid(['inlet1'])")
    assert node.kind is Kind.VECTOR
    node = parse("Magnitude(MakeVec(1,2,3))")
    assert node.kind is Kind.SCALAR


def test_parse_unregistered_call_defaults_to_scalar():
    node = parse("SomeFuture(1,2)")
    assert isinstance(node, Call) and node.kind is Kind.SCALAR


# --------------------------------------------------------------------------- #
# Round-tripping                                                              #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "canonical",
    [
        "AbsolutePressure",
        "Velocity.x",
        "42",
        "3.14",
        "5.0 [m/s]",
        "['inlet1']",
        "['inlet1', 'inlet2']",
        "AreaAve(AbsolutePressure,['inlet1'])",
        "AreaAve(AbsolutePressure,['inlet1', 'inlet2'])",
        "Sum(AbsolutePressure,['inlet1'],Weight=Area)",
        "Count(['inlet1'])",
        "Centroid(['inlet1'])",
        "MakeVec(1,2,3)",
        "Magnitude(MakeVec(1,2,3))",
        "Dot(MakeVec(1,0,0),MakeVec(0,1,0))",
        "sqrt(VelocityMagnitude)",
        "pow(VelocityMagnitude,2)",
        "IF((VelocityMagnitude > 10),VelocityMagnitude,0)",
        "(AreaAve(AbsolutePressure,['inlet1']) - AreaAve(AbsolutePressure,['outlet']))",
        "((2 * VelocityMagnitude) + 1)",
        "(-VelocityMagnitude)",
    ],
)
def test_round_trip_canonical(canonical):
    assert str(parse(canonical)) == canonical


def test_round_trip_of_builder_output(b):
    # Whatever the builder produces should re-parse identically.
    dp = b.reductions.area_ave(
        expression=V.ABSOLUTE_PRESSURE, locations=["inlet1"]
    ) - b.reductions.area_ave(expression=V.ABSOLUTE_PRESSURE, locations=["outlet"])
    s = str(dp)
    assert str(parse(s)) == s


def test_parse_via_builder_class(b):
    node = b.parse("AreaAve(AbsolutePressure,['inlet1'])")
    assert isinstance(node, Call) and node.name == "AreaAve"


# --------------------------------------------------------------------------- #
# Editing a parsed tree                                                       #
# --------------------------------------------------------------------------- #


def test_edit_parsed_tree(b):
    original = "AreaAve(AbsolutePressure,['inlet1'])"
    node = b.parse(original)
    # Replace with a subtraction against another reduction.
    outlet = b.reductions.area_ave(expression=V.ABSOLUTE_PRESSURE, locations=["outlet"])
    edited = node - outlet
    assert str(edited) == (
        "(AreaAve(AbsolutePressure,['inlet1']) - "
        "AreaAve(AbsolutePressure,['outlet']))"
    )


# --------------------------------------------------------------------------- #
# Error handling                                                              #
# --------------------------------------------------------------------------- #


def test_parse_empty_string_raises():
    with pytest.raises(ExpressionBuildError, match="empty"):
        parse("")


def test_parse_non_string_raises():
    with pytest.raises(ExpressionBuildError, match="string"):
        parse(123)  # type: ignore[arg-type]


def test_parse_unbalanced_parens():
    with pytest.raises(ExpressionBuildError):
        parse("AreaAve(AbsolutePressure,['inlet1']")


def test_parse_trailing_garbage():
    with pytest.raises(ExpressionBuildError):
        parse("42 garbage")


def test_parse_bad_character():
    with pytest.raises(ExpressionBuildError):
        parse("1 @ 2")
