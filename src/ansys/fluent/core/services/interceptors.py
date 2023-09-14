"""Interceptor classes to use with gRPC services."""

import logging
import os
from typing import Any

from google.protobuf.json_format import MessageToDict
import grpc

from ansys.fluent.core.services.batch_ops import BatchOps

network_logger = logging.getLogger("pyfluent.networking")
log_bytes_limit = int(os.getenv("PYFLUENT_GRPC_LOG_BYTES_LIMIT", 1000))
truncate_len = log_bytes_limit // 5


def _truncate_grpc_str(message):
    message_bytes = message.ByteSize()
    message_str = str(MessageToDict(message))
    if not log_bytes_limit or message_bytes < log_bytes_limit:
        return message_str
    else:
        network_logger.debug(
            f"GRPC_TRACE: message partially hidden, {message_bytes} bytes > "
            f"{log_bytes_limit} bytes limit. To see the full message, set PYFLUENT_GRPC_LOG_BYTES_LIMIT to 0."
        )
        return f"{message_str[:truncate_len]} < ... > {message_str[-truncate_len:]}"


class TracingInterceptor(grpc.UnaryUnaryClientInterceptor):
    """Interceptor class to trace gRPC calls."""

    def __init__(self):
        """__init__ method of TracingInterceptor class."""
        super().__init__()

    def _intercept_call(
        self,
        continuation: Any,
        client_call_details: grpc.ClientCallDetails,
        request: Any,
    ):
        network_logger.debug(
            f"GRPC_TRACE: rpc = {client_call_details.method}, request = {_truncate_grpc_str(request)}"
        )
        response = continuation(client_call_details, request)
        if not response.exception():
            # call _truncate_grpc_str early to get the size warning even when hiding secrets
            response_str = _truncate_grpc_str(response.result())
            if os.getenv("PYFLUENT_HIDE_LOG_SECRETS") != "1":
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
    """Interceptor class to check Fluent server error state before gRPC calls are made."""

    def __init__(self, fluent_error_state):
        """__init__ method of ErrorStateInterceptor class."""
        super().__init__()
        self._fluent_error_state = fluent_error_state

    def _intercept_call(
        self,
        continuation: Any,
        client_call_details: grpc.ClientCallDetails,
        request: Any,
    ):
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


class BatchedFuture(grpc.Future):
    """Class implementing gRPC.Future interface.

    An instance of BatchedFuture is returned if the gRPC method is
    queued to be executed in batch later.
    """

    def __init__(self, result_cls):
        """__init__ method of BatchedFuture class."""
        self._result_cls = result_cls

    def cancel(self):
        """Attempts to cancel the computation."""
        return False

    def cancelled(self):
        """Describes whether the computation was cancelled."""
        return False

    def running(self):
        """Describes whether the computation is taking place."""
        return False

    def done(self):
        """Describes whether the computation has taken place."""
        return True

    def result(self, timeout=None):
        """Returns the result of the computation or raises its exception."""
        return self._result_cls()

    def exception(self, timeout=None):
        """Return the exception raised by the computation."""
        return None

    def traceback(self, timeout=None):
        """Access the traceback of the exception raised by the computation."""
        return None

    def add_done_callback(self, fn):
        """Adds a function to be called at completion of the computation."""
        pass


class BatchInterceptor(grpc.UnaryUnaryClientInterceptor):
    """Interceptor class to batch gRPC calls."""

    def __init__(self):
        """__init__ method of BatchInterceptor class."""
        super().__init__()

    def _intercept_call(
        self,
        continuation: Any,
        client_call_details: grpc.ClientCallDetails,
        request: Any,
    ):
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
