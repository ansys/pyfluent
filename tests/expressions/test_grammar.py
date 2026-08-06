# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""Tests for the full Fluent expression grammar coverage.

Reductions, math functions, vector operations, and the ``IF`` conditional.
"""

import pytest

from ansys.fluent.core.expressions import (
    ExpressionBuilder,
    ExpressionBuildError,
    Weight,
)
from ansys.units import VariableCatalog as V


@pytest.fixture
def b():
    return ExpressionBuilder()


# --------------------------------------------------------------------------- #
# Reductions -- shape coverage                                                #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "py_name, fluent_name",
    [
        ("area_ave", "AreaAve"),
        ("area_int", "AreaInt"),
        ("volume_ave", "VolumeAve"),
        ("volume_int", "VolumeInt"),
        ("mass_ave", "MassAve"),
        ("mass_int", "MassInt"),
        ("mass_flow_ave", "MassFlowAve"),
        ("mass_flow_int", "MassFlowInt"),
        ("mass_flow_ave_abs", "MassFlowAveAbs"),
        ("mass_flow_int_abs", "MassFlowIntAbs"),
        ("minimum", "Minimum"),
        ("maximum", "Maximum"),
        ("average", "Average"),
    ],
)
def test_expression_and_locations_reductions(b, py_name, fluent_name):
    fn = getattr(b.reductions, py_name)
    node = fn(expression=V.ABSOLUTE_PRESSURE, locations=["inlet1"])
    assert str(node) == f"{fluent_name}(AbsolutePressure,['inlet1'])"


@pytest.mark.parametrize(
    "py_name, fluent_name",
    [
        ("area", "Area"),
        ("volume", "Volume"),
        ("count", "Count"),
        ("mass", "Mass"),
        ("mass_flow", "MassFlow"),
        ("mass_flow_abs", "MassFlowAbs"),
    ],
)
def test_extent_only_reductions(b, py_name, fluent_name):
    fn = getattr(b.reductions, py_name)
    node = fn(locations=["inlet1"])
    assert str(node) == f"{fluent_name}(['inlet1'])"


# --------------------------------------------------------------------------- #
# Vector reductions                                                           #
# --------------------------------------------------------------------------- #


def test_centroid_is_vector(b):
    from ansys.fluent.core.expressions import Kind

    node = b.reductions.centroid(locations=["inlet1"])
    assert str(node) == "Centroid(['inlet1'])"
    assert node.kind is Kind.VECTOR


def test_force_is_vector(b):
    from ansys.fluent.core.expressions import Kind

    node = b.reductions.force(locations=["wall"])
    assert node.kind is Kind.VECTOR


# --------------------------------------------------------------------------- #
# Sum with Weight= keyword                                                    #
# --------------------------------------------------------------------------- #


def test_sum_without_weight(b):
    node = b.reductions.sum(expression=V.ABSOLUTE_PRESSURE, locations=["inlet1"])
    assert str(node) == "Sum(AbsolutePressure,['inlet1'])"


def test_sum_with_weight_enum(b):
    node = b.reductions.sum(
        expression=V.ABSOLUTE_PRESSURE,
        locations=["inlet1"],
        weight=Weight.AREA,
    )
    assert str(node) == "Sum(AbsolutePressure,['inlet1'],Weight=Area)"


def test_sum_with_weight_string(b):
    # String form should be accepted too (matches enum value).
    node = b.reductions.sum(
        expression=V.ABSOLUTE_PRESSURE, locations=["inlet1"], weight="Mass"
    )
    assert str(node) == "Sum(AbsolutePressure,['inlet1'],Weight=Mass)"


def test_sum_with_invalid_weight_rejected(b):
    with pytest.raises(ExpressionBuildError, match="weight"):
        b.reductions.sum(
            expression=V.ABSOLUTE_PRESSURE,
            locations=["inlet1"],
            weight="Bogus",
        )


# --------------------------------------------------------------------------- #
# Math functions                                                              #
# --------------------------------------------------------------------------- #


def test_math_group_available(b):
    names = b.math.available()
    assert {"sqrt", "sin", "cos", "log10", "atan2", "pow", "mod"} <= set(names)


def test_math_unary_renders_lowercase(b):
    v = b.variable(V.VELOCITY_MAGNITUDE)
    assert str(b.math.sqrt(v)) == "sqrt(VelocityMagnitude)"
    assert str(b.math.sin(v)) == "sin(VelocityMagnitude)"


def test_math_binary_renders(b):
    v = b.variable(V.VELOCITY_MAGNITUDE)
    assert str(b.math.pow(v, 2)) == "pow(VelocityMagnitude,2)"
    assert str(b.math.atan2(1, v)) == "atan2(1,VelocityMagnitude)"
    assert str(b.math.min(v, 10)) == "min(VelocityMagnitude,10)"


def test_math_arity_enforced(b):
    with pytest.raises(ExpressionBuildError):
        b.math.pow(2)  # missing exponent
    with pytest.raises(ExpressionBuildError):
        b.math.sqrt(1, 2)  # too many args


# --------------------------------------------------------------------------- #
# Vector ops                                                                  #
# --------------------------------------------------------------------------- #


def test_make_vec(b):
    node = b.vector.make_vec(1, 2, 3)
    from ansys.fluent.core.expressions import Kind

    assert str(node) == "MakeVec(1,2,3)"
    assert node.kind is Kind.VECTOR


def test_magnitude_requires_vector(b):
    v = b.variable(V.VELOCITY_MAGNITUDE)  # scalar
    with pytest.raises(ExpressionBuildError, match="vector"):
        b.vector.magnitude(v)


def test_magnitude_of_makevec(b):
    vec = b.vector.make_vec(1, 2, 3)
    node = b.vector.magnitude(vec)
    assert str(node) == "Magnitude(MakeVec(1,2,3))"


def test_dot_and_cross(b):
    a = b.vector.make_vec(1, 0, 0)
    c = b.vector.make_vec(0, 1, 0)
    assert str(b.vector.dot(a, c)) == "Dot(MakeVec(1,0,0),MakeVec(0,1,0))"
    assert str(b.vector.cross(a, c)) == "Cross(MakeVec(1,0,0),MakeVec(0,1,0))"


def test_dot_rejects_scalar(b):
    with pytest.raises(ExpressionBuildError, match="vector"):
        b.vector.dot(1, b.vector.make_vec(0, 1, 0))


# --------------------------------------------------------------------------- #
# IF conditional                                                              #
# --------------------------------------------------------------------------- #


def test_if_basic(b):
    v = b.variable(V.VELOCITY_MAGNITUDE)
    node = b.conditional.if_(v > 10, v, 0)
    assert str(node) == "IF((VelocityMagnitude > 10),VelocityMagnitude,0)"


def test_if_requires_boolean_condition(b):
    with pytest.raises(ExpressionBuildError, match="boolean"):
        b.conditional.if_(1, 2, 3)  # 1 is scalar, not boolean


def test_if_in_reduction(b):
    v = b.variable(V.VELOCITY_MAGNITUDE)
    inner = b.conditional.if_(v > 10, v, 0)
    node = b.reductions.area_ave(expression=inner, locations=["inlet1"])
    assert str(node) == (
        "AreaAve(IF((VelocityMagnitude > 10),VelocityMagnitude,0)," "['inlet1'])"
    )


# --------------------------------------------------------------------------- #
# Registry coverage smoke tests                                               #
# --------------------------------------------------------------------------- #


def test_registered_groups(b):
    from ansys.fluent.core.expressions._registry import REGISTRY

    assert set(REGISTRY.groups()) >= {"reductions", "math", "vector", "conditional"}


def test_make_call_escape_hatch(b):
    # For anything not yet catalogued, users can still hand-roll a Call.
    from ansys.fluent.core.expressions import Kind
    from ansys.fluent.core.expressions._registry import make_call

    node = make_call("Grad", b.variable(V.TEMPERATURE), returns=Kind.VECTOR)
    assert str(node) == "Grad(StaticTemperature)"
    assert node.kind is Kind.VECTOR
