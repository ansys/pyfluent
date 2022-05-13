import dash_bootstrap_components as dbc
from dash import html
import dash_core_components as dcc

from ansys.fluent.core.solver.flobject import to_python_name
from property_editor import PropertyEditor
from objects_handle import SettingsObjectsHandle
from sessions_manager import SessionsManager
from ansys.fluent.post import set_config
set_config(blocking=False)



class SettingsPropertyEditor(PropertyEditor):
    def __init__(self):
        super().__init__()
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

                print(name, si_info_child["type"])
                if si_info_child["type"] not in ("group", "named-object"):
                    widget = self.get_widget(
                        child_obj,
                        name,
                        f"{parent}/{name}:remote:{object_type}:{object_index}",
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
            print("commands", obj, commands)
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
                        "index": f"{to_python_name(command_name)}:remote:{object_type}:{object_index}",
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

        obj, static_info = SettingsObjectsHandle(SessionsManager).get_object_and_static_info(
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
