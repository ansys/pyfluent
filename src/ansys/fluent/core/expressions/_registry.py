# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""Layer 1: declarative catalog of Fluent expression functions.

Each :class:`Signature` describes a Fluent-side function: its name, the
kinds and order of its parameters, and its return kind.  The registry is
the *single source of truth* driving both the user-facing factory
(:class:`~.builder.ExpressionBuilder`) and validation performed by the AST.

Adding a new function to the builder is a one-line change here.
"""

from __future__ import annotations

from dataclasses import dataclass

from ._ast import (
    Call,
    Expr,
    Kind,
    _coerce,
    coerce_location_list,
)
from .errors import ExpressionBuildError


@dataclass(frozen=True)
class Param:
    name: str
    kind: Kind

    def coerce(self, value) -> Expr:
        if self.kind is Kind.LOCATION_LIST:
            return coerce_location_list(value)
        expr = _coerce(value)
        if not _kind_compatible(expr.kind, self.kind):
            raise ExpressionBuildError(
                f"Parameter {self.name!r} expects {self.kind.value}, "
                f"got {expr.kind.value}.",
                slot=self.name,
            )
        return expr


_COMPAT = {
    Kind.SCALAR: {Kind.SCALAR, Kind.QUANTITY},
    Kind.QUANTITY: {Kind.QUANTITY, Kind.SCALAR},
    Kind.VECTOR: {Kind.VECTOR},
    Kind.BOOLEAN: {Kind.BOOLEAN},
    Kind.LOCATION_LIST: {Kind.LOCATION_LIST},
}


def _kind_compatible(actual: Kind, expected: Kind) -> bool:
    return actual in _COMPAT[expected]


@dataclass(frozen=True)
class Signature:
    """Describes a Fluent-side function callable from expressions."""

    name: str            # Fluent-side name, e.g. "AreaAve"
    py_name: str         # Python-side snake_case, e.g. "area_ave"
    params: tuple[Param, ...]
    returns: Kind = Kind.SCALAR

    def build(self, *args, **kwargs) -> Call:
        bound = self._bind(args, kwargs)
        coerced = tuple(p.coerce(v) for p, v in zip(self.params, bound))
        return Call(self.name, coerced, return_kind=self.returns)

    def _bind(self, args, kwargs) -> list:
        if len(args) > len(self.params):
            raise ExpressionBuildError(
                f"{self.py_name}() takes {len(self.params)} positional "
                f"args at most, got {len(args)}."
            )
        result = [None] * len(self.params)
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
            if v is None:
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


def _reg_reduction(name: str, py_name: str, *, with_expr: bool = True,
                   returns: Kind = Kind.SCALAR) -> Signature:
    params = []
    if with_expr:
        params.append(Param("expression", Kind.SCALAR))
    params.append(Param("locations", Kind.LOCATION_LIST))
    return REGISTRY.register(
        "reductions",
        Signature(name=name, py_name=py_name, params=tuple(params), returns=returns),
    )


# Reductions -- names mirror reduction.py / Fluent expression grammar.
_reg_reduction("AreaAve",   "area_ave")
_reg_reduction("AreaInt",   "area_int")
_reg_reduction("VolumeAve", "volume_ave")
_reg_reduction("VolumeInt", "volume_int")
_reg_reduction("Minimum",   "minimum")
_reg_reduction("Maximum",   "maximum")
_reg_reduction("Sum",       "sum")
_reg_reduction("Area",      "area", with_expr=False)
_reg_reduction("Volume",    "volume", with_expr=False)
_reg_reduction("Count",     "count", with_expr=False)


def _reg_math(name: str, py_name: str, arity: int = 1) -> Signature:
    params = tuple(Param(f"x{i}", Kind.SCALAR) for i in range(arity))
    return REGISTRY.register(
        "math",
        Signature(name=name, py_name=py_name, params=params, returns=Kind.SCALAR),
    )


# A small starter set of math functions.
for _n in ("sqrt", "abs", "exp", "log", "sin", "cos", "tan"):
    _reg_math(_n.capitalize() if _n != "abs" else "Abs", _n, arity=1)
_reg_math("Pow", "pow", arity=2)


# Convenience access -- lets callers hand-roll a Call for anything we haven't
# yet catalogued.
def make_call(fluent_name: str, *args, returns: Kind = Kind.SCALAR) -> Call:
    return Call(fluent_name, tuple(_coerce(a) for a in args), return_kind=returns)
