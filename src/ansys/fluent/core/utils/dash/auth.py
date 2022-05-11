import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
import plotly

# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = {"hello": "world"}

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)

app.layout = html.Div(
    [
        html.H1("Welcome to the app"),
        html.H3("You are successfully authorized"),
        dcc.Dropdown(["A", "B"], "A", id="dropdown"),
        dcc.Graph(id="graph"),
    ],
    className="container",
)


@app.callback(
    dash.dependencies.Output("graph", "figure"),
    [dash.dependencies.Input("dropdown", "value")],
)
def update_graph(dropdown_value):
    return {
        "layout": {
            "title": "Graph of {}".format(dropdown_value),
            "margin": {"l": 20, "b": 20, "r": 10, "t": 60},
        },
        "data": [{"x": [1, 2, 3], "y": [4, 1, 2]}],
    }


if __name__ == "__main__":
    app.run_server(debug=True)
