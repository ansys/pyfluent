# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""Layer 1: declarative catalog of Fluent expression functions.

Each :class:`Signature` describes a Fluent-side function: its name, the
kinds and order of its parameters, and its return kind.  The registry is
the *single source of truth* driving both the user-facing factory
(:class:`~.builder.ExpressionBuilder`) and validation performed by the AST.

Adding a new function to the builder is a one-line change here.

Function groups
---------------

- ``reductions``  -- ``AreaAve``, ``VolumeInt``, ``Sum``, ``Force``, ...
- ``math``        -- ``sqrt``, ``pow``, ``atan2``, ``min``, ``max``, ...
- ``vector``      -- ``MakeVec``, ``Magnitude``, ``Dot``, ``Cross``
- ``conditional`` -- ``IF``
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from ._ast import (
    Call,
    Expr,
    KeywordArg,
    Kind,
    RawName,
    _coerce,
    coerce_location_list,
)
from .errors import ExpressionBuildError


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

    def __str__(self):
        return self.value


# --------------------------------------------------------------------------- #
# Params                                                                      #
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class Param:
    """One parameter slot of a :class:`Signature`.

    Parameters
    ----------
    name :
        Python-side keyword.
    kind :
        Expected :class:`Kind` of the argument.
    optional :
        When ``True``, callers may omit the argument.
    keyword :
        When set, the argument renders as ``<keyword>=<value>`` inside the
        Fluent-side argument list (e.g. ``Weight=Area``).
    allowed_literals :
        When set, restricts values to the given literals (typically an
        :class:`Enum` class).  The stringified value is used for rendering
        as a raw token (unquoted).
    """

    name: str
    kind: Kind
    optional: bool = False
    keyword: str | None = None
    allowed_literals: object | None = field(default=None, compare=False)

    def coerce(self, value) -> Expr | None:
        if value is None:
            if self.optional:
                return None
            raise ExpressionBuildError(
                f"Missing required argument {self.name!r}."
            )

        if self.allowed_literals is not None:
            token = self._validate_literal(value)
            arg: Expr = RawName(token)
        elif self.kind is Kind.LOCATION_LIST:
            arg = coerce_location_list(value)
        else:
            arg = _coerce(value)
            if not _kind_compatible(arg.kind, self.kind):
                raise ExpressionBuildError(
                    f"Parameter {self.name!r} expects {self.kind.value}, "
                    f"got {arg.kind.value}.",
                    slot=self.name,
                )

        if self.keyword is not None:
            return KeywordArg(self.keyword, arg)
        return arg

    def _validate_literal(self, value) -> str:
        allowed = self.allowed_literals
        if isinstance(allowed, type) and issubclass(allowed, Enum):
            if isinstance(value, allowed):
                return str(value.value)
            for m in allowed:
                if m.value == value or m.name == value:
                    return str(m.value)
            raise ExpressionBuildError(
                f"Parameter {self.name!r} must be one of "
                f"{[m.value for m in allowed]}, got {value!r}."
            )
        allowed_list = list(allowed)  # type: ignore[arg-type]
        if value not in allowed_list:
            raise ExpressionBuildError(
                f"Parameter {self.name!r} must be one of {allowed_list}, "
                f"got {value!r}."
            )
        return str(value)


_COMPAT = {
    Kind.SCALAR: {Kind.SCALAR, Kind.QUANTITY},
    Kind.QUANTITY: {Kind.QUANTITY, Kind.SCALAR},
    Kind.VECTOR: {Kind.VECTOR},
    Kind.BOOLEAN: {Kind.BOOLEAN},
    Kind.LOCATION_LIST: {Kind.LOCATION_LIST},
}


def _kind_compatible(actual: Kind, expected: Kind) -> bool:
    return actual in _COMPAT[expected]


# --------------------------------------------------------------------------- #
# Signature                                                                   #
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class Signature:
    """Describes a Fluent-side function callable from expressions."""

    name: str            # Fluent-side name, e.g. "AreaAve"
    py_name: str         # Python-side snake_case, e.g. "area_ave"
    params: tuple[Param, ...]
    returns: Kind = Kind.SCALAR

    def build(self, *args, **kwargs) -> Call:
        bound = self._bind(args, kwargs)
        rendered: list[Expr] = []
        for p, v in zip(self.params, bound):
            if v is None and p.optional:
                continue
            coerced = p.coerce(v)
            if coerced is not None:
                rendered.append(coerced)
        return Call(self.name, tuple(rendered), return_kind=self.returns)

    def _bind(self, args, kwargs) -> list:
        if len(args) > len(self.params):
            raise ExpressionBuildError(
                f"{self.py_name}() takes {len(self.params)} positional "
                f"args at most, got {len(args)}."
            )
        result: list = [None] * len(self.params)
        for i, v in enumerate(args):
            result[i] = v
        by_name = {p.name: i for i, p in enumerate(self.params)}
        for k, v in kwargs.items():
            if k not in by_name:
                raise ExpressionBuildError(
                    f"{self.py_name}() got unexpected keyword {k!r}."
                )
            i = by_name[k]
            if result[i] is not None:
                raise ExpressionBuildError(
                    f"{self.py_name}() got multiple values for {k!r}."
                )
            result[i] = v
        for p, v in zip(self.params, result):
            if v is None and not p.optional:
                raise ExpressionBuildError(
                    f"{self.py_name}() missing required argument {p.name!r}."
                )
        return result


