# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""Declarative function signatures and an empty, populatable registry.

Each :class:`Signature` describes a function callable from expressions: its
product-side name, the kinds and order of its parameters, and its return kind.
A :class:`FunctionRegistry` groups signatures (for example ``"reductions"`` or
``"math"``) and drives both the user-facing builder
(:class:`~.builder.ExpressionBuilder`) and the parser.

No functions are registered here: every product supplies its own registry
through its :class:`~._dialect.Dialect`.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING

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

if TYPE_CHECKING:
    from ._dialect import Dialect

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
        argument list (for example ``Weight=Area``).
    allowed_literals :
        When set, restricts values to the given literals (an :class:`Enum`
        class or an iterable of values). The value is rendered as a raw,
        unquoted token.
    """

    name: str
    kind: Kind
    optional: bool = False
    keyword: str | None = None
    allowed_literals: type[Enum] | Iterable[object] | None = field(
        default=None, compare=False
    )

    def coerce(self, value: object, dialect: Dialect | None = None) -> Expr | None:
        """Validate and coerce ``value`` to an :class:`~._ast.Expr` for this parameter.

        Raises
        ------
        ExpressionBuildError
            If ``value`` is missing for a required parameter or fails kind/literal
            validation.
        """
        if value is None:
            if self.optional:
                return None
            raise ExpressionBuildError(f"Missing required argument {self.name!r}.")

        if self.allowed_literals is not None:
            token = self._validate_literal(value)
            arg: Expr = RawName(token, dialect=dialect)
        elif self.kind is Kind.LOCATION_LIST:
            arg = coerce_location_list(value)
        else:
            arg = _coerce(value, dialect)
            if not _kind_compatible(arg.kind, self.kind):
                raise ExpressionBuildError(
                    f"Parameter {self.name!r} expects {self.kind.value}, "
                    f"got {arg.kind.value}.",
                    slot=self.name,
                )

        if self.keyword is not None:
            return KeywordArg(self.keyword, arg, dialect=dialect)
        return arg

    def _validate_literal(self, value: object) -> str:
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
        allowed_list = list(allowed or ())
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
    """Describes a function callable from expressions."""

    name: str  # product-side name, for example "AreaAve"
    py_name: str  # Python-side snake_case, for example "area_ave"
    params: tuple[Param, ...]
    returns: Kind = Kind.SCALAR

    def build(self, *args: object, **kwargs: object) -> Call:
        """Bind arguments and return a :class:`~._ast.Call` node."""
        return self.build_for(None, args, kwargs)

    def build_for(
        self,
        dialect: Dialect | None,
        args: tuple[object, ...],
        kwargs: dict[str, object],
    ) -> Call:
        """Bind arguments and return a :class:`~._ast.Call` built for ``dialect``."""
        bound = self._bind(args, kwargs)
        rendered: list[Expr] = []
        for p, v in zip(self.params, bound):
            if v is None and p.optional:
                continue
            coerced = p.coerce(v, dialect)
            if coerced is not None:
                rendered.append(coerced)
        return Call(self.name, tuple(rendered), self.returns, dialect=dialect)

    def _bind(
        self, args: tuple[object, ...], kwargs: dict[str, object]
    ) -> list[object]:
        if len(args) > len(self.params):
            raise ExpressionBuildError(
                f"{self.py_name}() takes {len(self.params)} positional "
                f"args at most, got {len(args)}."
            )
        result: list[object] = [None] * len(self.params)
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


class FunctionRegistry:
    """Named groups of :class:`Signature` objects."""

    def __init__(self) -> None:
        self._by_group: dict[str, dict[str, Signature]] = {}
        self._by_name: dict[str, Signature] = {}

    def register(self, group: str, sig: Signature) -> Signature:
        """Register ``sig`` under ``group`` and return it."""
        self._by_group.setdefault(group, {})[sig.py_name] = sig
        self._by_name[sig.name] = sig
        return sig

    def group(self, name: str) -> dict[str, Signature]:
        """Return a copy of the signatures registered under ``name``."""
        return dict(self._by_group.get(name, {}))

    def groups(self) -> tuple[str, ...]:
        """Return the names of all registered groups."""
        return tuple(self._by_group)

    def find(self, name: str) -> Signature | None:
        """Return the signature with product-side ``name``, or ``None``."""
        return self._by_name.get(name)


# --------------------------------------------------------------------------- #
# Convenience: hand-roll a Call for anything not (yet) in a registry.         #
# --------------------------------------------------------------------------- #


def make_call(
    name: str,
    *args: object,
    returns: Kind = Kind.SCALAR,
    dialect: Dialect | None = None,
) -> Call:
    """Build a :class:`~._ast.Call` node for a function not in any registry."""
    return Call(
        name,
        tuple(_coerce(a, dialect) for a in args),
        returns,
        dialect=dialect,
    )
