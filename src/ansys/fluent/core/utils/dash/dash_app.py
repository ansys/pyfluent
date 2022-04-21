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
from dash import Input, Output, State, dcc, html
from dash.exceptions import PreventUpdate

from ansys.fluent.core.utils.dash.post_widgets import GraphicsWidget, PlotWidget

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.config.suppress_callback_exceptions=True

SIDEBAR_STYLE = {
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "height": "55rem",
    "overflow-y": "scroll"
}

sidebar = html.Div(
    [
        html.P(
            "Outline", className="lead"
        ),
        dbc.Col(
            dbc.Button("Connect to Session", id="connect-session", size="lg", n_clicks=0, active=True)
        ),
        
        html.Div(
            children =[],
            id =  "session-list",           
        )
    ],
    style=SIDEBAR_STYLE,
)

class SessionView:
    _sessions_state = {}
    def __init__(self, connection_id, session_id):
        session_id = f"session-{session_id}-{connection_id}"
        session_state = SessionView._sessions_state.get(
            session_id
        )           
        if not session_state:  
            SessionView._sessions_state[
                session_id
            ] = self.__dict__  
        else:            
            self.__dict__ = session_state 

def serve_layout():
    connection_id = str(uuid.uuid4())
    GraphicsWidget(app, connection_id, 1)
    PlotWidget(app, connection_id, 1)
    return dbc.Container(
        fluid=True,
        children=[            
            dcc.Store(data=connection_id, id="connection-id"),
            dcc.Store(id="tab-info"),
            html.H1("Ansys pyFluent post web App"),
            html.Hr(),            
            dbc.Row(
                children=[
                    dbc.Col(sidebar, align="start", width="auto"),
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
                                active_tab="scatter",
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
    Output("session-list", "children"),
    Input("connect-session", "n_clicks"),
    State("session-list", "children"),
)
def connect_to_session(n_clicks, session_list):
    if n_clicks==0:
        raise PreventUpdate
    id = f"{len(session_list)}"
    session_list.append(dbc.Button(f"Session-{id}", id=f"session-{id}", n_clicks=0, style={"margin-top": "10px", "margin-left": "5px", "margin-right": "15px"}))  
    return session_list


@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab"),
    Input("connection-id", "data"),
    State("tab-content", "children"),
)
def render_tab_content(active_tab, connection_id, tab_content):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """

    if active_tab == "graphics":        
        return GraphicsWidget(app, connection_id, 1).layout()
            
    elif active_tab == "plots":
        return PlotWidget(app, connection_id, 1).layout()


if __name__ == "__main__":
    app.run_server(debug=True, port=8888)
