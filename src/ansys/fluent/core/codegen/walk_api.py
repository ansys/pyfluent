"""Module containing tool for walking API."""


def walk_api(api_root_cls, on_each_path, current_path=""):
    """
    Recursively traverse the API hierarchy, calling `on_each_path` for each item.

    Parameters:
    - api_root_cls: The root class of the API hierarchy.
    - on_each_path: A callback function to call for each path.
    - current_path: The current dot-separated path in the hierarchy (default: empty string).
    """
    # Skip the root path
    if current_path:
        on_each_path(current_path)

    # Get child names and their respective classes
    child_names = getattr(api_root_cls, "child_names", [])
    child_classes = getattr(api_root_cls, "_child_classes", {})

    # Traverse each child
    for child_name in child_names:
        if child_name in child_classes:
            child_cls = child_classes[child_name]
            # Construct the new path
            new_path = f"{current_path}.{child_name}" if current_path else child_name
            # Recursively walk the child
            walk_api(child_cls, on_each_path, new_path)
