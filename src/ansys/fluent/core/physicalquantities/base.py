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
Defines the core PhysicalQuantity class and predefined quantities.

This module provides a structured, extensible way to represent physical quantities
(e.g., pressure, velocity) independently of any product-specific naming conventions.
"""

from dataclasses import dataclass
from enum import Enum, auto


class Dimension(Enum):
    """Enumerates physical dimensions."""

    PRESSURE = auto()
    VELOCITY = auto()
    TEMPERATURE = auto()
    # etc.


@dataclass(frozen=True)
class PhysicalQuantity:
    """Defines a physical quantity."""

    name: str  # Human-readable name
    dimension: Dimension
    si_unit: str  # Preferred SI unit (e.g., "Pa", "m/s", "K")


class PhysicalQuantities:
    """A catalogue of physical quantities."""

    PRESSURE = PhysicalQuantity("static pressure", Dimension.PRESSURE, "Pa")
    VELOCITY_X = PhysicalQuantity("velocity x", Dimension.VELOCITY, "m/s")
    TEMPERATURE = PhysicalQuantity("temperature", Dimension.TEMPERATURE, "K")
    # Add more quantities as needed
