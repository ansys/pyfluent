import uuid

import dash
from dash.exceptions import PreventUpdate
from dash import Input, Output, State, ALL
from dash import html

from sessions_manager import SessionsManager
from local_property_editor import (
    MonitorWindow,
    PlotWindowCollection,
    GraphicsWindowCollection,
    PostWindowCollection,
    LocalPropertyEditor,
)
from tree_view import TreeView
from dash_component import RCTree as dash_tree

user_name_to_session_map = {}

def register_callbacks(app):

    @app.callback(
        Output("need-to-data-fetch", "value"),
        Input("tab-content-created", "value"),
        Input("interval-component", "n_intervals"),
        Input("connection-id", "data"),
        State("session-id", "value"),
        State("need-to-data-fetch", "value"),
    )
    def watcher(tab_content_created, n_intervals, user_id, session_id, need_to_fetch):

        ctx = dash.callback_context
        triggered_from_list = [v["prop_id"].split(".")[0] for v in ctx.triggered]
        if (
            "tab-content-created" in triggered_from_list
            and PostWindowCollection._show_outline
        ):
            PostWindowCollection._show_outline = False
            graphics = GraphicsWindowCollection(app, user_id, session_id, SessionsManager)
            graphics._window_data[graphics._active_window] = {
                "object_type": "Mesh",
                "object_index": "outline",
                "itr_index": None,
            }
            return "yes"

        elif "interval-component" in triggered_from_list:
            event_info = SessionsManager(app, user_id, session_id).get_event_info(
                "CalculationsStartedEvent"
            )           
            if event_info:
                if PostWindowCollection._is_executing == False:
                    PostWindowCollection._is_executing = True
                    return "yes"
                else:
                    raise PreventUpdate
            else:
                if need_to_fetch == "yes":
                    return "no"
                else:
                    raise PreventUpdate

        raise PreventUpdate


    @app.callback(
        Output("progress-container", "style"),
        Output("progress-bar", "value"),
        Output("progress-bar", "label"),
        Output("progress-messgae", "children"),
        Input("interval-component", "n_intervals"),
        Input("connection-id", "data"),
        State("session-id", "value"),
        prevent_initial_call=True,
    )
    def on_progress_update(n_intervals, user_id, session_id):
        event_info = SessionsManager(app, user_id, session_id).get_event_info(
            "ProgressEvent"
        )
        if event_info is None:
            return [{"display": "none"}, dash.no_update, dash.no_update, dash.no_update]

        return [
            {"display": "flex", "flex-direction": "row"},
            event_info.percentComplete,
            str(event_info.percentComplete) + "%",
            event_info.message,
        ]


    @app.callback(
        Output("session-id", "options"),
        Output("session-id", "value"),
        Input("connect-session", "n_clicks"),
        Input("connection-id", "data"),
        State("session-token", "value"),
        State("session-id", "options"),
    )
    def create_session(n_clicks, user_id, session_token, options):

        ctx = dash.callback_context
        triggered_value = ctx.triggered[0]["value"]
        triggered_from = ctx.triggered[0]["prop_id"].split(".")[0]

        if n_clicks == 0 or triggered_value is None:
            raise PreventUpdate
       
        user_sessions = user_name_to_session_map.get(user_id)
        if not user_sessions:
            user_sessions = user_name_to_session_map[user_id] = []

        session_id = f"session-{len(options)}"
        user_sessions.append((session_id, user_id + ":" + uuid.uuid4().hex))
        sessions_manager = SessionsManager(app, user_id, session_id)
        sessions_manager.add_session(session_token, user_name_to_session_map)
        sessions = []
        if options is not None:
            sessions = options
        sessions.append(session_id)

        return [sessions, session_id]


    @app.callback(
        Output("object-id", "value"),
        Input("connection-id", "data"),  #
        Input("tree-view", "selected"),
        Input("session-id", "value"),
    )
    def update_object(user_id, object_id, session_id):
        
        if session_id is None:
            raise PreventUpdate
        ctx = dash.callback_context
        triggered_from = ctx.triggered[0]["prop_id"].split(".")[0]
        print("update_object", user_id, session_id, object_id, triggered_from)
        if triggered_from == "tree-view":
            if object_id is None or len(object_id) == 0:
                raise PreventUpdate
            object_id = object_id[0]
            if "local" in object_id or "remote" in object_id:
                return object_id
            else:
                raise PreventUpdate
        else:
            PostWindowCollection._is_executing = False
            return None


    @app.callback(
        Output("tree-container", "children"),
        Output("uuid-id", "value"),
        Input("connection-id", "data"),  #
        Input("session-id", "value"),
        Input("save-button-clicked", "value"),
        Input("delete-button-clicked", "value"),
        State("object-id", "value"),
        # prevent_initial_call=True,
    )
    def update_tree(user_id, session_id, save_n_clicks, delete_n_clicks, object_id):
        ctx = dash.callback_context
        triggered_value = ctx.triggered[0]["value"]
        triggered_from = ctx.triggered[0]["prop_id"].split(".")[0]
        print("update_tree", triggered_from, triggered_value)
        if session_id is None or user_id is None or triggered_value is None:
            raise PreventUpdate

        if triggered_from == "save-button-clicked":
            object_location, object_type, object_index = object_id.split(":")
            editor = LocalPropertyEditor(app, SessionsManager)
            new_object = editor.create_new_object(
                user_id, session_id, object_type, object_index
            )
        elif triggered_from == "delete-button-clicked":
            object_location, object_type, object_index = object_id.split(":")
            editor = LocalPropertyEditor(app, SessionsManager)
            new_object = editor.delete_object(
                user_id, session_id, object_type, object_index
            )
        print("update_tree", triggered_from, triggered_value)
        tree_nodes, keys = TreeView(
            app, user_id, session_id, SessionsManager
        ).get_tree_nodes()
        filtered = filter(lambda x: session_id == x[0], user_name_to_session_map[user_id])
        print(keys)
        print(tree_nodes)
        return (
            dash_tree(
                id="tree-view",
                data=tree_nodes,
                selected=[],
                expandedKeys=keys.append("Root"),
            ),
            list(filtered)[0][1],
        )


    @app.callback(
        Output("save-button-clicked", "value"),
        Input("save-button", "n_clicks"),
        prevent_initial_call=True,
    )
    def manage_save_delete_object(save_n_clicks):
        if save_n_clicks is None or save_n_clicks == 0:
            raise PreventUpdate
        return str(save_n_clicks)


    @app.callback(
        Output("delete-button-clicked", "value"),
        Input("delete-button", "n_clicks"),
        prevent_initial_call=True,
    )
    def manage_save_delete_object(delete_n_clicks):
        if delete_n_clicks is None or delete_n_clicks == 0:
            raise PreventUpdate
        return str(delete_n_clicks)


    @app.callback(
        Output("graphics-button-clicked", "value"),
        Input("graphics-button", "n_clicks"),
    )
    def on_button_click(n_graphics_clicks):
        if n_graphics_clicks is None:
            raise PreventUpdate
        return str(n_graphics_clicks)


    @app.callback(
        Output("plot-button-clicked", "value"),
        Input("plot-button", "n_clicks"),
    )
    def on_button_click(n_post_clicks):
        if n_post_clicks is None:
            raise PreventUpdate
        return str(n_post_clicks)


    @app.callback(
        Output("tabs", "active_tab"),
        Input(
            {"type": "add-post-window", "index": ALL},
            "n_clicks",
        ),
        Input(
            {"type": "remove-post-window", "index": ALL},
            "n_clicks",
        ),
        Input("connection-id", "data"),
        State("session-id", "value"),
        prevent_initial_call=True,
    )
    def add_remove_post_window(add_clicks, remove_clicks, user_id, session_id):

        print("add_remove_window", add_clicks, remove_clicks, user_id, session_id)
        if not add_clicks or not remove_clicks:
            raise PreventUpdate
        ctx = dash.callback_context
        print("add_remove_window", ctx.triggered)
        input_value = ctx.triggered[0]["value"]
        if input_value is None:
            raise PreventUpdate

        input_data = eval(ctx.triggered[0]["prop_id"].split(".")[0])

        input_index = input_data["index"]
        input_type = input_data["type"]
        window = (
            PlotWindowCollection(app, user_id, session_id, SessionsManager)
            if input_index == "plot"
            else GraphicsWindowCollection(app, user_id, session_id, SessionsManager)
        )
        opr = "add" if input_type.startswith("add") else "remove"
        print("add_remove_window", opr, input_index, input_value)
        if opr == "add":
            if input_value == 0:
                raise PreventUpdate
            id = 0
            while True:
                if id not in window._windows:
                    break
                id = id + 1
            window._active_window = id
            window._windows.append(id)
            print("add_remove_window:add", window._active_window, window._windows)
        elif opr == "remove":
            if input_value == 0 or len(window._windows) == 1:
                raise PreventUpdate
            if window._state.get(window._active_window):
                del window._state[window._active_window]
            index = window._windows.index(window._active_window)
            new_index = (
                window._windows[index + 1] if index == 0 else window._windows[index - 1]
            )
            window._windows.remove(window._active_window)
            window._active_window = new_index

        return "plots" if input_index == "plot" else "graphics"


    @app.callback(
        Output("tab-content", "children"),
        Output("tab-content-created", "value"),
        Input("tabs", "active_tab"),
        Input("connection-id", "data"),
        Input("session-id", "value"),
    )
    def render_tab_content(active_tab, user_id, session_id):
        """
        This callback takes the 'active_tab' property as input, as well as the
        stored graphs, and renders the tab content depending on what the value of
        'active_tab' is.
        """
        print("render_tab_content", active_tab, user_id, session_id)
        if session_id is None:
            return (
                html.Pre(
                    """
                  Welcome to ANSYS PyFluent Web Client 22.2.0
                  
                  Copyright 1987-2022 ANSYS, Inc. All Rights Reserved.
                  Unauthorized use, distribution or duplication is prohibited.
                  This product is subject to U.S. laws governing export and re-export.
                  For full Legal Notice, see documentation.
                  
                  Use session token to get connected with runnng session.
                  Please visit https://github.com/pyansys/pyfluent for more information.
                  
                  """,
                    style={"font": "14px 'Segoe UI'"},
                ),
                dash.no_update,
            )

        if active_tab == "graphics":
            return (
                GraphicsWindowCollection(app, user_id, session_id, SessionsManager)(),
                "yes",
            )

        elif active_tab == "plots":
            return (
                PlotWindowCollection(app, user_id, session_id, SessionsManager)(),
                "yes",
            )

        elif active_tab == "monitors":
            return MonitorWindow(app, user_id, session_id, SessionsManager)(), "yes"