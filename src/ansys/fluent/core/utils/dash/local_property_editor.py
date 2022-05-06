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
SAVE_BUTTON_ID = "save-button"
DELETE_BUTTON_ID = "delete-button"


class LocalPropertyEditor:
    def __init__(self, app, SessionsManager):

        self._app = app
        self._all_widgets = {}
        self.SessionsManager = SessionsManager
        self._graphics_property_editor = GraphicsPropertyEditor(app, SessionsManager)
        self._plot_property_editor = PlotPropertyEditor(app, SessionsManager)

    def _get_editor(self, object_type):
        return (
            self._graphics_property_editor
            if self._graphics_property_editor.is_type_supported(object_type)
            else self._plot_property_editor
        )

    def get_child_indices(self, connection_id, session_id, object_type):
        collection = self._get_editor(object_type).get_collection(
            connection_id, session_id, object_type
        )
        indices = []
        if collection is not None:
            base_name = self._get_name(connection_id, session_id, object_type, "")
            for name in list(collection):
                if name.startswith(base_name):
                    indices.append(name.split("-")[-1])
        return indices

    def _get_name(self, connection_id, session_id, object_type, object_index):       
        return f"{self.SessionsManager(self._app, connection_id, session_id)._complete_session_id}-{object_type}-{object_index}"

    def create_new_object(self, connection_id, session_id, object_type, from_index):
        object_index = self.get_next_index(connection_id, session_id, object_type)
        new_object = self._get_object(
            connection_id, session_id, object_type, object_index
        )
        from_object = self._get_object(
            connection_id, session_id, object_type, from_index
        )
        new_object.update(from_object())
        return new_object

    def get_next_index(self, connection_id, session_id, object_type):
        collection = self._get_editor(object_type).get_collection(
            connection_id, session_id, object_type
        )
        if collection is not None:
            object_index = 0
            while True:
                object_name = self._get_name(
                    connection_id, session_id, object_type, object_index
                )
                if object_name not in list(collection):
                    break
                object_index = object_index + 1
            return object_index

    def _get_object(self, connection_id, session_id, object_type, object_index):
        collection = self._get_editor(object_type).get_collection(
            connection_id, session_id, object_type
        )
        if collection is not None:

            object_name = self._get_name(
                connection_id, session_id, object_type, object_index
            )
            return collection[object_name]

    def delete_object(self, connection_id, session_id, object_type, object_index):
        collection = self._get_editor(object_type).get_collection(
            connection_id, session_id, object_type
        )
        if collection is not None:
            object_name = self._get_name(
                connection_id, session_id, object_type, object_index
            )
            del collection[object_name]

    def get_object_and_static_info(
        self, connection_id, session_id, object_type, object_index
    ):
        return (
            self._get_object(connection_id, session_id, object_type, object_index),
            None,
        )

    def get_label(self, name):
        name_list = re.split("[^a-zA-Z]", name)
        return " ".join([name.capitalize() for name in name_list])

    def get_widgets(
        self, connection_id, session_id, object_type, object_index, widget_type
    ):
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
            connection_id, session_id, object_type, object_index
        )
        self._all_widgets = {}

        if widget_type == "input":
            store_all_widgets(object_type, obj)
        else:
            self._all_widgets = self._get_editor(object_type).get_widgets(
                connection_id, session_id, object_type, object_index
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
                    "padding": "4px",
                },
            )
        return widget


class GraphicsPropertyEditor:
    def __init__(self, app, SessionsManager):
        self._app = app
        self.SessionsManager = SessionsManager

    def is_type_supported(self, type):
        return type in ("Contour", "Mesh", "Vector", "Surface")

    def get_widgets(self, connection_id, session_id, object_type, object_index):
        return (
            {
                "display-button": dbc.Button(
                    "Display", id=f"{DISPLAY_BUTTON_ID}", n_clicks=0, size="sm"
                ),
                "delete-button": dbc.Button(
                    "Delete", id=f"{DELETE_BUTTON_ID}", n_clicks=0, size="sm"
                ),
            }
            if object_index
            else {
                "display-button": dbc.Button(
                    "Display", id=f"{DISPLAY_BUTTON_ID}", n_clicks=0, size="sm"
                ),
                "save-button": dbc.Button(
                    "New", id=f"{SAVE_BUTTON_ID}", n_clicks=0, size="sm"
                ),
            }
        )

    def get_collection(self, connection_id, session_id, object_type):
        session = self.SessionsManager(self._app, connection_id, session_id).session
        graphics_session = Graphics(session)
        if object_type == "Contour":
            return graphics_session.Contours
        if object_type == "Mesh":
            return graphics_session.Meshes
        if object_type == "Vector":
            return graphics_session.Vectors
        if object_type == "Surface":
            return graphics_session.Surfaces


