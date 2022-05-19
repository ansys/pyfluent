"""Module proving post window components."""

from typing import List, Optional, Tuple

from app_defn import app
import dash
from dash import ALL, Input, Output, dcc, html, no_update
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_vtk
import pandas as pd
import plotly.graph_objs as go

from ansys.fluent.gui.components.component_base import ComponentBase
from ansys.fluent.gui.components.objects_handle import LocalObjectsHandle
from ansys.fluent.gui.components.post_representation import (
    get_graphics_representation,
    get_plot_representation,
)
from ansys.fluent.gui.components.sessions_handle import SessionsHandle
from ansys.fluent.gui.components.state_manager import StateManager

pd.options.plotting.backend = "plotly"


class PostWindow(ComponentBase):

    _objects = {}

    def __init__(self, user_id, session_id, window_type, index):
        unique_id = f"{user_id}-{session_id}-{window_type}-{'default' if index is None else index}"
        post_window = PostWindow._objects.get(unique_id)
        if not post_window:
            PostWindow._objects[unique_id] = self.__dict__
            self._unique_id = unique_id
            self._user_id = user_id
            self._session_id = session_id
            self._index = index
            self._window_type = window_type
            self._windows = [0]
            self._active_window = 0
            self._post_representation = {}
            self._window_data = {}

            @app.callback(
                Output(f"post-window-container-{self._unique_id}", "children"),
                Input(
                    {"type": "post-window-tabs-updated", "index": ALL},
                    "n_clicks",
                ),
                prevent_initial_call=True,
            )
            def update_tabs(
                n_clicks,
            ):
                ctx = dash.callback_context
                triggered_value = ctx.triggered[0]["value"]
                triggered_from = eval(ctx.triggered[0]["prop_id"].split(".")[0])
                if not triggered_value:
                    raise PreventUpdate
                unique_id, opr = triggered_from["index"].split(":")
                if unique_id != self._unique_id:
                    raise PreventUpdate
                if opr == "add":
                    id = 0
                    while True:
                        if id not in self._windows:
                            break
                        id = id + 1
                    self._active_window = id
                    self._windows.append(id)
                elif opr == "remove":
                    if len(self._windows) == 1:
                        raise PreventUpdate
                    if self._post_representation.get(self._active_window):
                        del self._post_representation[self._active_window]
                    if self._window_data.get(self._active_window):
                        del self._window_data[self._active_window]
                    index = self._windows.index(self._active_window)
                    new_index = (
                        self._windows[index + 1]
                        if index == 0
                        else self._windows[index - 1]
                    )
                    self._windows.remove(self._active_window)
                    self._active_window = new_index
                return self.render()

            @app.callback(
                Output(f"auto-refresh-value-{self._unique_id}", "value"),
                Input(
                    {"type": "auto-refresh-switch", "index": ALL},
                    "value",
                ),
            )
            def store_auto_update(auto_update):
                ctx = dash.callback_context
                triggered_value = ctx.triggered[0]["value"]
                if triggered_value is None:
                    raise PreventUpdate
                user_id, session_id, window_type = eval(
                    ctx.triggered[0]["prop_id"].split(".")[0]
                )["index"].split(":")
                if (
                    user_id != self._user_id
                    or session_id != self._session_id
                    or window_type != self._window_type
                ):
                    raise PreventUpdate
                active_window_data = self._window_data.get(self._active_window)
                if not active_window_data:
                    active_window_data = self._window_data[self._active_window] = {}
                active_window_data["auto-refresh"] = triggered_value
                return str(triggered_value)

            @app.callback(
                Output(f"post-window-tab-content-{self._unique_id}", "children"),
                Output(
                    {
                        "type": "auto-refresh-switch",
                        "index": f"{self._user_id}:{self._session_id}:{self._window_type}",
                    },
                    "value",
                ),
                Input(
                    {"type": "post-render-button", "index": ALL},
                    "n_clicks",
                ),
                Input(
                    {"type": "refresh-button", "index": ALL},
                    "n_clicks",
                ),
                Input(f"post-window-tabs-{self._unique_id}", "active_tab"),
                Input("auto-refresh", "value"),
                prevent_initial_call=True,
            )
            def refresh_post_window(
                n_clicks,
                refresh_clicks,
                active_tab,
                refresh,
            ):
                with StateManager.BusyWith(
                    self._user_id,
                    self._session_id,
                    SessionsHandle,
                    f"post-window-{self._unique_id}",
                ):
                    ctx = dash.callback_context
                    triggered_value = ctx.triggered[0]["value"]
                    if not triggered_value:
                        raise PreventUpdate
                    try:
                        triggered_data = eval(ctx.triggered[0]["prop_id"].split(".")[0])
                        triggered_from = triggered_data["type"]
                    except NameError:
                        triggered_from = ctx.triggered[0]["prop_id"].split(".")[0]
                    if triggered_from == "auto-refresh" and not self._window_data.get(
                        self._active_window, {}
                    ).get("auto-refresh", False):
                        raise PreventUpdate
                    event_info = SessionsHandle(
                        self._user_id, self._session_id
                    ).get_event_info("IterationEndedEvent")
                    if triggered_from == "post-render-button":
                        (
                            user_id,
                            session_id,
                            location_id,
                            object_path,
                            object_name,
                            editor_index,
                        ) = triggered_data["index"].split(":")
                        if (
                            int(editor_index) != self._index
                            or not self._is_type_supported(object_path)
                            or user_id != self._user_id
                            or session_id != self._session_id
                        ):
                            raise PreventUpdate
                        handle = LocalObjectsHandle()

                        active_window_data = self._window_data.get(int(active_tab))
                        if not active_window_data:
                            active_window_data = self._window_data[int(active_tab)] = {}
                        active_window_data["object"] = handle.get_object(
                            user_id, session_id, object_path, object_name
                        )
                        active_window_data["index"] = (
                            event_info.index if event_info else None
                        )

                    if (
                        triggered_from == "refresh-button"
                        and triggered_data["index"] != self._unique_id
                    ):
                        raise PreventUpdate
                    self._active_window = int(active_tab)
                    data = self._refresh_tab(self._active_window, triggered_from)
                    return data, self._window_data.get(self._active_window, {}).get(
                        "auto-refresh", False
                    )

        else:
            self.__dict__ = post_window

    def copy_from(self, user_id: str, session_id: str) -> None:
        source = PostWindow(
            user_id,
            session_id,
            self._window_type,
        )
        """Copy state from another window.
        Parameters
        ----------
        user_id : str
            User ID.
        session_id : str
            Session ID.
        Returns
        --------
        None
        """
        self._windows = source._windows
        self._window_data = source._window_data
        self._post_representation = source._post_representation

    def __call__(
        self,
        component_height: Optional[int] = 1000,
        init_data: Optional[List[Tuple[str, str]]] = [],
    ) -> html.Div:
        """Render customized ``GraphicsWindow`` or ``PlotWindow`` component within container.
        Parameters
        ----------
        component_height : int, optional
            Component height in px.
        init_data: List[Tuple[str, str]], optional
            List of Tuple of `object path` and `object name`. These object will be automatically displayed
            while component is rendered. For example, It can be used to display mesh outline.
        Returns
        --------
        html.Div
            Customized component within html.Div container.
        """
        handle = LocalObjectsHandle()
        self._component_height = component_height
        for index, object_data in enumerate(init_data):
            if index != 0:
                self._windows.append(index)
            self._window_data[index] = {
                "object": handle.get_object(
                    self._user_id, self._session_id, *object_data
                ),
                "index": None,
            }
        return html.Div(
            self.render(),
            style={
                "height": f"{self._component_height-55}px",
                "overflow-y": "auto",
                "overflow-x": "hidden",
            },
            id=f"post-window-container-{self._unique_id}",
        )

    def render(self) -> dbc.Row:
        """Render PostWindow i.e ``GraphicsWindow`` or ``PlotWindow`` component.
        Parameters
        ----------
        None

        Returns
        --------
        dbc.Row
            dbc.Row as ``PostWindow`` component.
        """
        return [
            dbc.Row(
                [
                    html.Data(id=f"auto-refresh-value-{self._unique_id}"),
                    dbc.Col(
                        dbc.Tabs(
                            [
                                dbc.Tab(label=f"window-{window}", tab_id=f"{window}")
                                for window in self._windows
                            ],
                            id=f"post-window-tabs-{self._unique_id}",
                            active_tab=f"{self._active_window}",
                            style={
                                "margin": "10px 0px 0px 0px",
                                "padding": "4px 4px 0px 4px",
                            },
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                dbc.Switch(
                                    id={
                                        "type": "auto-refresh-switch",
                                        "index": f"{self._user_id}:{self._session_id}:{self._window_type}",
                                    },
                                    style={
                                        "height": "30px",
                                        "padding": "2px 2px 2px 2px",
                                    },
                                ),
                                html.Img(
                                    src="/assets/icons/refresh.png",
                                    style={
                                        "height": "30px",
                                        "padding": "2px 2px 2px 2px",
                                    },
                                    id={
                                        "type": "refresh-button",
                                        "index": f"{self._unique_id}",
                                    },
                                    className="button",
                                ),
                                html.Img(
                                    src="/assets/icons/add.png",
                                    style={
                                        "height": "30px",
                                        "padding": "2px 2px 2px 2px",
                                    },
                                    id={
                                        "type": "post-window-tabs-updated",
                                        "index": f"{self._unique_id}:add",
                                    },
                                    className="button",
                                ),
                                html.Img(
                                    src="/assets/icons/remove.png",
                                    style={
                                        "height": "30px",
                                        "padding": "2px 2px 2px 2px",
                                    },
                                    id={
                                        "type": "post-window-tabs-updated",
                                        "index": f"{self._unique_id}:remove",
                                    },
                                    className="button",
                                ),
                            ],
                            style={
                                "padding": "4px 4px 4px 4px",
                                "display": "flex",
                                "flex-direction": "row",
                            },
                        ),
                        width="auto",
                    ),
                ]
            ),
            html.Div(
                id=f"post-window-tab-content-{self._unique_id}",
                style={"padding": "4px 4px 0px 4px"},
                children=self._refresh_tab(self._active_window),
            ),
        ]

    #   Private methods
    def _refresh_tab(self, active_tab, triggered_from=None):
        with StateManager.BusyWith(
            self._user_id,
            self._session_id,
            SessionsHandle,
            f"post-window-{self._unique_id}1",
        ):
            event_info = SessionsHandle(self._user_id, self._session_id).get_event_info(
                "IterationEndedEvent"
            )
            obj = self._window_data.get(active_tab, {}).get("object")
            index = self._window_data.get(active_tab, {}).get("index")
            if triggered_from in ("post-render-button", "refresh-button"):
                return self._get_updated_post_representation(obj)
            elif triggered_from == "auto-refresh":
                if index == event_info.index if event_info else None:
                    return no_update
                else:
                    return self._get_updated_post_representation(obj)
            else:
                # print(obj, self._active_window)
                if (
                    obj is not None
                    and self._post_representation.get(self._active_window) is None
                ):
                    return self._get_updated_post_representation(obj)
                else:
                    return self._get_stored_post_representation()


