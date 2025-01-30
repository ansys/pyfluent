"""Reader for Fluent case files.

Example
-------

.. code-block:: python

    >>> from ansys.fluent.core import examples
    >>> from ansys.fluent.core.filereader.case_file import CaseFile

    >>> case_file_name = examples.download_file("Static_Mixer_Parameters.cas.h5", "pyfluent/static_mixer", return_without_path=False)

    >>> reader = CaseFile(case_file_name=case_file_name) # Instantiate a CaseFile class
    >>> input_parameters = reader.input_parameters()     # Get lists of input parameters
    >>> output_parameters = reader.output_parameters()   # Get lists of output parameters
"""

import codecs
from enum import Enum
import gzip
import os
from os.path import dirname
from pathlib import Path
from typing import Dict, List
import xml.etree.ElementTree as ET

from lxml import etree
import numpy as np

from ansys.fluent.core.solver.error_message import allowed_name_error_message

from . import lispy

try:
    import h5py
except ModuleNotFoundError as exc:
    raise ModuleNotFoundError(
        "Missing dependencies, use 'pip install ansys-fluent-core[reader]' to install them."
    ) from exc


class InputParameterOld:
    """Represents an input parameter (old format).

    Attributes
    ----------
    name : str
    value
        The value of this input parameter, usually
        a string, qualified by units
    """

    def __init__(self, raw_data: List) -> None:
        """Initialize InputParameter.

        Parameters
        ----------
        raw_data : List
            Input parameter data as a list.
        """
        self.name = raw_data[1][1][1][1].strip('"')
        self.value = raw_data[1][2]

    @property
    def units(self) -> str:
        """Get the unit label of a Fluent input parameter.

        Returns
        -------
        str
            Unit label of the Fluent input parameter.
        """
        return str(self.value[-1][-1])

    @property
    def numeric_value(self) -> float:
        """Get the numeric value of a Fluent input parameter.

        Returns
        -------
        float
            Numeric value of the Fluent input parameter.
        """
        return float(self.value[2][1])


class InputParameter:
    """Represents an input parameter.

    Attributes
    ----------
    name : str
    value
        The value of this input parameter, usually
        a string, qualified by units
    """

    def __init__(self, raw_data: Dict[str, str]) -> None:
        """Initialize InputParameter.

        Parameters
        ----------
        raw_data : Dict[str, str]
            Input parameter data as a nested dictionary.
        """
        self.name, self.value = None, None
        for k, v in raw_data:
            if k == "name":
                self.name = v.strip('"')
            elif k == "definition":
                self.value = v.strip('"')
                if "[" in self.value:
                    sep_index = self.value.index("[")
                    if self.value[sep_index - 1] != " ":
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
    def numeric_value(self) -> float:
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
    """Represents an output parameter.

    Attributes
    ----------
    name : str
    """

    def __init__(self, raw_data: list) -> None:
        """Initialize OutputParameter.

        Parameters
        ----------
        raw_data : list
            Output parameter as a nested list.
        """
        parameter = raw_data[1]
        for elem in parameter:
            if len(elem) and elem[0] == "name":
                self.name = elem[1][1].strip('"')
            if len(elem) and elem[0] == "fluent-units":
                self.units = elem[1].strip('"').strip()


