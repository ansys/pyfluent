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

"""Web UI for Fluent settings using Panel with lazy loading and batched property access."""

from __future__ import annotations

from typing import Any, Callable, Dict, List

try:
    import panel as pn
    import param
except ModuleNotFoundError as exc:
    raise ModuleNotFoundError(
        "Missing dependencies, use 'pip install ansys-fluent-core[ui]' to install them."
    ) from exc

from ansys.fluent.core.solver.flobject import (
    BaseCommand,
    Group,
    NamedObject,
)
from ansys.fluent.core.ui.utils import (
    _parse_path,
    _render_widget_from_props_generic,
    _safe_get_properties,
)

_path_backup_dict = {}

AUTO_REFRESH = False


def set_auto_refresh():
    """Refreshes the UI w.r.t. server state for each command execution or parameter invocation."""
    global AUTO_REFRESH
    AUTO_REFRESH = True


pn.extension()

# global trigger for refresh (Panel Param depends on it)
_refresh = pn.state.cache.get("fluent_refresh", None)
if _refresh is None:

    class Refresh(param.Parameterized):
        """Refresh."""

        bump = param.Event()

    _refresh = Refresh()
    pn.state.cache["fluent_refresh"] = _refresh


def _render_widget_from_props(
    settings_obj, label: str, props: Dict[str, Any]
) -> pn.viewable.Viewable:
    """Produce a Panel widget from type+props. No backend mutation here."""
    return _render_widget_from_props_generic(settings_obj, label, props, pn.widgets)


def _param_view(settings_obj, props: Dict[str, Any]) -> pn.viewable.Viewable:
    label = props["python_name"].replace("_", " ").capitalize()

    def get_fn():
        try:
            return getattr(props["parent"], props["python_name"])
        except AttributeError:
            return props["parent"][props["obj_name"]]

    def set_fn(v):
        return setattr(settings_obj.parent, props["python_name"], v)

    w = _render_widget_from_props(get_fn(), label, props)
    obj_apth = _parse_path(settings_obj)
    if obj_apth in _path_backup_dict:
        console = pn.pane.Markdown(
            f"```\n{obj_apth} = {_path_backup_dict[obj_apth]}\n```",
            sizing_mode="stretch_width",
        )
    else:
        console = pn.pane.Markdown(f"```\n{obj_apth}\n```", sizing_mode="stretch_width")

    # Change handlers
    if hasattr(w, "_is_list_text"):
        typ, parse_csv = w._is_list_text

        def _commit_list(event):
            if event is None:
                return
            newv = event.new
            if parse_csv:
                raw = newv or ""
                vals = [typ(v.strip()) for v in raw.split(",") if v.strip()]
            else:
                vals = list(newv or [])
            try:
                set_fn(vals)
                console.object = f"```\n{_parse_path(settings_obj)} = {vals}\n```"
                _path_backup_dict[_parse_path(settings_obj)] = vals
                if AUTO_REFRESH:
                    _refresh.bump = True
            except Exception as e:
                console.object = f"```\nError setting {label}: {e}\n```"

        w.param.watch(_commit_list, "value", onlychanged=True)
    else:

        def _commit(event):
            if event is None:
                return
            try:
                set_fn(event.new)
                console.object = f"```\n{_parse_path(settings_obj)} = {event.new}\n```"
                _path_backup_dict[_parse_path(settings_obj)] = event.new
                if AUTO_REFRESH:
                    _refresh.bump = True
            except Exception as e:
                console.object = f"```\nError setting {label}: {e}\n```"

        w.param.watch(_commit, "value", onlychanged=True)

    return pn.Column(
        w, console, sizing_mode="stretch_width", margin=(10, 20), align="start"
    )


