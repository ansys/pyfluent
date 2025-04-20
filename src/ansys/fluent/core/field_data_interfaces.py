# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Common interfaces for field data."""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable, Dict, List, NamedTuple

import numpy as np
import numpy.typing as npt

from ansys.fluent.core.exceptions import DisallowedValuesError


class SurfaceDataType(Enum):
    """Provides surface data types."""

    Vertices = "vertices"
    FacesConnectivity = "faces"
    FacesNormal = "face-normal"
    FacesCentroid = "centroid"


class SurfaceFieldDataRequest(NamedTuple):
    """Container storing parameters for surface data request."""

    data_types: List[SurfaceDataType] | List[str]
    surfaces: List[int | str]
    overset_mesh: bool | None = False


class ScalarFieldDataRequest(NamedTuple):
    """Container storing parameters for scalar field data request."""

    field_name: str
    surfaces: List[int | str]
    node_value: bool | None = True
    boundary_value: bool | None = True


class VectorFieldDataRequest(NamedTuple):
    """Container storing parameters for vector field data request."""

    field_name: str
    surfaces: List[int | str]


class PathlinesFieldDataRequest(NamedTuple):
    """Container storing parameters for path-lines field data request."""

    field_name: str
    surfaces: List[int | str]
    additional_field_name: str = ""
    provide_particle_time_field: bool | None = False
    node_value: bool | None = True
    steps: int | None = 500
    step_size: float | None = 500
    skip: int | None = 0
    reverse: bool | None = False
    accuracy_control_on: bool | None = False
    tolerance: float | None = 0.001
    coarsen: int | None = 1
    velocity_domain: str | None = "all-phases"
    zones: list | None = None


class BaseFieldInfo(ABC):
    """
    Abstract base class for field information retrieval.

    This class defines the interface for obtaining metadata about scalar and vector fields,
    as well as surface details. It provides abstract methods that allow users to implement
    their own data sources for retrieving field value ranges,  field characteristics,
    and surface information.

    Implementing classes should define:
    - Methods to retrieve the range of scalar fields.
    - Methods to obtain metadata about scalar and vector fields.
    - Methods to retrieve surface-related information.

    Subclasses must provide concrete implementations for all abstract methods.
    """

    @abstractmethod
    def get_scalar_field_range(
        self, field: str, node_value: bool = False, surface_ids: List[int] = None
    ) -> List[float]:
        """
        Retrieve the range (minimum and maximum values) of a scalar field.

        Parameters
        ----------
            field (str): The name of the scalar field.
            node_value (bool, optional): Whether to retrieve node-based values instead of element-based. Defaults to False.
            surface_ids (List[int], optional): List of surface IDs for filtering data. Defaults to None.

        Returns
        -------
            List[float]: A list containing the minimum and maximum values of the requested scalar field.
        """
        pass

    @abstractmethod
    def get_scalar_fields_info(self) -> Dict[str, Dict]:
        """
        Retrieve information about available scalar fields.

        This includes field names, associated domains, and sections.

        Returns
        -------
            Dict[str, Dict]: A dictionary containing scalar field metadata.
        """
        pass

    @abstractmethod
    def get_vector_fields_info(self) -> Dict[str, Dict]:
        """ "
        Retrieve information about available vector fields.

        This includes vector components and relevant metadata.

        Returns
        -------
            Dict[str, Dict]: A dictionary containing vector field metadata.
        """
        pass

    @abstractmethod
    def get_surfaces_info(self) -> Dict[str, Dict]:
        """
        Retrieve information about available surfaces.

        This includes surface names, IDs, and types.

        Returns
        -------
            Dict[str, Dict]: A dictionary containing surface metadata.
        """
        pass


