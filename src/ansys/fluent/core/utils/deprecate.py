# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Deprecate Arguments."""

import functools
import inspect
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

    if len(old_args) != len(new_args) and converter is None:
        raise ValueError(
            f"Cannot automatically convert {old_args} → {new_args}: too many old args. "
            f"Provide a custom converter."
        )

    def _default_converter(
        kwargs: dict[str, Any],
        old_params: list[str],
        new_params: list[str],
    ) -> dict[str, Any]:
        """Default converter that maps all old args to new args one-to-one."""
        for old_arg, new_arg in zip(old_params, new_params):
            if old_arg in kwargs:
                old_val = kwargs.pop(old_arg)
                target_arg = new_arg
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

    old_str = ", ".join(f"'{o}'" for o in old_args)
    new_str = ", ".join(f"'{n}'" for n in new_args)
    if len(old_args) > 1:
        reason = f"Arguments {old_str} are deprecated; use {new_str} instead."
    else:
        reason = f"Argument {old_str} is deprecated; use {new_str} instead."

    def decorator(func: Callable):
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

                sig = inspect.signature(converter)
                params = sig.parameters
                n_params = len(params)
                if n_params == 1:
                    kwargs = converter(kwargs)
                elif n_params == 3:
                    kwargs = converter(kwargs, old_args, new_args)
                else:
                    raise TypeError(
                        f"Converter must accept either (kwargs) or (kwargs, old_args, new_args), "
                        f"but got {n_params} parameter(s): {list(params)}"
                    )
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

        if new_func:
            reason = f"Function '{func_name}' is deprecated since version {version}. Use '{new_func}' instead."
        else:
            reason = f"Function '{func_name}' is deprecated since version {version}."

        decorated = deprecated(version=version, reason=reason)(func)

        @functools.wraps(decorated)
        def wrapper(*args, **kwargs):
            warnings.warn(reason, warning_cls, stacklevel=2)
            return decorated(*args, **kwargs)

        return wrapper

    return decorator