class PlotWindow(PostWindow):
    """``PlotWindow`` component.

    Component to display plots.
    """

    def __init__(self, user_id, session_id, index=None):
        super().__init__(user_id, session_id, "plot", index)

    def _get_graph(self):
        return [
            dcc.Graph(
                figure=self._post_representation.get(
                    self._active_window, get_plot_representation(None)
                ),
                style={"height": f"{self._component_height-115}px"},
            )
        ]

    def _is_type_supported(self, type):
        return LocalObjectsHandle().get_handle(type).type == "plot"

    def _get_stored_post_representation(self):
        return [
            html.Div(
                id=f"post-viewer-{self._unique_id}",
                style={"height": "100%"},
                children=self._get_graph(),
            )
        ]

    def _get_updated_post_representation(self, obj):
        if obj is None:
            raise PreventUpdate
        self._post_representation[self._active_window] = get_plot_representation(obj)
        return self._get_stored_post_representation()


class GraphicsWindow(PostWindow):
    """``GraphicsWindow`` component.

    Component to display graphics.
    """

    def __init__(self, user_id, session_id, index=None):
        super().__init__(user_id, session_id, "graphics", index)
        self._visible_index = 0

    def _is_type_supported(self, type):
        return LocalObjectsHandle().get_handle(type).type == "graphics"

    def _get_colorbar(self):
        representation = self._post_representation.get(self._active_window)
        color_bar_data = representation[1]
        return self._make_colorbar(color_bar_data[0], color_bar_data[1:])

    def _get_stored_post_representation(self):
        self._visible_index += 1
        representation = self._post_representation.get(self._active_window)
        content = [
            dbc.Col(
                dash_vtk.View(
                    id=f"post-viewer-{self._unique_id}-{self._visible_index}",
                    children=representation[0] if representation else [],
                    style={"height": f"{self._component_height-115}px"},
                )
            )
        ]
        if representation and representation[1]:
            content.append(
                dbc.Col(
                    dcc.Graph(
                        id=f"color-bar-{self._unique_id}",
                        figure=self._get_colorbar(),
                    ),
                    width="auto",
                )
            )

        return [
            dbc.Row(
                content,
                className="g-0",
            )
        ]

    def _get_updated_post_representation(self, obj):
        if obj is None:
            raise PreventUpdate
        self._post_representation[self._active_window] = get_graphics_representation(
            obj
        )
        return self._get_stored_post_representation()

    def _make_colorbar(self, title, rng, bgnd="rgb(51, 76, 102)"):
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                marker=dict(
                    colorscale="rainbow",
                    showscale=True,
                    cmin=rng[0],
                    cmax=rng[1],
                    colorbar=dict(
                        title_text=title,
                        title_font_color="white",
                        title_side="top",
                        thicknessmode="pixels",
                        thickness=50,
                        #  lenmode="pixels", len=200,
                        yanchor="middle",
                        y=0.5,
                        ypad=10,
                        xanchor="left",
                        x=0.0,
                        xpad=10,
                        ticks="outside",
                        tickcolor="white",
                        tickfont={"color": "white"}
                        #  dtick=5
                    ),
                ),
                hoverinfo="none",
            )
        )
        fig.update_layout(
            width=150,
            height=self._component_height - 115,  # px
            margin={"b": 0, "l": 0, "r": 0, "t": 0},
            autosize=False,
            plot_bgcolor=bgnd,
        )
        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)
        return fig


