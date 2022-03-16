"""Module providing dump session data functionality."""
import pickle


def dump_session_data(
    session, file_path: str, fields: list = [], surfaces: list = []
):
    """
    Dump session data.

    Parameters
    ----------
    session :
        Session object.
    file_path: str
        Session dump file path.
    fields: list, optional
        List of fields to write. If empty then all fields will be written.
    surfaces: list, optional
        List of surfaces to write. If empty then all surfaces will be written.
    """
    session_data = {}
    session_data["scalar_fields_info"] = {
        k: v
        for k, v in session.field_info.get_fields_info().items()
        if (not fields or v["solver_name"] in fields)
    }
    session_data["surfaces_info"] = {
        k: v
        for k, v in session.field_info.get_surfaces_info().items()
        if (not surfaces or k in surfaces)
    }
    session_data[
        "vector_fields_info"
    ] = session.field_info.get_vector_fields_info()
    if not fields:
        fields = [
            v["solver_name"]
            for k, v in session_data["scalar_fields_info"].items()
        ]
    surfaces_id = [
        v["surface_id"][0] for k, v in session_data["surfaces_info"].items()
    ]
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

    session_data["scalar-field"] = {}
    for field in fields:
        session_data["scalar-field"][field] = {}
        for surface in surfaces_id:
            session_data["scalar-field"][field][surface] = {}
            session_data["scalar-field"][field][surface][
                "node_value"
            ] = session.field_data.get_scalar_field([surface], field, True)[
                surface
            ]
            session_data["scalar-field"][field][surface][
                "cell_value"
            ] = session.field_data.get_scalar_field([surface], field, False)[
                surface
            ]

    session_data["surfaces"] = {}
    for surface in surfaces_id:
        session_data["surfaces"][surface] = session.field_data.get_surfaces(
            [surface]
        )[surface]

    session_data["vector-field"] = {}
    for surface in surfaces_id:
        session_data["vector-field"][
            surface
        ] = session.field_data.get_vector_field([surface])[surface]

    pickle_obj = open(file_path, "wb")
    pickle.dump(session_data, pickle_obj)
    pickle_obj.close()
