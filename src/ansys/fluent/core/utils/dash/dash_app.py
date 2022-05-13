import dash
import dash_auth
from dash import dcc, html
import dash_bootstrap_components as dbc

from users_info import VALID_USERNAME_PASSWORD_PAIRS
from app_layout import app_layout
from callbacks import register_callbacks, user_name_to_session_map

from flask import request

from app_defn import app


def get_storage():
    user_id = request.authorization["username"]
    return [
        
        dcc.Interval(
            id="interval-component",
            interval=1 * 1000,
            n_intervals=0,
        ),
        dcc.Store(data=user_id, id="connection-id"),
        html.Data(id="window-id", value="0"),
        html.Data(id="object-id"),
        html.Data(
            id="uuid-id",
            value=user_name_to_session_map.get(user_id, [[None, ""]])[0][1],
        ),        
        
        
        html.Data(id="tree-view-selection"),
        
        html.Data(id="graphics-button-clicked"),
        html.Data(id="plot-button-clicked"),
        html.Data(id="save-button-clicked"),
        html.Data(id="delete-button-clicked"),
        html.Data(id="tab-content-created"),
        html.Data(id="refresh-property-editor"),
        html.Data(id="need-to-data-fetch", value="no"),
        html.Data(id="command-output"),

    ]


def mod_app_layout():

    storage = get_storage()    
    container = app_layout()
    container.children = storage + container.children
    return container


app.layout = mod_app_layout

register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True, port=8800)
