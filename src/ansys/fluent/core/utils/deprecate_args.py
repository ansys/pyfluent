"""Module that provides a method to handle deprecated arguments."""

import functools
import logging
import warnings

from ansys.fluent.core.launcher.pyfluent_enums import FluentEnum

logger = logging.getLogger("pyfluent.general")


def deprecate_argument(
    old_arg, new_arg, converter, deprecation_class=DeprecationWarning
):
    """Warns that the argument provided is deprecated and automatically replaces the
    deprecated argument with the appropriate new argument."""

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
                new_value = kwargs.get(new_arg)
                if new_value is None:
                    warnings.warn(
                        f"'{old_arg}' is deprecated. Use '{new_arg}' instead.",
                        deprecation_class,
                        stacklevel=2,
                    )
                    new_value = converter(kwargs[old_arg])
                    kwargs[new_arg] = new_value
                    logger.warning(
                        f"Using '{func.__name__}({new_arg} = {_str_repr(new_value)})'"
                        f" instead of '{old_arg} = {_str_repr(old_value)}'."
                    )
                else:
                    logger.warning(
                        f"Ignoring '{old_arg} = {_str_repr(old_value)}' specification for {func.__name__}(),"
                        f" only '{new_arg} = {_str_repr(new_value)}' applies."
                    )
                kwargs.pop(old_arg)
            return func(*args, **kwargs)

        return wrapper

    return decorator
