from functools import partial
import dash_bootstrap_components as dbc
from dash import html
import dash_core_components as dcc


from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
import dash_vtk
from post_data import update_vtk_fun, update_graph_fun, update_graph_fun_xyplot
from objects_handle import LocalObjectsHandle

from ansys.fluent.post import set_config
set_config(blocking=False)



class PostWindowCollection:

    _windows = {}
    _is_executing = False
    _show_outline = False

    def __init__(self, app, connection_id, session_id, window_type, SessionsManager):
        unique_id = f"{window_type}-{connection_id}-{session_id}"
        window_state = PostWindowCollection._windows.get(unique_id)
        if not window_state:
            PostWindowCollection._windows[unique_id] = self.__dict__
            self._window_type = window_type
            self._state = {}
            self._unique_id = unique_id
            self._app = app
            self._windows = [0]
            self._active_window = 0
            self._window_data = {}
            self._SessionsManager = SessionsManager
        else:
            self.__dict__ = window_state

    def copy_from(self, connection_id, session_id):
        source = PostWindowCollection(
            self._app,
            connection_id,
            session_id,
            self._window_type,
            self._SessionsManager,
        )
        self._windows = source._windows
        self._window_data = source._window_data
        self._state = source._state

    def __call__(self):

        return html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Tabs(
                                [
                                    dbc.Tab(
                                        label=f"window-{window}", tab_id=f"{window}"
                                    )
                                    for window in self._windows
                                ],
                                id="post-window-tabs",
                                active_tab=f"{self._active_window}",
                                style={
                                    "margin": "10px 0px 0px 0px",
                                    "padding": "4px 4px 0px 4px",
                                },
                            )
                        ),
                        dbc.Col(
                            html.Div(
                                [
                                    dbc.Button(
                                        "Add Window",
                                        id={
                                            "type": "add-post-window",
                                            "index": self._window_type,
                                        },
                                        size="sm",
                                        n_clicks=0,
                                        outline=True,
                                        color="secondary",
                                        className="me-1",
                                    ),
                                    dbc.Button(
                                        "Remove Window",
                                        id={
                                            "type": "remove-post-window",
                                            "index": self._window_type,
                                        },
                                        size="sm",
                                        n_clicks=0,
                                        outline=True,
                                        color="secondary",
                                        className="me-1",
                                    ),
                                ],
                                style={
                                    "padding": "4px 4px 4px 4px",
                                },
                            ),
                            width="auto",
                        ),
                    ]
                ),
                html.Div(
                    id="post-window-tab-content",
                    style={"padding": "4px 4px 0px 4px", "height": "837px"},
                    children=self.get_content(),
                ),
            ],
            style={
                "height": "57rem",
                "overflow-y": "auto",
                "overflow-x": "hidden",
            },
        )


class PlotWindowCollection(PostWindowCollection):
    def __init__(self, app, connection_id, session_id, SessionsManager):
        super().__init__(app, connection_id, session_id, "plot", SessionsManager)

    def _get_graph(self):
        return [
            dcc.Graph(
                figure=self._state.get(self._active_window, update_graph_fun_xyplot()),
                style={"height": "100%"},
            )
        ]

    def is_type_supported(self, type):
        return LocalObjectsHandle(self._SessionsManager).get_handle_type(type)=="plot"
       

    def get_content(self):
        print("data updated")
        return [
            html.Div(
                id=f"post-viewer-{self._unique_id}",
                style={"height": "100%"},
                children=self._get_graph(),
            )
        ]

    def get_viewer(self, connection_id, session_id, object_type, object_index):
        handle = LocalObjectsHandle(self._SessionsManager)
        obj = handle._get_object(connection_id, session_id, object_type, object_index)
        if obj is None:
            raise PreventUpdate
        self._state[self._active_window] = update_graph_fun(obj)
        print("data fetched")
        return self.get_content()


