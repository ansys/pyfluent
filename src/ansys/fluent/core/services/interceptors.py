"""Interceptor classes to use with gRPC services."""

import logging
from typing import Any

from google.protobuf.json_format import MessageToDict
import grpc

from ansys.fluent.core.services.batch_ops import BatchOps

network_logger = logging.getLogger("ansys.fluent.networking")


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
            "GRPC_TRACE: rpc = %s, request = %s",
            client_call_details.method,
            MessageToDict(request),
        )
        response = continuation(client_call_details, request)
        if not response.exception():
            network_logger.debug(
                "GRPC_TRACE: response = %s",
                MessageToDict(response.result()),
            )
        return response

    def intercept_unary_unary(
        self,
        continuation: Any,
        client_call_details: grpc.ClientCallDetails,
        request: Any,
    ) -> Any:
        """Intercept unary-unary call for tracing."""
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
