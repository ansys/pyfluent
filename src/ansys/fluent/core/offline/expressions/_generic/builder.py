# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""User-facing expression builder facade.

Exposes :class:`ExpressionBuilder`, a thin, discoverable wrapper over a
dialect's :class:`~._registry.FunctionRegistry`:

* ``builder.<group>.<function>(...)`` (for example
  ``builder.reductions.area_ave(expression=..., locations=...)``) returns an
  AST :class:`~._ast.Call` node ready to be composed further.
* ``builder.<group>.<function>.<param>.allowed_values()`` queries the attached
  :class:`~._discovery.Discovery` for legal values.
* ``builder.variable(V.TEMPERATURE)`` and ``builder.literal(1.5)`` build
  leaf nodes.
"""

from __future__ import annotations

from collections.abc import Sequence

from ansys.units.variable_descriptor import VariableDescriptor

from ._ast import (
    Call,
    Expr,
    Literal,
    LocationList,
    Quantity,
    RawName,
    Variable,
    coerce_location_list,
)
from ._dialect import DEFAULT_DIALECT, Dialect
from ._discovery import Discovery, StaticDiscovery
from ._parser import parse as _parse
from ._registry import Signature
from ._slots import SlotAccessor, make_slot


class FunctionGroup:
    """Attribute-style access to one group of registered signatures."""

    def __init__(self, group: str, dialect: Dialect, discovery: Discovery) -> None:
        self._group = group
        self._sigs = dialect.functions.group(group)
        self._dialect = dialect
        self._discovery = discovery

    def __dir__(self) -> list[str]:
        return sorted(list(self._sigs) + list(super().__dir__()))

    def __getattr__(self, item: str) -> FunctionInvoker:
        sigs = self.__dict__.get("_sigs", {})
        try:
            sig = sigs[item]
        except KeyError as exc:
            raise AttributeError(
                f"No {self.__dict__.get('_group')!r} named {item!r}. "
                f"Available: {sorted(sigs)}"
            ) from exc
        return FunctionInvoker(sig, self._dialect, self._discovery)

    def available(self) -> list[str]:
        """List the Python-side names of registered functions in this group."""
        return sorted(self._sigs)


class FunctionInvoker:
    """Callable wrapper for a :class:`Signature`.

    Alongside invocation it exposes:

    * ``inv.<param>`` -- a :class:`SlotAccessor` for per-slot discovery.
    * ``inv.signature`` / ``inv.params()`` -- introspection.
    """

    def __init__(self, sig: Signature, dialect: Dialect, discovery: Discovery) -> None:
        self._sig = sig
        self._dialect = dialect
        self._slots: dict[str, SlotAccessor] = {
            p.name: make_slot(p, discovery) for p in sig.params
        }

    def __call__(self, *args: object, **kwargs: object) -> Call:
        return self._sig.build_for(self._dialect, args, kwargs)

    def __getattr__(self, item: str) -> SlotAccessor:
        slots = self.__dict__.get("_slots", {})
        if item in slots:
            return slots[item]
        raise AttributeError(
            f"{self._sig.py_name!r} has no parameter {item!r}. "
            f"Available: {list(slots)}"
        )

    def __dir__(self) -> list[str]:
        return sorted(list(super().__dir__()) + list(self._slots))

    @property
    def signature(self) -> Signature:
        """The underlying :class:`~._registry.Signature` for this invoker."""
        return self._sig

    def params(self) -> list[str]:
        """Return the parameter names for this signature."""
        return [p.name for p in self._sig.params]

    def __repr__(self) -> str:
        params = ", ".join(f"{p.name}: {p.kind.value}" for p in self._sig.params)
        return (
            f"<{self._sig.py_name}({params}) "
            f"-> {self._sig.returns.value} | {self._dialect.name}={self._sig.name!r}>"
        )


# --------------------------------------------------------------------------- #
# Public builder                                                              #
# --------------------------------------------------------------------------- #


class ExpressionBuilder:
    """Entry point for constructing expression trees.

    Function groups registered in the dialect are exposed as attributes, for
    example ``builder.math.sqrt(x)``.

    Parameters
    ----------
    dialect : optional
        Dialect that supplies variable naming and functions. Defaults to
        :data:`~._dialect.DEFAULT_DIALECT`.
    discovery : optional
        Source of legal values for per-parameter slots. Defaults to a
        permissive :class:`~._discovery.StaticDiscovery`.
    """

    def __init__(
        self,
        dialect: Dialect | None = None,
        discovery: Discovery | None = None,
    ) -> None:
        self._dialect = dialect or DEFAULT_DIALECT
        self._discovery = discovery or StaticDiscovery(self._dialect)
        self._groups = {
            group: FunctionGroup(group, self._dialect, self._discovery)
            for group in self._dialect.functions.groups()
        }

    def __getattr__(self, item: str) -> FunctionGroup:
        groups = self.__dict__.get("_groups", {})
        if item in groups:
            return groups[item]
        raise AttributeError(
            f"{type(self).__name__!r} object has no attribute {item!r}. "
            f"Function groups: {sorted(groups)}"
        )

    def __dir__(self) -> list[str]:
        return sorted(list(super().__dir__()) + list(self._groups))

    # -- leaf constructors ------------------------------------------------- #

    def literal(self, value: float | int) -> Literal:
        """Build a numeric literal node."""
        return Literal(value, dialect=self._dialect)

    def quantity(self, value: float, units: str) -> Quantity:
        """Build a value-with-units node (for example ``5 [m/s]``)."""
        return Quantity(value, units, dialect=self._dialect)

    def variable(self, descriptor: VariableDescriptor) -> Variable:
        """Build a field variable node from a ``VariableCatalog`` entry.

        Raises
        ------
        ExpressionBuildError
            If the dialect cannot name ``descriptor``.
        """
        return Variable(descriptor, dialect=self._dialect)

    def raw(self, name: str) -> RawName:
        """Build a raw-identifier node (for example a named expression name).

        Escape hatch. Prefer :meth:`variable` for catalog-backed fields.
        """
        return RawName(name, dialect=self._dialect)

    def locations(self, names: Sequence[str]) -> LocationList:
        """Build a :class:`LocationList` from a sequence of strings."""
        return coerce_location_list(names)

    # -- discovery / convenience ------------------------------------------ #

    @property
    def dialect(self) -> Dialect:
        """The dialect this builder builds for."""
        return self._dialect

    @property
    def discovery(self) -> Discovery:
        """The underlying :class:`~._discovery.Discovery` object (advanced use)."""
        return self._discovery

    def location_names(self) -> list[str]:
        """All location names visible via the attached discovery."""
        return self._discovery.location_names()

    def named_expression_names(self) -> list[str]:
        """All in-scope named expressions visible via the attached discovery."""
        return self._discovery.named_expression_names()

    def variables(self) -> list[VariableDescriptor]:
        """Every :class:`VariableDescriptor` available via the attached discovery."""
        return self._discovery.variable_descriptors()

    def render(self, expr: Expr) -> str:
        """Render an expression tree with this builder's dialect."""
        return expr.render(self._dialect)

    def parse(self, text: str) -> Expr:
        """Parse an expression string with this builder's dialect.

        Round-trips with :meth:`render`::

            b.render(b.parse(s)) == s  # for canonical builder output
        """
        return _parse(text, self._dialect)
