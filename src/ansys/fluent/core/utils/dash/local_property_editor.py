import re 

from dash import dcc, html
import dash_bootstrap_components as dbc

from property_editor import PropertyEditor
from objects_handle import LocalObjectsHandle
from sessions_manager import SessionsManager

class LocalPropertyEditor(PropertyEditor):
    def __init__(self, user_id, session_id, index=None):
        super().__init__(user_id, session_id, "local", index)
        self._all_widgets = {}        
        self._graphics_property_editor = GraphicsPropertyEditor()
        self._plot_property_editor = PlotPropertyEditor()
        self._get_objects_handle = LocalObjectsHandle(SessionsManager)

    def _get_editor(self, object_type):
        return (
            self._graphics_property_editor
            if self._get_objects_handle.get_handle_type(object_type)=="graphics"
            else self._plot_property_editor
        )
       

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
                            f"{parent}/{name}:{self._user_id}:{self._session_id}:local:{object_type}:{object_index}",
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

        obj = self._get_objects_handle._get_object(
            connection_id, session_id, object_type, object_index
        )
        

        if widget_type == "input":
            self._all_widgets = {}
            store_all_widgets(object_type, obj)
            return self._all_widgets
        else:
            return self._get_editor(object_type).get_widgets(
                connection_id, session_id, object_type, object_index, self._index
            )

        

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


    def get_widgets(self, connection_id, session_id, object_type, object_index, editor_index):
        return (
            {
                "display-button": dbc.Button(
                    "Display", 
                    id={
                        "type": "post-render-button",
                        "index": f"{connection_id}:{session_id}:local:{object_type}:{object_index}:{editor_index}",
                    },                                                           
                    n_clicks=0, 
                    size="sm"
                ),
                "delete-button": dbc.Button(
                    "Delete", 
                    id={
                        "type": "graphics-button",
                        "index": f"{connection_id}:{session_id}:local:{object_type}:{object_index}:delete:{editor_index}",
                    },                                      
                    n_clicks=0, 
                    size="sm"
                ),
            }
            if object_index
            else {
                "display-button": dbc.Button(
                    "Display", 
                    id={
                        "type": "post-render-button",
                        "index": f"{connection_id}:{session_id}:local:{object_type}:{object_index}:{editor_index}",
                    },                   
                    n_clicks=0, 
                    size="sm"
                ),
                "new-button": dbc.Button(
                    "New", 
                    id={
                        "type": "graphics-button",
                        "index": f"{connection_id}:{session_id}:local:{object_type}:{object_index}:new:{editor_index}",
                    },
                    n_clicks=0, size="sm"
                ),
            }
        )



class PlotPropertyEditor:

    def get_widgets(self, connection_id, session_id, object_type, object_index, editor_index):
        return (
            {
                "plot-button": dbc.Button(
                    "Plot", 
                    id={
                        "type": "post-render-button",
                        "index": f"{connection_id}:{session_id}:local:{object_type}:{object_index}:{editor_index}",
                    },                                                           
                    n_clicks=0, 
                    size="sm"
                ),
                "delete-button": dbc.Button(
                    "Delete", 
                    id={
                        "type": "graphics-button",
                        "index": f"{connection_id}:{session_id}:local:{object_type}:{object_index}:delete:{editor_index}",
                    },                                      
                    n_clicks=0, 
                    size="sm"
                ),
            }
            if object_index
            else {
                "plot-button": dbc.Button(
                    "Plot", 
                    id={
                        "type": "post-render-button",
                        "index": f"{connection_id}:{session_id}:local:{object_type}:{object_index}:{editor_index}",
                    },                   
                    n_clicks=0, 
                    size="sm"
                ),
                "new-button": dbc.Button(
                    "New", 
                    id={
                        "type": "graphics-button",
                        "index": f"{connection_id}:{session_id}:local:{object_type}:{object_index}:new:{editor_index}",
                    },
                    n_clicks=0, size="sm"
                ),
            }
        )    