class GraphicsWindowCollection(PostWindowCollection):
    def __init__(self, app, connection_id, session_id, SessionsManager):
        super().__init__(app, connection_id, session_id, "graphics", SessionsManager)

    def _get_graphics(self):
        return self._state.get(self._active_window, [[]])[0]

    def _get_colorbar(self):
        color_bar_data = self._state.get(self._active_window, [None, None])[1]
        try:
            return (
                self.make_colorbar(color_bar_data[0], color_bar_data[1:])
                if color_bar_data
                else go.Figure()
            )
        except:
            return go.Figure()

    def is_type_supported(self, type):
        return LocalObjectsHandle(self._SessionsManager).get_handle_type(type)=="graphics"
        

    def get_content(self):
        print("get_content", self._active_window, list(self._state.keys()))
        print("_get_graphics", self._get_graphics())
        content = [
            dbc.Col(
                dash_vtk.View(
                    id=f"post-viewer-{self._unique_id}",
                    pickingModes=["hover"],
                    children=self._get_graphics(),
                    style={"height": "837px"},
                )
            )
        ]
        if self._state.get(self._active_window, [None, None])[1]:
            content.append(
                dbc.Col(
                    dcc.Graph(
                        id=f"color-bar-{self._unique_id}",
                        figure=self._get_colorbar(),
                    ),
                    width="auto",
                )
            )

        return [
            dbc.Row(
                content,
                className="g-0",
            )
        ]

    def get_viewer(self, connection_id, session_id, object_type, object_index):
        handle = LocalObjectsHandle(self._SessionsManager)
        obj = handle._get_object(connection_id, session_id, object_type, object_index)
        if obj is None:
            print("state not updated")
            raise PreventUpdate
        color_bar = []
        self._state[self._active_window] = (
            update_vtk_fun(obj, color_bar)[0],
            color_bar,
        )
        return self.get_content()

    def make_colorbar(self, title, rng, bgnd="rgb(51, 76, 102)"):
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                marker=dict(
                    colorscale="rainbow",
                    showscale=True,
                    cmin=rng[0],
                    cmax=rng[1],
                    colorbar=dict(
                        title_text=title,
                        title_font_color="white",
                        title_side="top",
                        thicknessmode="pixels",
                        thickness=50,
                        #  lenmode="pixels", len=200,
                        yanchor="middle",
                        y=0.5,
                        ypad=10,
                        xanchor="left",
                        x=0.0,
                        xpad=10,
                        ticks="outside",
                        tickcolor="white",
                        tickfont={"color": "white"}
                        #  dtick=5
                    ),
                ),
                hoverinfo="none",
            )
        )
        fig.update_layout(
            width=150,
            height=837,  # px
            margin={"b": 0, "l": 0, "r": 0, "t": 0},
            autosize=False,
            plot_bgcolor=bgnd,
        )
        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)
        return fig


class MonitorWindow:

    _windows = {}

    def __init__(self, app, connection_id, session_id, SessionsManager):
        unique_win_id = f"monitor-{connection_id}-{session_id}"
        window_state = MonitorWindow._windows.get(unique_win_id)
        if not window_state:
            MonitorWindow._windows[unique_win_id] = self.__dict__

            self._unique_win_id = unique_win_id
            self._app = app
            self._connection_id = connection_id
            self._session_id = session_id
            self.SessionsManager = SessionsManager

        else:
            self.__dict__ = window_state

    def __call__(self):
        session = self.SessionsManager(
            self._app, self._connection_id, self._session_id
        ).session

        monitor_sets = session.monitors_manager.get_monitor_sets_name()
        if len(monitor_sets) == 0:
            return []
        return dbc.Col(
            [
                dbc.Tabs(
                    [
                        dbc.Tab(label=monitor_set, tab_id=monitor_set)
                        for monitor_set in monitor_sets
                    ],
                    id=f"monitor-tabs",
                    active_tab=monitor_sets[0],
                    style={
                        "margin": "10px 0px 0px 0px",
                        "padding": "4px 4px 0px 4px",
                    },
                ),
                html.Div(
                    id=f"monitor-tab-content",
                    style={"height": "100%"},
                ),
            ],
            style={"height": "837px"},
        )
