# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""Fluent discovery: bridge between the builder and live solver state.

Everything here is best-effort. When no session/settings handle is
attached, accessors still work but simply return empty lists /
conservative ``is_allowed`` answers.

:class:`FluentDiscovery` implements the generic
:class:`ansys.expressions.Discovery` protocol. Three concerns are served:

* **Surfaces** (locations): live surface list from ``field_info`` when
  available, otherwise a walk of the settings tree.
* **Variables**: entries of ``VariableCatalog`` that are (a) supported by
  the Fluent dialect for rendering and (b) currently active on the server,
  if a ``field_info`` handle is available.
* **Named expressions**: user-defined named expressions in scope.
"""

from __future__ import annotations

import logging
from typing import Any

from ansys.variables import VariableDescriptor

from ._fluent import FLUENT_DIALECT

_logger = logging.getLogger("pyfluent.expressions")


def _field_data_naming():
    """Lazy import to avoid a hard dependency on field_data_interfaces at import time."""
    try:
        from ansys.fluent.core._variable_strategies import (
            FluentFieldDataNamingStrategy as naming_strategy,
        )

        _naming_strategy_instance = naming_strategy()
        return _naming_strategy_instance
    except Exception:
        return None


class FluentDiscovery:
    """Answers discovery queries against optional session/settings handles.

    Parameters
    ----------
    settings :
        Root of a solver settings tree, or ``None``.
    field_info :
        A ``FieldInfo`` (typically ``session.fields.field_info``) exposing
        ``get_surfaces_info()`` / ``get_scalar_fields_info()`` /
        ``get_vector_fields_info()``.  ``None`` if unavailable.
    """

    def __init__(
        self,
        settings: Any | None = None,
        field_info: Any | None = None,
    ):
        self.settings = settings
        self.field_info = field_info

    # ------------------------------------------------------------------ #
    # Introspection                                                      #
    # ------------------------------------------------------------------ #

    def has_settings(self) -> bool:
        """Return ``True`` if a settings tree is attached."""
        return self.settings is not None

    def has_field_info(self) -> bool:
        """Return ``True`` if a ``FieldInfo`` handle is attached."""
        return self.field_info is not None

    # ------------------------------------------------------------------ #
    # Surfaces / locations                                               #
    # ------------------------------------------------------------------ #

    def location_names(self) -> list[str]:
        """Return all surface / zone names available in the current session.

        Prefers a live query via ``field_info.get_surfaces_info()`` (which
        includes boundary zones plus derived surfaces).  Falls back to a
        settings-tree walk when ``field_info`` is unavailable.
        """
        # Preferred: ask field_info -- it's the canonical, live list.
        if self.has_field_info():
            try:
                info = self.field_info.get_surfaces_info() or {}
                if info:
                    return list(info.keys())
            except Exception as exc:  # fall through to settings walk
                _logger.debug("get_surfaces_info() failed: %s", exc)

        if not self.has_settings():
            return []

        names: list[str] = []
        names.extend(self._names_of(("setup", "boundary_conditions")))
        names.extend(self._names_of(("results", "surfaces")))
        # De-duplicate while preserving order.
        seen: set[str] = set()
        out: list[str] = []
        for n in names:
            if n not in seen:
                seen.add(n)
                out.append(n)
        return out

    def surface_names(self) -> list[str]:
        """Alias of :meth:`location_names`."""
        return self.location_names()

    # ------------------------------------------------------------------ #
    # Variables                                                          #
    # ------------------------------------------------------------------ #

    def variable_descriptors(self) -> list[VariableDescriptor]:
        """VariableDescriptors legal for the current session, if known.

        When a ``field_info`` handle is available, returns the intersection
        of (a) descriptors supported for rendering by the Fluent dialect
        and (b) fields currently active on the server (per
        ``get_scalar_fields_info`` + ``get_vector_fields_info``).

        When ``field_info`` is unavailable, returns the full static set
        of expression-supported descriptors.
        """
        supported = FLUENT_DIALECT.supported_variables()
        active = self._active_descriptors()
        if active is None:
            return supported
        active_set = set(active)
        return [d for d in supported if d in active_set]

    def variable_names(self) -> list[str]:
        """Fluent-side (expression) names of the descriptors from
        :meth:`variable_descriptors`.
        """
        return [FLUENT_DIALECT.variable_name(d) for d in self.variable_descriptors()]

    def is_variable_supported(self, descriptor: VariableDescriptor) -> bool:
        """Whether ``descriptor`` can be rendered *and* (if known) is active."""
        if not FLUENT_DIALECT.supports_variable(descriptor):
            return False
        active = self._active_descriptors()
        if active is None:
            return True
        return descriptor in set(active)

    # ------------------------------------------------------------------ #
    # Named expressions                                                  #
    # ------------------------------------------------------------------ #

    def named_expression_names(self) -> list[str]:
        """Names of user-defined named expressions in scope.

        Returns an empty list when no settings handle is attached.
        """
        if not self.has_settings():
            return []
        return self._names_of(("setup", "named_expressions"))

    # ------------------------------------------------------------------ #
    # Helpers                                                            #
    # ------------------------------------------------------------------ #

    def _active_descriptors(self) -> list[VariableDescriptor] | None:
        """List of descriptors active on the server, or ``None`` if unknown.

        Uses the field-data naming strategy to map server-side field names
        (e.g. ``"absolute-pressure"``) back to catalog descriptors.
        """
        if not self.has_field_info():
            return None
        fd_naming = _field_data_naming()
        if fd_naming is None:
            return None

        active_names: list[str] = []
        for getter in ("get_scalar_fields_info", "get_vector_fields_info"):
            fn = getattr(self.field_info, getter, None)
            if not callable(fn):
                continue
            try:
                info = fn() or {}
            except Exception as exc:
                _logger.debug("%s() failed: %s", getter, exc)
                continue
            active_names.extend(info.keys())

        descriptors: list[VariableDescriptor] = []
        for name in active_names:
            try:
                d = fd_naming.to_variable_descriptor(name)
            except Exception as exc:
                _logger.debug("to_variable_descriptor(%r) failed: %s", name, exc)
                d = None
            if d is not None:
                descriptors.append(d)
        return descriptors

    def _names_of(self, path: tuple[str, ...]) -> list[str]:
        """Best-effort child-name listing for ``self.settings.<path>``."""
        node: Any = self.settings
        for step in path:
            node = getattr(node, step, None)
            if node is None:
                return []
        # Prefer the explicit API when present.
        getter = getattr(node, "get_object_names", None)
        if callable(getter):
            try:
                return list(getter())
            except Exception as exc:
                _logger.debug("get_object_names() failed at %s: %s", path, exc)
        # Fall back to iteration (NamedObject containers are iterable).
        try:
            return list(iter(node))
        except Exception as exc:
            _logger.debug("iter() failed at %s: %s", path, exc)
            return []
