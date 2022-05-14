from functools import partial
import dash_bootstrap_components as dbc
from dash import html, no_update
import dash_core_components as dcc
from dash import Input, Output, State, ALL
import dash

import itertools
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
import dash_vtk
from post_data import update_vtk_fun, update_graph_fun, update_graph_fun_xyplot
from objects_handle import LocalObjectsHandle

from sessions_manager import SessionsManager
from app_defn import app
from ansys.fluent.post import set_config
set_config(blocking=False)



class PostWindowCollection:

    _windows = {}  
    def __init__(self, user_id, session_id, window_type, index):
        unique_id = f"{user_id}-{session_id}-{window_type}-{'default' if index is None else index}"
        window_state = PostWindowCollection._windows.get(unique_id)
        if not window_state:
            PostWindowCollection._windows[unique_id] = self.__dict__
            self._window_type = window_type
            self._state = {}
            self._unique_id = unique_id
            self._windows = [0]
            self._active_window = 0
            self._window_data = {}
            self._index = index 
            self._user_id =  user_id           
            self._session_id =  session_id
            
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
                if not triggered_value :
                    raise PreventUpdate
                unique_id, opr = triggered_from["index"].split(":") 
                if  unique_id!=self._unique_id:
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
                    if self._state.get(self._active_window):
                        del self._state[self._active_window]
                    if self._window_data.get(self._active_window):
                        del self._window_data[self._active_window]                        
                    index = self._windows.index(self._active_window)
                    new_index = (
                        self._windows[index + 1] if index == 0 else self._windows[index - 1]
                    )
                    self._windows.remove(self._active_window)
                    self._active_window = new_index  
                return self.get_widgets()                    
                                    
                    
                                                    
            @app.callback(
                Output(f"post-window-tab-content-{self._unique_id}", "children"),
                Input(
                    {"type": "post-render-button", "index": ALL},
                    "n_clicks",
                ),                
                Input(f"post-window-tabs-{self._unique_id}", "active_tab"),
                Input("need-to-data-fetch", "value"),                                   
                prevent_initial_call=True,
            )
            def refresh_post_window(
                n_clicks,          
                active_tab,
                refresh,                          
            ):
                ctx = dash.callback_context
                triggered_value = ctx.triggered[0]["value"]                
                if not triggered_value :
                    raise PreventUpdate
                    
                try:    
                    triggered_data = eval(ctx.triggered[0]["prop_id"].split(".")[0])
                    triggered_from = triggered_data["type"]                    
                except NameError:
                    triggered_from = ctx.triggered[0]["prop_id"].split(".")[0]
                    pass                 
                                    
                event_info = SessionsManager(self._user_id, self._session_id).get_event_info(
                    "IterationEndedEvent"
                )
                print('refresh_post_window', triggered_from, triggered_value, active_tab)
                if triggered_from == "post-render-button":                                     
                    user_id, session_id, object_location, object_type, object_index, editor_index = triggered_data["index"].split(":")                                       
                    if int(editor_index) != self._index or not self.is_type_supported(object_type) or user_id!=self._user_id or  session_id!=self._session_id:  
                        print('PreventUpdate', int(editor_index) != self._index , not self.is_type_supported(object_type) , user_id!=self._user_id ,  session_id!=self._session_id)                    
                        raise PreventUpdate                        
                    handle = LocalObjectsHandle(SessionsManager)
                    self._window_data[int(active_tab)] = {
                        "object" : handle._get_object(user_id, session_id, object_type, object_index),
                        "index" : event_info.index if event_info else None                                       
                    }                    
                self._active_window =  int(active_tab)
                obj = self._window_data.get(int(active_tab),{}).get("object")
                index = self._window_data.get(int(active_tab),{}).get("index")
                if triggered_from == "post-render-button":  
                    return self.get_updated_post_data(obj) 
                elif triggered_from=="need-to-data-fetch":  
                    if index== event_info.index if event_info else None:
                        return no_update 
                    else:
                        return self.get_updated_post_data(obj) 
                else:                         
                    return self.get_stored_post_data()                                                                                                                 
        else:
            self.__dict__ = window_state                

    def copy_from(self, user_id, session_id):
        source = PostWindowCollection(
            user_id,
            session_id,
            self._window_type,
        )
        self._windows = source._windows
        self._window_data = source._window_data
        self._state = source._state
        
    def get_widgets(self):

        return [
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Tabs(
                                [
                                    dbc.Tab(
                                        label=f"window-{window}", tab_id=f"{window}"
                                    )
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
                                    dbc.Button(
                                        "Add Window",
                                        id={
                                            "type": "post-window-tabs-updated",
                                            "index": f"{self._unique_id}:add",
                                        },
                                        size="sm",
                                        n_clicks=0,
                                        outline=True,
                                        color="secondary",
                                        className="me-1",
                                    ),
                                    dbc.Button(
                                        "Remove Window",
                                        id={
                                            "type": "post-window-tabs-updated",
                                            "index": f"{self._unique_id}:remove",
                                        },
                                        size="sm",
                                        n_clicks=0,
                                        outline=True,
                                        color="secondary",
                                        className="me-1",
                                    ),
                                ],
                                style={
                                    "padding": "4px 4px 4px 4px",
                                },
                            ),
                            width="auto",
                        ),
                    ]
                ),
                html.Div(
                    id=f"post-window-tab-content-{self._unique_id}",
                    style={"padding": "4px 4px 0px 4px", "height": "837px"},
                    children=self.get_stored_post_data(),
                ),
            ]
            
               

    def __call__(self):

        return html.Div(
            self.get_widgets() ,
            style={
                "height": "57rem",
                "overflow-y": "auto",
                "overflow-x": "hidden",
            },
          id=f"post-window-container-{self._unique_id}"  
        )


