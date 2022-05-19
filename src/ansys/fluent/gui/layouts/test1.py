from app_defn import app
import dash
from dash import ALL, Input, Output, State, dcc, html
import dash_bootstrap_components as dbc
from local_property_editor import LocalPropertyEditor
from post_windows import GraphicsWindowCollection, MonitorWindow
from sessions_manager import SessionsManager
from settings_property_editor import SettingsPropertyEditor


def get_post_objects(user_id, session_id):
    return [
        dbc.Row(
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
                dbc.Col(
                    [
                        GraphicsWindowCollection(user_id, session_id, 1)(
                            init_data={0: ("Mesh", "outline")}
                        )
                    ]
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [LocalPropertyEditor(user_id, session_id, 2)(f"local:Contour:1")],
                    width="auto",
                    style={"width": "350px"},
                ),
                dbc.Col([GraphicsWindowCollection(user_id, session_id, 2)()]),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [LocalPropertyEditor(user_id, "session-1", 2)(f"local:Contour:1")],
                    width="auto",
                    style={"width": "350px"},
                ),
                dbc.Col([GraphicsWindowCollection(user_id, "session-1", 2)()]),
            ]
        ),
    ]


def get_setup_objects(user_id, session_id):
    return [
        dbc.Row(
            [
                dbc.Col(
                    [
                        SettingsPropertyEditor(user_id, session_id, 1)(
                            "remote:setup/models/viscous:"
                        ),
                        SettingsPropertyEditor(user_id, session_id, 2)(
                            "remote:solution/initialization:",
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
                dbc.Col(
                    [
                        MonitorWindow(user_id, session_id, 1)(),
                        MonitorWindow(user_id, session_id, 2)(),
                    ]
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        SettingsPropertyEditor(user_id, "session-1", 1)(
                            "remote:setup/models/viscous:"
                        ),
                        SettingsPropertyEditor(user_id, "session-1", 2)(
                            "remote:solution/initialization:",
                            ["standard-initialize"],
                        ),
                        SettingsPropertyEditor(user_id, "session-1", 3)(
                            "remote:solution/run_calculation:",
                            ["iterate"],
                        ),
                    ],
                    width="auto",
                    style={"width": "350px"},
                ),
                dbc.Col(
                    [
                        MonitorWindow(user_id, "session-1", 1)(),
                        MonitorWindow(user_id, "session-1", 2)(),
                    ]
                ),
            ]
        ),
    ]


def app_layout():
    user_id = "Ansys User"
    session_id = "session-0"
    sessions_manager = SessionsManager(user_id, session_id)
    sessions_manager.add_session("56386", None)

    # session_id = "session-1"
    sessions_manager = SessionsManager(user_id, "session-1")
    sessions_manager.add_session("59801", None)

    SettingsPropertyEditor(user_id, session_id, 1)
    SettingsPropertyEditor(user_id, session_id, 2)
    SettingsPropertyEditor(user_id, session_id, 3)
    SettingsPropertyEditor(user_id, session_id, 4)
    LocalPropertyEditor(user_id, session_id, 1)
    LocalPropertyEditor(user_id, session_id, 2)
    LocalPropertyEditor(user_id, session_id, 3)
    GraphicsWindowCollection(user_id, session_id, 1)
    GraphicsWindowCollection(user_id, session_id, 2)
    GraphicsWindowCollection(user_id, session_id, 3)
    MonitorWindow(user_id, session_id, 1)
    MonitorWindow(user_id, session_id, 2)

    LocalPropertyEditor(user_id, "session-1", 2)
    GraphicsWindowCollection(user_id, "session-1", 2)
    SettingsPropertyEditor(user_id, "session-1", 1)
    SettingsPropertyEditor(user_id, "session-1", 2)
    SettingsPropertyEditor(user_id, "session-1", 3)
    MonitorWindow(user_id, "session-1", 1)
    MonitorWindow(user_id, "session-1", 2)

    return dbc.Container(
        children=[
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
    State("user-id", "data"),
    State("session-id", "value"),
)
def render_widget(post_object_type, user_id, session_id):
    return LocalPropertyEditor(user_id, session_id, 1)(f"local:{post_object_type}:0")


@app.callback(
    Output("demo-app-tab-content", "children"),
    Input("demo-app-tabs", "active_tab"),
    Input("user-id", "data"),
    Input("session-id", "value"),
)
def render_tab_content(active_tab, user_id, session_id):

    if active_tab == "setup":
        return get_setup_objects(user_id, session_id)
    if active_tab == "post":
        return get_post_objects(user_id, session_id)
