"""Module providing dump session data functionality."""
import pickle


def dump_session_data(session, file_path: str, fields: list = [], surfaces: list = []):
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
    session_data = {}
    session_data["scalar_fields_info"] = {
        k: v
        for k, v in session.field_info.get_fields_info().items()
        if (not fields or k in fields)
    }
    session_data["surfaces_info"] = {
        k: v
        for k, v in session.field_info.get_surfaces_info().items()
        if (not surfaces or k in surfaces)
    }
    session_data["vector_fields_info"] = session.field_info.get_vector_fields_info()
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

    session.field_data.add_get_surfaces_request(
        surfaces_id, provide_faces_centroid=True, provide_faces_normal=True
    )
    for field in fields:
        session.field_data.add_get_scalar_fields_request(
            surfaces_id, field, True, boundary_value=False
        )
        session.field_data.add_get_scalar_fields_request(
            surfaces_id, field, False, boundary_value=False
        )
        session.field_data.add_get_scalar_fields_request(
            surfaces_id, field, True, boundary_value=True
        )
        session.field_data.add_get_scalar_fields_request(
            surfaces_id, field, False, boundary_value=True
        )
    session.field_data.add_get_vector_fields_request(surfaces_id)
    session_data["fields"] = session.field_data.get_fields()

    with open(file_path, "wb") as pickle_obj:
        pickle.dump(session_data, pickle_obj)
