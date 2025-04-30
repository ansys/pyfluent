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
Defines the ConversionStrategy base class for translating `PhysicalQuantity` objects.

Each concrete strategy maps `PhysicalQuantity` instances to the string representations
required by a specific system.
"""

from abc import ABC, abstractmethod
import types

from ansys.fluent.core.physicalquantities.base import PhysicalQuantity


class ConversionStrategy(ABC):
    """
    Abstract base class for `PhysicalQuantity` conversion strategies.

    This class defines the interface for all conversion strategies. Derived classes
    must implement the methods defined here to handle the conversion of `PhysicalQuantity`
    objects to and from their string representations, as well as to check if a
    `PhysicalQuantity` is supported.
    """

    @abstractmethod
    def to_string(self, quantity: PhysicalQuantity | str | None) -> str | None:
        """
        Convert a `PhysicalQuantity` to its string representation.

        Parameters
        ----------
        quantity : PhysicalQuantity | str
            The `PhysicalQuantity` to convert, or a string representation.

        Returns
        -------
        str
            The string representation of the `PhysicalQuantity`.

        Raises
        ------
        NotImplementedError
            If the method is not implemented in a derived class.
        """
        pass

    @abstractmethod
    def to_quantity(self, quantity: PhysicalQuantity | str) -> PhysicalQuantity:
        """
        Convert a string to its corresponding `PhysicalQuantity`.

        Parameters
        ----------
        quantity : PhysicalQuantity | str
            The string representation to convert, or a `PhysicalQuantity`.

        Returns
        -------
        PhysicalQuantity
            The corresponding `PhysicalQuantity` instance.

        Raises
        ------
        NotImplementedError
            If the method is not implemented in a derived class.
        """
        pass

    @abstractmethod
    def supports(self, quantity: PhysicalQuantity) -> bool:
        """
        Check if the given `PhysicalQuantity` is supported by the strategy.

        Parameters
        ----------
        quantity : PhysicalQuantity
            The `PhysicalQuantity` to check.

        Returns
        -------
        bool
            `True` if the `PhysicalQuantity` is supported, `False` otherwise.

        Raises
        ------
        NotImplementedError
            If the method is not implemented in a derived class.
        """
        pass


class MappingConversionStrategy(ConversionStrategy):
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
        """
        Initialize the MappingConversionStrategy.

        This constructor initializes the reverse mapping attribute to `None`.
        The reverse mapping is lazily initialized when accessed via the `_reverse_mapping` property.
        """
        self.__reverse_mapping = None

    @property
    def _reverse_mapping(self):
        """
        Get the reverse mapping of `_mapping`.

        The reverse mapping is a dictionary that maps string representations
        back to their corresponding `PhysicalQuantity` instances. It is lazily
        initialized on first access.

        Returns
        -------
        dict
            A dictionary mapping string representations to `PhysicalQuantity` instances.
        """
        if self.__reverse_mapping is None:
            self.__reverse_mapping = {x: y for y, x in self._mapping.items()}
        return self.__reverse_mapping

    def to_string(self, quantity: PhysicalQuantity | str | None) -> str | None:
        """
        Convert a `PhysicalQuantity` to its string representation.

        If the input is already a string, it is returned as-is. If the input
        is a `PhysicalQuantity` and is supported by the strategy, its string
        representation is returned. Otherwise, a `ValueError` is raised.

        Parameters
        ----------
        quantity : PhysicalQuantity | str
            The `PhysicalQuantity` to convert, or a string representation.

        Returns
        -------
        str
            The string representation of the `PhysicalQuantity`.

        Raises
        ------
        ValueError
            If the `PhysicalQuantity` is not supported by the strategy.
        """
        if isinstance(quantity, (str, types.NoneType)):
            return quantity
        if not self.supports(quantity):
            raise ValueError(f"{quantity.name} not supported.")
        return self._mapping[quantity]

    def to_quantity(self, quantity: PhysicalQuantity | str) -> PhysicalQuantity:
        """
        Convert a string to its corresponding `PhysicalQuantity`.

        If the input is already a `PhysicalQuantity`, it is returned as-is.
        Otherwise, the string is converted to a `PhysicalQuantity` using the
        reverse mapping.

        Parameters
        ----------
        quantity : PhysicalQuantity | str
            The string representation to convert, or a `PhysicalQuantity`.

        Returns
        -------
        PhysicalQuantity
            The corresponding `PhysicalQuantity` instance, or `None` if the
            string is not found in the reverse mapping.
        """
        if isinstance(quantity, PhysicalQuantity):
            return quantity
        return self._reverse_mapping.get(quantity)

    def supports(self, quantity: PhysicalQuantity) -> bool:
        """
        Check if the given `PhysicalQuantity` is supported by the strategy.

        Parameters
        ----------
        quantity : PhysicalQuantity
            The `PhysicalQuantity` to check.

        Returns
        -------
        bool
            `True` if the `PhysicalQuantity` is supported, `False` otherwise.
        """
        return quantity in self._mapping
