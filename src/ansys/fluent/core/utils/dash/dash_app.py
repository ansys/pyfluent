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
pio.templates.default = "plotly_white"

from ansys.fluent.core.utils.dash.sessions_manager import SessionsManager

from local_property_editor import (
    MonitorWindow,
    PlotWindowCollection,
    GraphicsWindowCollection,
)
from PropertyEditor import PropertyEditor


# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = {
    'user1': 'abc',
    'user2': 'abc',
    'user3': 'abc',
    'user4': 'abc'
}
user_name_to_session_map={}

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

import dash_treeview_antd

app.config.suppress_callback_exceptions = True

app.config["suppress_callback_exceptions"] = True

SIDEBAR_STYLE = {
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "background-color": "#f8f9fa",
    "height": "53rem",
    "overflow-y": "scroll",
}

def get_side_bar(app, connection_id):

    session_id = user_name_to_session_map.get(connection_id,[None])[0]
    tree_view = []
    if session_id:
        tree_nodes, keys = TreeView(
            app, connection_id, session_id, SessionsManager
        ).get_tree_nodes()
        tree_view = dash_treeview_antd.TreeView(
            id="tree-view",
            multiple=False,
            expanded=keys,
            data=tree_nodes,
        )


    return  html.Div(
      [
          html.H5(
          [
          dbc.Badge(f"Welcome {connection_id}", color="primary", className="me-1"),
          ]
          ),
          html.H6("Outline"),
          html.Div(
              id="tree-view-container",
              children = tree_view
          ),
      ],
      style=SIDEBAR_STYLE,
    )


_max_session_count = 1


def serve_layout():
    #connection_id = str(uuid.uuid4())
    connection_id = request.authorization['username'] 
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
            html.Data(id="object-id"),
            html.Data(id="graphics-button-clicked"),
            html.Data(id="plot-button-clicked"),
            html.Data(id="save-button-clicked"),
            html.Data(id="delete-button-clicked"),
            html.Data(id="command-output"),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                html.Img(
                                    src="/assets/ansys.jpg",
                                    style={
                                        "width": "35px",
                                        "height": "35px",
                                        "padding": "5px 2px 2px 2px",
                                    },
                                ),
                                html.H2("Ansys PyFluent Web App"),
                            ],
                            style={"display": "flex", "flex-direction": "row"},
                        )
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
                        dbc.Input(
                            placeholder="Session token to connect",
                            id="session-token",
                            type="number",
                            style={"width": "200px"},
                        ),
                        width="auto",
                        align="end",
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            id="session-id",
                            options=user_name_to_session_map.get(connection_id,[]),
                            value=user_name_to_session_map.get(connection_id,[None])[0],
                            style={"width": "200px"},
                        ),
                        width="auto",
                        align="end",
                    ),
                ],
                style={
                    "background-color": "#f8f9fa",
                    "background-image": 'url("/resources//ansys-logo.png")',
                },
            ),
            html.Hr(),
            dbc.Row(
                children=[
                    dbc.Col(get_side_bar(app, connection_id), align="start", width="auto"),
                    dbc.Col(
                        id="property-editor",
                        width="auto",
                        style={
                            "width": "20rem",
                            "background-color": "#f8f9fa",
                            "overflow-y": "scroll",
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
                                    dbc.CardBody(
                                        id="tab-content",
                                        className="p-4",
                                    ),
                                ],
                                style={"height": "53rem"},
                            ),
                        ]
                    ),
                ]
            ),
        ],
    )


app.layout = serve_layout

print("serve_layout done")


@app.callback(
    Output("session-id", "options"),
    Output("session-id", "value"),
    Input("connect-session", "n_clicks"),
    Input("session-token", "value"),
    Input("connection-id", "data"),
    State("session-id", "options"),
)
def create_session(n_clicks, session_token, connection_id, options):

    ctx = dash.callback_context
    triggered_value = ctx.triggered[0]["value"]
    triggered_from = ctx.triggered[0]["prop_id"].split(".")[0]
    print('create_session', triggered_from, triggered_value)
    if n_clicks == 0 or triggered_value is None:
        raise PreventUpdate    
    
    user_sessions= user_name_to_session_map.get(connection_id)
    if not user_sessions:
        user_sessions =user_name_to_session_map[connection_id] = [] 
        
    session_id = f"session-{len(options)}"
    user_sessions.append(session_id)
    sessions_manager = SessionsManager(app, connection_id, session_id)
    sessions_manager.add_session(session_token)
    sessions = []
    if options is not None:
        sessions = options
    sessions.append(session_id)
    return [sessions, session_id]


@app.callback(
    Output("tree-view-container", "children"),
    Input("connection-id", "data"),  #
    Input("session-id", "value"),
    Input("save-button-clicked", "value"),
    Input("delete-button-clicked", "value"),
    State("object-id", "value"),
    #prevent_initial_call=True,
)
def update_tree(connection_id, session_id, save_n_clicks, delete_n_clicks, object_id):
    ctx = dash.callback_context
    triggered_value = ctx.triggered[0]["value"]
    triggered_from = ctx.triggered[0]["prop_id"].split(".")[0]
    print('update_tree', triggered_from, triggered_value)
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
    return dash_treeview_antd.TreeView(
        id="tree-view",
        multiple=False,
        expanded=keys,
        data=tree_nodes,
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
        raise PreventUpdate

    if active_tab == "graphics":
        return GraphicsWindowCollection(
            app, connection_id, session_id, SessionsManager
        )()
        return dbc.Row(
            GraphicsWindowCollection(app, connection_id, session_id, SessionsManager)(),
            style={"height": "auto"},
        )

    elif active_tab == "plots":
        return PlotWindowCollection(app, connection_id, session_id, SessionsManager)()
        return dbc.Row(
            PlotWindowCollection(app, connection_id, session_id, SessionsManager)(),
            style={"height": "auto"},
        )
    elif active_tab == "monitors":
        return MonitorWindow(app, connection_id, session_id, SessionsManager)()
        return dbc.Row(
            MonitorWindow(app, connection_id, session_id, SessionsManager)(),
            style={"height": "auto"},
        )


if __name__ == "__main__":
    app.run_server(debug=True, port=8800)
