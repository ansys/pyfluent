"""Provides a module for Metaclasses."""

from abc import ABCMeta


class SingletonMeta(type):
    """Provides the metaclass for the singleton type."""

    _single_instance = None

    def __call__(cls, *args, **kwargs):
        if not cls._single_instance:
            cls._single_instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._single_instance


class AbstractSingletonMeta(ABCMeta, SingletonMeta):
    """Meta class for abstract singleton type."""

    pass
