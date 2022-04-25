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
import numpy as np
import plotly.graph_objs as go
from dash import Input, Output, State, dcc, html, ALL
from dash.exceptions import PreventUpdate
from tree_view import TreeView

from ansys.fluent.core.utils.dash.sessions_manager import SessionsManager

from local_property_editor import PlotWindow, GraphicsWindow
from PropertyEditor import PropertyEditor

app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)
import dash_treeview_antd

app.config.suppress_callback_exceptions = True

SIDEBAR_STYLE = {
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",   
    "background-color": "#f8f9fa",
    "height": "53rem",
    "overflow-y": "scroll",
}



sidebar = html.Div(
    [
        html.H6("Outline"),
        html.Div(
            id="tree-view-container",  
        ),
    ],
    style=SIDEBAR_STYLE,
)


_max_session_count = 6


def serve_layout():
    connection_id = str(uuid.uuid4())
    for session_id in range(_max_session_count):
        SessionsManager(app, connection_id, f"session-{session_id}")
    PropertyEditor(app, SessionsManager)
    
    return dbc.Container(
        fluid=True,
        children=[
            dcc.Store(data=connection_id, id="connection-id"),
            html.Data(id="refresh-property-editor"),
            html.Data(id="window-id", value="0"),
            html.Data(id="object-id"),
            html.Data(id="command-output"),
            dbc.Row(
                [
                    dbc.Col(
                      html.Div(
                      [
                        html.Img(src='/assets/ansys.jpg', style={'width':'35px', 'height':'35px', "padding":"5px 2px 2px 2px"}),
                        html.H2("Ansys PyFluent Web App"), 
                        ],
                      style = {"display": "flex", "flex-direction": "row"}  
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
                            type = "number",                              
                            style={"width": "200px"},
                        ),
                        width="auto",
                        align="end",
                    ),                    
                    dbc.Col(
                        dcc.Dropdown(
                            id="session-id",
                            options=[],
                            value=None,
                            style={"width": "200px"},
                        ),
                        width="auto",
                        align="end",
                    ),
                ],
                        style={                                               
                            "background-color": "#f8f9fa",
                            "background-image": 'url("/resources//ansys-logo.png")',
                        }                 
            ),
            html.Hr(),
            dbc.Row(
                children=[
                    dbc.Col(sidebar, align="start", width="auto"),
                    dbc.Col(
                        [
                            html.Div(id="property-editor-title"),
                            html.Div(
                                html.Div(
                                    id="property-editor",
                                    children=[],
                                ),
                                className="mb-3",
                            ),
                        ],
                        width="auto",
                        style={
                            "padding": "1px 1px 1px 1px",
                            "width": "20rem",
                            "background-color": "#f8f9fa",
                            "overflow-y": "scroll",
                            "height": "53rem",
                        },
                    ),
                    dbc.Col(
                        [
                            dbc.Tabs(
                                [
                                    dbc.Tab(
                                        label="Graphics", tab_id="graphics"
                                    ),
                                    dbc.Tab(label="Plots", tab_id="plots"),
                                ],
                                id="tabs",
                                active_tab="graphics",
                            ),
                            html.Div(id="tab-content", className="p-4"),
                        ],
                    ),
                ]
            ),
        ],
    )


app.layout = serve_layout




@app.callback(
    Output("session-id", "options"),
    Output("session-id", "value"),
    Input("connect-session", "n_clicks"),
    Input("session-token", "value"),
    Input("connection-id", "data"),
    State("session-id", "options"),
)
def create_session(n_clicks, session_token, connection_id, options):
    if n_clicks == 0:
        raise PreventUpdate
    session_id = f"session-{len(options)}"
    sessions_manager = SessionsManager(app, connection_id, session_id)
    sessions_manager.add_session(session_token)
    sessions = []
    if options is not None:
        sessions = options
    sessions.append(session_id)
    return [sessions, session_id]

@app.callback(
    Output("tree-view-container", "children"),
    #Output("tree-view", "expanded"),
    Input("connection-id", "data"),  #
    Input("session-id", "value"),    
)
def session_changed(
    connection_id, session_id
):
    if session_id is None or connection_id is None:
        raise PreventUpdate    
    tree_nodes, keys = TreeView(app, connection_id, session_id, SessionsManager).get_tree_nodes()   
    return dash_treeview_antd.TreeView(
        id="tree-view",
        multiple=False,
        expanded=keys,
        data=tree_nodes,
    )   
   
    

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
        return dbc.Row(
            [
                dbc.Col(
                    children=list(
                        GraphicsWindow(
                            app, connection_id, session_id, 0, SessionsManager
                        )
                        .get_widgets()
                        .values()
                    )
                )
            ],
            style={"height": "49rem"},
        )

    elif active_tab == "plots":
        return dbc.Col(
            children=list(
                PlotWindow(app, connection_id, session_id, 0, SessionsManager)
                .get_widgets()
                .values()
            )
        )


if __name__ == "__main__":
    app.run_server(debug=True, port=8888)
