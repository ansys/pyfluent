# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""Typed, immutable, product-agnostic expression tree.

Nodes store neutral data only. In particular, a :class:`Variable` stores its
:class:`~ansys.units.variable_descriptor.VariableDescriptor`, not a
product-specific name. Product-specific details are supplied by a
:class:`~._dialect.Dialect` when the tree is rendered:

* :meth:`Expr.render` renders with an explicit dialect.
* ``str(expr)`` renders with the dialect the tree was built with (the first
  dialect found on a node of the tree), falling back to
  :data:`~._dialect.DEFAULT_DIALECT`.

Kinds
-----
Expression nodes carry a :class:`Kind` describing what they *produce*.
Parameter slots validate against that kind, so mismatches (for example a
:class:`VectorExpr` passed where a :class:`ScalarExpr` is expected) are caught
when the tree is built.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, ClassVar, TypeAlias

import ansys.units
from ansys.units.variable_descriptor import (
    VariableDescriptor,
    VectorVariableDescriptor,
)

from .errors import ExpressionBuildError

if TYPE_CHECKING:
    from ._dialect import Dialect


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


@dataclass(frozen=True, eq=False)
class Expr:
    """Abstract base for every expression tree node.

    Subclasses set the class attribute :attr:`kind` and implement
    :meth:`_render`. Composite nodes also override :meth:`children`.

    Parameters
    ----------
    dialect :
        Keyword-only. The dialect this node was built for, or ``None``.
        Used by ``str()`` when no dialect is passed explicitly.
    """

    kind: ClassVar[Kind]
    dialect: Dialect | None = field(default=None, kw_only=True, repr=False)

    # -- tree structure ---------------------------------------------------- #
    def children(self) -> tuple[Expr, ...]:
        """Return the direct child nodes of this node."""
        return ()

    def find_dialect(self) -> Dialect | None:
        """Return the first dialect set on this node or any descendant."""
        if self.dialect is not None:
            return self.dialect
        for child in self.children():
            found = child.find_dialect()
            if found is not None:
                return found
        return None

    # -- rendering --------------------------------------------------------- #
    def _render(self, dialect: Dialect) -> str:  # pragma: no cover - abstract
        raise NotImplementedError

    def render(self, dialect: Dialect | None = None) -> str:
        """Render this tree to an expression string.

        Parameters
        ----------
        dialect :
            Dialect to render with. Defaults to the dialect the tree was built
            with, or :data:`~._dialect.DEFAULT_DIALECT` if it has none.

        Raises
        ------
        ExpressionBuildError
            If a node cannot be represented in ``dialect``.
        """
        if dialect is None:
            dialect = self.find_dialect()
        if dialect is None:
            # Imported here because ``_dialect`` depends on this module.
            from ._dialect import DEFAULT_DIALECT

            dialect = DEFAULT_DIALECT
        return self._render(dialect)

    def __str__(self) -> str:
        return self.render()

    # -- settings-layer protocol ------------------------------------------- #
    #   Consumers (for example a settings API) can accept expression objects
    #   through these domain-neutral dunder methods without importing this
    #   package.
    def __settings_str__(self) -> str:
        """Render this node to the string a settings leaf stores."""
        return self.render()

    def __settings_kind__(self) -> str | None:
        """Return the neutral structural-kind tag (for example ``"scalar"``).

        The value mirrors :class:`Kind` (``scalar``, ``vector``, ``boolean``,
        ``quantity``, ``location_list``), so consumers can reject structurally
        incompatible assignments without importing this package. Returns
        ``None`` when the kind is unknown.
        """
        kind = getattr(self, "kind", None)
        return kind.value if isinstance(kind, Kind) else None

    def __settings_dimensions__(self) -> dict[str, float] | None:
        """Return physical dimensions as ``{base_dimension_name: exponent}``.

        Dimensions are only known for leaf nodes that carry units or a
        variable descriptor (see :class:`Quantity` and :class:`Variable`).
        Composite nodes return ``None`` so consumers can skip the dimensional
        check for them.
        """
        return None

    # -- operator overloading (scalar arithmetic) -------------------------- #
    #   These live on the base so that any subclass whose kind is compatible
    #   with arithmetic just works. A kind check happens inside _binop.
    def __add__(self, other: Operand) -> BinOp:
        return _binop(self, other, "+")

    def __radd__(self, other: Operand) -> BinOp:
        return _binop(other, self, "+")

    def __sub__(self, other: Operand) -> BinOp:
        return _binop(self, other, "-")

    def __rsub__(self, other: Operand) -> BinOp:
        return _binop(other, self, "-")

    def __mul__(self, other: Operand) -> BinOp:
        return _binop(self, other, "*")

    def __rmul__(self, other: Operand) -> BinOp:
        return _binop(other, self, "*")

    def __truediv__(self, other: Operand) -> BinOp:
        return _binop(self, other, "/")

    def __rtruediv__(self, other: Operand) -> BinOp:
        return _binop(other, self, "/")

    def __pow__(self, other: Operand) -> BinOp:
        return _binop(self, other, "**")

    def __neg__(self) -> UnaryOp:
        return UnaryOp("-", self, dialect=self.find_dialect())

    # -- comparisons produce Compare nodes --------------------------------- #
    def __lt__(self, other: Operand) -> Compare:
        return _cmp(self, other, "<")

    def __le__(self, other: Operand) -> Compare:
        return _cmp(self, other, "<=")

    def __gt__(self, other: Operand) -> Compare:
        return _cmp(self, other, ">")

    def __ge__(self, other: Operand) -> Compare:
        return _cmp(self, other, ">=")

    def __eq__(self, other: Operand) -> Compare:  # type: ignore[override]
        return _cmp(self, other, "==")

    def __ne__(self, other: Operand) -> Compare:  # type: ignore[override]
        return _cmp(self, other, "!=")

    # ``__eq__`` is overridden above, which would otherwise make instances
    # unhashable; nodes are hashable by identity so they can be put in sets.
    __hash__ = object.__hash__


