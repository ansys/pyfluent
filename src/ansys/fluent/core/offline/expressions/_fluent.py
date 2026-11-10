# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""The Fluent dialect of the expression language.

Supplies the Fluent-specific parts to the generic expression package:

* variable naming via :class:`FluentExprNamingStrategy`, and
* the catalog of Fluent expression functions (:data:`FLUENT_FUNCTIONS`).

Function groups
---------------

- ``reductions``  -- ``AreaAve``, ``VolumeInt``, ``Sum``, ``Force``, ...
- ``math``        -- ``sqrt``, ``pow``, ``atan2``, ``min``, ``max``, ...
- ``vector``      -- ``MakeVec``, ``Magnitude``, ``Dot``, ``Cross``
- ``conditional`` -- ``IF``

Adding a new function to the builder is a one-line change here.
"""

from __future__ import annotations

from enum import Enum

from ansys.expressions import Dialect, FunctionRegistry, Kind, Param, Signature
from ansys.fluent.core._variable_strategies import FluentExprNamingStrategy

# --------------------------------------------------------------------------- #
# Weighting options (for Sum's ``Weight=`` keyword argument)                  #
# --------------------------------------------------------------------------- #


class Weight(Enum):
    """Weighting options accepted by ``Sum`` and other reductions."""

    AREA = "Area"
    VOLUME = "Volume"
    MASS = "Mass"
    MASS_FLOW_RATE = "MassFlowRate"
    ABS_MASS_FLOW_RATE = "AbsMassFlowRate"

    def __str__(self) -> str:
        return self.value


FLUENT_FUNCTIONS = FunctionRegistry()
"""Functions available in Fluent expressions."""


# --------------------------------------------------------------------------- #
# Reductions                                                                  #
# --------------------------------------------------------------------------- #
#
# Two shapes dominate:
#   1. expression + locations   -> scalar
#   2. locations only           -> scalar or vector
# ``Sum`` additionally accepts an optional ``Weight=`` keyword.


def _reg_reduction(
    name: str,
    py_name: str,
    *,
    with_expr: bool = True,
    with_weight: bool = False,
    returns: Kind = Kind.SCALAR,
) -> Signature:
    params: list[Param] = []
    if with_expr:
        params.append(Param("expression", Kind.SCALAR))
    params.append(Param("locations", Kind.LOCATION_LIST))
    if with_weight:
        params.append(
            Param(
                "weight",
                Kind.SCALAR,
                optional=True,
                keyword="Weight",
                allowed_literals=Weight,
            )
        )
    return FLUENT_FUNCTIONS.register(
        "reductions",
        Signature(name=name, py_name=py_name, params=tuple(params), returns=returns),
    )


# Scalar reductions: expression + locations.
_reg_reduction("AreaAve", "area_ave")
_reg_reduction("AreaInt", "area_int")
_reg_reduction("VolumeAve", "volume_ave")
_reg_reduction("VolumeInt", "volume_int")
_reg_reduction("MassAve", "mass_ave")
_reg_reduction("MassInt", "mass_int")
_reg_reduction("MassFlowAve", "mass_flow_ave")
_reg_reduction("MassFlowInt", "mass_flow_int")
_reg_reduction("MassFlowAveAbs", "mass_flow_ave_abs")
_reg_reduction("MassFlowIntAbs", "mass_flow_int_abs")
_reg_reduction("Minimum", "minimum")
_reg_reduction("Maximum", "maximum")
_reg_reduction("Average", "average")
_reg_reduction("Sum", "sum", with_weight=True)

# Extent-only (no expression) reductions.
_reg_reduction("Area", "area", with_expr=False)
_reg_reduction("Volume", "volume", with_expr=False)
_reg_reduction("Count", "count", with_expr=False)
_reg_reduction("Mass", "mass", with_expr=False)
_reg_reduction("MassFlow", "mass_flow", with_expr=False)
_reg_reduction("MassFlowAbs", "mass_flow_abs", with_expr=False)

# Vector reductions.
_reg_reduction("Centroid", "centroid", with_expr=False, returns=Kind.VECTOR)
_reg_reduction("Force", "force", with_expr=False, returns=Kind.VECTOR)


# --------------------------------------------------------------------------- #
# Math functions (Fluent-side names are lowercase)                            #
# --------------------------------------------------------------------------- #


def _reg_math(
    fluent_name: str, py_name: str | None = None, arity: int = 1
) -> Signature:
    py_name = py_name or fluent_name
    params = tuple(Param(f"x{i}", Kind.SCALAR) for i in range(arity))
    return FLUENT_FUNCTIONS.register(
        "math",
        Signature(
            name=fluent_name, py_name=py_name, params=params, returns=Kind.SCALAR
        ),
    )


# Unary scalar math.
for _n in (
    "sqrt",
    "abs",
    "fabs",
    "exp",
    "ln",
    "log10",
    "sin",
    "cos",
    "tan",
    "asin",
    "acos",
    "atan",
    "sinh",
    "cosh",
    "tanh",
    "asinh",
    "acosh",
    "atanh",
    "ceil",
    "floor",
    "trunc",
    "sign",
):
    _reg_math(_n, arity=1)

# Binary scalar math.
for _n in ("pow", "atan2", "min", "max", "mod"):
    _reg_math(_n, arity=2)


# --------------------------------------------------------------------------- #
# Vector operations                                                           #
# --------------------------------------------------------------------------- #


FLUENT_FUNCTIONS.register(
    "vector",
    Signature(
        name="MakeVec",
        py_name="make_vec",
        params=(
            Param("x", Kind.SCALAR),
            Param("y", Kind.SCALAR),
            Param("z", Kind.SCALAR),
        ),
        returns=Kind.VECTOR,
    ),
)

FLUENT_FUNCTIONS.register(
    "vector",
    Signature(
        name="Magnitude",
        py_name="magnitude",
        params=(Param("v", Kind.VECTOR),),
        returns=Kind.SCALAR,
    ),
)

FLUENT_FUNCTIONS.register(
    "vector",
    Signature(
        name="Dot",
        py_name="dot",
        params=(Param("a", Kind.VECTOR), Param("b", Kind.VECTOR)),
        returns=Kind.SCALAR,
    ),
)

FLUENT_FUNCTIONS.register(
    "vector",
    Signature(
        name="Cross",
        py_name="cross",
        params=(Param("a", Kind.VECTOR), Param("b", Kind.VECTOR)),
        returns=Kind.VECTOR,
    ),
)


# --------------------------------------------------------------------------- #
# Conditional                                                                 #
# --------------------------------------------------------------------------- #


FLUENT_FUNCTIONS.register(
    "conditional",
    Signature(
        name="IF",
        py_name="if_",
        params=(
            Param("condition", Kind.BOOLEAN),
            Param("then_value", Kind.SCALAR),
            Param("else_value", Kind.SCALAR),
        ),
        returns=Kind.SCALAR,
    ),
)


FLUENT_DIALECT = Dialect(
    name="fluent",
    naming=FluentExprNamingStrategy(),
    functions=FLUENT_FUNCTIONS,
)
"""The Fluent expression dialect."""
