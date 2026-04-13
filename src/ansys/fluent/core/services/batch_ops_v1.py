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

"""Batch RPC service (v1 proto API).

All shared logic lives in batch_ops.py (v0). This module keeps only
v1-specific proto and stub bindings required for compatibility.
"""

import importlib
import pkgutil

import ansys.api.fluent.v1 as api
from ansys.api.fluent.v1 import batch_ops_pb2, batch_ops_pb2_grpc
import ansys.fluent.core.services.batch_ops as _v0

network_logger = _v0.network_logger


class BatchOpsService(_v0.BatchOpsService):
    """Class wrapping methods in batch RPC service (v1 proto API)."""

    def _create_stub(self, intercept_channel):
        """Create the v1 gRPC stub."""
        return batch_ops_pb2_grpc.BatchOpsStub(intercept_channel)


class BatchOps(_v0.BatchOps):
    """Class to execute operations in batch in Fluent (v1 proto API)."""

    @staticmethod
    def _load_proto_modules():
        """Load v1 proto modules exposing DESCRIPTOR for batch support checks."""
        proto_modules = []
        for module_info in pkgutil.iter_modules(api.__path__, api.__name__ + "."):
            if not module_info.name.endswith("_pb2"):
                continue
            module = importlib.import_module(module_info.name)
            if hasattr(module, "DESCRIPTOR"):
                proto_modules.append(module)
        return proto_modules

    _api_module = api
    _proto_module = batch_ops_pb2
    _proto_files = _load_proto_modules.__func__()