Operand: TypeAlias = "Expr | VariableDescriptor | int | float"
"""Values accepted wherever an expression operand is expected."""


# --------------------------------------------------------------------------- #
# Marker mixins -- useful for type hints in parameter declarations            #
# --------------------------------------------------------------------------- #


class ScalarExpr(Expr):
    """Marker mixin for expression nodes that produce a scalar result."""

    kind = Kind.SCALAR


class VectorExpr(Expr):
    """Marker mixin for expression nodes that produce a vector result."""

    kind = Kind.VECTOR


class BooleanExpr(Expr):
    """Marker mixin for expression nodes that produce a boolean result."""

    kind = Kind.BOOLEAN


# --------------------------------------------------------------------------- #
# Leaf nodes                                                                  #
# --------------------------------------------------------------------------- #


def _dimension_names(dimensions: object) -> dict[str, float]:
    """Normalize a dimensions mapping to ``{base_dimension_name: exponent}``."""
    items = dict(dimensions).items()  # type: ignore[call-overload]
    return {getattr(k, "name", str(k)): float(v) for k, v in items if v}


@dataclass(frozen=True, eq=False)
class Literal(ScalarExpr):
    """A numeric literal (dimensionless)."""

    value: float | int

    def _render(self, dialect: Dialect) -> str:
        return repr(self.value)


@dataclass(frozen=True, eq=False)
class Quantity(Expr):
    """A value with units, rendered as ``<value> [<units>]``."""

    kind = Kind.QUANTITY
    value: float
    units: str

    def _render(self, dialect: Dialect) -> str:
        return f"{self.value} [{self.units}]"

    def __settings_dimensions__(self) -> dict[str, float] | None:
        """Derive physical dimensions from the units string.

        Any failure (for example an unknown unit) yields ``None`` so consumers
        skip the dimensional check rather than blocking the user.
        """
        try:
            dimensions = ansys.units.Quantity(self.value, self.units).dimensions
            return _dimension_names(dimensions)
        except Exception:
            return None


