import dash_bootstrap_components as dbc
from dash import Input, Output, State, ALL
from dash import html
import itertools
from dash.exceptions import PreventUpdate
from app_defn import app
import re
class PropertyEditor:


    _editors = {}
    def __init__(self, user_id, session_id, editor_type, index):
        unique_id = f"{user_id}-{session_id}-{editor_type}-{'default' if index is None else index}"
        editor = PropertyEditor._editors.get(unique_id)
        if not editor:
            PropertyEditor._editors[unique_id] = self.__dict__    
            self._id = unique_id
            self._user_id =   user_id
            self._session_id = session_id          
            self._object_id = None
            self._filter_list = [] 
            self._index =  index           

            @app.callback(
                Output(f"property-editor-{self._id}", "children"),
                Input("object-id", "value"),           
                prevent_initial_call=True,
            )
            def refresh_widgets(object_id):
                if object_id != self._object_id:
                    raise PreventUpdate            
                return self.render(self._user_id, self._session_id , object_id)
        else:
            self.__dict__ = editor         

    def __call__(self, object_id, filter_list=[]):
        self._object_id = object_id
        self._filter_list = filter_list              
        return html.Div(
            children=self.render(self._user_id, self._session_id, self._object_id),
            id=f"property-editor-{self._id}",
        )
        
    def get_label(self, name):
        name_list = re.split("[^a-zA-Z]", name)
        return " ".join([name.capitalize() for name in name_list])        

    def render(self, user_id, session_id, object_id):
        object_location, object_type, object_index = object_id.split(":")
        all_input_widgets = self.get_widgets(
            user_id, session_id, object_type, object_index, "input"
        )
        all_command_widgets = self.get_widgets(
            user_id, session_id, object_type, object_index, "command"
        )
        object_type = object_type.split("/")[-1]
        object_name = object_type + "-" + object_index if object_index else object_type
        object_name = object_name.capitalize()        
        return (
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                object_name,
                            ),
                            dbc.CardBody(
                                [
                                    v
                                    for k, v in all_input_widgets.items()
                                    if not self._filter_list or k in self._filter_list
                                ]
                            ),                            
                            html.Div(
                                [
                                    v
                                    for k, v in all_command_widgets.items()
                                    if not self._filter_list
                                    or k.split(":")[0] in self._filter_list
                                ],                               
                                className="d-grid gap-1",
                                style={"padding": "4px 4px 4px 4px"},
                            ),
                        ],
                    ),
                ]
            ),
        )
