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
from post_data import update_vtk_fun, update_graph_fun
set_config(blocking=False)
DISPLAY_BUTTON_ID = "display-graphics-button"
PLOT_BUTTON_ID = "plot-graph-button"


class LocalPropertyEditor:
    def __init__(self, app, SessionsManager):
        self._app = app
        self._all_widgets = {}
        self.SessionsManager = SessionsManager
        self._graphics_property_editor = GraphicsPropertyEditor(
            app, SessionsManager
        )
        self._plot_property_editor = PlotPropertyEditor(app, SessionsManager)

    def get_object_and_static_info(
        self, graphics_type, connection_id, session_id, object_id=None
    ):
        if self._graphics_property_editor.is_type_supported(graphics_type):
            return self._graphics_property_editor.get_object(
                graphics_type, connection_id, session_id
            ), None
        if self._plot_property_editor.is_type_supported(graphics_type):
            return self._plot_property_editor.get_object(
                graphics_type, connection_id, session_id
            ), None

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

                    if (
                        value.__class__.__class__.__name__
                        == "PyLocalPropertyMeta"
                    ):
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
                        
        obj, static_info = self.get_object_and_static_info(graphics_type, connection_id, session_id)
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

    def get_object(
        self, graphics_type, connection_id, session_id, object_id=None
    ):
        if graphics_type is not None:
            session = self.SessionsManager(
                self._app, connection_id, session_id
            ).session
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

    def get_object(
        self, graphics_type, connection_id, session_id, object_id=None
    ):
        if graphics_type is not None:
            session = self.SessionsManager(
                self._app, connection_id, session_id
            ).session
            plots_session = Plots(session)
            if graphics_type == "XYPlot":
                return plots_session.XYPlots[
                    f"xyplot-{connection_id}-{session_id}-{object_id if object_id else 'dummy'}"
                ]


class GraphicsWindow:

    _windows = {}

    def __init__(self, app, connection_id, session_id, win_id, SessionsManager):
        unique_win_id = f"graphics-{connection_id}-{session_id}-{win_id}"
        window_state = GraphicsWindow._windows.get(unique_win_id)
        if not window_state:
            GraphicsWindow._windows[unique_win_id] = self.__dict__

            self._state = []
            self._win_id = win_id
            self._unique_win_id = unique_win_id
            self._app = app

            @self._app.callback(
                Output(f"vtk-view-{self._unique_win_id}", "children"),
                Input(f"{DISPLAY_BUTTON_ID}", "n_clicks"),
                Input("connection-id", "data"),
                State("window-id", "value"),
                State("session-id", "value"),
                State("object-id", "value"),
            )
            def on_button_click(
                n_clicks, connection_id, window_id, session_id, object_id
            ):                
                print('on_button_click', n_clicks, connection_id, window_id, session_id, object_id, self._win_id)
                if n_clicks == 0:
                    raise PreventUpdate
                object_location, object_type = object_id.split(":")                
                if object_location != "local":
                    raise PreventUpdat
                if int(window_id) != self._win_id:
                    raise PreventUpdate
                editor = GraphicsPropertyEditor(app, SessionsManager)    
                obj = editor.get_object(object_type, connection_id, session_id)
                print("n_clicks on_button_click", n_clicks, obj._name)
                vtk_rendering_data = update_vtk_fun(obj)
                self._state = vtk_rendering_data[0]
                return self._state

        else:
            self.__dict__ = window_state

    def get_widgets(self):
        return {f"vtk-widget-{self._unique_win_id}": html.Div(
            dash_vtk.View(
                id=f"vtk-view-{self._unique_win_id}",
                pickingModes=["hover"],
                children=self._state,
            ),
            style={"height": "100%", "width": "100%"},
        )}


class PlotWindow:

    _windows = {}

    def __init__(self, app, connection_id, session_id, win_id, SessionsManager):
        unique_win_id = f"plot-{connection_id}-{session_id}-{win_id}"        
        window_state = PlotWindow._windows.get(unique_win_id)
        if not window_state:
            PlotWindow._windows[unique_win_id] = self.__dict__

            self._state = {}
            self._win_id = win_id
            self._unique_win_id = unique_win_id
            self._app = app

            @self._app.callback(
                Output(f"plot-viewer-{self._unique_win_id}", "figure"),
                Input(f"{PLOT_BUTTON_ID}", "n_clicks"),
                Input("connection-id", "data"),
                State("window-id", "value"),
                State("session-id", "value"),
                State("object-id", "value"),
            )
            def on_button_click(
                n_clicks, connection_id, window_id, session_id, object_id
            ):
                if n_clicks == 0:
                    raise PreventUpdate
                object_location, object_type = object_id.split(":")
                if object_location != "local":
                    raise PreventUpdat
                if int(window_id) != self._win_id:
                    raise PreventUpdate
                editor = PlotPropertyEditor(app, SessionsManager)       
                obj = editor.get_object(object_type, connection_id, session_id)
                print("n_clicks on_button_click", n_clicks, obj._name)
                self._state = update_graph_fun(obj)
                return self._state

        else:
            self.__dict__ = window_state

    def get_widgets(self):
        return {f"plot-viewer-{self._unique_win_id}": dcc.Graph(
            id=f"plot-viewer-{self._unique_win_id}",
            figure=self._state,
            style={"height": 900},
        )}
