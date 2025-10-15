"""Deprecate Arguments."""

import functools
from typing import Any, Callable
import warnings

from deprecated.sphinx import deprecated

from ansys.fluent.core.pyfluent_warnings import PyFluentDeprecationWarning


def deprecate_arguments(
    old_args: str | list[str],
    new_args: str | list[str],
    version: str,
    converter: Callable | None = None,
    warning_cls: type[Warning] = PyFluentDeprecationWarning,
) -> Callable:
    """
    Deprecate multiple arguments (possibly grouped) and automatically replace them with new ones.

    Parameters
    ----------
    old_args : str | list[str]
        Old argument name(s) to deprecate.
    new_args : str | list[str]
        New argument name(s) to use instead.
    version : str
        The version in which the arguments were deprecated.
    converter : callable, optional
        Custom converter function taking (kwargs, old_args, new_args) and returning modified kwargs.
        If not provided, a default converter is used.
    warning_cls : warnings, optional
        The warning class to use for deprecation warnings.

    Raises
    ------
    ValueError
        For arguments mismatch.

    Returns
    -------
    Callable
        The decorated function.
    """
    if isinstance(old_args, str):
        old_args = [old_args]

    if isinstance(new_args, str):
        new_args = [new_args]

    # Validation
    if len(old_args) != len(new_args) and converter is None:
        raise ValueError(
            f"Cannot automatically convert {old_args} → {new_args}: too many old args. "
            f"Provide a custom converter."
        )

    # Default converter
    def _default_converter(
        kwargs: dict[str, Any],
        old_params: list[str],
        new_params: list[str],
    ) -> dict[str, Any]:
        """Default converter that maps all old args to new args one-to-one."""
        for i, old_arg in enumerate(old_params):
            if old_arg in kwargs:
                old_val = kwargs.pop(old_arg)
                target_arg = new_params[i]
                if target_arg in kwargs:
                    warnings.warn(
                        f"Both deprecated argument '{old_arg}' and new argument '{target_arg}' were provided. "
                        f"Ignoring {old_arg}.",
                        PyFluentDeprecationWarning,
                        stacklevel=2,
                    )
                else:
                    kwargs[target_arg] = old_val
        return kwargs

    converter = converter or _default_converter

    # Build reason message for @deprecated
    old_str = ", ".join(f"'{o}'" for o in old_args)
    new_str = ", ".join(f"'{n}'" for n in new_args)
    if len(old_args) > 1:
        reason = f"Arguments {old_str} are deprecated; use {new_str} instead."
    else:
        reason = f"Argument {old_str} is deprecated; use {new_str} instead."

    def decorator(func: Callable):
        # Documentation
        deprecated_func = deprecated(version=version, reason=reason)(func)

        @functools.wraps(deprecated_func)
        def wrapper(*args, **kwargs):
            # Warn only if any old arg(s) present
            if any(arg in kwargs for arg in old_args):
                warnings.warn(
                    reason,
                    warning_cls,
                    stacklevel=2,
                )

            # Perform conversion (default or custom)
            try:
                kwargs = converter(kwargs, old_args, new_args)
            except TypeError:
                # If the custom converter takes only kwargs
                kwargs = converter(kwargs)
            return deprecated_func(*args, **kwargs)

        return wrapper

    return decorator


def deprecate_function(
    version: str,
    new_func: str | None = None,
    warning_cls: type[Warning] = PyFluentDeprecationWarning,
) -> Callable:
    """
    Decorator to mark a function as deprecated.

    Parameters
    ----------
    version : str
        Version in which this function was deprecated.
    new_func : str, optional
        Name of the new/replacement function to use.
    warning_cls : type[Warning], optional
        Warning class to use for the deprecation warning.

    Returns
    -------
    Callable
        The decorated function.
    """

    def decorator(func):
        func_name = func.__name__

        # Build reason message for @deprecated
        if new_func:
            reason = f"Function '{func_name}' is deprecated since version {version}. Use '{new_func}' instead."
        else:
            reason = f"Function '{func_name}' is deprecated since version {version}."

        # Documentation
        decorated = deprecated(version=version, reason=reason)(func)

        @functools.wraps(decorated)
        def wrapper(*args, **kwargs):
            warnings.warn(reason, warning_cls, stacklevel=2)
            return decorated(*args, **kwargs)

        return wrapper

    return decorator
