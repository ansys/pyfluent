"""Module providing dump session data functionality."""
from pathlib import Path
import pickle
from typing import Optional, Union

import numpy as np

from ansys.fluent.core.services.field_data import SurfaceDataType


def dump_session_data(
    session,
    file_path: str,
    fields: Optional[list] = None,
    surfaces: Optional[list] = None,
):
    """Dump session data.

    Parameters
    ----------
    session :
        Session object.
    file_path: str
        File path for the session dump.
    fields: list, optional
        List of fields to write. If the list is empty, all fields are written.
    surfaces: list, optional
        List of surfaces to write. If the list is empty, all surfaces are written.
    """
    session_data = {
        "scalar_fields_info": {
            k: v
            for k, v in session.field_info.get_scalar_fields_info().items()
            if (not fields or k in fields)
        },
        "surfaces_info": {
            k: v
            for k, v in session.field_info.get_surfaces_info().items()
            if (not surfaces or k in surfaces)
        },
        "vector_fields_info": session.field_info.get_vector_fields_info(),
    }
    if not fields:
        fields = [
            v["solver_name"] for k, v in session_data["scalar_fields_info"].items()
        ]
    surfaces_id = [v["surface_id"][0] for k, v in session_data["surfaces_info"].items()]
    session_data["range"] = {}
    for field in fields:
        session_data["range"][field] = {}
        for surface in surfaces_id:
            session_data["range"][field][surface] = {}
            session_data["range"][field][surface][
                "node_value"
            ] = session.field_info.get_scalar_fields_range(field, True, [surface])
            session_data["range"][field][surface][
                "cell_value"
            ] = session.field_info.get_scalar_fields_range(field, False, [surface])

    transaction = session.field_data.new_transaction()
    transaction.add_surfaces_request(
        surface_ids=surfaces_id, provide_faces_centroid=True, provide_faces_normal=True
    )
    for field in fields:
        transaction.add_scalar_fields_request(
            surface_ids=surfaces_id,
            field_name=field,
            node_value=True,
            boundary_value=False,
        )
        transaction.add_scalar_fields_request(
            surface_ids=surfaces_id,
            field_name=field,
            node_value=False,
            boundary_value=False,
        )
        transaction.add_scalar_fields_request(
            surface_ids=surfaces_id,
            field_name=field,
            node_value=True,
            boundary_value=True,
        )
        transaction.add_scalar_fields_request(
            surface_ids=surfaces_id,
            field_name=field,
            node_value=False,
            boundary_value=True,
        )
    transaction.add_vector_fields_request(
        surface_ids=surfaces_id, field_name="velocity"
    )
    transaction.add_pathlines_fields_request(
        surface_ids=surfaces_id, field_name="velocity-magnitude"
    )
    session_data["fields"] = transaction.get_fields()

    with open(file_path, "wb") as pickle_obj:
        pickle.dump(session_data, pickle_obj)


class DumpDataReader:
    def __init__(self, file_path: str):
        with open(
            str(Path(file_path).resolve()),
            "rb",
        ) as pickle_obj:
            self._session_data = pickle.load(pickle_obj)

    def get_session_data(self):
        return self._session_data

    def get_surface_data(self, surface_ids, data_types) -> list[Union[np.array, None]]:
        tag_id = (("type", "surface-data"),)

        enum_to_field_name = {
            SurfaceDataType.FacesConnectivity: "faces",
            SurfaceDataType.Vertices: "vertices",
            SurfaceDataType.FacesCentroid: "centroid",
            SurfaceDataType.FacesNormal: "face-normal",
        }

        surfaces_data = []
        surfaces_data_int = []

        for data_type in data_types:
            for surface_id in surface_ids:
                surfaces_data_int.append(
                    self._session_data["fields"][tag_id][surface_id][
                        enum_to_field_name[data_type]
                    ]
                )

            surfaces_data.append(surfaces_data_int[:])
            surfaces_data_int = []

        return surfaces_data

    def get_scalar_field_data(
        self, surface_ids, data_location, provide_boundary_values, field_names
    ) -> list[Union[np.array, None]]:
        tag_id = (
            ("type", "scalar-field"),
            ("dataLocation", data_location),
            ("boundaryValues", provide_boundary_values),
        )

        scalar_field_data = [
            self._session_data["fields"][tag_id][surface_id][field_name]
            for field_name in field_names
            for surface_id in surface_ids
        ]

        return scalar_field_data

    def get_vector_field_data(
        self, surface_ids, field_names
    ) -> list[Union[np.array, None]]:
        tag_id = (("type", "vector-field"),)

        vector_field_data = [
            self._session_data["fields"][tag_id][surface_id][field_name]
            for field_name in field_names
            for surface_id in surface_ids
        ]

        return vector_field_data

    def get_pathlines_data(
        self, surface_ids, field_names, key
    ) -> list[Union[np.array, None]]:
        pathlines_data = []
        for surface_id in surface_ids:
            for field_name in field_names:
                tag_id = (("type", "pathlines-field"), ("field", field_name))
                pathlines_data.append(
                    self._session_data["fields"][tag_id][surface_id][key]
                )

        return pathlines_data