@dataclass(frozen=True, eq=False)
class Variable(ScalarExpr):
    """A field variable identified by a :class:`VariableDescriptor`.

    The rendered name comes from the dialect's naming strategy. When the node
    is created with a ``dialect``, an unsupported descriptor is rejected
    immediately; otherwise it is rejected when the tree is rendered.
    """

    descriptor: VariableDescriptor

    def __post_init__(self) -> None:
        if not isinstance(self.descriptor, VariableDescriptor):
            raise ExpressionBuildError(
                f"{self.descriptor!r} is not a VariableDescriptor."
            )
        if self.dialect is not None:
            self.dialect.variable_name(self.descriptor)

    def _render(self, dialect: Dialect) -> str:
        return dialect.variable_name(self.descriptor)

    def __settings_kind__(self) -> str | None:
        """Report the structural kind, distinguishing vector descriptors.

        :class:`Variable` inherits ``kind = Kind.SCALAR`` so the builder treats
        every catalog entry as a scalar operand. Vector descriptors report
        ``"vector"`` here so consumers can reject vector-to-scalar
        assignments without changing the builder's ``kind`` behavior.
        """
        if isinstance(self.descriptor, VectorVariableDescriptor):
            return Kind.VECTOR.value
        return super().__settings_kind__()

    def __settings_dimensions__(self) -> dict[str, float] | None:
        """Expose the descriptor's physical dimensions, when available.

        Keys are base-dimension names (``"MASS"``, ``"LENGTH"``, ...), matching
        :meth:`Quantity.__settings_dimensions__`. Returns ``None`` when the
        descriptor carries no usable dimension.
        """
        dimension = self.descriptor.dimension
        if not dimension:
            return None
        return _dimension_names(dimension)


@dataclass(frozen=True, eq=False)
class RawName(ScalarExpr):
    """Escape hatch: a raw identifier (for example a named expression).

    Prefer :class:`Variable` for catalog-backed field names.
    """

    name: str

    def _render(self, dialect: Dialect) -> str:
        return self.name


@dataclass(frozen=True, eq=False)
class LocationList(Expr):
    """A list of location names (surfaces, zones, ...), rendered as a list."""

    kind = Kind.LOCATION_LIST
    names: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not all(isinstance(n, str) and n for n in self.names):
            raise ExpressionBuildError(
                f"LocationList entries must be non-empty strings; got {self.names!r}"
            )

    def _render(self, dialect: Dialect) -> str:
        return "[" + ", ".join(f"'{n}'" for n in self.names) + "]"


# --------------------------------------------------------------------------- #
# Composite nodes                                                             #
# --------------------------------------------------------------------------- #


@dataclass(frozen=True, eq=False)
class UnaryOp(ScalarExpr):
    """A unary prefix operation, for example ``(-expr)``."""

    op: str
    operand: Expr

    def children(self) -> tuple[Expr, ...]:
        """Return the operand."""
        return (self.operand,)

    def _render(self, dialect: Dialect) -> str:
        return f"({self.op}{self.operand._render(dialect)})"


@dataclass(frozen=True, eq=False)
class BinOp(ScalarExpr):
    """A binary infix operation, for example ``(left + right)``."""

    op: str
    left: Expr
    right: Expr

    def children(self) -> tuple[Expr, ...]:
        """Return the left and right operands."""
        return (self.left, self.right)

    def _render(self, dialect: Dialect) -> str:
        return f"({self.left._render(dialect)} {self.op} {self.right._render(dialect)})"


@dataclass(frozen=True, eq=False)
class Compare(BooleanExpr):
    """A comparison that produces a boolean result, for example ``(a < b)``."""

    op: str
    left: Expr
    right: Expr

    def children(self) -> tuple[Expr, ...]:
        """Return the left and right operands."""
        return (self.left, self.right)

    def _render(self, dialect: Dialect) -> str:
        return f"({self.left._render(dialect)} {self.op} {self.right._render(dialect)})"


