# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""Tests for Textual.set_state's expression-object integration.

Verifies -- without a live Fluent session -- that:

* At a path listed in :data:`EXPRESSION_DEFINITION_PATHS`, a Textual leaf
  accepts an object implementing ``__fluent_expr__`` and stores its
  rendered string.
* At other paths, expression objects are rejected (falls through to the
  existing ``TypeError`` for non-string input).
* Strings and VariableDescriptors continue to work as before.
"""

import pytest
from ansys.units import VariableCatalog as V

from ansys.fluent.core.expressions import ExpressionBuilder
from ansys.fluent.core.solver.flobject import (
    EXPRESSION_DEFINITION_PATHS,
    Textual,
    _matches_expression_definition_path,
    _python_name_chain,
)


# --------------------------------------------------------------------------- #
# Test doubles                                                                #
# --------------------------------------------------------------------------- #


class _FakeNode:
    """Minimal stand-in for a settings-tree node.

    Provides just enough shape (``python_name`` + ``_parent``) for
    :func:`_python_name_chain` and :func:`_matches_expression_definition_path`
    to work, plus a ``base_set_state`` capture used by
    :class:`Textual.set_state`.
    """

    _has_migration_adapter = False

    def __init__(self, python_name: str, parent=None):
        self.python_name = python_name
        self._parent = parent
        self.captured = None

    def base_set_state(self, state=None, **kwargs):
        self.captured = state
        return state


def _make_leaf(chain: list[str]) -> _FakeNode:
    """Build a chain root->leaf and return the leaf."""
    node = None
    for name in chain:
        node = _FakeNode(name, parent=node)
    return node


# Use Textual.set_state as an unbound method on a _FakeNode.
def _set_state(node, state):
    return Textual.set_state(node, state)


# --------------------------------------------------------------------------- #
# Constant / helpers                                                          #
# --------------------------------------------------------------------------- #


def test_default_expression_definition_paths():
    assert ("setup", "named_expressions", "definition") in EXPRESSION_DEFINITION_PATHS


def test_python_name_chain_strips_indices():
    leaf = _make_leaf(["setup", "named_expressions", "[test_expr]", "definition"])
    assert _python_name_chain(leaf) == [
        "setup", "named_expressions", "definition"
    ]


def test_matches_expression_definition_path_positive():
    leaf = _make_leaf(["setup", "named_expressions", "[dp]", "definition"])
    assert _matches_expression_definition_path(leaf) is True


def test_matches_expression_definition_path_negative():
    leaf = _make_leaf(["setup", "boundary_conditions", "[inlet1]", "name"])
    assert _matches_expression_definition_path(leaf) is False


# --------------------------------------------------------------------------- #
# Textual.set_state at whitelisted path                                       #
# --------------------------------------------------------------------------- #


@pytest.fixture
def definition_leaf():
    return _make_leaf(
        ["setup", "named_expressions", "[test_expr_1]", "definition"]
    )


@pytest.fixture
def expr():
    b = ExpressionBuilder()
    return b.reductions.area_ave(
        expression=V.ABSOLUTE_PRESSURE, locations=["inlet1"]
    )


def test_expression_object_rendered_at_whitelisted_path(definition_leaf, expr):
    _set_state(definition_leaf, expr)
    assert definition_leaf.captured == "AreaAve(AbsolutePressure,['inlet1'])"


def test_string_still_accepted_at_whitelisted_path(definition_leaf):
    _set_state(definition_leaf, "AreaAve(AbsolutePressure, ['inlet1'])")
    assert definition_leaf.captured == "AreaAve(AbsolutePressure, ['inlet1'])"


def test_variable_descriptor_still_accepted_at_whitelisted_path(definition_leaf):
    _set_state(definition_leaf, V.ABSOLUTE_PRESSURE)
    # Textual uses its own field-name naming strategy for VariableDescriptors;
    # the exact spelling is not the concern of this test -- only that a string
    # was captured (i.e. we did not intercept and mis-handle the descriptor).
    assert isinstance(definition_leaf.captured, str)
    assert definition_leaf.captured  # non-empty


# --------------------------------------------------------------------------- #
# Textual.set_state at non-whitelisted path                                   #
# --------------------------------------------------------------------------- #


def test_expression_object_rejected_at_other_path(expr):
    leaf = _make_leaf(["setup", "some_group", "[x]", "some_string_field"])
    with pytest.raises(TypeError):
        _set_state(leaf, expr)
