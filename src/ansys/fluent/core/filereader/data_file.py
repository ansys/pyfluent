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
import codecs
import gzip
import os
from os.path import dirname
from pathlib import Path
from typing import List
import xml.etree.ElementTree as ET

import h5py
from lxml import etree

from ansys.fluent.core.solver.error_message import allowed_name_error_message

from . import lispy

class DataFile:
    """Class to read a Fluent case file.

    Methods
    -------
    input_parameters
        Get a list of input parameter objects
    output_parameters
        Get a list of output parameter objects
    num_dimensions
        Get the dimensionality of the case (2 or 3)
    precision
        Get the precision (1 or 2 for 1D of 2D)
    iter_count
        Get the number of iterations
    rp_vars
        Get dictionary of all RP vars
    rp_var
        Get specific RP var by name, either by providing
        the Scheme name:
            `reader.rp_var("rad/enable-netm?")`
        or a pythonic version:
            `reader.rp_var.rad.enable_netm__q()`
    has_rp_var
        Whether case has particular RP var
    config_vars
        Get dictionary of all RP vars
    config_var
        Get specific config var by name, either by providing
        the Scheme name:
            `reader.config_var("rp-3d?")`
        or a pythonic version:
            `reader.config_var.rp_3d__q()`
    has_config_var
        Whether case has particular config var
    """

    def __init__(self, data_filepath: str = None, project_filepath: str = None, case_file_handle = None):
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
                    project_dir + _get_case_filepath_from_flprj(project_filepath)
                )
            else:
                raise FileNotFoundError(
                    "Please provide a valid fluent project file path"
                )

        try:
            if Path(data_filepath).match("*.dat.h5"):
                file = h5py.File(data_filepath)
                results = file["results"]
                self._settings = file["settings"]
                self._field_data = results["1"]
                #self._residuals = results["residuals"]
                self._case_file =   self._settings["Case File"][0]               
            else:
                error_message = (
                    "Could not read case file. "
                    "Only valid Case files (.h5, .cas, .cas.gz) can be read. "
                )
                raise RuntimeError(error_message)

        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"The case file {data_filepath} cannot be found."
            ) from e

        except OSError as e:
            raise OSError(f"Error while reading case file {data_filepath}") from e

        except BaseException as e:
            raise RuntimeError(f"Could not read case file {data_filepath}") from e

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

    def get_face_data(self, phase_name, field_name, surface_id) -> int:
        min_id, max_id = self._case_file_handle.get_mesh().get_surface_locs(surface_id)
        field_data = self._field_data[phase_name]["faces"][field_name] 
        keys = list(field_data.keys())   
        print('length is', len(field_data["1"]))        
        return field_data["1"][min_id: max_id +1]          