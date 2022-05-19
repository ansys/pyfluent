"""Module proving property editor components."""


import re
from typing import List, Optional

from app_defn import app
from config import async_commands, commands_output
import dash
from dash import ALL, Input, Output, State, dcc, html
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

from ansys.fluent.core.solver.flobject import to_python_name
from ansys.fluent.core.utils.async_execution import asynchronous
from ansys.fluent.gui.components.component_base import ComponentBase
from ansys.fluent.gui.components.objects_handle import (
    LOCAL_ID,
    SETTINGS_ID,
    LocalObjectsHandle,
    SettingsObjectsHandle,
)
from ansys.fluent.gui.components.widgets_factory import (
    PropertyEditorDataType,
    widgets_factory,
)


class PropertyEditor(ComponentBase):
    """``PropertyEditor`` component."""

    _objects = {}

    def __init__(self, user_id, session_id, editor_type, index):
        unique_id = f"{user_id}-{session_id}-{editor_type}-{'default' if index is None else index}"
        editor = PropertyEditor._objects.get(unique_id)
        if not editor:
            PropertyEditor._objects[unique_id] = self.__dict__
            self._id = unique_id
            self._user_id = user_id
            self._session_id = session_id
            self._object_id = None
            self._filter_list = []
            self._index = index

            @app.callback(
                Output(f"property-editor-container-{self._id}", "children"),
                Input(f"object-id-{self._id}", "value"),
                prevent_initial_call=True,
            )
            def refresh_widgets(object_id):
                if object_id != self._object_id:
                    raise PreventUpdate
                return self.render()

            @app.callback(
                Output(f"object-id-{self._id}", "value"),
                Input(
                    {"type": f"input-widget", "index": ALL},
                    "value",
                ),
                prevent_initial_call=True,
            )
            def on_value_changed(
                input_values,
            ):
                ctx = dash.callback_context
                input_value = ctx.triggered[0]["value"]
                if input_value is None:
                    raise PreventUpdate
                else:
                    prop_id = eval(ctx.triggered[0]["prop_id"].split(".")[0])["index"]
                    (
                        input_index,
                        user_id,
                        session_id,
                        location_id,
                        object_path,
                        object_name,
                    ) = prop_id.split(":")
                    if location_id == LOCAL_ID:
                        obj, static_info = (
                            LocalObjectsHandle().get_object(
                                user_id, session_id, object_path, object_name
                            ),
                            None,
                        )
                        path_list = input_index.split("/")[1:]
                        for path in path_list:
                            obj = getattr(obj, path)
                    else:
                        (
                            obj,
                            static_info,
                        ) = SettingsObjectsHandle().get_object_and_static_info(
                            user_id, session_id, object_path, object_name
                        )
                        path_list = input_index.split("/")[1:]
                        for path in path_list:
                            if static_info["type"] == "named-object":
                                obj = obj[path]
                                static_info = static_info["object-type"]
                            else:
                                obj = getattr(obj, path)
                                static_info = static_info["children"][obj.obj_name]
                    if obj is None:
                        raise PreventUpdate

                    if isinstance(obj(), bool):
                        input_value = bool(input_value)
                    if input_value == obj():
                        raise PreventUpdate
                    obj.set_state(input_value)
                    object_id = f"{location_id}:{object_path}:{object_name}"
                    return object_id

            if editor_type == SETTINGS_ID:

                @app.callback(
                    Output(f"command-output-{self._id}", "value"),
                    Output(f"command-output-{self._id}", "style"),
                    Input(
                        {"type": "settings-command-button", "index": ALL}, "n_clicks"
                    ),
                    State({"type": "settings-command-input", "index": ALL}, "value"),
                )
                def on_settings_command_execution(
                    commands,
                    args_value,
                ):
                    ctx = dash.callback_context
                    triggered_value = ctx.triggered[0]["value"]
                    if not triggered_value:
                        raise PreventUpdate

                    (
                        command_name,
                        user_id,
                        session_id,
                        location_id,
                        object_path,
                        object_name,
                    ) = eval(ctx.triggered[0]["prop_id"].split(".")[0])["index"].split(
                        ":"
                    )

                    (
                        obj,
                        static_info,
                    ) = SettingsObjectsHandle().get_object_and_static_info(
                        user_id, session_id, object_path, object_name
                    )

                    kwargs = {}
                    exec_async = (
                        obj.path in async_commands
                        and command_name in async_commands[obj.path]
                    )
                    show_output = (
                        obj.path in commands_output
                        and command_name in commands_output[obj.path]
                    )
                    cmd_obj = getattr(obj, command_name)
                    # args_value is not correct.Will not work for multiple commands.
                    args_iter = iter(args_value)
                    args_info = static_info["commands"][cmd_obj.obj_name].get(
                        "arguments", {}
                    )
                    for arg_name, arg_info in args_info.items():
                        if arg_info["type"] == "boolean":
                            kwargs[to_python_name(arg_name)] = (
                                True if next(args_iter) else False
                            )
                        else:
                            kwargs[to_python_name(arg_name)] = next(args_iter)

                    @asynchronous
                    def run_async(f, **kwargs):
                        f(**kwargs)

                    return_value = (
                        run_async(cmd_obj, **kwargs)
                        if exec_async
                        else cmd_obj(**kwargs)
                    )
                    if show_output:
                        return (
                            commands_output[obj.path][command_name]["output"](
                                f"{return_value}"
                            ),
                            commands_output[obj.path][command_name]["style"],
                        )
                    return f"{return_value}", {"display": "none"}

        else:
            self.__dict__ = editor

    def __call__(self, object_id: str, filter_list: Optional[List] = []) -> html.Div:
        """Render customized ``PropertyEditor`` component.
        Parameters
        ----------
        object_id : str
            Object ID. It consists of `<location_id>:<object_path>:<object_name>`.
            location_id should be `settings` for ``SettingsPropertyEditor`` and `local`
            for ``LocalPropertyEditor``.
            object_path should be settings path for ``SettingsPropertyEditor``  and
            `Contour`, `Vector`, `Mesh` or 'Surface` for  ``LocalPropertyEditor``.
            object_name should be blank string ``SettingsPropertyEditor`` and object
            name for ``LocalPropertyEditor``.

        filter_list : list, optional
            If provided, widgets will be filtered as per the List i.e. only widget names
            passed in the list will be rendered.

        Returns
        --------
        html.Div
            Customized ``PropertyEditor`` component within html.Div container.
        """
        self._object_id = object_id
        self._filter_list = filter_list
        return html.Div(
            children=self.render(),
            id=f"property-editor-container-{self._id}",
        )

    def render(self) -> html.Div:
        """Render ``PropertyEditor`` component.
        Parameters
        ----------
        None

        Returns
        --------
        html.Div
            html.Div as ``PropertyEditor`` component.
        """
        location_id, object_path, object_name = self._object_id.split(":")
        all_input_widgets = self._get_widgets(
            self._user_id, self._session_id, object_path, object_name, "input"
        )
        all_command_widgets = self._get_widgets(
            self._user_id, self._session_id, object_path, object_name, "command"
        )
        object_path = object_path.split("/")[-1]
        object_name = object_path + "-" + object_name if object_name else object_path
        object_name = object_name.capitalize()
        return (
            html.Div(
                [
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                object_name,
                            ),
                            dbc.CardBody(
                                [
                                    v
                                    for k, v in all_input_widgets.items()
                                    if not self._filter_list or k in self._filter_list
                                ]
                            ),
                            html.Div(
                                [
                                    v
                                    for k, v in all_command_widgets.items()
                                    if not self._filter_list
                                    or k.split(":")[0] in self._filter_list
                                ]
                                + [html.Data(id=f"object-id-{self._id}")],
                                className="d-grid gap-1",
                                style={"padding": "0px 4px 0px 4px"},
                            ),
                        ],
                    ),
                ]
            ),
        )

    # Private methods
    def _get_widget(self, name, property_editor_data_type, id_type, id_index, **kwargs):
        widgets_provider = widgets_factory.get_widgets_provider("DBC")
        return widgets_provider.get_widget(
            self._get_label(name),
            property_editor_data_type,
            id_type,
            id_index,
            **kwargs,
        )

    def _get_label(self, name):
        name_list = re.split("[^a-zA-Z]", name)
        return " ".join([name.capitalize() for name in name_list])


