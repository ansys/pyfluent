# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""Tests for the generic settings-expression protocol in ``flobject``.

These tests verify -- without a live Fluent session -- that the settings layer
accepts "expression objects" through a domain-neutral protocol
(``__settings_str__`` / ``__settings_kind__`` / ``__settings_dimensions__``)
rather than any Fluent-specific hook or hard-coded path. Specifically:

* A :class:`Textual` leaf (``String`` / ``Filename``) accepts an expression
  object *anywhere* and stores its rendered string.
* A :class:`RealNumerical` leaf (``Real`` / ``RealList``) accepts an expression
  object wherever expression strings are permitted.
* Quantity-type validation (structural kind and physical dimension) runs
  *before* the expression is rendered to a string.
* Plain strings and ``VariableDescriptor`` values keep working as before.
"""

import pytest

from ansys.fluent.core.offline.expressions import ExpressionBuilder
from ansys.fluent.core.offline.expressions._ast import Quantity
from ansys.fluent.core.solver.flobject import (
    RealNumerical,
    Textual,
    _is_settings_expression,
    _normalize_dimensions,
    _render_settings_expression,
)
from ansys.units import VariableCatalog as V

# --------------------------------------------------------------------------- #
# Test doubles                                                                #
# --------------------------------------------------------------------------- #


class _FakeTextualLeaf:
    """Minimal stand-in for a ``String``/``Filename`` settings leaf.

    Captures whatever ``base_set_state`` receives so tests can assert on the
    value the settings layer would have stored.
    """

    _has_migration_adapter = False
    _expression_kinds = Textual._expression_kinds
    python_path = "setup.named_expressions['x'].definition"

    def __init__(self):
        self.captured = None

    def base_set_state(self, state=None, **kwargs):
        self.captured = state
        return state

    def set_state_via(self, state):
        """Route through the real ``Textual.set_state`` for this fake leaf."""
        return Textual.set_state(self, state)


class _FakeRealLeaf:
    """Minimal stand-in for a ``Real`` settings leaf with a fixed unit.

    ``units()`` mirrors :meth:`RealNumerical.units`, enabling the dimensional
    check. ``_expression_kinds`` is inherited from :class:`RealNumerical`.
    """

    _expression_kinds = RealNumerical._expression_kinds
    python_path = "setup.boundary_conditions['inlet'].pressure"

    def __init__(self, units="Pa"):
        self._units = units
        self.captured = None

    def units(self):
        return self._units

    def base_set_state(self, state=None, **kwargs):
        self.captured = state
        return state

    def set_state_via(self, state):
        """Route through the real ``RealNumerical.set_state`` for this fake leaf."""
        return RealNumerical.set_state(self, state)


@pytest.fixture
def builder():
    return ExpressionBuilder()  # settings=None -- offline construction


@pytest.fixture
def pressure_expr(builder):
    """A scalar, pressure-dimensioned reduction expression."""
    return builder.reductions.area_ave(
        expression=V.ABSOLUTE_PRESSURE, locations=["inlet1"]
    )


# --------------------------------------------------------------------------- #
# Protocol detection / helpers                                                #
# --------------------------------------------------------------------------- #


def test_expr_implements_settings_protocol(pressure_expr):
    assert _is_settings_expression(pressure_expr) is True
    assert pressure_expr.__settings_str__() == "AreaAve(AbsolutePressure,['inlet1'])"
    assert pressure_expr.__settings_kind__() == "scalar"


def test_plain_values_are_not_settings_expressions():
    assert _is_settings_expression("AbsolutePressure") is False
    assert _is_settings_expression(3.14) is False
    assert _is_settings_expression(V.ABSOLUTE_PRESSURE) is False


def test_normalize_dimensions_accepts_name_and_enum_keys():
    import ansys.units

    from_quantity = _normalize_dimensions(ansys.units.Quantity(1, "Pa").dimensions)
    from_names = _normalize_dimensions({"MASS": 1.0, "LENGTH": -1.0, "TIME": -2.0})
    assert from_quantity == from_names
    # Zero exponents are dropped.
    assert _normalize_dimensions({"MASS": 0.0, "LENGTH": 1.0}) == {"LENGTH": 1.0}


# --------------------------------------------------------------------------- #
# Textual leaves accept expression objects anywhere                           #
# --------------------------------------------------------------------------- #


def test_textual_leaf_accepts_expression_object(pressure_expr):
    leaf = _FakeTextualLeaf()
    Textual.set_state(leaf, pressure_expr)
    assert leaf.captured == "AreaAve(AbsolutePressure,['inlet1'])"


def test_textual_leaf_still_accepts_string():
    leaf = _FakeTextualLeaf()
    Textual.set_state(leaf, "AreaAve(AbsolutePressure, ['inlet1'])")
    assert leaf.captured == "AreaAve(AbsolutePressure, ['inlet1'])"


def test_textual_leaf_still_accepts_variable_descriptor():
    leaf = _FakeTextualLeaf()
    # A VariableDescriptor does not implement the expression protocol, so it is
    # handled by Textual's own field-name strategy: only that a string was
    # captured matters here, not its exact spelling.
    Textual.set_state(leaf, V.ABSOLUTE_PRESSURE)
    assert isinstance(leaf.captured, str) and leaf.captured


def test_textual_leaf_rejects_location_list_expression(builder):
    leaf = _FakeTextualLeaf()
    location_list = builder.locations(["inlet1", "inlet2"])
    with pytest.raises(TypeError, match="kind 'location_list'"):
        Textual.set_state(leaf, location_list)


# --------------------------------------------------------------------------- #
# Real leaves accept expression objects (the new capability)                  #
# --------------------------------------------------------------------------- #


def test_real_leaf_accepts_expression_object(pressure_expr):
    leaf = _FakeRealLeaf(units="Pa")
    RealNumerical.set_state(leaf, pressure_expr)
    assert leaf.captured == "AreaAve(AbsolutePressure,['inlet1'])"


def test_real_leaf_still_accepts_plain_float():
    leaf = _FakeRealLeaf(units="Pa")
    RealNumerical.set_state(leaf, 101325.0)
    assert leaf.captured == 101325.0


# --------------------------------------------------------------------------- #
# Quantity-type validation runs before str conversion                         #
# --------------------------------------------------------------------------- #


def test_real_leaf_rejects_dimension_mismatch():
    # A velocity-dimensioned quantity assigned to a pressure (Pa) leaf must be
    # rejected *before* it is rendered to a string.
    leaf = _FakeRealLeaf(units="Pa")
    velocity = Quantity(5.0, "m s^-1")
    with pytest.raises(TypeError, match="not compatible"):
        RealNumerical.set_state(leaf, velocity)
    assert leaf.captured is None  # never rendered / stored


def test_real_leaf_accepts_matching_dimension():
    leaf = _FakeRealLeaf(units="Pa")
    pressure_quantity = Quantity(101325.0, "Pa")
    RealNumerical.set_state(leaf, pressure_quantity)
    assert leaf.captured == "101325.0 [Pa]"


def test_real_leaf_rejects_vector_expression_kind(builder):
    # A scalar Real leaf does not accept a vector expression regardless of
    # dimensions.
    leaf = _FakeRealLeaf(units="m s^-1")
    vector = builder.vector.make_vec(
        x=builder.literal(1.0), y=builder.literal(2.0), z=builder.literal(3.0)
    )
    with pytest.raises(TypeError, match="kind 'vector'"):
        RealNumerical.set_state(leaf, vector)
    assert leaf.captured is None


def test_unknown_dimension_expression_is_not_blocked(pressure_expr):
    # A composite reduction reports no dimensions, so the dimensional check is
    # skipped and the expression is stored even against a differently-united
    # leaf (the kind check still passes: both scalar).
    assert pressure_expr.__settings_dimensions__() is None
    leaf = _FakeRealLeaf(units="m s^-1")
    RealNumerical.set_state(leaf, pressure_expr)
    assert leaf.captured == "AreaAve(AbsolutePressure,['inlet1'])"


# --------------------------------------------------------------------------- #
# _render_settings_expression contract                                        #
# --------------------------------------------------------------------------- #


def test_render_helper_returns_none_for_plain_value():
    leaf = _FakeRealLeaf()
    assert _render_settings_expression(leaf, 42.0) is None


def test_render_helper_validates_before_rendering():
    leaf = _FakeRealLeaf(units="Pa")
    velocity = Quantity(5.0, "m s^-1")
    with pytest.raises(TypeError):
        _render_settings_expression(leaf, velocity)


# --------------------------------------------------------------------------- #
# Parse a string, read its quantity type, compare with the target parameter   #
# --------------------------------------------------------------------------- #
#
# This mirrors the end-to-end flow a caller cares about: start from an
# expression *string*, parse it back into an expression object, ask that
# object for its quantity (structural) type, and check it against the quantity
# type the target settings parameter accepts -- all before any assignment.


@pytest.mark.parametrize(
    ("expression_string", "expected_kind"),
    [
        ("AreaAve(AbsolutePressure, ['inlet1'])", "scalar"),  # reduction -> scalar
        ("AbsolutePressure", "scalar"),  # bare variable -> scalar
        ("5 [m/s]", "quantity"),  # value-with-units -> quantity
        ("MakeVec(1, 2, 3)", "vector"),  # vector constructor -> vector
        ("AbsolutePressure > 0", "boolean"),  # comparison -> boolean
    ],
)
def test_parsed_expression_reports_its_quantity_type(
    builder, expression_string, expected_kind
):
    # Parse the string back into an expression object via the builder ...
    expr = builder.parse(expression_string)
    # ... and read the quantity (structural) type of the built object.
    assert expr.__settings_kind__() == expected_kind


@pytest.mark.parametrize(
    ("expression_string", "target_leaf_factory", "compatible"),
    [
        # A scalar expression is compatible with a scalar Real parameter.
        ("AreaAve(AbsolutePressure, ['inlet1'])", _FakeRealLeaf, True),
        # A value-with-units is also accepted by a Real parameter.
        ("101325 [Pa]", _FakeRealLeaf, True),
        # A vector expression is NOT compatible with a scalar Real parameter.
        ("MakeVec(1, 2, 3)", _FakeRealLeaf, False),
        # A boolean expression is NOT compatible with a scalar Real parameter.
        ("AbsolutePressure > 0", _FakeRealLeaf, False),
        # A vector expression IS compatible with a (string) definition
        # parameter, which accepts scalar/vector/boolean/quantity.
        ("MakeVec(1, 2, 3)", _FakeTextualLeaf, True),
    ],
)
def test_parsed_expression_kind_vs_target_parameter_kind(
    builder, expression_string, target_leaf_factory, compatible
):
    # Build the expression object from its string form.
    expr = builder.parse(expression_string)
    expr_kind = expr.__settings_kind__()

    # The "quantity type of the target parameter" is the set of kinds it
    # accepts, exposed via ``_expression_kinds``.
    target = target_leaf_factory()
    accepted_kinds = target._expression_kinds

    # Direct comparison of the two quantity types.
    assert (expr_kind in accepted_kinds) is compatible

    # And the settings layer enforces exactly this comparison before storing:
    if compatible:
        target.set_state_via(expr)  # stores the rendered string
        assert target.captured is not None
    else:
        with pytest.raises(TypeError, match=f"kind '{expr_kind}'"):
            target.set_state_via(expr)
        assert target.captured is None
