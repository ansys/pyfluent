"""Module to instantiate and set app properties."""

import dash
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
    suppress_callback_exceptions=True,
    title="PyFluent",
)
app._favicon = "assets/favicon.ico"
MAX_SESSION_COUNT = 6
DEFAULT_USER_ID = "AnsysUser"
