import itertools
import re

from app_defn import app
from dash import ALL, Input, Output, State, dcc, html
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from objects_handle import LocalObjectsHandle, SettingsObjectsHandle
from sessions_handle import SessionsHandle

from ansys.fluent.core.solver.flobject import to_python_name


class PropertyEditor:

    _editors = {}

    def __init__(self, user_id, session_id, editor_type, index):
        unique_id = f"{user_id}-{session_id}-{editor_type}-{'default' if index is None else index}"
        editor = PropertyEditor._editors.get(unique_id)
        if not editor:
            PropertyEditor._editors[unique_id] = self.__dict__
            self._id = unique_id
            self._user_id = user_id
            self._session_id = session_id
            self._object_id = None
            self._filter_list = []
            self._index = index

            @app.callback(
                Output(f"property-editor-{self._id}", "children"),
                Input("object-id", "value"),
                prevent_initial_call=True,
            )
            def refresh_widgets(object_id):
                if object_id != self._object_id:
                    raise PreventUpdate
                return self.render(self._user_id, self._session_id, object_id)

        else:
            self.__dict__ = editor

    def __call__(self, object_id, filter_list=[]):
        self._object_id = object_id
        self._filter_list = filter_list
        return html.Div(
            children=self.render(self._user_id, self._session_id, self._object_id),
            id=f"property-editor-{self._id}",
        )

    def get_label(self, name):
        name_list = re.split("[^a-zA-Z]", name)
        return " ".join([name.capitalize() for name in name_list])

    def render(self, user_id, session_id, object_id):
        object_location, object_type, object_index = object_id.split(":")
        all_input_widgets = self.get_widgets(
            user_id, session_id, object_type, object_index, "input"
        )
        all_command_widgets = self.get_widgets(
            user_id, session_id, object_type, object_index, "command"
        )
        object_type = object_type.split("/")[-1]
        object_name = object_type + "-" + object_index if object_index else object_type
        object_name = object_name.capitalize()
        return (
            dbc.Col(
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
                                ],
                                className="d-grid gap-1",
                                style={"padding": "4px 4px 4px 4px"},
                            ),
                        ],
                    ),
                ]
            ),
        )


class LocalPropertyEditor(PropertyEditor):
    def __init__(self, user_id, session_id, index=None):
        super().__init__(user_id, session_id, "local", index)
        self._all_widgets = {}
        self._graphics_property_editor = GraphicsPropertyEditor()
        self._plot_property_editor = PlotPropertyEditor()
        self._get_objects_handle = LocalObjectsHandle(SessionsHandle)

    def _get_editor(self, object_type):
        return (
            self._graphics_property_editor
            if self._get_objects_handle.get_handle(object_type).type == "graphics"
            else self._plot_property_editor
        )

    def get_widgets(
        self, connection_id, session_id, object_type, object_index, widget_type
    ):
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
                        widget = self.get_widget(
                            value,
                            value._type,
                            name,
                            f"{parent}/{name}:{self._user_id}:{self._session_id}:local:{object_type}:{object_index}",
                            # parent + "/" + name+":local:"+object_type+":"+object_index,
                            getattr(value, "attributes", None),
                        )
                        self._all_widgets[name] = widget
                    else:
                        store_all_widgets(
                            obj_type,
                            value,
                            parent + "/" + name,
                        )

        obj = self._get_objects_handle.get_object(
            connection_id, session_id, object_type, object_index
        )

        if widget_type == "input":
            self._all_widgets = {}
            store_all_widgets(object_type, obj)
            return self._all_widgets
        else:
            return self._get_editor(object_type).get_widgets(
                connection_id, session_id, object_type, object_index, self._index
            )

    def get_widget(
        self,
        obj,
        type,
        name,
        unique_name,
        attributes,
    ):
        widget = html.Div(f"Widget not found for {name}.")
        if str(type) == "<class 'str'>":
            if attributes and "allowed_values" in attributes:
                widget = dcc.Dropdown(
                    id={
                        "type": f"input-widget",
                        "index": unique_name,
                    },
                    options=getattr(obj, "allowed_values"),
                    value=obj(),
                )
            else:
                widget = dcc.Input(
                    id={
                        "type": f"input-widget",
                        "index": unique_name,
                    },
                    type="text",
                    value=obj(),
                )
        elif str(type) == "typing.List[str]":
            widget = dcc.Dropdown(
                id={
                    "type": f"input-widget",
                    "index": unique_name,
                },
                options=getattr(obj, "allowed_values"),
                value=obj(),
                multi=True,
            )
            # print('widget', widget)
        elif str(type) == "<class 'bool'>":
            widget = dcc.Checklist(
                id={
                    "type": f"input-widget",
                    "index": unique_name,
                },
                options={
                    "selected": self.get_label(name),
                },
                value=["selected"] if obj() else [],
                style={"padding": "5px"},
                labelStyle={"display": "inline-block"},
                inputStyle={"padding": "1px 1px 1px 5px"},
            )
        elif str(type) == "<class 'float'>":
            if attributes and "range" in attributes:
                range = getattr(obj, "range")
                widget = dcc.Input(
                    id={
                        "type": f"input-widget",
                        "index": unique_name,
                    },
                    type="number",
                    value=obj(),
                    min=range[0] if range else None,
                    max=range[1] if range else None,
                )
            else:
                widget = dcc.Input(
                    id={
                        "type": f"input-widget",
                        "index": unique_name,
                    },
                    type="number",
                    value=obj(),
                )
        elif str(type) == "<class 'int'>":
            if attributes and "range" in attributes:
                widget = dcc.Input(
                    id={
                        "type": f"input-widget",
                        "index": unique_name,
                    },
                    type="number",
                    value=obj(),
                    min=getattr(obj, "range")[0],
                    max=getattr(obj, "range")[1],
                )
            else:
                widget = dcc.Input(
                    id={
                        "type": f"input-widget",
                        "index": unique_name,
                    },
                    type="number",
                    value=obj(),
                )

        if str(type) == "<class 'bool'>":
            widget = html.Div(
                [widget],
            )
        else:
            widget = html.Div(
                [
                    dbc.Label(self.get_label(name)),
                    widget,
                ],
                style={
                    "display": "flex",
                    "flex-direction": "column",
                    "padding": "4px",
                },
            )
        return widget


