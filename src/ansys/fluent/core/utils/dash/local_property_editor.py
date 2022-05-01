from functools import partial
import dash_bootstrap_components as dbc
from dash import html
import dash_core_components as dcc
import dash_vtk
from dash.dependencies import Input, Output, State, MATCH, ALL
import dash
from dash.exceptions import PreventUpdate
import re
from ansys.fluent.core.utils.generic import SingletonMeta
from ansys.fluent.post.pyvista import Graphics
from ansys.fluent.post.matplotlib import Plots
from ansys.fluent.post.pyvista.pyvista_objects import (
    Contour,
    Mesh,
    Surface,
    Vector,
)
from ansys.fluent.post import set_config
from post_data import update_vtk_fun, update_graph_fun, update_graph_fun_xyplot

set_config(blocking=False)
DISPLAY_BUTTON_ID = "graphics-button"
PLOT_BUTTON_ID = "plot-button"


class LocalPropertyEditor:
    def __init__(self, app, SessionsManager):
        self._app = app
        self._all_widgets = {}
        self.SessionsManager = SessionsManager
        self._graphics_property_editor = GraphicsPropertyEditor(app, SessionsManager)
        self._plot_property_editor = PlotPropertyEditor(app, SessionsManager)

    def get_object_and_static_info(
        self, graphics_type, connection_id, session_id, object_id=None
    ):
        if self._graphics_property_editor.is_type_supported(graphics_type):
            return (
                self._graphics_property_editor.get_object(
                    graphics_type, connection_id, session_id
                ),
                None,
            )
        if self._plot_property_editor.is_type_supported(graphics_type):
            return (
                self._plot_property_editor.get_object(
                    graphics_type, connection_id, session_id
                ),
                None,
            )

    def get_label(self, name):
        name_list = re.split("[^a-zA-Z]", name)
        return " ".join([name.capitalize() for name in name_list])

    def get_widgets(self, graphics_type, connection_id, session_id):
        def store_all_widgets(obj_type, obj, parent="", parent_visible=True):
            for name, value in obj.__dict__.items():
                if name == "_parent":
                    continue

                if value.__class__.__class__.__name__ in (
                    "PyLocalPropertyMeta",
                    "PyLocalObjectMeta",
                ):
                    visible = (
                        getattr(obj, "_availability")(name)
                        if hasattr(obj, "_availability")
                        else True
                    )

                    if not visible:
                        continue

                    if value.__class__.__class__.__name__ == "PyLocalPropertyMeta":
                        widget = self.get_widget(
                            value,
                            value._type,
                            name,
                            parent + "/" + name,
                            getattr(value, "attributes", None),
                        )
                        self._all_widgets[name] = widget
                    else:
                        store_all_widgets(
                            obj_type,
                            value,
                            parent + "/" + name,
                            parent_visible and visible,
                        )

        obj, static_info = self.get_object_and_static_info(
            graphics_type, connection_id, session_id
        )
        self._all_widgets = {}
        store_all_widgets(graphics_type, obj)
        if self._graphics_property_editor.is_type_supported(graphics_type):
            self._all_widgets.update(
                self._graphics_property_editor.get_widgets(
                    graphics_type, connection_id, session_id
                )
            )
        if self._plot_property_editor.is_type_supported(graphics_type):
            self._all_widgets.update(
                self._plot_property_editor.get_widgets(
                    graphics_type, connection_id, session_id
                )
            )
        return self._all_widgets

    def get_widget(
        self,
        obj,
        type,
        name,
        unique_name,
        attributes,
    ):
        widget = html.Div(f"Widget not found for {name}.")
        if str(type) == "<class 'str'>":
            if attributes and "allowed_values" in attributes:
                widget = dcc.Dropdown(
                    id={
                        "type": f"input-widget",
                        "index": unique_name,
                    },
                    options=getattr(obj, "allowed_values"),
                    value=obj(),
                )
            else:
                widget = dcc.Input(
                    id={
                        "type": f"input-widget",
                        "index": unique_name,
                    },
                    type="text",
                    value=obj(),
                )
        elif str(type) == "typing.List[str]":
            widget = dcc.Dropdown(
                id={
                    "type": f"input-widget",
                    "index": unique_name,
                },
                options=getattr(obj, "allowed_values"),
                value=obj(),
                multi=True,
            )
            # print('widget', widget)
        elif str(type) == "<class 'bool'>":
            widget = dcc.Checklist(
                id={
                    "type": f"input-widget",
                    "index": unique_name,
                },
                options={
                    "selected": self.get_label(name),
                },
                value=["selected"] if obj() else [],
                style={"padding": "5px"},
                labelStyle={"display": "inline-block"},
                inputStyle={"padding": "1px 1px 1px 5px"},
            )
        elif str(type) == "<class 'float'>":
            if attributes and "range" in attributes:
                range = getattr(obj, "range")
                widget = dcc.Input(
                    id={
                        "type": f"input-widget",
                        "index": unique_name,
                    },
                    type="number",
                    value=obj(),
                    min=range[0] if range else None,
                    max=range[1] if range else None,
                )
            else:
                widget = dcc.Input(
                    id={
                        "type": f"input-widget",
                        "index": unique_name,
                    },
                    type="number",
                    value=obj(),
                )
        elif str(type) == "<class 'int'>":
            if attributes and "range" in attributes:
                widget = dcc.Input(
                    id={
                        "type": f"input-widget",
                        "index": unique_name,
                    },
                    type="number",
                    value=obj(),
                    min=getattr(obj, "range")[0],
                    max=getattr(obj, "range")[1],
                )
            else:
                widget = dcc.Input(
                    id={
                        "type": f"input-widget",
                        "index": unique_name,
                    },
                    type="number",
                    value=obj(),
                )

        if str(type) == "<class 'bool'>":
            widget = html.Div(
                [widget],
            )
        else:
            widget = html.Div(
                [
                    dbc.Label(self.get_label(name)),
                    widget,
                ],
                style={
                    "display": "flex",
                    "flex-direction": "column",
                    "padding": "10px 1px 2px",
                },
            )
        return widget