class PlotWindowCollection(PostWindowCollection):
    def __init__(self, user_id, session_id, index=None):
        super().__init__(user_id, session_id, "plot", index)

    def _get_graph(self):
        return [
            dcc.Graph(
                figure=self._state.get(self._active_window, update_graph_fun_xyplot()),
                style={"height": "100%"},
            )
        ]

    def is_type_supported(self, type):
        return LocalObjectsHandle(SessionsManager).get_handle_type(type)=="plot"
       
    def get_stored_post_data(self):
        return [
            html.Div(
                id=f"post-viewer-{self._unique_id}",
                style={"height": "100%"},
                children=self._get_graph(),
            )
        ]

    def get_updated_post_data(self,obj):       
        if obj is None:
            raise PreventUpdate
        self._state[self._active_window] = update_graph_fun(obj)
        print("data fetched")
        return self.get_stored_post_data()


class GraphicsWindowCollection(PostWindowCollection):
    def __init__(self, user_id, session_id, index=None):
        super().__init__(user_id, session_id, "graphics", index)

    def _get_graphics(self):
        return self._state.get(self._active_window, [[]])[0]

    def _get_colorbar(self):
        color_bar_data = self._state.get(self._active_window, [None, None])[1]
        try:
            return (
                self.make_colorbar(color_bar_data[0], color_bar_data[1:])
                if color_bar_data
                else go.Figure()
            )
        except:
            return go.Figure()

    def is_type_supported(self, type):
        return LocalObjectsHandle(SessionsManager).get_handle_type(type)=="graphics"
        

    def get_stored_post_data(self):       
        content = [
            dbc.Col(
                dash_vtk.View(
                    id=f"post-viewer-{self._unique_id}",
                    pickingModes=["hover"],
                    children=self._get_graphics(),
                    style={"height": "837px"},
                )
            )
        ]
        if self._state.get(self._active_window, [None, None])[1]:
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

    def get_updated_post_data(self, obj):        
        if obj is None:            
            raise PreventUpdate
        color_bar = []
        self._state[self._active_window] = (
            update_vtk_fun(obj, color_bar)[0],
            color_bar,
        )
        return self.get_stored_post_data()

    def make_colorbar(self, title, rng, bgnd="rgb(51, 76, 102)"):
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
            height=837,  # px
            margin={"b": 0, "l": 0, "r": 0, "t": 0},
            autosize=False,
            plot_bgcolor=bgnd,
        )
        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)
        return fig


class MonitorWindow:       
    _windows = {}
    def __init__(self, user_id, session_id, index=None):
        unique_id = f"{user_id}-{session_id}{'defaut' if index is None else index}"
        window_state = MonitorWindow._windows.get(unique_id)
        if not window_state:
            MonitorWindow._windows[unique_id] = self.__dict__   
            self._unique_id = unique_id
            self._user_id = user_id
            self._session_id = session_id                       
            @app.callback(
                Output(f"monitor-tab-content-{self._unique_id}", "children"),
                Input(f"monitor-tabs-{self._unique_id}", "active_tab"),
                Input("need-to-data-fetch", "value"),           
            )
            def refresh_monitor(active_tab, fetch_data):                                    
                return MonitorWindow.get_monitor_data(active_tab, self._user_id, self._session_id)            
        else:
            self.__dict__ = window_state    
        

    @classmethod
    def get_monitor_data(cls, active_tab, user_id, session_id):             
        session = SessionsManager(user_id, session_id).session
        fig = session.monitors_manager.get_monitor_set_data(active_tab)
        if fig is None:
            PostWindowCollection._is_executing = False
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
        PostWindowCollection._is_executing = False
        print("return Graph")
        return dcc.Graph(figure=fig, style={"height": "100%"},)

    def __call__(self, style={}):       
        session = SessionsManager(self._user_id, self._session_id).session
        monitor_sets = session.monitors_manager.get_monitor_sets_name()
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
                    children = MonitorWindow.get_monitor_data(monitor_sets[0], self._user_id, self._session_id)
                ),
            ],
            style={"height": "837px"}.update(style),
        )
