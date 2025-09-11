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

"""Utilities methods for ui rendering."""

from ansys.fluent.core.solver.flobject import (
    BaseCommand,
    Boolean,
    Integer,
    IntegerList,
    NamedObject,
    Real,
    RealList,
    String,
    StringList,
)
from ansys.fluent.core.ui import in_jupyter


def _parse_path(settings_obj):
    """Convert a settings object path to a string representation
    with proper indexing for NamedObject keys."""
    local_obj = settings_obj._root
    path_str = "<solver_session>.settings."
    for path in settings_obj.path.replace("/", ".").replace("?", "").split("."):
        py_path = path.replace("-", "_")
        if not path:
            break
        if isinstance(local_obj, NamedObject):
            try:
                local_obj = local_obj[path]
                path_str = path_str[:-1] + f"['{path}']" + "."
            except KeyError:
                local_obj = getattr(local_obj, py_path)
                path_str += f"{py_path}."
        else:
            local_obj = getattr(local_obj, py_path)
            path_str += f"{py_path}."

    return path_str[:-1]


def _safe_get_properties(settings_obj):
    """Fetch potentially expensive properties once."""
    props = {}
    try:
        props["is_active"] = settings_obj.is_active()
    except RuntimeError:
        props["is_active"] = False

    try:
        if isinstance(settings_obj, BaseCommand):
            props["value"] = ""
        else:
            props["value"] = settings_obj() if props["is_active"] else ""
    except RuntimeError:
        props["value"] = ""

    props["allowed_values"] = None
    if hasattr(settings_obj, "allowed_values"):
        try:
            av = settings_obj.allowed_values()
            props["allowed_values"] = list(av) if av else None
        except RuntimeError:
            pass

    props["path"] = getattr(settings_obj, "path", "")
    props["python_name"] = getattr(settings_obj, "python_name", "")
    props["obj_name"] = getattr(settings_obj, "obj_name", "")
    props["parent"] = getattr(settings_obj, "parent", None)
    return props


def _render_widget_from_props_generic(
    settings_obj, label: str, props: dict, parent_widget
):
    """
    Render a widget from type+props using either ipywidgets or Panel.
    """
    if in_jupyter():
        widget_map = {
            "bool": lambda v: parent_widget.Checkbox(
                value=v, description=label, indent=False
            ),
            "int": lambda v: parent_widget.IntText(value=v, description=label),
            "float": lambda v: parent_widget.FloatText(value=v, description=label),
            "text": lambda v: parent_widget.Text(value=v, description=label),
            "select": lambda opts, v: parent_widget.Dropdown(
                options=opts, value=v, description=label
            ),
            "multi": lambda opts, v: parent_widget.SelectMultiple(
                options=opts, value=v, description=label
            ),
        }
    else:
        widget_map = {
            "bool": lambda v: parent_widget.Checkbox(name=label, value=v),
            "int": lambda v: parent_widget.IntInput(name=label, value=v),
            "float": lambda v: parent_widget.FloatInput(name=label, value=v),
            "text": lambda v: parent_widget.TextInput(name=label, value=v),
            "select": lambda opts, v: parent_widget.Select(
                name=label, options=opts, value=v
            ),
            "multi": lambda opts, v: parent_widget.MultiChoice(
                name=label, options=opts, value=v
            ),
        }

    settings_val = props.get("value")
    allowed = props.get("allowed_values")

    try:
        if isinstance(settings_obj, Boolean):
            return widget_map["bool"](bool(settings_val))
        elif isinstance(settings_obj, Integer):
            return widget_map["int"](int(settings_val))
        elif isinstance(settings_obj, Real):
            return widget_map["float"](float(settings_val))
        elif isinstance(settings_obj, String):
            if allowed:
                options = [str(v) for v in allowed]
                val = str(settings_val)
                if val not in options:
                    val = options[0]
                return widget_map["select"](options, val)
            else:
                if settings_val is False:
                    settings_val = ""
                return widget_map["text"](str(settings_val))
        elif isinstance(settings_obj, StringList):
            if allowed:
                options = [str(v) for v in allowed]
                current = [str(v) for v in (settings_val or []) if str(v) in options]
                w = widget_map["multi"](options, current)
                w._is_list_text = (str, False)
                return w
            else:
                w = widget_map["text"](",".join(map(str, settings_val or [])))
                w._is_list_text = (str, True)
                return w
        elif isinstance(settings_obj, IntegerList):
            w = widget_map["text"](",".join(map(str, settings_val or [])))
            w._is_list_text = (int, True)
            return w
        elif isinstance(settings_obj, RealList):
            w = widget_map["text"](",".join(map(str, settings_val or [])))
            w._is_list_text = (float, True)
            return w
        else:
            if settings_val is False:
                settings_val = ""
            return widget_map["text"](str(settings_val))
    except ValueError:
        return widget_map["text"](str(settings_val))
