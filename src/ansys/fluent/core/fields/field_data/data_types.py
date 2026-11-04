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

"""Public response models returned by Fluent field-data requests."""

import numpy as np
import numpy.typing as npt

from ansys.fluent.core.fields.field_data.requests import SurfaceDataType

__all__ = ("PathlinesData", "SurfaceData")


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
