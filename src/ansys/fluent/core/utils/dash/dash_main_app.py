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
from vtk_apis import update_vtk_fun, update_graph_fun

from ansys.fluent.core.utils.dash.graphics_widgets import GraphicsWidget
from ansys.fluent.core.utils.dash.plots_widgets import PlotsWidget

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.config.suppress_callback_exceptions=True

SIDEBAR_STYLE = {
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

sidebar = html.Div(
    [

        html.P(
            "Outline", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Contour", href="/", active="exact"),
                dbc.NavLink("Vector", href="/page-1", active="exact"),
                dbc.NavLink("Mesh", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)


def serve_layout():
    session_id = str(uuid.uuid4())
    GraphicsWidget(app, update_vtk_fun)
    PlotsWidget(app, update_graph_fun)
    return dbc.Container(
        fluid=True,
        children=[
            html.Data(id="refresh-trigger"),
            dcc.Store(data=session_id, id="session-id"),
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
    Output("tab-content", "children"),
    Input("tabs", "active_tab"),
    State("tab-content", "children"),
)
def render_tab_content(active_tab, tab_content):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """

    if active_tab == "graphics":        
        return GraphicsWidget(app, update_vtk_fun).refresh()
            
    elif active_tab == "plots":
        return PlotsWidget(app).layout()


if __name__ == "__main__":
    app.run_server(debug=True, port=8888)
