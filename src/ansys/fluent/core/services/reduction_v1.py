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

"""Wrappers over Reduction gRPC service of Fluent (v1 proto API).

All shared logic lives in reduction.py (v0). This module keeps only
v1-specific proto and stub bindings for compatibility.
"""

from ansys.api.fluent.v1 import reduction_pb2 as ReductionProtoModule
from ansys.api.fluent.v1 import reduction_pb2_grpc as ReductionGrpcModule
import ansys.fluent.core.services.reduction as _v0

# Re-export shared helpers/types for compatibility with legacy imports.
Path = _v0.Path
BadReductionRequest = _v0.BadReductionRequest
_validate_locn_list = _v0._validate_locn_list
_is_iterable = _v0._is_iterable
_expand_locn_container = _v0._expand_locn_container
_locn_name_and_obj = _v0._locn_name_and_obj
_locn_names_and_objs = _v0._locn_names_and_objs
_root = _v0._root
_locns = _v0._locns
Weight = _v0.Weight


class ReductionService(_v0.ReductionService):
    """Reduction service of Fluent (v1 proto API)."""

    def _create_stub(self, intercept_channel):
        """Create the v1 gRPC stub."""
        return ReductionGrpcModule.ReductionStub(intercept_channel)


class Reduction(_v0.Reduction):
    """Reduction (v1 proto API)."""

    _proto_module = ReductionProtoModule
