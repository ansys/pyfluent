import dash_bootstrap_components as dbc
from dash import Input, Output, State, ALL
from dash import html
import itertools
from dash.exceptions import PreventUpdate


class PropertyEditor:

    _id_iter = itertools.count()

    def __init__(self, app):
        self._app = app
        self._id = next(PropertyEditor._id_iter)
        self._object_id = None
        self._filter_list = []

        @app.callback(
            Output(f"property-editor-{self._id}", "children"),
            Input("refresh-property-editor", "value"),
            Input("connection-id", "data"),
            State("session-id", "value"),
            prevent_initial_call=True,
        )
        def refresh_widgets(object_id, connection_id, session_id):
            if object_id != self._object_id:
                raise PreventUpdate
            print(
                "\nrefresh_widg ets",
                f"property-editor-{self._id}",
                connection_id,
                object_id,
                session_id,
            )
            if object_id is None or session_id is None:
                return []
            if not object_id:
                return []

            object_location, object_type, object_index = object_id.split(":")
            return self.fun2(connection_id, session_id, object_id)

    def __call__(self, user_id, session_id, object_id, filter_list=[]):
        self._object_id = object_id
        self._filter_list = filter_list
        print("\n fun", f"property-editor-{self._id}")
        return html.Div(
            children=self.fun2(user_id, session_id, object_id),
            id=f"property-editor-{self._id}",
        )

    def fun2(self, user_id, session_id, object_id):
        object_location, object_type, object_index = object_id.split(":")
        self._all_input_widgets = self.get_widgets(
            user_id, session_id, object_type, object_index, "input"
        )
        self._all_command_widgets = self.get_widgets(
            user_id, session_id, object_type, object_index, "command"
        )
        object_type = object_type.split("/")[-1]
        object_name = object_type + "-" + object_index if object_index else object_type
        object_name = object_name.capitalize()
        print("fun2", user_id, session_id, object_id)
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
                                    for k, v in self._all_input_widgets.items()
                                    if not self._filter_list or k in self._filter_list
                                ]
                            ),
                            # dbc.CardBody(list(self._all_input_widgets.values())),
                            html.Div(
                                [
                                    v
                                    for k, v in self._all_command_widgets.items()
                                    if not self._filter_list
                                    or k.split(":")[0] in self._filter_list
                                ],
                                # list(self._all_command_widgets.values()),
                                className="d-grid gap-1",
                                style={"padding": "4px 4px 4px 4px"},
                            ),
                        ],
                    ),
                ]
            ),
        )
