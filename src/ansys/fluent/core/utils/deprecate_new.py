"""Deprecate Arguments."""

import functools
from typing import Any, Callable
import warnings

from deprecated.sphinx import deprecated

from ansys.fluent.core.pyfluent_warnings import PyFluentDeprecationWarning


def deprecate_arguments(
    old_arg_list: list[list[str]],
    new_arg_list: list[list[str]],
    version: str,
    converter: Callable | None = None,
    warning_cls: type[Warning] = PyFluentDeprecationWarning,
) -> Callable:
    """
    Deprecate multiple arguments (possibly grouped) and automatically replace them with new ones.

    Parameters
    ----------
    old_arg_list : list[list[str]]
        Each inner list represents a group of old argument names being deprecated.
    new_arg_list : list[list[str]]
        Each inner list represents a corresponding group of new argument names.
    version : str
        The version in which the arguments were deprecated.
    converter : callable, optional
        Custom converter function that takes (kwargs, old_arg_list, new_arg_list)
        and returns modified kwargs.
        If not provided, a default converter is used.
    warning_cls : warnings, optional
        The warning class to use for deprecation warnings.

    Raises
    ------
    ValueError
        For arguments mismatch.
    """

    # Validation
    if len(old_arg_list) != len(new_arg_list):
        raise ValueError(
            f"old_arg_list and new_arg_list must have the same number of groups. "
            f"Got {len(old_arg_list)} vs {len(new_arg_list)}."
        )

    # Default converter
    def _default_converter(
        kwargs: dict[str, Any],
        old_param_list: list[list[str]],
        new_param_list: list[list[str]],
    ) -> dict[str, Any]:
        """Default converter that maps all old args to new args one-to-one across groups."""
        for old_group, new_group in zip(old_param_list, new_param_list):
            if len(old_group) > len(new_group):
                raise ValueError(
                    f"Cannot automatically convert {old_group} → {new_group}: "
                    "too many old args. Provide a custom converter."
                )

            for i, old_arg in enumerate(old_group):
                if old_arg in kwargs:
                    old_val = kwargs.pop(old_arg)
                    target_arg = new_group[i]
                    if target_arg in kwargs:
                        warnings.warn(
                            f"Both deprecated argument '{old_arg}' and new argument '{target_arg}' were provided. "
                            f"Ignoring {old_arg}."
                        )
                    else:
                        kwargs[target_arg] = old_val
        return kwargs

    converter = converter or _default_converter

    def _message(old: str, new: str) -> str:
        if "," in old:
            return f"Arguments {old} are deprecated; use {new} instead."
        else:
            return f"Argument {old} is deprecated; use {new} instead."

    def build_warning_messages() -> list[str]:
        messages = []
        for old_group, new_group in zip(old_arg_list, new_arg_list):
            old_str = ", ".join(f"'{o}'" for o in old_group)
            new_str = ", ".join(f"'{n}'" for n in new_group)
            messages.append(_message(old_str, new_str))
        return messages

    reason = " ".join(build_warning_messages())

    def decorator(func: Callable):
        # Documentation
        deprecated_func = deprecated(version=version, reason=reason)(func)

        @functools.wraps(deprecated_func)
        def wrapper(*args, **kwargs):
            # Issue warnings for all relevant mappings
            for old_group, new_group in zip(old_arg_list, new_arg_list):
                if any(arg in kwargs for arg in old_group):
                    old_str = ", ".join(f"'{o}'" for o in old_group)
                    new_str = ", ".join(f"'{n}'" for n in new_group)
                    warnings.warn(
                        _message(old_str, new_str),
                        warning_cls,
                        stacklevel=2,
                    )

            # Perform conversion (default or custom)
            kwargs = converter(kwargs, old_arg_list, new_arg_list)
            return deprecated_func(*args, **kwargs)

        return wrapper

    return decorator
