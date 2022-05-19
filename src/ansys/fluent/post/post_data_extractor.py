"""Module providing data extractor APIs."""

from typing import Dict

import numpy as np

from ansys.api.fluent.v0.field_data_pb2 import PayloadTag
from ansys.fluent.post.post_object_defns import GraphicsDefn, PlotDefn


class FieldDataExtractor:
    """FieldData DataExtractor."""

    def __init__(self, post_object: GraphicsDefn):
        """Instantiate FieldData DataExtractor.

        Parameters
        ----------
        post_object : GraphicsDefn
            Graphics definition object for which data needs to be extracted.
        """
        self._post_object: GraphicsDefn = post_object

    def fetch_data(self, *args, **kwargs):
        """Fetch data for Graphics object.

        Parameters
        ----------
        None

        Returns
        -------
        Dict[int: Dict[str: np.array]]
            Return dictionary of surfaces id to field name to numpy array.
        """
        if self._post_object.__class__.__name__ == "Mesh":
            return self._fetch_mesh_data(self._post_object, *args, **kwargs)
        elif self._post_object.__class__.__name__ == "Surface":
            return self._fetch_surface_data(self._post_object, *args, **kwargs)
        elif self._post_object.__class__.__name__ == "Contour":
            return self._fetch_contour_data(self._post_object, *args, **kwargs)
        elif self._post_object.__class__.__name__ == "Vector":
            return self._fetch_vector_data(self._post_object, *args, **kwargs)

    def _fetch_mesh_data(self, obj, *args, **kwargs):
        if not obj.surfaces_list():
            raise RuntimeError("Mesh definition is incomplete.")
        obj._pre_display()
        field_info = obj._data_extractor.field_info()
        field_data = obj._data_extractor.field_data()
        surfaces_info = field_info.get_surfaces_info()
        surface_ids = [
            id
            for surf in map(
                obj._data_extractor.remote_surface_name, obj.surfaces_list()
            )
            for id in surfaces_info[surf]["surface_id"]
        ]

        field_data.add_get_surfaces_request(surface_ids, *args, **kwargs)
        surface_tag = 0
        surfaces_data = field_data.get_fields()[surface_tag]
        obj._post_display()
        return surfaces_data

    def _fetch_surface_data(self, obj, *args, **kwargs):
        surface_api = obj._data_extractor.surface_api
        surface_api.create_surface_on_server()
        dummy_object = "dummy_object"
        post_session = obj._get_top_most_parent()
        if (
            obj.surface.type() == "iso-surface"
            and obj.surface.iso_surface.rendering() == "contour"
        ):
            contour = post_session.Contours[dummy_object]
            contour.field = obj.surface.iso_surface.field()
            contour.surfaces_list = [obj._name]
            contour.show_edges = True
            contour.range.auto_range_on.global_range = True
            surface_data = self._fetch_contour_data(contour)
            del post_session.Contours[dummy_object]
        else:
            mesh = post_session.Meshes[dummy_object]
            mesh.surfaces_list = [obj._name]
            mesh.show_edges = True
            surface_data = self._fetch_mesh_data(mesh)
        surface_api.delete_surface_on_server()
        return surface_data

    def _fetch_contour_data(self, obj, *args, **kwargs):
        if not obj.surfaces_list() or not obj.field():
            raise RuntimeError("Contour definition is incomplete.")

        # contour properties
        obj._pre_display()
        field = obj.field()
        range_option = obj.range.option()
        filled = obj.filled()
        contour_lines = obj.contour_lines()
        node_values = obj.node_values()
        boundary_values = obj.boundary_values()

        field_info = obj._data_extractor.field_info()
        field_data = obj._data_extractor.field_data()
        surfaces_info = field_info.get_surfaces_info()
        surface_ids = [
            id
            for surf in map(
                obj._data_extractor.remote_surface_name, obj.surfaces_list()
            )
            for id in surfaces_info[surf]["surface_id"]
        ]
        # get scalar field data
        field_data.add_get_surfaces_request(surface_ids, *args, **kwargs)
        field_data.add_get_scalar_fields_request(
            surface_ids,
            field,
            node_values,
            boundary_values,
        )

        location_tag = (
            field_data._payloadTags[PayloadTag.NODE_LOCATION]
            if node_values
            else field_data._payloadTags[PayloadTag.ELEMENT_LOCATION]
        )
        boundary_value_tag = (
            field_data._payloadTags[PayloadTag.BOUNDARY_VALUES]
            if boundary_values
            else 0
        )
        surface_tag = 0

        scalar_field_payload_data = field_data.get_fields()
        data_tag = location_tag | boundary_value_tag
        scalar_field_data = scalar_field_payload_data[data_tag]
        surface_data = scalar_field_payload_data[surface_tag]
        obj._post_display()
        return self._merge(surface_data, scalar_field_data)

    def _fetch_vector_data(self, obj, *args, **kwargs):

        if not obj.surfaces_list():
            raise RuntimeError("Vector definition is incomplete.")

        obj._pre_display()
        field_info = obj._data_extractor.field_info()
        field_data = obj._data_extractor.field_data()

        # surface ids
        surfaces_info = field_info.get_surfaces_info()
        surface_ids = [
            id
            for surf in map(
                obj._data_extractor.remote_surface_name, obj.surfaces_list()
            )
            for id in surfaces_info[surf]["surface_id"]
        ]

        field_data.add_get_surfaces_request(surface_ids, *args, **kwargs)
        field_data.add_get_vector_fields_request(surface_ids, obj.vectors_of())
        vector_field_tag = 0
        fields = field_data.get_fields()[vector_field_tag]
        obj._post_display()
        return fields

    def _merge(self, a, b):
        if b is not None:
            for k, v in a.items():
                if b.get(k):
                    a[k].update(b[k])
                    del b[k]
            a.update(b)
        return a


