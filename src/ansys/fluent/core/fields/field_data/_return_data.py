# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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

"""Internal converters for Fluent field-data transport responses."""

import warnings

import numpy as np

from ansys.fluent.core.fields.field_data._field_data_interfaces import (
    _get_surfaces_from_objects,
    _transform_faces_connectivity_data,
)
from ansys.fluent.core.fields.field_data.data_types import PathlinesData, SurfaceData
from ansys.fluent.core.fields.field_data.requests import SurfaceDataType


class _ReturnFieldData:
    @staticmethod
    def _scalar_data(
        field_name: str,
        surfaces: list[int | str | object],
        surface_ids: list[int],
        scalar_field_data: np.ndarray,
    ) -> dict[int | str, np.ndarray]:
        surfaces = _get_surfaces_from_objects(surfaces)
        return {
            surface: scalar_field_data[surface_ids[count]][field_name]
            for count, surface in enumerate(surfaces)
        }

    @staticmethod
    def _surface_data(
        data_types: list[SurfaceDataType],
        surfaces: list[int | str | object],
        surface_ids: list[int],
        surface_data: np.ndarray | list[np.ndarray],
        deprecated_flag: bool | None = False,
        flatten_connectivity: bool = False,
    ) -> dict[int | str, dict[SurfaceDataType, np.ndarray | list[np.ndarray]]]:
        surfaces = _get_surfaces_from_objects(surfaces)
        ret_surf_data = {}
        for count, surface in enumerate(surfaces):
            ret_surf_data[surface] = {}
            for data_type in data_types:
                if data_type == SurfaceDataType.FacesConnectivity:
                    if flatten_connectivity:
                        ret_surf_data[surface][data_type] = surface_data[
                            surface_ids[count]
                        ][SurfaceDataType.FacesConnectivity.value]
                    else:
                        from ansys.fluent.core.exceptions import (
                            PyFluentDeprecationWarning,
                        )

                        warnings.warn(
                            "Structured face connectivity output is deprecated and will be replaced by the flat format "
                            "in a future release. In the current release, pass 'flatten_connectivity=True' argument while creating the "
                            "'SurfaceFieldDataRequest' to request data in the flat format.",
                            PyFluentDeprecationWarning,
                        )
                        ret_surf_data[surface][data_type] = (
                            _transform_faces_connectivity_data(
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
        surfaces: list[int | str | object],
        surface_ids: list[int],
        vector_field_data: np.ndarray,
    ) -> dict[int | str, np.ndarray]:
        surfaces = _get_surfaces_from_objects(surfaces)
        return {
            surface: vector_field_data[surface_ids[count]][field_name].reshape(-1, 3)
            for count, surface in enumerate(surfaces)
        }

    @staticmethod
    def _pathlines_data(
        field_name: str,
        surfaces: list[int | str | object],
        surface_ids: list[int],
        pathlines_data: dict,
        deprecated_flag: bool | None = False,
        flatten_connectivity: bool = False,
    ) -> dict[int | str, dict[str, np.ndarray | list[np.ndarray]]]:
        surfaces = _get_surfaces_from_objects(surfaces)
        path_lines_dict = {}
        for count, surface in enumerate(surfaces):
            if flatten_connectivity:
                lines_data = pathlines_data[surface_ids[count]]["lines"]
            else:
                from ansys.fluent.core.exceptions import (
                    PyFluentDeprecationWarning,
                )

                warnings.warn(
                    "Structured face connectivity output is deprecated and will be replaced by the flat format "
                    "in a future release. In the current release, pass 'flatten_connectivity=True' argument while creating the "
                    "'PathlinesFieldDataRequest' to request data in the flat format.",
                    PyFluentDeprecationWarning,
                )
                lines_data = _transform_faces_connectivity_data(
                    pathlines_data[surface_ids[count]]["lines"]
                )
            temp_dict = {
                "vertices": pathlines_data[surface_ids[count]]["vertices"].reshape(
                    -1, 3
                ),
                "lines": lines_data,
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
