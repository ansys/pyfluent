# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""Layer 2: typed, immutable AST for Fluent expressions.

Every node knows how to render itself to a Fluent expression string via
:meth:`Expr.__fluent_expr__` (also exposed through ``__str__``).

Kinds
-----
Expression nodes carry a :class:`Kind` describing what they *produce*.
That kind is what parameter slots in Layer 1 validate against, so slot
mismatches (e.g. handing a :class:`VectorExpr` to a slot that wants a
:class:`ScalarExpr`) are caught at build time -- not by Fluent complaining
downstream.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Sequence

from ansys.units.variable_descriptor import VariableDescriptor

from ansys.fluent.core.variable_strategies import FluentExprNamingStrategy

from .errors import ExpressionBuildError

_NAMING = FluentExprNamingStrategy()


class Kind(Enum):
    """Return kind of an expression node."""

    SCALAR = "scalar"
    VECTOR = "vector"
    BOOLEAN = "boolean"
    LOCATION_LIST = "location_list"
    QUANTITY = "quantity"  # scalar with units, e.g. 5 [m/s]


# --------------------------------------------------------------------------- #
# Base class                                                                  #
# --------------------------------------------------------------------------- #


class Expr:
    """Abstract base for every expression tree node.

    Subclasses must set the class attribute :attr:`kind` and implement
    :meth:`__fluent_expr__`.
    """

    kind: Kind

    # -- rendering --------------------------------------------------------- #
    def __fluent_expr__(self) -> str:  # pragma: no cover - abstract
        raise NotImplementedError

    def __str__(self) -> str:
        return self.__fluent_expr__()

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.__fluent_expr__()!r}>"

    # -- operator overloading (scalar arithmetic) -------------------------- #
    #   These live on the base so that any subclass whose kind is compatible
    #   with arithmetic just works.  A kind-check happens inside _binop.
    def __add__(self, other):  return _binop(self, other, "+")
    def __radd__(self, other): return _binop(other, self, "+")
    def __sub__(self, other):  return _binop(self, other, "-")
    def __rsub__(self, other): return _binop(other, self, "-")
    def __mul__(self, other):  return _binop(self, other, "*")
    def __rmul__(self, other): return _binop(other, self, "*")
    def __truediv__(self, other):  return _binop(self, other, "/")
    def __rtruediv__(self, other): return _binop(other, self, "/")
    def __pow__(self, other):  return _binop(self, other, "**")
    def __neg__(self):         return UnaryOp("-", _coerce(self))

    # -- comparisons produce BooleanExpr ----------------------------------- #
    def __lt__(self, other): return _cmp(self, other, "<")
    def __le__(self, other): return _cmp(self, other, "<=")
    def __gt__(self, other): return _cmp(self, other, ">")
    def __ge__(self, other): return _cmp(self, other, ">=")
    def __eq__(self, other): return _cmp(self, other, "==")
    def __ne__(self, other): return _cmp(self, other, "!=")

    # dataclasses set __hash__ to None when __eq__ is defined; we need nodes
    # hashable by identity so users can put them into sets during traversal.
    __hash__ = object.__hash__


# --------------------------------------------------------------------------- #
# Marker mixins -- useful for type hints in Layer 1 param declarations        #
# --------------------------------------------------------------------------- #


class ScalarExpr(Expr):
    kind = Kind.SCALAR


class VectorExpr(Expr):
    kind = Kind.VECTOR


class BooleanExpr(Expr):
    kind = Kind.BOOLEAN


# --------------------------------------------------------------------------- #
# Leaf nodes                                                                  #
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class Literal(ScalarExpr):
    """A numeric literal (dimensionless)."""

    value: float | int

    def __fluent_expr__(self) -> str:
        return repr(self.value)


@dataclass(frozen=True)
class Quantity(Expr):
    """A value with units, rendered as ``<value> [<units>]``."""

    kind = Kind.QUANTITY
    value: float
    units: str

    def __fluent_expr__(self) -> str:
        return f"{self.value} [{self.units}]"


