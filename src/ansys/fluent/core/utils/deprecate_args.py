"""Module that provides a method to handle deprecated arguments."""

import functools
import warnings


def deprecate_argument(
    old_arg, new_arg, converter, deprecation_class=DeprecationWarning
):
    """Warns user that the argument provided is deprecated, and automatically replaces
    the deprecated argument with the appropriate new argument."""

    def decorator(func):
        """Holds the original method to perform operations on it."""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """Warns about the deprecated argument and replaces it with the new
            argument."""
            if old_arg in kwargs:
                warnings.warn(
                    f"'{old_arg}' is deprecated. Using '{new_arg}' instead.",
                    deprecation_class,
                )
                new_value = converter(kwargs[old_arg])
                if new_value is not None and kwargs.get(new_arg) is None:
                    kwargs[new_arg] = new_value
                kwargs.pop(old_arg)
            return func(*args, **kwargs)

        return wrapper

    return decorator
