# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""Layer 3: user-facing expression builder facade.

Exposes :class:`ExpressionBuilder`, the entry point users interact with.
The builder is a thin, discoverable wrapper over the Layer 1 registry:

* ``builder.reductions.area_ave(expression=..., locations=...)`` returns an
  AST :class:`~._ast.Call` node ready to be composed further.
* ``builder.reductions.area_ave.locations.allowed_values()`` queries the
  attached settings tree for legal surface names.
* ``builder.variable(V.TEMPERATURE)`` and ``builder.literal(1.5)`` build
  leaf nodes.
"""

from __future__ import annotations

from typing import Any

from ansys.units.variable_descriptor import VariableDescriptor

from ._ast import (
    Expr,
    Literal,
    LocationList,
    Quantity,
    RawName,
    Variable,
    coerce_location_list,
)
from ._discovery import Discovery
from ._registry import REGISTRY, Signature
from ._slots import SlotAccessor, make_slot


class _GroupFacade:
    """Attribute-style access to one group of registered signatures."""

    def __init__(self, group: str, discovery: Discovery):
        self._group = group
        self._sigs = REGISTRY.group(group)
        self._discovery = discovery

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
        return _SigInvoker(sig, self._discovery)

    def available(self) -> list[str]:
        """List the Python-side names of registered functions in this group."""
        return sorted(self._sigs)


class _SigInvoker:
    """Callable wrapper for a :class:`Signature`.

    Alongside invocation it exposes:

    * ``inv.<param>`` -- a :class:`SlotAccessor` for per-slot discovery.
    * ``inv.signature`` / ``inv.params()`` -- introspection.
    """

    def __init__(self, sig: Signature, discovery: Discovery):
        self._sig = sig
        self._discovery = discovery
        self._slots: dict[str, SlotAccessor] = {
            p.name: make_slot(p, discovery) for p in sig.params
        }

    def __call__(self, *args, **kwargs):
        return self._sig.build(*args, **kwargs)

    def __getattr__(self, item: str) -> SlotAccessor:
        slots = self.__dict__.get("_slots", {})
        if item in slots:
            return slots[item]
        raise AttributeError(
            f"{self._sig.py_name!r} has no parameter {item!r}. "
            f"Available: {list(slots)}"
        )

    def __dir__(self):
        return sorted(list(super().__dir__()) + list(self._slots))

    @property
    def signature(self) -> Signature:
        return self._sig

    def params(self) -> list[str]:
        return [p.name for p in self._sig.params]

    def __repr__(self):
        params = ", ".join(f"{p.name}: {p.kind.value}" for p in self._sig.params)
        return (f"<{self._sig.py_name}({params}) "
                f"-> {self._sig.returns.value} | fluent={self._sig.name!r}>")


# --------------------------------------------------------------------------- #
# Public builder                                                              #
# --------------------------------------------------------------------------- #


class ExpressionBuilder:
    """Entry point for constructing Fluent expression trees.

    Parameters
    ----------
    session : optional
        A live PyFluent session (or anything exposing ``session.settings``
        and/or ``session.fields.field_info``).  When provided, discovery
        can use both the settings tree *and* live field/surface info RPCs.
    settings : optional
        Root of a solver settings tree.  Ignored when ``session`` is given
        (in which case it is derived from ``session.settings``).  Useful
        when a caller already has a settings root but no session handle.
    field_info : optional
        A ``FieldInfo``-like object (typically ``session.fields.field_info``).
        Same fallback rules as ``settings``: derived from ``session`` when
        not given explicitly.

    Notes
    -----
    All three parameters are optional.  With none, the builder still works
    fully; only server-backed discovery (live surface / variable lists,
    in-scope named expressions) is disabled.
    """

    def __init__(
        self,
        session: Any | None = None,
        settings: Any | None = None,
        field_info: Any | None = None,
    ):
        if session is not None:
            if settings is None:
                settings = getattr(session, "settings", None)
            if field_info is None:
                fields = getattr(session, "fields", None)
                field_info = getattr(fields, "field_info", None) if fields else None

        self._discovery = Discovery(settings=settings, field_info=field_info)
        for group in REGISTRY.groups():
            setattr(self, group, _GroupFacade(group, self._discovery))

    # -- leaf constructors ------------------------------------------------- #

    @staticmethod
    def literal(value: float | int) -> Literal:
        """Build a numeric literal node."""
        return Literal(value)

    @staticmethod
    def quantity(value: float, units: str) -> Quantity:
        """Build a value-with-units node (e.g. ``5 [m/s]``)."""
        return Quantity(value, units)

    @staticmethod
    def variable(descriptor: VariableDescriptor) -> Variable:
        """Build a field variable node from a ``VariableCatalog`` entry."""
        return Variable(descriptor)

    @staticmethod
    def raw(name: str) -> RawName:
        """Build a raw-identifier node (e.g. a named expression name).

        Escape hatch.  Prefer :meth:`variable` for catalog-backed fields.
        """
        return RawName(name)

    @staticmethod
    def locations(names) -> LocationList:
        """Build a :class:`LocationList` from an iterable of strings."""
        return coerce_location_list(names)

    # -- discovery / convenience ------------------------------------------ #

    @property
    def settings(self) -> Any | None:
        """The attached settings handle, or ``None``."""
        return self._discovery.settings

    @property
    def discovery(self) -> Discovery:
        """The underlying :class:`Discovery` object (advanced use)."""
        return self._discovery

    def surface_names(self) -> list[str]:
        """All surface / zone names visible via the attached settings tree."""
        return self._discovery.surface_names()

    def named_expression_names(self) -> list[str]:
        """All in-scope named expressions visible via the attached settings tree."""
        return self._discovery.named_expression_names()

    def variables(self) -> list[VariableDescriptor]:
        """Every :class:`VariableDescriptor` the naming strategy supports."""
        return self._discovery.variable_descriptors()

    @staticmethod
    def render(expr: Expr) -> str:
        """Render an expression tree to its Fluent-side string form."""
        return expr.__fluent_expr__()

    @staticmethod
    def parse(text: str) -> Expr:
        """Parse a Fluent expression string into an :class:`Expr` tree.

        Round-trips with :meth:`render`::

            b.render(b.parse(s)) == s   # for canonical builder output
        """
        # Local import to avoid a cycle at module load.
        from ._parser import parse as _parse
        return _parse(text)
