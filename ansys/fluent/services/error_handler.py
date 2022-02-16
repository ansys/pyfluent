import functools
from typing import Any, Callable, Type, TypeVar

import grpc

from ansys.fluent import LOG

T = TypeVar("T")
F = TypeVar("F", bound=Callable[..., Any])


def catch_grpc_error(response_class: Type[T] = None) -> F:
    """
    Decorator to catch gRPC errors. If a response class is passed with
    the decorator, a default instance will be returned when a gRPC error
    occurs.

    Parameters
    ----------
    response_class : Type[T], optional
        response class, by default None

    """

    def catch_grpc_error_decorator(f: F) -> F:
        @functools.wraps(f)
        def func(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except grpc.RpcError as ex:
                LOG.error("GRPC_ERROR: %s", ex.details())
                if response_class:
                    return response_class()

        return func

    return catch_grpc_error_decorator
