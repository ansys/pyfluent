# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""Smoke test that exercises the expression builder against a live Fluent session.

This test is intentionally minimal: it launches a solver session (via the
shared ``static_mixer_case_session`` fixture), builds an ``AreaAve`` expression
using the Python builder, assigns it to a ``named_expressions`` definition
(which round-trips through the parser via the Fluent string form), and
evaluates the result.

It also confirms that the assignment flows through the *generic*
settings-expression protocol in ``flobject`` -- i.e. no hard-coded
``setup.named_expressions.definition`` path special-casing -- by checking that
the target leaf advertises its accepted quantity kinds via
``_expression_kinds`` and that the expression's kind matches before storage.
"""

from typing import Any

import pytest

from ansys.fluent.core.offline.expressions import ExpressionBuilder, parse
from ansys.units import VariableCatalog
from ansys.units import VariableCatalog as V


@pytest.mark.fluent_version(">=25.1")
def test_expression_builder_area_ave_on_static_mixer(
    static_mixer_case_session: Any,
):
    solver = static_mixer_case_session
    solver.solution.initialization.hybrid_initialize()

    b = ExpressionBuilder(session=solver)  # session enables validation

    # Build "AreaAve(AbsolutePressure, ['inlet1'])" with the Python builder.
    expr = b.reductions.area_ave(expression=V.ABSOLUTE_PRESSURE, locations=["inlet1"])
    rendered = str(expr)
    assert rendered == "AreaAve(AbsolutePressure,['inlet1'])"

    # Round-trip through the parser.
    assert str(parse(rendered)) == rendered

    # Assign as a named expression and evaluate on the live session.
    named = solver.setup.named_expressions.create()

    # The target leaf accepts expression objects through the generic protocol
    # (no hard-coded path): it advertises the quantity kinds it permits, and the
    # expression's own quantity kind is among them, so the type check passes.
    assert expr.__settings_kind__() in named.definition._expression_kinds

    named.definition = expr  # no str() needed, type checked
    value = named.get_value()

    assert isinstance(value, float) and value != 0.0


@pytest.mark.fluent_version(">=25.1")
def test_named_expression_assignment_matches_requested_snippet(
    static_mixer_case_session: Any,
):
    """End-to-end check mirroring the documented user snippet verbatim."""
    solver = static_mixer_case_session
    solver.solution.initialization.hybrid_initialize()

    b = ExpressionBuilder(session=solver)  # session enables validation
    expr = b.reductions.area_ave(
        expression=VariableCatalog.ABSOLUTE_PRESSURE, locations=["inlet1"]
    )  # -> AreaAve(AbsolutePressure, ['inlet1'])

    named = solver.setup.named_expressions.create()
    named.definition = expr  # no str() needed, type checked
    value = named.get_value()

    assert isinstance(value, float)
