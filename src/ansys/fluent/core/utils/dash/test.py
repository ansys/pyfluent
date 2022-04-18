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
import uuid
from dash_vtk.utils import presets

random.seed(42)


from ansys.fluent.post import set_config
from ansys.fluent.core.session  import Session
session =Session.create_from_server_info_file("E:\\ajain\\Demo\\pyApp\\pyvista\\server.txt", False)

from ansys.fluent.post import set_config
set_config(blocking=False)
#import module



from ansys.fluent.post.pyvista.pyvista_windows_manager import PyVistaWindow

def toDropOption(name):
    return {"label": name, "value": name}


# Get point cloud data from PyVista
uniformGrid = examples.download_crater_topo()
subset = uniformGrid.extract_subset((500, 900, 400, 800, 0, 0), (5, 5, 1))
   
def update_vtk_fun(obj):
        if obj.__class__.__name__ == "Mesh":
            return update_vtk_fun_mesh(obj)
        elif obj.__class__.__name__ == "Surface":
            return update_vtk_fun_field(obj) 
        elif obj.__class__.__name__ == "Contour":
            return update_vtk_fun_field(obj) 

   
def update_vtk_fun_field(obj):
    try:
        set_config(blocking=True)   
        surface_iter = iter([obj._name]) if obj.__class__.__name__ == "Surface" else iter(obj.surfaces_list())
        field = obj.surface.iso_surface.field() if obj.__class__.__name__ == "Surface" else obj.field()
        node_values = True if obj.__class__.__name__ == "Surface" else obj.node_values()
        #print(obj.surface)
        win = PyVistaWindow("x", obj)
        if obj.__class__.__name__ == "Surface":
            surface_data, scalar_field_data =  win.fetch_surface_data(obj) 
        elif obj.__class__.__name__ == "Contour":
            surface_data, scalar_field_data =  win.fetch_contour_data(obj) 
        elif obj.__class__.__name__ == "Vector":
            pass        
        print('update_vtk_fun', field, 'surface_data', surface_data, 'scalar_field_data', scalar_field_data) 
        
        fields_data = []  
        fields_min  = None 
        fields_max  = None 
        #print('update_vtk_fun', contour1())
        for surface_id, mesh_data in surface_data.items():
            scalar_field  = scalar_field_data[surface_id][field]
            range_min = np.amin(scalar_field)
            range_max = np.amax(scalar_field) 
            fields_min =  min(fields_min, range_min) if fields_min else range_min
            fields_max =  max(fields_max, range_max) if fields_max else range_max       
            fields_data.append([mesh_data["vertices"], mesh_data["faces"], scalar_field, next(surface_iter)])
        fields_range = [fields_min, fields_max]
        print(fields_data, fields_range)
    except Exception as e:
        print(e)
        return [], None     
    return [[
        dash_vtk.GeometryRepresentation(
            id="vtk-representation-"+field_data[3],
            children=[
                dash_vtk.PolyData(
                    id=f"vtk-polydata-{'point-data' if node_values else 'cell-data'}"+field_data[3],
                    points=field_data[0],
                    polys=field_data[1],
                    children=[
                        dash_vtk.PointData(
                            [
                                dash_vtk.DataArray(
                                    id="vtk-array-point-data"+field_data[3],
                                    registration="setScalars",
                                    name="vtk-array-point-data"+field_data[3],
                                    values=field_data[2],
                                )
                            ]
                        )
                        if node_values else
                        dash_vtk.CellData(
                            [
                                dash_vtk.DataArray(
                                    id="vtk-array-cell-data"+field_data[3],
                                    registration="setScalars",
                                    name="vtk-array-cell-data"+field_data[3],
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
            
            
            property={"edgeVisibility": obj.show_edges(), "showScalarBar" : True, "scalarBarTitle" : field,},            
        )
        for field_data in fields_data
    ],
     random.random(),
    ]

def update_vtk_fun_mesh(obj):
    try:
        set_config(blocking=True)   
        surface_iter = iter([obj._name]) if obj.__class__.__name__ == "Surface" else iter(obj.surfaces_list())       
        win = PyVistaWindow("x", obj)
        if obj.__class__.__name__ == "Mesh":
            surface_data =  win.fetch_mesh_data(obj) 
        elif obj.__class__.__name__ == "Surface":
            surface_data, scalar_field_data =  win.fetch_surface_data(obj) 
       
        print('update_vtk_fun', 'surface_data', surface_data) 
        
        fields_data = []  
        for surface_id, mesh_data in surface_data.items():               
            fields_data.append([mesh_data["vertices"], mesh_data["faces"], next(surface_iter)])       
        print(fields_data)
    except Exception as e:
        print(e)
        return [], None     
    return [[
        dash_vtk.GeometryRepresentation(
            id="vtk-representation-"+field_data[2],
            children=[
                dash_vtk.Mesh(
                    id=f"vtk-mesh-"+field_data[2],
                    state = {"mesh":
                    {"points":field_data[0],
                    "polys":field_data[1],}
                    }
                )
                #for field_data in fields_data
            ],                                                
            property={"edgeVisibility": obj.show_edges()},            
        )
        for field_data in fields_data
    ],
     random.random(),
    ]
        

def get_surfaces():
    set_config(blocking=True)
    graphics_session1 = Graphics(session)
    contour1 = graphics_session1.Contours["contour-1"]    
    return contour1.surfaces_list.allowed_values    
        

#points, polys, elevation, color_range = updateWarp(1)
#print(points, polys, elevation, color_range)
# Setup VTK rendering of PointCloud


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.config.suppress_callback_exceptions=True


external_stylesheets = [
    # Dash CSS
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    # Loading screen CSS
    'https://codepen.io/chriddyp/pen/brPBPO.css']

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#server = app.server

#vtk_view = dash_vtk.View(
#    id="vtk-view",    
#    pickingModes=["hover"],
#    children=[       
#    ],
#)


def serve_layout():
    session_id = str(uuid.uuid4())


    return  dbc.Container(
    fluid=True,
    style={"height": "100vh"},
    children=[
        dcc.Store(data=session_id, id='session-id'),
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
               # dbc.Col(
               #     children=dcc.Dropdown(
               #         id="dropdown-surfaces",
               #         options=list(map(toDropOption, get_surfaces())),
               #         value= [],
               #         multi=True
               #     ),
               # ),
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
                dbc.Col(
                    children=dbc.Button(
                        "Restore View",
                        id="restore-view",                        
                    ),
                ),                
                
                                
            ],
            style={"height": "12%", "alignItems": "center"},
        ),
        GraphicsWidget(app, update_vtk_fun).refresh(),
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
app.layout = serve_layout








if __name__ == "__main__":
    app.run_server(debug=True)