"""Module that provides a method to handle deprecated arguments."""

import functools
import logging
from typing import List
import warnings

from ansys.fluent.core.warnings import PyFluentDeprecationWarning

logger = logging.getLogger("pyfluent.general")


def deprecate_argument(
    old_arg,
    new_arg,
    converter,
    warning_cls=PyFluentDeprecationWarning,
):
    """Warns that the argument provided is deprecated and automatically replaces the
    deprecated argument with the appropriate new argument."""

    def _str_repr(var):
        """Converts a string or FluentEnum variable to quoted string representation."""
        from ansys.fluent.core.launcher.pyfluent_enums import Dimension, FluentEnum

        if isinstance(var, Dimension):
            return 2 if var == Dimension.TWO else 3
        elif isinstance(var, (str, FluentEnum)):
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
                warnings.warn(
                    f"'{old_arg}' is deprecated. Use '{new_arg}' instead.",
                    warning_cls,
                    stacklevel=2,
                )
                old_value = kwargs[old_arg]
                new_value = kwargs.get(new_arg)
                if new_value is None:
                    new_value = converter(kwargs[old_arg])
                    kwargs[new_arg] = new_value
                    logger.warning(
                        f"Using '{new_arg} = {_str_repr(new_value)}' for '{func.__name__}()'"
                        f" instead of '{old_arg} = {_str_repr(old_value)}'."
                    )
                else:
                    logger.warning(
                        f"Ignoring '{old_arg} = {_str_repr(old_value)}' specification for '{func.__name__}()',"
                        f" only '{new_arg} = {_str_repr(new_value)}' applies."
                    )
                kwargs.pop(old_arg)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def deprecate_arguments(
    old_args: List,
    new_args: List,
    converter,
    warning_cls=PyFluentDeprecationWarning,
):
    """Warns that the arguments provided are deprecated and automatically replaces the
    deprecated arguments with the appropriate new arguments."""

    def decorator(func):
        """Holds the original method to perform operations on it."""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """Warns about the deprecated arguments and replaces them with the new
            arguments."""
            warnings.warn(
                f"The arguments: {', '.join(old_args)} are deprecated. Use {', '.join(new_args)} instead.",
                warning_cls,
                stacklevel=2,
            )
            old_args_dict = {}
            for arg in old_args:
                if arg in kwargs:
                    old_args_dict[arg] = kwargs.pop(arg)
            new_args_dict = converter(old_args_dict, new_args)
            for key, val in new_args_dict.items():
                if key in kwargs:
                    logger.warning(
                        f"Ignoring deprecated specification for '{func.__name__}()',"
                        f" only '{key} = {kwargs[key]}' applies."
                    )

            kwargs = {**new_args_dict, **kwargs}

            return func(*args, **kwargs)

        return wrapper

    return decorator
