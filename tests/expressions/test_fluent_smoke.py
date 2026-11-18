# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""Smoke test that exercises the expression builder against a live Fluent session.

This test is intentionally minimal: it launches a solver session (via the
shared ``static_mixer_case_session`` fixture), builds an ``AreaAve`` expression
using the Python builder, assigns it to a ``named_expressions`` definition
(which round-trips through the parser via the Fluent string form), and
evaluates the result.
"""

from typing import Any

import pytest

from ansys.fluent.core.offline.expressions import ExpressionBuilder, parse
from ansys.variables import Catalog as V


@pytest.mark.fluent_version(">=25.1")
def test_expression_builder_area_ave_on_static_mixer(
    static_mixer_case_session: Any,
):
    solver = static_mixer_case_session
    solver.solution.initialization.hybrid_initialize()

    b = ExpressionBuilder(session=solver)

    # Build "AreaAve(AbsolutePressure, ['inlet1'])" with the Python builder.
    expr = b.reductions.area_ave(expression=V.ABSOLUTE_PRESSURE, locations=["inlet1"])
    rendered = str(expr)
    assert rendered == "AreaAve(AbsolutePressure,['inlet1'])"

    # Round-trip through the parser.
    assert str(parse(rendered)) == rendered

    # Assign the builder object directly as a named-expression definition and
    # evaluate it on the live session. A named-expression definition is a
    # whitelisted textual path, so the expression object is accepted directly
    # (rendered to its string form by the flobject settings integration).
    named = solver.setup.named_expressions.create()
    named.definition = expr
    value = named.get_value()

    assert isinstance(value, float) and value != 0.0


@pytest.mark.fluent_version(">=25.1")
def test_expression_builder_on_boundary_condition_parameters(
    static_mixer_case_session: Any,
):
    """Assign expression objects to boundary-condition parameters.

    Unlike ``named_expressions.definition`` (a whitelisted textual path), a
    boundary-condition value leaf is a real-valued setting. It accepts an
    expression object directly, but validates the expression's quantity type
    (structural kind and physical dimensions) against the leaf *before*
    rendering it to a string. This exercises both an allowed assignment and the
    two ways an assignment is rejected.
    """
    solver = static_mixer_case_session
    solver.solution.initialization.hybrid_initialize()

    b = ExpressionBuilder(session=solver)

    inlet = solver.setup.boundary_conditions.velocity_inlet["inlet1"]
    velocity_magnitude = inlet.momentum.velocity_magnitude.value

    # Allowed: a velocity-dimensioned expression on a velocity-magnitude leaf.
    velocity_magnitude.set_state(b.quantity(1.5, "m/s"))
    assert velocity_magnitude.get_state() == "1.5 [m/s]"

    # Disallowed (dimension mismatch): a pressure-dimensioned expression on a
    # velocity leaf is rejected before it is rendered or stored.
    with pytest.raises(TypeError, match="not compatible"):
        velocity_magnitude.set_state(b.quantity(101325.0, "Pa"))

    # Disallowed (kind mismatch): a vector expression cannot be assigned to a
    # scalar real leaf, regardless of dimensions.
    vector = b.vector.make_vec(x=b.literal(1.0), y=b.literal(2.0), z=b.literal(3.0))
    with pytest.raises(TypeError, match="kind 'vector'"):
        velocity_magnitude.set_state(vector)

    # Neither rejected assignment disturbed the previously stored value.
    assert velocity_magnitude.get_state() == "1.5 [m/s]"
