from dash.dependencies import Input, Output, State, MATCH, ALL
import dash
from dash.exceptions import PreventUpdate
from local_property_editor import LocalPropertyEditor
from ansys.fluent.core.utils.generic import SingletonMeta
class PropertyEditor(metaclass=SingletonMeta):
    def __init__(self, app, SessionsManager):
        self._app = app
        self._remote_property_editor = (
            None  # SettingsEditor(app, SessionsManager)
        )
        self._local_property_editor = LocalPropertyEditor(app, SessionsManager)
        self._id_map = {}
        self.create_callback()

    def create_callback(self):
        def update_stored_widgets(object_id, connection_id, session_id):
            object_location, object_type = object_id.split(":")
            editor = (
                self._local_property_editor
                if object_location == "local"
                else self._remote_property_editor
            )
            self._all_widgets = editor.get_widgets(
                object_type, connection_id, session_id
            )

        @self._app.callback(
            Output("refresh-property-editor", "value"),
            Input(
                {"type": f"input-widget", "index": ALL},
                "value",
            ),
            Input("connection-id", "data"),
            State("session-id", "value"),
            State("object-id", "value"),
        )
        def on_value_changed(
            input_values,
            connection_id,
            session_id,
            object_id,
        ):
            ctx = dash.callback_context
            input_value = ctx.triggered[0]["value"]
            if input_value is None:
                raise PreventUpdate
            input_index = eval(ctx.triggered[0]["prop_id"].split(".")[0])[
                "index"
            ]
            object_location, object_type = object_id.split(":")
            editor = (
                self._local_property_editor
                if object_location == "local"
                else self._remote_property_editor
            )

            print("value_changed", input_index, input_value)
            obj = editor.get_object(object_type, connection_id, session_id)
            path_list = input_index.split("/")[1:]
            for path in path_list:
                obj = getattr(obj, path)
                if obj is None:
                    raise PreventUpdate

            if isinstance(obj(), bool):
                input_value = True if input_value else False
            if input_value == obj():
                print("PreventUpdate")
                raise PreventUpdate
            obj.set_state(input_value)
            return str(input_index) + str(input_value)

        @self._app.callback(
            Output("property-editor", "children"),
            Input("refresh-property-editor", "value"),
            Input("connection-id", "data"),
            Input("object-id", "value"),
            State("session-id", "value"),
        )
        def refresh_widgets(_, connection_id, object_id, session_id):
            print("show hide", _, connection_id, object_id, session_id)
            if object_id is None or session_id is None:
                raise PreventUpdate
            self._id_map[f"{connection_id}-{session_id}"] = object_id
            update_stored_widgets(object_id, connection_id, session_id)
            return list(self._all_widgets.values())

        @self._app.callback(
            Output("object-id", "value"),
            Input("connection-id", "data"),
            Input("session-id", "value"),
        )
        def session_changed(connection_id, session_id):
            print("session_changed", connection_id, session_id)
            if session_id is None:
                raise PreventUpdate
            object_id = self._id_map.get(f"{connection_id}-{session_id}")
            if object_id is None:
                raise PreventUpdate
            return object_id
