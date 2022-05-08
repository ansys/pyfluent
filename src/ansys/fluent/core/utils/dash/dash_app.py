"""
A simple app demonstrating how to dynamically render tab content containing
dcc.Graph components to ensure graphs get sized correctly. We also show how
dcc.Store can be used to cache the results of an expensive graph generation
process so that switching tabs is fast.
"""
import time
import uuid
import dash
import dash_bootstrap_components as dbc
import dash_auth
import numpy as np
import plotly.graph_objs as go
from dash import Input, Output, State, dcc, html, ALL
from dash.exceptions import PreventUpdate
from tree_view import TreeView
from local_property_editor import LocalPropertyEditor
import plotly.io as pio
from flask import request
from dash.long_callback import DiskcacheLongCallbackManager

pio.templates.default = "plotly_white"
from dash_component import DashComponent
from local_property_editor import PostWindowCollection
from ansys.fluent.core.utils.dash.sessions_manager import SessionsManager

from local_property_editor import (
    MonitorWindow,
    PlotWindowCollection,
    GraphicsWindowCollection,
)
from PropertyEditor import PropertyEditor


VALID_USERNAME_PASSWORD_PAIRS = {
    "user1": "abc",
    "user2": "abc",
    "user3": "abc",
    "user4": "abc",
}
user_name_to_session_map = {}

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

import diskcache

cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheLongCallbackManager(cache)

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
    suppress_callback_exceptions=True,
    long_callback_manager=long_callback_manager,
)

auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)
# from dash_component import TreeView as dash_treeview_antd
# from  dash_treeview_antd import TreeView as dash_treeview_antd
from dash_component import RCTree as dash_treeview_antd

app.config.suppress_callback_exceptions = True

app.config["suppress_callback_exceptions"] = True

SIDEBAR_STYLE = {
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "background-color": "#f8f9fa",
    "height": "53rem",
    "overflow-y": "auto",
}


def get_side_bar(app, connection_id):

    session_id, uuid_id = user_name_to_session_map.get(connection_id, [[None, None]])[0]
    tree_view = []
    if session_id:
        tree_nodes, keys = TreeView(
            app, connection_id, session_id, SessionsManager
        ).get_tree_nodes()
        tree_view = dash_treeview_antd(
            id="tree-view",
            # multiple=False,
            # expanded=keys,
            data=tree_nodes,
        )

    return html.Div(
        [
            dbc.CardHeader(
                [
                    html.B(
                        [
                            "Welcome ",
                            dbc.Badge(
                                html.I(f"{connection_id}", style={"font-size": "18px"}),
                                color="secondary",
                            ),
                        ]
                    ),
                ]
            ),
            html.Div(id="tree-view-container", children=tree_view),
        ],
        style=SIDEBAR_STYLE,
    )


_max_session_count = 6


