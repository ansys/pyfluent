import functools

import grpc

from ansys.fluent import LOG


def catch_grpc_error(f):
    """
    Decorator to catch gRPC errors
    """

    @functools.wraps(f)
    def func(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except grpc.RpcError as ex:
            LOG.error("GRPC_ERROR: %s", ex.details())
            raise RuntimeError(ex.details()) from None

    return func
