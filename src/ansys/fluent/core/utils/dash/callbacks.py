import uuid

import dash
from dash.exceptions import PreventUpdate
from dash import Input, Output, State, ALL
from dash import html, dcc
import dash_bootstrap_components as dbc

from sessions_manager import SessionsManager
from objects_handle import LocalObjectsHandle, SettingsObjectsHandle
from local_property_editor import LocalPropertyEditor
from post_windows import (
    MonitorWindow,
    PlotWindowCollection,
    GraphicsWindowCollection,
    PostWindowCollection,
)
from settings_property_editor import SettingsPropertyEditor
from tree_view import TreeView
from ansys.fluent.core.solver.flobject import to_python_name
from state_manager import StateManager
from dash_component import RCTree as dash_tree
import itertools
user_name_to_session_map = {}


def register_callbacks(app):
    @app.callback(
        Output("command-output", "value"),
        Input({"type": "settings-command-button", "index": ALL}, "n_clicks"),
        Input("connection-id", "data"),
        State({"type": "settings-command-input", "index": ALL}, "value"),
        State("session-id", "value"),
    )
    def on_settings_command_execution(
        commnads,
        user_id,
        args_value,
        session_id,
    ):
        """"Callback executed setting command button is pressed"""
        ctx = dash.callback_context
        triggered_value = ctx.triggered[0]["value"]
        if not triggered_value:
            raise PreventUpdate
        command_name, object_location, object_type, object_index = eval(
            ctx.triggered[0]["prop_id"].split(".")[0]
        )["index"].split(":")
                    
           
        obj, static_info = SettingsObjectsHandle(SessionsManager).get_object_and_static_info(user_id, session_id, object_type, object_index)
                
        kwargs = {}
        cmd_obj = getattr(obj, command_name)
        args_iter = iter(args_value)
        args_info = static_info["commands"][cmd_obj.obj_name].get("arguments", {})
        for arg_name, arg_info in args_info.items():
            kwargs[to_python_name(arg_name)] = next(args_iter)
        return_value = cmd_obj(**kwargs)
        return f"{return_value}"

    @app.callback(
        Output("property-editor-container", "children"),
        Input("object-id", "value"),
        Input("connection-id", "data"),
        State("session-id", "value"),
    )
    def show_property_editor(object_id, user_id, session_id):
        
        if object_id is None or session_id is None:
            return []
        object_location, object_type, object_index = object_id.split(":")
        editor = (
            LocalPropertyEditor()
            if object_location == "local"
            else SettingsPropertyEditor()
        )
        return editor(user_id, session_id, object_id)


    @app.callback(
        Output("monitor-tab-content-main", "children"),
        Input("monitor-tabs-main", "active_tab"),
        Input("need-to-data-fetch", "value"),
        Input("connection-id", "data"),
        State("session-id", "value"),
        prevent_initial_call=True,
    )
    def update_monitor_graph(active_tab, need_to_data_fetch, user_id, session_id):
        return MonitorWindow.get_graph(active_tab, user_id, session_id)
                
        
    @app.callback(
        Output("post-window-tab-content", "children"),
        Input("graphics-button-clicked", "value"),
        Input("plot-button-clicked", "value"),
        Input("connection-id", "data"),
        Input("post-window-tabs", "active_tab"),
        Input("need-to-data-fetch", "value"),
        State("session-id", "value"),
        State("object-id", "value"),
        State("tab-content-created", "value"),
        prevent_initial_call=True,
    )
    def on_click_update(
        n_graphics_clicks,
        n_plot_clicks,
        user_id,
        active_tab,
        need_to_data_fetch,
        session_id,
        object_id,
        main_active_tab,
    ):
        ctx = dash.callback_context
        triggered_value = ctx.triggered[0]["value"]
        triggered_from = ctx.triggered[0]["prop_id"].split(".")[0]
        if triggered_from in ("graphics-button-clicked", "plot-button-clicked"):
            post_window_collection = (
                GraphicsWindowCollection(
                    user_id, session_id
                )
                if triggered_from == "graphics-button-clicked"
                else PlotWindowCollection(
                    user_id, session_id
                )
            )
        elif main_active_tab == "graphics":
            post_window_collection = GraphicsWindowCollection(
                user_id, session_id
            )
        else:
            post_window_collection = PlotWindowCollection(
                user_id, session_id
            )

        print(
            "\n on_click_update:",
            triggered_from,
            triggered_value,
            post_window_collection._active_window,
            session_id,
        )
        if triggered_value is None:
            print("triggered_value is None")
            raise PreventUpdate

        post_window_collection._active_window = int(active_tab)
        event_info = SessionsManager(user_id, session_id).get_event_info(
            "IterationEndedEvent"
        )

        if triggered_from in ("plot-button-clicked", "graphics-button-clicked"):
            if object_id is None or triggered_value == "0":
                raise PreventUpdate
            object_location, object_type, object_index = object_id.split(":")
            if object_location != "local":
                raise PreventUpdate
            if not post_window_collection.is_type_supported(object_type):
                raise PreventUpdate
            post_window_collection._window_data[
                post_window_collection._active_window
            ] = {
                "object_type": object_type,
                "object_index": object_index,
                "itr_index": event_info.index if event_info else None,
            }
            return post_window_collection.get_viewer(
                user_id, session_id, object_type, object_index
            )
        elif triggered_from == "need-to-data-fetch":
            if need_to_data_fetch == "yes":

                window_data = post_window_collection._window_data.get(
                    post_window_collection._active_window
                )
                if window_data is None:
                    PostWindowCollection._is_executing = False
                    return post_window_collection.get_content()
                object_type = window_data["object_type"]
                object_index = window_data["object_index"]
                window_data["itr_index"] = event_info.index if event_info else None
                print(
                    "get_viewer",
                    user_id,
                    session_id,
                    object_type,
                    object_index,
                )
                viewer = post_window_collection.get_viewer(
                    user_id, session_id, object_type, object_index
                )
                PostWindowCollection._is_executing = False
                return viewer
        else:
            window_data = post_window_collection._window_data.get(
                post_window_collection._active_window
            )
            if (
                event_info
                and window_data
                and window_data["itr_index"] != event_info.index
            ):
                object_type = window_data["object_type"]
                object_index = window_data["object_index"]
                window_data["itr_index"] = event_info.index
                return post_window_collection.get_viewer(
                    user_id, session_id, object_type, object_index
                )

        return post_window_collection.get_content()

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
        triggered_value = ctx.triggered[0]["value"]
        if user_id is None or session_id is None:
            raise PreventUpdate
        #print('watcher', user_id, session_id, triggered_from_list, StateManager(user_id, session_id, SessionsManager).get_var_value("show-outline"))
        if (
            "tab-content-created" in triggered_from_list
            and StateManager(user_id, session_id, SessionsManager).get_var_value("show-outline")
        ):
            StateManager(user_id, session_id, SessionsManager).set_var_value("show-outline", False)
            graphics = GraphicsWindowCollection(
                user_id, session_id
            )
            graphics._window_data[graphics._active_window] = {
                "object_type": "Mesh",
                "object_index": "outline",
                "itr_index": None,
            }
            return "yes"

        elif "interval-component" in triggered_from_list:
            event_info = SessionsManager(user_id, session_id).get_event_info(
                "CalculationsStartedEvent"
            )
            if event_info:
                print(PostWindowCollection._is_executing)
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
        event_info = SessionsManager(user_id, session_id).get_event_info(
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
        sessions_manager = SessionsManager(user_id, session_id)
        sessions_manager.add_session(session_token, user_name_to_session_map)
        sessions = []
        if options is not None:
            sessions = options
        sessions.append(session_id)

        return [sessions, session_id]

    @app.callback(
        Output("tree-view-selection", "value"),
        Input("tree-view", "selected"),
    )
    def on_tree_selection(tree_selection):
        if tree_selection and isinstance(tree_selection, list):
            return tree_selection[0]
        else:
            raise PreventUpdate

    @app.callback(
        Output("refresh-property-editor", "value"),
        Output("object-id", "value"),
        Input(
            {"type": f"input-widget", "index": ALL},
            "value",
        ),
        Input("tree-view-selection", "value"),
        Input("connection-id", "data"),
        Input("session-id", "value"),
        prevent_initial_call=True,
    )
    def on_value_changed(
        input_values,
        selected_node,
        user_id,
        session_id,
    ):
        ctx = dash.callback_context
        input_value = ctx.triggered[0]["value"]
        if input_value is None:
            raise PreventUpdate
        triggered_from = ctx.triggered[0]["prop_id"].split(".")[0]
        if triggered_from == "tree-view-selection":
            if "local" in selected_node or "remote" in selected_node:
                return selected_node, selected_node
            else:
                raise PreventUpdate

        elif triggered_from == "session-id":
            PostWindowCollection._is_executing = False
            return None, None
        else:
            input_index = eval(triggered_from)["index"]
            input_index, object_location, object_type, object_index = input_index.split(
                ":"
            )
            print(
                "\n on_value_changed",
                input_index,
                object_location,
                object_type,
                object_index,
            )
            
            
            if object_location == "local":
                obj, static_info =  LocalObjectsHandle(SessionsManager)._get_object(user_id, session_id, object_type, object_index), None 
            else:
                obj, static_info = SettingsObjectsHandle(SessionsManager).get_object_and_static_info(user_id, session_id, object_type, object_index) 
                       
            path_list = input_index.split("/")[1:]            
            for path in path_list:
                try:
                    obj = getattr(obj, path)
                    if static_info:
                        static_info = static_info["children"][obj.obj_name]
                except AttributeError:
                    obj = obj[path]
                    static_info = static_info["object-type"]
            if obj is None:
                raise PreventUpdate

            if (static_info and static_info["type"] == "boolean") or isinstance(
                obj(), bool
            ):
                input_value = True if input_value else False
            if input_value == obj():               
                raise PreventUpdate
            print("set_state \n", obj, input_value)            
            obj.set_state(input_value)
            object_id = f"{object_location}:{object_type}:{object_index}"
            return object_id, object_id

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
            handle = LocalObjectsHandle(SessionsManager)
            new_object = handle.create_new_object(
                user_id, session_id, object_type, object_index
            )
        elif triggered_from == "delete-button-clicked":
            object_location, object_type, object_index = object_id.split(":")
            handle = LocalObjectsHandle(SessionsManager)
            new_object = handle.delete_object(
                user_id, session_id, object_type, object_index
            )
        print("update_tree", triggered_from, triggered_value)
        tree_nodes, keys = TreeView(
            app, user_id, session_id, SessionsManager
        ).get_tree_nodes()
        filtered = filter(
            lambda x: session_id == x[0], user_name_to_session_map[user_id]
        )
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
        prevent_initial_call=True,
    )
    def on_button_click(n_graphics_clicks):
        if n_graphics_clicks is None:
            raise PreventUpdate
        return str(n_graphics_clicks)

    @app.callback(
        Output("plot-button-clicked", "value"),
        Input("plot-button", "n_clicks"),
        prevent_initial_call=True,
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
            PlotWindowCollection(user_id, session_id)
            if input_index == "plot"
            else GraphicsWindowCollection(user_id, session_id)
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
                GraphicsWindowCollection( user_id, session_id)(),
                active_tab,
            )

        elif active_tab == "plots":
            return (
                PlotWindowCollection( user_id, session_id)(),
                active_tab,
            )

        elif active_tab == "monitors":
            MonitorWindow._id_iter = itertools.count(-1)
            return (
                MonitorWindow(user_id, session_id)(),
                active_tab,
            )
