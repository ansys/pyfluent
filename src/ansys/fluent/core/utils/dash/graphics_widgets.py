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
from ansys.fluent.post.pyvista.pyvista_objects import (
    Contour,
    Mesh,
    Surface,
    Vector,
)
from ansys.fluent.post import set_config
from ansys.fluent.core.session import Session

session = Session.create_from_server_info_file(
    "E:\\ajain\\Demo\\pyApp\\pyvista\\server.txt", False
)
set_config(blocking=False)
graphics_session1 = Graphics(session)
import uuid

# contour1 = graphics_session1.Contours["contour-1"]
# contour1.field = "velocity-magnitude"
# contour1.surfaces_list = ["symmetry"]
# contour1.node_values = False

# contour2 = graphics_session1.Contours["contour-2"]
# contour2.field = "temperature"
# contour2.surfaces_list = ["wall"]


class GraphicsWidget(metaclass=SingletonMeta):
    def __init__(self, app, update_vtk_fun):
        self._app = app
        self._object = None
        self._update_vtk_fun = update_vtk_fun
        self._all_widgets = {}
        self._graphics = ["Mesh", "Contour", "Vector", "Surface"]
        self.create_callback()

    def get_label(self, name):
        name_list = re.split("[^a-zA-Z]", name)
        return " ".join([name.capitalize() for name in name_list])

    def get_unique_name(self, name):
        return name + self._object.__class__.__name__

    def refresh(self, graphics_selector_value=None):

        return dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        dash_vtk.View(
                            id="vtk-view",
                            pickingModes=["hover"],
                            children=[],
                        ),
                        style={"height": "100%", "width": "100%"},
                    ),
                ),
                dbc.Col(
                    [
                        html.Div(
                            [
                                dbc.Label("Select Graphics"),
                                dcc.Dropdown(
                                    id="graphics-selector",
                                    options=self._graphics,
                                    value=graphics_selector_value,
                                ),
                            ],
                            style={
                                "padding": "1px 1px 10px 1px",
                                "width": "20rem",
                            },
                        ),
                    ]
                    + [
                        html.Div(
                            html.Div(id="graphics-card-body"),
                            className="mb-3",
                            style={
                                "padding": "1px 1px 10px 1px",
                                "width": "20rem",
                            },
                        )
                    ],
                    width="auto",
                ),
            ],
            style={"height": "50rem"},
        )

    def create_callback(self):
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
                            obj_type,
                            parent,
                            parent_visible and visible,
                            parent + "/" + name,                           
                            getattr(value, "attributes", None),
                        )
                        self._all_widgets[
                            self.get_unique_name(name)
                        ] = widget
                    else:
                        store_all_widgets(
                            obj_type,
                            value,
                            parent + "/" + name,
                            parent_visible and visible,
                        )

        def update_object(value, session_id=None):
            if value is not None:
                if value == "Contour":
                    self._object = graphics_session1.Contours[
                        "dummy-contour" + session_id if session_id else ""
                    ]
                if value == "Mesh":
                    self._object = graphics_session1.Meshes[
                        "dummy-mesh" + session_id if session_id else ""
                    ]
                if value == "Vector":
                    self._object = graphics_session1.Vectors[
                        "dummy-vector" + session_id if session_id else ""
                    ]
                if value == "Surface":
                    self._object = graphics_session1.Surfaces[
                        "dummy-surface" + session_id if session_id else ""
                    ]

        def update_stored_widgets(graphics_type, session_id=None):
            update_object(graphics_type, session_id)
            self._all_widgets = {}
            store_all_widgets(graphics_type, self._object)
            self._all_widgets[
                self.get_unique_name("display")
            ] = self.get_button("display", "display_button")

        @self._app.callback(
            Output("refresh-trigger", "value"),
            Input({"type": "graphics-widget", "index": ALL}, "value"),
            Input("session-id", "data"),
            State("graphics-selector", "value"),
        )
        def on_value_changed(
            values,
            session_id,
            graphics_selection,
        ):
            ctx = dash.callback_context
            prop_id = eval(ctx.triggered[0]["prop_id"].split(".")[0])["index"]
            prop_value = ctx.triggered[0]["value"]
            print("value_changed", prop_id, prop_value)
            update_object(graphics_selection, session_id)
            obj = self._object
            path_list = prop_id.split("/")[1:]
            for path in path_list:
                obj = getattr(obj, path)
                if obj is None:
                    raise PreventUpdate

            if isinstance(obj(), bool):
                prop_value = True if prop_value else False
            if prop_value == obj():
                print("PreventUpdate")
                raise PreventUpdate
            obj.set_state(prop_value)
            return str(prop_id) + str(prop_value)

        @self._app.callback(
            [
                Output("vtk-view", "children"),
                Output("vtk-view", "triggerResetCamera"),
            ],
            Input("display_button", "n_clicks"),
        )
        def on_button_click(n_clicks):
            print("n_clicks", self._object._name)
            if n_clicks == 0:
                raise PreventUpdate
            return self._update_vtk_fun(self._object)

        @self._app.callback(
            Output("graphics-card-body", "children"),
            Input("refresh-trigger", "value"),
            Input("session-id", "data"),
            Input("graphics-selector", "value"),
        )
        def refresh_widgets(_, session_id, graphics_selector):
            print("show hide", _, session_id, graphics_selector)
            if graphics_selector is None:
                raise PreventUpdate
            update_stored_widgets(graphics_selector, session_id)
            return list(self._all_widgets.values())

    def get_button(self, name, unique_name):
        return dbc.Button(self.get_label(name), id=unique_name, n_clicks=0)

    def get_widget(
        self,
        obj,
        type,
        name,
        obj_type,
        parent,
        visible,
        unique_name,
        attributes,
    ):
        if str(type) == "<class 'str'>":
            if attributes and "allowed_values" in attributes:
                widget = dcc.Dropdown(
                    id={"type": "graphics-widget", "index": unique_name},
                    options=getattr(obj, "allowed_values"),
                    value=obj(),
                )
            else:
                widget = dcc.Input(
                    id={"type": "graphics-widget", "index": unique_name},
                    type="text",
                    value=obj(),
                )
        elif str(type) == "typing.List[str]":
            widget = dcc.Dropdown(
                id={"type": "graphics-widget", "index": unique_name},
                options=getattr(obj, "allowed_values"),
                value=obj(),
                multi=True,
            )
            # print('widget', widget)
        elif str(type) == "<class 'bool'>":
            widget = dcc.Checklist(
                id={"type": "graphics-widget", "index": unique_name},
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
                    id={"type": "graphics-widget", "index": unique_name},
                    type="number",
                    value=obj(),
                    min=range[0] if range else None,
                    max=range[1] if range else None,
                )
            else:
                widget = dcc.Input(
                    id={"type": "graphics-widget", "index": unique_name},
                    type="number",
                    value=obj(),
                )
        elif str(type) == "<class 'int'>":
            if attributes and "range" in attributes:
                widget = dcc.Input(
                    id={"type": "graphics-widget", "index": unique_name},
                    type="number",
                    value=obj(),
                    min=getattr(obj, "range")[0],
                    max=getattr(obj, "range")[1],
                )
            else:
                widget = dcc.Input(
                    id={"type": "graphics-widget", "index": unique_name},
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
