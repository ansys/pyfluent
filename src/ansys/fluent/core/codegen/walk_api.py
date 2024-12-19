"""Module containing tool for walking (generated) API class hierarchy.

Example
-------

.. code-block:: python

    >>> from ansys.fluent.core.codegen import walk_api
    >>> from ansys.fluent.core.generated.solver import settings_252
    >>> walk_api.walk_api(settings_252.root, lambda p, is_method: print(p), current_path=[])

"""

from typing import List


def walk_api(
    api_cls, on_each_path, current_path: str | List[str] = "", is_method: bool = False
):
    """
    Recursively traverse the API hierarchy, calling `on_each_path` for each item.

    Parameters:
    - api_cls: The current class of the API hierarchy.
    - on_each_path: A callback function to call for each path.
    - current_path: The current path in the hierarchy (default: empty string).
      Paths can be either dot-separated strings or string lists. The type is
      determined by the client.
    """
    # Skip the root path
    if current_path:
        on_each_path(current_path, is_method)

    child_classes = getattr(api_cls, "_child_classes", {})

    def _traverse(child_name, is_method):
        if child_name in child_classes:
            child_cls = child_classes[child_name]
            # Construct the new path
            if isinstance(current_path, list):
                new_path = current_path + [child_name]
            else:
                new_path = (
                    f"{current_path}.{child_name}" if current_path else child_name
                )
            # Recursively walk the child
            walk_api(child_cls, on_each_path, new_path, is_method)

            # Delegate directly to any child_object_type (relevant for named objects)
            child_object_type = getattr(api_cls, "child_object_type", None)
            if child_object_type:
                walk_api(child_cls, on_each_path, current_path, is_method)

    # Get child names and their respective classes
    if is_method:
        arg_names = [
            name for attr in ("argument_names",) for name in getattr(api_cls, attr, [])
        ]

        for arg_name in arg_names:
            _traverse(arg_name, is_method=False)

    else:

        child_names = [
            name for attr in ("child_names",) for name in getattr(api_cls, attr, [])
        ]

        for child_name in child_names:
            _traverse(child_name, is_method=False)

        method_names = [
            name
            for attr in ("command_names", "query_names")
            for name in getattr(api_cls, attr, [])
        ]

        for method_name in method_names:
            _traverse(method_name, is_method=True)