def serve_layout():
    uuid_id = str(uuid.uuid4())
    connection_id = uuid_id
    connection_id = request.authorization["username"]
    for session_id in range(_max_session_count):
        SessionsManager(app, connection_id, f"session-{session_id}")
    PropertyEditor(app, SessionsManager)
    print("connection_id********************", connection_id)
    return dbc.Container(
        fluid=True,
        children=[
            dcc.Store(data=connection_id, id="connection-id"),
            dcc.Interval(
                id="interval-component",
                interval=1 * 1000,  # in milliseconds
                n_intervals=0,
            ),
            html.Data(id="refresh-property-editor"),
            html.Data(id="window-id", value="0"),
            html.Data(id="need-to-data-fetch", value="no"),
            html.Data(id="object-id"),
            html.Data(id="graphics-button-clicked"),
            html.Data(id="plot-button-clicked"),
            html.Data(id="save-button-clicked"),
            html.Data(id="delete-button-clicked"),
            html.Data(id="command-output"),
            html.Data(
                id="uuid-id",
                value=user_name_to_session_map.get(connection_id, [[None, ""]])[0][1],
            ),
            dbc.CardHeader(
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                [
                                    html.Img(
                                        src="/assets/pyansys.png",
                                        style={"height": "35px"},
                                    ),
                                    html.P(
                                        html.B("PyFluent Web Client"),
                                        style={
                                            "font": "24px 'Segoe UI'",
                                            "padding": "0px 0px 0px 20px",
                                            # "text-shadow": "0.5px 0.5px"
                                        },
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "flex-direction": "row",  # "border-bottom": "5px solid darkgray"
                                },
                            ),
                            style={"border-bottom": "3px solid gray"},
                        ),
                        dbc.Col(
                            dcc.Dropdown(
                                id="session-id",
                                # options=map(lambda x: x[0],user_name_to_session_map.get(connection_id, [])),
                                options=list(
                                    map(
                                        lambda x: x[0],
                                        user_name_to_session_map.get(connection_id),
                                    )
                                )
                                if user_name_to_session_map.get(connection_id)
                                else [],
                                value=user_name_to_session_map.get(
                                    connection_id, [[None, None]]
                                )[0][0],
                                style={"width": "200px"},
                            ),
                            width="auto",
                            align="end",
                        ),
                        dbc.Col(
                            dbc.Input(
                                placeholder="Session token to connect",
                                id="session-token",
                                style={"width": "200px"},
                            ),
                            width="auto",
                            align="end",
                        ),
                        dbc.Col(
                            dbc.Button(
                                "Connect to Session",
                                id="connect-session",
                                n_clicks=0,
                                style={"width": "200px"},
                            ),
                            width="auto",
                            align="end",
                        ),
                        dbc.Col(
                            dcc.Clipboard(
                                target_id="uuid-id",
                                title="Share",
                                style={
                                    "display": "inline-block",
                                    "fontSize": 20,
                                    "verticalAlign": "top",
                                },
                            ),
                            width="auto",
                            align="end",
                        ),
                    ],
                    style={
                        "font": "14px 'Segoe UI'",
                        "padding": "0px 0px 5px",
                        "border-bottom": "14px solid black",
                        "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 10px 0 rgba(0, 0, 0, 0.19)",
                    },
                ),
                style={
                    #  "background-color": "#f8f9fa",
                    #  "background-image": 'url("/assets/background.png")',
                    #  "background-size": "contain",
                    "font": "14px 'Segoe UI'"
                },
            ),
            dbc.Row(
                children=[
                    dbc.Col(
                        get_side_bar(app, connection_id), align="start", width="auto"
                    ),
                    dbc.Col(
                        id="property-editor",
                        width="auto",
                        style={
                            "width": "20rem",
                            "background-color": "#f8f9fa",
                            "overflow-y": "auto",
                            "height": "53rem",
                        },
                    ),
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        dbc.Tabs(
                                            [
                                                dbc.Tab(
                                                    label="Graphics",
                                                    tab_id="graphics",
                                                ),
                                                dbc.Tab(label="Plots", tab_id="plots"),
                                                dbc.Tab(
                                                    label="Monitors", tab_id="monitors"
                                                ),
                                            ],
                                            id="tabs",
                                            active_tab="graphics",
                                        )
                                    ),
                                    html.Div(
                                        id="tab-content",
                                        # className="p-4",
                                    ),
                                ],
                                style={"height": "53rem"},
                            ),
                        ]
                    ),
                ],
                style={"font": "14px 'Segoe UI'", "padding": "4px"},
            ),
            html.Div(
                [
                    html.Div(id="progress-messgae"),
                    html.Div(
                        dbc.Progress(
                            id="progress-bar",
                            value=0,
                            label="",
                            style={"height": "25px"},
                        ),
                        style={"display": "block", "width": "100%"},
                    ),
                ],
                id="progress-container",
                style={"font": "14px 'Segoe UI'"},
            ),
        ],
    )


app.layout = serve_layout

print("serve_layout done")


@app.callback(
    Output("need-to-data-fetch", "value"),
    Input("interval-component", "n_intervals"),
    Input("connection-id", "data"),
    State("session-id", "value"),
    State("need-to-data-fetch", "value"),
)
def watcher(n_intervals, connection_id, session_id, need_to_fetch):
    event_info = SessionsManager(app, connection_id, session_id).get_event_info(
        "CalculationsStartedEvent"
    )
    if event_info:
        if PostWindowCollection._is_executing == False:
            PostWindowCollection._is_executing = True
            return "yes"
        else:
            raise PreventUpdate
    else:
        if need_to_fetch == "yes":
            return "no"
        else:
            raise PreventUpdate