def _command_view(func, props: Dict[str, Any]) -> pn.viewable.Viewable:
    """Render command arguments (on demand) and execute only on click."""
    # Safely fetch argument names (does NOT execute the command)
    if not hasattr(func, "argument_names"):
        return pn.pane.HTML("<i>Command has no 'argument_names()'.</i>")
    arg_names = func.argument_names
    arg_widgets: Dict[str, Any] = {}
    controls: List[pn.viewable.Viewable] = []

    # Build argument widgets immediately when this view is created
    for name in arg_names:
        param_obj = getattr(func, name)  # safe: this just references the arg handle
        pprops = _safe_get_properties(param_obj)
        widget = _render_widget_from_props(param_obj, name, pprops)
        arg_widgets[name] = widget
        controls.append(widget)

    btn = pn.widgets.Button(name=f"Run {props['python_name']}", button_type="success")
    obj_path = _parse_path(func)
    if obj_path in _path_backup_dict:
        console = pn.pane.Markdown(
            f"```\n{_path_backup_dict[obj_path]}\n```", sizing_mode="stretch_width"
        )
    else:
        console = pn.pane.Markdown(f"```\n{obj_path}\n```", sizing_mode="stretch_width")

    def _run(_):
        kwargs = {n: w.value for n, w in arg_widgets.items()}
        try:
            func(**kwargs)  # Executes ONLY here
            # Render kwargs similarly to your ipywidgets formatter
            parts = []
            for k, v in kwargs.items():
                if isinstance(v, str):
                    if v != "":
                        parts.append(f"{k}='{v}'")
                else:
                    parts.append(f"{k}={v}")
            call = f"{_parse_path(func)}({', '.join(parts)})"
            console.object = f"```\n{call}\n```"
            _path_backup_dict[_parse_path(func)] = call
            if AUTO_REFRESH:
                _refresh.bump = True
        except Exception as e:
            console.object = f"```\nError: {e}\n```"

    btn.on_click(_run)
    return pn.Column(
        *controls,
        btn,
        console,
        sizing_mode="stretch_width",
        margin=(10, 20),
        align="start",
    )


# ---------------------------
# Lazy accordion (recursive)
# ---------------------------


def _lazy_section(
    title: str, loader: Callable[[], pn.viewable.Viewable]
) -> pn.Accordion:
    """
    A single-node Accordion whose body is constructed ON FIRST EXPAND.
    Subsequent expands reuse the existing content.
    """
    placeholder = pn.pane.Markdown("*(loading…)*")
    acc = pn.Accordion((title, placeholder), sizing_mode="stretch_width")

    def _load_content():
        try:
            return loader()
        except Exception as e:
            return pn.pane.Markdown(f"**Error loading section**: {e}")

    def _maybe_load(event=None):
        if acc.active and 0 in acc.active:
            content = _load_content()
            acc[0] = (title, content)

    # Trigger when first opened
    acc.param.watch(_maybe_load, "active", onlychanged=True)

    def _on_refresh(event):
        if acc.active and 0 in acc.active:
            _maybe_load()

    _refresh.param.watch(_on_refresh, "bump")

    return acc


# ---------------------------
# Main entry (recursive renderer)
# ---------------------------


def _settings_view(obj, indent: int = 0) -> pn.viewable.Viewable:
    """Recursively build the view for a settings object (lazy children)."""
    props = _safe_get_properties(obj)

    if isinstance(obj, (Group, NamedObject)):
        if isinstance(obj, Group):
            command_names = obj.get_active_command_names()
            child_names = obj.get_active_child_names() + command_names
        else:
            command_names = obj.command_names
            child_names = list(obj) + command_names
    else:
        if isinstance(obj, BaseCommand):
            return _command_view(obj, props) if props["is_active"] else pn.pane.HTML("")
        else:
            return _param_view(obj, props) if props["is_active"] else pn.pane.HTML("")

    sections: List[pn.viewable.Viewable] = []

    for child_name in child_names:
        # Build a lazy loader that only resolves the child on expand
        def _loader(name=child_name, parent=obj, lvl=indent + 1):
            try:
                child_obj = getattr(parent, name)
            except AttributeError:
                child_obj = parent[name]
            return _settings_view(child_obj, lvl)

        # Each child gets its own one-item accordion (mirrors your ipywidgets UX)
        if child_name in command_names:
            display_name = f"⚡ {child_name}"
        else:
            display_name = child_name
        sections.append(_lazy_section(display_name, _loader))

    return pn.Column(
        *(pn.Column(sec, margin=(5, 0)) for sec in sections),
        sizing_mode="fixed",
        margin=(10, 20),
        align="start",
        css_classes=["rounded-box"],
    )


def build_settings_view(settings_obj) -> pn.viewable.Viewable:
    """
    Public API: pass any Fluent settings object.
    Internally uses _root to render absolute paths and builds a lazy, web UI.
    """
    return _settings_view(settings_obj)
