from app_defn import app
from dash import dcc, html
import dash_bootstrap_components as dbc
from flask import request
from sessions_manager import SessionsManager


def app_layout():
    user_id = request.authorization["username"]
    session_id = "session-0"
    sessions_manager = SessionsManager(app, app_layout.user_id, session_id)
    sessions_manager.add_session("53583", None)

    return dbc.Container(
        children=[
            html.Data(id="session-id", value="session-0"),
        ],
    )