@app.callback(
    Output("progress-container", "style"),
    Output("progress-bar", "value"),
    Output("progress-bar", "label"),
    Output("progress-messgae", "children"),
    Input("interval-component", "n_intervals"),
    Input("connection-id", "data"),
    State("session-id", "value"),
    prevent_initial_call=True,
)
def on_progress_update(n_intervals, connection_id, session_id):
    event_info = SessionsManager(app, connection_id, session_id).get_event_info(
        "ProgressEvent"
    )
    if event_info is None:
        return [{"display": "none"}, dash.no_update, dash.no_update, dash.no_update]

    return [
        {"display": "flex", "flex-direction": "row"},
        event_info.percentComplete,
        str(event_info.percentComplete) + "%",
        event_info.message,
    ]


@app.callback(
    Output("session-id", "options"),
    Output("session-id", "value"),
    Input("connect-session", "n_clicks"),
    Input("connection-id", "data"),
    State("session-token", "value"),
    State("session-id", "options"),
)
def create_session(n_clicks, connection_id, session_token, options):

    ctx = dash.callback_context
    triggered_value = ctx.triggered[0]["value"]
    triggered_from = ctx.triggered[0]["prop_id"].split(".")[0]
    print("create_session", triggered_from, triggered_value)
    if n_clicks == 0 or triggered_value is None:
        raise PreventUpdate

    user_sessions = user_name_to_session_map.get(connection_id)
    if not user_sessions:
        user_sessions = user_name_to_session_map[connection_id] = []

    session_id = f"session-{len(options)}"
    user_sessions.append((session_id, connection_id + ":" + uuid.uuid4().hex))
    sessions_manager = SessionsManager(app, connection_id, session_id)
    sessions_manager.add_session(session_token, user_name_to_session_map)
    sessions = []
    if options is not None:
        sessions = options
    sessions.append(session_id)
    return [sessions, session_id]


@app.callback(
    Output("object-id", "value"),
    Input("connection-id", "data"),  #
    Input("tree-view", "selected"),
    Input("session-id", "value"),
)
def update_object(connection_id, object_id, session_id):
    print("update_object", connection_id, session_id, object_id)

    if object_id is None or len(object_id) == 0 or session_id is None:
        raise PreventUpdate
    object_id = object_id[0]
    ctx = dash.callback_context
    triggered_from = ctx.triggered[0]["prop_id"].split(".")[0]
    if triggered_from == "tree-view":
        if "local" in object_id or "remote" in object_id:
            return object_id
        else:
            raise PreventUpdate
    else:
        PostWindowCollection._is_executing = False
        return None


@app.callback(
    Output("tree-view-container", "children"),
    Output("uuid-id", "value"),
    Input("connection-id", "data"),  #
    Input("session-id", "value"),
    Input("save-button-clicked", "value"),
    Input("delete-button-clicked", "value"),
    State("object-id", "value"),
    # prevent_initial_call=True,
)
def update_tree(connection_id, session_id, save_n_clicks, delete_n_clicks, object_id):
    ctx = dash.callback_context
    triggered_value = ctx.triggered[0]["value"]
    triggered_from = ctx.triggered[0]["prop_id"].split(".")[0]
    print("update_tree", triggered_from, triggered_value)
    if session_id is None or connection_id is None or triggered_value is None:
        raise PreventUpdate

    if triggered_from == "save-button-clicked":
        object_location, object_type, object_index = object_id.split(":")
        editor = LocalPropertyEditor(app, SessionsManager)
        new_object = editor.create_new_object(
            connection_id, session_id, object_type, object_index
        )
    elif triggered_from == "delete-button-clicked":
        object_location, object_type, object_index = object_id.split(":")
        editor = LocalPropertyEditor(app, SessionsManager)
        new_object = editor.delete_object(
            connection_id, session_id, object_type, object_index
        )
    print("update_tree", triggered_from, triggered_value)
    tree_nodes, keys = TreeView(
        app, connection_id, session_id, SessionsManager
    ).get_tree_nodes()
    filtered = filter(
        lambda x: session_id == x[0], user_name_to_session_map[connection_id]
    )
    return (
        dash_treeview_antd(
            id="tree-view",
            data=tree_nodes,
        ),
        list(filtered)[0][1],
    )


