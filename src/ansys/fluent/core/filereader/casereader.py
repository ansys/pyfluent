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
import codecs
import glob
import gzip
import itertools
from os.path import dirname
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
            if len(elem) and elem[0] == "fluent-units":
                self.units = elem[1].strip()


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

    def __init__(self, case_filepath: str = None, project_filepath: str = None):
        if case_filepath and project_filepath:
            raise RuntimeError(
                "Please enter either the case file path or the project file path"
            )
        if project_filepath:
            if Path(project_filepath).suffix in [".flprj", ".flprz"]:
                case_filepath = _get_case_filepath(dirname(project_filepath))
            else:
                raise RuntimeError("Please provide a valid fluent project file path")
        try:
            if "".join(Path(case_filepath).suffixes) == ".cas.h5":
                file = h5py.File(case_filepath)
                settings = file["settings"]
                rpvars = settings["Rampant Variables"][0]
                rp_vars_str = rpvars.decode()
            elif Path(case_filepath).suffix == ".cas":
                with open(case_filepath, "rb") as file:
                    rp_vars_str = file.read()
                rp_vars_str = _get_processed_string(rp_vars_str)
            elif "".join(Path(case_filepath).suffixes) == ".cas.gz":
                with gzip.open(case_filepath, "rb") as file:
                    rp_vars_str = file.read()
                rp_vars_str = _get_processed_string(rp_vars_str)
            else:
                raise RuntimeError()

        except FileNotFoundError:
            raise RuntimeError(f"The case file {case_filepath} cannot be found.")

        except OSError:
            error_message = (
                "Could not read case file. "
                "Only valid Case files (.h5, .cas, .cas.gz) can be read. "
            )
            raise RuntimeError(error_message)

        except BaseException:
            raise RuntimeError(f"Could not read case file {case_filepath}")

        self._rp_vars = lispy.parse(rp_vars_str)[1]
        self._rp_var_cache = {}

    def input_parameters(self) -> List[InputParameter]:
        exprs = self._named_expressions()
        if exprs:
            input_params = []
            for expr in exprs:
                for attr in expr:
                    if attr[0] == "input-parameter" and attr[1] is True:
                        input_params.append(InputParameter(expr))
            return input_params
        else:
            parameters = self._find_rp_var("parameters/input-parameters")
            return [InputParameter(param) for param in parameters]

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


def _get_processed_string(input_string: bytes) -> str:
    """Processes the input string (binary) with help of an identifier to return
    it in a format which can be parsed by lispy.parse()

    Parameters
    ----------
    input_string : bytes
        The input string in bytes

    Returns
    -------
    processed string (str)
    """
    rp_vars_str = codecs.decode(input_string, errors="ignore")
    string_identifier = "(37 ("
    return string_identifier + rp_vars_str.split(string_identifier)[1]


def _get_case_filepath(project_dir_path: str) -> str:
    """Gets case file path within the provided project directory path.

    Parameters
    ----------
    project_dir_path : str
        The directory containing the case file

    Returns
    -------
    case file path (str)
    """
    file_list = list(
        itertools.chain(
            *(
                glob.glob(project_dir_path + r"/**/**-Solve/*.%s" % ext)
                for ext in ["cas", "cas.h5", "cas.gz"]
            )
        )
    )
    if len(file_list) < 1:
        raise RuntimeError(f"No case files are present in: {project_dir_path}")
    elif len(file_list) > 1:
        raise RuntimeError(f"More than one case file is present in: {project_dir_path}")
    else:
        return file_list[0]
