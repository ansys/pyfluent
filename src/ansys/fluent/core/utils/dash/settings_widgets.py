from functools import partial
import dash_bootstrap_components as dbc
from dash import html
import dash_core_components as dcc
import dash_vtk
from dash.dependencies import Input, Output, State, MATCH, ALL
import dash
from dash.exceptions import PreventUpdate
import re
from ansys.fluent.core.utils.generic import SingletonMeta
from ansys.fluent.post.pyvista import Graphics
from ansys.fluent.post.matplotlib import Plots
from ansys.fluent.post.pyvista.pyvista_objects import (
    Contour,
    Mesh,
    Surface,
    Vector,
)
from ansys.fluent.post import set_config
from post_data import update_vtk_fun, update_graph_fun

set_config(blocking=False)
from ansys.fluent.core.solver.flobject import to_python_name


class SettingsWidgetBase:
    def __init__(self, app, id, SessionsManager):
        self._app = app
        self._id = id
        self._selected_object_type = None
        self._all_widgets = {}
        self.SessionsManager = SessionsManager
        self.create_callback()

    def get_label(self, name):
        name_list = re.split("[^a-zA-Z]", name)
        return " ".join([name.capitalize() for name in name_list])

    def get_unique_name(self, name):
        return name

    def get_object_and_static_info(
        self, object_type, connection_id, session_id, object_id=None
    ):
        self._selected_object_type = object_type
        if object_type is not None:
            object_type_path = self._type_to_path[object_type]
            path_list = object_type_path.split("/")
            session = self.SessionsManager(
                self._app, connection_id, session_id
            ).session
            static_info = self.SessionsManager(
                self._app, connection_id, session_id
            ).static_info
            obj = self.SessionsManager(
                self._app, connection_id, session_id
            ).settings_root
            for path in path_list:
                obj = getattr(obj, path)
                static_info = static_info["children"][obj.scheme_name]
            return obj, static_info

    def create_callback(self):
        def store_all_widgets(obj, si_info, state, parent=""):
            for name, value in obj.get_state().items():
                child_obj = getattr(obj, name)
                si_info_child = si_info["children"][child_obj.scheme_name]
                
                if si_info_child["type"] != "group":
                    widget = self.get_widget(
                        child_obj,
                        name,
                        parent + "/" + name,
                        si_info_child,
                    )
                    self._all_widgets[self.get_unique_name(name)] = widget
                else:
                    store_all_widgets(
                        child_obj,
                        si_info_child,
                        state[name],
                        parent + "/" + name,
                    )
        def store_all_buttons(obj, si_info):
            commands  = si_info.get("commands",[])
            for command_name in commands:
                try:             
                    cmd_obj = getattr(obj, command_name)
                except AttributeError:
                    continue                
                if not cmd_obj.is_active():
                    continue
                self._all_widgets[self.get_unique_name(command_name)] = dbc.Button(
                  self.get_label(command_name),
                  id = {"type": f"settings-command-button-{self._id}", "index": command_name},
                  n_clicks=0,
                )               
                si_info_command = si_info["commands"][cmd_obj.scheme_name]
                command_args = si_info_command['arguments']
                for command_arg, arg_info in command_args.items():
                    if arg_info['type']=="integer":
                        self._all_widgets[self.get_unique_name(command_arg)] = dcc.Input(
                            id={"type": f"settings-command-widget-{self._id}", "index": command_name+":"+command_arg},
                            type="number"                            
                        ) 
                    if arg_info['type']=="real":
                        self._all_widgets[self.get_unique_name(command_arg)] = dcc.Input(
                            id={"type": f"settings-command-widget-{self._id}", "index": command_name+":"+command_arg},
                            type="number"                            
                        )                         
                   
        @self._app.callback(
            Output(f"command-output-{self._id}", "value"),
            Input(
                {"type": f"settings-command-button-{self._id}", "index": ALL}, "n_clicks"
            ),            
            Input("connection-id", "data"),
            State(
                {"type": f"settings-command-widget-{self._id}", "index": ALL}, "value"
            ),            
            State("sessions", "value"),
            State(f"selected-object-type-{self._id}", "value"),
        )
        def on_command_execution(
            commnads,
            connection_id,
            args_value,
            session_id,
            object_type,
        ):
            ctx = dash.callback_context
            prop_value = ctx.triggered[0]["value"]
            if prop_value is None:
                raise PreventUpdate
            command_name = eval(ctx.triggered[0]["prop_id"].split(".")[0])["index"]            
            print("on_command_execution", command_name, prop_value, args_value, ctx.triggered)
            obj, static_info = self.get_object_and_static_info(
                object_type, connection_id, session_id
            )
            kwargs = {}
            cmd_obj = getattr(obj, command_name)
            args_iter = iter(args_value)
            args_info = static_info["commands"][cmd_obj.scheme_name]["arguments"]
            for arg_name, arg_info in  args_info.items():
                kwargs[to_python_name(arg_name)] =  next(args_iter)
            print(kwargs)    
            cmd_obj(**kwargs)
            return ""
                                                  

        def update_stored_widgets(object_type, connection_id, session_id):
            obj, static_info = self.get_object_and_static_info(
                object_type, connection_id, session_id
            )
            self._all_widgets = {}
            print("update_stored_widgets", obj, obj.get_state())
            store_all_widgets(obj, static_info, obj.get_state())
            store_all_buttons(obj, static_info)

        @self._app.callback(
            Output(f"refresh-settings-trigger-{self._id}", "value"),
            Input(
                {"type": f"settings-widget-{self._id}", "index": ALL}, "value"
            ),
            Input("connection-id", "data"),
            State("sessions", "value"),
            State(f"selected-object-type-{self._id}", "value"),
        )
        def on_value_changed(
            values,
            connection_id,
            session_id,
            object_type,
        ):
            ctx = dash.callback_context
            prop_value = ctx.triggered[0]["value"]
            if prop_value is None:
                raise PreventUpdate
            prop_id = eval(ctx.triggered[0]["prop_id"].split(".")[0])["index"]

            print("value_changed", prop_id, prop_value)
            obj, static_info = self.get_object_and_static_info(
                object_type, connection_id, session_id
            )
            path_list = prop_id.split("/")[1:]
            for path in path_list:
                obj = getattr(obj, path)
                if obj is None:
                    raise PreventUpdate

            if static_info["type"] == "boolean":
                prop_value = True if prop_value else False
            if prop_value == obj():
                print("PreventUpdate value is same.")
                raise PreventUpdate
            obj.set_state(prop_value)
            return str(prop_id) + str(prop_value)

        @self._app.callback(
            Output(f"settings-card-body-{self._id}", "children"),
            Input(f"refresh-settings-trigger-{self._id}", "value"),
            Input("connection-id", "data"),
            Input(f"selected-object-type-{self._id}", "value"),
            State("sessions", "value"),
        )
        def refresh_widgets(_, connection_id, object_type, session_id):
            print(
                "show hide settings", _, connection_id, session_id, object_type
            )
            if object_type is None or session_id is None:
                raise PreventUpdate
            update_stored_widgets(object_type, connection_id, session_id)
            return list(self._all_widgets.values())
                      

    def get_widget(
        self,
        obj,
        name,
        path,
        static_info,
    ):
        print("get_widget", obj, name, path)
        widget = html.Div(f"Widget not found for {name}.")
        if static_info["type"] == "string":
            if static_info.get("has_allowed_values"):
                widget = dcc.Dropdown(
                    id={"type": f"settings-widget-{self._id}", "index": path},
                    options=obj.get_attr("allowed-values"),
                    value=obj(),
                )
            else:
                widget = dcc.Input(
                    id={"type": f"settings-widget-{self._id}", "index": path},
                    type="text",
                    value=obj(),
                )
        elif static_info["type"] == "string-list":
            widget = dcc.Dropdown(
                id={"type": f"settings-widget-{self._id}", "index": path},
                options=obj.get_attr("allowed-values"),
                value=obj(),
                multi=True,
            )
            # print('widget', widget)
        elif static_info["type"] == "boolean":
            widget = dcc.Checklist(
                id={"type": f"settings-widget-{self._id}", "index": path},
                options={
                    "selected": self.get_label(name),
                },
                value=["selected"] if obj() else [],
                style={"padding": "5px"},
                labelStyle={"display": "inline-block"},
                inputStyle={"padding": "1px 1px 1px 5px"},
            )
        elif static_info["type"] == "real":
            if static_info.get("has_range"):
                range = (obj.get_attr("range"),)
                widget = dcc.Input(
                    id={"type": f"settings-widget-{self._id}", "index": path},
                    type="number",
                    value=obj(),
                    min=range[0] if range else None,
                    max=range[1] if range else None,
                )
            else:
                widget = dcc.Input(
                    id={"type": f"settings-widget-{self._id}", "index": path},
                    type="number",
                    value=obj(),
                )
        elif static_info["type"] == "integer":
            if static_info.get("has_range"):
                range = (obj.get_attr("range"),)
                widget = dcc.Input(
                    id={"type": f"settings-widget-{self._id}", "index": path},
                    type="number",
                    value=obj(),
                    min=range[0] if range else None,
                    max=range[1] if range else None,
                )
            else:
                widget = dcc.Input(
                    id={"type": f"settings-widget-{self._id}", "index": path},
                    type="number",
                    value=obj(),
                )

        if static_info["type"] == "boolean":
            widget = html.Div(
                [widget],
            )
        else:
            widget = html.Div(
                [
                    dbc.Label(self.get_label(name)),
                    widget,
                ],
            )
        return widget


