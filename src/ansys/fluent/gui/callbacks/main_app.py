import uuid

import dash
from dash import ALL, Input, Output, State, dcc, html
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash_component import RCTree as dash_tree
from objects_handle import LocalObjectsHandle, SettingsObjectsHandle
from post_windows import GraphicsWindow, MonitorWindow, PlotWindow
from property_editors import LocalPropertyEditor, SettingsPropertyEditor
from sessions_handle import SessionsHandle
from state_manager import StateManager
from tree_data_extractor import TreeDataExtractor

from ansys.fluent.core.solver.flobject import to_python_name

user_name_to_session_map = {}


def register_callbacks(app):
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
        Output("session-id", "value"),
        Input("sessions-list", "value"),
    )
    def on_session_change(selected_session):
        return selected_session

    @app.callback(
        Output("property-editor-container", "children"),
        Input("object-id", "value"),
        Input("session-id", "value"),
        State("user-id", "data"),
    )
    def show_property_editor(object_id, session_id, user_id):
        if object_id is None or session_id is None:
            return []
        ctx = dash.callback_context
        triggered_value = ctx.triggered[0]["value"]
        triggered_from = ctx.triggered[0]["prop_id"].split(".")[0]
        if triggered_from == "session-id":
            return []
        object_location, object_type, object_index = object_id.split(":")
        editor = (
            LocalPropertyEditor(user_id, session_id, 1)
            if object_location == "local"
            else SettingsPropertyEditor(user_id, session_id, 1)
        )
        return editor(object_id)

    @app.callback(
        Output("progress-container", "style"),
        Output("progress-bar", "value"),
        Output("progress-bar", "label"),
        Output("progress-messgae", "children"),
        Input("interval-component", "n_intervals"),
        Input("user-id", "data"),
        State("session-id", "value"),
        prevent_initial_call=True,
    )
    def on_progress_update(n_intervals, user_id, session_id):
        event_info = SessionsHandle(user_id, session_id).get_event_info("ProgressEvent")
        if event_info is None:
            return [{"display": "none"}, dash.no_update, dash.no_update, dash.no_update]

        return [
            {"display": "flex", "flex-direction": "row"},
            event_info.percentComplete,
            str(event_info.percentComplete) + "%",
            event_info.message,
        ]

    @app.callback(
        Output("sessions-list", "options"),
        Output("sessions-list", "value"),
        Input("connect-session", "n_clicks"),
        Input("user-id", "data"),
        State("session-token", "value"),
        State("sessions-list", "options"),
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
        sessions_manager = SessionsHandle(user_id, session_id)
        sessions_manager.add_session(session_token, user_name_to_session_map)
        sessions = []
        if options is not None:
            sessions = options
        sessions.append(session_id)

        return [sessions, session_id]

    @app.callback(
        Output("tree-container", "children"),
        Output("uuid-id", "value"),
        Input("session-id", "value"),
        Input(
            {"type": "graphics-button", "index": ALL},
            "n_clicks",
        ),
        State("user-id", "data"),
        prevent_initial_call=True,
    )
    def update_tree(session_id, graphics_button_clicks, user_id):
        ctx = dash.callback_context
        triggered_value = ctx.triggered[0]["value"]
        if triggered_value is None:
            raise PreventUpdate
        triggered_from = ctx.triggered[0]["prop_id"].split(".")[0]
        print("update_tree", triggered_from, graphics_button_clicks, triggered_value)
        if triggered_from != "session-id":
            if triggered_value == 0:
                raise PreventUpdate
            triggered_data = eval(triggered_from)
            (
                user_id,
                session_id,
                object_location,
                object_type,
                object_index,
                opr,
                editor_id,
            ) = triggered_data["index"].split(":")
            if opr == "new":
                handle = LocalObjectsHandle(SessionsHandle)
                new_object = handle.create_new_object(
                    user_id, session_id, object_type, object_index
                )
            elif opr == "delete":
                handle = LocalObjectsHandle(SessionsHandle)
                new_object = handle.delete_object(
                    user_id, session_id, object_type, object_index
                )
        tree_nodes, keys = TreeDataExtractor(user_id, session_id).get_tree_nodes()
        filtered = filter(
            lambda x: session_id == x[0], user_name_to_session_map[user_id]
        )
        # print('update_tree', user_id, session_id, keys)
        return (
            dash_tree(
                id="tree-view",
                data=tree_nodes,
                selected=[],
                expandedKeys=["Root"] + keys,
            ),
            list(filtered)[0][1],
        )

    @app.callback(
        Output("tab-content", "children"),
        Output("tab-content-created", "value"),
        Input("tabs", "active_tab"),
        Input("session-id", "value"),
        State("user-id", "data"),
    )
    def render_tab_content(active_tab, session_id, user_id):
        """This callback takes the 'active_tab' property as input, as well as
        the stored graphs, and renders the tab content depending on what the
        value of 'active_tab' is."""
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
                GraphicsWindow(user_id, session_id, 1)(
                    init_data={0: ("Mesh", "outline")}
                ),
                active_tab,
            )

        elif active_tab == "plots":
            return (
                PlotWindow(user_id, session_id, 1)(),
                active_tab,
            )

        elif active_tab == "monitors":
            return (
                MonitorWindow(user_id, session_id, 1)(),
                active_tab,
            )
