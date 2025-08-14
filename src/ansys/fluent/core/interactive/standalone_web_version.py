# fluent_panel_ui.py
"""Web UI for Fluent settings using Panel with lazy loading and batched property access."""

from __future__ import annotations

from typing import Any, Callable, Dict, List

try:
    import panel as pn
except ModuleNotFoundError as exc:
    raise ModuleNotFoundError(
        "Missing dependencies, use 'pip install ansys-fluent-core[interactive]' to install them."
    ) from exc

from ansys.fluent.core.interactive.utils import (
    _parse_path,
    _render_widget_from_props_generic,
    _safe_get_properties,
)
from ansys.fluent.core.solver.flobject import (
    BaseCommand,
    Group,
    NamedObject,
)

pn.extension()


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
    console = pn.pane.Markdown(
        f"```\n{_parse_path(settings_obj)}\n```", sizing_mode="stretch_width"
    )

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
            except Exception as e:
                console.object = f"```\nError setting {label}: {e}\n```"

        w.param.watch(_commit, "value", onlychanged=True)

    return pn.Column(w, console, sizing_mode="stretch_width")


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
    console = pn.pane.Markdown(
        f"```\n{_parse_path(func)}\n```", sizing_mode="stretch_width"
    )

    def _run(_):
        kwargs = {n: w.value for n, w in arg_widgets.items()}
        try:
            result = func(**kwargs)  # Executes ONLY here
            # Render kwargs similarly to your ipywidgets formatter
            parts = []
            for k, v in kwargs.items():
                if isinstance(v, str):
                    if v != "":
                        parts.append(f"{k}='{v}'")
                else:
                    parts.append(f"{k}={v}")
            call = f"{_parse_path(func)}({', '.join(parts)})"
            if result is not None:
                console.object = f"```\n{call}\nResult: {result}\n```"
            else:
                console.object = f"```\n{call}\n```"
        except Exception as e:
            console.object = f"```\nError: {e}\n```"

    btn.on_click(_run)
    return pn.Column(*controls, btn, console, sizing_mode="stretch_width")


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

    # 'active' is a list of indices; when [0], first (and only) section is open
    loaded = {"done": False}

    def _maybe_load(event):
        if loaded["done"]:
            return
        active = event.new
        if active and 0 in active:
            try:
                content = loader()
            except Exception as e:
                content = pn.pane.Markdown(f"**Error loading section**: {e}")
            acc[0] = (title, content)
            loaded["done"] = True

    # Trigger when first opened
    acc.param.watch(_maybe_load, "active", onlychanged=True)
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
            display_name = f"⚡ {child_name.upper()}"
        else:
            display_name = child_name
        sections.append(_lazy_section(display_name, _loader))

    return pn.Column(*sections, sizing_mode="stretch_width")


def build_settings_view(settings_obj) -> pn.viewable.Viewable:
    """
    Public API: pass any Fluent settings object.
    Internally uses _root to render absolute paths and builds a lazy, web UI.
    """
    return _settings_view(settings_obj)
