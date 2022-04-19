import functools
from typing import Callable

import grpc

from ansys.fluent.core.utils.logging import LOG


def catch_grpc_error(f: Callable) -> Callable:
    """Decorator to catch gRPC errors."""

    @functools.wraps(f)
    def func(*args, **kwargs) -> Callable:
        try:
            return f(*args, **kwargs)
        except grpc.RpcError as ex:
            LOG.error("GRPC_ERROR: %s", ex.details())
            raise RuntimeError(ex.details()) from None

    return func
