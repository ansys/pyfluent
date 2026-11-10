# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""Product-agnostic, unit-aware expression trees.

This package must not depend on any product. Product-specific details
(variable names and the available functions) are supplied through a
:class:`Dialect`.

The package is organised in layers:

* :mod:`._ast`       -- typed, immutable expression tree.
* :mod:`._registry`  -- declarative function signatures and registries.
* :mod:`._dialect`   -- product-specific naming and functions.
* :mod:`._parser`    -- expression string to tree.
* :mod:`._discovery` / :mod:`._slots` -- legal values for builder parameters.
* :mod:`.builder`    -- user-facing, discoverable facade.

Typical use::

    from ansys.units.variable_descriptor import VariableCatalog as V

    reductions = FunctionRegistry()
    reductions.register(
        "reductions",
        Signature(
            "AreaAve",
            "area_ave",
            (Param("expression", Kind.SCALAR), Param("locations", Kind.LOCATION_LIST)),
        ),
    )
    dialect = Dialect("my_product", functions=reductions)
    builder = ExpressionBuilder(dialect)

    expr = builder.reductions.area_ave(V.ABSOLUTE_PRESSURE, ["inlet"]) * 2
    str(expr)  # "(AreaAve(absolute_pressure,['inlet']) * 2)"
"""

from ._ast import (
    BinOp,
    BooleanExpr,
    Call,
    Compare,
    Expr,
    KeywordArg,
    Kind,
    Literal,
    LocationList,
    Operand,
    Quantity,
    RawName,
    ScalarExpr,
    UnaryOp,
    Variable,
    VectorExpr,
    common_dialect,
)
from ._dialect import DEFAULT_DIALECT, DescriptorNameStrategy, Dialect
from ._discovery import Discovery, StaticDiscovery
from ._parser import parse
from ._registry import FunctionRegistry, Param, Signature, make_call
from ._slots import LocationSlot, ScalarSlot, SlotAccessor
from .builder import ExpressionBuilder, FunctionGroup, FunctionInvoker
from .errors import ExpressionBuildError

__all__ = [
    "BinOp",
    "BooleanExpr",
    "Call",
    "Compare",
    "DEFAULT_DIALECT",
    "DescriptorNameStrategy",
    "Dialect",
    "Discovery",
    "Expr",
    "ExpressionBuildError",
    "ExpressionBuilder",
    "FunctionGroup",
    "FunctionInvoker",
    "FunctionRegistry",
    "KeywordArg",
    "Kind",
    "Literal",
    "LocationList",
    "LocationSlot",
    "Operand",
    "Param",
    "Quantity",
    "RawName",
    "ScalarExpr",
    "ScalarSlot",
    "Signature",
    "SlotAccessor",
    "StaticDiscovery",
    "UnaryOp",
    "Variable",
    "VectorExpr",
    "common_dialect",
    "make_call",
    "parse",
]