class GraphicsPropertyEditor:
    def __init__(self, app, SessionsManager):
        self._app = app
        self.SessionsManager = SessionsManager

    def is_type_supported(self, type):
        return type in ("Contour", "Mesh", "Vector", "Surface")

    def get_widgets(self, graphics_type, connection_id, session_id):
        return {
            "display-button": dbc.Button(
                "Display",
                id=f"{DISPLAY_BUTTON_ID}",
                n_clicks=0,
            )
        }

    def get_object(self, graphics_type, connection_id, session_id, object_id=None):
        if graphics_type is not None:
            session = self.SessionsManager(self._app, connection_id, session_id).session
            graphics_session = Graphics(session)

            if graphics_type == "Contour":
                return graphics_session.Contours[
                    f"contour-{connection_id}-{session_id}-{object_id if object_id else 'dummy'}"
                ]
            if graphics_type == "Mesh":
                return graphics_session.Meshes[
                    f"mesh-{connection_id}-{session_id}-{object_id if object_id else 'dummy'}"
                ]
            if graphics_type == "Vector":
                return graphics_session.Vectors[
                    f"vector-{connection_id}-{session_id}-{object_id if object_id else 'dummy'}"
                ]
            if graphics_type == "Surface":
                return graphics_session.Surfaces[
                    f"surface-{connection_id}-{session_id}-{object_id if object_id else 'dummy'}"
                ]


class PlotPropertyEditor:
    def __init__(self, app, SessionsManager):
        self._app = app
        self.SessionsManager = SessionsManager

    def is_type_supported(self, type):
        return type in ("XYPlot")

    def get_widgets(self, graphics_type, connection_id, session_id):
        return {
            "plot-button": dbc.Button(
                "Plot",
                id=f"{PLOT_BUTTON_ID}",
                n_clicks=0,
            )
        }

    def get_object(self, graphics_type, connection_id, session_id, object_id=None):
        if graphics_type is not None:
            session = self.SessionsManager(self._app, connection_id, session_id).session
            plots_session = Plots(session)
            if graphics_type == "XYPlot":
                return plots_session.XYPlots[
                    f"xyplot-{connection_id}-{session_id}-{object_id if object_id else 'dummy'}"
                ]


