from typing import List, Optional

from ansys.api.fluent.v0.field_data_pb2 import DataLocation
from ansys.fluent.core.filereader.case_file import CaseFile
from ansys.fluent.core.filereader.data_file import DataFile


class Transaction:
    class _SurfaceTransaction:
        def __init__(self, surface_id, provide_vertices, provide_faces):
            self.surface_id = surface_id
            self.provide_vertices = provide_vertices
            self.provide_faces = provide_faces

    class _ScalarFieldTransaction:
        def __init__(self, field_name, surface_ids):
            self.field_name = field_name
            self.surface_ids = surface_ids

    def __init__(self, file_session):
        self._surface_transactions = []
        self._scalar_field_transactions = []
        self._file_session = file_session

    def add_surfaces_request(
        self, surface_ids, provide_vertices=True, provide_faces=True
    ) -> None:
        for surface_id in surface_ids:
            self._surface_transactions.append(
                Transaction._SurfaceTransaction(
                    surface_id, provide_vertices, provide_faces
                )
            )

    def add_scalar_fields_request(
        self,
        field_name: str,
        surface_ids: Optional[List[int]] = None,
        surface_names: Optional[List[str]] = None,
        node_value: Optional[bool] = True,
        boundary_value: Optional[bool] = False,
    ) -> None:
        for surface_id in surface_ids:
            self._scalar_field_transactions.append(
                Transaction._ScalarFieldTransaction(field_name, surface_ids)
            )

    def get_fields(self):
        mesh = self._file_session._case_file.get_mesh()
        field_data = {}

        scalar_field_tag = (
            ("type", "scalar-field"),
            (
                "dataLocation",
                DataLocation.Elements,
            ),
            ("boundaryValues", False),
        )

        for transaction in self._scalar_field_transactions:
            if (scalar_field_tag) not in field_data:
                field_data[scalar_field_tag] = {}
            field_data_surface = field_data[scalar_field_tag]
            for surface_id in transaction.surface_ids:
                field_data_surface[surface_id] = {}
                field_data_surface[surface_id][
                    transaction.field_name
                ] = self._file_session._data_file.get_face_data(
                    "phase-1", transaction.field_name, surface_id
                )

        for transaction in self._surface_transactions:
            if (("type", "surface-data"),) not in field_data:
                field_data[(("type", "surface-data"),)] = {}
            field_data_surface = field_data[(("type", "surface-data"),)]
            field_data_surface[transaction.surface_id] = {}
            field_data_surface[transaction.surface_id]["faces"] = mesh.get_connectivity(
                transaction.surface_id
            )
            field_data_surface[transaction.surface_id]["vertices"] = mesh.get_vertices(
                transaction.surface_id
            )
        return field_data


class FileFieldData:
    def __init__(self, file_session):
        self._file_session = file_session

    def new_transaction(self):
        """Create a new field transaction."""
        return Transaction(
            self._file_session,
        )


class FileFieldInfo:
    def __init__(self, file_session):
        self._file_session = file_session

    def get_scalar_field_range(
        self, field: str, node_value: bool = False, surface_ids: List[int] = None
    ) -> List[float]:
        """Get the range (minimum and maximum values) of the field.

        Parameters
        ----------
        field: str
            Field name
        node_value: bool
        surface_ids : List[int], optional
            List of surface IDS for the surface data.

        Returns
        -------
        List[float]
        """
        minimum = None
        maximum = None
        if not surface_ids:
            surface_ids = self._file_session._case_file.get_mesh().get_surface_ids()
        for surface_id in surface_ids:
            data = self._file_session._data_file.get_face_data(
                "phase-1", field, surface_id
            )
            if len(data) == 0:
                continue
            minimum = min(data) if minimum is None else min(minimum, min(data))
            maximum = max(data) if maximum is None else max(maximum, max(data))

        return [minimum, maximum]

    def get_scalar_fields_info(self):
        """Get fields information (field name, domain, and section).

        Returns
        -------
        Dict
        """
        phases = self._file_session._data_file.get_phases()

        return {
            face_variable: {
                "display_name": face_variable,
                "section": "field-data",
                "domain": phase,
            }
            for phase in phases
            for face_variable in self._file_session._data_file.get_face_variables(phase)
        }

    def get_surfaces_info(self):
        """Get surfaces information (surface name, ID, and type).

        Returns
        -------
        Dict
        """
        mesh = self._file_session._case_file.get_mesh()
        surface_names = mesh.get_surface_names()
        surface_ids = mesh.get_surface_ids()
        info = {
            name: {
                "surface_id": [surface_id],
                "zone_id": -1,
                "zone_type": "wall",
                "type": "plane",
            }
            for name, surface_id in zip(surface_names, surface_ids)
        }
        return info


class FileSession:
    def __init__(self):
        self._case_file = None
        self._data_file = None
        self.field_info = FileFieldInfo(self)
        self.field_data = FileFieldData(self)
        self.monitors_manager = lambda: None
        self.session_id = 1

    def read_case(self, case_filepath):
        self._case_file = CaseFile(case_filepath)

    def read_data(self, data_filepath):
        self._data_file = DataFile(data_filepath, case_file_handle=self._case_file)
