"""Module that provides a method to handle deprecated arguments."""

import functools
import warnings

from ansys.fluent.core.launcher.pyfluent_enums import FluentEnum


def deprecate_argument(
    old_arg, new_arg, converter, deprecation_class=DeprecationWarning
):
    """Warns user that the argument provided is deprecated, and automatically replaces
    the deprecated argument with the appropriate new argument."""

    def _str_repr(var):
        """Converts string or FluentEnum variable to quoted string representation."""
        if isinstance(var, (str, FluentEnum)):
            return f'"{str(var)}"'
        else:
            return var

    def decorator(func):
        """Holds the original method to perform operations on it."""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """Warns about the deprecated argument and replaces it with the new
            argument."""
            if old_arg in kwargs:
                old_value = kwargs[old_arg]
                new_value = converter(kwargs[old_arg])
                if new_value is not None and kwargs.get(new_arg) is None:
                    kwargs[new_arg] = new_value
                kwargs.pop(old_arg)
                warnings.warn(
                    f"'{old_arg} = {_str_repr(old_value)}' is deprecated. "
                    f"Use '{new_arg} = {_str_repr(new_value)}' instead.",
                    deprecation_class,
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator
