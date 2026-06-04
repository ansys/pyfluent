"""
Get completer information.
Shared implementation for both datamodel and settings objects.
"""

import inspect
from typing import Callable, Iterable, List


def get_completer_info(
    obj,
    base_class: type,
    prefix: str = "",
    excluded: Iterable = None,
    predicate: Callable = None,
    get_type_for_completer_info: Callable = None,
) -> List[List[str]]:
    """Get completer information of all children.

    Returns
    -------
    List[List[str]]
        Name, type and docstring of all children.
    """
    excluded = excluded or []
    ret = []
    public_members = (
        (k, v)
        for k, v in inspect.getmembers(obj, predicate=predicate)
        if not k.startswith("_")
    )
    filtered_members = (
        (k, v)
        for k, v in public_members
        if (k not in excluded and k.startswith(prefix))
    )
    for k, v in filtered_members:
        if isinstance(v, base_class):
            ret.append(
                [
                    k,
                    (
                        get_type_for_completer_info(v.__class__)
                        if get_type_for_completer_info is not None
                        else v.__class__.__bases__[0].__name__
                    ),
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
