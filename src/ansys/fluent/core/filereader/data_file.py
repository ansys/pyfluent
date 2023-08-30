"""Reader for Fluent case files.

Example
-------

.. code-block:: python

    >>> from ansys.fluent.core import examples
    >>> from ansys.fluent.core.filereader.casereader import CaseReader

    >>> case_filepath = examples.download_file("Static_Mixer_Parameters.cas.h5", "pyfluent/static_mixer")

    >>> reader = CaseReader(case_filepath=case_filepath) # Instantiate a CaseFile class
    >>> input_parameters = reader.input_parameters()     # Get lists of input parameters
    >>> output_parameters = reader.output_parameters()   # Get lists of output parameters

"""
import os
from os.path import dirname
from pathlib import Path
import xml.etree.ElementTree as ET

import h5py
from lxml import etree
import numpy as np

from . import lispy


class DataFile:
    """Class to read a Fluent case file.

    Methods
    -------
    case_file
        Get the name of case file.
    get_face_variables
        Get the variables list available at face.
    get_phases
        Get the list of phases.
    get_cell_variables
        Get the variables list available at cell.
    get_face_scalar_field_data
        Get the scalar field data for face.
    get_face_vector_field_data
        Get the vector field data for face.
    """

    def __init__(
        self,
        data_filepath: str = None,
        project_filepath: str = None,
        case_file_handle=None,
    ):
        """__init__ method of CaseFile class."""
        self._case_file_handle = case_file_handle
        if data_filepath and project_filepath:
            raise RuntimeError(
                "Please enter either the data file path or the project file path"
            )
        if project_filepath:
            if Path(project_filepath).suffix in [".flprj", ".flprz"]:
                project_dir = os.path.join(
                    dirname(project_filepath),
                    Path(project_filepath).name.split(".")[0] + ".cffdb",
                )
                data_filepath = Path(
                    project_dir + _get_data_filepath_from_flprj(project_filepath)
                )
            else:
                raise FileNotFoundError(
                    "Please provide a valid fluent project file path"
                )

        try:
            if Path(data_filepath).match("*.dat.h5"):
                _file = h5py.File(data_filepath)
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
                f"The data file {data_filepath} cannot be found."
            ) from e

        except OSError as e:
            raise OSError(f"Error while reading data file {data_filepath}") from e

        except Exception as e:
            raise RuntimeError(f"Could not read data file {data_filepath}") from e

    @property
    def case_file(self) -> str:
        return self._settings["Case File"][0].decode()

    def variables(self) -> int:
        data_vars_str = self._settings["Data Variables"][0].decode()
        return {v[0]: v[1] for v in lispy.parse(data_vars_str)[1]}

    def get_phases(self):
        return list(self._field_data.keys())

    def get_face_variables(self, phase_name) -> int:
        return self._field_data[phase_name]["faces"]["fields"][0].decode().split(";")

    def get_cell_variables(self, phase_name) -> int:
        return self._field_data[phase_name]["cells"]["fields"][0].decode().split(";")

    def get_face_scalar_field_data(self, phase_name, field_name, surface_id) -> int:
        min_id, max_id = self._case_file_handle.get_mesh().get_surface_locs(surface_id)
        field_data = self._field_data[phase_name]["faces"][field_name]
        keys = list(field_data.keys())
        return field_data["1"][min_id : max_id + 1]

    def get_face_vector_field_data(self, phase_name, surface_id):
        x_comp = self.get_face_scalar_field_data(phase_name, "SV_U", surface_id)
        y_comp = self.get_face_scalar_field_data(phase_name, "SV_V", surface_id)
        z_comp = self.get_face_scalar_field_data(phase_name, "SV_W", surface_id)

        vector_data = np.array([])
        for a, b, c in zip(x_comp, y_comp, z_comp):
            vector_data = np.append(vector_data, [a, b, c])

        return vector_data


def _get_data_filepath_from_flprj(flprj_file):
    parser = etree.XMLParser(recover=True)
    tree = ET.parse(flprj_file, parser)
    root = tree.getroot()
    folder_name = root.find("Metadata").find("CurrentSimulation").get("value")[5:-1]
    return root.find(folder_name).find("Input").find("Case").find("Target").get("value")
