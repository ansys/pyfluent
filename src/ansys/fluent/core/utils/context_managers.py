"""Module for context managers used in PyFluent."""

from contextlib import contextmanager
from threading import local

_thread_local = local()


def _get_stack():
    if not hasattr(_thread_local, "stack"):
        _thread_local.stack = []
    return _thread_local.stack


@contextmanager
def using(session):
    """Context manager to use a Fluent session."""
    stack = _get_stack()
    stack.append(session)
    try:
        yield
    finally:
        stack.pop()
