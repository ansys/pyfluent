"""Module providing data extractor APIs."""

import itertools
from typing import Dict

import numpy as np

from ansys.api.fluent.v0.field_data_pb2 import DataLocation, PayloadTag
from ansys.fluent.core.graphics_definitions.post_object_defns import (
    GraphicsDefn,
    PlotDefn,
)
from ansys.fluent.core.services.field_data import (
    _FieldDataConstants,
    merge_pathlines_data,
)


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
        elif self._post_object.__class__.__name__ == "Pathlines":
            return self._fetch_pathlines_data(self._post_object, *args, **kwargs)

    def _fetch_mesh_data(self, obj, *args, **kwargs):
        if not obj.surfaces_list():
            raise RuntimeError("Mesh definition is incomplete.")
        obj._pre_display()
        field_info = obj._api_helper.field_info()
        field_data = obj._api_helper.field_data()
        transaction = field_data.new_transaction()
        surfaces_info = field_info.get_surfaces_info()
        surface_ids = [
            id
            for surf in map(obj._api_helper.remote_surface_name, obj.surfaces_list())
            for id in surfaces_info[surf]["surface_id"]
        ]

        transaction.add_surfaces_request(surface_ids, *args, **kwargs)
        try:
            fields = transaction.get_fields()
            # 0 is old tag
            surfaces_data = fields.get(0) or fields[(("type", "surface-data"),)]
        except:
            raise RuntimeError("Error while requesting data from server.")
        finally:
            obj._post_display()
        return surfaces_data

    def _fetch_surface_data(self, obj, *args, **kwargs):
        surface_api = obj._api_helper.surface_api
        surface_api.create_surface_on_server()
        dummy_object = "dummy_object"
        post_session = obj._get_top_most_parent()
        if (
            obj.definition.type() == "iso-surface"
            and obj.definition.iso_surface.rendering() == "contour"
        ):
            contour = post_session.Contours[dummy_object]
            contour.field = obj.definition.iso_surface.field()
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

        field_info = obj._api_helper.field_info()
        field_data = obj._api_helper.field_data()
        transaction = field_data.new_transaction()
        surfaces_info = field_info.get_surfaces_info()
        surface_ids = [
            id
            for surf in map(obj._api_helper.remote_surface_name, obj.surfaces_list())
            for id in surfaces_info[surf]["surface_id"]
        ]
        # get scalar field data
        transaction.add_surfaces_request(surface_ids=surface_ids, *args, **kwargs)
        transaction.add_scalar_fields_request(
            field_name=field,
            surface_ids=surface_ids,
            node_value=node_values,
            boundary_value=boundary_values,
        )

        location_tag = (
            _FieldDataConstants.payloadTags[PayloadTag.NODE_LOCATION]
            if node_values
            else _FieldDataConstants.payloadTags[PayloadTag.ELEMENT_LOCATION]
        )
        boundary_value_tag = (
            _FieldDataConstants.payloadTags[PayloadTag.BOUNDARY_VALUES]
            if boundary_values
            else 0
        )

        try:
            fields = transaction.get_fields()
            data_tag = location_tag | boundary_value_tag
            scalar_field_data = (
                fields.get(data_tag)
                or fields[
                    (
                        ("type", "scalar-field"),
                        (
                            "dataLocation",
                            DataLocation.Nodes
                            if node_values
                            else DataLocation.Elements,
                        ),
                        ("boundaryValues", boundary_values),
                    )
                ]
            )
            surface_data = fields.get(0) or fields[(("type", "surface-data"),)]
        except Exception:
            raise RuntimeError("Error while requesting data from server.")
        finally:
            obj._post_display()
        return self._merge(surface_data, scalar_field_data)

    def _fetch_pathlines_data(self, obj, *args, **kwargs):
        if not obj.surfaces_list() or not obj.field():
            raise RuntimeError("Ptahline definition is incomplete.")

        obj._pre_display()
        field = obj.field()
        surfaces_list = obj.surfaces_list()

        field_info = obj._api_helper.field_info()
        field_data = obj._api_helper.field_data()
        surfaces_info = field_info.get_surfaces_info()
        transaction = field_data.new_transaction()
        surface_ids = [
            id
            for surf in map(obj._api_helper.remote_surface_name, obj.surfaces_list())
            for id in surfaces_info[surf]["surface_id"]
        ]
        transaction.add_pathlines_fields_request(
            surface_ids=surface_ids, field_name=field
        )

        try:
            fields = transaction.get_fields()
            pathlines_data = fields[(("type", "pathlines-field"), ("field", field))]
            data = merge_pathlines_data(pathlines_data, field)
        except Exception as e:
            raise RuntimeError("Error while requesting data from server." + str(e))
        finally:
            obj._post_display()
        return data

    def _fetch_vector_data(self, obj, *args, **kwargs):

        if not obj.surfaces_list():
            raise RuntimeError("Vector definition is incomplete.")

        obj._pre_display()
        field = obj.field()
        if not field:
            field = obj.field = "velocity-magnitude"
        field_info = obj._api_helper.field_info()
        field_data = obj._api_helper.field_data()

        transaction = field_data.new_transaction()

        # surface ids
        surfaces_info = field_info.get_surfaces_info()
        surface_ids = [
            id
            for surf in map(obj._api_helper.remote_surface_name, obj.surfaces_list())
            for id in surfaces_info[surf]["surface_id"]
        ]

        transaction.add_surfaces_request(surface_ids=surface_ids, *args, **kwargs)
        transaction.add_scalar_fields_request(
            surface_ids=surface_ids,
            field_name=field,
            node_value=False,
            boundary_value=False,
        )
        transaction.add_vector_fields_request(
            surface_ids=surface_ids, field_name=obj.vectors_of()
        )
        try:
            fields = transaction.get_fields()
            vector_field = fields.get(0) or fields[(("type", "vector-field"),)]
            scalar_field = (
                fields.get(_FieldDataConstants.payloadTags[PayloadTag.ELEMENT_LOCATION])
                or fields[
                    (
                        ("type", "scalar-field"),
                        (
                            "dataLocation",
                            DataLocation.Elements,
                        ),
                        ("boundaryValues", False),
                    )
                ]
            )
            surface_data = fields.get(0) or fields[(("type", "surface-data"),)]
        except:
            raise RuntimeError("Error while requesting data from server.")
        finally:
            obj._post_display()
        data = self._merge(surface_data, vector_field)
        return self._merge(data, scalar_field)

    def _merge(self, a, b):
        if a is b:
            return a
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
        """Fetch data for visualization object.

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
        obj._pre_display()
        field = obj.y_axis_function()
        node_values = obj.node_values()
        boundary_values = obj.boundary_values()
        direction_vector = obj.direction_vector()
        surfaces_list = obj.surfaces_list()
        field_info = obj._api_helper.field_info()
        field_data = obj._api_helper.field_data()
        transaction = field_data.new_transaction()
        surfaces_info = field_info.get_surfaces_info()
        surface_ids = [
            id
            for surf in map(obj._api_helper.remote_surface_name, obj.surfaces_list())
            for id in surfaces_info[surf]["surface_id"]
        ]
        # For group surfaces, expanded surf name is used.
        # If group1 consists of id 3,4,5 then corresponding surface name will be
        # group:3, group:4, group:5
        surfaces_list_expanded = [
            expanded_surf_name
            for expanded_surf_name_list in itertools.starmap(
                lambda local_surface_name, id_list: [local_surface_name]
                if len(id_list) == 1
                else [f"{local_surface_name}:{id}" for id in id_list],
                [
                    (
                        local_surface_name,
                        surfaces_info[remote_surface_name]["surface_id"],
                    )
                    for remote_surface_name, local_surface_name in zip(
                        map(obj._api_helper.remote_surface_name, surfaces_list),
                        surfaces_list,
                    )
                ],
            )
            for expanded_surf_name in expanded_surf_name_list
        ]

        # get scalar field data
        transaction.add_surfaces_request(
            surface_ids=surface_ids,
            provide_faces=False,
            provide_vertices=True if node_values else False,
            provide_faces_centroid=False if node_values else True,
        )
        transaction.add_scalar_fields_request(
            field_name=field,
            surface_ids=surface_ids,
            node_value=node_values,
            boundary_value=boundary_values,
        )

        location_tag = (
            _FieldDataConstants.payloadTags[PayloadTag.NODE_LOCATION]
            if node_values
            else _FieldDataConstants.payloadTags[PayloadTag.ELEMENT_LOCATION]
        )
        boundary_value_tag = (
            _FieldDataConstants.payloadTags[PayloadTag.BOUNDARY_VALUES]
            if boundary_values
            else 0
        )
        surface_tag = 0
        xyplot_payload_data = transaction.get_fields()
        data_tag = location_tag | boundary_value_tag
        if data_tag not in xyplot_payload_data:
            data_tag = (
                ("type", "scalar-field"),
                (
                    "dataLocation",
                    DataLocation.Nodes if node_values else DataLocation.Elements,
                ),
                ("boundaryValues", boundary_values),
            )
            surface_tag = (("type", "surface-data"),)
            if data_tag not in xyplot_payload_data:
                raise RuntimeError("Plot surface is not valid.")
        xyplot_data = xyplot_payload_data[data_tag]
        surface_data = xyplot_payload_data[surface_tag]

        # loop over all surfaces
        xy_plots_data = {}
        surfaces_list_iter = iter(surfaces_list_expanded)
        for surface_id, mesh_data in surface_data.items():
            mesh_data["vertices" if node_values else "centroid"].shape = (
                mesh_data["vertices" if node_values else "centroid"].size // 3,
                3,
            )
            y_values = xyplot_data[surface_id][field]
            if y_values is None:
                continue
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
        obj._post_display()
        return xy_plots_data
