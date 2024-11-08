"""Provides a module for file session."""

from typing import List
import warnings

import numpy as np

from ansys.api.fluent.v0.field_data_pb2 import DataLocation
from ansys.fluent.core import PyFluentDeprecationWarning
from ansys.fluent.core.filereader.case_file import CaseFile
from ansys.fluent.core.filereader.data_file import DataFile
from ansys.fluent.core.services.field_data import SurfaceDataType
from ansys.fluent.core.utils.deprecate import deprecate_argument, deprecate_arguments


class InvalidMultiPhaseFieldName(ValueError):
    """Raised when multi-phase field name is inappropriate."""

    def __init__(self):
        """Initialize InvalidMultiPhaseFieldName."""
        super().__init__("Multi-phase field name should start with 'phase-'.")


class InvalidFieldName(ValueError):
    """Raised when a field name is inappropriate."""

    def __init__(self):
        """Initialize InvalidFieldName."""
        super().__init__("The only allowed field is 'velocity'.")


def _data_type_convertor(args_dict):
    d_type_list = []
    d_type_map = {
        "provide_vertices": SurfaceDataType.Vertices,
        "provide_faces": SurfaceDataType.FacesConnectivity,
    }
    for key, val in d_type_map.items():
        if args_dict.get(key):
            d_type_list.append(val)
        args_dict.pop(key, None)
    args_dict["data_types"] = d_type_list
    return args_dict


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

    @deprecate_argument(
        old_arg="surface_names",
        new_arg="surfaces",
        converter=lambda old_arg_val: old_arg_val,
        warning_cls=PyFluentDeprecationWarning,
    )
    @deprecate_argument(
        old_arg="surface_ids",
        new_arg="surfaces",
        converter=lambda old_arg_val: old_arg_val,
        warning_cls=PyFluentDeprecationWarning,
    )
    @deprecate_arguments(
        converter=_data_type_convertor,
        warning_cls=PyFluentDeprecationWarning,
    )
    def add_surfaces_request(
        self,
        data_types: List[SurfaceDataType] | List[str],
        surfaces: List[int | str],
    ) -> None:
        """Add request to get surface data (vertices, face connectivity, centroids, and
        normals).

        Parameters
        ----------
        data_types : List[SurfaceDataType] | List[str],
            SurfaceDataType Enum members.
        surfaces : List[int | str]
            List of surface IDS or surface names for the surface data.

        Returns
        -------
        None
        """
        updated_types = []
        for d_type in data_types:
            if isinstance(d_type, str):
                updated_types.append(SurfaceDataType(d_type))
            else:
                updated_types.append(d_type)
        data_types = updated_types
        provide_vertices = SurfaceDataType.Vertices in data_types
        provide_faces = SurfaceDataType.FacesConnectivity in data_types
        surface_ids = _get_surface_ids(
            field_info=self._field_info,
            surfaces=surfaces,
        )
        for surface_id in surface_ids:
            self._surface_transactions.append(
                Transaction._SurfaceTransaction(
                    surface_id, provide_vertices, provide_faces
                )
            )

    @deprecate_argument(
        old_arg="surface_names",
        new_arg="surfaces",
        converter=lambda old_arg_val: old_arg_val,
        warning_cls=PyFluentDeprecationWarning,
    )
    @deprecate_argument(
        old_arg="surface_ids",
        new_arg="surfaces",
        converter=lambda old_arg_val: old_arg_val,
        warning_cls=PyFluentDeprecationWarning,
    )
    def add_scalar_fields_request(
        self,
        field_name: str,
        surfaces: List[int | str],
        node_value: bool | None = True,
        boundary_value: bool | None = True,
    ) -> None:
        """Add request to get scalar field data on surfaces.

        Parameters
        ----------
        field_name : str
            Name of the scalar field.
        surfaces : List[int | str]
            List of surface IDS or surface names for the surface data.
        node_value : bool, optional
            Whether to provide the nodal location. The default is ``True``. If
            ``False``, the element location is provided.
        boundary_value : bool, optional
            Whether to provide the slip velocity at the wall boundaries. The default
            is ``True``. When ``True``, no slip velocity is provided.

        Returns
        -------
        None

        Raises
        ------
        InvalidMultiPhaseFieldName
            If field name does not have prefix ``phase-`` for multi-phase cases.
        """
        surface_ids = _get_surface_ids(
            field_info=self._field_info,
            surfaces=surfaces,
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

    @deprecate_argument(
        old_arg="surface_names",
        new_arg="surfaces",
        converter=lambda old_arg_val: old_arg_val,
        warning_cls=PyFluentDeprecationWarning,
    )
    @deprecate_argument(
        old_arg="surface_ids",
        new_arg="surfaces",
        converter=lambda old_arg_val: old_arg_val,
        warning_cls=PyFluentDeprecationWarning,
    )
    def add_vector_fields_request(
        self,
        field_name: str,
        surfaces: List[int | str],
    ) -> None:
        """Add request to get vector field data on surfaces.

        Parameters
        ----------
        field_name : str
            Name of the vector field.
        surfaces : List[int | str]
            List of surface IDS or surface names for the surface data.

        Returns
        -------
        None

        Raises
        ------
        InvalidMultiPhaseFieldName
            If field name does not have prefix ``phase-`` for multi-phase cases.
        """
        surface_ids = _get_surface_ids(
            field_info=self._field_info,
            surfaces=surfaces,
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

    @deprecate_argument(
        old_arg="surface_names",
        new_arg="surfaces",
        converter=lambda old_arg_val: old_arg_val,
        warning_cls=PyFluentDeprecationWarning,
    )
    @deprecate_argument(
        old_arg="surface_ids",
        new_arg="surfaces",
        converter=lambda old_arg_val: old_arg_val,
        warning_cls=PyFluentDeprecationWarning,
    )
    def add_pathlines_fields_request(
        self,
        field_name: str,
        surfaces: List[int | str],
    ):
        """Add request to get pathlines field on surfaces.

        Parameters
        ----------
        field_name : str
            Name of the scalar field to color pathlines.
        surfaces : List[int | str]
            List of surface IDS or surface names for the surface data.

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
            tag int | Tuple-> surface_id [int] -> field_name [str] -> field_data[np.array]

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
        """Initialize FileFieldData."""
        self._file_session = file_session
        self._field_info = field_info

    def new_transaction(self):
        """Create a new field transaction."""
        return Transaction(self._file_session, self._field_info)

    @deprecate_argument(
        old_arg="surface_name",
        new_arg="surfaces",
        converter=lambda old_arg_val: [old_arg_val],
        warning_cls=PyFluentDeprecationWarning,
    )
    @deprecate_argument(
        old_arg="surface_ids",
        new_arg="surfaces",
        converter=lambda old_arg_val: old_arg_val,
        warning_cls=PyFluentDeprecationWarning,
    )
    @deprecate_argument(
        old_arg="data_type",
        new_arg="data_types",
        converter=lambda old_arg_val: [old_arg_val] if old_arg_val else None,
        warning_cls=PyFluentDeprecationWarning,
    )
    def get_surface_data(
        self,
        data_types: List[SurfaceDataType] | List[str],
        surfaces: List[int | str],
        overset_mesh: bool | None = False,
    ):
        """Get surface data (vertices and faces connectivity).

        Parameters
        ----------
        data_types : List[SurfaceDataType] | List[str],
            SurfaceDataType Enum members.
        surfaces : List[int | str]
            List of surface IDS or surface names for the surface data.
        overset_mesh : bool, optional
            Whether to provide the overset method. The default is ``False``.

        Returns
        -------
        Vertices | FacesConnectivity | Dict[int, Vertices | FacesConnectivity]
             If a surface name is provided as input, face vertices, connectivity data, and normal or centroid data are returned.
             If surface IDs are provided as input, a dictionary containing a map of surface IDs to face
             vertices, connectivity data, and normal or centroid data is returned.
        """

        for d_type in data_types:
            if isinstance(d_type, str):
                data_types.remove(d_type)
                data_types.append(SurfaceDataType(d_type))

        surface_ids = _get_surface_ids(
            field_info=self._field_info,
            surfaces=surfaces,
        )

        if SurfaceDataType.Vertices in data_types:
            return {
                surface: self._file_session._case_file.get_mesh()
                .get_vertices(surface_ids[count])
                .reshape(-1, 3)
                for count, surface in enumerate(surfaces)
            }

        if SurfaceDataType.FacesConnectivity in data_types:
            return {
                surface: self._get_faces_connectivity_data(
                    self._file_session._case_file.get_mesh().get_connectivity(
                        surface_ids[count]
                    )
                )
                for count, surface in enumerate(surfaces)
            }

    @staticmethod
    def _get_faces_connectivity_data(data):
        faces_data = []
        i = 0
        while i < len(data):
            end = i + 1 + data[i]
            faces_data.append(data[i + 1 : end])
            i = end
        return faces_data

    @deprecate_argument(
        old_arg="surface_name",
        new_arg="surfaces",
        converter=lambda old_arg_val: [old_arg_val],
        warning_cls=PyFluentDeprecationWarning,
    )
    @deprecate_argument(
        old_arg="surface_ids",
        new_arg="surfaces",
        converter=lambda old_arg_val: old_arg_val,
        warning_cls=PyFluentDeprecationWarning,
    )
    def get_scalar_field_data(
        self,
        field_name: str,
        surfaces: List[int | str],
        node_value: bool | None = True,
        boundary_value: bool | None = True,
    ):
        """Get scalar field data on a surface.

        Parameters
        ----------
        field_name : str
            Name of the scalar field.
        surfaces : List[int | str]
            List of surface IDS or surface names for the surface data.
        node_value : bool, optional
            Whether to provide data for the nodal location. The default is ``True``.
            When ``False``, data is provided for the element location.
        boundary_value : bool, optional
            Whether to provide slip velocity at the wall boundaries. The default is
            ``True``. When ``True``, no slip velocity is provided.

        Returns
        -------
        ScalarFieldData | Dict[int, ScalarFieldData]
            If a surface name is provided as input, scalar field data is returned. If surface
            IDs are provided as input, a dictionary containing a map of surface IDs to scalar
            field data.

        Raises
        ------
        InvalidMultiPhaseFieldName
            If field name does not have prefix ``phase-`` for multi-phase cases.
        """
        surface_ids = _get_surface_ids(
            field_info=self._field_info,
            surfaces=surfaces,
        )
        if len(self._file_session._data_file.get_phases()) > 1:
            if not field_name.startswith("phase-"):
                raise InvalidMultiPhaseFieldName()
            return {
                surface: self._file_session._data_file.get_face_scalar_field_data(
                    field_name.split(":")[0],
                    field_name.split(":")[1],
                    surface_ids[count],
                )
                for count, surface in enumerate(surfaces)
            }
        else:
            return {
                surface: self._file_session._data_file.get_face_scalar_field_data(
                    "phase-1", field_name, surface_ids[count]
                )
                for count, surface in enumerate(surfaces)
            }

    @deprecate_argument(
        old_arg="surface_name",
        new_arg="surfaces",
        converter=lambda old_arg_val: [old_arg_val],
        warning_cls=PyFluentDeprecationWarning,
    )
    @deprecate_argument(
        old_arg="surface_ids",
        new_arg="surfaces",
        converter=lambda old_arg_val: old_arg_val,
        warning_cls=PyFluentDeprecationWarning,
    )
    def get_vector_field_data(
        self,
        field_name: str,
        surfaces: List[int | str],
    ):
        """Get vector field data on a surface.

        Parameters
        ----------
        field_name : str
            Name of the vector field.
        surfaces : List[int | str]
            List of surface IDS or surface names for the surface data.

        Returns
        -------
        VectorFieldData | Dict[int, VectorFieldData]
            If a surface name is provided as input, vector field data is returned.
            If surface IDs are provided as input, a dictionary containing a map of
            surface IDs to vector field data is returned.

        Raises
        ------
        InvalidFieldName
            If any field other than ``"velocity"`` is provided.
        InvalidMultiPhaseFieldName
            If field name does not have prefix ``phase-`` for multi-phase cases.
        """
        surface_ids = _get_surface_ids(
            field_info=self._field_info,
            surfaces=surfaces,
        )
        if (
            field_name.lower() != "velocity"
            and field_name.split(":")[1].lower() != "velocity"
        ):
            raise InvalidFieldName()

        if len(self._file_session._data_file.get_phases()) > 1:
            if not field_name.startswith("phase-"):
                raise InvalidMultiPhaseFieldName()
            return {
                surface: self._file_session._data_file.get_face_vector_field_data(
                    field_name.split(":")[0], surface_ids[count]
                ).reshape(-1, 3)
                for count, surface in enumerate(surfaces)
            }
        else:
            return {
                surface: self._file_session._data_file.get_face_vector_field_data(
                    "phase-1", surface_ids[count]
                ).reshape(-1, 3)
                for count, surface in enumerate(surfaces)
            }

    @deprecate_argument(
        old_arg="surface_name",
        new_arg="surfaces",
        converter=lambda old_arg_val: [old_arg_val],
        warning_cls=PyFluentDeprecationWarning,
    )
    @deprecate_argument(
        old_arg="surface_ids",
        new_arg="surfaces",
        converter=lambda old_arg_val: old_arg_val,
        warning_cls=PyFluentDeprecationWarning,
    )
    def get_pathlines_field_data(
        self,
        field_name: str,
        surfaces: List[int | str],
    ):
        """Get the pathlines field data on a surface.

        Parameters
        ----------
        field_name : str
            Name of the scalar field to color pathlines.
        surfaces : List[int | str]
            List of surface IDS or surface names for the surface data.

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
        """Initialize FileFieldInfo."""
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
        self.monitors = None
        self.session_id = 1

        class Fields:
            """Container for field and solution variables."""

            def __init__(self, _session):
                """Initialize Fields."""
                self.field_info = FileFieldInfo(_session)
                self.field_data = FileFieldData(_session, self.field_info)

        self.fields = Fields(self)

    def read_case(self, case_file_name):
        """Read Case file."""
        self._case_file = CaseFile(case_file_name)

    def read_data(self, data_file_name):
        """Read Data file."""
        self._data_file = DataFile(data_file_name, case_file_handle=self._case_file)

    @property
    def field_info(self):
        """Provides access to Fluent field information."""
        warnings.warn(
            "field_info is deprecated. Use fields.field_info instead.",
            PyFluentDeprecationWarning,
        )
        return self.fields.field_info

    @property
    def field_data(self):
        """Fluent field data on surfaces."""
        warnings.warn(
            "field_data is deprecated. Use fields.field_data instead.",
            PyFluentDeprecationWarning,
        )
        return self.fields.field_data


def _get_surface_ids(
    field_info: FileFieldInfo,
    surfaces: List[int | str],
) -> List[int]:
    """Get surface IDs based on surface names or IDs.

    Parameters
    ----------
    surfaces : List[int], | List[str]
        List of surface IDs or surface names.

    Returns
    -------
    List[int]
    """
    surface_ids = []
    for surf in surfaces:
        if isinstance(surf, str):
            surface_ids.extend(field_info.get_surfaces_info()[surf]["surface_id"])
        else:
            surface_ids.append(surf)
    return surface_ids
