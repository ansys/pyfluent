"""Deprecates old argument and replaces them with corresponding new argument."""

import functools
import warnings


def deprecate_arguments(
    old_arg, new_arg, converter, deprecation_class=DeprecationWarning
):
    """Deprecates old argument and replaces them with corresponding new argument."""

    def decorator(func):
        """Holds the original method to perform operations on it."""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """Performs deprecation operation on arguments of the original method."""
            if old_arg in kwargs:
                warnings.warn(
                    f"'{old_arg}' is deprecated. Use '{new_arg}' instead.",
                    deprecation_class,
                )
                val = converter(kwargs[old_arg])
                if val is not None:
                    kwargs[new_arg] = val
                kwargs.pop(old_arg)
            return func(*args, **kwargs)

        return wrapper

    return decorator