class XYPlotDataExtractor:
    """XYPlot DataExtractor."""

    def __init__(self, post_object: PlotDefn):
        """Instantiate XYPlot DataExtractor.

        Parameters
        ----------
        post_object : PlotDefn
            Plot definition object for which data needs to be extracted.
        """
        self._post_object: PlotDefn = post_object

    def fetch_data(self) -> Dict[str, Dict[str, np.array]]:
        """Fetch data for post object.

        Parameters
        ----------
        None

        Returns
        -------
        Dict[str: Dict[str: np.array]]
            Return dictionary of surfaces name to numpy array of x and y values.
        """

        if self._post_object.__class__.__name__ == "XYPlot":
            return self._fetch_xy_data(self._post_object)

    def _fetch_xy_data(self, obj):
        field = obj.y_axis_function()
        node_values = obj.node_values()
        boundary_values = obj.boundary_values()
        direction_vector = obj.direction_vector()
        surfaces_list = obj.surfaces_list()
        field_info = obj._data_extractor.field_info()
        field_data = obj._data_extractor.field_data()
        surfaces_info = field_info.get_surfaces_info()
        surface_ids = [
            id
            for surf in map(
                obj._data_extractor.remote_surface_name, obj.surfaces_list()
            )
            for id in surfaces_info[surf]["surface_id"]
        ]

        # get scalar field data
        field_data.add_get_surfaces_request(
            surface_ids,
            provide_faces=False,
            provide_vertices=True if node_values else False,
            provide_faces_centroid=False if node_values else True,
        )
        field_data.add_get_scalar_fields_request(
            surface_ids,
            field,
            node_values,
            boundary_values,
        )

        location_tag = (
            field_data._payloadTags[PayloadTag.NODE_LOCATION]
            if node_values
            else field_data._payloadTags[PayloadTag.ELEMENT_LOCATION]
        )
        boundary_value_tag = (
            field_data._payloadTags[PayloadTag.BOUNDARY_VALUES]
            if boundary_values
            else 0
        )
        surface_tag = 0
        xyplot_payload_data = field_data.get_fields()
        data_tag = location_tag | boundary_value_tag
        xyplot_data = xyplot_payload_data[data_tag]
        surface_data = xyplot_payload_data[surface_tag]

        # loop over all surfaces
        xy_plots_data = {}
        surfaces_list_iter = iter(surfaces_list)
        for surface_id, mesh_data in surface_data.items():
            mesh_data["vertices" if node_values else "centroid"].shape = (
                mesh_data["vertices" if node_values else "centroid"].size // 3,
                3,
            )
            y_values = xyplot_data[surface_id][field]
            x_values = np.matmul(
                mesh_data["vertices" if node_values else "centroid"],
                direction_vector,
            )
            structured_data = np.empty(
                x_values.size,
                dtype={
                    "names": ("xvalues", "yvalues"),
                    "formats": ("f8", "f8"),
                },
            )
            structured_data["xvalues"] = x_values
            structured_data["yvalues"] = y_values
            sort = np.argsort(structured_data, order=["xvalues"])
            surface_name = next(surfaces_list_iter)
            xy_plots_data[surface_name] = structured_data[sort]
        return xy_plots_data
