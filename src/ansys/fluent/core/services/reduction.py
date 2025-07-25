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

"""Wrappers over Reduction gRPC service of Fluent."""
from collections.abc import Iterable
from typing import Any, List, Tuple
import weakref

import grpc

from ansys.api.fluent.v0 import reduction_pb2 as ReductionProtoModule
from ansys.api.fluent.v0 import reduction_pb2_grpc as ReductionGrpcModule
from ansys.fluent.core.exceptions import DisallowedValuesError
from ansys.fluent.core.services.datamodel_se import _convert_variant_to_value
from ansys.fluent.core.services.interceptors import (
    BatchInterceptor,
    ErrorStateInterceptor,
    GrpcErrorInterceptor,
    TracingInterceptor,
)
from ansys.fluent.core.solver.function.reduction import Weight
from ansys.fluent.core.variable_strategies import (
    FluentExprNamingStrategy as naming_strategy,
)

Path = List[Tuple[str, str]]


class ReductionService:
    """Reduction Service."""

    def __init__(
        self, channel: grpc.Channel, metadata: List[Tuple[str, str]], fluent_error_state
    ):
        """__init__ method of Reduction class."""
        intercept_channel = grpc.intercept_channel(
            channel,
            GrpcErrorInterceptor(),
            ErrorStateInterceptor(fluent_error_state),
            TracingInterceptor(),
            BatchInterceptor(),
        )
        self._stub = ReductionGrpcModule.ReductionStub(intercept_channel)
        self._metadata = metadata

    def area(
        self, request: ReductionProtoModule.AreaRequest
    ) -> ReductionProtoModule.AreaResponse:
        """Area RPC of Reduction service."""
        return self._stub.Area(request, metadata=self._metadata)

    def area_average(
        self, request: ReductionProtoModule.AreaAveRequest
    ) -> ReductionProtoModule.AreaAveResponse:
        """Area average RPC of Reduction service."""
        return self._stub.AreaAve(request, metadata=self._metadata)

    def area_integral(
        self, request: ReductionProtoModule.AreaIntRequest
    ) -> ReductionProtoModule.AreaIntResponse:
        """Area integral RPC of Reduction service."""
        return self._stub.AreaInt(request, metadata=self._metadata)

    def centroid(
        self, request: ReductionProtoModule.CentroidRequest
    ) -> ReductionProtoModule.CentroidResponse:
        """Centroid RPC of Reduction service."""
        return self._stub.Centroid(request, metadata=self._metadata)

    def count(
        self, request: ReductionProtoModule.CountRequest
    ) -> ReductionProtoModule.CountResponse:
        """Count RPC of Reduction service."""
        return self._stub.Count(request, metadata=self._metadata)

    def count_if(
        self, request: ReductionProtoModule.CountIfRequest
    ) -> ReductionProtoModule.CountIfResponse:
        """Count If RPC of Reduction service."""
        return self._stub.CountIf(request, metadata=self._metadata)

    def force(
        self, request: ReductionProtoModule.ForceRequest
    ) -> ReductionProtoModule.ForceResponse:
        """Force RPC of Reduction service."""
        return self._stub.Force(request, metadata=self._metadata)

    def mass_average(
        self, request: ReductionProtoModule.MassAveRequest
    ) -> ReductionProtoModule.MassAveResponse:
        """Mass average RPC of Reduction service."""
        return self._stub.MassAve(request, metadata=self._metadata)

    def mass_flow_average(
        self, request: ReductionProtoModule.MassFlowAveRequest
    ) -> ReductionProtoModule.MassFlowAveResponse:
        """Mass flow average RPC of Reduction service."""
        return self._stub.MassFlowAve(request, metadata=self._metadata)

    def mass_flow_average_absolute(
        self, request: ReductionProtoModule.MassFlowAveAbsRequest
    ) -> ReductionProtoModule.MassFlowAveAbsResponse:
        """Absolute mass flow average RPC of Reduction service."""
        return self._stub.MassFlowAveAbs(request, metadata=self._metadata)

    def mass_flow_integral(
        self, request: ReductionProtoModule.MassFlowIntRequest
    ) -> ReductionProtoModule.MassFlowIntResponse:
        """Mass flow integral RPC of Reduction service."""
        return self._stub.MassFlowInt(request, metadata=self._metadata)

    def mass_integral(
        self, request: ReductionProtoModule.MassIntRequest
    ) -> ReductionProtoModule.MassIntResponse:
        """Mass integral RPC of Reduction service."""
        return self._stub.MassInt(request, metadata=self._metadata)

    def maximum(
        self, request: ReductionProtoModule.MaximumRequest
    ) -> ReductionProtoModule.MaximumResponse:
        """Maximum RPC of Reduction service."""
        return self._stub.Maximum(request, metadata=self._metadata)

    def minimum(
        self, request: ReductionProtoModule.MinimumRequest
    ) -> ReductionProtoModule.MinimumResponse:
        """Minimum RPC of Reduction service."""
        return self._stub.Minimum(request, metadata=self._metadata)

    def pressure_force(
        self, request: ReductionProtoModule.PressureForceRequest
    ) -> ReductionProtoModule.PressureForceResponse:
        """Pressure force RPC of Reduction service."""
        return self._stub.PressureForce(request, metadata=self._metadata)

    def viscous_force(
        self, request: ReductionProtoModule.ViscousForceRequest
    ) -> ReductionProtoModule.ViscousForceResponse:
        """Viscous force RPC of Reduction service."""
        return self._stub.ViscousForce(request, metadata=self._metadata)

    def volume(
        self, request: ReductionProtoModule.VolumeRequest
    ) -> ReductionProtoModule.VolumeResponse:
        """Volume RPC of Reduction service."""
        return self._stub.Volume(request, metadata=self._metadata)

    def volume_average(
        self, request: ReductionProtoModule.VolumeAveRequest
    ) -> ReductionProtoModule.VolumeAveResponse:
        """Volume average RPC of Reduction service."""
        return self._stub.VolumeAve(request, metadata=self._metadata)

    def volume_integral(
        self, request: ReductionProtoModule.VolumeIntRequest
    ) -> ReductionProtoModule.VolumeIntResponse:
        """Volume integral RPC of Reduction service."""
        return self._stub.VolumeInt(request, metadata=self._metadata)

    def moment(
        self, request: ReductionProtoModule.MomentRequest
    ) -> ReductionProtoModule.MomentResponse:
        """Moment RPC of Reduction service."""
        return self._stub.Moment(request, metadata=self._metadata)

    def sum(
        self, request: ReductionProtoModule.SumRequest
    ) -> ReductionProtoModule.SumResponse:
        """Sum RPC of Reduction service."""
        return self._stub.Sum(request, metadata=self._metadata)

    def sum_if(
        self, request: ReductionProtoModule.SumIfRequest
    ) -> ReductionProtoModule.SumIfResponse:
        """Sum RPC of Reduction service."""
        return self._stub.SumIf(request, metadata=self._metadata)


