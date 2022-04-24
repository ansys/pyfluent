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
from ansys.fluent.core.solver.flobject import to_python_name

set_config(blocking=False)
DISPLAY_BUTTON_ID = "display-graphics-button"
PLOT_BUTTON_ID = "plot-graph-button"


class SettingsPropertyEditor:
    def __init__(self, app, SessionsManager):
        self._app = app
        self._all_widgets = {}
        self.SessionsManager = SessionsManager  
        self._type_to_path = {
            "Viscous": "setup/models/viscous",
            "Multiphase": "setup/models/multiphase",
            "Initialization": "solution/initialization",
            "calculation": "solution/run_calculation",
        }        

        @self._app.callback(
            Output(f"command-output", "value"),
            Input(
                {"type": "settings-command-button", "index": ALL}, "n_clicks"
            ),            
            Input("connection-id", "data"),
            State(
                {"type": "settings-command-input", "index": ALL}, "value"
            ),            
            State("session-id", "value"),
            State("object-id", "value"),
        )
        def on_settings_command_execution(
            commnads,
            connection_id,
            args_value,
            session_id,
            object_id,
        ):
            print('on_settings_command_execution', connection_id, args_value, session_id, object_id)
            if object_id is None or session_id is None:
                raise PreventUpdate 
            object_location, object_type = object_id.split(":")                
            if object_location != "remote":
                raise PreventUpdate        
            ctx = dash.callback_context
            n_clicks = ctx.triggered[0]["value"]
            if not n_clicks:
                raise PreventUpdate
            command_name = eval(ctx.triggered[0]["prop_id"].split(".")[0])["index"]            
            print("on_command_execution", command_name, n_clicks, args_value, ctx.triggered)
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
            return_value = cmd_obj(**kwargs)
            return f"{return_value}"        

    def get_object_and_static_info(
        self, object_type, connection_id, session_id, object_id=None
    ):        
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


    def get_label(self, name):
        name_list = re.split("[^a-zA-Z]", name)
        return " ".join([name.capitalize() for name in name_list])
            
    def get_widgets(self, object_type, connection_id, session_id):
    
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
                    self._all_widgets[name] = widget
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
                self._all_widgets[command_name] = dbc.Button(
                  self.get_label(command_name),
                  id = {"type": "settings-command-button", "index": command_name},
                  n_clicks=0,
                )               
                si_info_command = si_info["commands"][cmd_obj.scheme_name]
                command_args = si_info_command['arguments']
                for command_arg, arg_info in command_args.items():
                    if arg_info['type']=="integer":
                        self._all_widgets[command_arg] = dcc.Input(
                            id={"type": "settings-command-input", "index": command_name+":"+command_arg},
                            type="number"                            
                        ) 
                    if arg_info['type']=="real":
                        self._all_widgets[command_arg] = dcc.Input(
                            id={"type": "settings-command-input", "index": command_name+":"+command_arg},
                            type="number"                            
                        )                             

        obj, static_info = self.get_object_and_static_info(
            object_type, connection_id, session_id
        )
        self._all_widgets = {}
        print("update_stored_widgets", obj, obj.get_state())
        store_all_widgets(obj, static_info, obj.get_state())
        store_all_buttons(obj, static_info)
        return self._all_widgets                        

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
                id={"type":"input-widget", "index": path},
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