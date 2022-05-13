import dash_bootstrap_components as dbc
from dash import Input, Output, State, ALL
from dash import html
import itertools
from dash.exceptions import PreventUpdate
from app_defn import app
import re
class PropertyEditor:

    _id_iter = itertools.count()

    def __init__(self):
        self._id = next(PropertyEditor._id_iter)
        self._object_id = None
        self._filter_list = []

        @app.callback(
            Output(f"property-editor-{self._id}", "children"),
            Input("object-id", "value"),
            Input("connection-id", "data"),
            State("session-id", "value"),
            prevent_initial_call=True,
        )
        def refresh_widgets(object_id, connection_id, session_id):
            if object_id != self._object_id:
                raise PreventUpdate
            object_location, object_type, object_index = object_id.split(":")
            return self.render(connection_id, session_id, object_id)

    def __call__(self, user_id, session_id, object_id, filter_list=[]):
        self._object_id = object_id
        self._filter_list = filter_list       
        return html.Div(
            children=self.render(user_id, session_id, object_id),
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
