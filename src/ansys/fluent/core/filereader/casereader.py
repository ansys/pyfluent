"""Reader for Fluent case files.

Example
-------

from ansys.fluent.core.filereader.casereader import CaseReader

Instantiate a case reader

reader = CaseReader(hdf5_case_filepath=case_filepath)

Get lists of input and output parameters

input_parameters = reader.input_parameters()
output_parameters = reader.output_parameters()
"""

from pathlib import Path
from typing import List

import h5py

from . import lispy


class InputParameter:
    """Class to represent an input parameter.

    Attributes
    ----------
    name : str
    value
        The value of this input parameter, usually
        a string, qualified by units
    """

    def __init__(self, raw_data):
        self.name, self.name = None, None
        for k, v in raw_data:
            if k == "name":
                self.name = v
            elif k == "definition":
                self.value = v


class OutputParameter:
    """Class to represent an output parameter.

    Attributes
    ----------
    name : str
    """

    def __init__(self, raw_data):
        parameter = raw_data[1]
        for elem in parameter:
            if len(elem) and elem[0] == "name":
                self.name = elem[1][1]


class CaseReader:
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
    """

    def __init__(self, hdf5_case_filepath: str):
        try:
            file = h5py.File(hdf5_case_filepath)
        except FileNotFoundError:
            raise RuntimeError(f"The case file {hdf5_case_filepath} cannot be found.")
        except OSError:
            error_message = (
                "Could not read case file. " "Only valid HDF5 files can be read. "
            )
            if Path(hdf5_case_filepath).suffix != ".h5":
                error_message += (
                    f"The file {hdf5_case_filepath} does not have a .h5 extension."
                )
            raise RuntimeError(error_message)
        except BaseException:
            raise RuntimeError(f"Could not read case file {hdf5_case_filepath}")
        settings = file["settings"]
        rpvars = settings["Rampant Variables"][0]
        rp_vars_str = rpvars.decode()
        self._rp_vars = lispy.parse(rp_vars_str)[1]
        self._rp_var_cache = {}

    def input_parameters(self) -> List[InputParameter]:
        exprs = self._named_expressions()
        input_params = []
        for expr in exprs:
            for attr in expr:
                if attr[0] == "input-parameter" and attr[1] is True:
                    input_params.append(InputParameter(expr))
        return input_params

    def output_parameters(self) -> List[OutputParameter]:
        parameters = self._find_rp_var("parameters/output-parameters")
        return [OutputParameter(param) for param in parameters]

    def num_dimensions(self) -> int:
        for attr in self._case_config():
            if attr[0] == "rp-3d?":
                return 3 if attr[1] is True else 2

    def precision(self) -> int:
        for attr in self._case_config():
            if attr[0] == "rp-double?":
                return 2 if attr[1] is True else 1

    def _named_expressions(self):
        return self._find_rp_var("named-expressions")

    def _case_config(self):
        return self._find_rp_var("case-config")

    def _find_rp_var(self, name: str):
        try:
            return self._rp_var_cache[name]
        except KeyError:
            for var in self._rp_vars:
                if type(var) == list and len(var) and var[0] == name:
                    self._rp_var_cache[name] = var[1]
                    return var[1]
