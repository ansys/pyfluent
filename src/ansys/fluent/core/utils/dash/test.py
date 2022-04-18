import dash
import dash_vtk
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

from ansys.fluent.core.utils.dash.widgets import GraphicsWidget
import random
import json
import numpy as np
import pyvista as pv
from pyvista import examples
from vtk.util.numpy_support import vtk_to_numpy

from dash_vtk.utils import presets

random.seed(42)


from ansys.fluent.post import set_config
from ansys.fluent.core.session  import Session
session =Session.create_from_server_info_file("E:\\ajain\\Demo\\pyApp\\pyvista\\server.txt", False)

from ansys.fluent.post import set_config
set_config(blocking=False)
#import module

from ansys.fluent.post.pyvista import  Graphics
from ansys.fluent.post.pyvista.pyvista_objects import Contour
from ansys.fluent.post.matplotlib import Plots
from ansys.fluent.post.pyvista.pyvista_windows_manager import (  # noqa: F401
    PyVistaWindow,
)

graphics_session1 = Graphics(session)
contour1 = graphics_session1.Contours["contour-1"]
contour1.field = "velocity-magnitude"
contour1.surfaces_list = ["symmetry"]

contour2 = graphics_session1.Contours["contour-2"]
contour2.field = "temperature"
contour2.surfaces_list = ["wall"]

def toDropOption(name):
    return {"label": name, "value": name}


# Get point cloud data from PyVista
uniformGrid = examples.download_crater_topo()
subset = uniformGrid.extract_subset((500, 900, 400, 800, 0, 0), (5, 5, 1))
   
def update_vtk_fun(obj):
    try:
        set_config(blocking=True)
        contour1 = obj        
        surface_iter = iter(contour1.surfaces_list())
        win = PyVistaWindow("x", contour1)
        surface_data, scalar_field_data =  win.fetch_contour_data(contour1)  
        fields_data = []  
        fields_min  = None 
        fields_max  = None 
        print('update_vtk_fun', contour1.surfaces_list())
        for surface_id, mesh_data in surface_data.items():
            field  = scalar_field_data[surface_id][contour1.field()]
            range_min = np.amin(field)
            range_max = np.amax(field) 
            fields_min =  min(fields_min, range_min) if fields_min else range_min
            fields_max =  max(fields_max, range_max) if fields_max else range_max       
            fields_data.append([mesh_data["vertices"], mesh_data["faces"], field, next(surface_iter)])
        fields_range = [fields_min, fields_max]
    except Exception as e:
        print(e)
        return [], None     
    return [[
        dash_vtk.GeometryRepresentation(
            id="vtk-representation-"+field_data[3],
            children=[
                dash_vtk.PolyData(
                    id="vtk-polydata-"+field_data[3],
                    points=field_data[0],
                    polys=field_data[1],
                    children=[
                        dash_vtk.PointData(
                            [
                                dash_vtk.DataArray(
                                    id="vtk-array-"+field_data[3],
                                    registration="setScalars",
                                    name=field_data[3],
                                    values=field_data[2],
                                )
                            ]
                        )
                    ],
                )
                #for field_data in fields_data
            ],            
            colorMapPreset="Rainbow Blended White",
            colorDataRange=fields_range,
            property={"edgeVisibility": contour1.show_edges()},            
        )
        for field_data in fields_data
    ],
     random.random(),
    ]

def updateWarp(surfaces):
    try:
        set_config(blocking=True)
        graphics_session1 = Graphics(session)
        contour1 = graphics_session1.Contours["contour-1"]
        contour1.field = "velocity-magnitude"
        contour1.surfaces_list = surfaces
        surface_iter = iter(contour1.surfaces_list())
        win = PyVistaWindow("x", contour1)
        surface_data, scalar_field_data =  win.fetch_contour_data(contour1)  
        fields_data = []  
        fields_min  = None 
        fields_max  = None 
        print('updateWarp', contour1.surfaces_list())
        for surface_id, mesh_data in surface_data.items():
            field  = scalar_field_data[surface_id][contour1.field()]
            range_min = np.amin(field)
            range_max = np.amax(field) 
            fields_min =  min(fields_min, range_min) if fields_min else range_min
            fields_max =  max(fields_max, range_max) if fields_max else range_max       
            fields_data.append([mesh_data["vertices"], mesh_data["faces"], field, next(surface_iter)])
        return  fields_data, [fields_min, fields_max]
    except Exception as e:
        print(e)
        None, None         

def get_surfaces():
    set_config(blocking=True)
    graphics_session1 = Graphics(session)
    contour1 = graphics_session1.Contours["contour-1"]    
    return contour1.surfaces_list.allowed_values    
        

#points, polys, elevation, color_range = updateWarp(1)
#print(points, polys, elevation, color_range)
# Setup VTK rendering of PointCloud


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

#vtk_view = dash_vtk.View(
#    id="vtk-view",    
#    pickingModes=["hover"],
#    children=[       
#    ],
#)

app.layout = dbc.Container(
    fluid=True,
    style={"height": "100vh"},
    children=[
        dbc.Row(
            [
                dbc.Col(
                    children=dcc.Slider(
                        id="scale-factor",
                        min=0.1,
                        max=5,
                        step=0.1,
                        value=1,
                        marks={0.1: "0.1", 5: "5"},
                    )
                ),
                dbc.Col(
                    children=dcc.Dropdown(
                        id="dropdown-surfaces",
                        options=list(map(toDropOption, get_surfaces())),
                        value= [],
                        multi=True
                    ),
                ),
                dbc.Col(
                    children=dcc.Checklist(
                        id="toggle-cube-axes",
                        options=[
                            {"label": " Show axis grid", "value": "grid"},
                        ],
                        value=[],
                        labelStyle={"display": "inline-block"},
                    ),
                ),
            ],
            style={"height": "12%", "alignItems": "center"},
        ),
        GraphicsWidget(app, contour1, update_vtk_fun).refresh(),
        # GraphicsWidget(app, contour2, update_vtk_fun).refresh(),
        
        html.Pre(
            id="tooltip",
            style={
                "position": "absolute",
                "bottom": "25px",
                "left": "25px",
                "zIndex": 1,
                "color": "white",
            },
        ),
    ],
)









if __name__ == "__main__":
    app.run_server(debug=True)