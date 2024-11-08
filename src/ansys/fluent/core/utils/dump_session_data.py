"""Module providing dump session data functionality."""

from pathlib import Path
import pickle

import numpy as np

from ansys.fluent.core.services.field_data import SurfaceDataType


def dump_session_data(
    session,
    file_name: str,
    fields: list | None = None,
    surfaces: list | None = None,
):
    """Dump session data.

    Parameters
    ----------
    session :
        Session object.
    file_name: str
        File path for the session dump.
    fields: list, optional
        List of fields to write. If the list is empty, all fields are written.
    surfaces: list, optional
        List of surfaces to write. If the list is empty, all surfaces are written.
    """
    session_data = {
        "scalar_fields_info": {
            k: v
            for k, v in session.fields.field_info.get_scalar_fields_info().items()
            if (not fields or k in fields)
        },
        "surfaces_info": {
            k: v
            for k, v in session.fields.field_info.get_surfaces_info().items()
            if (not surfaces or k in surfaces)
        },
        "vector_fields_info": session.fields.field_info.get_vector_fields_info(),
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
            session_data["range"][field][surface]["node_value"] = (
                session.fields.field_info.get_scalar_field_range(field, True, [surface])
            )
            session_data["range"][field][surface]["cell_value"] = (
                session.fields.field_info.get_scalar_field_range(
                    field, False, [surface]
                )
            )

    transaction = session.fields.field_data.new_transaction()
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

    with open(file_name, "wb") as pickle_obj:
        pickle.dump(session_data, pickle_obj)


class DumpDataReader:
    """Reads dump data."""

    def __init__(self, file_name: str):
        """Initialize DumpDataReader."""
        with open(
            str(Path(file_name).resolve()),
            "rb",
        ) as pickle_obj:
            self._session_data = pickle.load(pickle_obj)

    def get_session_data(self):
        """Get session data."""
        return self._session_data

    def get_surface_data(self, surface_ids, data_types) -> list[np.ndarray | None]:
        """Get surface data."""
        tag_id = (("type", "surface-data"),)

        surfaces_data = [
            self._session_data["fields"][tag_id][surface_id][
                SurfaceDataType(data_type).value
            ]
            for data_type in data_types
            for surface_id in surface_ids
        ]

        return surfaces_data

    def get_scalar_field_data(
        self, surface_ids, data_location, provide_boundary_values, field_names
    ) -> list[np.ndarray | None]:
        """Get scalar field data."""
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
    ) -> list[np.ndarray | None]:
        """Get vector field data."""
        tag_id = (("type", "vector-field"),)

        vector_field_data = [
            (
                self._session_data["fields"][tag_id][surface_id][field_name],
                self._session_data["fields"][tag_id][surface_id]["vector-scale"],
            )
            for field_name in field_names
            for surface_id in surface_ids
        ]

        return vector_field_data

    def get_pathlines_data(
        self, surface_ids, field_names, key
    ) -> list[np.ndarray | None]:
        """Get pathlines data."""
        pathlines_data = []
        for surface_id in surface_ids:
            for field_name in field_names:
                tag_id = (("type", "pathlines-field"), ("field", field_name))
                pathlines_data.append(
                    self._session_data["fields"][tag_id][surface_id][key]
                )

        return pathlines_data