class LocalPropertyEditor(PropertyEditor):
    """``LocalPropertyEditor`` component.

    Component for rendering local i.e graphics and plot objects.
    """

    _item_type_to_editor_type_map = {
        "<class 'str'>": PropertyEditorDataType.STRING,
        "typing.List[str]": PropertyEditorDataType.STRING_LIST,
        "<class 'bool'>": PropertyEditorDataType.BOOLEAN,
        "<class 'float'>": PropertyEditorDataType.REAL,
        "<class 'int'>": PropertyEditorDataType.INTEGER,
    }

    def __init__(self, user_id, session_id, index=None):
        super().__init__(user_id, session_id, LOCAL_ID, index)
        self._graphics_property_editor = GraphicsPropertyEditor()
        self._plot_property_editor = PlotPropertyEditor()
        self._get_objects_handle = LocalObjectsHandle()
        self._all_widgets = {}

    def _get_editor(self, object_path):
        return (
            self._graphics_property_editor
            if self._get_objects_handle.get_handle(object_path).type == "graphics"
            else self._plot_property_editor
        )

    def _get_widgets(self, user_id, session_id, object_path, object_name, widget_type):
        def store_all_widgets(obj_type, obj, parent=""):
            for name, value in obj.__dict__.items():
                if name == "_parent":
                    continue

                if value.__class__.__class__.__name__ in (
                    "PyLocalPropertyMeta",
                    "PyLocalObjectMeta",
                ):
                    visible = not hasattr(obj, "_availability") or getattr(
                        obj, "_availability"
                    )(name)

                    if not visible:
                        continue

                    if value.__class__.__class__.__name__ == "PyLocalPropertyMeta":
                        kwargs = {}
                        attributes = getattr(value, "attributes", None)
                        if attributes is not None:
                            if "allowed_values" in attributes:
                                kwargs["allowed-values"] = getattr(
                                    value, "allowed_values"
                                )
                            if "range" in attributes:
                                kwargs["range"] = getattr(value, "range")
                        kwargs["value"] = value()
                        widget = self._get_widget(
                            name=name,
                            property_editor_data_type=self._item_type_to_editor_type_map.get(
                                str(value._type), PropertyEditorDataType.UNDEFINED
                            ),
                            id_type="input-widget",
                            id_index=f"{parent}/{name}:{self._user_id}:{self._session_id}:{LOCAL_ID}:{object_path}:{object_name}",
                            **kwargs,
                        )
                        self._all_widgets[name] = widget
                    else:
                        store_all_widgets(
                            obj_type,
                            value,
                            parent + "/" + name,
                        )

        obj = self._get_objects_handle.get_object(
            user_id, session_id, object_path, object_name
        )

        if widget_type == "input":
            self._all_widgets = {}
            store_all_widgets(object_path, obj)
            return self._all_widgets
        else:
            return self._get_editor(object_path)._get_widgets(
                user_id, session_id, object_path, object_name, self._index
            )


