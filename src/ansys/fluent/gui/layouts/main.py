"""Module providing main layout for PyFluent GUI."""

from app_defn import DEFAULT_USER_ID, MAX_SESSION_COUNT, app
from components import (
    LOCAL_ID,
    SETTINGS_ID,
    GraphicsWindow,
    LocalPropertyEditor,
    MonitorWindow,
    Outline,
    PlotWindow,
    ProgressBar,
    SessionsHandle,
    SettingsPropertyEditor,
)
import dash
from dash import ALL, Input, Output, State, dcc, html
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.io as pio

user_name_to_session_map = {}
pio.templates.default = "plotly_white"
APP_HEIGHT = 1050  # 900 1200 in px


def app_layout():
    user_id = DEFAULT_USER_ID
    session_id = None
    sessions = user_name_to_session_map.get(user_id)
    if sessions:
        session_id = next(iter(sessions))
    # Instantiate all required components
    for session in range(MAX_SESSION_COUNT):
        SettingsPropertyEditor(user_id, f"session-{session}", 1)
        LocalPropertyEditor(user_id, f"session-{session}", 1)
        GraphicsWindow(user_id, f"session-{session}", 1)
        MonitorWindow(user_id, f"session-{session}", 1)
        PlotWindow(user_id, f"session-{session}", 1)
        ProgressBar(user_id, f"session-{session}", 1)
        Outline(user_id, f"session-{session}", 1)

    # Main container
    return dbc.Container(
        fluid=True,
        children=[
            dcc.Store(data="AnsysUser", id="user-id"),
            # App header
            dbc.CardHeader(
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                [
                                    html.Img(
                                        src="/assets/images/pyansys.png",
                                        style={"height": "35px"},
                                    ),
                                    html.P(
                                        html.B("PyFluent Web Client"),
                                        style={
                                            "font-size": "24px",
                                            "padding": "0px 0px 0px 20px",
                                        },
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "flex-direction": "row",
                                },
                            ),
                            style={"border-bottom": "3px solid gray"},
                        ),
                        dbc.Col(
                            html.Div(
                                [
                                    dcc.Loading(
                                        id="loading-sessions-id",
                                        type="default",
                                        parent_className="loading-visible",
                                        children=dbc.Select(
                                            id="session-id",
                                            options=[
                                                {"label": session, "value": session}
                                                for session in user_name_to_session_map.get(
                                                    user_id, []
                                                )
                                            ],
                                            size="sm",
                                            placeholder="Select Session",
                                            value=session_id,
                                            style={"width": "200px"},
                                        ),
                                    ),
                                    dbc.Input(
                                        placeholder="Session token to connect",
                                        id="session-token",
                                        style={
                                            "width": "200px",
                                            "margin": "0px 5px 0px 5px",
                                        },
                                        size="sm",
                                    ),
                                    dbc.Button(
                                        "Connect to Session",
                                        id="connect-session",
                                        n_clicks=0,
                                        style={"width": "200px"},
                                        size="sm",
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "flex-direction": "row",
                                },
                            ),
                            width="auto",
                            align="end",
                        ),
                    ],
                    style={
                        "padding": "0px 0px 5px",
                        "border-bottom": "14px solid black",
                    },
                ),
            ),
            # App main body
            dbc.Row(
                children=[
                    # App side Bar
                    dbc.Col(
                        html.Div(
                            [
                                dbc.CardHeader(
                                    [
                                        html.B(
                                            [
                                                "Welcome ",
                                                dbc.Badge(
                                                    html.I(
                                                        f"{user_id.capitalize()}",
                                                        style={"font-size": "16px"},
                                                    ),
                                                    color="secondary",
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                                dcc.Loading(
                                    html.Div(
                                        id="outline-container",
                                        children=Outline(user_id, session_id, 1)()
                                        if session_id
                                        else [],
                                    ),
                                    id="loading-outline",
                                    type="default",
                                    parent_className="loading-visible",
                                ),
                            ],
                            style={
                                "width": "18rem",
                                "background-color": "#f8f9fa",
                                "height": APP_HEIGHT,
                                "overflow-y": "auto",
                            },
                        ),
                        align="start",
                        width="auto",
                    ),
                    # App property editor
                    dbc.Col(
                        dcc.Loading(
                            className="dcc_loader",
                            id="loading-property-editor-container",
                            type="default",
                            parent_className="loading-visible",
                            children=html.Div(
                                id="property-editor-container",
                                style={
                                    "width": "20rem",
                                    "background-color": "#f8f9fa",
                                    "overflow-y": "auto",
                                    "height": APP_HEIGHT,
                                },
                            ),
                        ),
                        width="auto",
                    ),
                    # App post windows
                    dbc.Col(
                        dcc.Loading(
                            className="dcc_loader",
                            id="loading-tab-contents",
                            type="default",
                            parent_className="loading-visible",
                            children=html.Div(
                                children=[
                                    dbc.Card(
                                        [
                                            dbc.CardHeader(
                                                dbc.Tabs(
                                                    [
                                                        dbc.Tab(
                                                            label="Graphics",
                                                            tab_id="graphics",
                                                        ),
                                                        dbc.Tab(
                                                            label="Plots",
                                                            tab_id="plots",
                                                        ),
                                                        dbc.Tab(
                                                            label="Monitors",
                                                            tab_id="monitors",
                                                        ),
                                                    ],
                                                    id="tabs",
                                                    active_tab="graphics",
                                                )
                                            ),
                                            html.Div(
                                                id="tab-content",
                                            ),
                                        ],
                                        style={"height": APP_HEIGHT},
                                    ),
                                ],
                            ),
                        )
                    ),
                ],
                style={"padding": "4px 0px 4px 0px"},
            ),
            # App progress bar
            html.Div(
                id="progress-bar-container",
                children=ProgressBar(user_id, session_id, 1)() if session_id else [],
            ),
        ],
    )


@app.callback(
    Output("session-id", "options"),
    Output("session-id", "value"),
    Input("connect-session", "n_clicks"),
    State("user-id", "data"),
    State("session-token", "value"),
    State("session-id", "options"),
)
def create_session(n_clicks, user_id, session_token, current_sessions):
    """This callback takes `user id`, `session token` and `current sessions` as
    inputs and create new session when App`s ``connect-session`` is
    executed."""
    ctx = dash.callback_context
    triggered_value = ctx.triggered[0]["value"]
    triggered_from = ctx.triggered[0]["prop_id"].split(".")[0]
    if n_clicks == 0 or triggered_value is None:
        raise PreventUpdate

    user_sessions = user_name_to_session_map.get(user_id)
    if not user_sessions:
        user_sessions = user_name_to_session_map[user_id] = []

    session_id = f"session-{len(current_sessions)}"
    user_sessions.append(session_id)
    session_handle = SessionsHandle(user_id, session_id)
    session_handle.connect(session_token)
    sessions = []
    if current_sessions is not None:
        sessions = current_sessions
    sessions.append({"label": session_id, "value": session_id})
    return sessions, session_id


@app.callback(
    Output("property-editor-container", "children"),
    Input({"type": "outline", "index": ALL}, "selected"),
    Input("session-id", "value"),
    State("user-id", "data"),
    prevent_initial_call=True,
)
def show_property_editor(tree_selection, session_id, user_id):
    """This callback takes `tree selection`, `session id` and `user id` as
    inputs and renders ``LocalPropertyEditor`` or ``SettingsPropertyEditor``
    component inside App's ``property-editor-container``."""
    ctx = dash.callback_context
    triggered_from = ctx.triggered[0]["prop_id"].split(".")[0]
    triggered_value = ctx.triggered[0]["value"]
    if session_id is None or triggered_from == "session-id":
        return []
    triggered_data = eval(triggered_from)
    outline_user_id, outline_session_id, outline_index = triggered_data["index"].split(
        ":"
    )
    if user_id != outline_user_id or session_id != outline_session_id:
        raise PreventUpdate

    if triggered_value and isinstance(triggered_value, list):
        selected_node = triggered_value[0]
        if selected_node.startswith(SETTINGS_ID) or selected_node.startswith(LOCAL_ID):
            location_id, object_path, object_index = selected_node.split(":")
            editor = (
                LocalPropertyEditor(user_id, session_id, 1)
                if location_id == LOCAL_ID
                else SettingsPropertyEditor(user_id, session_id, 1)
            )
            return editor(selected_node)
    return []


@app.callback(
    Output("progress-bar-container", "children"),
    Input("session-id", "value"),
    State("user-id", "data"),
    prevent_initial_call=True,
)
def show_progress_bar(session_id, user_id):
    """This callback takes `session id` and `user id` as inputs and renders
    ``ProgressBar`` component inside App's ``progress-bar-container``."""
    if session_id is None:
        return []
    return ProgressBar(user_id, session_id, 1)()


@app.callback(
    Output("outline-container", "children"),
    Input("session-id", "value"),
    State("user-id", "data"),
    prevent_initial_call=True,
)
def show_outline(session_id, user_id):
    """This callback takes `session id` and `user id` as inputs and renders
    ``Outline`` component inside App's ``outline-container``."""
    if session_id is None:
        return []
    return Outline(user_id, session_id, 1)()


@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab"),
    Input("session-id", "value"),
    State("user-id", "data"),
)
def show_tabs(active_tab, session_id, user_id):
    """This callback takes the `active tab`, `session id` and `user id` as
    inputs and renders post components i.e. ``GraphicsWindow``, ``PlotWindow``,
    ``MonitorWindow`` inside App`s ``tab-content`` depending on what the value
    of `active_tab` is."""
    if session_id is None:
        return html.Pre(
            """
              Welcome to ANSYS PyFluent Web Client 22.2.0

              Use session token to get connected with runnng session.
              Please visit https://github.com/pyansys/pyfluent for more information.
              """,
            style={"font": "14px 'Segoe UI'"},
        )

    if active_tab == "graphics":
        return GraphicsWindow(user_id, session_id, 1)(
            init_data=[("Mesh", "outline")], component_height=APP_HEIGHT
        )

    elif active_tab == "plots":
        return PlotWindow(user_id, session_id, 1)(component_height=APP_HEIGHT)

    elif active_tab == "monitors":
        return MonitorWindow(user_id, session_id, 1)(component_height=APP_HEIGHT)
