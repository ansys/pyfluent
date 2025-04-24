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

"""Reader for Fluent data files.

Example
-------

.. code-block:: python

    >>> from ansys.fluent.core import examples
    >>> from ansys.fluent.core.filereader.data_file import DataFile

    >>> data_file_name = examples.download_file("elbow1.dat.h5", "pyfluent/file_session", return_without_path=False)

    >>> reader = DataFile(data_file_name=data_file_name) # Instantiate a DataFile class
"""

import os
from os.path import dirname
from pathlib import Path

import defusedxml.ElementTree as ET
import numpy as np

from . import lispy
from .pre_processor import remove_unsupported_xml_chars

try:
    import h5py
except ModuleNotFoundError as exc:
    raise ModuleNotFoundError(
        "Missing dependencies, use 'pip install ansys-fluent-core[reader]' to install them."
    ) from exc


class DataFile:
    """Class to read a Fluent case file.

    Methods
    -------
    case_file()
        Get the name of case file.
    get_phases()
        Get the list of phases.
    get_face_variables(phase_name)
        Get the variables list available at face.
    get_cell_variables(phase_name)
        Get the variables list available at cell.
    get_face_scalar_field_data(phase_name, field_name, surface_id)
        Get the scalar field data for face.
    get_face_vector_field_data(phase_name, surface_id)
        Get the vector field data for face.
    """

    def __init__(
        self,
        data_file_name: str | None = None,
        project_file_name: str | None = None,
        case_file_handle=None,
    ):
        """__init__ method of CaseFile class."""
        self._case_file_handle = case_file_handle
        if data_file_name and project_file_name:
            raise RuntimeError(
                "Please enter either the data file path or the project file path"
            )
        if project_file_name:
            if Path(project_file_name).suffix in [".flprj", ".flprz"]:
                project_dir = os.path.join(
                    dirname(project_file_name),
                    Path(project_file_name).name.split(".")[0] + ".cffdb",
                )
                data_file_name = Path(
                    project_dir + _get_data_file_name_from_flprj(project_file_name)
                )
            else:
                raise FileNotFoundError(
                    "Please provide a valid fluent project file path"
                )

        try:
            if Path(data_file_name).match("*.dat.h5"):
                _file = h5py.File(data_file_name)
                results = _file["results"]
                self._settings = _file["settings"]
                self._field_data = results["1"]
                # self._residuals = results["residuals"]
                self._case_file = self._settings["Case File"][0]
            else:
                error_message = (
                    "Could not read case file. "
                    "Only valid data files (.h5, .cas, .cas.gz) can be read. "
                )
                raise RuntimeError(error_message)

        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"The data file {data_file_name} cannot be found."
            ) from e

        except OSError as e:
            raise OSError(f"Error while reading data file {data_file_name}") from e

        except Exception as e:
            raise RuntimeError(f"Could not read data file {data_file_name}") from e

    @property
    def case_file(self) -> str:
        """Returns the name of the associated case file in string format."""
        return self._settings["Case File"][0].decode()

    def variables(self) -> dict:
        """Returns all associated data variables in form of a dictionary."""
        data_vars_str = self._settings["Data Variables"][0].decode()
        return {v[0]: v[1] for v in lispy.parse(data_vars_str)[1]}

    def get_phases(self) -> list:
        """Returns list of phases available."""
        return list(self._field_data.keys())

    def get_face_variables(self, phase_name) -> list:
        """Extracts face variables available for a particular phase.

        Parameters
        ----------
        phase_name : str
            Name of the phase.

        Returns
        -------
            List of face variables.
        """
        return self._field_data[phase_name]["faces"]["fields"][0].decode().split(";")

    def get_cell_variables(self, phase_name) -> list:
        """Extracts cell variables available for a particular phase.

        Parameters
        ----------
        phase_name : str
            Name of the phase.

        Returns
        -------
            List of cell variables.
        """
        return self._field_data[phase_name]["cells"]["fields"][0].decode().split(";")

    def get_face_scalar_field_data(
        self, phase_name: str, field_name: str, surface_id: int
    ) -> np.array:
        """Gets scalar field data for face.

        Parameters
        ----------
        phase_name : str
            Name of the phase.

        field_name: str
            Name of the field

        surface_id : List[int]
            List of surface IDs for scalar field data.

        Returns
        -------
            Numpy array containing scalar field data for a particular phase, field and surface.
        """
        if ":" in field_name:
            field_name = field_name.split(":")[1]
        min_id, max_id = self._case_file_handle.get_mesh().get_surface_locs(surface_id)
        field_data = self._field_data[phase_name]["faces"][field_name]
        for field_array_name in field_data:
            field_array = field_data[field_array_name]
            array_min_id = int(field_array.attrs["minId"][0] - 1)
            array_max_id = int(field_array.attrs["maxId"][0] - 1)
            if min_id >= array_min_id and max_id <= array_max_id:
                return field_array[min_id - array_min_id : max_id + 1 - array_min_id]
        return np.zeros(max_id + 1 - min_id)

    def get_face_vector_field_data(self, phase_name: str, surface_id: int) -> np.array:
        """Gets vector field data for face.

        Parameters
        ----------
        phase_name : str
            Name of the phase.

        surface_id : List[int]
            List of surface IDs for vector field data.

        Returns
        -------
            Numpy array containing scalar field data for a particular phase, field and surface.
        """
        x_comp = self.get_face_scalar_field_data(phase_name, "SV_U", surface_id)
        y_comp = self.get_face_scalar_field_data(phase_name, "SV_V", surface_id)
        z_comp = self.get_face_scalar_field_data(phase_name, "SV_W", surface_id)

        vector_data = np.array([])
        for a, b, c in zip(x_comp, y_comp, z_comp):
            vector_data = np.append(vector_data, [a, b, c])

        return vector_data


def _get_data_file_name_from_flprj(flprj_file):
    with open(flprj_file, "r") as file:
        content = file.read()
        content = remove_unsupported_xml_chars(content)
        root = ET.fromstring(content)
        folder_name = root.find("Metadata").find("CurrentSimulation").get("value")[5:-1]
        return (
            root.find(folder_name)
            .find("Input")
            .find("Case")
            .find("Target")
            .get("value")
        )
