# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""Fluent expression builder.

A high-level, object-based API for constructing Fluent expression strings
(e.g. ``AreaAve(AbsolutePressure,['velocity-inlet-5'])``) without hand-writing
them.

The package is split into:

* :mod:`._generic`   -- product-agnostic expression trees, parser, and builder.
  It must not import anything Fluent-specific.
* :mod:`._fluent`    -- the Fluent dialect: variable naming and the catalog of
  Fluent expression functions.
* :mod:`._discovery` -- discovery backed by a live PyFluent session.
* :mod:`.builder`    -- :class:`ExpressionBuilder` bound to the Fluent dialect.

Typical use::

    from ansys.fluent.core.offline.expressions import ExpressionBuilder
    from ansys.units import VariableCatalog as V

    builder = ExpressionBuilder(settings=solver.settings)

    dp = (
        builder.reductions.area_ave(
            expression=V.ABSOLUTE_PRESSURE, locations=["inlet1"]
        )
        - builder.reductions.area_ave(
            expression=V.ABSOLUTE_PRESSURE, locations=["outlet"]
        )
    )

    solver.setup.named_expressions["dp"] = {}
    # The settings layer accepts the expression object directly at a named
    # expression's ``definition``, so no manual ``str(dp)`` conversion is
    # required (plain strings still work too):
    solver.setup.named_expressions["dp"].definition = dp
"""

from ._fluent import FLUENT_DIALECT, Weight  # noqa: F401
from ._generic import (  # noqa: F401
    BooleanExpr,
    Expr,
    ExpressionBuildError,
    Kind,
    LocationList,
    Quantity,
    ScalarExpr,
    VectorExpr,
)
from .builder import ExpressionBuilder, make_call, parse  # noqa: F401
