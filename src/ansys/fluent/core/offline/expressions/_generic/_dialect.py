# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""Dialects: the product-specific parts of an expression language.

A :class:`Dialect` supplies everything the generic expression tree, parser,
and builder need to know about a particular product:

* ``naming`` -- a
  :class:`~ansys.units.variable_descriptor.ConversionStrategy` that converts
  variable descriptors to and from the product's variable names.
* ``functions`` -- a :class:`~._registry.FunctionRegistry` of the functions the
  product's expression language provides.

:data:`DEFAULT_DIALECT` names variables by their catalog name (for example
``absolute_pressure``) and provides no functions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import types

from ansys.units.variable_descriptor import (
    ConversionStrategy,
    MappingConversionStrategy,
    VariableCatalog,
    VariableDescriptor,
)

from ._registry import FunctionRegistry, Signature
from .errors import ExpressionBuildError


class DescriptorNameStrategy(ConversionStrategy):
    """Name variables by their catalog name, for example ``"absolute_pressure"``."""

    def to_string(self, variable: VariableDescriptor | str | None) -> str | None:
        """Return the catalog name of ``variable``; strings pass through."""
        if isinstance(variable, (str, types.NoneType)):
            return variable
        return variable.name

    def to_variable_descriptor(
        self, variable: VariableDescriptor | str
    ) -> VariableDescriptor | None:
        """Return the catalog descriptor named ``variable``, or ``None``."""
        if isinstance(variable, VariableDescriptor):
            return variable
        candidate = getattr(VariableCatalog, variable.upper(), None)
        return candidate if isinstance(candidate, VariableDescriptor) else None

    def supports(self, variable: VariableDescriptor) -> bool:
        """Return ``True`` for any variable descriptor."""
        return isinstance(variable, VariableDescriptor)


@dataclass(frozen=True, eq=False)
class Dialect:
    """The product-specific parts of an expression language.

    Parameters
    ----------
    name :
        Short identifier used in error messages, for example ``"generic"``.
    naming :
        Converts variable descriptors to and from product variable names.
    functions :
        Functions available in the product's expression language.
    """

    name: str
    naming: ConversionStrategy = field(default_factory=DescriptorNameStrategy)
    functions: FunctionRegistry = field(default_factory=FunctionRegistry)

    def variable_name(self, descriptor: VariableDescriptor) -> str:
        """Return the product-side name of ``descriptor``.

        Raises
        ------
        ExpressionBuildError
            If the naming strategy does not support ``descriptor``.
        """
        try:
            name = self.naming.to_string(descriptor)
        except (ValueError, AttributeError, TypeError, KeyError) as exc:
            raise ExpressionBuildError(
                f"{descriptor!r} has no variable name in the {self.name!r} dialect."
            ) from exc
        if not isinstance(name, str):
            raise ExpressionBuildError(
                f"{descriptor!r} has no variable name in the {self.name!r} dialect."
            )
        return name

    def variable_descriptor(self, name: str) -> VariableDescriptor | None:
        """Return the descriptor for product-side variable ``name``, or ``None``."""
        try:
            descriptor = self.naming.to_variable_descriptor(name)
        except (ValueError, AttributeError, TypeError, KeyError):
            return None
        return descriptor if isinstance(descriptor, VariableDescriptor) else None

    def supports_variable(self, descriptor: VariableDescriptor) -> bool:
        """Return ``True`` if ``descriptor`` can be rendered in this dialect."""
        try:
            return bool(self.naming.supports(descriptor))
        except (ValueError, AttributeError, TypeError, KeyError):
            return False

    def supported_variables(self) -> list[VariableDescriptor]:
        """Return every descriptor this dialect is known to support.

        Enumerable for :class:`~ansys.units.variable_descriptor.MappingConversionStrategy`
        and :class:`DescriptorNameStrategy`; empty for other strategies.
        """
        if isinstance(self.naming, MappingConversionStrategy):
            return list(self.naming._mapping)
        if isinstance(self.naming, DescriptorNameStrategy):
            return [
                descriptor
                for descriptors in VariableCatalog.all().values()
                for descriptor in descriptors
            ]
        return []

    def find_function(self, name: str) -> Signature | None:
        """Return the registered function with product-side ``name``, or ``None``."""
        return self.functions.find(name)


DEFAULT_DIALECT = Dialect("generic")
"""Dialect that names variables by catalog name and provides no functions."""
