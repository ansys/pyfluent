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

"""Render ui UI in Jupyter notebook."""

from ansys.fluent.core.ui.utils import (
    _parse_path,
    _render_widget_from_props_generic,
    _safe_get_properties,
)

try:
    import ipywidgets as widgets
except ModuleNotFoundError as exc:
    raise ModuleNotFoundError(
        "Missing dependencies, use 'pip install ansys-fluent-core[ui-jupyter]' to install them."
    ) from exc

from ansys.fluent.core.solver.flobject import (
    BaseCommand,
    Group,
    NamedObject,
)


def set_auto_refresh():
    """Refreshes the UI w.r.t. server state for each command execution or parameter invocation."""
    raise NotImplementedError("This is yet to be implemented in jupyter environment.")


def _render_widgets_from_props(settings_obj, label, props):
    """Render widget using pre-fetched props instead of repeated calls."""
    return _render_widget_from_props_generic(settings_obj, label, props, widgets)


def _param_ui(settings_obj, props):
    label = props["python_name"].replace("_", " ").capitalize()

    def get_fn():
        try:
            return getattr(props["parent"], props["python_name"])
        except AttributeError:
            return props["parent"][props["obj_name"]]

    def set_fn(v):
        return setattr(settings_obj.parent, props["python_name"], v)

    widget = _render_widgets_from_props(get_fn(), label, props)
    output = widgets.Output()
    with output:
        output.clear_output()
        print(_parse_path(settings_obj))
    if hasattr(widget, "_is_list_text"):
        typ, parse_csv = widget._is_list_text

        def commit_text_list(change):
            if change["name"] == "value":
                raw = change["new"]
                vals = (
                    [typ(v.strip()) for v in raw.split(",") if v.strip()]
                    if parse_csv
                    else list(change["new"])
                )
                with output:
                    output.clear_output()
                    set_fn(vals)
                    print(f"{_parse_path(settings_obj)} = {vals}")

        widget.observe(commit_text_list)
    else:

        def on_change(change):
            if change["name"] == "value":
                with output:
                    output.clear_output()
                    try:
                        set_fn(change["new"])
                        print(f"{_parse_path(settings_obj)} = {change['new']}")
                    except Exception as e:
                        print(f"Error setting {label}: {e}")

        widget.observe(on_change)
    return widgets.VBox([widget, output])


def _command_ui(func, props):
    """
    Renders input widgets for function arguments based on .argument_names()
    and executes func(**kwargs) on button click.
    """

    # Get argument names from the function object
    if not hasattr(func, "argument_names"):
        return widgets.HTML("Command has no 'argument_names()'.")

    arg_names = func.argument_names
    arg_widgets = {}
    controls = []
    for name in arg_names:
        child_obj = getattr(func, name)
        child_props = _safe_get_properties(child_obj)
        widget = _render_widgets_from_props(child_obj, name, child_props)
        arg_widgets[name] = widget
        controls.append(widget)

    # Run button
    button = widgets.Button(
        description=f"Run {props['python_name']}", button_style="success"
    )
    output = widgets.Output()
    with output:
        output.clear_output()
        print(_parse_path(func))

    def on_click(_):
        kwargs = {name: w.value for name, w in arg_widgets.items()}
        with output:
            output.clear_output()
            try:
                func(**kwargs)
                kwargs_str = "("
                for k, v in kwargs.items():
                    if type(v) is str:
                        if v != "":
                            kwargs_str += f"{k}='{v}', "
                    else:
                        kwargs_str += f"{k}={v}, "
                print(f"{_parse_path(func)}" + kwargs_str.strip()[:-1] + ")")
            except Exception as e:
                print("Error:", e)

    button.on_click(on_click)
    return widgets.VBox(controls + [button, output])


def settings_ui(obj, indent=0):
    """Render settings objects into ui graphics."""
    props = _safe_get_properties(obj)
    if isinstance(obj, (Group, NamedObject)):
        if isinstance(obj, Group):
            command_names = obj.get_active_command_names()
            child_names = obj.get_active_child_names() + command_names
        else:
            command_names = obj.command_names
            child_names = list(obj) + command_names
        accordions = []
        for child_name in child_names:

            def lazy_loader(name=child_name, parent=obj, lvl=indent + 1):
                try:
                    child_obj = getattr(parent, name)
                except AttributeError:
                    child_obj = parent[name]
                return settings_ui(child_obj, lvl)

            acc = widgets.Accordion(children=[widgets.HTML("Loading...")])
            if child_name in command_names:
                acc.set_title(0, f"⚡ {child_name}")
            else:
                acc.set_title(0, child_name)

            def on_selected(change, loader=lazy_loader, accordion=acc):
                if change["name"] == "selected_index" and change["new"] == 0:
                    if isinstance(accordion.children[0], widgets.HTML):
                        accordion.children = [loader()]

            acc.observe(on_selected, names="selected_index")
            accordions.append(acc)

        return widgets.VBox(accordions)

    else:
        if isinstance(obj, BaseCommand):
            return (
                widgets.VBox([_command_ui(obj, props)])
                if props["is_active"]
                else widgets.HTML("")
            )
        else:
            return (
                widgets.VBox([_param_ui(obj, props)])
                if props["is_active"]
                else widgets.HTML("")
            )
