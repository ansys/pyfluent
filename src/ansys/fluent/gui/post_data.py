import json
import random
import uuid

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import dash_vtk
from dash_vtk.utils import presets
import numpy as np
import pandas as pd
import pyvista as pv
from vtk.util.numpy_support import vtk_to_numpy

random.seed(42)


from ansys.fluent.post import set_config
from ansys.fluent.post.matplotlib.matplot_windows_manager import get_xy_plot_data
from ansys.fluent.post.pyvista.pyvista_windows_manager import (
    DataExtractor,
    PyVistaWindow,
)


def update_graph_fun(obj):
    if obj.__class__.__name__ == "XYPlot":
        return update_graph_fun_xyplot(obj)


def update_graph_fun_xyplot(obj=None):
    try:

        xy_plot_data = get_xy_plot_data(obj) if obj else {}

        # columns_data = {}
        # for curve_name, curve_data in xy_plot_data.items():
        #    columns_data[curve_name] = curve_data["yvalues"]
        #    columns_data["xvalues"] = curve_data["xvalues"]
        # df = pd.DataFrame(columns_data)
        # df.set_index("xvalues", inplace = True)
        # print(df)

        xy_plot_figures_data = {}
        xy_plot_figures_data["data"] = []

        xy_plot_figures_data["layout"] = (
            {
                "title": "XYPlot",
                "xaxis": {"title": ""},
                "yaxis": {"title": obj.y_axis_function()},
                "font": {
                    "color": "black",
                    "family": "Courier New, monospace",
                    "size": 14,
                },
                "template": "plotly",
                "margin": {"t": 60},
            }
            if obj is not None
            else {
                "xaxis": {"visible": False},
                "yaxis": {"visible": False},
                "template": "plotly",
                "annotations": [
                    {
                        "text": "",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {"size": 28},
                    }
                ],
            }
        )

        for curve_name, curve_data in xy_plot_data.items():
            figure_data = {}
            figure_data["x"] = curve_data["xvalues"]
            figure_data["y"] = curve_data["yvalues"]
            figure_data["type"] = "scatter"
            figure_data["name"] = curve_name
            xy_plot_figures_data["data"].append(figure_data)

        return xy_plot_figures_data
    except Exception as e:
        print(e)
        return {}


def update_vtk_fun(obj, color_bar=[]):
    if obj.__class__.__name__ == "Mesh":
        return update_vtk_fun_mesh(obj)
    elif obj.__class__.__name__ == "Surface":
        if (
            obj.surface.type() == "iso-surface"
            and obj.surface.iso_surface.rendering() == "contour"
        ):
            return update_vtk_fun_field(obj, color_bar)
        else:
            return update_vtk_fun_mesh(obj)
    elif obj.__class__.__name__ == "Contour":
        return update_vtk_fun_field(obj, color_bar)
    elif obj.__class__.__name__ == "Vector":
        return update_vtk_fun_vector(obj, color_bar)


