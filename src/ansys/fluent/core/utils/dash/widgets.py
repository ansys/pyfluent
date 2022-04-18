from functools import partial
import dash_bootstrap_components as dbc
from dash import html
import dash_core_components as dcc
import dash_vtk
from dash.dependencies import Input, Output, State

from dash.exceptions import PreventUpdate
import re
from ansys.fluent.core.utils.generic import SingletonMeta
from ansys.fluent.post.pyvista import  Graphics
from ansys.fluent.post.pyvista.pyvista_objects import Contour, Mesh, Surface, Vector
from ansys.fluent.post import set_config
from ansys.fluent.core.session  import Session
session =Session.create_from_server_info_file("E:\\ajain\\Demo\\pyApp\\pyvista\\server.txt", False)
set_config(blocking=False)
graphics_session1 = Graphics(session)
import uuid
#contour1 = graphics_session1.Contours["contour-1"]
#contour1.field = "velocity-magnitude"
#contour1.surfaces_list = ["symmetry"]
#contour1.node_values = False

#contour2 = graphics_session1.Contours["contour-2"]
#contour2.field = "temperature"
#contour2.surfaces_list = ["wall"]


class GraphicsWidget(metaclass=SingletonMeta):

    def __init__(self, app, update_vtk_fun):
        self._app = app
        self._object = None
        self._vtk_view_id = "vtk-view"
        self._vtk_view = dash_vtk.View(
            id=self._vtk_view_id,
            pickingModes=["hover"],
            children=[],
        )        
        self._widget_value_map = {}
        self._update_vtk_fun = update_vtk_fun
        self._all_widgets = {}
        self._graphics = ["Contour", "Surface", "Mesh", "Vector"]
        self._button_widget = None 
        self.create_callback()

    def get_label(self, name):
        name_list = re.split("[^a-zA-Z]", name)
        return " ".join([name.capitalize() for name in name_list])

    def get_unique_name(self, name):
        return name + self._object.__class__.__name__

    def refresh(self):

        return dbc.Row(
            [
                dbc.Col(
                  
                        html.Div(
                            self._vtk_view,
                            style={"height": "100%", "width": "100%"},
                        ),
                        
                   
                    md=9,
                ),
                dbc.Col(
                    [
                    html.Div(
                        [
                            dbc.Label("Select Graphics"),
                            dcc.Dropdown(
                                id="graphics-selector",
                                options=["Contour", "Vector",  "Surface"],
                               
                                
                            ),
                            #html.Data(id="graphics-selectordata"),
                        ],                
                        id="graphics-selector" + "container",
                        style = {'padding': "1px 1px 10px 1px"},  
                    ),
                    ]+
                    [
                    
                      dbc.Card(
                          [
                              #dbc.CardHeader(id=f"{graphics_type}-graphics-card-header"),
                              dbc.CardBody(list(self._all_widgets[graphics_type].values()), id=f"{graphics_type}-graphics-card-body"),
                          ],
                          body=True,
                          className="mb-3",
                          id=f"{graphics_type}-graphics-card"
                      )
                      
                      for graphics_type in self._graphics
                    ],
                    md=2,
                ),
            ],
            style={"height": "50rem"},
        )

    def update_object(self, value, session_id=None):
        if value is not None:
            if value=="Contour":
                self._object = graphics_session1.Contours["dummy-contour"+session_id if session_id else ""]
            if value=="Mesh":
                self._object = graphics_session1.Meshes["dummy-mesh"+session_id if session_id else ""] 
            if value=="Vector":
                self._object = graphics_session1.Vectors["dummy-vector"+session_id if session_id else ""] 
            if value=="Surface":
                self._object = graphics_session1.Surfaces["dummy-surface"+session_id if session_id else ""] 
                    
    def create_callback(self):
                   
    
        def update_stored_widgets(value):
            if value is not None:
                self.update_object(value)
                self._all_widgets[value] ={}
                self.store_all_widgets(value, self._object)
                self._all_widgets[value][self.get_unique_name("display")] =self.get_button(
                    "display", self.get_unique_name("display")
                )
                
        for value in self._graphics:
            update_stored_widgets(value)                 

        @self._app.callback(
            [Output(f"{graphics_type}-graphics-card", "style")  for graphics_type in self._graphics],
            Input("graphics-selector", "value"),
            Input('session-id', 'data')
        )
        def show_graphics_object(value, session_id):
            self.update_object(value, session_id)
            return [
                {"display": "block"}
                if graphics_type==value
                else {"display": "none"}
                for graphics_type in self._graphics
            ] 
            
        print([list(self._all_widgets[graphics_type].keys())[-1]  for graphics_type in self._graphics])    
        @self._app.callback(
            [
                Output("vtk-view", "children"),
                Output("vtk-view", "triggerResetCamera"),
            ],
            [Input(list(self._all_widgets[graphics_type].keys())[-1], "n_clicks")  for graphics_type in self._graphics],
        )
        def display_graphics(*args):
            print("n_clicks", args, self._object._name)
            return self._update_vtk_fun(self._object)            
        
        for value in self._graphics:
              
            #print("all widgets", self._all_widgets.keys())
            inputs = [
                Input(name + "data", "value")
                for name in list(self._all_widgets[value].keys())[:-1]
            ]            
            inputs.append(Input('session-id', 'data'))
            inputs.append(State("graphics-selector", "value"))
            
            outputs = [
                Output(name + "container", "style")
                for name in list(self._all_widgets[value].keys())[:-1]
            ]
            outputs = outputs + [
                Output(name, "value")
                for name in list(self._all_widgets[value].keys())[:-1]
            ]

            @self._app.callback(*outputs, *inputs)
            def callback(*args): 
                nonlocal value
                callback_type = lambda : value 
                value = args[-1]
                session_id = args[-2]
                    
                if value is None or callback_type() != value:
                    raise PreventUpdate    
                self.update_object(value, session_id)
                if self._object is None:
                    raise PreventUpdate
                print('show hide callback', callback_type(), value, session_id, self._object._name)
                self._visible_widgets = []
                self.update_visible_widgets(self._object)
                visible_widgets = [pair[0] for pair in self._visible_widgets]
                widgets_value_map = {
                    pair[0]: pair[1] for pair in self._visible_widgets
                }
                widget_values = []
                for widget_value in [
                    widgets_value_map[name] if name in visible_widgets else self._widget_value_map[name]
                    for name in list(self._all_widgets[value].keys())[:-1]
                ]:
                    if isinstance(widget_value, bool):
                        widget_values.append(["selected"] if widget_value else [])
                    else:
                        widget_values.append(widget_value)
                return [
                    {"display": "block"}
                    if name in visible_widgets
                    else {"display": "none"}
                    for name in list(self._all_widgets[value].keys())[:-1]
                ] + widget_values
        
           


            

                       

    def store_all_widgets(self, obj_type, obj, parent="" , parent_visible=True):
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
                
                if value.__class__.__class__.__name__ == "PyLocalPropertyMeta":
                    widget = self.get_widget(
                        value,
                        value._type,
                        name,
                        obj_type,
                        parent,
                        parent_visible and visible,
                        self.get_unique_name(name),
                        getattr(value, "attributes", None),
                    )
                    self._all_widgets[obj_type][self.get_unique_name(name)] = widget
                else:
                    self.store_all_widgets(obj_type, value, parent+"/"+name, parent_visible and visible)

    def update_visible_widgets(self, obj):
        for name, value in obj.__dict__.items():
            if name == "_parent":
                continue

            if value.__class__.__class__.__name__ in (
                "PyLocalPropertyMeta",
                "PyLocalObjectMeta",
            ):
                availability = (
                    getattr(obj, "_availability")(name)
                    if hasattr(obj, "_availability")
                    else True
                )
                if not availability:
                    continue
                # print(name, value, value.__class__.__class__.__name__)
                if value.__class__.__class__.__name__ == "PyLocalPropertyMeta":

                    self._visible_widgets.append(
                        (self.get_unique_name(name), value() if value._type != "<class 'bool'>" else ['selected'] if value() else [])
                    )
                else:
                    self.update_visible_widgets(value)

    def get_button(self, name, unique_name):        

        self._button_widget = dbc.Button(self.get_label(name), id=unique_name, n_clicks=0)
        #@self._app.callback(
        #    [
        #        Output("vtk-view", "children"),
        #        Output("vtk-view", "triggerResetCamera"),
        #    ],
        #    Input("display", "n_clicks"),
        #)
        def fun(n_clicks):
            print("n_clicks", n_clicks, self._object._name)
            return self._update_vtk_fun(self._object)


        return self._button_widget

    def get_widget(self, obj, type, name, obj_type, parent, visible, unique_name, attributes):
        widget = self._all_widgets.get(obj_type,{}).get(unique_name)
        if widget is not None:
            return widget
        # print(str(type), unique_name)
        if str(type) == "<class 'str'>":
            if attributes and "allowed_values" in attributes:
                widget = dcc.Dropdown(
                    id=unique_name,
                    options=getattr(obj, "allowed_values"),
                    value=obj(),
                )
            else:
                widget = dcc.Input(id=unique_name, type="text", value=obj())
        elif str(type) == "typing.List[str]":
            widget = dcc.Dropdown(
                id=unique_name,
                options=getattr(obj, "allowed_values"),
                value=obj(),
                multi=True,
            )
            # print('widget', widget)
        elif str(type) == "<class 'bool'>":
            widget = dcc.Checklist(
                id=unique_name,
                options={
                    "selected": self.get_label(name),
                },
                value=["selected"] if obj() else [],
                style = {'padding': "5px"},
                labelStyle = {"display": "inline-block"},
                inputStyle = {'padding': "1px 1px 1px 5px"},
            )
        elif str(type) == "<class 'float'>":
            if attributes and "range" in attributes:
                range  = getattr(obj, "range")
                widget = dcc.Input(
                    id=unique_name,
                    type="number",
                    value=obj(),
                    min=range[0] if range else None,
                    max=range[1] if range else None,
                )
            else:
                widget = dcc.Input(id=unique_name, type="number", value=obj())
        elif str(type) == "<class 'int'>":
            if attributes and "range" in attributes:
                widget = dcc.Input(
                    id=unique_name,
                    type="number",
                    value=obj(),
                    min=getattr(obj, "range")[0],
                    max=getattr(obj, "range")[1],
                )
            else:
                widget = dcc.Input(id=unique_name, type="number", value=obj())

        # if not widget:
        #    print('return', widget)
        #    return

        @self._app.callback(
            Output(unique_name + "data", "value"),
            Input(unique_name, "value"),
            Input("session-id", "data"),
            State("graphics-selector", "value"),
        )
        def update_oject(value, session_id, graphics_selection):
            if graphics_selection != obj_type:
                raise PreventUpdate    
            print("update_oject", session_id, graphics_selection, unique_name, value)
            self.update_object(graphics_selection, session_id)
            obj = self._object
            path_list = parent.split("/")
            if len(path_list)>1:
                path_list = path_list[1:]
                for path in  path_list:
                    obj = getattr(obj, path)
                    if obj is None:
                        raise PreventUpdate                    
            obj = getattr(obj, name)                    
            if obj is None:
                raise PreventUpdate               
            #self.__old_defn = self._object()
            if value is None or value == obj():
                #print('PreventUpdate')
                raise PreventUpdate
                
            if str(type) == "<class 'bool'>":
                value = True if value else False
                if value == obj():
                    #print('PreventUpdate')
                    raise PreventUpdate
                obj.set_state(value)
                self._widget_value_map[unique_name]= ['selected'] if value else []
            else:
                self._widget_value_map[unique_name]= value
                obj.set_state(value)
            return str(value)




        
        
        
        if str(type) == "<class 'bool'>":
            self._widget_value_map[unique_name]=["selected"] if obj() else []
            widget = html.Div(
                
                [widget, html.Data(id=unique_name + "data")],
                id=unique_name + "container",
                style = {"display":"block"} if visible else {"display":"none"}
            )
        else:
            self._widget_value_map[unique_name]= obj()
            widget = html.Div(
                [
                    dbc.Label(self.get_label(name)),
                    widget,
                    html.Data(id=unique_name + "data"),
                ],
                id=unique_name + "container",
                style = {"display":"block"} if visible else {"display":"none"}
            )    
        return widget

