"""Interceptor classes to use with gRPC services."""

from typing import Any

from google.protobuf.json_format import MessageToDict
import grpc

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
