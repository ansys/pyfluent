# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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

"""Abstract contract for Fluent reduction operations."""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Union

# Type alias for reduction results
ReductionResult = Union[float, list[float], tuple[float, float, float]]

__all__ = ("AbstractReduction",)


class AbstractReduction(ABC):
    """Abstract interface for area, volume, force, and statistical reductions."""

    @abstractmethod
    def area(self, locations, ctxt=None) -> ReductionResult:
        """Get area."""
        pass

    @abstractmethod
    def area_average(self, expression, locations, ctxt=None) -> ReductionResult:
        """Get area average."""
        pass

    @abstractmethod
    def area_integral(self, expression, locations, ctxt=None) -> ReductionResult:
        """Get area integral."""
        pass

    @abstractmethod
    def centroid(self, locations, ctxt=None) -> ReductionResult:
        """Get centroid."""
        pass

    @abstractmethod
    def count(self, locations, ctxt=None) -> ReductionResult:
        """Count the number of faces or cells within the locations."""
        pass

    @abstractmethod
    def count_if(self, condition, locations, ctxt=None) -> ReductionResult:
        """Count the number of faces or cells where the specified condition is satisfied."""
        pass

    @abstractmethod
    def force(self, locations, ctxt=None) -> ReductionResult:
        """Get force."""
        pass

    @abstractmethod
    def mass_average(self, expression, locations, ctxt=None) -> ReductionResult:
        """Get mass average."""
        pass

    @abstractmethod
    def mass_flow_average(self, expression, locations, ctxt=None) -> ReductionResult:
        """Get mass flow average."""
        pass

    @abstractmethod
    def mass_flow_average_absolute(
        self, expression, locations, ctxt=None
    ) -> ReductionResult:
        """Compute the mass flow average of the absolute value of the given expression."""
        pass

    @abstractmethod
    def mass_flow_integral(self, expression, locations, ctxt=None) -> ReductionResult:
        """Get mass flow integral."""
        pass

    @abstractmethod
    def mass_integral(self, expression, locations, ctxt=None) -> ReductionResult:
        """Get mass integral."""
        pass

    @abstractmethod
    def maximum(self, expression, locations, ctxt=None) -> ReductionResult:
        """Get maximum."""
        pass

    @abstractmethod
    def minimum(self, expression, locations, ctxt=None) -> ReductionResult:
        """Get minimum."""
        pass

    @abstractmethod
    def pressure_force(self, locations, ctxt=None) -> ReductionResult:
        """Get pressure force."""
        pass

    @abstractmethod
    def viscous_force(self, locations, ctxt=None) -> ReductionResult:
        """Get viscous force."""
        pass

    @abstractmethod
    def volume(self, locations, ctxt=None) -> ReductionResult:
        """Get volume."""
        pass

    @abstractmethod
    def volume_average(self, expression, locations, ctxt=None) -> ReductionResult:
        """Get volume average."""
        pass

    @abstractmethod
    def volume_integral(self, expression, locations, ctxt=None) -> ReductionResult:
        """Get volume integral."""
        pass

    @abstractmethod
    def moment(self, expression, locations, ctxt=None) -> ReductionResult:
        """Get moment."""
        pass

    @abstractmethod
    def sum(
        self, expression, locations, weight: str | Enum, ctxt=None
    ) -> ReductionResult:
        """Get sum."""
        pass

    @abstractmethod
    def sum_if(
        self, expression, condition, locations, weight: str | Enum, ctxt=None
    ) -> ReductionResult:
        """Compute the weighted sum of the expression at locations where the given condition is satisfied."""
        pass