class PostWindowCollection:

    _windows = {}

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
            self._last_clicked = 0
            self._SessionsManager = SessionsManager

            @self._app.callback(
                Output(f"{self._unique_id}-tab-content", "children"),
                Input(f"{self._unique_id}-tabs", "active_tab"),
                Input("connection-id", "data"),
                Input("session-id", "value"),
                prevent_initial_call=True,
            )
            def render_tab_content(active_tab, connection_id, session_id):
                """
                This callback takes the 'active_tab' property as input, as well as the
                stored graphs, and renders the tab content depending on what the value of
                'active_tab' is.
                """
                self._active_window = int(active_tab)
                return self.get_content()

            @self._app.callback(
                Output(f"post-viewer-{self._unique_id}", "children"),
                Input(f"{window_type}-button", "n_clicks"),
                Input("connection-id", "data"),
                State("window-id", "value"),
                State("session-id", "value"),
                State("object-id", "value"),
                prevent_initial_call=True,
            )
            def on_button_click(
                n_clicks, connection_id, window_id, session_id, object_id
            ):
                print("on_button_click", n_clicks, self._last_clicked)
                if n_clicks == 0:
                    raise PreventUpdate
                self._last_clicked = n_clicks
                object_location, object_type = object_id.split(":")
                if object_location != "local":
                    raise PreventUpdate
                return self.get_viewer(object_type, connection_id, session_id)

        else:
            self.__dict__ = window_state

    def __call__(self):
        return dbc.Col(
            [
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
                            className="me-2",
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
                    style={"padding": "4px 4px 4px 4px", "border": "1px ridge lightgrey", "margin" : "0px 0px 4px 0px"},
                ),
                dbc.Tabs(
                    [
                        dbc.Tab(label=f"window-{window}", tab_id=f"{window}")
                        for window in self._windows
                    ],
                    id=f"{self._unique_id}-tabs",
                    active_tab=f"{self._active_window}",
                ),
                dbc.CardBody(
                    id=f"{self._unique_id}-tab-content",
                    style={"height": "100%"},
                    children=self.get_content(),
                ),
            ],
           
            style={"height": "43rem"},
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

    def get_content(self):
        return [
            html.Div(
                id=f"post-viewer-{self._unique_id}",
                style={"height": "100%"},
                children=self._get_graph(),
            )
        ]

    def get_viewer(self, object_type, connection_id, session_id):
        editor = PlotPropertyEditor(self._app, self._SessionsManager)
        obj = editor.get_object(object_type, connection_id, session_id)
        if obj is None:
            raise PreventUpdate
        self._state[self._active_window] = update_graph_fun(obj)
        return self._get_graph()


class GraphicsWindowCollection(PostWindowCollection):
    def __init__(self, app, connection_id, session_id, SessionsManager):
        super().__init__(app, connection_id, session_id, "graphics", SessionsManager)

    def _get_graphics(self):
        return self._state.get(self._active_window, [])

    def get_content(self):
        return [
            dash_vtk.View(
                id=f"post-viewer-{self._unique_id}",
                pickingModes=["hover"],
                children=self._get_graphics(),
            )
        ]

    def get_viewer(self, object_type, connection_id, session_id):
        editor = GraphicsPropertyEditor(self._app, self._SessionsManager)
        obj = editor.get_object(object_type, connection_id, session_id)
        if obj is None:
            raise PreventUpdate
        self._state[self._active_window] = update_vtk_fun(obj)[0]
        print("get_viewer", self._state[self._active_window])
        return self._get_graphics()


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

            @app.callback(
                Output(f"{self._unique_win_id}-tab-content", "children"),
                Input(f"{self._unique_win_id}-tabs", "active_tab"),
                Input("interval-component", "n_intervals"),
                Input("connection-id", "data"),
                Input("session-id", "value"),
            )
            def render_tab_content(active_tab, n_intervals, connection_id, session_id):
                """
                This callback takes the 'active_tab' property as input, as well as the
                stored graphs, and renders the tab content depending on what the value of
                'active_tab' is.
                """
                session = self.SessionsManager(
                    self._app, connection_id, session_id
                ).session
                fig = session.monitors_manager.get_monitor_set_data(active_tab)

                if active_tab == "residual":
                    fig.update_yaxes(type="log")

                fig.update_layout(
                    title={
                        "text": session.monitors_manager.get_monitor_set_prop(
                            active_tab, "title"
                        ),
                        "y": 0.95,
                        "x": 0.5,
                        "xanchor": "center",
                        "yanchor": "top",
                    },
                    xaxis_title=session.monitors_manager.get_monitor_set_prop(
                        active_tab, "xlabel"
                    ),
                    yaxis_title=session.monitors_manager.get_monitor_set_prop(
                        active_tab, "ylabel"
                    ),
                    legend_title=session.monitors_manager.get_monitor_set_prop(
                        active_tab, active_tab
                    ),
                    font=dict(family="Courier New, monospace", size=14, color="black"),
                )
                print(fig)
                return dcc.Graph(
                    figure=fig,
                    style={"height": "100%"},
                )

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
                    id=f"{self._unique_win_id}-tabs",
                    active_tab=monitor_sets[0],
                ),
                html.Div(
                    id=f"{self._unique_win_id}-tab-content",
                    style={"height": "100%"},
                ),
            ],
            style={"height": "43rem"},
        )
