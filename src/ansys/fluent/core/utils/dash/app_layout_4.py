import dash
from app_defn import app
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash import Input, Output, State, ALL
from flask import request
from sessions_manager import SessionsManager


from local_property_editor import LocalPropertyEditor
from post_windows import GraphicsWindowCollection

local_editor = LocalPropertyEditor(app, SessionsManager)


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
                            dcc.Dropdown(
                                id="post-object-type",
                                options=["Mesh", "Surface", "Contour", "Vector"],
                                value="Contour",
                                style={"padding": "10px 5px 5px 5px"},
                            ),
                            html.Div(id="post-object-container"),
                        ],
                        width="auto",
                        style={"width": "350px"},
                    ),
                    dbc.Col(
                        [
                            GraphicsWindowCollection(
                                app, user_id, session_id, SessionsManager
                            )()
                        ]
                    ),
                ],
            ),
        ],
    )


@app.callback(
    Output("post-object-container", "children"),
    Input("post-object-type", "value"),
    State("connection-id", "data"),
    State("session-id", "value"),
)
def render_widget(post_object_type, user_id, session_id):
    return local_editor(user_id, session_id, f"local:{post_object_type}:0")
