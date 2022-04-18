from functools import partial
import dash_bootstrap_components as dbc
from dash import html
import dash_core_components as dcc                  
import dash_vtk 
from dash.dependencies import Input, Output, State




class GraphicsWidget:
    _fun = None
    _exe_method = None
    def __init__(self, app, obj, update_vtk_fun, vtk_view=None):
        self._app = app
        self._object = obj
        self._create_vtk_view = False
        self._vtk_view_id = "vtk-view-"+self._object._name
        if not vtk_view:
            self._create_vtk_view = True
            vtk_view = dash_vtk.View(
                id=self._vtk_view_id,    
                pickingModes=["hover"],
                children=[       
                ],
            )        
        self._vtk_view = vtk_view
        
        self._update_vtk_fun =  update_vtk_fun
        #self.refresh()       
        #self.__plotter_id = plotter_id
        #print(self.__object.__class__.__name__)
        #if self.__object.__class__.__name__=="XYPlot":
        #    self.__plotter = xyplotter  
        #else:
        #    self.__plotter = plotter
        #self.__plotter.set_graphics(obj, plotter_id)        
                       
   
    def update_widgets(self):
        self.__widgets=[]
        self.__refresh_bcs=[]
        self.populate_widgets(self._object)
        self.populate_buttons(self._object)
        
        
    def refresh(self):
        self.create_callback()
        self.update_widgets()        
        if self._create_vtk_view:
            return dbc.Row(
                                
             [
              dbc.Col(
                html.Div(
                html.Div(self._vtk_view, style={"height": "100%", "width": "100%"}),
                style={"height": "100%", "width": "100%"},
                ), md=10),        
                dbc.Col(dbc.Card(children = self.__widgets, body=True, id=f"{self._object._name}-container"), md=2),#
          
              ],
              style={"height": "50rem"},
            )        
        
        else:
            rv = dbc.Card(children = self.__widgets, body=True)
        #print(rv)
        return rv
        
    
    def _need_to_refresh(self):
        return not self.__compare_dicts(self.__old_defn, self._object())
        
    def __compare_dicts(self, old, new):
        for key, value in new.items():
          if not key in old:        
              return False
          if isinstance(value, dict):
              rv = self.__compare_dicts(old[key], value)          
              if not rv:
                  return False
        return True          
              
    def create_callback(self):

        inputs =[Input(name+self._object._name, "value") for name in ["field", "surfaces_list"]]   
        @self._app.callback(
          Output(f"{self._object._name}-container", "children"),                      
          *inputs                   
        )
        def update_oject2(*args): 
            print('update_oject2', args)              
            self.update_widgets()
            return [self.__widgets]            
        #    if self._need_to_refresh():
        #       pass
        #        #self.refresh()
        #    else:
        #        for cb in self.__refresh_bcs:
        #            cb()   
        #    return [1]               
        
    def populate_widgets(self, obj):        
        for name,value in obj.__dict__.items():       
            if name=="_parent":
                continue
            
            if value.__class__.__class__.__name__ in ("PyLocalPropertyMeta", "PyLocalObjectMeta"):
                availability = (
                    getattr(obj, "availability")(name)
                    if hasattr(obj, "availability")
                    else True
                )  
                if not availability:
                    continue
                #print(name, value, value.__class__.__class__.__name__)    
                if value.__class__.__class__.__name__ == "PyLocalPropertyMeta":
                    widget =  self.get_widget(value, value._type, name+self._object._name, getattr(value, "attributes", None) )
                    #if widget:
                    if isinstance(widget, list):
                        self.__widgets.extend(widget)
                    else:                    
                        self.__widgets.append(widget)
                else:
                    self.populate_widgets(value) 
                    
    def populate_buttons(self, obj):                         
        self.__widgets.append(self.get_button("refresh"+self._object._name))

                   
                   
                    
    def get_button(self, description):
                     
        button = html.Button(description, id=description,  n_clicks=0) 
        
        
        @self._app.callback( 
            [
                Output(self._vtk_view_id, "children"),
                Output(self._vtk_view_id, "triggerResetCamera"),
            ],            
            Input(description, "n_clicks"),                     
        )
        def fun(n_clicks):                    
            return self._update_vtk_fun(self._object)      
       
        return button        
    
    def get_widget(self, obj, type, description, attributes): 
        widget = None    
        #print(str(type), description)
        if str(type)=="<class 'str'>":
            if attributes and "allowed_values" in attributes:
                widget = dcc.Dropdown(
                    id=description,
                    options=getattr(obj, "allowed_values"),
                    value= obj()                    
                )                
            else:
                widget = dcc.Input(
                    id=description,
                    type="text",
                    value = obj()
                )
        elif str(type)=="typing.List[str]":
            widget = dcc.Dropdown(
                id=description,
                options=getattr(obj, "allowed_values"),
                value= obj(),
                multi=True
            )
            #print('widget', widget)            
        elif str(type)=="<class 'bool'>":    
            widget = dcc.Checklist(
               id=description,
               options={
                    'selected': description,                   
               },
               value=['selected'] if obj() else []
            )                    
        elif str(type)=="<class 'float'>":  
            if attributes and "range" in attributes:
                widget = dcc.Input(
                    id=description,
                    type="number",
                    value = obj(),
                    min = getattr(obj, "range")[0],
                    max = getattr(obj, "range")[1],
                )                            
            else:
                widget = dcc.Input(
                    id=description,
                    type="number",
                    value = obj()
                )                
        elif str(type)=="<class 'int'>":  
            if attributes and "range" in attributes:          
                widget = dcc.Input(
                    id=description,
                    type="number",
                    value = obj(),
                    min = getattr(obj, "range")[0],
                    max = getattr(obj, "range")[1],
                )                
            else:
                widget = dcc.Input(
                    id=description,
                    type="number",
                    value = obj()
                ) 
                
        #if not widget:
        #    print('return', widget)
        #    return 
            
        @self._app.callback(         
          Output("scale-factor", description),            
          Input(description, "value"),                     
        )
        def update_oject(value): 
            print('update_oject', description, value)
            self.__old_defn = self._object()   
            if str(type)=="<class 'bool'>": 
               obj.set_state(True if value else False)      
            else:            
                obj.set_state(value)  
        #    self.update_widgets()
        #    return [self.__widgets]            
        #    if self._need_to_refresh():
        #       pass
        #        #self.refresh()
        #    else:
        #        for cb in self.__refresh_bcs:
        #            cb()   
            return [1]        
                                       
        def refresh_bc(widget, obj):
            widget.value = obj()
        w=widget    
                  
        self.__refresh_bcs.append(partial(refresh_bc, w, obj))            
        return html.Div(
            [
                description,
                widget
            ]
        )        
        
        return widget    
                        
        
   
        
               