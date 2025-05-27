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

"""Module containing tool for walking (generated) API class hierarchy.

Example
-------

.. code-block:: python

    >>> from ansys.fluent.core.codegen import walk_api
    >>> from ansys.fluent.core.generated.solver import settings_252
    >>> walk_api.walk_api(settings_252.root, lambda p: print(p), current_path=[])
    >>> walk_api.walk_api(settings_252.root, lambda p, api_item_type: print(p, api_item_type), current_path=[])

"""

from inspect import signature
from typing import List

import ansys.fluent.core.solver.flobject as flobject


def walk_api(
    api_cls, on_each_path, current_path: str | List[str] = "", api_item_type: str = ""
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
        if len(signature(on_each_path).parameters) == 3:
            on_each_path(current_path, api_item_type, api_cls)
        elif len(signature(on_each_path).parameters) == 2:
            on_each_path(current_path, api_item_type)
        else:
            on_each_path(current_path)

    child_classes = getattr(api_cls, "_child_classes", {})

    def _traverse(child_name, api_item_type):
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
            if not api_item_type:
                api_item_type = (
                    "parameter"
                    if isinstance(child_cls, flobject.Property)
                    else "object"
                )
            walk_api(child_cls, on_each_path, new_path, api_item_type)

            # Delegate directly to any child_object_type (relevant for named objects)
            child_object_type = getattr(api_cls, "child_object_type", None)
            if child_object_type:
                walk_api(child_cls, on_each_path, current_path, api_item_type)

    # Get child names and their respective classes
    if api_item_type == "method":
        arg_names = [
            name for attr in ("argument_names",) for name in getattr(api_cls, attr, [])
        ]

        for arg_name in arg_names:
            _traverse(arg_name, api_item_type="argument")

    else:

        child_names = [
            name for attr in ("child_names",) for name in getattr(api_cls, attr, [])
        ]

        for child_name in child_names:
            _traverse(child_name, api_item_type="")

        method_names = [
            name
            for attr in ("command_names", "query_names")
            for name in getattr(api_cls, attr, [])
        ]

        for method_name in method_names:
            _traverse(method_name, api_item_type="method")
