# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""Fluent expression builder.

A high-level, object-based API for constructing Fluent expression strings
(e.g. ``AreaAve(AbsolutePressure,['velocity-inlet-5'])``) without hand-writing
them.

The package is organised in three layers:

* :mod:`._ast`      -- Layer 2: typed, immutable expression AST.
* :mod:`._registry` -- Layer 1: declarative catalog of Fluent functions.
* :mod:`.builder`   -- Layer 3: user-facing fluent/discoverable facade.

Typical use::

    from ansys.fluent.core.expressions import ExpressionBuilder
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
    solver.setup.named_expressions["dp"].definition = str(dp)
"""

from ._ast import (  # noqa: F401
    BooleanExpr,
    Expr,
    Kind,
    LocationList,
    Quantity,
    ScalarExpr,
    VectorExpr,
)
from ._registry import Weight  # noqa: F401
from .builder import ExpressionBuilder  # noqa: F401
from .errors import ExpressionBuildError  # noqa: F401
