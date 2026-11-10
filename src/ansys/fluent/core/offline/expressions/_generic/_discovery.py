# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""Discovery: what values are legal in the current context.

The builder's per-parameter slots (see :mod:`._slots`) ask a :class:`Discovery`
object which locations, named expressions, and variables are available.
Products implement this protocol on top of their own data sources (for example
a live session). :class:`StaticDiscovery` is used when there is no data
source: it is permissive and driven by the dialect.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from ansys.units.variable_descriptor import VariableDescriptor

from ._dialect import Dialect


@runtime_checkable
class Discovery(Protocol):
    """Answers which values are legal in the current context."""

    def location_names(self) -> list[str]:
        """Return the available location names (surfaces, zones, ...)."""
        ...

    def named_expression_names(self) -> list[str]:
        """Return the names of named expressions that are in scope."""
        ...

    def variable_descriptors(self) -> list[VariableDescriptor]:
        """Return the variable descriptors available in the current context."""
        ...

    def is_variable_supported(self, descriptor: VariableDescriptor) -> bool:
        """Return ``True`` if ``descriptor`` is usable in the current context."""
        ...


class StaticDiscovery:
    """Discovery without a live data source.

    Parameters
    ----------
    dialect :
        Dialect that determines which variables are supported.
    locations :
        Known location names. Empty means "unknown", which slots treat
        permissively.
    named_expressions :
        Known named-expression names. Empty means "unknown".
    """

    def __init__(
        self,
        dialect: Dialect,
        locations: Sequence[str] = (),
        named_expressions: Sequence[str] = (),
    ) -> None:
        self._dialect = dialect
        self._locations = list(locations)
        self._named_expressions = list(named_expressions)

    def location_names(self) -> list[str]:
        """Return the known location names."""
        return list(self._locations)

    def named_expression_names(self) -> list[str]:
        """Return the known named-expression names."""
        return list(self._named_expressions)

    def variable_descriptors(self) -> list[VariableDescriptor]:
        """Return every descriptor the dialect supports."""
        return self._dialect.supported_variables()

    def is_variable_supported(self, descriptor: VariableDescriptor) -> bool:
        """Return ``True`` if the dialect can render ``descriptor``."""
        return self._dialect.supports_variable(descriptor)