@dataclass(frozen=True, eq=False)
class Call(Expr):
    """Generic call node: ``name(arg1, arg2, ...)``.

    Used to render any registered function (reductions, math functions, ...).
    """

    name: str
    args: tuple[Expr, ...]
    return_kind: Kind = Kind.SCALAR

    @property  # type: ignore[override]
    def kind(self) -> Kind:  # noqa: D401
        """Return kind of the call's return value."""
        return self.return_kind

    def children(self) -> tuple[Expr, ...]:
        """Return the call arguments."""
        return self.args

    def _render(self, dialect: Dialect) -> str:
        args = ",".join(a._render(dialect) for a in self.args)
        return f"{self.name}({args})"


@dataclass(frozen=True, eq=False)
class KeywordArg(Expr):
    """A ``Keyword=value`` fragment inside a :class:`Call` argument list."""

    kind = Kind.SCALAR  # nominal; never used as an operand
    keyword: str
    value: Expr

    def children(self) -> tuple[Expr, ...]:
        """Return the argument value."""
        return (self.value,)

    def _render(self, dialect: Dialect) -> str:
        return f"{self.keyword}={self.value._render(dialect)}"


# --------------------------------------------------------------------------- #
# Coercion helpers                                                            #
# --------------------------------------------------------------------------- #


_SCALAR_KINDS = {Kind.SCALAR, Kind.QUANTITY}


def _coerce(value: object, dialect: Dialect | None = None) -> Expr:
    """Coerce a Python value into an :class:`Expr` if possible."""
    if isinstance(value, Expr):
        return value
    if isinstance(value, (int, float)):
        return Literal(value, dialect=dialect)
    if isinstance(value, VariableDescriptor):
        return Variable(value, dialect=dialect)
    raise ExpressionBuildError(
        f"Cannot use {value!r} (type {type(value).__name__}) as an expression."
    )


def common_dialect(*exprs: Expr) -> Dialect | None:
    """Return the single dialect used by ``exprs``, or ``None`` if they have none.

    Raises
    ------
    ExpressionBuildError
        If the expressions were built for different dialects.
    """
    found: Dialect | None = None
    for expr in exprs:
        dialect = expr.find_dialect()
        if dialect is None:
            continue
        if found is not None and dialect is not found:
            raise ExpressionBuildError(
                f"Cannot combine expressions from the {found.name!r} and "
                f"{dialect.name!r} dialects."
            )
        found = dialect
    return found


def _binop(a: object, b: object, op: str) -> BinOp:
    """Build a :class:`BinOp` node, coercing operands and checking kinds.

    Raises
    ------
    ExpressionBuildError
        If either operand is not a scalar-compatible kind.
    """
    ea, eb = _coerce(a), _coerce(b)
    for side, e in (("left", ea), ("right", eb)):
        if e.kind not in _SCALAR_KINDS:
            raise ExpressionBuildError(
                f"Operator {op!r} requires scalar operands; "
                f"{side} operand is a {e.kind.value}.",
                node=e,
                slot=side,
            )
    return BinOp(op, ea, eb, dialect=common_dialect(ea, eb))


def _cmp(a: object, b: object, op: str) -> Compare:
    ea, eb = _coerce(a), _coerce(b)
    return Compare(op, ea, eb, dialect=common_dialect(ea, eb))


def coerce_location_list(value: object) -> LocationList:
    """Coerce a list/tuple of strings (or an existing LocationList) into one.

    Raises
    ------
    ExpressionBuildError
        If ``value`` is a bare string or cannot be interpreted as a sequence of
        location names.
    """
    if isinstance(value, LocationList):
        return value
    if isinstance(value, str):
        raise ExpressionBuildError(
            "locations must be a sequence of strings, not a single string."
        )
    if isinstance(value, Sequence):
        return LocationList(tuple(value))  # type: ignore[arg-type]
    raise ExpressionBuildError(f"Cannot use {value!r} as a LocationList.")
