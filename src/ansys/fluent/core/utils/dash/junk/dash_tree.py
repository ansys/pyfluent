import dash
import dash_html_components as html
import dash_treeview_antd
from dash.dependencies import Input, Output

app = dash.Dash("")

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

app.layout = html.Div(
    [
        dash_treeview_antd.TreeView(
            id="input",
            multiple=True,
            # checkable=True,
            # checked=['0-0-1'],
            # selected=[],
            expanded=["0"],
            data={
                "title": "Parent",
                "key": "0",
                "children": [
                    {
                        "title": "Child",
                        "key": "0-0",
                        "children": [
                            {"title": "Subchild1", "key": "0-0-1"},
                            {"title": "Subchild2", "key": "0-0-2"},
                            {
                                "title": "Subchild3",
                                "key": "0-0-3",
                                "children": [
                                    {"title": "Subchild1", "key": "0-0-3-1"},
                                    {"title": "Subchild2", "key": "0-0-3-2"},
                                    {
                                        "title": "Subchild3",
                                        "key": "0-0-3-3",
                                    },
                                ],
                            },
                        ],
                    }
                ],
            },
        ),
        html.Div(id="output-checked"),
        html.Div(id="output-selected"),
        html.Div(id="output-expanded"),
    ]
)


@app.callback(Output("output-checked", "children"), [Input("input", "checked")])
def _display_checked(checked):
    return "You have checked {}".format(checked)


@app.callback(Output("output-selected", "children"), [Input("input", "selected")])
def _display_selected(selected):
    return "You have checked {}".format(selected)


@app.callback(Output("output-expanded", "children"), [Input("input", "expanded")])
def _display_expanded(expanded):
    return "You have selected {}".format(expanded)


if __name__ == "__main__":
    app.run_server(debug=True)
