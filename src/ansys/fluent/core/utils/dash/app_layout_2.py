import dash
from app_defn import app
from dash import dcc, html
import dash_bootstrap_components as dbc
from flask import request
from sessions_manager import SessionsManager


from settings_property_editor import SettingsPropertyEditor
from post_windows import MonitorWindow

setting1 = SettingsPropertyEditor(app, SessionsManager)
setting2 = SettingsPropertyEditor(app, SessionsManager)
setting3 = SettingsPropertyEditor(app, SessionsManager)


def app_layout():
    user_id = request.authorization["username"]
    session_id = "session-0"
    sessions_manager = SessionsManager(app, app_layout.user_id, session_id)
    sessions_manager.add_session("53583", None)

    return dbc.Container(
        children=[
            html.Data(id="session-id", value="session-0"),
            dbc.Row(
                children=[
                    dbc.Col(
                        [
                            setting1(user_id, session_id, "remote:setup/models/viscous:"),
                            setting2(
                                user_id,
                                session_id,
                                "remote:solution/initialization:",
                                ["standard-initialize"],
                            ),
                            setting3(
                                user_id,
                                session_id,
                                "remote:solution/run_calculation:",
                                ["iterate"],
                            ),
                        ],
                        width="auto",
                        style={"width": "350px"},
                    ),
                    dbc.Col([MonitorWindow(app, user_id, session_id, SessionsManager)()]),
                ],
            ),
        ],
    )
