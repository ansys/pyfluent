# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""Per-parameter slot accessors.

For a registered signature ``area_ave(expression, locations)``, users can
introspect what values are legal for each slot *before* filling it::

    inv = builder.reductions.area_ave
    inv.expression.variables.allowed_values()   # catalog entries
    inv.expression.named.allowed_values()       # in-scope named exprs
    inv.locations.allowed_values()              # surface names
    inv.locations.is_allowed("inlet1")

Each :class:`SlotAccessor` is created lazily by :class:`_SigInvoker`
based on the :class:`~._registry.Param`'s kind.
"""

from __future__ import annotations

from typing import Any

from ansys.units.variable_descriptor import VariableDescriptor

from ._ast import Kind
from ._discovery import Discovery
from ._registry import Param


class SlotAccessor:
    """Base class for per-slot discovery helpers."""

    def __init__(self, param: Param, discovery: Discovery):
        self._param = param
        self._discovery = discovery

    @property
    def name(self) -> str:
        """Name of the parameter this slot represents."""
        return self._param.name

    @property
    def kind(self) -> Kind:
        """Expected :class:`~._ast.Kind` for this slot."""
        return self._param.kind

    def allowed_values(self) -> list[Any]:  # pragma: no cover - abstract
        """Return the list of values permitted for this slot."""
        raise NotImplementedError

    def is_allowed(self, value: Any) -> bool:
        """Return ``True`` if ``value`` is a permitted value for this slot."""
        return value in self.allowed_values()

    def __repr__(self) -> str:
        return f"<slot {self.name!r}: {self.kind.value}>"


# --------------------------------------------------------------------------- #
# Location slot                                                               #
# --------------------------------------------------------------------------- #


class LocationSlot(SlotAccessor):
    """Accessor for a :attr:`Kind.LOCATION_LIST` parameter."""

    def allowed_values(self) -> list[str]:
        return self._discovery.surface_names()

    def is_allowed(self, value: Any) -> bool:
        names = self.allowed_values()
        # If we have no settings/field_info-derived list, be permissive but still
        # validate that inputs are strings.
        if not names:
            if isinstance(value, str):
                return True
            if isinstance(value, (list, tuple)):
                return all(isinstance(v, str) for v in value)
            return False

        if isinstance(value, str):
            return value in names
        if isinstance(value, (list, tuple)):
            return all(isinstance(v, str) and v in names for v in value)
        return False


# --------------------------------------------------------------------------- #
# Scalar-expression slot                                                      #
# --------------------------------------------------------------------------- #


class _VariablesSubSlot:
    """Sub-namespace: catalog variables accepted by the scalar slot."""

    def __init__(self, discovery: Discovery):
        self._discovery = discovery

    def allowed_values(self) -> list[VariableDescriptor]:
        """Return ``VariableDescriptor`` entries available in the current session."""
        return self._discovery.variable_descriptors()

    def is_allowed(self, value: Any) -> bool:
        """Return ``True`` if ``value`` is a supported :class:`VariableDescriptor`."""
        if isinstance(value, VariableDescriptor):
            return self._discovery.is_variable_supported(value)
        return False


class _NamedExprSubSlot:
    """Sub-namespace: in-scope named expressions accepted by the scalar slot."""

    def __init__(self, discovery: Discovery):
        self._discovery = discovery

    def allowed_values(self) -> list[str]:
        """Return names of user-defined named expressions currently in scope."""
        return self._discovery.named_expression_names()

    def is_allowed(self, value: Any) -> bool:
        """Return ``True`` if ``value`` is an in-scope named expression name."""
        if not isinstance(value, str):
            return False
        names = self.allowed_values()
        # Permissive when offline (no settings): we can't verify.
        return not names or value in names


class ScalarSlot(SlotAccessor):
    """Accessor for a :attr:`Kind.SCALAR` parameter.

    Exposes segregated sub-slots (``.variables``, ``.named``) plus an
    agglomerated :meth:`allowed_values` view.
    """

    def __init__(self, param: Param, discovery: Discovery):
        super().__init__(param, discovery)
        self.variables = _VariablesSubSlot(discovery)
        self.named = _NamedExprSubSlot(discovery)

    def allowed_values(self) -> list[Any]:
        # Union of both sub-slots. Descriptors first, then named-expr strings.
        return [*self.variables.allowed_values(), *self.named.allowed_values()]

    def is_allowed(self, value: Any) -> bool:
        return self.variables.is_allowed(value) or self.named.is_allowed(value)


# --------------------------------------------------------------------------- #
# Factory                                                                     #
# --------------------------------------------------------------------------- #


_SLOTS: dict[Kind, type[SlotAccessor]] = {
    Kind.LOCATION_LIST: LocationSlot,
    Kind.SCALAR: ScalarSlot,
}


def make_slot(param: Param, discovery: Discovery) -> SlotAccessor:
    """Return the appropriate :class:`SlotAccessor` for ``param``."""
    cls = _SLOTS.get(param.kind, SlotAccessor)
    return cls(param, discovery)
