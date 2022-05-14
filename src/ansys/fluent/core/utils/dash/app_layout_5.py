import dash
from app_defn import app
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash import Input, Output, State, ALL
from flask import request
from sessions_manager import SessionsManager


from settings_property_editor import SettingsPropertyEditor
from local_property_editor import LocalPropertyEditor
from post_windows import MonitorWindow, GraphicsWindowCollection





def get_post_objects(user_id, session_id):
    return dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Dropdown(
                        id="post-object-type",
                        options=["Mesh", "Surface", "Contour", "Vector"],
                        value="Contour",
                        style={"padding": "10px 5px 5px 5px"},
                    ),
                    html.Div(id="post-object-container"),
                ],
                width="auto",
                style={"width": "350px"},
            ),
            dbc.Col([GraphicsWindowCollection(user_id, session_id, 1)()]),
        ]
    )


def get_setup_objects(user_id, session_id):
    return dbc.Row(
        [
            dbc.Col(
                [
                    SettingsPropertyEditor(user_id, session_id, 1)("remote:setup/models/viscous:"),                   
                    SettingsPropertyEditor(user_id, session_id, 2)("remote:solution/initialization:",
                        ["standard-initialize"],
                    ),
                    SettingsPropertyEditor(user_id, session_id, 3)(                       
                        "remote:solution/run_calculation:",
                        ["iterate"],
                    ),                    
                ],
                width="auto",
                style={"width": "350px"},
            ),
            dbc.Col([
            
            MonitorWindow(user_id, session_id)(),
            #MonitorWindow(user_id, "session-1")()
            
            ]
            
            
            ),
        ]
    )


def app_layout():
    user_id = request.authorization["username"]
    session_id = "session-0"
    sessions_manager = SessionsManager(user_id, session_id)
    sessions_manager.add_session("53583", None)
    MonitorWindow(user_id, session_id)
   
    
    #session_id = "session-1"
    #sessions_manager = SessionsManager(user_id, session_id)
    #sessions_manager.add_session("59801", None)    
    #MonitorWindow(user_id, "session-1")    
    
    
    SettingsPropertyEditor(user_id, session_id, 1)
    SettingsPropertyEditor(user_id, session_id, 2)
    SettingsPropertyEditor(user_id, session_id, 3)
    SettingsPropertyEditor(user_id, session_id, 4)
    LocalPropertyEditor(user_id, session_id, 1)
    GraphicsWindowCollection(user_id, session_id, 1)
    MonitorWindow(user_id, session_id)

    return dbc.Container(
        children=[
            html.Data(id="session-id", value="session-0"),
            dbc.Col(
                [
                    dbc.Tabs(
                        [
                            dbc.Tab(
                                label="Setup",
                                tab_id="setup",
                            ),
                            dbc.Tab(label="Post", tab_id="post"),
                        ],
                        id="demo-app-tabs",
                        active_tab="setup",
                    ),
                    html.Div(
                        id="demo-app-tab-content",
                    ),
                ],
            ),
        ],
    )


@app.callback(
    Output("post-object-container", "children"),
    Input("post-object-type", "value"),
    State("connection-id", "data"),
    State("session-id", "value"),
)
def render_widget(post_object_type, user_id, session_id):
    return LocalPropertyEditor(user_id, session_id, 1)(f"local:{post_object_type}:0")


@app.callback(
    Output("demo-app-tab-content", "children"),
    Input("demo-app-tabs", "active_tab"),
    Input("connection-id", "data"),
    Input("session-id", "value"),
)
def render_tab_content(active_tab, user_id, session_id):

    if active_tab == "setup":
        return get_setup_objects(user_id, session_id)
    if active_tab == "post":
        return get_post_objects(user_id, session_id)