class SettingsWidget(SettingsWidgetBase):

    _state = {}

    def __init__(self, app, connection_id, session_id, SessionsManager):
        id = f"settings-{session_id}-{connection_id}"
        window_state = SettingsWidget._state.get(id)
        if not window_state:
            SettingsWidget._state[id] = self.__dict__
            self._type_to_path = {}
            self._type_to_path = {
                "Viscous": "setup/models/viscous",
                "Multiphase": "setup/models/multiphase",
                "Initialization": "solution/initialization",
                "calculation": "solution/run_calculation",
            }
            super().__init__(app, id, SessionsManager)
        else:
            self.__dict__ = window_state

    def layout(self):

        return dbc.Row(
            [
                dbc.Col(
                    [
                        html.Data(id=f"command-output-{self._id}"),
                        html.Data(id=f"refresh-settings-trigger-{self._id}"),
                    ],
                ),
                dbc.Col(
                    [
                        html.Div(
                            [
                                dbc.Label("Select Settings"),
                                dcc.Dropdown(
                                    id=f"selected-object-type-{self._id}",
                                    options=list(self._type_to_path.keys()),
                                    value=self._selected_object_type,
                                ),
                            ],
                            style={
                                "padding": "1px 1px 10px 1px",
                                "width": "20rem",
                            },
                        ),
                    ]
                    + [
                        html.Div(
                            html.Div(
                                id=f"settings-card-body-{self._id}",
                                children=list(self._all_widgets.values()),
                            ),
                            className="mb-3",
                            style={
                                "padding": "1px 1px 10px 1px",
                                "width": "20rem",
                            },
                        )
                    ],
                    width="auto",
                ),
            ],
            style={"height": "50rem"},
        )
