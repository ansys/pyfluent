"""Reader for Fluent case files.

Example
-------

from ansys.fluent.core.filereader.casereader import CaseReader

Instantiate a case reader

reader = CaseReader(case_filepath=case_filepath)

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
        self.name, self.value = None, None
        for k, v in raw_data:
            if k == "name":
                self.name = v
            elif k == "definition":
                self.value = v

    @property
    def units(self) -> str:
        """Get the unit label of a Fluent input parameter.
        Returns
        -------
        str
            Unit label of the Fluent input parameter.
        """
        return self._component(1).lstrip("[").rstrip("]")

    @property
    def number(self):
        """Get the value of a Fluent input parameter.
        Returns
        -------
        float
            Value of the Fluent input parameter.
        """
        return float(self._component(0))

    def _component(self, idx: int):
        try:
            return self.value.split(maxsplit=1)[idx]
        except IndexError:
            return ""


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


class _CaseVariable:
    def __init__(self, variables: dict, path: str = ""):
        self._variables = variables
        self._path = path

    def __call__(self, name: str = ""):
        if not name:
            error_name = self._path[:-1] if self._path else self._path
            raise RuntimeError(f"Invalid variable {error_name}")
        return self._variables[name]

    def __getattr__(self, name: str):
        for orig, sub in (
            ("__q", "?"),
            ("__dot", "."),
            ("__plus", "+"),
            ("_", "-"),
        ):
            name = name.replace(orig, sub)
        try:
            name = self._path + name
            result = self._variables[name]
            return lambda: result
        except KeyError:
            return _CaseVariable(self._variables, name + "/")


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

        self._rp_vars = {v[0]: v[1] for v in lispy.parse(rp_vars_str)[1]}

        self._config_vars = {v[0]: v[1] for v in self._rp_vars["case-config"]}

    def input_parameters(self) -> List[InputParameter]:
        exprs = self._named_expressions()
        if exprs:
            input_params = []
            for expr in exprs:
                for attr in expr:
                    if attr[0] in ["parameter", "input-parameter"] and attr[1] is True:
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

    def iter_count(self) -> int:
        return self._find_rp_var("number-of-iterations")

    def rp_vars(self) -> dict:
        return self._rp_vars

    @property
    def rp_var(self):
        return _CaseVariable(self._rp_vars)

    def has_rp_var(self, name):
        return name in self._rp_vars

    def config_vars(self):
        return self._config_vars

    @property
    def config_var(self):
        return _CaseVariable(self._config_vars)

    def has_config_var(self, name):
        return name in self._config_vars

    def _named_expressions(self):
        return self._find_rp_var("named-expressions")

    def _case_config(self):
        return self._find_rp_var("case-config")

    def _find_rp_var(self, name: str):
        return self._rp_vars[name]


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
