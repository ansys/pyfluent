from functools import partial
import dash_bootstrap_components as dbc
from dash import html
import dash_core_components as dcc                  
import dash_vtk 
from dash.dependencies import Input, Output, State

from dash.exceptions import PreventUpdate


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
        self._all_widgets = {}        
        self.__refresh_bcs=[] 
        self._update_vtk_fun =  update_vtk_fun
        self.store_all_widgets(self._object)   
        self._all_widgets["display"+self._object._name]= self.get_button("display"+self._object._name)               
   
    def update_widgets(self):
        self.__widgets=[]   
        self.populate_widgets(self._object)
        self.__widgets.append(self.get_button("display"+self._object._name))  
        
        
    def refresh(self):
        print(list(self._all_widgets.keys())[:-1])
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

        inputs =[Input(name+"data", "value") for name in list(self._all_widgets.keys())[:-1]] 
        outputs =[Output(name+"container", "style") for name in list(self._all_widgets.keys())[:-1]] 
        outputs =outputs + [Output(name, "value") for name in list(self._all_widgets.keys())[:-1]] 
        #inputs =[Input(name, "value") for name in ['fieldcontour-1', 'surfaces_listcontour-1',]]        
        @self._app.callback(
          #Output(f"{self._object._name}-container", "children"), 
          *outputs,          
          *inputs                   
        )
        def update_oject2(*args): 

            #for cb in self.__refresh_bcs:
            #    cb()
            print('update_oject2')                                 
            #if self._need_to_refresh():
            self._visible_widgets = []
            self.visible_widgets(self._object)
            visible_widgets = [pair[0] for pair in self._visible_widgets]
            widgets_value_map = {pair[0]:pair[1] for pair in self._visible_widgets}
            widget_values = []
            for value in [widgets_value_map[name] if name in  visible_widgets else None for name in list(self._all_widgets.keys())[:-1]]:
                if isinstance(value, bool):
                    widget_values.append(['selected'] if value else [])
                else:
                    widget_values.append(value)
            
            return ([{'display': 'block'} if name in  visible_widgets else {'display': 'none'} for name in list(self._all_widgets.keys())[:-1]] +  
                  widget_values)
                                     
            #else:
            #   print('PreventUpdate...') 
            #   raise PreventUpdate
               
        def update_oject2(*args): 
            print('update_oject2')                                 
            if self._need_to_refresh():
               self.update_widgets() 
               print('update_widgets...')               
               #return []
               return [self.__widgets] 
            else:
               print('PreventUpdate...') 
               raise PreventUpdate               
             
        

    def store_all_widgets(self, obj):        
        for name,value in obj.__dict__.items():       
            if name=="_parent":
                continue
            
            if value.__class__.__class__.__name__ in ("PyLocalPropertyMeta", "PyLocalObjectMeta"):               
                if value.__class__.__class__.__name__ == "PyLocalPropertyMeta":
                    widget =  self.get_widget(value, value._type, name+self._object._name, getattr(value, "attributes", None) )
                    #if widget:
                    if isinstance(widget, list):
                        self._all_widgets[name+self._object._name]=widget
                    else:                    
                        self._all_widgets[name+self._object._name]=widget
                else:
                    self.store_all_widgets(value)
                   
                    
    def populate_widgets(self, obj):              
        for name,value in obj.__dict__.items():       
            if name=="_parent":
                continue
            
            if value.__class__.__class__.__name__ in ("PyLocalPropertyMeta", "PyLocalObjectMeta"):
                availability = (
                    getattr(obj, "_availability")(name)
                    if hasattr(obj, "_availability")
                    else True
                )  
                #if not availability:
                #    continue
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
                    
                    
    def visible_widgets(self, obj):              
        for name,value in obj.__dict__.items():       
            if name=="_parent":
                continue
            
            if value.__class__.__class__.__name__ in ("PyLocalPropertyMeta", "PyLocalObjectMeta"):
                availability = (
                    getattr(obj, "_availability")(name)
                    if hasattr(obj, "_availability")
                    else True
                )  
                if not availability:
                    continue
                #print(name, value, value.__class__.__class__.__name__)    
                if value.__class__.__class__.__name__ == "PyLocalPropertyMeta":
                   
                    self._visible_widgets.append((name+self._object._name, value()))
                else:
                    self.visible_widgets(value)                     
                   
                         
        

                   
                   
                    
    def get_button(self, description):
        widget = self._all_widgets.get(description) 
        if widget is not None:            
            return widget    
                     
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
        widget = self._all_widgets.get(description) 
        if widget is not None:            
            return widget        
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
          Output(description+"data", "value"),            
          Input(description, "value"),                     
        )
        def update_oject(value): 
            print('update_oject', description, value)
            self.__old_defn = self._object()   
            if str(type)=="<class 'bool'>": 
               value =True if value else False
               obj.set_state(value)      
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
            return str(value)        
                                       
        def refresh_bc(widget, obj):
            print('refresh_bc', description, obj())           
            if str(type)=="<class 'bool'>":                
                widget.value = ["selected"] if obj() else []      
            else:            
                widget.value = obj()         
            
        w=widget    
                  
        self.__refresh_bcs.append(partial(refresh_bc, w, obj))            
        widget = html.Div(
            [
                description,
                widget,
                html.Data(id = description+"data")
            ],
            id = description+"container"
        )                  
        return widget    
                        
        
   
        
               