"""Render interactive UI in Jupyter notebook."""

import ipywidgets as widgets

from ansys.fluent.core.solver.flobject import (
    BaseCommand,
    Boolean,
    Group,
    Integer,
    IntegerList,
    NamedObject,
    Real,
    RealList,
    String,
    StringList,
)


def _parse_path(settings_obj):
    local_obj = settings_obj._root
    path_str = "<solver_session>.settings."
    for path in settings_obj.path.replace("/", ".").replace("?", "").split("."):
        if not path:
            break
        if isinstance(local_obj, NamedObject):
            local_obj = local_obj[path]
            path_str = path_str[:-1] + f"[{path}]" + "."
        else:
            local_obj = getattr(local_obj, path.replace("-", "_"))
            path_str += path.replace("-", "_") + "."

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


def _render_widgets_from_props(settings_obj, label, props):
    """Render widget using pre-fetched props instead of repeated calls."""
    settings_val = props["value"]
    allowed_values = props["allowed_values"]
    try:
        if isinstance(settings_obj, Boolean):
            widget = widgets.Checkbox(
                value=bool(settings_val), description=label, indent=False
            )
        elif isinstance(settings_obj, Integer):
            widget = widgets.IntText(value=int(settings_val), description=label)
        elif isinstance(settings_obj, Real):
            widget = widgets.FloatText(value=float(settings_val), description=label)
        elif isinstance(settings_obj, String):
            if allowed_values:
                allowed_values = [str(v) for v in allowed_values]
                val = str(settings_val)
                if val not in allowed_values:
                    # Exceptional case, might raise a warning here.....
                    val = allowed_values[0]
                widget = widgets.Dropdown(
                    options=allowed_values, value=val, description=label
                )
            else:
                if settings_val is False:
                    settings_val = ""
                widget = widgets.Text(value=str(settings_val), description=label)
        elif isinstance(settings_obj, StringList):
            if allowed_values:
                allowed_values = [str(v) for v in allowed_values]
                current_values = [
                    str(v) for v in (settings_val or []) if str(v) in allowed_values
                ]
                widget = widgets.SelectMultiple(
                    options=allowed_values, value=current_values, description=label
                )
            else:
                widget = widgets.Text(
                    value=",".join(map(str, settings_val or [])), description=label
                )
            widget._is_list_text = (str, allowed_values is None)
        elif isinstance(settings_obj, IntegerList):
            widget = widgets.Text(
                value=",".join(map(str, settings_val or [])), description=label
            )
            widget._is_list_text = (int, True)
        elif isinstance(settings_obj, RealList):
            widget = widgets.Text(
                value=",".join(map(str, settings_val or [])), description=label
            )
            widget._is_list_text = (float, True)
        else:
            if settings_val is False:
                settings_val = ""
            widget = widgets.Text(value=str(settings_val), description=label)
    except ValueError:
        widget = widgets.Text(value=str(settings_val), description=label)
    return widget


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
                result = func(**kwargs)
                kwargs_str = "("
                for k, v in kwargs.items():
                    if type(v) is str:
                        if v != "":
                            kwargs_str += f"{k}='{v}', "
                    else:
                        kwargs_str += f"{k}={v}, "
                print(f"{_parse_path(func)}" + kwargs_str.strip()[:-1] + ")")
                if result is not None:
                    print("Result:", result)
            except Exception as e:
                print("Error:", e)

    button.on_click(on_click)
    return widgets.VBox(controls + [button, output])


def settings_ui(obj, indent=0):
    """Render settings objects into interactive graphics."""
    props = _safe_get_properties(obj)
    if isinstance(obj, (Group, NamedObject)):
        if isinstance(obj, Group):
            child_names = obj.get_active_child_names() + obj.get_active_command_names()
        else:
            child_names = list(obj) + obj.command_names
        accordions = []
        for child_name in child_names:

            def lazy_loader(name=child_name, parent=obj, lvl=indent + 1):
                try:
                    child_obj = getattr(parent, name)
                except AttributeError:
                    child_obj = parent[name]
                return settings_ui(child_obj, lvl)

            acc = widgets.Accordion(children=[widgets.HTML("Loading...")])
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
