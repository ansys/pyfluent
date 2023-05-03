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
                self.name = v.strip('"')
            elif k == "definition":
                self.value = v.strip('"')
                if "[" in self.value:
                    sep_index = self.value.index("[")
                    if not self.value[sep_index - 1] == " ":
                        self.value = "".join(
                            (self.value[:sep_index], " ", self.value[sep_index:])
                        )

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
    def numeric_value(self):
        """Get the numeric value of a Fluent input parameter.
        Returns
        -------
        float
            Numeric value of the Fluent input parameter.
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
                self.name = elem[1][1].strip('"')
            if len(elem) and elem[0] == "fluent-units":
                self.units = elem[1].strip('"').strip()


class _CaseVariable:
    def __init__(self, variables: dict, path: str = ""):
        self._variables = variables
        self._path = path

    def __call__(self, name: str = ""):
        if not name:
            error_name = self._path[:-1] if self._path else self._path
            raise RuntimeError(f"Invalid variable {error_name}")
        try:
            return self._variables[name]
        except KeyError:
            raise ValueError(
                allowed_name_error_message(
                    "config-vars", name, list(self._variables.keys())
                )
            )

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


class CaseFile:
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
                project_dir = os.path.join(
                    dirname(project_filepath),
                    Path(project_filepath).name.split(".")[0] + ".cffdb",
                )
                case_filepath = Path(
                    project_dir + _get_case_filepath_from_flprj(project_filepath)
                )
            else:
                raise FileNotFoundError(
                    "Please provide a valid fluent project file path"
                )

        try:
            if Path(case_filepath).match("*.cas.h5"):
                file = h5py.File(case_filepath)
                settings = file["settings"]
                rpvars = settings["Rampant Variables"][0]
                rp_vars_str = rpvars.decode()
            elif Path(case_filepath).match("*.cas"):
                with open(case_filepath, "rb") as file:
                    rp_vars_str = file.read()
                rp_vars_str = _get_processed_string(rp_vars_str)
            elif Path(case_filepath).match("*.cas.gz"):
                with gzip.open(case_filepath, "rb") as file:
                    rp_vars_str = file.read()
                rp_vars_str = _get_processed_string(rp_vars_str)
            else:
                error_message = (
                    "Could not read case file. "
                    "Only valid Case files (.h5, .cas, .cas.gz) can be read. "
                )
                raise RuntimeError(error_message)

        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"The case file {case_filepath} cannot be found."
            ) from e

        except OSError as e:
            raise OSError(f"Error while reading case file {case_filepath}") from e

        except BaseException as e:
            raise RuntimeError(f"Could not read case file {case_filepath}") from e

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


def _get_case_filepath_from_flprj(flprj_file):
    parser = etree.XMLParser(recover=True)
    tree = ET.parse(flprj_file, parser)
    root = tree.getroot()
    folder_name = root.find("Metadata").find("CurrentSimulation").get("value")[5:-1]
    return root.find(folder_name).find("Input").find("Case").find("Target").get("value")