class GraphicsPropertyEditor:
    """``GraphicsPropertyEditor`` component.

    Component for rendering graphics objects.
    """

    def _get_widgets(self, user_id, session_id, object_path, object_name, editor_index):
        widgets = {
            "display-button": dbc.Button(
                "Display",
                id={
                    "type": "post-render-button",
                    "index": f"{user_id}:{session_id}:{LOCAL_ID}:{object_path}:{object_name}:{editor_index}",
                },
                n_clicks=0,
                size="sm",
            )
        }
        widgets.update(
            {
                "delete-button": dbc.Button(
                    "Delete",
                    id={
                        "type": "graphics-button",
                        "index": f"{user_id}:{session_id}:{LOCAL_ID}:{object_path}:{object_name}:delete:{editor_index}",
                    },
                    n_clicks=0,
                    size="sm",
                ),
            }
            if object_name
            else {
                "new-button": dbc.Button(
                    "New",
                    id={
                        "type": "graphics-button",
                        "index": f"{user_id}:{session_id}:{LOCAL_ID}:{object_path}:{object_name}:new:{editor_index}",
                    },
                    n_clicks=0,
                    size="sm",
                ),
            }
        )
        return widgets


class PlotPropertyEditor:
    """``PlotPropertyEditor`` component.

    Component for rendering plot objects.
    """

    def _get_widgets(self, user_id, session_id, object_path, object_name, editor_index):

        widgets = {
            "plot-button": dbc.Button(
                "Plot",
                id={
                    "type": "post-render-button",
                    "index": f"{user_id}:{session_id}:{LOCAL_ID}:{object_path}:{object_name}:{editor_index}",
                },
                n_clicks=0,
                size="sm",
            )
        }
        widgets.update(
            {
                "delete-button": dbc.Button(
                    "Delete",
                    id={
                        "type": "graphics-button",
                        "index": f"{user_id}:{session_id}:{LOCAL_ID}:{object_path}:{object_name}:delete:{editor_index}",
                    },
                    n_clicks=0,
                    size="sm",
                ),
            }
            if object_name
            else {
                "new-button": dbc.Button(
                    "New",
                    id={
                        "type": "graphics-button",
                        "index": f"{user_id}:{session_id}:{LOCAL_ID}:{object_path}:{object_name}:new:{editor_index}",
                    },
                    n_clicks=0,
                    size="sm",
                ),
            }
        )
        return widgets


