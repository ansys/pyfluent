# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
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

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
import dataclasses
from typing import TYPE_CHECKING, Iterable
import warnings

from ansys.fluent.core.exceptions import DisallowedValuesError

if TYPE_CHECKING:

    from ansys.units.variable_descriptor import (
        ScalarVariableDescriptor,
        VariableDescriptor,
        VectorVariableDescriptor,
    )


def _set_dataclass_field_docs(cls: type, field_docs: dict[str, str]) -> None:
    """Set docstrings for dataclass-generated field attributes.

    Without this, Sphinx may render default ``dataclass`` field docs like
    "Alias for field number N" in attribute/member tables.
    """
    if dataclasses.is_dataclass(cls):
        # Update metadata dict inside dataclass fields for Sphinx/autodoc parsing
        for field in dataclasses.fields(cls):
            if field.name in field_docs:
                # Add to metadata dict (or modify existing proxy wrapper)
                current_metadata = dict(field.metadata)
                current_metadata["doc"] = field_docs[field.name]
                field.metadata = current_metadata
        return


def _validate_scalar_variable_descriptor(
    field_name: "ScalarVariableDescriptor",
) -> None:
    """Validate that the provided field_name is a ScalarVariableDescriptor."""
    from ansys.units.variable_descriptor import ScalarVariableDescriptor

    if not isinstance(field_name, ScalarVariableDescriptor):
        raise TypeError("field_name must be a `ScalarVariableDescriptor`.")


def _validate_vector_variable_descriptor(
    field_name: "VectorVariableDescriptor",
) -> None:
    """Validate that the provided field_name is a VectorVariableDescriptor."""
    from ansys.units.variable_descriptor import VectorVariableDescriptor

    if not isinstance(field_name, VectorVariableDescriptor):
        raise TypeError("field_name must be a `VectorVariableDescriptor`.")


