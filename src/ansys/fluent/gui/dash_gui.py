from app_defn import app
from callbacks.general import register_callbacks
from dash import dcc, html
from layouts.main import app_layout


def get_default_components():
    return [
        html.Data(
            id="uuid-id",
            # value=user_name_to_session_map.get(user_id, [[None, ""]])[0][1],
        ),
        dcc.Interval(
            id="interval-component",
            interval=1 * 1000,
            n_intervals=0,
        ),
        dcc.Store(data="AnsysUser", id="user-id"),
        dcc.Loading(
            id="loading-session",
            type="default",
            children=html.Data(id="session-id", value="session-0"),
        ),
        html.Data(id="object-id"),
        html.Data(id="tree-view-selection"),
        html.Data(id="tab-content-created"),
        html.Data(id="need-to-data-fetch", value="no"),
        dcc.Loading(
            className="dcc_loader",
            id="loading-command",
            type="default",
            children=html.Data(id="command-output"),
        ),
    ]


def mod_app_layout():
    layout = app_layout()
    layout.children += get_default_components()
    return layout


app.layout = mod_app_layout

register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True, port=8800)