def update_vtk_fun_vector(obj, color_bar):
    try:
        set_config(blocking=True)
        surface_iter = iter(obj.surfaces_list())
        field = obj.vectors_of()

        # win = PyVistaWindow("x", obj)
        vector_field_data = DataExtractor(obj).fetch_data()
        color_bar.append(field)
        fields_data = []
        fields_min = None
        fields_max = None
        for surface_id, vector_data in vector_field_data.items():

            faces_centroid = vector_data["centroid"]
            vector_field = vector_data[field]
            vector_field_saved = vector_field
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

            vector_end_points = np.add(
                faces_centroid,
                vector_field * vector_data["vector-scale"][0] * obj.scale(),
            )
            line_sgements_vertices = np.append(faces_centroid, vector_end_points)
            line_segements_connectivity = [
                x
                for l in [
                    (2, index + 1, index + 1 + faces_centroid.size // 3)
                    for index in range(faces_centroid.size // 3)
                ]
                for x in l
            ]

            vector_field_saved.shape = (
                vector_field_saved.size // 3,
                3,
            )
            velocity_magnitude = np.linalg.norm(vector_field_saved, axis=1)
            range_min = np.amin(velocity_magnitude)
            range_max = np.amax(velocity_magnitude)
            fields_min = min(fields_min, range_min) if fields_min else range_min
            fields_max = max(fields_max, range_max) if fields_max else range_max
            if obj.skip():
                velocity_magnitude = velocity_magnitude[:: obj.skip() + 1]

            fields_data.append(
                [
                    vector_data["vertices"],
                    vector_data["faces"],
                    line_sgements_vertices,
                    line_segements_connectivity,
                    velocity_magnitude,
                    next(surface_iter),
                ]
            )
        fields_range = [fields_min, fields_max]
        color_bar.extend(fields_range)
    except Exception as e:
        print(e)
        return [], None
    return [
        [
            dash_vtk.GeometryRepresentation(
                id="vtk-representation-" + field_data[5],
                children=[
                    dash_vtk.PolyData(
                        id=f"vtk-polydata-" + field_data[5],
                        points=field_data[2],
                        lines=field_data[3],
                        connectivity="points",
                        children=[
                            dash_vtk.PointData(
                                [
                                    dash_vtk.DataArray(
                                        id="vtk-array-point-data" + field_data[5],
                                        registration="setScalars",
                                        name="vtk-array-point-data" + field_data[5],
                                        values=field_data[4] + field_data[4],
                                    )
                                ]
                            )
                        ],
                    )
                ],
                colorMapPreset="Rainbow Blended White",
                colorDataRange=fields_range,
            )
            for field_data in fields_data
        ]
        + (update_vtk_fun_mesh(obj)[0] if obj.show_edges() else []),
        random.random(),
    ]


def update_vtk_fun_field(obj, color_bar):
    try:
        set_config(blocking=True)
        surface_iter = (
            iter([obj._name])
            if obj.__class__.__name__ == "Surface"
            else iter(obj.surfaces_list())
        )
        field = (
            obj.surface.iso_surface.field()
            if obj.__class__.__name__ == "Surface"
            else obj.field()
        )
        color_bar.append(field)
        node_values = True if obj.__class__.__name__ == "Surface" else obj.node_values()

        if obj.__class__.__name__ == "Surface":
            surface_data, scalar_field_data = DataExtractor(obj).fetch_data()
        elif obj.__class__.__name__ == "Contour":
            surface_data, scalar_field_data = DataExtractor(obj).fetch_data()

        fields_data = []
        fields_min = None
        fields_max = None
        # print('update_vtk_fun', contour1())
        for surface_id, mesh_data in surface_data.items():
            scalar_field = scalar_field_data[surface_id][field]
            range_min = np.amin(scalar_field)
            range_max = np.amax(scalar_field)
            fields_min = min(fields_min, range_min) if fields_min else range_min
            fields_max = max(fields_max, range_max) if fields_max else range_max
            fields_data.append(
                [
                    mesh_data["vertices"],
                    mesh_data["faces"],
                    scalar_field,
                    next(surface_iter),
                ]
            )
        fields_range = [fields_min, fields_max]
        color_bar.extend(fields_range)
        # print(fields_data, fields_range)
    except Exception as e:
        print(e)
        return [], None
    return [
        [
            dash_vtk.GeometryRepresentation(
                id="vtk-representation-" + field_data[3],
                children=[
                    dash_vtk.PolyData(
                        id=f"vtk-polydata-{'point-data' if node_values else 'cell-data'}"
                        + field_data[3],
                        points=field_data[0],
                        polys=field_data[1],
                        children=[
                            dash_vtk.PointData(
                                [
                                    dash_vtk.DataArray(
                                        id="vtk-array-point-data" + field_data[3],
                                        registration="setScalars",
                                        name="vtk-array-point-data" + field_data[3],
                                        values=field_data[2],
                                    )
                                ]
                            )
                            if node_values
                            else dash_vtk.CellData(
                                [
                                    dash_vtk.DataArray(
                                        id="vtk-array-cell-data" + field_data[3],
                                        registration="setScalars",
                                        name="vtk-array-cell-data" + field_data[3],
                                        values=field_data[2],
                                    )
                                ]
                            )
                        ],
                    )
                    # for field_data in fields_data
                ],
                colorMapPreset="rainbow",
                colorDataRange=fields_range,
                # showScalarBar= True,
                # scalarBarTitle = field,
                property={
                    "edgeVisibility": obj.show_edges(),
                },
            )
            for field_data in fields_data
        ],
        random.random(),
    ]


def update_vtk_fun_mesh(obj):
    try:

        set_config(blocking=True)
        surface_iter = (
            iter([obj._name])
            if obj.__class__.__name__ == "Surface"
            else iter(obj.surfaces_list())
        )

        if obj.__class__.__name__ == "Mesh" or obj.__class__.__name__ == "Vector":
            surface_data = DataExtractor(obj).fetch_data()
        elif obj.__class__.__name__ == "Surface":
            surface_data, scalar_field_data = DataExtractor(obj).fetch_data()

        fields_data = []
        for surface_id, mesh_data in surface_data.items():
            fields_data.append(
                [mesh_data["vertices"], mesh_data["faces"], next(surface_iter)]
            )
        # print(fields_data)
    except Exception as e:
        print(e)
        return [], None
    return [
        [
            dash_vtk.GeometryRepresentation(
                id="vtk-representation-" + field_data[2],
                children=[
                    dash_vtk.Mesh(
                        id=f"vtk-mesh-" + field_data[2],
                        state={
                            "mesh": {
                                "points": field_data[0],
                                "polys": field_data[1],
                            }
                        },
                    )
                    # for field_data in fields_data
                ],
                property={
                    "edgeVisibility": obj.show_edges(),
                    "faceVisibility": False,
                },
            )
            for field_data in fields_data
        ],
        random.random(),
    ]