@dataclass(frozen=True)
class Variable(ScalarExpr):
    """A Fluent field variable.

    Constructed from a :class:`VariableDescriptor` (from the shared
    ``ansys.units`` catalog) and mapped via :class:`FluentExprNamingStrategy`
    so we use exactly the same source of truth as the reduction API.
    """

    descriptor: VariableDescriptor

    def __post_init__(self):
        # Fail fast if the descriptor isn't in the naming map. The strategy
        # raises ValueError for unsupported descriptors; anything else (e.g.
        # a completely bogus object) surfaces as AttributeError/TypeError.
        try:
            name = _NAMING.to_string(self.descriptor)
        except (ValueError, AttributeError, TypeError) as exc:
            raise ExpressionBuildError(
                f"VariableCatalog entry {self.descriptor!r} has no Fluent "
                f"expression name in FluentExprNamingStrategy."
            ) from exc
        if not isinstance(name, str):
            raise ExpressionBuildError(
                f"VariableCatalog entry {self.descriptor!r} has no Fluent "
                f"expression name in FluentExprNamingStrategy."
            )
        object.__setattr__(self, "_fluent_name", name)

    def __fluent_expr__(self) -> str:
        return self._fluent_name  # type: ignore[attr-defined]


@dataclass(frozen=True)
class RawName(ScalarExpr):
    """Escape hatch: a raw identifier (e.g. a named expression).

    Prefer :class:`Variable` for catalog-backed field names.
    """

    name: str

    def __fluent_expr__(self) -> str:
        return self.name


@dataclass(frozen=True)
class LocationList(Expr):
    """A list of Fluent surface / zone names, rendered as a Python-style list."""

    kind = Kind.LOCATION_LIST
    names: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self):
        if not all(isinstance(n, str) and n for n in self.names):
            raise ExpressionBuildError(
                f"LocationList entries must be non-empty strings; got {self.names!r}"
            )

    def __fluent_expr__(self) -> str:
        # Matches Fluent's expected form, e.g. ['inlet1', 'inlet2']
        return "[" + ", ".join(f"'{n}'" for n in self.names) + "]"


# --------------------------------------------------------------------------- #
# Composite nodes                                                             #
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class UnaryOp(ScalarExpr):
    op: str
    operand: Expr

    def __fluent_expr__(self) -> str:
        return f"({self.op}{self.operand})"


@dataclass(frozen=True)
class BinOp(ScalarExpr):
    op: str
    left: Expr
    right: Expr

    def __fluent_expr__(self) -> str:
        return f"({self.left} {self.op} {self.right})"


@dataclass(frozen=True)
class Compare(BooleanExpr):
    op: str
    left: Expr
    right: Expr

    def __fluent_expr__(self) -> str:
        return f"({self.left} {self.op} {self.right})"


@dataclass(frozen=True)
class Call(Expr):
    """Generic call node: ``name(arg1, arg2, ...)``.

    Used to render any Layer 1 registered function (reductions, math funcs).
    """

    name: str
    args: tuple[Expr, ...]
    return_kind: Kind = Kind.SCALAR

    # dataclass-safe kind override
    @property  # type: ignore[override]
    def kind(self) -> Kind:  # noqa: D401
        return self.return_kind

    def __fluent_expr__(self) -> str:
        return f"{self.name}(" + ",".join(str(a) for a in self.args) + ")"


# --------------------------------------------------------------------------- #
# Coercion helpers                                                            #
# --------------------------------------------------------------------------- #


_SCALAR_KINDS = {Kind.SCALAR, Kind.QUANTITY}


def _coerce(value) -> Expr:
    """Coerce a Python value into an :class:`Expr` if possible."""
    if isinstance(value, Expr):
        return value
    if isinstance(value, (int, float)):
        return Literal(value)
    if isinstance(value, VariableDescriptor):
        return Variable(value)
    raise ExpressionBuildError(
        f"Cannot use {value!r} (type {type(value).__name__}) as an expression."
    )


def _binop(a, b, op: str) -> BinOp:
    ea, eb = _coerce(a), _coerce(b)
    for side, e in (("left", ea), ("right", eb)):
        if e.kind not in _SCALAR_KINDS:
            raise ExpressionBuildError(
                f"Operator {op!r} requires scalar operands; "
                f"{side} operand is a {e.kind.value}.",
                node=e,
                slot=side,
            )
    return BinOp(op, ea, eb)


def _cmp(a, b, op: str) -> Compare:
    ea, eb = _coerce(a), _coerce(b)
    return Compare(op, ea, eb)


def coerce_location_list(value) -> LocationList:
    """Coerce a list/tuple of strings (or an existing LocationList) into one."""
    if isinstance(value, LocationList):
        return value
    if isinstance(value, str):
        raise ExpressionBuildError(
            "locations must be a sequence of strings, not a single string."
        )
    if isinstance(value, Sequence):
        return LocationList(tuple(value))
    raise ExpressionBuildError(
        f"Cannot use {value!r} as a LocationList."
    )
