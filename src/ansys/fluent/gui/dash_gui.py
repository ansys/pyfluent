from app_defn import app
from dash import ALL, Input, Output, State, dcc, html
from dash.exceptions import PreventUpdate
from layouts.main import app_layout
from sessions_handle import SessionsHandle
from state_manager import StateManager

def get_default_components():
    return [
        dcc.Interval(
            id="interval-component",
            interval=1 * 1000,
            n_intervals=0,
        ),
        html.Data(id="need-to-data-fetch", value="no"),
    ]


def mod_app_layout():
    layout = app_layout()
    layout.children = get_default_components() + layout.children
    return layout


app.layout = mod_app_layout


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
                sessions
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


if __name__ == "__main__":
    app.run_server(debug=True, port=8800)
