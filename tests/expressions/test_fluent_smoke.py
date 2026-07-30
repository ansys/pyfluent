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

from ansys.fluent.core.expressions import ExpressionBuilder, parse
from ansys.units import VariableCatalog as V


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

    # Assign as a named expression and evaluate on the live session.
    named = solver.setup.named_expressions.create()
    named.definition = expr  # Expr accepted directly by flobject integration.
    val = named.get_value()

    assert isinstance(val, float) and val != 0.0
