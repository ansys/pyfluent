# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""Layer 3: user-facing expression builder facade.

Exposes :class:`ExpressionBuilder`, the entry point users interact with.
The builder is a thin, discoverable wrapper over the Layer 1 registry:

* ``builder.reductions.area_ave(expression=..., locations=...)`` returns an
  AST :class:`~._ast.Call` node ready to be composed further.
* ``builder.variable(V.TEMPERATURE)`` and ``builder.literal(1.5)`` build
  leaf nodes.
* ``builder.locations([...])`` builds a :class:`~._ast.LocationList`.
* ``builder.settings`` (optional) is a handle to the live solver settings
  tree; when present, discovery helpers may consult it.
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
from ._registry import REGISTRY, Signature


class _GroupFacade:
    """Attribute-style access to one group of registered signatures.

    ``builder.reductions.area_ave(...)`` is dispatched here.
    """

    def __init__(self, group: str, discovery: "_Discovery"):
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
    """A callable wrapper for a :class:`Signature` that also exposes metadata."""

    def __init__(self, sig: Signature, discovery: "_Discovery"):
        self._sig = sig
        self._discovery = discovery

    def __call__(self, *args, **kwargs):
        return self._sig.build(*args, **kwargs)

    # -- introspection ---------------------------------------------------- #
    @property
    def signature(self) -> Signature:
        return self._sig

    def params(self) -> list[str]:
        return [p.name for p in self._sig.params]

    def __repr__(self):
        params = ", ".join(f"{p.name}: {p.kind.value}" for p in self._sig.params)
        return (f"<{self._sig.py_name}({params}) "
                f"-> {self._sig.returns.value} | fluent={self._sig.name!r}>")


class _Discovery:
    """Thin bridge to the live solver ``settings`` tree.

    Kept deliberately small for the prototype; expand as we wire up
    surface / variable / named-expression queries.
    """

    def __init__(self, settings: Any | None):
        self.settings = settings

    def has_settings(self) -> bool:
        return self.settings is not None

    def surface_names(self) -> list[str]:
        """Return all surface / zone names available in the current session.

        Returns an empty list when no settings handle is attached.
        """
        if not self.has_settings():
            return []
        # Best-effort: aggregate everything under setup.boundary_conditions.
        try:
            bcs = self.settings.setup.boundary_conditions
        except AttributeError:
            return []
        names: list[str] = []
        for child in getattr(bcs, "get_object_names", lambda: [])():
            names.append(child)
        return names


# --------------------------------------------------------------------------- #
# Public builder                                                              #
# --------------------------------------------------------------------------- #


class ExpressionBuilder:
    """Entry point for constructing Fluent expression trees.

    Parameters
    ----------
    settings : optional
        Root of a live solver settings tree.  When provided, discovery
        helpers (``allowed_values`` etc.) may query it.  When ``None``,
        the builder still works fully; only discovery is disabled.
    """

    def __init__(self, settings: Any | None = None):
        self._discovery = _Discovery(settings)
        # One facade per registered group.
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

    # -- convenience ------------------------------------------------------- #

    @property
    def settings(self) -> Any | None:
        """The attached settings handle, or ``None``."""
        return self._discovery.settings

    @staticmethod
    def render(expr: Expr) -> str:
        """Render an expression tree to its Fluent-side string form."""
        return expr.__fluent_expr__()
