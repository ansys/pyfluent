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



from ansys.fluent.core.utils.dash.sessions_manager import SessionsManager
import dash_treeview_antd
from local_property_editor import PlotWindow, GraphicsWindow
from PropertyEditor import PropertyEditor
app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)
app.config.suppress_callback_exceptions = True

SIDEBAR_STYLE = {
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "height": "55rem",
    "overflow-y": "scroll",
}

sidebar = html.Div(
    [
        html.P("Outline", className="lead"),
        dbc.Col(
            dbc.Button(
                "Connect to Session",
                id="connect-session",
                size="lg",
                n_clicks=0,
                active=True,
            )
        ),
        html.Div(
            children =[],
            id =  "session-list",           
        ),
        
        html.Div(
            [
                dash_treeview_antd.TreeView(
                    id="tree-view",
                    multiple=True,
                    expanded=["0"],
                    data={
                        "title": "Parent",
                        "key": "0",
                        "children": [
                            {
                                "title": "Child",
                                "key": "0-0",
                                "children": [
                                    {
                                        "title": "Subchild1", 
                                        "key": "0-0-1"
                                    },
                                    {
                                        "title": "Subchild2", 
                                        "key": "0-0-2"
                                    },
                                    {
                                        "title": "Subchild3",
                                        "key": "0-0-3",
                                        "children": [
                                            {
                                                "title": "Subchild1",
                                                "key": "0-0-3-1",
                                            },
                                            {
                                                "title": "Subchild2",
                                                "key": "0-0-3-2",
                                            },
                                            {
                                                "title": "Subchild3",
                                                "key": "0-0-3-3",
                                            },
                                        ],
                                    },
                                ],
                            }
                        ],
                    },
                ),               
            ],
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
            html.Data(id="command-output"),
            dbc.Row(
                [
                    dbc.Col(html.H1("Ansys pyFluent post web App")),
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
                ]
            ),
            html.Hr(),
            dbc.Row(
                children=[
                    dbc.Col(sidebar, align="start", width="auto"),
            dbc.Col(
                    [
                        html.Div(
                            [
                                dbc.Label("Select Graphics"),
                                dcc.Dropdown(
                                    id="object-id",
                                    options=[
                                    "local:Mesh", "local:Surface", "local:Contour", "local:Vector",
                                    "remote:Viscous", "remote:Multiphase", "remote:Initialization", "remote:calculation"
                                    
                                    
                                    ],                                    
                                ),
                            ],
                            style={
                                "padding": "1px 1px 10px 1px",
                                "width": "20rem",
                            },
                        ),
                    
                    
                        html.Div(
                            html.Div(
                                id="property-editor",
                                children=[],
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
    [
        Output("session-list", "children"),
        Output("session-id", "options"),
    ],
    Input("connect-session", "n_clicks"),
    Input("connection-id", "data"),
    State("session-list", "children"),
    State("session-id", "options"),
)
def create_session(n_clicks, connection_id, session_list, options):
    if n_clicks == 0:
        raise PreventUpdate
    session_id = f"session-{len(session_list)}"
    sessions_manager = SessionsManager(app, connection_id, session_id)
    sessions_manager.add_session("E:\\ajain\\Demo\\pyApp\\pyvista\\server.txt")
    sessions = []
    if options is not None:
        sessions = options
    sessions.append(session_id)
    session_list.append(
        dbc.Button(
            session_id,
            id={"type": f"create-session-button", "index": session_id},
            n_clicks=0,
            style={
                "margin-top": "10px",
                "margin-left": "5px",
                "margin-right": "15px",
            },
        )
    )
    return [session_list, sessions]





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
            [ dbc.Col( children=list(GraphicsWindow(
            app, connection_id, session_id, 0, SessionsManager
        ).get_widgets().values()))],
         style={"height": "50rem"},
        
        )

    elif active_tab == "plots":
        return  dbc.Col( children=list(PlotWindow(
            app, connection_id, session_id, 0, SessionsManager
        ).get_widgets().values()))


if __name__ == "__main__":
    app.run_server(debug=True, port=8888)
