# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""Fluent expression builder.

:class:`ExpressionBuilder` is the generic
:class:`~._generic.ExpressionBuilder` bound to the Fluent dialect, with
discovery backed by a live PyFluent session.
"""

from __future__ import annotations

from typing import Any

from ._discovery import FluentDiscovery
from ._fluent import FLUENT_DIALECT
from ._generic import Call, Expr
from ._generic import ExpressionBuilder as _GenericExpressionBuilder
from ._generic import Kind
from ._generic import make_call as _make_call
from ._generic import parse as _parse


class ExpressionBuilder(_GenericExpressionBuilder):
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

    _fluent_discovery: FluentDiscovery

    def __init__(
        self,
        session: Any | None = None,
        settings: Any | None = None,
        field_info: Any | None = None,
    ) -> None:
        if session is not None:
            if settings is None:
                settings = getattr(session, "settings", None)
            if field_info is None:
                fields = getattr(session, "fields", None)
                field_info = getattr(fields, "field_info", None) if fields else None

        self._fluent_discovery = FluentDiscovery(
            settings=settings, field_info=field_info
        )
        super().__init__(FLUENT_DIALECT, self._fluent_discovery)

    @property
    def discovery(self) -> FluentDiscovery:
        """The underlying :class:`FluentDiscovery` object (advanced use)."""
        return self._fluent_discovery

    @property
    def settings(self) -> Any | None:
        """The attached settings handle, or ``None``."""
        return self._fluent_discovery.settings

    def surface_names(self) -> list[str]:
        """All surface / zone names visible via the attached discovery handle."""
        return self.location_names()


def parse(text: str) -> Expr:
    """Parse a Fluent expression string into an :class:`Expr` tree.

    Raises
    ------
    ExpressionBuildError
        On any lexical or grammatical error.
    """
    return _parse(text, FLUENT_DIALECT)


def make_call(name: str, *args: object, returns: Kind = Kind.SCALAR) -> Call:
    """Build a :class:`Call` node for a Fluent function not in the registry."""
    return _make_call(name, *args, returns=returns, dialect=FLUENT_DIALECT)
