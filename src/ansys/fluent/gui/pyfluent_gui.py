"""App starting module."""

from app_defn import app
from dash import Input, Output, State, dcc, html
from dash.exceptions import PreventUpdate
from layouts.main import app_layout

from ansys.fluent.gui.components import SessionsHandle, StateManager


def mod_app_layout():
    default_components = [
        dcc.Interval(
            id="interval-component",
            interval=1 * 1000,
            n_intervals=0,
        ),
        html.Data(id="auto-refresh", value="no"),
    ]
    layout = app_layout()
    layout.children = default_components + layout.children
    return layout


app.layout = mod_app_layout


@app.callback(
    Output("auto-refresh", "value"),
    Input("interval-component", "n_intervals"),
    State("user-id", "data"),
    State("auto-refresh", "value"),
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
            # print("Busy..")
            raise PreventUpdate
        else:
            return "yes"
    else:
        if need_to_fetch == "yes":
            return "no"
        else:
            raise PreventUpdate

    raise PreventUpdate


if __name__ == "__main__":
    app.run_server(debug=True, port=8800)
