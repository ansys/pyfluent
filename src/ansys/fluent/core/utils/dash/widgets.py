from functools import partial
import dash_bootstrap_components as dbc
from dash import html
import dash_core_components as dcc
import dash_vtk
from dash.dependencies import Input, Output, State

from dash.exceptions import PreventUpdate
import re


class GraphicsWidget:
    _fun = None
    _exe_method = None

    def __init__(self, app, obj, update_vtk_fun):
        self.__refresh_bcs = []
        self._app = app
        self._object = obj
        self._vtk_view_id = self.get_unique_name("vtk-view-")
        self._vtk_view = dash_vtk.View(
            id=self._vtk_view_id,
            pickingModes=["hover"],
            children=[],
        )
        self._update_vtk_fun = update_vtk_fun
        self._all_widgets = {}
        self.store_all_widgets(self._object)
        self._all_widgets[self.get_unique_name("display")] = self.get_button(
            "display", self.get_unique_name("display")
        )
        self.create_callback()

    def get_label(self, name):
        name_list = re.split("[^a-zA-Z]", name)
        return " ".join([name.capitalize() for name in name_list])

    def get_unique_name(self, name):
        return name + self._object._name

    def refresh(self):

        return dbc.Row(
            [
                dbc.Col(
                  
                        html.Div(
                            self._vtk_view,
                            style={"height": "100%", "width": "100%"},
                        ),
                        
                   
                    md=9,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(self._object.__class__.__name__),
                            dbc.CardBody(list(self._all_widgets.values())),
                        ],
                        body=True,
                        className="mb-3",
                    ),
                    md=2,
                ),
            ],
            style={"height": "50rem"},
        )

    def create_callback(self):

        inputs = [
            Input(name + "data", "value")
            for name in list(self._all_widgets.keys())[:-1]
        ]
        outputs = [
            Output(name + "container", "style")
            for name in list(self._all_widgets.keys())[:-1]
        ]
        outputs = outputs + [
            Output(name, "value")
            for name in list(self._all_widgets.keys())[:-1]
        ]

        @self._app.callback(*outputs, *inputs)
        def callback(*args):
            self._visible_widgets = []
            self.update_visible_widgets(self._object)
            visible_widgets = [pair[0] for pair in self._visible_widgets]
            widgets_value_map = {
                pair[0]: pair[1] for pair in self._visible_widgets
            }
            widget_values = []
            for value in [
                widgets_value_map[name] if name in visible_widgets else None
                for name in list(self._all_widgets.keys())[:-1]
            ]:
                if isinstance(value, bool):
                    widget_values.append(["selected"] if value else [])
                else:
                    widget_values.append(value)

            return [
                {"display": "block"}
                if name in visible_widgets
                else {"display": "none"}
                for name in list(self._all_widgets.keys())[:-1]
            ] + widget_values

    def store_all_widgets(self, obj):
        for name, value in obj.__dict__.items():
            if name == "_parent":
                continue

            if value.__class__.__class__.__name__ in (
                "PyLocalPropertyMeta",
                "PyLocalObjectMeta",
            ):
                if value.__class__.__class__.__name__ == "PyLocalPropertyMeta":
                    widget = self.get_widget(
                        value,
                        value._type,
                        name,
                        self.get_unique_name(name),
                        getattr(value, "attributes", None),
                    )
                    self._all_widgets[self.get_unique_name(name)] = widget
                else:
                    self.store_all_widgets(value)

    def update_visible_widgets(self, obj):
        for name, value in obj.__dict__.items():
            if name == "_parent":
                continue

            if value.__class__.__class__.__name__ in (
                "PyLocalPropertyMeta",
                "PyLocalObjectMeta",
            ):
                availability = (
                    getattr(obj, "_availability")(name)
                    if hasattr(obj, "_availability")
                    else True
                )
                if not availability:
                    continue
                # print(name, value, value.__class__.__class__.__name__)
                if value.__class__.__class__.__name__ == "PyLocalPropertyMeta":

                    self._visible_widgets.append(
                        (self.get_unique_name(name), value())
                    )
                else:
                    self.update_visible_widgets(value)

    def get_button(self, name, unique_name):
        widget = self._all_widgets.get(unique_name)
        if widget is not None:
            return widget

        button = dbc.Button(self.get_label(name), id=unique_name, n_clicks=0)

        @self._app.callback(
            [
                Output(self._vtk_view_id, "children"),
                Output(self._vtk_view_id, "triggerResetCamera"),
            ],
            Input(unique_name, "n_clicks"),
        )
        def fun(n_clicks):
            return self._update_vtk_fun(self._object)

        return button

    def get_widget(self, obj, type, name, unique_name, attributes):
        widget = self._all_widgets.get(unique_name)
        if widget is not None:
            return widget
        # print(str(type), unique_name)
        if str(type) == "<class 'str'>":
            if attributes and "allowed_values" in attributes:
                widget = dcc.Dropdown(
                    id=unique_name,
                    options=getattr(obj, "allowed_values"),
                    value=obj(),
                )
            else:
                widget = dcc.Input(id=unique_name, type="text", value=obj())
        elif str(type) == "typing.List[str]":
            widget = dcc.Dropdown(
                id=unique_name,
                options=getattr(obj, "allowed_values"),
                value=obj(),
                multi=True,
            )
            # print('widget', widget)
        elif str(type) == "<class 'bool'>":
            widget = dcc.Checklist(
                id=unique_name,
                options={
                    "selected": self.get_label(name),
                },
                value=["selected"] if obj() else [],
                style = {'padding': "5px"},
                labelStyle = {"display": "inline-block"},
                inputStyle = {'padding': "1px 1px 1px 5px"},
            )
        elif str(type) == "<class 'float'>":
            if attributes and "range" in attributes:
                widget = dcc.Input(
                    id=unique_name,
                    type="number",
                    value=obj(),
                    min=getattr(obj, "range")[0],
                    max=getattr(obj, "range")[1],
                )
            else:
                widget = dcc.Input(id=unique_name, type="number", value=obj())
        elif str(type) == "<class 'int'>":
            if attributes and "range" in attributes:
                widget = dcc.Input(
                    id=unique_name,
                    type="number",
                    value=obj(),
                    min=getattr(obj, "range")[0],
                    max=getattr(obj, "range")[1],
                )
            else:
                widget = dcc.Input(id=unique_name, type="number", value=obj())

        # if not widget:
        #    print('return', widget)
        #    return

        @self._app.callback(
            Output(unique_name + "data", "value"),
            Input(unique_name, "value"),
        )
        def update_oject(value):
            #print("update_oject", unique_name, value)
            #self.__old_defn = self._object()
            if str(type) == "<class 'bool'>":
                value = True if value else False
                obj.set_state(value)
            else:
                obj.set_state(value)
            #    self.update_widgets()
            #    return [self.__widgets]
            #    if self._need_to_refresh():
            #       pass
            #        #self.refresh()
            #    else:
            #        for cb in self.__refresh_bcs:
            #            cb()
            return str(value)

        def refresh_bc(widget, obj):
            print("refresh_bc", unique_name, obj())
            if str(type) == "<class 'bool'>":
                widget.value = ["selected"] if obj() else []
            else:
                widget.value = obj()

        w = widget

        self.__refresh_bcs.append(partial(refresh_bc, w, obj))
        if str(type) == "<class 'bool'>":
            widget = html.Div(
                
                [widget, html.Data(id=unique_name + "data")],
                id=unique_name + "container",
            )
        else:
            widget = html.Div(
                [
                    dbc.Label(self.get_label(name)),
                    widget,
                    html.Data(id=unique_name + "data"),
                ],
                id=unique_name + "container",
            )
        return widget