class SettingsPropertyEditor(PropertyEditor):
    """``SettingsPropertyEditor`` component.

    Component for rendering settings objects.
    """

    _item_type_to_editor_type_map = {
        "string": PropertyEditorDataType.STRING,
        "string-list": PropertyEditorDataType.STRING_LIST,
        "boolean": PropertyEditorDataType.BOOLEAN,
        "real": PropertyEditorDataType.REAL,
        "integer": PropertyEditorDataType.INTEGER,
    }

    def __init__(self, user_id, session_id, index=None):
        super().__init__(user_id, session_id, SETTINGS_ID, index)
        self._all_widgets = {}

    def _get_widgets(self, user_id, session_id, object_path, object_name, widget_type):
        def store_all_input_widgets(obj, si_info, state, parent=""):
            try:
                items = obj.get_state().items()
            except AttributeError:
                print(obj.path, "State is empty")
                return
            for name, value in items:
                if si_info["type"] == "named-object":
                    child_obj = obj[name]
                    si_info_child = si_info["object-type"]
                else:
                    child_obj = getattr(obj, name)
                    si_info_child = si_info["children"][child_obj.obj_name]
                if si_info_child["type"] not in ("group", "named-object"):
                    kwargs = {}
                    if si_info_child.get("has_allowed_values"):
                        kwargs["allowed-values"] = child_obj.get_attr("allowed-values")
                    if si_info_child.get("has_range"):
                        kwargs["range"] = (child_obj.get_attr("range"),)
                    kwargs["value"] = child_obj()
                    widget = self._get_widget(
                        name=name,
                        property_editor_data_type=self._item_type_to_editor_type_map.get(
                            si_info_child["type"], PropertyEditorDataType.UNDEFINED
                        ),
                        id_type="input-widget",
                        id_index=f"{parent}/{name}:{self._user_id}:{self._session_id}:{SETTINGS_ID}:{object_path}:{object_name}",
                        **kwargs,
                    )
                    self._all_widgets[name] = widget
                elif si_info_child["type"] not in ("named-object"):
                    store_all_input_widgets(
                        child_obj,
                        si_info_child,
                        state[name],
                        parent + "/" + name,
                    )

        def store_all_command_buttons(obj, si_info):
            commands = si_info.get("commands", [])
            for command_name in commands:
                try:
                    cmd_obj = getattr(obj, to_python_name(command_name))
                except AttributeError:
                    continue
                if not cmd_obj.is_active():
                    continue
                self._all_widgets[command_name] = dbc.Button(
                    self._get_label(command_name),
                    id={
                        "type": "settings-command-button",
                        "index": f"{to_python_name(command_name)}:{self._user_id}:{self._session_id}:{SETTINGS_ID}:{object_path}:{object_name}",
                    },
                    n_clicks=0,
                    size="sm",
                )
                si_info_command = si_info["commands"][cmd_obj.obj_name]
                command_args = si_info_command.get("arguments", {})
                for command_arg, arg_info in command_args.items():
                    command_arg_obj = getattr(cmd_obj, to_python_name(command_arg))
                    kwargs = {}
                    if arg_info.get("has_allowed_values"):
                        kwargs["allowed-values"] = command_arg_obj.get_attr(
                            "allowed-values"
                        )
                    if arg_info.get("has_range"):
                        kwargs["range"] = (command_arg_obj.get_attr("range"),)
                    widget = self._get_widget(
                        name=command_arg,
                        property_editor_data_type=self._item_type_to_editor_type_map.get(
                            arg_info["type"], PropertyEditorDataType.UNDEFINED
                        ),
                        id_type="settings-command-input",
                        id_index=f"{command_name}:{command_arg}",
                        **kwargs,
                    )
                    self._all_widgets[command_name + ":" + command_arg] = widget

            self._all_widgets["command_output"] = dcc.Textarea(
                id=f"command-output-{self._id}", style={"display": "none"}
            )

        obj, static_info = SettingsObjectsHandle().get_object_and_static_info(
            user_id, session_id, object_path, object_name
        )
        self._all_widgets = {}
        if widget_type == "input":
            store_all_input_widgets(obj, static_info, obj.get_state())
        else:
            store_all_command_buttons(obj, static_info)
        return self._all_widgets
