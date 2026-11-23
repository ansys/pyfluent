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

from unittest.mock import Mock

import pytest

from ansys.api.fluent.v1 import reduction_pb2, variant_pb2
from ansys.fluent.core._grpc_services.reduction_service import ReductionService
from ansys.fluent.core.fields.reduction import Reduction


@pytest.mark.parametrize(
    "method_name,args,rpc_name,request_type,response_type",
    [
        (
            "volume",
            (),
            "Volume",
            reduction_pb2.VolumeRequest,
            reduction_pb2.VolumeResponse,
        ),
        (
            "volume_average",
            ("Temperature",),
            "VolumeAve",
            reduction_pb2.VolumeAveRequest,
            reduction_pb2.VolumeAveResponse,
        ),
        (
            "volume_integral",
            ("Temperature",),
            "VolumeInt",
            reduction_pb2.VolumeIntRequest,
            reduction_pb2.VolumeIntResponse,
        ),
    ],
)
def test_volume_reduction_request(
    method_name, args, rpc_name, request_type, response_type
):
    service = ReductionService(Mock(), [])
    service._stub = Mock()
    rpc = getattr(service._stub, rpc_name)
    rpc.return_value = response_type(value=variant_pb2.Variant(double_state=300.0))
    expected = request_type(locations=["fluid"])
    if args:
        expected.expression = "Temperature"

    assert getattr(Reduction(service), method_name)(*args, locations=["fluid"]) == 300.0
    rpc.assert_called_once_with(expected, metadata=[])
