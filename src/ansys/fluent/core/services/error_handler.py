import functools
from typing import Callable

import grpc


def catch_grpc_error(f: Callable) -> Callable:
    """Decorator to catch gRPC errors."""

    @functools.wraps(f)
    def func(*args, **kwargs) -> Callable:
        # return f(*args, **kwargs)
        try:
            return f(*args, **kwargs)
        except grpc.RpcError as ex:
            raise RuntimeError(ex.details()) from None

    return func