class GraphicsPropertyEditor:
    def get_widgets(
        self, connection_id, session_id, object_type, object_index, editor_index
    ):
        return (
            {
                "display-button": dbc.Button(
                    "Display",
                    id={
                        "type": "post-render-button",
                        "index": f"{connection_id}:{session_id}:local:{object_type}:{object_index}:{editor_index}",
                    },
                    n_clicks=0,
                    size="sm",
                ),
                "delete-button": dbc.Button(
                    "Delete",
                    id={
                        "type": "graphics-button",
                        "index": f"{connection_id}:{session_id}:local:{object_type}:{object_index}:delete:{editor_index}",
                    },
                    n_clicks=0,
                    size="sm",
                ),
            }
            if object_index
            else {
                "display-button": dbc.Button(
                    "Display",
                    id={
                        "type": "post-render-button",
                        "index": f"{connection_id}:{session_id}:local:{object_type}:{object_index}:{editor_index}",
                    },
                    n_clicks=0,
                    size="sm",
                ),
                "new-button": dbc.Button(
                    "New",
                    id={
                        "type": "graphics-button",
                        "index": f"{connection_id}:{session_id}:local:{object_type}:{object_index}:new:{editor_index}",
                    },
                    n_clicks=0,
                    size="sm",
                ),
            }
        )


class PlotPropertyEditor:
    def get_widgets(
        self, connection_id, session_id, object_type, object_index, editor_index
    ):
        return (
            {
                "plot-button": dbc.Button(
                    "Plot",
                    id={
                        "type": "post-render-button",
                        "index": f"{connection_id}:{session_id}:local:{object_type}:{object_index}:{editor_index}",
                    },
                    n_clicks=0,
                    size="sm",
                ),
                "delete-button": dbc.Button(
                    "Delete",
                    id={
                        "type": "graphics-button",
                        "index": f"{connection_id}:{session_id}:local:{object_type}:{object_index}:delete:{editor_index}",
                    },
                    n_clicks=0,
                    size="sm",
                ),
            }
            if object_index
            else {
                "plot-button": dbc.Button(
                    "Plot",
                    id={
                        "type": "post-render-button",
                        "index": f"{connection_id}:{session_id}:local:{object_type}:{object_index}:{editor_index}",
                    },
                    n_clicks=0,
                    size="sm",
                ),
                "new-button": dbc.Button(
                    "New",
                    id={
                        "type": "graphics-button",
                        "index": f"{connection_id}:{session_id}:local:{object_type}:{object_index}:new:{editor_index}",
                    },
                    n_clicks=0,
                    size="sm",
                ),
            }
        )


