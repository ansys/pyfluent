"""Module providing graphics represtantion of the post objects."""

from typing import Dict, List, Tuple, Union

import dash_vtk
import numpy as np

from ansys.fluent.post.post_data_extractor import (
    FieldDataExtractor,
    XYPlotDataExtractor,
)


def get_graphics_representation(
    post_object,
) -> Tuple[List[dash_vtk.GeometryRepresentation], Union[List[float], None]]:
    """Get graphics represtantion of the post graphics object i.e. Mesh, Contour, Vector and Surface.
    Parameters
    ----------
    post_object : object
        Post object.

    Returns
    --------
    Tuple[List[dash_vtk.GeometryRepresentation], Union[List[float],None]]
        Tuple contains two items:
        1. List of graphics represtantion (dash_vtk.GeometryRepresentation) for each
           surface in post_object.
        2. List of field name and range if applicable i.e. for contours and vectors.
           Otherwise None.
    """
    if post_object.__class__.__name__ == "Mesh":
        return _get_mesh_representation(post_object)
    elif post_object.__class__.__name__ == "Surface":
        if (
            post_object.surface.type() == "iso-surface"
            and post_object.surface.iso_surface.rendering() == "contour"
        ):
            return _get_contour_representation(post_object)
        else:
            return _get_mesh_representation(post_object)
    elif post_object.__class__.__name__ == "Contour":
        return _get_contour_representation(post_object)
    elif post_object.__class__.__name__ == "Vector":
        return _get_vector_representation(post_object)


def get_plot_representation(post_object) -> Dict:
    """Get graphics represtantion of the plot object i.e. XYPlot.
    Parameters
    ----------
    post_object : object
        Post object.

    Returns
    --------
    Dict
        Dictionary containing plotly figures data.
    """
    return _get_xy_plot_representation(post_object)


def _get_vector_representation(obj):
    """Get vector representation.

    Here vectors are drawn as line segments.
    """
    field_name = obj.vectors_of()
    fields = FieldDataExtractor(obj).fetch_data(
        provide_faces_centroid=True,
        provide_faces_normal=True,
        provide_vertices=False,
        provide_faces=False,
    )
    fields_data = []

    vector_field_magnitude = {}
    for surface_id, field_for_surface in fields.items():

        vector_field = field_for_surface[field_name]
        vector_field_size = vector_field.size
        vector_field.shape = (
            vector_field_size // 3,
            3,
        )
        vector_field_magnitude[surface_id] = {
            field_name: np.linalg.norm(vector_field, axis=1)
        }
        vector_field.shape = (vector_field_size,)
    field_range = _get_range(vector_field_magnitude, field_name)
    for surface_id, field_for_surface in fields.items():
        faces_centroid = field_for_surface["centroid"]
        vector_field = field_for_surface[field_name]
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
            vector_field * field_for_surface["vector-scale"][0] * obj.scale(),
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
        if obj.skip():
            vector_field_magnitude[surface_id][field_name] = vector_field_magnitude[
                surface_id
            ][field_name][:: obj.skip() + 1]
        fields_data.append(
            [
                line_sgements_vertices,
                line_segements_connectivity,
                vector_field_magnitude[surface_id][field_name],
                f"surface-{surface_id}",
            ]
        )

    return [
        dash_vtk.GeometryRepresentation(
            id="vtk-representation-" + field_data[3],
            children=[
                dash_vtk.PolyData(
                    id=f"vtk-polydata-" + field_data[3],
                    points=field_data[0],
                    lines=field_data[1],
                    connectivity="points",
                    children=[
                        dash_vtk.PointData(
                            [
                                dash_vtk.DataArray(
                                    id="vtk-array-point-data" + field_data[3],
                                    registration="setScalars",
                                    name="vtk-array-point-data" + field_data[3],
                                    values=field_data[2] / 2.0 + field_data[2] / 2.0,
                                )
                            ]
                        )
                    ],
                )
            ],
            colorMapPreset="rainbow",
            colorDataRange=field_range,
        )
        for field_data in fields_data
    ] + (_get_mesh_representation(obj)[0] if obj.show_edges() else []), [
        field_name,
        field_range[0],
        field_range[1],
    ]


def _get_range(fields, field_name):
    field_min = None
    field_max = None
    for surface_id, fields_for_surface in fields.items():
        field = fields_for_surface[field_name]
        range_min = np.amin(field)
        range_max = np.amax(field)
        field_min = min(field_min, range_min) if field_min else range_min
        field_max = max(field_max, range_max) if field_max else range_max
    return field_min, field_max


def _get_contour_representation(obj):
    """Get contour representation."""
    field_name = (
        obj.surface.iso_surface.field()
        if obj.__class__.__name__ == "Surface"
        else obj.field()
    )
    node_values = True if obj.__class__.__name__ == "Surface" else obj.node_values()
    fields = FieldDataExtractor(obj).fetch_data()
    field_range = _get_range(fields, field_name)
    return [
        dash_vtk.GeometryRepresentation(
            id=f"vtk-representation-{surface_id}",
            children=[
                dash_vtk.PolyData(
                    id=f"vtk-polydata-{'point-data' if node_values else 'cell-data'}-{surface_id}",
                    points=fields_for_surface["vertices"],
                    polys=fields_for_surface["faces"],
                    children=[
                        dash_vtk.PointData(
                            [
                                dash_vtk.DataArray(
                                    id=f"vtk-array-point-data-{surface_id}",
                                    registration="setScalars",
                                    name=f"vtk-array-point-data-{surface_id}",
                                    values=fields_for_surface[field_name],
                                )
                            ]
                        )
                        if node_values
                        else dash_vtk.CellData(
                            [
                                dash_vtk.DataArray(
                                    id=f"vtk-array-cell-data-{surface_id}",
                                    registration="setScalars",
                                    name=f"vtk-array-cell-data-{surface_id}",
                                    values=fields_for_surface[field_name],
                                )
                            ]
                        )
                    ],
                )
            ],
            colorMapPreset="rainbow",
            colorDataRange=field_range,
            property={
                "edgeVisibility": obj.show_edges(),
            },
        )
        for surface_id, fields_for_surface in fields.items()
    ], [field_name, field_range[0], field_range[1]]


def _get_mesh_representation(obj):
    """Get mesh representation."""
    fields = FieldDataExtractor(obj).fetch_data()
    return [
        dash_vtk.GeometryRepresentation(
            id=f"vtk-representation-{surface_id}",
            children=[
                dash_vtk.Mesh(
                    id=f"vtk-mesh-{surface_id}",
                    state={
                        "mesh": {
                            "points": fields_for_surface["vertices"],
                            "polys": fields_for_surface["faces"],
                        }
                    },
                )
            ],
            property={
                "edgeVisibility": obj.show_edges(),
                "faceVisibility": False,
            },
        )
        for surface_id, fields_for_surface in fields.items()
    ], None


def _get_xy_plot_representation(obj):
    """Get xy plot representation."""
    xy_plot_data = XYPlotDataExtractor(obj).fetch_data() if obj else {}
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
        figure_data = dict(
            x=curve_data["xvalues"],
            y=curve_data["yvalues"],
            type="scatter",
            name=curve_name,
        )
        xy_plot_figures_data["data"].append(figure_data)
    return xy_plot_figures_data
