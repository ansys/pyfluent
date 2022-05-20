import itertools
import uuid

from config import async_commands
import dash
from dash import ALL, Input, Output, State, dcc, html
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from objects_handle import LocalObjectsHandle, SettingsObjectsHandle
from property_editors import LocalPropertyEditor, SettingsPropertyEditor
from sessions_handle import SessionsHandle
from state_manager import StateManager

from ansys.fluent.core.solver.flobject import to_python_name
from ansys.fluent.core.utils.async_execution import asynchronous


def register_callbacks(app):
    @app.callback(
        Output("command-output", "value"),
        Input({"type": "settings-command-button", "index": ALL}, "n_clicks"),
        State({"type": "settings-command-input", "index": ALL}, "value"),
    )
    def on_settings_command_execution(
        commnads,
        args_value,
    ):
        """"Callback executed setting command button is pressed."""
        ctx = dash.callback_context
        triggered_value = ctx.triggered[0]["value"]
        if not triggered_value:
            raise PreventUpdate
        (
            command_name,
            user_id,
            session_id,
            object_location,
            object_type,
            object_index,
        ) = eval(ctx.triggered[0]["prop_id"].split(".")[0])["index"].split(":")

        obj, static_info = SettingsObjectsHandle(
            SessionsHandle
        ).get_object_and_static_info(user_id, session_id, object_type, object_index)

        kwargs = {}
        exec_async = (
            obj.path in async_commands and command_name in async_commands[obj.path]
        )
        cmd_obj = getattr(obj, command_name)
        args_iter = iter(args_value)
        args_info = static_info["commands"][cmd_obj.obj_name].get("arguments", {})
        for arg_name, arg_info in args_info.items():
            kwargs[to_python_name(arg_name)] = next(args_iter)

        @asynchronous
        def run_async(f, **kwargs):
            print("running async")
            f(**kwargs)

        return_value = run_async(cmd_obj, **kwargs) if exec_async else cmd_obj(**kwargs)
        return f"{return_value}"

    @app.callback(
        Output("need-to-data-fetch", "value"),
        Input("interval-component", "n_intervals"),
        State("user-id", "data"),
        State("need-to-data-fetch", "value"),
    )
    def event_loop(n_intervals, user_id, need_to_fetch):
        sessions = SessionsHandle.get_sessions(user_id)
        event_info = any(
            [
                SessionsHandle(user_id, session_id).get_event_info(
                    "CalculationsStartedEvent"
                )
                for session_id in sessions
            ]
        )
        if event_info:
            if any(
                map(
                    lambda session: StateManager(
                        user_id, session, SessionsHandle
                    ).is_busy(),
                    sessions,
                )
            ):
                print("Busy..")
                raise PreventUpdate
            else:
                return "yes"
        else:
            if need_to_fetch == "yes":
                return "no"
            else:
                raise PreventUpdate

        raise PreventUpdate

    @app.callback(
        Output("object-id", "value"),
        Input(
            {"type": f"input-widget", "index": ALL},
            "value",
        ),
        Input("tree-view-selection", "value"),
        State("user-id", "data"),
        prevent_initial_call=True,
    )
    def on_value_changed(
        input_values,
        selected_node,
        user_id,
    ):
        ctx = dash.callback_context
        input_value = ctx.triggered[0]["value"]
        if input_value is None:
            raise PreventUpdate
        triggered_from = ctx.triggered[0]["prop_id"].split(".")[0]
        if triggered_from == "tree-view-selection":
            if "local" in selected_node or "remote" in selected_node:
                return selected_node
            else:
                raise PreventUpdate
        else:
            input_index = eval(triggered_from)["index"]
            (
                input_index,
                user_id,
                session_id,
                object_location,
                object_type,
                object_index,
            ) = input_index.split(":")
            print(
                "\n on_value_changed",
                input_index,
                user_id,
                session_id,
                object_location,
                object_type,
                object_index,
            )

            if object_location == "local":
                obj, static_info = (
                    LocalObjectsHandle(SessionsHandle).get_object(
                        user_id, session_id, object_type, object_index
                    ),
                    None,
                )
            else:
                obj, static_info = SettingsObjectsHandle(
                    SessionsHandle
                ).get_object_and_static_info(
                    user_id, session_id, object_type, object_index
                )
            # print(user_id, session_id, obj)
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
            # print("set_state \n", obj, input_value)
            obj.set_state(input_value)
            object_id = f"{object_location}:{object_type}:{object_index}"
            return object_id
