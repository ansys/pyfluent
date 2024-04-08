"""Provides a module for the event loop."""

import asyncio
from functools import partial

loop = asyncio.get_event_loop()


def execute_in_event_loop_threadsafe(f):
    """Decorates function to be executed in an event loop from another thread."""

    def cb(*args, **kwargs):
        par = partial(f, *args, **kwargs)
        loop.call_soon_threadsafe(par)

    return cb


def execute_in_event_loop(f):
    """Decorates function to be executed in an event loop."""

    def cb(*args, **kwargs):
        par = partial(f, *args, **kwargs)
        loop.call_soon(par)

    return cb