class CaseVariable:
    """Provides access to variables defined in the case."""

    def __init__(self, variables: dict, path: str | None = ""):
        """Initialize CaseVariable.

        Parameters
        ----------
        variables : dict
            The variables dictionary.
        path : str
            The path to the variables.
        """
        self._variables = variables
        self._path = path

    def __call__(self, name: str | None = ""):
        if not name:
            error_name = self._path[:-1] if self._path else self._path
            raise RuntimeError(f"Invalid variable {error_name}")
        try:
            return self._variables[name]
        except KeyError:
            raise ValueError(
                allowed_name_error_message(
                    context="config-vars",
                    trial_name=name,
                    allowed_values=list(self._variables),
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
            return CaseVariable(self._variables, name + "/")


class MeshType(Enum):
    """Types of Mesh."""

    SURFACE = "surface"
    VOLUME = "volume"
    UNKNOWN = "unknown"


class Mesh:
    """Class to provide data from and information about Fluent mesh files.

    This class is applicable only to HDF5, Fluent's default format for mesh files.
    HDF5 (Hierarchical Data Format version 5) is commonly used for storing large amounts
    of scientific data, including Fluent mesh data.

    Methods
    -------

    get_surface_ids()
        Get a list of surface ids.
    get_surface_names()
        Get a list of surface names.
    get_surface_locs(surface_id)
        Get the min and max location index of surface.
    get_connectivity(surface_id)
        Get the surface connectivity.
    get_vertices(surface_id)
        Get list of vertices of the surface.
    """

    def __init__(self, file_handle):
        """Initialize the object."""
        self._file_handle = file_handle

    def get_mesh_type(self) -> MeshType:
        """Returns the type of the mesh."""
        try:
            if "cells" in self._file_handle["meshes"]["1"].keys():
                return MeshType.VOLUME
            else:
                return MeshType.SURFACE
        except Exception:
            return MeshType.UNKNOWN

    def get_surface_ids(self) -> list:
        """Returns list of ids of all available surfaces."""
        id_data = self._file_handle["meshes"]["1"]["faces"]["zoneTopology"]["id"]
        return [id_data[i] for i in range(id_data.size)]

    def get_surface_names(self) -> list:
        """Returns list of names of all available surfaces."""
        return (
            self._file_handle["meshes"]["1"]["faces"]["zoneTopology"]["name"][0]
            .decode()
            .split(";")
        )

    def get_surface_locs(self, surface_id) -> list:
        """Returns range of surface locations for a particular surface."""
        ids = self.get_surface_ids()
        index = ids.index(surface_id)
        min_id = self._file_handle["meshes"]["1"]["faces"]["zoneTopology"]["minId"][
            index
        ]
        max_id = self._file_handle["meshes"]["1"]["faces"]["zoneTopology"]["maxId"][
            index
        ]
        return [int(min_id - 1), int(max_id - 1)]

    def _get_nodes(self, surface_id):
        min_id, max_id = self.get_surface_locs(surface_id)
        nnodes = self._file_handle["meshes"]["1"]["faces"]["nodes"]["1"]["nnodes"]
        nodes = self._file_handle["meshes"]["1"]["faces"]["nodes"]["1"]["nodes"]
        previous = sum(nnodes[0:min_id])
        nnodes = nnodes[min_id : max_id + 1]
        nodes = nodes[previous : previous + sum(nnodes)]
        return [nodes, nnodes]

    def get_connectivity(self, surface_id) -> np.array:
        """Returns numpy array of face connectivity data for a particular surface."""
        nodes, nnodes = self._get_nodes(surface_id)
        key = nodes.copy()
        key.sort()
        key = np.unique(key)
        value = np.arange(0, len(key))
        replace = np.array([key, value])
        mask = np.in1d(nodes, key)
        nodes[mask] = replace[1, np.searchsorted(replace[0, :], nodes[mask])]
        obj = np.cumsum(nnodes)
        obj = np.insert(obj, 0, 0)
        obj = np.delete(obj, len(obj) - 1)
        nodes = np.insert(nodes, obj, nnodes)
        return nodes

    def get_vertices(self, surface_id) -> np.array:
        """Returns numpy array of vertices data for a particular surface."""
        nodes, nnodes = self._get_nodes(surface_id)
        nodes = np.unique(nodes)
        nodes = np.sort(nodes)
        nodes -= 1
        vertices_dict = self._file_handle["meshes"]["1"]["nodes"]["coords"]
        vertices = vertices_dict[str(list(vertices_dict.keys())[0])]
        return vertices[:][nodes].flatten()


class RPVarProcessor:
    """Class to process RP Vars string to expose required outputs.

    Methods
    -------
    input_parameters()
        Get a list of input parameter objects
    output_parameters()
        Get a list of output parameter objects
    num_dimensions()
        Get the dimensionality of the case (2 or 3)
    precision()
        Get the precision (1 or 2 for 1D of 2D)
    iter_count()
        Get the number of iterations
    rp_vars()
        Get dictionary of all RP vars
    rp_var(name)
        Get specific RP var by name, either by providing
        the Scheme name:
            `reader.rp_var("rad/enable-netm?")`
        or a pythonic version:
            `reader.rp_var.rad.enable_netm__q()`
    has_rp_var(name)
        Whether case has particular RP var
    config_vars()
        Get dictionary of all RP vars
    config_var(name)
        Get specific config var by name, either by providing
        the Scheme name:
            `reader.config_var("rp-3d?")`
        or a pythonic version:
            `reader.config_var.rp_3d__q()`
    has_config_var(name)
        Whether case has particular config var
    """

    def __init__(
        self,
        rp_vars_str: str,
    ) -> None:
        """Initialize a RPVarProcessor object.

        Parameters
        ----------
        rp_vars_str :str
            RP Vars string.
        """

        self.rp_vars_str = rp_vars_str

        self._rp_vars = {v[0]: v[1] for v in lispy.parse(rp_vars_str)[1]}

        self._config_vars = {v[0]: v[1] for v in self._rp_vars["case-config"]}

    def input_parameters(self) -> List[InputParameter] | List[InputParameterOld]:
        """Get the input parameters.

        Returns
        -------
        List[InputParameter] | List[InputParameterOld]
            The list of input parameters.
        """
        exprs = self._named_expressions()
        if exprs:
            input_params = []
            for expr in exprs:
                for attr in expr:
                    if attr[0] in ["parameter", "input-parameter"] and attr[1] is True:
                        input_params.append(InputParameter(expr))
            return input_params

        rp_var_params = self._find_rp_var("parameters/input-parameters") or []
        try:
            return [InputParameter(param) for param in rp_var_params]
        except ValueError:
            return [InputParameterOld(param) for param in rp_var_params]

    def output_parameters(self) -> List[OutputParameter]:
        """Get the output parameters.

        Returns
        -------
        List[OutputParameter]
            The list of output parameters.
        """
        parameters = self._find_rp_var("parameters/output-parameters")
        return [OutputParameter(param) for param in parameters]

    def num_dimensions(self) -> int:
        """Get the dimensionality associated with this case.

        Returns
        -------
        int
            The number of dimensions.
        """
        for attr in self._case_config():
            if attr[0] == "rp-3d?":
                return 3 if attr[1] is True else 2

    def precision(self) -> int:
        """Get the precision associated with this case (single or double).

        Returns
        -------
        int
            Either 1 or 2 to indicate single or double precision respectively.
        """
        for attr in self._case_config():
            if attr[0] == "rp-double?":
                return 2 if attr[1] is True else 1

    def iter_count(self) -> int:
        """Get the number of iterations associated with this case.

        Returns
        -------
        int
            The number of iterations associated with this case.
        """
        return self._find_rp_var("number-of-iterations")

    def rp_vars(self) -> dict:
        """Get the rpvars associated with this case.

        Returns
        -------
        dict
            The rpvars associated with this case.
        """
        return self._rp_vars

    @property
    def rp_var(self) -> CaseVariable:
        """Access the rpvars associated with this case.

        Returns
        -------
        CaseVariable
            The rpvars associated with this case.
        """
        return CaseVariable(self._rp_vars)

    def has_rp_var(self, name: str) -> bool:
        """Find if this case has the given rpvar.

        Parameters
        ----------
        name : str
            Name of the rpvar.

        Returns
        -------
        bool
            Whether this case has the given rpvar.
        """
        return name in self._rp_vars

    def config_vars(self) -> dict:
        """Get the config variables associated with this case.

        Returns
        -------
        dict
            The config variables associated with this case.
        """
        return self._config_vars

    @property
    def config_var(self) -> CaseVariable:
        """Access the config variables associated with this case.

        Returns
        -------
        CaseVariable
            The config variables associated with this case.
        """
        return CaseVariable(self._config_vars)

    def has_config_var(self, name):
        """Get whether the case has a given variable."""
        return name in self._config_vars

    def _named_expressions(self):
        return self._find_rp_var("named-expressions")

    def _case_config(self):
        return self._find_rp_var("case-config")

    def _find_rp_var(self, name: str):
        return self._rp_vars.get(name)


class SettingsFile(RPVarProcessor):
    """Class to read a Fluent Settings file."""

    def __init__(self, settings_file_name: str | None = None) -> None:
        """Initialize a SettingsFile object. Exactly one file path argument must be
        specified.

        Parameters
        ----------
        settings_file_name : str
            The path of a settings file.
        """
        if settings_file_name:
            try:
                with open(settings_file_name, "r") as file:
                    rp_vars_str = file.read()
                if not rp_vars_str.startswith("(rp ("):
                    raise RuntimeError("Not a valid settings file.")

            except FileNotFoundError as e:
                raise FileNotFoundError(
                    f"The settings file {settings_file_name} cannot be found."
                ) from e

            except OSError as e:
                raise OSError(
                    f"Error while reading settings file {settings_file_name}"
                ) from e

            except Exception as e:
                raise RuntimeError(
                    f"Could not read settings file {settings_file_name}"
                ) from e

        super().__init__(rp_vars_str)


class EmptyContainer:
    """Empty Container."""

    def __getattr__(self, item):
        return lambda *args, **kwargs: None

    def __call__(self, *args, **kwargs):
        return None


class CaseFile(RPVarProcessor):
    """Class to read a Fluent case file.

    Methods
    -------
    get_mesh()
        Get the mesh data.
    """

    def __init__(
        self,
        case_file_name: str | None = None,
        project_file_name: str | None = None,
    ) -> None:
        """Initialize a CaseFile object. Exactly one file path argument must be
        specified.

        Parameters
        ----------
        case_file_name : str
            The path of a case file.
        project_file_name : str
            The path of a project file from which the case file is selected.
        """
        self._is_case_file = False

        if (not case_file_name) == (not project_file_name):
            raise RuntimeError(
                "Please enter either the case file path or the project file path"
            )
        if project_file_name:
            if Path(project_file_name).suffix in [".flprj", ".flprz"]:
                project_dir = os.path.join(
                    dirname(project_file_name),
                    Path(project_file_name).name.split(".")[0] + ".cffdb",
                )
                case_file_name = Path(
                    project_dir + _get_case_file_name_from_flprj(project_file_name)
                )
            else:
                raise FileNotFoundError(
                    "Please provide a valid fluent project file path"
                )

        try:
            if Path(case_file_name).match("*.cas.h5") or Path(case_file_name).match(
                "*.msh.h5"
            ):
                _file = h5py.File(case_file_name)
                if Path(case_file_name).match("*.cas.h5"):
                    self._is_case_file = True
                    settings = _file["settings"]
                    rpvars = settings["Rampant Variables"][0]
                    rp_vars_str = rpvars.decode()
            elif Path(case_file_name).match("*.cas") or Path(case_file_name).match(
                "*.msh"
            ):
                with open(case_file_name, "rb") as _file:
                    rp_vars_str = _file.read()
                if Path(case_file_name).match("*.cas"):
                    self._is_case_file = True
                    rp_vars_str = _get_processed_string(rp_vars_str)
            elif Path(case_file_name).match("*.cas.gz") or Path(case_file_name).match(
                "*.msh.gz"
            ):
                with gzip.open(case_file_name, "rb") as _file:
                    rp_vars_str = _file.read()
                if Path(case_file_name).match("*.cas.gz"):
                    self._is_case_file = True
                    rp_vars_str = _get_processed_string(rp_vars_str)
            else:
                error_message = (
                    "Could not read case file. "
                    "Only valid Case files (.h5, .cas, .cas.gz) or Mesh files (.msh.h5, .msh, .msh.gz) can be read. "
                )
                raise RuntimeError(error_message)

        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"The case file {case_file_name} cannot be found."
            ) from e

        except OSError as e:
            raise OSError(f"Error while reading case file {case_file_name}") from e

        except Exception as e:
            raise RuntimeError(f"Could not read case file {case_file_name}") from e

        if self._is_case_file:
            super().__init__(rp_vars_str=rp_vars_str)
        self._mesh = Mesh(_file)

    def get_mesh(self):
        """Get the mesh data."""
        return self._mesh

    def __getattribute__(self, item):
        if (
            item != "_is_case_file"
            and not self._is_case_file
            and item
            in set(filter(lambda k: not k.startswith("__"), dir(RPVarProcessor)))
        ):
            return EmptyContainer()
        return super().__getattribute__(item)


def _get_processed_string(input_string: bytes) -> str:
    """Processes the input string (binary) with help of an identifier to return it in a
    format which can be parsed by lispy.parse().

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


def _get_case_file_name_from_flprj(flprj_file):
    parser = etree.XMLParser(recover=True)
    tree = ET.parse(flprj_file, parser)
    root = tree.getroot()
    folder_name = root.find("Metadata").find("CurrentSimulation").get("value")[5:-1]
    # If the project file name begins with a digit then the node to find will be prepended
    # with "_". Rather than making any assumptions that this is a hard rule, or what
    # the scope of the rule is, simply retry with the name prepended:
    folder_obj = (
        root.find(folder_name)
        if root.find(folder_name) and len(root.find(folder_name)) > 0
        else root.find("_" + folder_name)
    )
    return folder_obj.find("Input").find("Case").find("Target").get("value")
