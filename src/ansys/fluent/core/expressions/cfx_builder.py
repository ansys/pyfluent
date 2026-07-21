# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""CFX (CEL) expression builder.

A first cut at reusing the generic pieces of the expression package to
target ANSYS CFX's expression language (CEL) instead of Fluent's.  The
two languages share:

* arithmetic / comparison operators,
* a small set of scalar math functions,
* value-with-units quantity syntax (``5 [m s^-1]``),

but differ in reductions: CFX uses a ``name(expr)@location`` postfix
instead of Fluent's list-argument form ``Name(expr,['loc'])``.

Only a small, illustrative subset of CEL is wired here to prove the
split; extending the registry is a one-line change per function.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ansys.units import VariableCatalog as V
from ansys.units.variable_descriptor import VariableDescriptor

from ._ast import (
    Expr,
    Kind,
    Literal,
    Quantity,
    RawName,
    ScalarExpr,
)
from ._registry import Param
from .errors import ExpressionBuildError

# --------------------------------------------------------------------------- #
# Naming (tiny built-in map; real CFX naming strategy TBD)                    #
# --------------------------------------------------------------------------- #

_CFX_VAR_NAMES: dict[VariableDescriptor, str] = {
    V.ABSOLUTE_PRESSURE: "Absolute Pressure",
    V.TEMPERATURE: "Temperature",
    V.VELOCITY: "Velocity",
}


# --------------------------------------------------------------------------- #
# CFX-specific AST nodes                                                      #
# --------------------------------------------------------------------------- #


@dataclass(frozen=True, eq=False)
class CfxVariable(ScalarExpr):
    """A CFX field variable (rendered using the CFX naming map)."""

    descriptor: VariableDescriptor

    def __post_init__(self):
        if self.descriptor not in _CFX_VAR_NAMES:
            raise ExpressionBuildError(
                f"VariableCatalog entry {self.descriptor!r} has no CFX "
                f"expression name registered."
            )

    def __fluent_expr__(self) -> str:  # naming inherited from base; renders CFX
        return _CFX_VAR_NAMES[self.descriptor]


@dataclass(frozen=True, eq=False)
class CfxCall(Expr):
    """A CFX call, optionally with a ``@location`` postfix.

    ``areaAve(Pressure)@inlet1`` -> ``CfxCall("areaAve", (Var,), "inlet1")``.
    Math calls without a location render as plain ``sqrt(x)``.
    """

    name: str
    args: tuple[Expr, ...]
    location: str | None = None
    return_kind: Kind = Kind.SCALAR

    @property  # type: ignore[override]
    def kind(self) -> Kind:  # noqa: D401
        """Return kind of the call's return value."""
        return self.return_kind

    def __fluent_expr__(self) -> str:
        body = f"{self.name}(" + ", ".join(str(a) for a in self.args) + ")"
        return f"{body}@{self.location}" if self.location else body