class BaseFieldDataSource(ABC):
    """
    Abstract base class for accessing field data.

    This class defines the interface for retrieving field data based on user requests.
    It provides abstract methods that allow users to implement their own data sources
    for fetching field data related to surfaces, scalars, vectors, or pathlines.

    Implementing classes should define:
    - A method to obtain surface IDs from user-provided surface names or numerical identifiers.
    - A method to retrieve field data based on a given request.

    Subclasses must provide concrete implementations for all abstract methods.
    """

    @abstractmethod
    def get_surface_ids(self, surfaces: List[str | int]) -> List[int]:
        """Retrieve a list of surface IDs based on input surface names or numerical identifiers."""
        pass

    @abstractmethod
    def get_field_data(
        self,
        obj: (
            SurfaceFieldDataRequest
            | ScalarFieldDataRequest
            | VectorFieldDataRequest
            | PathlinesFieldDataRequest
        ),
    ) -> Dict[int | str, Dict | np.array]:
        """
        Retrieve the field data for a given request.

        This method processes the specified request and returns the corresponding
        field data in a structured format.

        Returns
        -------
            Dict[int | str, Dict | np.array]: A dictionary where keys represent surface
            IDs or names, and values contain the corresponding field data.
        """
        pass


class FieldDataSource(BaseFieldDataSource, ABC):
    """
    Abstract base class for accessing field data.

    This class defines the interface for retrieving field data based on user requests.
    In addition to the methods in `BaseFieldDataSource` it provides a method to create
    new field transaction objects.

    Implementing classes should define:
    - A method to obtain surface IDs from user-provided surface names or numerical identifiers.
    - A method to retrieve field data based on a given request.
    - A method to create new field transaction.

    Subclasses must provide concrete implementations for all abstract methods.
    """

    @abstractmethod
    def new_transaction(self):
        """Create a new field transaction."""
        pass


class FieldTransaction(ABC):
    """
    Abstract base class for handling field data transactions.

    This class defines the interface for requesting field data based on user inputs
    and retrieving responses from the server. It provides abstract methods that allow
    users to develop their own implementations for interacting with different field
    data sources.

    Implementing classes should define:
    - Methods to obtain surface IDs from user-provided surface names or identifiers.
    - A mechanism to add requests for different types of field data (surface, scalar,
      vector, or pathlines).
    - A method to fetch the response containing the requested field data.

    Subclasses must provide concrete implementations for all abstract methods.
    """

    @abstractmethod
    def get_surface_ids(self, surfaces: List[str | int]) -> List[int]:
        """Retrieve a list of surface IDs based on input surface names or numerical identifiers."""
        pass

    @abstractmethod
    def add_requests(
        self,
        obj: (
            SurfaceFieldDataRequest
            | ScalarFieldDataRequest
            | VectorFieldDataRequest
            | PathlinesFieldDataRequest
        ),
        *args: SurfaceFieldDataRequest
        | ScalarFieldDataRequest
        | VectorFieldDataRequest
        | PathlinesFieldDataRequest,
    ):
        """
        Add field data requests for surfaces, scalars, vectors, or pathlines.

        This method allows users to specify multiple field data requests, which will
        later be processed when retrieving responses.
        """
        pass

    @abstractmethod
    def get_response(self) -> FieldDataSource:
        """
        Retrieve the response containing data for previously added field requests.

        This method processes all pending requests and returns the corresponding
        field data.
        """
        pass


class _AllowedNames:
    def __init__(
        self, field_info: BaseFieldInfo | None = None, info: dict | None = None
    ):
        self._field_info = field_info
        self._info = info

    def is_valid(self, name, respect_data_valid=True):
        """Checks validity."""
        return name in self(respect_data_valid)


# this can be switched to False in scenarios where the field_data request inputs are
# fed by results of field_info queries, which might be true in GUI code.
validate_inputs = True


class _AllowedFieldNames(_AllowedNames):
    def __init__(
        self,
        is_data_valid: Callable[[], bool],
        field_info: BaseFieldInfo | None = None,
        info: dict | None = None,
    ):
        super().__init__(field_info=field_info, info=info)
        self._is_data_valid = is_data_valid

    def valid_name(self, field_name):
        """Returns valid names."""
        if validate_inputs:
            names = self
            if not names.is_valid(field_name, respect_data_valid=False):
                raise self._field_name_error(
                    context="field",
                    name=field_name,
                    allowed_values=list(names(respect_data_valid=False).keys()),
                )
            if not names.is_valid(field_name, respect_data_valid=True):
                raise self._field_unavailable_error(
                    f"{field_name} is not a currently available field."
                )
        return field_name