class BadReductionRequest(Exception):
    """Raised on an attempt to make a bad reduction request."""

    def __init__(self, err):
        """Initialize BadReductionRequest."""
        super().__init__(f"Could not complete reduction function request: {err}")


def _validate_locn_list(locn_list, ctxt):
    if not all(locn[0] for locn in locn_list) and (
        any(locn[0] for locn in locn_list) or not ctxt
    ):
        raise BadReductionRequest("Invalid combination of arguments")


def _is_iterable(obj):
    return hasattr(type(obj), "__iter__")


def _expand_locn_container(locns):
    try:
        return [[locn, locns] for locn in locns]
    except TypeError as ex:
        raise BadReductionRequest(ex)


def _locn_name_and_obj(locn, locns):
    if isinstance(locn, str):
        return [locn, locns]
    # should call locn_get_name()
    if _is_iterable(locn):
        return _locn_names_and_objs(locn)
    else:
        return [locn.obj_name, locn]


def _locn_names_and_objs(locns):
    if _is_iterable(locns):
        names_and_objs = []
        for locn in locns:
            name_and_obj = _locn_name_and_obj(locn, locns)
            if _is_iterable(name_and_obj):
                if isinstance(name_and_obj[0], str):
                    names_and_objs.append(name_and_obj)
                else:
                    names_and_objs.extend(name_and_obj)
        return names_and_objs
    else:
        return _expand_locn_container(locns)


