from typing import List, Optional

import numpy as np

from ansys.api.fluent.v0.field_data_pb2 import DataLocation
from ansys.fluent.core.filereader.case_file import CaseFile
from ansys.fluent.core.filereader.data_file import DataFile
from ansys.fluent.core.services.field_data import (
    FacesConnectivity,
    ScalarFieldData,
    SurfaceDataType,
    VectorFieldData,
    Vertices,
)


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

    class _VectorFieldTransaction:
        def __init__(self, field_name, surface_ids):
            self.field_name = field_name
            self.surface_ids = surface_ids

    def __init__(self, file_session):
        self._surface_transactions = []
        self._scalar_field_transactions = []
        self._vector_field_transactions = []
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

    def add_vector_fields_request(
        self,
        field_name: str,
        surface_ids: Optional[List[int]] = None,
        surface_names: Optional[List[str]] = None,
    ) -> None:
        for surface_id in surface_ids:
            self._vector_field_transactions.append(
                Transaction._VectorFieldTransaction(field_name, surface_ids)
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
            if scalar_field_tag not in field_data:
                field_data[scalar_field_tag] = {}
            field_data_surface = field_data[scalar_field_tag]
            for surface_id in transaction.surface_ids:
                field_data_surface[surface_id] = {}
                field_data_surface[surface_id][
                    transaction.field_name
                ] = self._file_session._data_file.get_face_data(
                    "phase-1", transaction.field_name, surface_id
                )

        vector_field_tag = (("type", "vector-field"),)

        for transaction in self._vector_field_transactions:
            if transaction.field_name != "velocity":
                raise RuntimeError("Only 'velocity' is allowed field.")
            if vector_field_tag not in field_data:
                field_data[vector_field_tag] = {}
            field_data_surface = field_data[vector_field_tag]
            for surface_id in transaction.surface_ids:
                field_data_surface[surface_id] = {}
                field_data_surface[surface_id][
                    transaction.field_name
                ] = _form_vector_array_from_data(
                    self._file_session._data_file, surface_id
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


def _form_vector_array_from_data(data, surface_id, phase="phase-1"):
    x_comp = data.get_face_data(phase, "SV_U", surface_id)
    y_comp = data.get_face_data(phase, "SV_V", surface_id)
    z_comp = data.get_face_data(phase, "SV_W", surface_id)

    vector_data = np.array([])
    for a, b, c in zip(x_comp, y_comp, z_comp):
        vector_data = np.append(vector_data, [a, b, c])

    return vector_data


class FileFieldData:
    def __init__(self, file_session, field_info):
        self._file_session = file_session
        self._field_info = field_info

    def new_transaction(self):
        """Create a new field transaction."""
        return Transaction(
            self._file_session,
        )

    def get_surface_data(
        self,
        data_type: SurfaceDataType,
        surface_ids: Optional[List[int]] = None,
        surface_name: Optional[str] = None,
        overset_mesh: Optional[bool] = False,
    ):
        if surface_ids and surface_name:
            raise RuntimeError("Please provide either surface name or surface ids.")

        if data_type == SurfaceDataType.Vertices:
            if surface_name:
                surface_ids = self._field_info.get_surfaces_info()[surface_name][
                    "surface_id"
                ]
                return Vertices(
                    surface_ids[0],
                    self._file_session._case_file.get_mesh().get_vertices(
                        surface_ids[0]
                    ),
                )
            else:
                return {
                    surface_id: Vertices(
                        surface_id,
                        self._file_session._case_file.get_mesh().get_vertices(
                            surface_id
                        ),
                    )
                    for surface_id in surface_ids
                }

        if data_type == SurfaceDataType.FacesConnectivity:
            if surface_name:
                surface_ids = self._field_info.get_surfaces_info()[surface_name][
                    "surface_id"
                ]
                return FacesConnectivity(
                    surface_ids[0],
                    self._file_session._case_file.get_mesh().get_connectivity(
                        surface_ids[0]
                    ),
                )
            else:
                return {
                    surface_id: FacesConnectivity(
                        surface_id,
                        self._file_session._case_file.get_mesh().get_connectivity(
                            surface_id
                        ),
                    )
                    for surface_id in surface_ids
                }

    def get_scalar_field_data(
        self,
        field_name: str,
        surface_ids: Optional[List[int]] = None,
        surface_name: Optional[str] = None,
        node_value: Optional[bool] = True,
        boundary_value: Optional[bool] = False,
    ):
        if surface_ids and surface_name:
            raise RuntimeError("Please provide either surface name or surface ids.")

        if surface_name:
            surface_ids = self._field_info.get_surfaces_info()[surface_name][
                "surface_id"
            ]
            if len(self._file_session._data_file.get_phases()) > 1:
                return ScalarFieldData(
                    surface_ids[0],
                    self._file_session._data_file.get_face_data(
                        field_name.split(":")[0],
                        field_name.split(":")[1],
                        surface_ids[0],
                    ),
                )
            else:
                return ScalarFieldData(
                    surface_ids[0],
                    self._file_session._data_file.get_face_data(
                        "phase-1", field_name, surface_ids[0]
                    ),
                )
        else:
            if len(self._file_session._data_file.get_phases()) > 1:
                return {
                    surface_id: ScalarFieldData(
                        surface_id,
                        self._file_session._data_file.get_face_data(
                            field_name.split(":")[0],
                            field_name.split(":")[1],
                            surface_id,
                        ),
                    )
                    for surface_id in surface_ids
                }
            else:
                return {
                    surface_id: ScalarFieldData(
                        surface_id,
                        self._file_session._data_file.get_face_data(
                            "phase-1", field_name, surface_id
                        ),
                    )
                    for surface_id in surface_ids
                }

    def get_vector_field_data(
        self,
        field_name: str,
        surface_ids: Optional[List[int]] = None,
        surface_name: Optional[str] = None,
    ):
        if surface_ids and surface_name:
            raise RuntimeError("Please provide either surface name or surface ids.")

        if (
            field_name.lower() != "velocity"
            and field_name.split(":")[1].lower() != "velocity"
        ):
            raise RuntimeError("Only 'velocity' is allowed field.")

        if surface_name:
            surface_ids = self._field_info.get_surfaces_info()[surface_name][
                "surface_id"
            ]
            if len(self._file_session._data_file.get_phases()) > 1:
                vector_data = _form_vector_array_from_data(
                    self._file_session._data_file,
                    surface_ids[0],
                    field_name.split(":")[0],
                )
            else:
                vector_data = _form_vector_array_from_data(
                    self._file_session._data_file, surface_ids[0]
                )

            return VectorFieldData(surface_ids[0], vector_data, scale=1.0)
        else:
            if len(self._file_session._data_file.get_phases()) > 1:
                return {
                    surface_id: VectorFieldData(
                        surface_id,
                        _form_vector_array_from_data(
                            self._file_session._data_file,
                            surface_id,
                            field_name.split(":")[0],
                        ),
                        scale=1.0,
                    )
                    for surface_id in surface_ids
                }
            else:
                return {
                    surface_id: VectorFieldData(
                        surface_id,
                        _form_vector_array_from_data(
                            self._file_session._data_file, surface_id
                        ),
                        scale=1.0,
                    )
                    for surface_id in surface_ids
                }


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
        self.field_data = FileFieldData(self, self.field_info)
        self.monitors_manager = lambda: None
        self.session_id = 1

    def read_case(self, case_filepath):
        self._case_file = CaseFile(case_filepath)

    def read_data(self, data_filepath):
        self._data_file = DataFile(data_filepath, case_file_handle=self._case_file)