# --------------------------------------------------------------------------- #
# Registry                                                                    #
# --------------------------------------------------------------------------- #


class _Registry:
    def __init__(self):
        self._by_group: dict[str, dict[str, Signature]] = {}

    def register(self, group: str, sig: Signature) -> Signature:
        self._by_group.setdefault(group, {})[sig.py_name] = sig
        return sig

    def group(self, name: str) -> dict[str, Signature]:
        return dict(self._by_group.get(name, {}))

    def groups(self) -> tuple[str, ...]:
        return tuple(self._by_group)


REGISTRY = _Registry()


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
    return REGISTRY.register(
        "reductions",
        Signature(name=name, py_name=py_name, params=tuple(params), returns=returns),
    )


# Scalar reductions: expression + locations.
_reg_reduction("AreaAve",         "area_ave")
_reg_reduction("AreaInt",         "area_int")
_reg_reduction("VolumeAve",       "volume_ave")
_reg_reduction("VolumeInt",       "volume_int")
_reg_reduction("MassAve",         "mass_ave")
_reg_reduction("MassInt",         "mass_int")
_reg_reduction("MassFlowAve",     "mass_flow_ave")
_reg_reduction("MassFlowInt",     "mass_flow_int")
_reg_reduction("MassFlowAveAbs",  "mass_flow_ave_abs")
_reg_reduction("MassFlowIntAbs",  "mass_flow_int_abs")
_reg_reduction("Minimum",         "minimum")
_reg_reduction("Maximum",         "maximum")
_reg_reduction("Average",         "average")
_reg_reduction("Sum",             "sum", with_weight=True)

# Extent-only (no expression) reductions.
_reg_reduction("Area",         "area",           with_expr=False)
_reg_reduction("Volume",       "volume",         with_expr=False)
_reg_reduction("Count",        "count",          with_expr=False)
_reg_reduction("Mass",         "mass",           with_expr=False)
_reg_reduction("MassFlow",     "mass_flow",      with_expr=False)
_reg_reduction("MassFlowAbs",  "mass_flow_abs",  with_expr=False)

# Vector reductions.
_reg_reduction("Centroid", "centroid", with_expr=False, returns=Kind.VECTOR)
_reg_reduction("Force",    "force",    with_expr=False, returns=Kind.VECTOR)


# --------------------------------------------------------------------------- #
# Math functions (Fluent-side names are lowercase)                            #
# --------------------------------------------------------------------------- #


def _reg_math(fluent_name: str, py_name: str | None = None, arity: int = 1) -> Signature:
    py_name = py_name or fluent_name
    params = tuple(Param(f"x{i}", Kind.SCALAR) for i in range(arity))
    return REGISTRY.register(
        "math",
        Signature(name=fluent_name, py_name=py_name, params=params, returns=Kind.SCALAR),
    )


# Unary scalar math.
for _n in (
    "sqrt", "abs", "fabs", "exp", "ln", "log10",
    "sin", "cos", "tan", "asin", "acos", "atan",
    "sinh", "cosh", "tanh", "asinh", "acosh", "atanh",
    "ceil", "floor", "trunc", "sign",
):
    _reg_math(_n, arity=1)

# Binary scalar math.
for _n in ("pow", "atan2", "min", "max", "mod"):
    _reg_math(_n, arity=2)


# --------------------------------------------------------------------------- #
# Vector operations                                                           #
# --------------------------------------------------------------------------- #


REGISTRY.register(
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

REGISTRY.register(
    "vector",
    Signature(
        name="Magnitude",
        py_name="magnitude",
        params=(Param("v", Kind.VECTOR),),
        returns=Kind.SCALAR,
    ),
)

REGISTRY.register(
    "vector",
    Signature(
        name="Dot",
        py_name="dot",
        params=(Param("a", Kind.VECTOR), Param("b", Kind.VECTOR)),
        returns=Kind.SCALAR,
    ),
)

REGISTRY.register(
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


REGISTRY.register(
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


# --------------------------------------------------------------------------- #
# Convenience: hand-roll a Call for anything not (yet) in the registry.       #
# --------------------------------------------------------------------------- #


def make_call(fluent_name: str, *args, returns: Kind = Kind.SCALAR) -> Call:
    return Call(fluent_name, tuple(_coerce(a) for a in args), return_kind=returns)