@app.callback(
    Output("save-button-clicked", "value"),
    Input("save-button", "n_clicks"),
    prevent_initial_call=True,
)
def manage_save_delete_object(save_n_clicks):
    if save_n_clicks is None or save_n_clicks == 0:
        raise PreventUpdate
    return str(save_n_clicks)


@app.callback(
    Output("delete-button-clicked", "value"),
    Input("delete-button", "n_clicks"),
    prevent_initial_call=True,
)
def manage_save_delete_object(delete_n_clicks):
    if delete_n_clicks is None or delete_n_clicks == 0:
        raise PreventUpdate
    return str(delete_n_clicks)


@app.callback(
    Output("graphics-button-clicked", "value"),
    Input("graphics-button", "n_clicks"),
)
def on_button_click(n_graphics_clicks):
    if n_graphics_clicks is None:
        raise PreventUpdate
    return str(n_graphics_clicks)


@app.callback(
    Output("plot-button-clicked", "value"),
    Input("plot-button", "n_clicks"),
)
def on_button_click(n_post_clicks):
    if n_post_clicks is None:
        raise PreventUpdate
    return str(n_post_clicks)


@app.callback(
    Output("tabs", "active_tab"),
    Input(
        {"type": "add-post-window", "index": ALL},
        "n_clicks",
    ),
    Input(
        {"type": "remove-post-window", "index": ALL},
        "n_clicks",
    ),
    Input("connection-id", "data"),
    State("session-id", "value"),
    prevent_initial_call=True,
)
def add_remove_post_window(add_clicks, remove_clicks, connection_id, session_id):

    print("add_remove_window", add_clicks, remove_clicks, connection_id, session_id)
    if not add_clicks or not remove_clicks:
        raise PreventUpdate
    ctx = dash.callback_context
    print("add_remove_window", ctx.triggered)
    input_value = ctx.triggered[0]["value"]
    if input_value is None:
        raise PreventUpdate

    input_data = eval(ctx.triggered[0]["prop_id"].split(".")[0])

    input_index = input_data["index"]
    input_type = input_data["type"]
    window = (
        PlotWindowCollection(app, connection_id, session_id, SessionsManager)
        if input_index == "plot"
        else GraphicsWindowCollection(app, connection_id, session_id, SessionsManager)
    )
    opr = "add" if input_type.startswith("add") else "remove"
    print("add_remove_window", opr, input_index, input_value)
    if opr == "add":
        if input_value == 0:
            raise PreventUpdate
        id = 0
        while True:
            if id not in window._windows:
                break
            id = id + 1
        window._active_window = id
        window._windows.append(id)
        print("add_remove_window:add", window._active_window, window._windows)
    elif opr == "remove":
        if input_value == 0 or len(window._windows) == 1:
            raise PreventUpdate
        if window._state.get(window._active_window):
            del window._state[window._active_window]
        index = window._windows.index(window._active_window)
        new_index = (
            window._windows[index + 1] if index == 0 else window._windows[index - 1]
        )
        window._windows.remove(window._active_window)
        window._active_window = new_index

    return "plots" if input_index == "plot" else "graphics"


@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab"),
    Input("connection-id", "data"),
    Input("session-id", "value"),
)
def render_tab_content(active_tab, connection_id, session_id):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    print("render_tab_content", active_tab, connection_id, session_id)
    if session_id is None:
        return html.Pre(
            """
              Welcome to ANSYS PyFluent Web Client 22.2.0
              
              Copyright 1987-2022 ANSYS, Inc. All Rights Reserved.
              Unauthorized use, distribution or duplication is prohibited.
              This product is subject to U.S. laws governing export and re-export.
              For full Legal Notice, see documentation.
              
              Use session token to get connected with runnng session.
              Please visit https://github.com/pyansys/pyfluent for more information.
              
              """,
            style={"font": "14px 'Segoe UI'"},
        )

    if active_tab == "graphics":
        return GraphicsWindowCollection(
            app, connection_id, session_id, SessionsManager
        )()

    elif active_tab == "plots":
        return PlotWindowCollection(app, connection_id, session_id, SessionsManager)()

    elif active_tab == "monitors":
        return MonitorWindow(app, connection_id, session_id, SessionsManager)()


if __name__ == "__main__":
    app.run_server(debug=True, port=8800)
