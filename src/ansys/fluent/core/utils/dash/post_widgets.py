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
from ansys.fluent.post.matplotlib import  Plots
from ansys.fluent.post.pyvista.pyvista_objects import (
    Contour,
    Mesh,
    Surface,
    Vector,
)
from ansys.fluent.post import set_config
from post_data import update_vtk_fun, update_graph_fun
set_config(blocking=False)



class PostWidget():

    def __init__(self, app, wind_id, SessionsManager):
        self._app = app
        self._wind_id = wind_id
        self._graphics_selector_value =None
        self._all_widgets = {}   
        self.SessionsManager = SessionsManager        
        self.create_callback()
        

    def get_label(self, name):
        name_list = re.split("[^a-zA-Z]", name)
        return " ".join([name.capitalize() for name in name_list])

    def get_unique_name(self, name):
        return name 

    def update_object(self, graphics_selector, connection_id, session_id, object_id=None):
        self._graphics_selector_value = graphics_selector
        if graphics_selector is not None:            
            session =  self.SessionsManager(self._app, connection_id, session_id).session
            graphics_session = Graphics(session)
            plots_session = Plots(session)        
            if graphics_selector == "Contour":
                return graphics_session.Contours[
                    f"contour-{connection_id}-{session_id}-{object_id if object_id else 'dummy'}" 
                ]
            if graphics_selector == "Mesh":
                return  graphics_session.Meshes[
                    f"mesh-{connection_id}-{session_id}-{object_id if object_id else 'dummy'}" 
                ]
            if graphics_selector == "Vector":
                return graphics_session.Vectors[
                    f"vector-{connection_id}-{session_id}-{object_id if object_id else 'dummy'}"
                ]
            if graphics_selector == "Surface":
                return graphics_session.Surfaces[
                    f"surface-{connection_id}-{session_id}-{object_id if object_id else 'dummy'}"
                ]
            if graphics_selector == "XYPlot":
                return plots_session.XYPlots[
                    f"xyplot-{connection_id}-{session_id}-{object_id if object_id else 'dummy'}"                    
                ]

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


        def update_stored_widgets(graphics_type, connection_id, session_id):
            obj = self.update_object(graphics_type, connection_id, session_id)
            self._all_widgets = {}
            store_all_widgets(graphics_type, obj)
            self._all_widgets[
                self.get_unique_name("display")
            ] = self.get_button("display", "display_button")

        @self._app.callback(
            Output(f"refresh-trigger-{self._wind_id}", "value"),
            Input({"type": f"graphics-widget-{self._wind_id}", "index": ALL}, "value"),
            Input("connection-id", "data"),
            State("session-id", "data"),
            State(f"graphics-selector-{self._wind_id}", "value"),
        )
        def on_value_changed(
            values,
            connection_id,
            session_id,
            graphics_selection,
        ):
            ctx = dash.callback_context
            prop_value = ctx.triggered[0]["value"]
            if prop_value is None:
                raise PreventUpdate
            prop_id = eval(ctx.triggered[0]["prop_id"].split(".")[0])["index"]
            
            print("value_changed", prop_id, prop_value)
            obj = self.update_object(graphics_selection, connection_id, session_id)            
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
            Output(f"graphics-card-body-{self._wind_id}", "children"),
            Input(f"refresh-trigger-{self._wind_id}", "value"),
            Input("connection-id", "data"),            
            Input(f"graphics-selector-{self._wind_id}", "value"),
            State("session-id", "data"),
        )
        def refresh_widgets(_, connection_id, graphics_selector, session_id):
            print("show hide", _, connection_id, session_id, graphics_selector)
            if graphics_selector is None or session_id is None:
                raise PreventUpdate
            update_stored_widgets(graphics_selector, connection_id, session_id)
            return list(self._all_widgets.values())

    def get_button(self, name, unique_name):
        return dbc.Button(self.get_label(name), id=f"{unique_name}-{self._wind_id}", n_clicks=0)

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
        widget = html.Div(f"Widget not found for {name}.")
        if str(type) == "<class 'str'>":
            if attributes and "allowed_values" in attributes:
                widget = dcc.Dropdown(
                    id={"type": f"graphics-widget-{self._wind_id}", "index": unique_name},
                    options=getattr(obj, "allowed_values"),
                    value=obj(),
                )
            else:
                widget = dcc.Input(
                    id={"type": f"graphics-widget-{self._wind_id}", "index": unique_name},
                    type="text",
                    value=obj(),
                )
        elif str(type) == "typing.List[str]":
            widget = dcc.Dropdown(
                id={"type": f"graphics-widget-{self._wind_id}", "index": unique_name},
                options=getattr(obj, "allowed_values"),
                value=obj(),
                multi=True,
            )
            # print('widget', widget)
        elif str(type) == "<class 'bool'>":
            widget = dcc.Checklist(
                id={"type": f"graphics-widget-{self._wind_id}", "index": unique_name},
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
                    id={"type": f"graphics-widget-{self._wind_id}", "index": unique_name},
                    type="number",
                    value=obj(),
                    min=range[0] if range else None,
                    max=range[1] if range else None,
                )
            else:
                widget = dcc.Input(
                    id={"type": f"graphics-widget-{self._wind_id}", "index": unique_name},
                    type="number",
                    value=obj(),
                )
        elif str(type) == "<class 'int'>":
            if attributes and "range" in attributes:
                widget = dcc.Input(
                    id={"type": f"graphics-widget-{self._wind_id}", "index": unique_name},
                    type="number",
                    value=obj(),
                    min=getattr(obj, "range")[0],
                    max=getattr(obj, "range")[1],
                )
            else:
                widget = dcc.Input(
                    id={"type": f"graphics-widget-{self._wind_id}", "index": unique_name},
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


        session_state = Graphics._sessions_state.get(
            session.id if session else 1
        )
        if not session_state:
            session_state = self.__dict__
            Graphics._sessions_state[
                session.id if session else 1
            ] = session_state
            self.session = session
            self._init_module(self, sys.modules[__name__])
        else:
            self.__dict__ = session_state

class GraphicsWidget(PostWidget):

    _windows_state = {}
    def __init__(self, app, connection_id, session_id, wind_id, SessionsManager):
        wind_id = f"graphics-win-{wind_id}-{session_id}-{connection_id}"
        window_state = GraphicsWidget._windows_state.get(
            wind_id
        )           
        if not window_state:  
            GraphicsWidget._windows_state[
                wind_id
            ] = self.__dict__
            
            self._post_objects = ["Mesh", "Contour", "Vector", "Surface"]
            super().__init__(app, wind_id, SessionsManager)
            self._vtk_children  = []

            @self._app.callback(
                [
                    Output(f"vtk-view-{self._wind_id}", "children"),
                    Output(f"vtk-view-{self._wind_id}", "triggerResetCamera"),
                ],
                Input(f"display_button-{self._wind_id}", "n_clicks"),
                Input("connection-id", "data"),
                State("session-id", "data"),
                State(f"graphics-selector-{self._wind_id}", "value"),            
            )
            def on_button_click(n_clicks, connection_id, session_id, graphics_type):
                obj = self.update_object(graphics_type, connection_id, session_id)
                print("n_clicks", obj._name)
                if n_clicks == 0:
                    raise PreventUpdate
                vtk_rendering = update_vtk_fun(obj)  
                self._vtk_children =  vtk_rendering[0]           
                return vtk_rendering 
        else:
            self.__dict__ = window_state                
        
    def layout(self):

        return dbc.Row(
            [
                dbc.Col(
                    [html.Data(id=f"refresh-trigger-{self._wind_id}"),
                    html.Div(
                        dash_vtk.View(
                            id=f"vtk-view-{self._wind_id}",
                            pickingModes=["hover"],
                            children=self._vtk_children,
                        ),
                        style={"height": "100%", "width": "100%"},
                    )],
                ),
                dbc.Col(
                    [
                        html.Div(
                            [
                                dbc.Label("Select Graphics"),
                                dcc.Dropdown(
                                    id=f"graphics-selector-{self._wind_id}",
                                    options=self._post_objects,
                                    value=self._graphics_selector_value,
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
                            html.Div(id=f"graphics-card-body-{self._wind_id}",
                            children = list(self._all_widgets.values())
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
            ],
            style={"height": "50rem"},
        )        
       
class PlotWidget(PostWidget):

    _windows_state = {}
    def __init__(self, app, connection_id, session_id, wind_id, SessionsManager):
        wind_id = f"plot-win-{wind_id}-{session_id}-{connection_id}"
        window_state = PlotWidget._windows_state.get(
            wind_id
        )           
        if not window_state:  
            PlotWidget._windows_state[
                wind_id
            ] = self.__dict__
            
            self._post_objects = ["XYPlot"]
            super().__init__(app, wind_id, SessionsManager)
            self._figure  = {}


            @self._app.callback(            
                Output(f"plot-viewer-{self._wind_id}", "figure"), 
                Input(f"display_button-{self._wind_id}", "n_clicks"),
                Input("connection-id", "data"),
                State("session-id", "data"),
                State(f"graphics-selector-{self._wind_id}", "value"),                         
            )
            def on_button_click(n_clicks, connection_id, session_id, graphics_type):
                obj = self.update_object(graphics_type, connection_id, session_id)
                print("n_clicks", obj._name)
                if n_clicks == 0:
                    raise PreventUpdate
                self._figure = update_graph_fun(obj)                           
                return self._figure                                         
        else:
            self.__dict__ = window_state                
        
    def layout(self):
        return dbc.Row(
            [
                dbc.Col(
                    [html.Data(id=f"refresh-trigger-{self._wind_id}"),
                    dcc.Graph(
                        id = f"plot-viewer-{self._wind_id}",
                        figure = self._figure, 
                        style ={"height":900}
                    ) ]                 

                ),
                dbc.Col(
                    [
                        html.Div(
                            [
                                dbc.Label("Select Graphics"),
                                dcc.Dropdown(
                                    id=f"graphics-selector-{self._wind_id}",
                                    options=self._post_objects,
                                    value=self._graphics_selector_value,
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
                            html.Div(id=f"graphics-card-body-{self._wind_id}",
                            children = list(self._all_widgets.values())
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
            ],
            style={"height": "50rem"},
        )       