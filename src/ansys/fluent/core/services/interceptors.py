"""Interceptor classes to use with gRPC services."""

from typing import Any

from google.protobuf.json_format import MessageToDict
import grpc

from ansys.fluent.core.services.batch_ops import BatchOps
from ansys.fluent.core.utils.logging import LOG


class TracingInterceptor(grpc.UnaryUnaryClientInterceptor):
    """Interceptor class to trace gRPC calls."""

    def _intercept_call(
        self,
        continuation: Any,
        client_call_details: grpc.ClientCallDetails,
        request: Any,
    ):
        LOG.debug(
            "GRPC_TRACE: rpc = %s, request = %s",
            client_call_details.method,
            MessageToDict(request),
        )
        response = continuation(client_call_details, request)
        if not response.exception():
            LOG.debug(
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
        return self._intercept_call(continuation, client_call_details, request)


class BatchedFuture(grpc.Future):
    """
    Class implementing gRPC.Future interface. An instance of BatchedFuture is returned
    if the gRPC method is queued to be executed in batch later.
    """
    def __init__(self, result_cls):
        self._result_cls = result_cls

    def cancel(self):
        return False

    def cancelled(self):
        return False

    def running(self):
        return False

    def done(self):
        return True

    def result(self, timeout=None):
        return self._result_cls()

    def exception(self, timeout=None):
        return None

    def traceback(self, timeout=None):
        return None

    def add_done_callback(self, fn):
        pass


class BatchInterceptor(grpc.UnaryUnaryClientInterceptor):
    """Interceptor class to batch gRPC calls."""

    def _intercept_call(
        self,
        continuation: Any,
        client_call_details: grpc.ClientCallDetails,
        request: Any,
    ):
        currentBatchOps = BatchOps.get_current()
        if currentBatchOps:
            qual_method = client_call_details.method
            package_and_service, method = qual_method.lstrip("/").split("/")
            package, service = package_and_service.rsplit(".", 1)
            op = currentBatchOps.add_op(package, service, method, request)
            if op.queued:
                return BatchedFuture(op.response_cls)

        return continuation(client_call_details, request)

    def intercept_unary_unary(
        self,
        continuation: Any,
        client_call_details: grpc.ClientCallDetails,
        request: Any,
    ) -> Any:
        return self._intercept_call(continuation, client_call_details, request)