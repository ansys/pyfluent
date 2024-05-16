"""Module that provides a method to handle deprecated arguments."""

import functools
import warnings

from ansys.fluent.core.launcher.pyfluent_enums import FluentEnum


def deprecate_argument(
    old_arg, new_arg, converter, deprecation_class=DeprecationWarning
):
    """Warns that the argument provided is deprecated and automatically replaces
    the deprecated argument with the appropriate new argument."""

    def _str_repr(var):
        """Converts a string or FluentEnum variable to quoted string representation."""
        if isinstance(var, (str, FluentEnum)):
            return f'"{var}"'
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
                warning_str = f"'{old_arg}' is deprecated. "
                new_value = converter(kwargs[old_arg])
                if kwargs.get(new_arg) is None:
                    kwargs[new_arg] = new_value
                    warning_str += f"Use '{new_arg} = {_str_repr(new_value)}' instead of '{old_arg} = {_str_repr(old_value)}'."
                else:
                    warning_str += f"Use only '{new_arg}' instead."
                kwargs.pop(old_arg)
                warnings.warn(warning_str, deprecation_class, stacklevel=2)
            return func(*args, **kwargs)

        return wrapper

    return decorator