# --------------------------------------------------------------------------- #
# Signature / registry (CFX flavour)                                          #
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class CfxSignature:
    """Describes a CFX-side callable.

    ``with_location`` indicates that the callable is a reduction and
    requires a ``location=`` keyword at call-time, which renders as a
    ``@<location>`` postfix.
    """

    name: str
    py_name: str
    params: tuple[Param, ...] = ()
    with_location: bool = False
    returns: Kind = Kind.SCALAR

    def build(self, *args, location: str | None = None, **kwargs) -> CfxCall:
        """Bind arguments and return a :class:`CfxCall` node.

        Raises
        ------
        ExpressionBuildError
            If ``value`` is missing for a required parameter or fails kind/literal
            validation.
        """
        if self.with_location and not isinstance(location, str):
            raise ExpressionBuildError(
                f"{self.py_name}() requires a string 'location=' argument."
            )
        if not self.with_location and location is not None:
            raise ExpressionBuildError(
                f"{self.py_name}() does not accept a 'location=' argument."
            )

        if len(args) > len(self.params):
            raise ExpressionBuildError(
                f"{self.py_name}() takes {len(self.params)} positional "
                f"args at most, got {len(args)}."
            )
        bound: list[Any] = [None] * len(self.params)
        for i, v in enumerate(args):
            bound[i] = v
        by_name = {p.name: i for i, p in enumerate(self.params)}
        for k, v in kwargs.items():
            if k not in by_name:
                raise ExpressionBuildError(
                    f"{self.py_name}() got unexpected keyword {k!r}."
                )
            if bound[by_name[k]] is not None:
                raise ExpressionBuildError(
                    f"{self.py_name}() got multiple values for {k!r}."
                )
            bound[by_name[k]] = v

        # Promote raw VariableDescriptors to CfxVariable so the generic
        # _coerce path in Param.coerce doesn't wrap them as Fluent Variables.
        # Alternative "Option A" approach — cleaner long-term: parameterize _coerce
        # with a "descriptor factory" so each backend chooses its Variable class.
        # Roughly:
        """
        _variable_factory = Variable  # default (Fluent)

        def _coerce(value, *, variable_factory=None) -> Expr:
            factory = variable_factory or _variable_factory
            ...
            if isinstance(value, VariableDescriptor):
                return factory(value)
            ...
        """
        # …and thread variable_factory=CfxVariable through Param.coerce / Signature.build.
        # Bigger change; better fit for the eventual framework/backend split.
        # Recommended for now: Option A — one small patch inside CfxSignature.build, no
        # cross-package edits, and test_comparison_produces_boolean_expr (and any other
        # reduction-with-descriptor test) will render "Absolute Pressure" correctly.
        # When we do the framework refactor, replace it with Option A. Option B for now:
        for i, v in enumerate(bound):
            if isinstance(v, VariableDescriptor):
                bound[i] = CfxVariable(v)
        # End of "Option B" code for handling VariableDescriptors in CFX signatures.

        rendered: list[Expr] = []
        for p, v in zip(self.params, bound):
            coerced = p.coerce(v)  # reuse the generic Param coercion
            if coerced is not None:
                rendered.append(coerced)
        return CfxCall(
            self.name, tuple(rendered), location=location, return_kind=self.returns
        )


class _CfxRegistry:
    def __init__(self):
        """Initialize the CFX registry."""
        self._by_group: dict[str, dict[str, CfxSignature]] = {}

    def register(self, group: str, sig: CfxSignature) -> CfxSignature:
        """Register a CFX signature under a specific group."""
        self._by_group.setdefault(group, {})[sig.py_name] = sig
        return sig

    def group(self, name: str) -> dict[str, CfxSignature]:
        """Retrieve all signatures for a given group."""
        return dict(self._by_group.get(name, {}))

    def groups(self) -> tuple[str, ...]:
        """Return a tuple of all registered group names."""
        return tuple(self._by_group)


CFX_REGISTRY = _CfxRegistry()


def _cfx_reduction(
    name: str, py_name: str, *, with_expr: bool = True, returns: Kind = Kind.SCALAR
) -> CfxSignature:
    params = (Param("expression", Kind.SCALAR),) if with_expr else ()
    return CFX_REGISTRY.register(
        "reductions",
        CfxSignature(
            name=name,
            py_name=py_name,
            params=params,
            with_location=True,
            returns=returns,
        ),
    )


# Scalar reductions (expression + @location).
_cfx_reduction("areaAve", "area_ave")
_cfx_reduction("areaInt", "area_int")
_cfx_reduction("volumeAve", "volume_ave")
_cfx_reduction("volumeInt", "volume_int")
_cfx_reduction("massFlowAve", "mass_flow_ave")
_cfx_reduction("massFlowInt", "mass_flow_int")
_cfx_reduction("minVal", "minimum")
_cfx_reduction("maxVal", "maximum")

# Extent-only reductions (@location only).
_cfx_reduction("area", "area", with_expr=False)
_cfx_reduction("volume", "volume", with_expr=False)
_cfx_reduction("massFlow", "mass_flow", with_expr=False)


def _cfx_math(name: str, arity: int = 1) -> CfxSignature:
    params = tuple(Param(f"x{i}", Kind.SCALAR) for i in range(arity))
    return CFX_REGISTRY.register(
        "math",
        CfxSignature(name=name, py_name=name, params=params, returns=Kind.SCALAR),
    )


for _n in ("sqrt", "abs", "exp", "ln", "log10", "sin", "cos", "tan"):
    _cfx_math(_n, 1)
for _n in ("min", "max", "pow"):
    _cfx_math(_n, 2)


# --------------------------------------------------------------------------- #
# Facade                                                                      #
# --------------------------------------------------------------------------- #


class _CfxGroupFacade:
    """Attribute-style access to one group of CFX signatures."""

    def __init__(self, group: str):
        self._group = group
        self._sigs = CFX_REGISTRY.group(group)

    def __dir__(self):
        return sorted(list(self._sigs) + list(super().__dir__()))

    def __getattr__(self, item: str):
        try:
            sig = self._sigs[item]
        except KeyError as exc:
            raise AttributeError(
                f"No {self._group!r} named {item!r}. "
                f"Available: {sorted(self._sigs)}"
            ) from exc
        return _CfxSigInvoker(sig)

    def available(self) -> list[str]:
        """List the Python-side names of registered functions in this group."""
        return sorted(self._sigs)


class _CfxSigInvoker:
    """Callable wrapper for a :class:`CfxSignature`."""

    def __init__(self, sig: CfxSignature):
        self._sig = sig

    def __call__(self, *args, **kwargs) -> CfxCall:
        return self._sig.build(*args, **kwargs)

    @property
    def signature(self) -> CfxSignature:
        """The underlying :class:`CfxSignature` for this invoker."""
        return self._sig

    def params(self) -> list[str]:
        """Return the parameter names for this signature."""
        return [p.name for p in self._sig.params]

    def __repr__(self):
        params = ", ".join(f"{p.name}: {p.kind.value}" for p in self._sig.params)
        loc = ", location: str" if self._sig.with_location else ""
        sep = ", " if params and loc else ""
        return (
            f"<{self._sig.py_name}({params}{sep}{loc.lstrip(', ')}) "
            f"-> {self._sig.returns.value} | cfx={self._sig.name!r}>"
        )


class CfxExpressionBuilder:
    """Entry point for constructing CFX (CEL) expression trees.

    Discoverable in the same way as :class:`ExpressionBuilder`::

        b = CfxExpressionBuilder()
        dp = (
            b.reductions.area_ave(expression=V.ABSOLUTE_PRESSURE, location="inlet1")
            - b.reductions.area_ave(expression=V.ABSOLUTE_PRESSURE, location="outlet")
        )
        str(dp)
        # '(areaAve(Absolute Pressure)@inlet1 - areaAve(Absolute Pressure)@outlet)'

    No live discovery yet -- there is no CFX-side field_info equivalent
    wired in.  Surface / variable validation is currently limited to the
    hard-coded CFX naming map and the generic AST kind checks.
    """

    def __init__(self):
        for group in CFX_REGISTRY.groups():
            setattr(self, group, _CfxGroupFacade(group))

    # -- leaf constructors ------------------------------------------------ #

    @staticmethod
    def literal(value: float | int) -> Literal:
        """Build a numeric literal node."""
        return Literal(value)

    @staticmethod
    def quantity(value: float, units: str) -> Quantity:
        """Build a value-with-units node (e.g. ``5 [m s^-1]``)."""
        return Quantity(value, units)

    @staticmethod
    def variable(descriptor: VariableDescriptor) -> CfxVariable:
        """Build a CFX field variable node from a ``VariableCatalog`` entry."""
        return CfxVariable(descriptor)

    @staticmethod
    def raw(name: str) -> RawName:
        """Build a raw-identifier node (escape hatch)."""
        return RawName(name)

    @staticmethod
    def render(expr: Expr) -> str:
        """Render an expression tree to its CFX-side string form."""
        return expr.__fluent_expr__()
