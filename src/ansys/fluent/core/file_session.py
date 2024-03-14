"""Provides a module for file session."""

from typing import List, Optional

import numpy as np

from ansys.api.fluent.v0.field_data_pb2 import DataLocation
from ansys.fluent.core.exceptions import SurfaceSpecificationError
from ansys.fluent.core.filereader.case_file import CaseFile
from ansys.fluent.core.filereader.data_file import DataFile
from ansys.fluent.core.services.field_data import (
    FacesConnectivity,
    ScalarFieldData,
    SurfaceDataType,
    VectorFieldData,
    Vertices,
)


class InvalidMultiPhaseFieldName(ValueError):
    """Raised when multi-phase field name is inappropriate."""

    def __init__(self):
        super().__init__("Multi-phase field name should start with 'phase-'.")


class InvalidFieldName(ValueError):
    """Raised when a field name is inappropriate."""

    def __init__(self):
        super().__init__("The only allowed field is 'velocity'.")


class Transaction:
    """Populates field data on surfaces."""

    class _SurfaceTransaction:
        def __init__(self, surface_id, provide_vertices, provide_faces):
            self.surface_id = surface_id
            self.provide_vertices = provide_vertices
            self.provide_faces = provide_faces

    class _ScalarFieldTransaction:
        def __init__(self, field_name, surface_ids, phase="phase-1"):
            self.phase_name = phase
            self.field_name = field_name
            self.surface_ids = surface_ids

    class _VectorFieldTransaction:
        def __init__(self, field_name, surface_ids, phase="phase-1"):
            self.phase_name = phase
            self.field_name = field_name
            self.surface_ids = surface_ids

    def __init__(self, file_session, field_info):
        """__init__ method of Transaction class."""
        self._surface_transactions = []
        self._scalar_field_transactions = []
        self._vector_field_transactions = []
        self._file_session = file_session
        self._field_info = field_info

    def add_surfaces_request(
        self, surface_ids, provide_vertices=True, provide_faces=True
    ) -> None:
        """Add request to get surface data (vertices, face connectivity, centroids, and
        normals).

        Parameters
        ----------
        surface_ids : List[int], optional
            List of surface IDS for the surface data.
        surface_names: List[str], optional
            List of surface names for the surface data.
        overset_mesh : bool, optional
            Whether to get the overset met. The default is ``False``.
        provide_vertices : bool, optional
            Whether to get node coordinates. The default is ``True``.
        provide_faces : bool, optional
            Whether to get face connectivity. The default is ``True``.
        provide_faces_centroid : bool, optional
            Whether to get face centroids. The default is ``False``.
        provide_faces_normal : bool, optional
            Whether to get faces normal. The default is ``False``

        Returns
        -------
        None
        """
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
        """Add request to get scalar field data on surfaces.

        Parameters
        ----------
        field_name : str
            Name of the scalar field.
        surface_ids : List[int], optional
            List of surface IDs for scalar field data.
        surface_names: List[str], optional
            List of surface names for scalar field data.
        node_value : bool, optional
            Whether to provide the nodal location. The default is ``True``. If
            ``False``, the element location is provided.
        boundary_value : bool, optional
            Whether to provide the slip velocity at the wall boundaries. The default
            is ``False``. When ``True``, no slip velocity is provided.

        Returns
        -------
        None

        Raises
        ------
        SurfaceSpecificationError
            If both ``surface_ids`` and ``surface_names`` are provided.
        InvalidMultiPhaseFieldName
            If field name does not have prefix ``phase-`` for multi-phase cases.
        """
        if surface_ids is None:
            surface_ids = []
        if surface_ids and surface_names:
            raise SurfaceSpecificationError()

        if surface_names:
            for surface_name in surface_names:
                surface_ids.append(
                    self._field_info.get_surfaces_info()[surface_name]["surface_id"][0]
                )

        if len(self._file_session._data_file.get_phases()) > 1:
            if not field_name.startswith("phase-"):
                raise InvalidMultiPhaseFieldName()
            self._scalar_field_transactions.append(
                Transaction._ScalarFieldTransaction(
                    field_name, surface_ids, field_name.split(":")[0]
                )
            )
        else:
            self._scalar_field_transactions.append(
                Transaction._ScalarFieldTransaction(field_name, surface_ids)
            )

    def add_vector_fields_request(
        self,
        field_name: str,
        surface_ids: Optional[List[int]] = None,
        surface_names: Optional[List[str]] = None,
    ) -> None:
        """Add request to get vector field data on surfaces.

        Parameters
        ----------
        field_name : str
            Name of the vector field.
        surface_ids : List[int], optional
            List of surface IDs for vector field data.
        surface_names: List[str], optional
            List of surface names for vector field data.

        Returns
        -------
        None

        Raises
        ------
        SurfaceSpecificationError
            If both ``surface_ids`` and ``surface_names`` are provided.
        InvalidMultiPhaseFieldName
            If field name does not have prefix ``phase-`` for multi-phase cases.
        """
        if surface_ids is None:
            surface_ids = []
        if surface_ids and surface_names:
            raise SurfaceSpecificationError()

        if surface_names:
            for surface_name in surface_names:
                surface_ids.append(
                    self._field_info.get_surfaces_info()[surface_name]["surface_id"][0]
                )

        if len(self._file_session._data_file.get_phases()) > 1:
            if not field_name.startswith("phase-"):
                raise InvalidMultiPhaseFieldName()
            self._vector_field_transactions.append(
                Transaction._VectorFieldTransaction(
                    field_name, surface_ids, field_name.split(":")[0]
                )
            )
        else:
            self._vector_field_transactions.append(
                Transaction._VectorFieldTransaction(field_name, surface_ids)
            )

    def add_pathlines_fields_request(
        self,
        field_name: str,
        surface_ids: Optional[List[int]] = None,
        surface_names: Optional[List[str]] = None,
    ):
        """Add request to get pathlines field on surfaces.

        Parameters
        ----------
        field_name : str
            Name of the scalar field to color pathlines.
        surface_ids : List[int], optional
            List of surface IDs for pathlines field data.
        surface_names : List[str], optional
            List of surface names for pathlines field data.

        Returns
        -------
        None
        """
        raise NotImplementedError("Pathlines are not supported.")

    def get_fields(self):
        """Get data for previously added requests and then clear all requests.

        Returns
        -------
        Dict[int, Dict[int, Dict[str, np.array]]]
            Data is returned as dictionary of dictionaries in the following structure:
            tag Union[int, Tuple]-> surface_id [int] -> field_name [str] -> field_data[np.array]

        Raises
        ------
        InvalidFieldName
            If any field other than ``"velocity"`` is provided.
        """
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
                field_data_surface[surface_id][transaction.field_name] = (
                    self._file_session._data_file.get_face_scalar_field_data(
                        transaction.phase_name, transaction.field_name, surface_id
                    )
                )

        vector_field_tag = (("type", "vector-field"),)

        for transaction in self._vector_field_transactions:
            if "velocity" not in transaction.field_name:
                raise InvalidFieldName()
            if vector_field_tag not in field_data:
                field_data[vector_field_tag] = {}
            field_data_surface = field_data[vector_field_tag]
            for surface_id in transaction.surface_ids:
                field_data_surface[surface_id] = {}
                field_data_surface[surface_id][transaction.field_name] = (
                    self._file_session._data_file.get_face_vector_field_data(
                        transaction.phase_name, surface_id
                    )
                )
                field_data_surface[surface_id]["vector-scale"] = np.array([0.1])

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
    """File field data."""

    def __init__(self, file_session, field_info):
        self._file_session = file_session
        self._field_info = field_info

    def new_transaction(self):
        """Create a new field transaction."""
        return Transaction(self._file_session, self._field_info)

    def get_surface_data(
        self,
        data_type: SurfaceDataType,
        surface_ids: Optional[List[int]] = None,
        surface_name: Optional[str] = None,
        overset_mesh: Optional[bool] = False,
    ):
        """Get surface data (vertices and faces connectivity).

        Parameters
        ----------
        data_type : SurfaceDataType
            SurfaceDataType Enum member.
        surface_ids : List[int], optional
            List of surface IDs for the surface data.
        surface_name : str, optional
            Surface name for the surface data.
        overset_mesh : bool, optional
            Whether to provide the overset method. The default is ``False``.

        Returns
        -------
        Union[Vertices, FacesConnectivity, Dict[int, Union[Vertices, FacesConnectivity]]]
             If a surface name is provided as input, face vertices, connectivity data, and normal or centroid data are returned.
             If surface IDs are provided as input, a dictionary containing a map of surface IDs to face
             vertices, connectivity data, and normal or centroid data is returned.

        Raises
        ------
        SurfaceSpecificationError
            If both ``surface_ids`` and ``surface_names`` are provided.
        """
        if surface_ids and surface_name:
            raise SurfaceSpecificationError()

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
        """Get scalar field data on a surface.

        Parameters
        ----------
        field_name : str
            Name of the scalar field.
        surface_ids : List[int], optional
            List of surface IDs for scalar field data.
        surface_name: str, optional
            Surface Name for scalar field data.
        node_value : bool, optional
            Whether to provide data for the nodal location. The default is ``True``.
            When ``False``, data is provided for the element location.
        boundary_value : bool, optional
            Whether to provide slip velocity at the wall boundaries. The default is
            ``False``. When ``True``, no slip velocity is provided.

        Returns
        -------
        Union[ScalarFieldData, Dict[int, ScalarFieldData]]
            If a surface name is provided as input, scalar field data is returned. If surface
            IDs are provided as input, a dictionary containing a map of surface IDs to scalar
            field data.

        Raises
        ------
        SurfaceSpecificationError
            If both ``surface_ids`` and ``surface_names`` are provided.
        InvalidMultiPhaseFieldName
            If field name does not have prefix ``phase-`` for multi-phase cases.
        """
        if surface_ids and surface_name:
            raise SurfaceSpecificationError()

        if surface_name:
            surface_ids = self._field_info.get_surfaces_info()[surface_name][
                "surface_id"
            ]
            if len(self._file_session._data_file.get_phases()) > 1:
                if not field_name.startswith("phase-"):
                    raise InvalidMultiPhaseFieldName()
                return ScalarFieldData(
                    surface_ids[0],
                    self._file_session._data_file.get_face_scalar_field_data(
                        field_name.split(":")[0],
                        field_name.split(":")[1],
                        surface_ids[0],
                    ),
                )
            else:
                return ScalarFieldData(
                    surface_ids[0],
                    self._file_session._data_file.get_face_scalar_field_data(
                        "phase-1", field_name, surface_ids[0]
                    ),
                )
        else:
            if len(self._file_session._data_file.get_phases()) > 1:
                if not field_name.startswith("phase-"):
                    raise InvalidMultiPhaseFieldName()
                return {
                    surface_id: ScalarFieldData(
                        surface_id,
                        self._file_session._data_file.get_face_scalar_field_data(
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
                        self._file_session._data_file.get_face_scalar_field_data(
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
        """Get vector field data on a surface.

        Parameters
        ----------
        field_name : str
            Name of the vector field.
        surface_ids : List[int], optional
            List of surface IDs for vector field data.
        surface_name: str, optional
            Surface Name for vector field data.

        Returns
        -------
        Union[VectorFieldData, Dict[int, VectorFieldData]]
            If a surface name is provided as input, vector field data is returned.
            If surface IDs are provided as input, a dictionary containing a map of
            surface IDs to vector field data is returned.

        Raises
        ------
        SurfaceSpecificationError
            If both ``surface_ids`` and ``surface_names`` are provided.
        InvalidFieldName
            If any field other than ``"velocity"`` is provided.
        InvalidMultiPhaseFieldName
            If field name does not have prefix ``phase-`` for multi-phase cases.
        """
        if surface_ids and surface_name:
            raise SurfaceSpecificationError()

        if (
            field_name.lower() != "velocity"
            and field_name.split(":")[1].lower() != "velocity"
        ):
            raise InvalidFieldName()

        if surface_name:
            surface_ids = self._field_info.get_surfaces_info()[surface_name][
                "surface_id"
            ]
            if len(self._file_session._data_file.get_phases()) > 1:
                if not field_name.startswith("phase-"):
                    raise InvalidMultiPhaseFieldName()
                vector_data = self._file_session._data_file.get_face_vector_field_data(
                    field_name.split(":")[0], surface_ids[0]
                )
            else:
                vector_data = self._file_session._data_file.get_face_vector_field_data(
                    "phase-1", surface_ids[0]
                )

            return VectorFieldData(surface_ids[0], vector_data, scale=1.0)
        else:
            if len(self._file_session._data_file.get_phases()) > 1:
                if not field_name.startswith("phase-"):
                    raise InvalidMultiPhaseFieldName()
                return {
                    surface_id: VectorFieldData(
                        surface_id,
                        self._file_session._data_file.get_face_vector_field_data(
                            field_name.split(":")[0], surface_id
                        ),
                        scale=1.0,
                    )
                    for surface_id in surface_ids
                }
            else:
                return {
                    surface_id: VectorFieldData(
                        surface_id,
                        self._file_session._data_file.get_face_vector_field_data(
                            "phase-1", surface_id
                        ),
                        scale=1.0,
                    )
                    for surface_id in surface_ids
                }

    def get_pathlines_field_data(
        self,
        field_name: str,
        surface_ids: Optional[List[int]] = None,
        surface_name: Optional[str] = None,
    ):
        """Get the pathlines field data on a surface.

        Parameters
        ----------
        field_name : str
            Name of the scalar field to color pathlines.
        surface_ids : List[int], optional
            List of surface IDs for pathlines field data.
        surface_name : str, optional
            Surface name for pathlines field data.

        Returns
        -------
        Dict
            Dictionary containing a map of surface IDs to the pathline data.
            For example, pathlines connectivity, vertices, and field.
        """
        raise NotImplementedError("Pathlines are not supported.")


class FileFieldInfo:
    """File field info."""

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
            data = self._file_session._data_file.get_face_scalar_field_data(
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

        scalar_field_info = {}

        if len(phases) > 1:
            for phase in phases:
                for face_variable in self._file_session._data_file.get_face_variables(
                    phase
                ):
                    if face_variable:
                        scalar_field_info[phase + ":" + face_variable] = {
                            "display_name": face_variable,
                            "section": "field-data",
                            "domain": phase,
                        }
        else:
            for face_variable in self._file_session._data_file.get_face_variables(
                phases[0]
            ):
                if face_variable:
                    scalar_field_info[face_variable] = {
                        "display_name": face_variable,
                        "section": "field-data",
                        "domain": phases[0],
                    }

        return scalar_field_info

    def get_vector_fields_info(self):
        """Get vector fields information (vector components).

        Returns
        -------
        Dict
        """
        phases = self._file_session._data_file.get_phases()

        if len(phases) > 1:
            return {
                phase
                + ":"
                + "velocity": {
                    "x-component": f"{phase}: SV_U",
                    "y-component": f"{phase}: SV_V",
                    "z-component": f"{phase}: SV_W",
                }
                for phase in phases
            }
        else:
            return {
                "velocity": {
                    "x-component": "SV_U",
                    "y-component": "SV_V",
                    "z-component": "SV_W",
                }
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
    """File session to read case and data file."""

    def __init__(self):
        """__init__ method of FileSession class."""
        self._case_file = None
        self._data_file = None
        self.field_info = FileFieldInfo(self)
        self.field_data = FileFieldData(self, self.field_info)
        self.monitors_manager = lambda: None
        self.session_id = 1

    def read_case(self, case_file_name):
        """Read Case file."""
        self._case_file = CaseFile(case_file_name)

    def read_data(self, data_file_name):
        """Read Data file."""
        self._data_file = DataFile(data_file_name, case_file_handle=self._case_file)
