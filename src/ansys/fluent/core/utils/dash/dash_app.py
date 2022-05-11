import dash
import dash_auth

import dash_bootstrap_components as dbc

from users_info import VALID_USERNAME_PASSWORD_PAIRS
from app_layout import app_layout
from callbacks import register_callbacks

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
    suppress_callback_exceptions=True,
    title="Ansys PyFluent",
)
app._favicon = "assets/favicon.ico"
dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)
app.layout = app_layout
app_layout.app=app
register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True, port=8800)
