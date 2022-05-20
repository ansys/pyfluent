from app_defn import app
from callbacks.main_app import register_callbacks, user_name_to_session_map
import dash
from dash import dcc, html
from dash.long_callback import DiskcacheLongCallbackManager
import dash_bootstrap_components as dbc
from dash_component import RCTree as dash_tree
import plotly.graph_objs as go
import plotly.io as pio
from post_windows import GraphicsWindow, MonitorWindow, PlotWindow
from property_editors import LocalPropertyEditor, SettingsPropertyEditor
from sessions_handle import SessionsHandle
from tree_data_extractor import TreeDataExtractor

HEIGHT = "59rem"
MAX_SESSION_COUNT = 6
pio.templates.default = "plotly_white"


def get_side_bar(user_id, session_id):
    tree_nodes_data = {"title": "Root", "key": "Root", "icon": None, "children": []}
    keys = ["Root"]
    if session_id:
        tree_nodes_data, keys = TreeDataExtractor(user_id, session_id).get_tree_nodes()
    tree = dash_tree(
        id="tree-view",
        expandedKeys=keys,
        data=tree_nodes_data,
        selected=[],
    )
    return html.Div(
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
            html.Div(id="tree-container", children=tree),
        ],
        style={
            "width": "18rem",
            "background-color": "#f8f9fa",
            "height": HEIGHT,
            "overflow-y": "auto",
        },
    )


register_callbacks(app)


def app_layout():
    user_id = "AnsysUser"

    for session in range(MAX_SESSION_COUNT):
        SettingsPropertyEditor(user_id, f"session-{session}", 1)
        LocalPropertyEditor(user_id, f"session-{session}", 1)
        GraphicsWindow(user_id, f"session-{session}", 1)
        MonitorWindow(user_id, f"session-{session}", 1)
        PlotWindow(user_id, f"session-{session}", 1)

    return dbc.Container(
        fluid=True,
        children=[
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
                                            "font": "24px 'Segoe UI'",
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
                            dcc.Loading(
                                parent_className="loading_wrapper",
                                id="loading-sessions-list",
                                type="default",
                                children=dcc.Dropdown(
                                    id="sessions-list",
                                    options=list(
                                        map(
                                            lambda x: x[0],
                                            user_name_to_session_map.get(user_id),
                                        )
                                    )
                                    if user_name_to_session_map.get(user_id)
                                    else [],
                                    value=user_name_to_session_map.get(
                                        user_id, [[None, None]]
                                    )[0][0],
                                    style={
                                        "width": "200px",
                                    },
                                ),
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
                                    "height": "30px",
                                },
                            ),
                            width="auto",
                            align="end",
                        ),
                        dbc.Col(
                            dbc.Input(
                                placeholder="Session token to connect",
                                id="session-token",
                                style={"width": "200px"},
                                size="sm",
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
                                size="sm",
                            ),
                            width="auto",
                            align="end",
                        ),
                    ],
                    style={
                        "padding": "0px 0px 5px",
                        "border-bottom": "14px solid black",
                        "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 10px 0 rgba(0, 0, 0, 0.19)",
                    },
                ),
                # style={
                #     "font": "14px 'Segoe UI'"
                # },
            ),
            dbc.Row(
                children=[
                    dbc.Col(
                        get_side_bar(
                            user_id,
                            user_name_to_session_map.get(user_id, [[None, None]])[0][0],
                        ),
                        align="start",
                        width="auto",
                    ),
                    dbc.Col(
                        id="property-editor-container",
                        width="auto",
                        style={
                            "width": "20rem",
                            "background-color": "#f8f9fa",
                            "overflow-y": "auto",
                            "height": HEIGHT,
                        },
                    ),
                    dbc.Col(
                        html.Div(
                            dcc.Loading(
                                id="loading-tabs",
                                type="default",
                                parent_className="loading_wrapper",
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
                                        style={"height": HEIGHT},
                                    ),
                                ],
                            )
                        )
                    ),
                ],
                style={"padding": "4px 0px 4px 0px"},
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
                        style={"display": "block", "width": "80%"},
                    ),
                ],
                id="progress-container",
                # style={"font": "14px 'Segoe UI'"},
            ),
        ],
        style={"font": "14px 'Segoe UI'"},
    )
