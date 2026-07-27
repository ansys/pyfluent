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

"""Wrapper over the reduction gRPC service of Fluent (v0 proto API)."""

from typing import Any

from ansys.api.fluent.v0 import reduction_pb2, reduction_pb2_grpc
from ansys.fluent.core._grpc_services.object_model_service_v0 import (
    _convert_variant_to_value,
)
from ansys.fluent.core._grpc_services.reduction_service import (
    BadReductionRequest,
    _locns,
)
from ansys.fluent.core.services._protocols import ServiceProtocol
from ansys.fluent.core.solver.function.reduction import Weight
from ansys.fluent.core.variable_strategies import (
    FluentExprNamingStrategy as naming_strategy,
)

Path = list[tuple[str, str]]


class ReductionService(ServiceProtocol):
    """Reduction gRPC service wrapper (v0 proto API)."""

    def __init__(
        self,
        intercept_channel,
        metadata: list[tuple[str, str]],
    ):
        """Initialize ReductionService."""
        self._stub = reduction_pb2_grpc.ReductionStub(intercept_channel)
        self._metadata = metadata
        self._to_str = naming_strategy().to_string

    def _get_location_string(self, locations, ctxt) -> list[str]:
        if locations == []:
            return []
        try:
            return _locns(locations, ctxt)[0][1]
        except BadReductionRequest:
            return locations

    def _make_request(
        self,
        requestName,
        locations,
        ctxt=None,
        expression=None,
        weight=None,
        condition=None,
    ) -> Any:
        request = getattr(reduction_pb2, requestName)()
        if expression is not None:
            if hasattr(expression, "definition"):
                expression = expression.definition()
            request.expression = self._to_str(expression)
        if weight is not None:
            request.weight = Weight(weight).value
        if condition is not None:
            request.condition = condition
        request.locations.extend(self._get_location_string(locations, ctxt))
        return request

    def area(self, locations, ctxt=None) -> Any:
        """Get area."""
        request = self._make_request("AreaRequest", locations, ctxt)
        response = self._stub.Area(request, metadata=self._metadata)
        return _convert_variant_to_value(response.value)

    def area_average(self, expression, locations, ctxt=None) -> Any:
        """Get area average."""
        request = self._make_request("AreaAveRequest", locations, ctxt, expression)
        response = self._stub.AreaAve(request, metadata=self._metadata)
        return _convert_variant_to_value(response.value)

    def area_integral(self, expression, locations, ctxt=None) -> Any:
        """Get area integral."""
        request = self._make_request("AreaIntRequest", locations, ctxt, expression)
        response = self._stub.AreaInt(request, metadata=self._metadata)
        return _convert_variant_to_value(response.value)

    def centroid(self, locations, ctxt=None) -> Any:
        """Get centroid."""
        request = self._make_request("CentroidRequest", locations, ctxt)
        response = self._stub.Centroid(request, metadata=self._metadata)
        return (response.value.x, response.value.y, response.value.z)

    def count(self, locations, ctxt=None) -> Any:
        """Count the number of faces or cells within the locations."""
        request = self._make_request("CountRequest", locations, ctxt)
        response = self._stub.Count(request, metadata=self._metadata)
        return _convert_variant_to_value(response.value)

    def count_if(self, condition, locations, ctxt=None) -> Any:
        """Count the number of faces or cells where the specified condition is satisfied."""
        request = self._make_request(
            "CountIfRequest", locations, ctxt, expression=condition
        )
        response = self._stub.CountIf(request, metadata=self._metadata)
        return _convert_variant_to_value(response.value)

    def force(self, locations, ctxt=None) -> Any:
        """Get force."""
        request = self._make_request("ForceRequest", locations, ctxt)
        response = self._stub.Force(request, metadata=self._metadata)
        return (response.value.x, response.value.y, response.value.z)

    def mass_average(self, expression, locations, ctxt=None) -> Any:
        """Get mass average."""
        request = self._make_request("MassAveRequest", locations, ctxt, expression)
        response = self._stub.MassAve(request, metadata=self._metadata)
        return _convert_variant_to_value(response.value)

    def mass_flow_average(self, expression, locations, ctxt=None) -> Any:
        """Get mass flow average."""
        request = self._make_request("MassFlowAveRequest", locations, ctxt, expression)
        response = self._stub.MassFlowAve(request, metadata=self._metadata)
        return _convert_variant_to_value(response.value)

    def mass_flow_average_absolute(self, expression, locations, ctxt=None) -> Any:
        """Compute the mass flow average of the absolute value of the given expression."""
        request = self._make_request(
            "MassFlowAveAbsRequest", locations, ctxt, expression
        )
        response = self._stub.MassFlowAveAbs(request, metadata=self._metadata)
        return _convert_variant_to_value(response.value)

    def mass_flow_integral(self, expression, locations, ctxt=None) -> Any:
        """Get mass flow integral."""
        request = self._make_request("MassFlowIntRequest", locations, ctxt, expression)
        response = self._stub.MassFlowInt(request, metadata=self._metadata)
        return _convert_variant_to_value(response.value)

    def mass_integral(self, expression, locations, ctxt=None) -> Any:
        """Get mass integral."""
        request = self._make_request("MassIntRequest", locations, ctxt, expression)
        response = self._stub.MassInt(request, metadata=self._metadata)
        return _convert_variant_to_value(response.value)

    def maximum(self, expression, locations, ctxt=None) -> Any:
        """Get maximum."""
        request = self._make_request("MaximumRequest", locations, ctxt, expression)
        response = self._stub.Maximum(request, metadata=self._metadata)
        return _convert_variant_to_value(response.value)

    def minimum(self, expression, locations, ctxt=None) -> Any:
        """Get minimum."""
        request = self._make_request("MinimumRequest", locations, ctxt, expression)
        response = self._stub.Minimum(request, metadata=self._metadata)
        return _convert_variant_to_value(response.value)

    def pressure_force(self, locations, ctxt=None) -> Any:
        """Get pressure force."""
        request = self._make_request("PressureForceRequest", locations, ctxt)
        response = self._stub.PressureForce(request, metadata=self._metadata)
        return (response.value.x, response.value.y, response.value.z)

    def viscous_force(self, locations, ctxt=None) -> Any:
        """Get viscous force."""
        request = self._make_request("ViscousForceRequest", locations, ctxt)
        response = self._stub.ViscousForce(request, metadata=self._metadata)
        return (response.value.x, response.value.y, response.value.z)

    def volume(self, locations, ctxt=None) -> Any:
        """Get volume."""
        request = self._make_request("VolumeRequest", locations, ctxt)
        response = self._stub.Volume(request, metadata=self._metadata)
        return _convert_variant_to_value(response.value)

    def volume_average(self, expression, locations, ctxt=None) -> Any:
        """Get volume average."""
        request = self._make_request("VolumeRequest", locations, ctxt, expression)
        response = self._stub.VolumeAve(request, metadata=self._metadata)
        return _convert_variant_to_value(response.value)

    def volume_integral(self, expression, locations, ctxt=None) -> Any:
        """Get volume integral."""
        request = self._make_request("VolumeIntRequest", locations, ctxt, expression)
        response = self._stub.VolumeInt(request, metadata=self._metadata)
        return _convert_variant_to_value(response.value)

    def moment(self, expression, locations, ctxt=None) -> Any:
        """Get moment."""
        request = self._make_request("MomentRequest", locations, ctxt, expression)
        response = self._stub.Moment(request, metadata=self._metadata)
        return (response.value.x, response.value.y, response.value.z)

    def sum(self, expression, locations, weight: str | Weight, ctxt=None) -> Any:
        """Get sum."""
        request = self._make_request("SumRequest", locations, ctxt, expression, weight)
        response = self._stub.Sum(request, metadata=self._metadata)
        return _convert_variant_to_value(response.value)

    def sum_if(
        self, expression, condition, locations, weight: str | Weight, ctxt=None
    ) -> Any:
        """Compute the weighted sum of the expression at locations where the given condition is satisfied."""
        request = self._make_request(
            "SumIfRequest", locations, ctxt, expression, weight, condition
        )
        response = self._stub.SumIf(request, metadata=self._metadata)
        return _convert_variant_to_value(response.value)