class _BaseFieldInfo(ABC):
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
    def _get_scalar_field_range(
        self,
        field: str | "ScalarVariableDescriptor",
        node_value: bool = False,
        surface_ids: list[int] | None = None,
    ) -> list[float]:
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

        Raises
        ------
        TypeError
            If `field` is not a scalar.
        """
        if not isinstance(field, (str)):
            _validate_scalar_variable_descriptor(field)

    @abstractmethod
    def _get_scalar_fields_info(self) -> dict[str, dict]:
        """
        Retrieve information about available scalar fields.

        This includes field names, associated domains, and sections.

        Returns
        -------
            Dict[str, Dict]: A dictionary containing scalar field metadata.
        """
        pass

    @abstractmethod
    def _get_vector_fields_info(self) -> dict[str, dict]:
        """ "
        Retrieve information about available vector fields.

        This includes vector components and relevant metadata.

        Returns
        -------
            Dict[str, Dict]: A dictionary containing vector field metadata.
        """
        pass

    @abstractmethod
    def _get_surfaces_info(self) -> dict[str, dict]:
        """
        Retrieve information about available surfaces.

        This includes surface names, IDs, and types.

        Returns
        -------
            Dict[str, Dict]: A dictionary containing surface metadata.
        """
        pass


class _SurfaceNames:
    def __init__(self, allowed_surface_names):
        self._allowed_surface_names = allowed_surface_names

    def allowed_values(self):
        """Lists available surface names."""
        return list(self._allowed_surface_names())

    def validate(self, surfaces: list[str]) -> bool:
        """
        Validate that the given surfaces are in the list of allowed surface names.

        Parameters
        ----------
        surfaces : List[int]
            A list of surface name strings to validate.

        Returns
        -------
        bool
            True if all surfaces are valid, False otherwise.
            If any name is invalid, a warning is issued and validation stops early.
        """
        for surf in surfaces:
            if surf not in self._allowed_surface_names():
                warnings.warn(f"'{surf}' is not a valid surface name.")
                return False
        return True

    def __call__(self):
        return self._allowed_surface_names()


class _SurfaceIds:
    def __init__(self, allowed_surface_ids):
        self._allowed_surface_ids = allowed_surface_ids

    def allowed_values(self):
        """Lists available surface ids."""
        return self._allowed_surface_ids()

    def validate(self, surface_ids: list[int]) -> bool:
        """
        Validate that the given surface IDs are in the list of allowed surface IDs.

        Parameters
        ----------
        surface_ids : List[int]
            A list of surface ID integers to validate.

        Returns
        -------
        bool
            True if all surface IDs are valid, False otherwise.
            If any ID is invalid, a warning is issued and validation stops early.
        """
        for surf in surface_ids:
            if surf not in self._allowed_surface_ids():
                warnings.warn(f"'{surf}' is not a valid surface id.")
                return False
        return True

    def __call__(self):
        return self._allowed_surface_ids()


class _Fields:
    def __init__(self, available_field_names):
        self._available_field_names = available_field_names

    def is_active(self, field_name: "VariableDescriptor" | str) -> bool:
        """Check whether a field is active in the given context.

        Parameters
        ----------
        field_name : VariableDescriptor | str
            Field name to check. Can be a VariableDescriptor or a string.
        """
        from ansys.fluent.core._variable_strategies import (
            FluentFieldDataNamingStrategy as naming_strategy,
        )

        _naming_strategy_instance = naming_strategy()
        _to_field_name_str = _naming_strategy_instance.to_string
        return _to_field_name_str(field_name) in self._available_field_names()

    def allowed_values(self):
        """Lists available scalar or vector field names as strings."""
        return list(self._available_field_names())

    def allowed_variables(self) -> list["VariableDescriptor"]:
        """Return allowed field names as VariableDescriptor objects.

        Returns
        -------
        list[VariableDescriptor]
            List of VariableDescriptor objects for all allowed fields.
            Fields without a corresponding VariableDescriptor are excluded,
            and a warning is issued listing them.
        """
        from ansys.fluent.core._variable_strategies import (
            FluentFieldDataNamingStrategy as naming_strategy,
        )

        _naming_strategy_instance = naming_strategy()
        descriptors = []
        unmatched = []
        for field_name in self._available_field_names():
            descriptor = _naming_strategy_instance.to_variable_descriptor(field_name)
            if descriptor is not None:
                descriptors.append(descriptor)
            else:
                unmatched.append(field_name)
        if unmatched:
            warnings.warn(
                "The following variables are available but do not have "
                f"corresponding descriptors: {', '.join(sorted(unmatched))}",
                stacklevel=2,
            )
        return descriptors

    def __call__(self):
        return self._available_field_names()


class _ScalarFields(_Fields):
    def __init__(self, available_field_names, field_info):
        super().__init__(available_field_names)
        self._field_info = field_info

    def range(
        self, field: str, node_value: bool = False, surface_ids: list[int] | None = None
    ) -> list[float]:
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
        return self._field_info._get_scalar_field_range(field, node_value, surface_ids)


class _VectorFields(_Fields):
    def __init__(self, available_field_names):
        super().__init__(available_field_names)


class _AllowedNames:
    def __init__(
        self, field_info: _BaseFieldInfo | None = None, info: dict | None = None
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
        field_info: _BaseFieldInfo | None = None,
        info: dict | None = None,
    ):
        super().__init__(field_info=field_info, info=info)
        self._is_data_valid = is_data_valid

    def valid_name(self, field_name):
        """Returns valid names.

        Raises
        ------
        DisallowedValuesError
            If field name is invalid.
        FieldUnavailableError
            If field name is valid but not currently available.
        """
        from ansys.fluent.core.exceptions import DisallowedValuesError

        if validate_inputs:
            names = self
            if not names.is_valid(field_name, respect_data_valid=False):
                raise DisallowedValuesError(
                    context="field",
                    name=field_name,
                    allowed_values=list(names(respect_data_valid=False).keys()),
                )
            if not names.is_valid(field_name, respect_data_valid=True):
                raise FieldUnavailableError(
                    f"{field_name} is not a currently available field."
                )
        return field_name


class _AllowedSurfaceNames(_AllowedNames):
    def __call__(self, respect_data_valid: bool = True) -> list[str]:
        return self._info if self._info else self._field_info._get_surfaces_info()

    def valid_name(self, surface_name: str) -> str:
        """Returns valid names.

        Raises
        ------
        RuntimeError
            If issue in retrieving surface list.
        DisallowedValuesError
            If surface name is invalid.
        """
        from ansys.fluent.core.exceptions import DisallowedValuesError

        try:
            valid_names = self()  # Fetch once, upfront
        except Exception as e:
            raise RuntimeError("Failed to retrieve valid surface names.") from e

        if validate_inputs and surface_name not in valid_names:
            raise DisallowedValuesError("surface", surface_name, valid_names)

        return surface_name


class _AllowedSurfaceIDs(_AllowedNames):
    def __call__(self, respect_data_valid: bool = True) -> list[int]:
        try:
            return [
                info["surface_id"][0]
                for _, info in self._field_info._get_surfaces_info().items()
            ]
        except (KeyError, IndexError):
            warnings.warn("Unable to retrieve surface ids from Fluent")
            return []


class FieldUnavailableError(RuntimeError):
    """Raised when field is unavailable."""

    pass


class _AllowedScalarFieldNames(_AllowedFieldNames):

    def __call__(self, respect_data_valid: bool = True) -> list[str]:
        field_dict = (
            self._info if self._info else self._field_info._get_scalar_fields_info()
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

    def __call__(self, respect_data_valid: bool = True) -> list[str]:
        return (
            self._info
            if self._info
            else (
                self._field_info._get_vector_fields_info()
                if (not respect_data_valid or self._is_data_valid())
                else []
            )
        )

    def is_valid(self, name, respect_data_valid=True):
        """Checks validity."""
        return name in self(respect_data_valid)


def _get_surfaces_from_objects(surfaces: list[int | str | object]):
    """
    Extract surface names or identifiers from a list of surfaces.

    Parameters
    ----------
    surfaces : List[int | str | object]
        A list of surface identifiers, which may include:
          - integers or strings representing surface names/IDs,
          - objects with a callable `name()` method,
          - or iterables (e.g., lists or tuples) containing such elements.

    Returns
    -------
    List
        A flattened list of surface names/identifiers:
          - If an element has a `name()` method, the result of `surface.name()` is used.
          - Otherwise, the element itself is returned as-is.
    """
    updated_surfaces = []
    for surface in surfaces:
        if hasattr(surface, "name"):
            updated_surfaces.append(surface.name())
        else:
            updated_surfaces.append(surface)
    return updated_surfaces


def _transform_faces_connectivity_data(data):
    """
    Transform flat face connectivity data into structured face-wise format.

    Each face in the flat array is represented by:
    [N, v0, v1, ..., vN], where:
      - N is the number of vertices in the face
      - v0...vN are the vertex indices

    This function parses such a flat array and returns a list of vertex index arrays,
    each representing a face.

    Parameters
    ----------
    data : array-like of int
        Flat array containing face connectivity data, typically returned from
        `faces_connectivity_data["inlet"].connectivity`.

    Returns
    -------
    faces_data : list of ndarray
        List of 1D NumPy arrays, where each array contains the vertex indices
        of a face.

    Examples
    --------
    >>> flat_data = np.array([4, 4, 5, 12, 11, 3, 1, 2, 3], dtype=np.int32)
    >>> _transform_faces_connectivity_data(flat_data)
    [array([ 4,  5, 12, 11]), array([1, 2, 3])]
    """
    faces_data = []
    i = 0
    while i < len(data):
        end = i + 1 + data[i]
        faces_data.append(data[i + 1 : end])
        i = end
    return faces_data


def _get_surface_ids(
    field_info: _BaseFieldInfo,
    allowed_surface_names,
    surfaces: list[int | str | object],
) -> list[int]:
    """Get surface IDs based on surface names or IDs.

    Parameters
    ----------
    surfaces : List[int] | List[str]
        List of surface IDs or surface names.

    Returns
    -------
    List[int]
    """
    surface_ids = []
    updated_surfaces = _get_surfaces_from_objects(surfaces)
    for surf in updated_surfaces:
        if isinstance(surf, str):
            surface_ids.extend(
                field_info._get_surfaces_info()[allowed_surface_names.valid_name(surf)][
                    "surface_id"
                ]
            )
        else:
            allowed_surf_ids = _AllowedSurfaceIDs(field_info)()
            if surf in allowed_surf_ids:
                surface_ids.append(surf)
            elif isinstance(surf, Iterable) and not isinstance(surf, (str, bytes)):
                raise DisallowedValuesError("surface", surf, list(surf))
            else:
                raise DisallowedValuesError("surface", surf, allowed_surf_ids)
    return surface_ids