class _AllowedSurfaceNames(_AllowedNames):
    def __call__(self, respect_data_valid: bool = True) -> List[str]:
        return self._info if self._info else self._field_info.get_surfaces_info()

    def valid_name(self, surface_name: str) -> str:
        """Returns valid names.

        Raises
        ------
        RuntimeError
            If issue in retrieving surface list.
        DisallowedValuesError
            If surface name is invalid.
        """
        try:
            valid_names = self()  # Fetch once, upfront
        except Exception as e:
            raise RuntimeError("Failed to retrieve valid surface names.") from e

        if validate_inputs and surface_name not in valid_names:
            raise DisallowedValuesError("surface", surface_name, valid_names)

        return surface_name


class _AllowedSurfaceIDs(_AllowedNames):
    def __call__(self, respect_data_valid: bool = True) -> List[int]:
        try:
            return [
                info["surface_id"][0]
                for _, info in self._field_info.get_surfaces_info().items()
            ]
        except (KeyError, IndexError):
            pass


class FieldUnavailable(RuntimeError):
    """Raised when field is unavailable."""

    pass


class _AllowedScalarFieldNames(_AllowedFieldNames):
    _field_name_error = DisallowedValuesError
    _field_unavailable_error = FieldUnavailable

    def __call__(self, respect_data_valid: bool = True) -> List[str]:
        field_dict = (
            self._info if self._info else self._field_info.get_scalar_fields_info()
        )
        return (
            field_dict
            if (not respect_data_valid or self._is_data_valid())
            else [
                name
                for name, info in field_dict.items()
                if info["section"] in ("Mesh...", "Cell Info...")
            ]
        )


class _AllowedVectorFieldNames(_AllowedFieldNames):
    _field_name_error = DisallowedValuesError
    _field_unavailable_error = FieldUnavailable

    def __call__(self, respect_data_valid: bool = True) -> List[str]:
        return (
            self._info
            if self._info
            else (
                self._field_info.get_vector_fields_info()
                if (not respect_data_valid or self._is_data_valid())
                else []
            )
        )

    def is_valid(self, name, respect_data_valid=True):
        """Checks validity."""
        return name in self(respect_data_valid)


class SurfaceData:
    """
    Class that enables object-style access to surface data structures.

    Attributes
    ----------
    vertices: npt.NDArray[np.float64] | None
    connectivity: list[npt.NDArray[np.float64]] | None
    face_centroids: npt.NDArray[np.float64] | None
    face_normals: npt.NDArray[np.float64] | None
    """

    def __init__(self, surf_data):
        """__init__ method of SurfaceData class."""
        self._surf_data = surf_data
        self.vertices: npt.NDArray[np.float64] | None = self._surf_data.get(
            SurfaceDataType.Vertices
        )
        self.connectivity: list[npt.NDArray[np.int32]] | None = self._surf_data.get(
            SurfaceDataType.FacesConnectivity
        )
        self.face_centroids: npt.NDArray[np.float64] | None = self._surf_data.get(
            SurfaceDataType.FacesCentroid
        )
        self.face_normals: npt.NDArray[np.float64] | None = self._surf_data.get(
            SurfaceDataType.FacesNormal
        )