class SettingsPropertyEditor(PropertyEditor):
    def __init__(self, user_id, session_id, index=None):
        super().__init__(user_id, session_id, "settings", index)
        self._all_widgets = {}

    def get_widgets(
        self, connection_id, session_id, object_type, object_index, widget_type
    ):
        def store_all_input_widgets(obj, si_info, state, parent=""):
            for name, value in obj.get_state().items():
                if si_info["type"] == "named-object":
                    child_obj = obj[name]
                    si_info_child = si_info["object-type"]
                else:
                    child_obj = getattr(obj, name)
                    si_info_child = si_info["children"][child_obj.obj_name]
                if si_info_child["type"] not in ("group", "named-object"):
                    widget = self.get_widget(
                        child_obj,
                        name,
                        f"{parent}/{name}:{self._user_id}:{self._session_id}:remote:{object_type}:{object_index}",
                        si_info_child,
                    )
                    self._all_widgets[name] = widget
                else:
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
                    self.get_label(command_name),
                    id={
                        "type": "settings-command-button",
                        "index": f"{to_python_name(command_name)}:{self._user_id}:{self._session_id}:remote:{object_type}:{object_index}",
                    },
                    n_clicks=0,
                    size="sm",
                )
                si_info_command = si_info["commands"][cmd_obj.obj_name]
                command_args = si_info_command.get("arguments", {})
                for command_arg, arg_info in command_args.items():
                    if arg_info["type"] == "integer":
                        self._all_widgets[command_name + ":" + command_arg] = dcc.Input(
                            id={
                                "type": "settings-command-input",
                                "index": command_name + ":" + command_arg,
                            },
                            type="number",
                        )
                    if arg_info["type"] == "real":
                        self._all_widgets[command_name + ":" + command_arg] = dcc.Input(
                            id={
                                "type": "settings-command-input",
                                "index": command_name + ":" + command_arg,
                            },
                            type="number",
                        )

        obj, static_info = SettingsObjectsHandle(
            SessionsHandle
        ).get_object_and_static_info(
            connection_id, session_id, object_type, object_index
        )
        self._all_widgets = {}
        if widget_type == "input":
            store_all_input_widgets(obj, static_info, obj.get_state())
        else:
            store_all_command_buttons(obj, static_info)
        return self._all_widgets

    def get_widget(
        self,
        obj,
        name,
        path,
        static_info,
    ):
        # print("get_widget", obj, name, path)
        widget = html.Div("Widget not found.")
        if static_info["type"] == "string":
            if static_info.get("has_allowed_values"):
                widget = dcc.Dropdown(
                    id={"type": "input-widget", "index": path},
                    options=obj.get_attr("allowed-values"),
                    value=obj(),
                )
            else:
                widget = dcc.Input(
                    id={"type": "input-widget", "index": path},
                    type="text",
                    value=obj(),
                )
        elif static_info["type"] == "string-list":
            widget = dcc.Dropdown(
                id={"type": "input-widget", "index": path},
                options=obj.get_attr("allowed-values"),
                value=obj(),
                multi=True,
            )
            # print('widget', widget)
        elif static_info["type"] == "boolean":
            widget = dcc.Checklist(
                id={"type": "input-widget", "index": path},
                options={
                    "selected": self.get_label(name),
                },
                value=["selected"] if obj() else [],
                style={"padding": "5px 5px"},
            )
        elif static_info["type"] == "real":
            if static_info.get("has_range"):
                range = (obj.get_attr("range"),)
                widget = dcc.Input(
                    id={"type": "input-widget", "index": path},
                    type="number",
                    value=obj(),
                    min=range[0] if range else None,
                    max=range[1] if range else None,
                )
            else:
                widget = dcc.Input(
                    id={"type": "input-widget", "index": path},
                    type="number",
                    value=obj(),
                )
        elif static_info["type"] == "integer":
            if static_info.get("has_range"):
                range = (obj.get_attr("range"),)
                widget = dcc.Input(
                    id={"type": "input-widget", "index": path},
                    type="number",
                    value=obj(),
                    min=range[0] if range else None,
                    max=range[1] if range else None,
                )
            else:
                widget = dcc.Input(
                    id={"type": "input-widget", "index": path},
                    type="number",
                    value=obj(),
                )

        if static_info["type"] == "boolean":
            widget = html.Div([widget], style={"padding": "10px 1px 2px"})
        else:
            widget = html.Div(
                [
                    dbc.Label(self.get_label(name)),
                    widget,
                ],
                style={
                    "display": "flex",
                    "flex-direction": "column",
                    "padding": "4px",
                },
            )
        return widget
