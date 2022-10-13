"""Module providing dump session data functionality."""
import pickle
from typing import Optional


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
            for k, v in session.field_info.get_fields_info().items()
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
            ] = session.field_info.get_range(field, True, [surface])
            session_data["range"][field][surface][
                "cell_value"
            ] = session.field_info.get_range(field, False, [surface])

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
    session_data["fields"] = transaction.get_fields()

    with open(file_path, "wb") as pickle_obj:
        pickle.dump(session_data, pickle_obj)
