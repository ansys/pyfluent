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


def _render_widgets(settings_obj, label):
    try:
        if not settings_obj.is_active():
            settings_val = ""
        else:
            settings_val = settings_obj()
    except RuntimeError:
        settings_val = ""
    allowed_values = None
    if hasattr(settings_obj, "allowed_values") and settings_obj.allowed_values():
        allowed_values = list(settings_obj.allowed_values())
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


def _param_ui(settings_obj):
    settings_obj_parent = settings_obj.parent
    attr = settings_obj.python_name
    label = attr.replace("_", " ").capitalize()

    def get_fn():
        try:
            return getattr(settings_obj_parent, attr)
        except AttributeError:
            return settings_obj_parent[settings_obj.obj_name]

    def set_fn(v):
        return setattr(settings_obj_parent, attr, v)

    widget = _render_widgets(get_fn(), label)
    output = widgets.Output()
    with output:
        output.clear_output()
        print(
            f"<solver_session>.settings.{settings_obj.path.replace('/', '.').replace('-', '_')}"
        )
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
                    print(
                        f"<solver_session>.settings.{settings_obj.path.replace('/', '.').replace('-', '_')} = {vals}"
                    )

        widget.observe(commit_text_list)
    else:

        def on_change(change):
            if change["name"] == "value":
                with output:
                    output.clear_output()
                    try:
                        set_fn(change["new"])
                        print(
                            f"<solver_session>.settings.{settings_obj.path.replace('/', '.').replace('-', '_')} = {change['new']}"
                        )
                    except Exception as e:
                        print(f"Error setting {label}: {e}")

        widget.observe(on_change)
    return widgets.VBox([widget, output])


def _command_ui(func, label: str = None):
    """
    Renders input widgets for function arguments based on .argument_names()
    and executes func(**kwargs) on button click.
    """

    # Get argument names from the function object
    if not hasattr(func, "argument_names"):
        print("Command has no 'argument_names()'.")
        return

    arg_names = func.argument_names
    arg_widgets = {}

    controls = []
    for name in arg_names:
        widget = _render_widgets(getattr(func, name), name)
        arg_widgets[name] = widget
        controls.append(widget)

    # Run button
    button = widgets.Button(
        description=label or f"Run {func.python_name}", button_style="success"
    )
    output = widgets.Output()
    with output:
        output.clear_output()
        print(
            f"<solver_session>.settings.{func.path.replace('/', '.')}".replace("-", "_")
        )

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
                print(
                    f"<solver_session>.settings.{func.path.replace('/', '.')}".replace(
                        "-", "_"
                    )
                    + kwargs_str.strip()[:-1]
                    + ")"
                )
                if result is not None:
                    print("Result:", result)
            except Exception as e:
                print("Error:", e)

    button.on_click(on_click)
    return widgets.VBox(controls + [button, output])


def settings_ui(obj, indent=0):
    """Render settings objects into interactive graphics."""
    if isinstance(obj, (Group, NamedObject)):
        if isinstance(obj, Group):
            child_names = obj.get_active_child_names() + obj.get_active_command_names()
        else:
            child_names = list(obj) + obj.command_names
        children_widgets = []
        for child_name in child_names:
            try:
                child_obj = getattr(obj, child_name)
            except AttributeError:
                child_obj = obj[child_name]
            child_widget = (
                settings_ui(child_obj, indent=indent + 1)
                if child_obj.is_active()
                else None
            )
            if child_widget:
                acc = widgets.Accordion(children=[child_widget])
                acc.set_title(0, child_name)
                children_widgets.append(acc)

        return widgets.VBox(children_widgets)

    else:
        if isinstance(obj, BaseCommand):
            leaf_widget = _command_ui(obj) if obj.is_active() else widgets.HTML("")
        else:
            leaf_widget = _param_ui(obj) if obj.is_active() else widgets.HTML("")
        return widgets.VBox([leaf_widget])
