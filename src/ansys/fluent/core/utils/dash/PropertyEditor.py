from dash.dependencies import Input, Output, State, MATCH, ALL
import dash
from dash.exceptions import PreventUpdate
from dash import html
from local_property_editor import LocalPropertyEditor
from settings_property_editor import SettingsPropertyEditor
from ansys.fluent.core.utils.generic import SingletonMeta
from ansys.fluent.core.solver.flobject import to_python_name
class PropertyEditor(metaclass=SingletonMeta):
    def __init__(self, app, SessionsManager):
        self._app = app
        self._remote_property_editor = (
             SettingsPropertyEditor(app, SessionsManager)
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
            obj, static_info = editor.get_object_and_static_info(object_type, connection_id, session_id)
            path_list = input_index.split("/")[1:]
            for path in path_list:
                obj = getattr(obj, path)
                if obj is None:
                    raise PreventUpdate
                if static_info:
                    static_info = static_info["children"][obj.scheme_name]                    

            if (static_info and static_info["type"] == "boolean") or isinstance(obj(), bool):
                input_value = True if input_value else False
            if input_value == obj():
                print("PreventUpdate")
                raise PreventUpdate
            obj.set_state(input_value)
            return str(input_index) + str(input_value)

        @self._app.callback(
            Output("property-editor-title", "children"),
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
            return html.H5(object_id.split(":")[-1].split("/")[-1].capitalize()),list(self._all_widgets.values())


        @self._app.callback(
            Output("object-id", "value"),
            Input("connection-id", "data"),#
            Input("session-id", "value"),
            Input("tree-view", "selected")
        )
        def session_changed_or_tree_selected(connection_id, session_id, object_id):
            print("session_changed", connection_id, session_id, object_id)

            if session_id is None:
                raise PreventUpdate
            if object_id is None or len(object_id)==0:
                raise PreventUpdate                
            object_id = object_id[0]
            ctx = dash.callback_context
            triggered_from = ctx.triggered[0]["prop_id"].split(".")[0]
            if triggered_from == 'tree-view':        
                if "local" in object_id or "remote" in object_id:           
                     return object_id 
                else:
                     raise PreventUpdate
            else:             
                object_id = self._id_map.get(f"{connection_id}-{session_id}")
                if object_id is None:
                    raise PreventUpdate
                return object_id
