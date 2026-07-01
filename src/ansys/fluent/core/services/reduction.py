# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
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

"""Wrappers over Reduction gRPC service of Fluent."""

from collections.abc import Iterable
from typing import Any
import weakref

from ansys.fluent.core.exceptions import DisallowedValuesError
from ansys.fluent.core.services.abstract_reduction import AbstractReduction
from ansys.fluent.core.solver.function.reduction import Weight

Path = list[tuple[str, str]]


class Reduction(AbstractReduction):
    """Reduction."""

    def __init__(self, service):
        """__init__ method of Reduction class."""
        self.service = service
        self.ctxt = None

    def set_context(self, ctxt):
        """Set the context over which reduction service should operate."""
        self.ctxt = weakref.proxy(ctxt)

    def _validate_str_location(self, loc: str):
        if not self.ctxt:
            return
        if all(
            loc not in names()
            for names in (
                self.ctxt.fields.field_data.surfaces,
                self.ctxt.settings.setup.cell_zone_conditions,
            )
        ):
            raise ValueError(f"Invalid location input: '{loc}'")

    def _validate_locations(self, locations):
        for loc in locations:
            if isinstance(loc, Iterable) and not isinstance(loc, (str, bytes)):
                raise DisallowedValuesError("location", loc, list(loc))
            if isinstance(loc, str):
                self._validate_str_location(loc)

    def area(self, locations, ctxt=None) -> Any:
        """Get area."""
        self._validate_locations(locations=locations)
        return self.service.area(locations, ctxt)

    def area_average(self, expression, locations, ctxt=None) -> Any:
        """Get area average."""
        self._validate_locations(locations=locations)
        return self.service.area_average(expression, locations, ctxt)

    def area_integral(self, expression, locations, ctxt=None) -> Any:
        """Get area integral."""
        self._validate_locations(locations=locations)
        return self.service.area_integral(expression, locations, ctxt)

    def centroid(self, locations, ctxt=None) -> Any:
        """Get centroid."""
        self._validate_locations(locations=locations)
        return self.service.centroid(locations, ctxt)

    def count(self, locations, ctxt=None) -> Any:
        """Count the number of faces or cells within the locations."""
        self._validate_locations(locations=locations)
        return self.service.count(locations, ctxt)

    def count_if(self, condition, locations, ctxt=None) -> Any:
        """Count the number of faces or cells where the specified condition is satisfied."""
        self._validate_locations(locations=locations)
        return self.service.count_if(condition, locations, ctxt)

    def force(self, locations, ctxt=None) -> Any:
        """Get force."""
        self._validate_locations(locations=locations)
        return self.service.force(locations, ctxt)

    def mass_average(self, expression, locations, ctxt=None) -> Any:
        """Get mass average."""
        self._validate_locations(locations=locations)
        return self.service.mass_average(expression, locations, ctxt)

    def mass_flow_average(self, expression, locations, ctxt=None) -> Any:
        """Get mass flow average."""
        self._validate_locations(locations=locations)
        return self.service.mass_flow_average(expression, locations, ctxt)

    def mass_flow_average_absolute(self, expression, locations, ctxt=None) -> Any:
        """Compute the mass flow average of the absolute value of the given expression."""
        self._validate_locations(locations=locations)
        return self.service.mass_flow_average_absolute(expression, locations, ctxt)

    def mass_flow_integral(self, expression, locations, ctxt=None) -> Any:
        """Get mass flow integral."""
        self._validate_locations(locations=locations)
        return self.service.mass_flow_integral(expression, locations, ctxt)

    def mass_integral(self, expression, locations, ctxt=None) -> Any:
        """Get mass integral."""
        self._validate_locations(locations=locations)
        return self.service.mass_integral(expression, locations, ctxt)

    def maximum(self, expression, locations, ctxt=None) -> Any:
        """Get maximum."""
        self._validate_locations(locations=locations)
        return self.service.maximum(expression, locations, ctxt)

    def minimum(self, expression, locations, ctxt=None) -> Any:
        """Get minimum."""
        self._validate_locations(locations=locations)
        return self.service.minimum(expression, locations, ctxt)

    def pressure_force(self, locations, ctxt=None) -> Any:
        """Get pressure force."""
        self._validate_locations(locations=locations)
        return self.service.pressure_force(locations, ctxt)

    def viscous_force(self, locations, ctxt=None) -> Any:
        """Get viscous force."""
        self._validate_locations(locations=locations)
        return self.service.viscous_force(locations, ctxt)

    def volume(self, locations, ctxt=None) -> Any:
        """Get volume."""
        self._validate_locations(locations=locations)
        return self.service.volume(locations, ctxt)

    def volume_average(self, expression, locations, ctxt=None) -> Any:
        """Get volume average."""
        self._validate_locations(locations=locations)
        return self.service.volume_average(expression, locations, ctxt)

    def volume_integral(self, expression, locations, ctxt=None) -> Any:
        """Get volume integral."""
        self._validate_locations(locations=locations)
        return self.service.volume_integral(expression, locations, ctxt)

    def moment(self, expression, locations, ctxt=None) -> Any:
        """Get moment."""
        self._validate_locations(locations=locations)
        return self.service.moment(expression, locations, ctxt)

    def sum(self, expression, locations, weight: str | Weight, ctxt=None) -> Any:
        """Get sum."""
        self._validate_locations(locations=locations)
        return self.service.sum(expression, locations, weight, ctxt)

    def sum_if(
        self, expression, condition, locations, weight: str | Weight, ctxt=None
    ) -> Any:
        """Compute the weighted sum of the expression at locations where the given condition is satisfied."""
        self._validate_locations(locations=locations)
        return self.service.sum_if(expression, condition, locations, weight, ctxt)