class PlotPropertyEditor:
    def __init__(self, app, SessionsManager):
        self._app = app
        self.SessionsManager = SessionsManager

    def is_type_supported(self, type):
        return type in ("XYPlot")

    def get_widgets(self, connection_id, session_id, object_type, object_index):
        return {
            "plot-button": dbc.Button(
                "Plot", id=f"{PLOT_BUTTON_ID}", n_clicks=0, size="sm"
            )
        }

    def get_collection(self, connection_id, session_id, object_type):
        session = self.SessionsManager(self._app, connection_id, session_id).session
        plots_session = Plots(session)
        if object_type == "XYPlot":
            return plots_session.XYPlots


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
            self._window_data = {}
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
                Input("graphics-button-clicked", "value"),
                Input("plot-button-clicked", "value"),
                Input("connection-id", "data"),
                Input("interval-component", "n_intervals"),
                State("window-id", "value"),
                State("session-id", "value"),
                State("object-id", "value"),
                prevent_initial_call=True,
            )
            def on_click_update(
                n_graphics_clicks,
                n_plot_clicks,
                connection_id,
                n_intervals,
                window_id,
                session_id,
                object_id,
            ):
                ctx = dash.callback_context
                triggered_value = ctx.triggered[0]["value"]
                if triggered_value is None:
                    raise PreventUpdate
                triggered_from = ctx.triggered[0]["prop_id"].split(".")[0]
                if triggered_from == "interval-component":
                    window_data = self._window_data.get(self._active_window)
                    if window_data is None:
                        raise PreventUpdate
                    event_info = self._SessionsManager(
                        self._app, connection_id, session_id
                    ).get_event_info("IterationEndedEvent")
                    if event_info is None:
                        raise PreventUpdate

                    last_updated_index = window_data.get("last_updated_index")
                    if last_updated_index and last_updated_index == event_info.index:
                        raise PreventUpdate

                    object_type = window_data["object_type"]
                    object_index = window_data["object_index"]
                    window_data["last_updated_index"] = event_info.index
                else:
                    if triggered_value == "0":
                        raise PreventUpdate
                    object_location, object_type, object_index = object_id.split(":")
                    if object_location != "local":
                        raise PreventUpdate
                    if not self.is_type_supported(object_type):
                        raise PreventUpdate
                    self._window_data[self._active_window] = {
                        "object_type": object_type,
                        "object_index": object_index,
                    }
                print("on_button_click..updating", triggered_from, triggered_value)
                return self.get_viewer(
                    connection_id, session_id, object_type, object_index
                )

        else:
            self.__dict__ = window_state

    def copy_from(self, connection_id, session_id):
        source = PostWindowCollection( self._app, connection_id, session_id, self._window_type, self._SessionsManager)
        PostWindowCollection._windows[self._unique_id] = PostWindowCollection._windows[source._unique_id]   

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
                                id=f"{self._unique_id}-tabs",
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
                                style={
                                    "padding": "4px 4px 4px 4px",
                                    "border": "0px ridge lightgrey",
                                },
                            ),
                            width="auto",
                        ),
                    ]
                ),
                html.Div(
                    id=f"{self._unique_id}-tab-content",
                    style={
                        "height": "746px",
                        "padding": "4px 4px 0px 4px",
                    },
                    children=self.get_content(),
                ),
            ],
            style={
                "height": "50rem",
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
        return PlotPropertyEditor(self._app, self._SessionsManager).is_type_supported(
            type
        )

    def get_content(self):
        return [
            html.Div(
                id=f"post-viewer-{self._unique_id}",
                style={"height": "100%"},
                children=self._get_graph(),
            )
        ]

    def get_viewer(self, connection_id, session_id, object_type, object_index):
        editor = LocalPropertyEditor(self._app, self._SessionsManager)
        obj = editor._get_object(connection_id, session_id, object_type, object_index)
        if obj is None:
            raise PreventUpdate
        self._state[self._active_window] = update_graph_fun(obj)
        return self._get_graph()


class GraphicsWindowCollection(PostWindowCollection):
    def __init__(self, app, connection_id, session_id, SessionsManager):
        super().__init__(app, connection_id, session_id, "graphics", SessionsManager)

    def _get_graphics(self):
        return self._state.get(self._active_window, [])

    def is_type_supported(self, type):
        return GraphicsPropertyEditor(
            self._app, self._SessionsManager
        ).is_type_supported(type)

    def get_content(self):
        return [
            dash_vtk.View(
                id=f"post-viewer-{self._unique_id}",
                pickingModes=["hover"],
                children=self._get_graphics(),
            )
        ]

    def get_viewer(self, connection_id, session_id, object_type, object_index):
        editor = LocalPropertyEditor(self._app, self._SessionsManager)
        obj = editor._get_object(connection_id, session_id, object_type, object_index)
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
                    style={
                        "margin": "10px 0px 0px 0px",
                        "padding": "4px 4px 0px 4px",
                    },
                ),
                html.Div(
                    id=f"{self._unique_win_id}-tab-content",
                    style={"height": "100%"},
                ),
            ],
            style={"height": "43rem"},
        )
