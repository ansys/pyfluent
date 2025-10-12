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
    warning_cls: type = PyFluentDeprecationWarning,
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
    warning_cls : type, optional
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

            # map values from old args to new args (1-to-1 or many-to-one)
            for i, old_arg in enumerate(old_group):
                if old_arg in kwargs:
                    old_val = kwargs.pop(old_arg)
                    target_arg = new_group[min(i, len(new_group) - 1)]
                    kwargs.setdefault(target_arg, old_val)
        return kwargs

    converter = converter or _default_converter

    def build_warning_messages() -> list[str]:
        messages = []
        for old_group, new_group in zip(old_arg_list, new_arg_list):
            old_str = ", ".join(f"'{o}'" for o in old_group)
            new_str = ", ".join(f"'{n}'" for n in new_group)
            messages.append(
                f"Arguments {old_str} are deprecated; use {new_str} instead."
            )
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
                        f"Arguments {old_str} are deprecated; use {new_str} instead.",
                        warning_cls,
                        stacklevel=2,
                    )

            # Perform conversion (default or custom)
            kwargs = converter(kwargs, old_arg_list, new_arg_list)
            return deprecated_func(*args, **kwargs)

        return wrapper

    return decorator