class MonitorWindow(ComponentBase):
    """``MonitorWindow`` component.

    Component to plot monitors.
    """

    _objects = {}

    def __init__(self, user_id, session_id, index=None):
        unique_id = f"{user_id}-{session_id}{'defaut' if index is None else index}"
        monitor_window = MonitorWindow._objects.get(unique_id)
        if not monitor_window:
            MonitorWindow._objects[unique_id] = self.__dict__
            self._unique_id = unique_id
            self._user_id = user_id
            self._session_id = session_id

            @app.callback(
                Output(f"monitor-tab-content-{self._unique_id}", "children"),
                Input(f"monitor-tabs-{self._unique_id}", "active_tab"),
                Input("auto-refresh", "value"),
            )
            def refresh_monitor(active_tab, fetch_data):
                with StateManager.BusyWith(
                    self._user_id,
                    self._session_id,
                    SessionsHandle,
                    f"monitor-window-{self._unique_id}",
                ):
                    return self._get_monitor_graph(
                        active_tab, self._user_id, self._session_id
                    )

        else:
            self.__dict__ = monitor_window

    def __call__(self, component_height: Optional[int] = 1000) -> html.Div:
        """Render customized ``MonitorWindow`` component within container.
        Parameters
        ----------
        component_height : int, optional
            Component height in px.

        Returns
        --------
        html.Div
            Customized ``MonitorWindow`` component within html.Div container.
        """
        self._component_height = component_height
        return html.Div(
            self.render(),
            style={
                "height": f"{self._component_height-55}px",
                "overflow-y": "auto",
                "overflow-x": "hidden",
            },
            id=f"monitor-window-container-{self._unique_id}",
        )

    def render(self):
        """Render ``MonitorWindow`` component.
        Parameters
        ----------
        None

        Returns
        --------
        dbc.Col
            dbc.Col as ``MonitorWindow`` component.
        """
        session = SessionsHandle(self._user_id, self._session_id).session
        monitor_sets = session.monitors_manager.get_monitor_set_names()
        if len(monitor_sets) == 0:
            return []
        return dbc.Col(
            [
                dbc.Tabs(
                    [
                        dbc.Tab(label=monitor_set, tab_id=monitor_set)
                        for monitor_set in monitor_sets
                    ],
                    id=f"monitor-tabs-{self._unique_id}",
                    active_tab=monitor_sets[0],
                    style={
                        "margin": "10px 0px 0px 0px",
                        "padding": "4px 4px 0px 4px",
                    },
                ),
                html.Div(
                    id=f"monitor-tab-content-{self._unique_id}",
                    style={"height": "100%"},
                    children=self._get_monitor_graph(
                        monitor_sets[0], self._user_id, self._session_id
                    ),
                ),
            ],
        )

    def _get_monitor_graph(self, active_tab, user_id, session_id):
        session = SessionsHandle(user_id, session_id).session
        fig = session.monitors_manager.get_monitor_set_plot(active_tab)
        if fig is None:
            print("return blank", active_tab)
            return dcc.Graph(
                figure={},
                style={"height": "100%"},
            )

        if active_tab == "residual":
            fig.update_yaxes(type="log")

        fig.update_layout(
            title={
                "text": session.monitors_manager.get_monitor_set_prop(
                    active_tab, "title"
                ),
                "y": 0.95,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            },
            xaxis_title=session.monitors_manager.get_monitor_set_prop(
                active_tab, "xlabel"
            ),
            yaxis_title=session.monitors_manager.get_monitor_set_prop(
                active_tab, "ylabel"
            ),
            legend_title=session.monitors_manager.get_monitor_set_prop(
                active_tab, active_tab
            ),
            font=dict(family="Courier New, monospace", size=14, color="black"),
        )
        # print("return Graph")
        return dcc.Graph(
            figure=fig,
            style={"height": f"{self._component_height-115}px"},
        )