def _root(obj):
    return (
        None
        if isinstance(obj, list)
        else obj if not getattr(obj, "obj_name", None) else _root(obj._parent)
    )


def _locns(locns, ctxt=None):
    locn_names_and_objs = _locn_names_and_objs(locns)
    locn_list = []
    for name, obj in locn_names_and_objs:
        root = _root(obj)
        found = False
        for locn in locn_list:
            if locn[0] is root:
                locn[1].append(name)
                found = True
                break
        if not found:
            locn_list.append([root, [name]])
    _validate_locn_list(locn_list, ctxt)
    return locn_list


class Reduction:
    """Reduction."""

    def __init__(self, service: ReductionService, ctxt=None):
        """__init__ method of Reduction class."""
        self.service = service
        self.ctxt = weakref.proxy(ctxt)
        self._to_str = naming_strategy().to_string

    def _validate_str_location(self, loc: str):
        if all(
            loc not in names()
            for names in (
                self.ctxt.fields.field_data.surfaces,
                self.ctxt.settings.setup.cell_zone_conditions,
            )
        ):
            raise ValueError(f"Invalid location input: '{loc}'")

    def _get_location_string(self, locations, ctxt) -> List[str]:
        if locations == []:
            return []
        for loc in locations:
            if isinstance(loc, Iterable) and not isinstance(loc, (str, bytes)):
                raise DisallowedValuesError("location", loc, list(loc))
            if isinstance(loc, str):
                self._validate_str_location(loc)
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
        request = getattr(ReductionProtoModule, requestName)()
        if expression is not None:
            request.expression = self._to_str(expression)
        if weight is not None:
            request.weight = Weight(weight).value
        if condition is not None:
            request.condition = condition
        request.locations.extend(self._get_location_string(locations, ctxt))
        return request

    @property
    def weight(self):
        """Weight for calculating sum."""
        return Weight

    def area(self, locations, ctxt=None) -> Any:
        """Get area."""
        request = self._make_request("AreaRequest", locations, ctxt)
        response = self.service.area(request)
        return _convert_variant_to_value(response.value)

    def area_average(self, expression, locations, ctxt=None) -> Any:
        """Get area average."""
        request = self._make_request("AreaAveRequest", locations, ctxt, expression)
        response = self.service.area_average(request)
        return _convert_variant_to_value(response.value)

    def area_integral(self, expression, locations, ctxt=None) -> Any:
        """Get area integral."""
        request = self._make_request("AreaIntRequest", locations, ctxt, expression)
        response = self.service.area_integral(request)
        return _convert_variant_to_value(response.value)

    def centroid(self, locations, ctxt=None) -> Any:
        """Get centroid."""
        request = self._make_request("CentroidRequest", locations, ctxt)
        response = self.service.centroid(request)
        return (response.value.x, response.value.y, response.value.z)

    def count(self, locations, ctxt=None) -> Any:
        """Count the number of faces or cells within the locations."""
        request = self._make_request("CountRequest", locations, ctxt)
        response = self.service.count(request)
        return _convert_variant_to_value(response.value)

    def count_if(self, condition, locations, ctxt=None) -> Any:
        """Count the number of faces or cells where the specified condition is satisfied."""
        request = self._make_request(
            "CountIfRequest", locations, ctxt, expression=condition
        )
        response = self.service.count_if(request)
        return _convert_variant_to_value(response.value)

    def force(self, locations, ctxt=None) -> Any:
        """Get force."""
        request = self._make_request("ForceRequest", locations, ctxt)
        response = self.service.force(request)
        return (response.value.x, response.value.y, response.value.z)

    def mass_average(self, expression, locations, ctxt=None) -> Any:
        """Get mass average."""
        request = self._make_request("MassAveRequest", locations, ctxt, expression)
        response = self.service.mass_average(request)
        return _convert_variant_to_value(response.value)

    def mass_flow_average(self, expression, locations, ctxt=None) -> Any:
        """Get mass flow average."""
        request = self._make_request("MassFlowAveRequest", locations, ctxt, expression)
        response = self.service.mass_flow_average(request)
        return _convert_variant_to_value(response.value)

    def mass_flow_average_absolute(self, expression, locations, ctxt=None) -> Any:
        """Compute the mass flow average of the absolute value of the given expression."""
        request = self._make_request(
            "MassFlowAveAbsRequest", locations, ctxt, expression
        )
        response = self.service.mass_flow_average_absolute(request)
        return _convert_variant_to_value(response.value)

    def mass_flow_integral(self, expression, locations, ctxt=None) -> Any:
        """Get mass flow integral."""
        request = self._make_request("MassFlowIntRequest", locations, ctxt, expression)
        response = self.service.mass_flow_integral(request)
        return _convert_variant_to_value(response.value)

    def mass_integral(self, expression, locations, ctxt=None) -> Any:
        """Get mass integral."""
        request = self._make_request("MassIntRequest", locations, ctxt, expression)
        response = self.service.mass_integral(request)
        return _convert_variant_to_value(response.value)

    def maximum(self, expression, locations, ctxt=None) -> Any:
        """Get maximum."""
        request = self._make_request("MaximumRequest", locations, ctxt, expression)
        response = self.service.maximum(request)
        return _convert_variant_to_value(response.value)

    def minimum(self, expression, locations, ctxt=None) -> Any:
        """Get minimum."""
        request = self._make_request("MinimumRequest", locations, ctxt, expression)
        response = self.service.minimum(request)
        return _convert_variant_to_value(response.value)

    def pressure_force(self, locations, ctxt=None) -> Any:
        """Get pressure force."""
        request = self._make_request("PressureForceRequest", locations, ctxt)
        response = self.service.pressure_force(request)
        return (response.value.x, response.value.y, response.value.z)

    def viscous_force(self, locations, ctxt=None) -> Any:
        """Get viscous force."""
        request = self._make_request("ViscousForceRequest", locations, ctxt)
        response = self.service.viscous_force(request)
        return (response.value.x, response.value.y, response.value.z)

    def volume(self, locations, ctxt=None) -> Any:
        """Get volume."""
        request = self._make_request("VolumeRequest", locations, ctxt)
        response = self.service.volume(request)
        return _convert_variant_to_value(response.value)

    def volume_average(self, expression, locations, ctxt=None) -> Any:
        """Get volume average."""
        request = self._make_request("VolumeRequest", locations, ctxt, expression)
        response = self.service.volume_average(request)
        return _convert_variant_to_value(response.value)

    def volume_integral(self, expression, locations, ctxt=None) -> Any:
        """Get volume integral."""
        request = self._make_request("VolumeIntRequest", locations, ctxt, expression)
        response = self.service.volume_integral(request)
        return _convert_variant_to_value(response.value)

    def moment(self, expression, locations, ctxt=None) -> Any:
        """Get moment."""
        request = self._make_request("MomentRequest", locations, ctxt, expression)
        response = self.service.moment(request)
        return (response.value.x, response.value.y, response.value.z)

    def sum(self, expression, locations, weight: str | Weight, ctxt=None) -> Any:
        """Get sum."""
        request = self._make_request("SumRequest", locations, ctxt, expression, weight)
        response = self.service.sum(request)
        return _convert_variant_to_value(response.value)

    def sum_if(
        self, expression, condition, locations, weight: str | Weight, ctxt=None
    ) -> Any:
        """Compute the weighted sum of the expression at locations where the given condition is satisfied."""
        request = self._make_request(
            "SumIfRequest", locations, ctxt, expression, weight, condition
        )
        response = self.service.sum_if(request)
        return _convert_variant_to_value(response.value)