class PathlinesData:
    """
    Class that enables object-style access to pathlines data structure.

    Attributes
    ----------
    scalar_field_name: str
    vertices: npt.NDArray[np.float64] | None
    lines: list[npt.NDArray[np.float64]] | None
    scalar_field: npt.NDArray[np.float64] | None
    pathlines_count: npt.NDArray[np.float64] | None
    particle_time: npt.NDArray[np.float64] | None
    """

    def __init__(self, pathlines_data_for_surface):
        """__init__ method of PathlinesData class."""
        self._pathlines_data_for_surface = pathlines_data_for_surface
        self.scalar_field_name: str = list(
            set(self._pathlines_data_for_surface.keys())
            - {"lines", "vertices", "pathlines-count", "particle-time"}
        )[0]
        self.vertices: npt.NDArray[np.float64] | None = (
            self._pathlines_data_for_surface.get("vertices")
        )
        self.lines: list[npt.NDArray[np.int32]] | None = (
            self._pathlines_data_for_surface.get("lines")
        )
        self.scalar_field: npt.NDArray[np.float64] | None = (
            self._pathlines_data_for_surface.get(self.scalar_field_name)
        )
        self.pathlines_count: npt.NDArray[np.float64] | None = (
            self._pathlines_data_for_surface.get("pathlines-count")
        )
        self.particle_time: npt.NDArray[np.float64] | None = (
            self._pathlines_data_for_surface.get("particle-time")
        )


class _ReturnFieldData:

    @staticmethod
    def _get_faces_connectivity_data(data):
        faces_data = []
        i = 0
        while i < len(data):
            end = i + 1 + data[i]
            faces_data.append(data[i + 1 : end])
            i = end
        return faces_data

    @staticmethod
    def _scalar_data(
        field_name: str,
        surfaces: List[int | str],
        surface_ids: List[int],
        scalar_field_data: np.array,
    ) -> Dict[int | str, np.array]:
        return {
            surface: scalar_field_data[surface_ids[count]][field_name]
            for count, surface in enumerate(surfaces)
        }

    @staticmethod
    def _surface_data(
        data_types: List[SurfaceDataType],
        surfaces: List[int | str],
        surface_ids: List[int],
        surface_data: np.array | List[np.array],
        deprecated_flag: bool | None = False,
    ) -> Dict[int | str, Dict[SurfaceDataType, np.array | List[np.array]]]:
        ret_surf_data = {}
        for count, surface in enumerate(surfaces):
            ret_surf_data[surface] = {}
            for data_type in data_types:
                if data_type == SurfaceDataType.FacesConnectivity:
                    ret_surf_data[surface][data_type] = (
                        _ReturnFieldData._get_faces_connectivity_data(
                            surface_data[surface_ids[count]][
                                SurfaceDataType.FacesConnectivity.value
                            ]
                        )
                    )
                else:
                    ret_surf_data[surface][data_type] = surface_data[
                        surface_ids[count]
                    ][data_type.value].reshape(-1, 3)
            if deprecated_flag is False:
                ret_surf_data[surface] = SurfaceData(ret_surf_data[surface])
        return ret_surf_data

    @staticmethod
    def _vector_data(
        field_name: str,
        surfaces: List[int | str],
        surface_ids: List[int],
        vector_field_data: np.array,
    ) -> Dict[int | str, np.array]:
        return {
            surface: vector_field_data[surface_ids[count]][field_name].reshape(-1, 3)
            for count, surface in enumerate(surfaces)
        }

    @staticmethod
    def _pathlines_data(
        field_name: str,
        surfaces: List[int | str],
        surface_ids: List[int],
        pathlines_data: Dict,
        deprecated_flag: bool | None = False,
    ) -> Dict:
        path_lines_dict = {}
        for count, surface in enumerate(surfaces):
            temp_dict = {
                "vertices": pathlines_data[surface_ids[count]]["vertices"].reshape(
                    -1, 3
                ),
                "lines": _ReturnFieldData._get_faces_connectivity_data(
                    pathlines_data[surface_ids[count]]["lines"]
                ),
                field_name: pathlines_data[surface_ids[count]][field_name],
                "pathlines-count": pathlines_data[surface_ids[count]][
                    "pathlines-count"
                ],
            }
            if "particle-time" in pathlines_data[surface_ids[count]]:
                temp_dict["particle-time"] = pathlines_data[surface_ids[count]][
                    "particle-time"
                ]
            if deprecated_flag is False:
                path_lines_dict[surface] = PathlinesData(temp_dict)
            else:
                path_lines_dict[surface] = temp_dict
        return path_lines_dict
