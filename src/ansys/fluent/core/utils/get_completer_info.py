"""
Get completer information.
Shared implementation for both datamodel and settings objects.
"""

import inspect
from typing import Callable, Iterable


def _get_custom_converter_name(cls, type_name_map: dict) -> str:
    for k, v in type_name_map.items():
        if issubclass(cls, k):
            return v
    return cls.__class__.__bases__[0].__name__


def get_completer_info(
    obj,
    base_class: type,
    prefix: str = "",
    excluded: Iterable = None,
    filter_function: Callable = None,
    type_name_map: dict = None,
) -> list[list[str]]:
    """Get completer information of all children.

    Returns
    -------
    list[list[str]]
        Name, type and docstring of all children.
    """
    excluded = excluded or []
    type_name_map = type_name_map or {}
    ret = []
    public_members = (
        (k, v)
        for k, v in inspect.getmembers(obj, predicate=filter_function)
        if not k.startswith("_")
    )
    filtered_members = (
        (k, v)
        for k, v in public_members
        if (k not in excluded and k.startswith(prefix))
    )
    for k, v in filtered_members:
        if isinstance(v, base_class):
            custom_name = _get_custom_converter_name(
                cls=v.__class__, type_name_map=type_name_map
            )
            ret.append(
                [
                    k,
                    custom_name,
                    v.__doc__,
                ]
            )
        elif inspect.ismethod(v):
            ret.append(
                [
                    k,
                    "Method",
                    v.__doc__ or "",
                ]
            )
        else:
            ret.append([k, "Data", ""])
    return ret
