# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Defines the ConversionStrategy base class for translating PhysicalQuantity objects.

Each concrete strategy maps PhysicalQuantity instances to the string representations
required by a specific system (e.g., Fluent, Mechanical).
"""

from abc import ABC, abstractmethod

from ansys.core.physicalquantities.base import PhysicalQuantity


class ConversionStrategy(ABC):
    """Abstract strategy for PhysicalQuantity"""

    @abstractmethod
    def to_string(self, quantity: PhysicalQuantity | str) -> str:
        """Convert from PhysicalQuantity to string."""
        pass

    @abstractmethod
    def to_quantity(self, quantity: PhysicalQuantity | str) -> PhysicalQuantity:
        """Convert from string to PhysicalQuantity."""
        pass

    @abstractmethod
    def supports(self, quantity: PhysicalQuantity) -> bool:
        """Whether the quantity is supported."""
        pass


class BaseConversionStrategy(ConversionStrategy):
    """
    Intermediate base class for implementing PhysicalQuantity conversion strategies.

    This class simplifies the creation of concrete strategy classes by providing
    default implementations for common methods. Classes inheriting from this base
    class only need to define a `_mapping` dictionary that maps `PhysicalQuantity`
    instances to their corresponding string representations.

    Attributes
    ----------
    _reverse_mapping : dict
        A lazily initialized reverse mapping of `_mapping`, used for converting
        strings back to `PhysicalQuantity` instances.

    Methods
    -------
    to_string(quantity: PhysicalQuantity | str) -> str
        Converts a `PhysicalQuantity` to its string representation. Raises a
        `ValueError` if the quantity is not supported.
    to_quantity(quantity: PhysicalQuantity | str) -> PhysicalQuantity
        Converts a string to its corresponding `PhysicalQuantity`.
    supports(quantity: PhysicalQuantity) -> bool
        Checks if the given `PhysicalQuantity` is supported by the strategy.

    Raises
    ------
    ValueError
        If a `PhysicalQuantity` is not supported during conversion to a string.
    """

    def __init__(self):
        self.__reverse_mapping = None

    @property
    def _reverse_mapping(self):
        if self.__reverse_mapping is None:
            self.__reverse_mapping = {x: y for y, x in self._mapping.items()}
        return self.__reverse_mapping

    def to_string(self, quantity: PhysicalQuantity | str) -> str:
        """Convert from PhysicalQuantity to string.

        Raises
        ------
        ValueError
            If the PhysicalQuantity is not supported.
        """
        if isinstance(quantity, str):
            return quantity
        if not self.supports(quantity):
            raise ValueError(f"{quantity.name} not supported.")
        return self._mapping[quantity]

    def to_quantity(self, quantity: PhysicalQuantity | str) -> PhysicalQuantity:
        """Convert from string to PhysicalQuantity."""
        if isinstance(quantity, PhysicalQuantity):
            return quantity
        return self._reverse_mapping.get(quantity)

    def supports(self, quantity: PhysicalQuantity) -> bool:
        """Whether the quantity is supported."""
        return quantity in self._mapping
