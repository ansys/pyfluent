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

def update_vtk_fun(obj):
        if obj.__class__.__name__ == "Mesh":
            return update_vtk_fun_mesh(obj)
        elif obj.__class__.__name__ == "Surface":
            return update_vtk_fun_field(obj) 
        elif obj.__class__.__name__ == "Contour":
            return update_vtk_fun_field(obj) 
        elif obj.__class__.__name__ == "Vector":
            return update_vtk_fun_vector(obj)             

def update_vtk_fun_vector(obj):
    try:
        set_config(blocking=True)   
        surface_iter = iter(obj.surfaces_list())
        field = obj.vectors_of()

        
        win = PyVistaWindow("x", obj)
        vector_field_data = win.fetch_vector_data(obj) 
               
        fields_data = []  
        fields_min  = None 
        fields_max  = None        
        for surface_id, vector_data in vector_field_data.items():
        
      
            faces_centroid = vector_data["centroid"]                  
            vector_field  = vector_data[field]
            vector_field_saved  = vector_field
            if obj.skip():   
                faces_centroid.shape = (
                    faces_centroid.size // 3,
                    3,
                )
                vector_field.shape = (
                    vector_field.size // 3,
                    3,
                )                  
                faces_centroid = faces_centroid[:: obj.skip() + 1]
                vector_field = vector_field[:: obj.skip() + 1]  
                faces_centroid = faces_centroid.ravel()
                vector_field = vector_field.ravel()
                
            vector_end_points = np.add(faces_centroid, vector_field*vector_data["vector-scale"][0]*obj.scale())                      
            line_sgements_vertices = np.append(faces_centroid, vector_end_points)                             
            line_segements_connectivity =  [x for l in [ (2, index+1,index+1+faces_centroid.size//3) for index in range(faces_centroid.size//3)] for x in l]
                        
            vector_field_saved.shape = (
                vector_field_saved.size // 3,
                3,
            )            
            velocity_magnitude = np.linalg.norm(
                vector_field_saved, axis=1
            )            
            range_min = np.amin(velocity_magnitude)
            range_max = np.amax(velocity_magnitude) 
            fields_min =  min(fields_min, range_min) if fields_min else range_min
            fields_max =  max(fields_max, range_max) if fields_max else range_max   
            if obj.skip():                
                velocity_magnitude = velocity_magnitude[:: obj.skip() + 1]                      
                
            fields_data.append([vector_data["vertices"], vector_data["faces"], line_sgements_vertices, line_segements_connectivity, velocity_magnitude, next(surface_iter)])            
        fields_range = [fields_min, fields_max]
        
    except Exception as e:
        print(e)
        return [], None     
    return [[
        dash_vtk.GeometryRepresentation(
            id="vtk-representation-"+field_data[5],
            children=[
            
                dash_vtk.PolyData(
                    id=f"vtk-polydata-"+field_data[5],
                    points=field_data[2],
                    lines=field_data[3],
                    connectivity='points',
                    children=[
                        dash_vtk.PointData(
                            [
                                dash_vtk.DataArray(
                                    id="vtk-array-point-data"+field_data[5],
                                    registration="setScalars",
                                    name="vtk-array-point-data"+field_data[5],
                                    values=field_data[4]+field_data[4],
                                )
                            ]
                        )                        
                    ],
                )               
            ]  
                                   
            ,             
            colorMapPreset="Rainbow Blended White",
            colorDataRange=fields_range,
            
            
                      
        )
        for field_data in fields_data
    ]+ (update_vtk_fun_mesh(obj)[0] if obj.show_edges() else []) 
    ,
     random.random(),
    ]

   
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
        print('update_vtk_fun_mesh..',)
        set_config(blocking=True)   
        surface_iter = iter([obj._name]) if obj.__class__.__name__ == "Surface" else iter(obj.surfaces_list())       
        win = PyVistaWindow("x", obj)
        if obj.__class__.__name__ == "Mesh" or obj.__class__.__name__ == "Vector":
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
            property={"edgeVisibility": obj.show_edges(), "faceVisibility":False},            
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
        

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.config.suppress_callback_exceptions=True

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