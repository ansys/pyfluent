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
import plotly.graph_objs as go
from ansys.fluent.post.pyvista.pyvista_objects import (
    Contour,
    Mesh,
    Surface,
    Vector,
)
from ansys.fluent.post import set_config
from post_data import update_vtk_fun, update_graph_fun, update_graph_fun_xyplot
from property_editor import PropertyEditor


set_config(blocking=False)
DISPLAY_BUTTON_ID = "graphics-button"
PLOT_BUTTON_ID = "plot-button"
SAVE_BUTTON_ID = "save-button"
DELETE_BUTTON_ID = "delete-button"


class LocalPropertyEditor(PropertyEditor):
    def __init__(self, app, SessionsManager):
        super().__init__(app)
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
                            f"{parent}/{name}:local:{object_type}:{object_index}",
                            # parent + "/" + name+":local:"+object_type+":"+object_index,
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
        return (
            {
                "plot-button": dbc.Button(
                    "Plot", id=f"{PLOT_BUTTON_ID}", n_clicks=0, size="sm"
                ),
                "delete-button": dbc.Button(
                    "Delete", id=f"{DELETE_BUTTON_ID}", n_clicks=0, size="sm"
                ),
            }
            if object_index
            else {
                "plot-button": dbc.Button(
                    "Plot", id=f"{PLOT_BUTTON_ID}", n_clicks=0, size="sm"
                ),
                "save-button": dbc.Button(
                    "New", id=f"{SAVE_BUTTON_ID}", n_clicks=0, size="sm"
                ),
            }
        )

    def get_collection(self, connection_id, session_id, object_type):
        session = self.SessionsManager(self._app, connection_id, session_id).session
        plots_session = Plots(session)
        if object_type == "XYPlot":
            return plots_session.XYPlots
