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

"""Interceptor classes to use with gRPC services."""

import builtins
import logging
from typing import Any

from google.protobuf.json_format import MessageToDict
from google.protobuf.message import DecodeError, Message
import grpc

from ansys.fluent.core.services.batch_ops import BatchOps

network_logger: logging.Logger = logging.getLogger("pyfluent.networking")


def _upper_snake_case_to_camel_case(name: str) -> str:
    return "".join([word.capitalize() for word in name.split("_") if word])


def _truncate_grpc_str(message: Message) -> str:
    from ansys.fluent.core import config

    truncate_len = config.grpc_log_bytes_limit // 5
    message_bytes = message.ByteSize()
    message_str = str(MessageToDict(message))
    if not config.grpc_log_bytes_limit or message_bytes < config.grpc_log_bytes_limit:
        return message_str
    else:
        network_logger.debug(
            f"GRPC_TRACE: message partially hidden, {message_bytes} bytes > "
            f"{config.grpc_log_bytes_limit} bytes limit. To see the full message, set PYFLUENT_GRPC_LOG_BYTES_LIMIT to 0."
        )
        return f"{message_str[:truncate_len]} < ... > {message_str[-truncate_len:]}"


class TracingInterceptor(grpc.UnaryUnaryClientInterceptor):
    """Interceptor class to trace gRPC calls."""

    def __init__(self) -> None:
        """__init__ method of TracingInterceptor class."""
        super().__init__()

    def _intercept_call(
        self,
        continuation: Any,
        client_call_details: grpc.ClientCallDetails,
        request: Any,
    ) -> Any:
        from ansys.fluent.core import config

        network_logger.debug(
            f"GRPC_TRACE: RPC = {client_call_details.method}, request = {_truncate_grpc_str(request)}"
        )
        response = continuation(client_call_details, request)
        if not response.exception():
            # call _truncate_grpc_str early to get the size warning even when hiding secrets
            response_str = _truncate_grpc_str(response.result())
            if not config.hide_log_secrets:
                network_logger.debug(f"GRPC_TRACE: response = {response_str}")
        return response

    def intercept_unary_unary(
        self,
        continuation: Any,
        client_call_details: grpc.ClientCallDetails,
        request: Any,
    ) -> Any:
        """Intercept unary-unary call for tracing."""
        return self._intercept_call(continuation, client_call_details, request)


class ErrorStateInterceptor(grpc.UnaryUnaryClientInterceptor):
    """Interceptor class to check Fluent server error state before gRPC calls are
    made."""

    def __init__(self, fluent_error_state) -> None:
        """__init__ method of ErrorStateInterceptor class."""
        super().__init__()
        self._fluent_error_state = fluent_error_state

    def _intercept_call(
        self,
        continuation: Any,
        client_call_details: grpc.ClientCallDetails,
        request: Any,
    ) -> Any:
        if self._fluent_error_state.name == "fatal":
            details = self._fluent_error_state.details
            raise RuntimeError(
                f"Fatal error identified on the Fluent server: {details}."
            )
        return continuation(client_call_details, request)

    def intercept_unary_unary(
        self,
        continuation: Any,
        client_call_details: grpc.ClientCallDetails,
        request: Any,
    ) -> Any:
        """Intercept unary-unary call for error state checking."""
        return self._intercept_call(continuation, client_call_details, request)


class GrpcErrorInterceptor(grpc.UnaryUnaryClientInterceptor):
    """Interceptor class to check Fluent server error state before gRPC calls are
    made."""

    def _intercept_call(
        self,
        continuation: Any,
        client_call_details: grpc.ClientCallDetails,
        request: Any,
    ) -> Any:
        response = continuation(client_call_details, request)
        if response.exception() is not None and response.code() != grpc.StatusCode.OK:
            new_ex_cls = RuntimeError
            try:
                from google.rpc import error_details_pb2
                from grpc_status import rpc_status

                status = rpc_status.from_call(response)
                if status:
                    for detail in status.details:
                        if detail.Is(error_details_pb2.ErrorInfo.DESCRIPTOR):
                            info = error_details_pb2.ErrorInfo()
                            detail.Unpack(info)
                            if info.domain == "Python":
                                reason = info.reason
                                ex_cls_name = _upper_snake_case_to_camel_case(reason)
                                if hasattr(builtins, ex_cls_name):
                                    cls = getattr(builtins, ex_cls_name)
                                    if issubclass(cls, Exception):
                                        new_ex_cls = cls
                                        break
            except DecodeError:
                pass
            ex = response.exception()
            new_ex = new_ex_cls(
                ex.details() if isinstance(ex, grpc.RpcError) else str(ex)
            )
            new_ex.__context__ = ex
            raise new_ex from None
        return response

    def intercept_unary_unary(
        self,
        continuation: Any,
        client_call_details: grpc.ClientCallDetails,
        request: Any,
    ) -> Any:
        """Intercept unary-unary call for error state checking."""
        return self._intercept_call(continuation, client_call_details, request)


class BatchedFuture(grpc.Future):
    """Class implementing gRPC.Future interface.

    An instance of BatchedFuture is returned if the gRPC method is queued to be executed
    in batch later.
    """

    def __init__(self, result_cls) -> None:
        """__init__ method of BatchedFuture class."""
        self._result_cls = result_cls

    def cancel(self) -> bool:
        """Attempts to cancel the computation."""
        return False

    def cancelled(self) -> bool:
        """Describes whether the computation was cancelled."""
        return False

    def running(self) -> bool:
        """Describes whether the computation is taking place."""
        return False

    def done(self) -> bool:
        """Describes whether the computation has taken place."""
        return True

    def result(self, timeout=None) -> Any:
        """Returns the result of the computation or raises its exception."""
        return self._result_cls()

    def exception(self, timeout=None) -> None:
        """Return the exception raised by the computation."""
        return None

    def traceback(self, timeout=None) -> None:
        """Access the traceback of the exception raised by the computation."""
        return None

    def add_done_callback(self, fn) -> None:
        """Adds a function to be called at completion of the computation."""
        pass


class BatchInterceptor(grpc.UnaryUnaryClientInterceptor):
    """Interceptor class to batch gRPC calls."""

    def __init__(self) -> None:
        """__init__ method of BatchInterceptor class."""
        super().__init__()

    def _intercept_call(
        self,
        continuation: Any,
        client_call_details: grpc.ClientCallDetails,
        request: Any,
    ) -> Any:
        batchOps = BatchOps.instance()
        if batchOps and batchOps.batching:
            qual_method = client_call_details.method
            package_and_service, method = qual_method.lstrip("/").split("/")
            package, service = package_and_service.rsplit(".", 1)
            op = batchOps.add_op(package, service, method, request)
            if op.queued:
                return BatchedFuture(op.response_cls)

        return continuation(client_call_details, request)

    def intercept_unary_unary(
        self,
        continuation: Any,
        client_call_details: grpc.ClientCallDetails,
        request: Any,
    ) -> Any:
        """Intercept unary-unary call for batch operation."""
        return self._intercept_call(continuation, client_call_details, request)
