# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
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

"""Batch RPC service (v0 proto API)."""

import inspect
import logging
import sys
from types import ModuleType

import ansys.api.fluent.v0 as api
from ansys.api.fluent.v0 import batch_ops_pb2, batch_ops_pb2_grpc
from ansys.fluent.core.services._protocols import ServiceProtocol

network_logger: logging.Logger = logging.getLogger("pyfluent.networking")


class BatchOpsService(ServiceProtocol):
    """Class wrapping the batch RPC service of Fluent (v0 proto API)."""

    _api_module = api
    _proto_module = batch_ops_pb2

    def __init__(
        self,
        intercept_channel,
        metadata: list[tuple[str, str]],
    ) -> None:
        """__init__ method of BatchOpsService class."""
        self._stub = batch_ops_pb2_grpc.BatchOpsStub(intercept_channel)
        self._metadata = metadata
        self._proto_files: list[ModuleType] | None = None
        self._response_cls_cache: dict[tuple[str, str, str], type | None] = {}

    def _ensure_proto_files(self) -> None:
        """Lazily populate the list of all known proto file descriptors."""
        if self._proto_files is not None:
            return
        owner_proto_files = [
            mod
            for _, mod in inspect.getmembers(self._api_module, inspect.ismodule)
            if hasattr(mod, "DESCRIPTOR")
        ]
        loaded_proto_files = [
            mod
            for name, mod in sys.modules.items()
            if name.endswith("_pb2") and hasattr(mod, "DESCRIPTOR")
        ]
        self._proto_files = owner_proto_files + [
            mod for mod in loaded_proto_files if mod not in owner_proto_files
        ]

    def _get_response_cls(self, package: str, service: str, method: str) -> type | None:
        """Return the proto response class for the given RPC, or None if not found."""
        key = (package, service, method)
        if key in self._response_cls_cache:
            return self._response_cls_cache[key]
        self._ensure_proto_files()
        result = None
        for file in self._proto_files:
            file_desc = file.DESCRIPTOR
            if file_desc.package == package:
                service_desc = file_desc.services_by_name.get(service)
                if service_desc:
                    method_desc = service_desc.methods_by_name.get(method)
                    if (
                        method_desc
                        and not method_desc.client_streaming
                        and not method_desc.server_streaming
                    ):
                        response_cls_name = method_desc.output_type.name
                        try:
                            result = getattr(file, response_cls_name)
                            break
                        except AttributeError:
                            pass
        self._response_cls_cache[key] = result
        return result

    def get_op_metadata(
        self, package: str, service: str, method: str
    ) -> tuple[bool, type | None]:
        """Return ``(is_supported, response_cls)`` for the given RPC.

        An operation is considered supported when it is not a getter and the
        proto descriptor exposes a non-streaming unary response type.
        """
        if method.startswith("Get") or method.startswith("get"):
            return False, None
        response_cls = self._get_response_cls(package, service, method)
        return response_cls is not None, response_cls

    def execute(self, ops: list) -> list[tuple]:
        """Execute a batch of queued operations and return ``(status, result)`` pairs.

        Execute is a bidirectional-streaming RPC: the client sends a stream of
        ``ExecuteRequest`` messages and the server returns a corresponding
        stream of ``ExecuteResponse`` messages.  Each response is deserialized
        into the appropriate proto message type before being returned.
        """
        requests = (
            self._proto_module.ExecuteRequest(
                package=op._package,
                service=op._service_name,
                method=op._method,
                request_body=op._request_body,
            )
            for op in ops
        )
        results = []
        for op, response in zip(
            ops, self._stub.Execute(requests, metadata=self._metadata)
        ):
            result = None
            if op.response_cls is not None:
                result = op.response_cls()
                try:
                    result.ParseFromString(response.response_body)
                except Exception as ex:
                    network_logger.warning(ex)
            results.append((response.status, result))
        return results
