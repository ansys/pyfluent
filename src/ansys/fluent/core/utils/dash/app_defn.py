import dash
import dash_auth
import dash_bootstrap_components as dbc
from users_info import VALID_USERNAME_PASSWORD_PAIRS


app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
    suppress_callback_exceptions=True,
    title="Ansys PyFluent",
)
app._favicon = "assets/favicon.ico"
dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)
