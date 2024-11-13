"""Module containing System Coupling-related functionality."""

from dataclasses import dataclass
import os
from typing import List
import xml.etree.ElementTree as XmlET

import ansys.fluent.core as pyfluent
from ansys.fluent.core.utils.fluent_version import FluentVersion


@dataclass
class Variable:
    """Provides variable data."""

    name: str
    display_name: str
    tensor_type: str
    is_extensive: bool
    location: str
    quantity_type: str


@dataclass
class Region:
    """Provides region data."""

    name: str
    display_name: str
    topology: str
    input_variables: List[str]
    output_variables: List[str]


class SystemCoupling:
    """Wrap a System Coupling object, adding methods to discover more about the System
    Coupling related setup and to help solving a System Coupling analysis.

    Methods
    -------
    get_variables()
        Get variables
    get_regions()
        Get regions
    get_analysis_type()
        Get analysis type
    connect()
        Connect parallelly
    solve()
        Initialize and solve
    """

    def __init__(self, solver):
        """Initialize SystemCoupling."""
        self._solver = solver
        # version check - this requires Fluent 2024 R1 or newer.
        if self._solver.get_fluent_version() < FluentVersion.v241:
            raise RuntimeError(
                f"Using {str(self._solver.get_fluent_version())}. PySystemCoupling integration requires {str(FluentVersion.v241)} or later."
            )
        if self._solver.get_fluent_version() >= FluentVersion.v251:
            # enable feature to be able to make System Coupling settings APIs calls
            self._solver.scheme_eval.scheme_eval(
                "(enable-feature 'sc/participant-info)"
            )

    @property
    def participant_type(self) -> str:
        """Get participant type."""
        return "FLUENT"

    def get_variables(self) -> List[Variable]:
        """Get variables."""

        if self._solver.get_fluent_version() >= FluentVersion.v251:
            variables = list()
            region_names = (
                self._solver.settings.setup.models.system_coupling.get_all_regions()
            )
            variable_names = set()
            for region_name in region_names:
                in_var_names = self._get_list(
                    self._solver.settings.setup.models.system_coupling.get_input_vars(
                        region_name=region_name
                    )
                )
                out_var_names = self._get_list(
                    self._solver.settings.setup.models.system_coupling.get_output_vars(
                        region_name=region_name
                    )
                )
                variable_names.update(in_var_names)
                variable_names.update(out_var_names)
            variable_names = sorted(list(variable_names))
            for variable_name in variable_names:
                variables.append(
                    Variable(
                        name=variable_name,
                        display_name=self._get_display_name(variable_name),
                        tensor_type=self._solver.settings.setup.models.system_coupling.get_tensor_type(
                            variable_name=variable_name
                        ),
                        is_extensive=self._solver.settings.setup.models.system_coupling.is_extensive_var(
                            variable_name=variable_name
                        ),
                        location=self._solver.settings.setup.models.system_coupling.get_data_location(
                            variable_name=variable_name
                        ),
                        quantity_type=self._get_quantity_type(variable_name),
                    )
                )
            return variables
        else:
            # maintains back-compatibility for 24.1 and 24.2
            return self.__get_syc_setup()["variables"]

    def get_regions(self) -> List[Region]:
        """Get regions."""

        if self._solver.get_fluent_version() >= FluentVersion.v251:
            region_names = (
                self._solver.settings.setup.models.system_coupling.get_all_regions()
            )
            regions = list()
            for region_name in region_names:
                regions.append(
                    Region(
                        name=region_name,
                        display_name=self._get_display_name(region_name),
                        topology=self._solver.settings.setup.models.system_coupling.get_topology(
                            region_name=region_name
                        ),
                        input_variables=self._get_list(
                            self._solver.settings.setup.models.system_coupling.get_input_vars(
                                region_name=region_name
                            )
                        ),
                        output_variables=self._get_list(
                            self._solver.settings.setup.models.system_coupling.get_output_vars(
                                region_name=region_name
                            )
                        ),
                    )
                )
            return regions
        else:
            # maintains back-compatibility for 24.1 and 24.2
            return self.__get_syc_setup()["regions"]

    def get_analysis_type(self) -> str:
        """Get analysis type."""
        if self._solver.get_fluent_version() >= FluentVersion.v251:
            return (
                self._solver.settings.setup.models.system_coupling.get_analysis_type()
            )
        else:
            # maintains back-compatibility for 24.1 and 24.2
            return self.__get_syc_setup()["analysis-type"]

    def connect(self, host: str, port: int, name: str) -> None:
        """Connect to System Coupling."""
        self._solver.settings.setup.models.system_coupling.connect_parallel(
            schost=host, scport=port, scname=name
        )

    def solve(self) -> None:
        """Initialize and solve."""
        self._solver.settings.setup.models.system_coupling.init_and_solve()

    @staticmethod
    def _get_quantity_type(variable_name: str) -> str:
        """
        For some variables, System Coupling should know the quantity type.
        """
        if variable_name in {"force", "lorentz-force"}:
            return "Force"
        elif variable_name in {"heatflow", "heatrate"}:
            return "Heat Rate"
        elif variable_name == "displacement":
            return "Incremental Displacement"
        elif variable_name == "temperature":
            return "Temperature"
        elif variable_name == "heat-transfer-coefficient":
            return "Heat Transfer Coefficient"
        elif variable_name == "near-wall-temperature":
            return "Convection Reference Temperature"
        elif variable_name == "electrical-conductivity":
            return "Electrical Conductivity"
        else:
            return "Unspecified"

    @staticmethod
    def _get_display_name(internal_name: str) -> str:
        """
        Display names should not contain dashes.
        """
        return internal_name.replace("-", " ")

    @staticmethod
    def _get_list(value: list | None) -> list:
        if isinstance(value, list):
            return value
        elif value is None:
            return list()
        raise TypeError(f"_get_list unexpected type of {value}")

    def __get_syc_setup(self) -> dict:
        """
        This function is for backward-compatibility reasons for 24.1 and 24.2 versions.
        It tells Fluent to write the SCP file and then parses it to get the setup
        information. The SCP file is then deleted.
        With newer versions, settings APIs can be used directly, without having
        to write the SCP file at all.
        """

        def get_scp_string() -> str:
            """Get the SCP file contents in the form of an XML string."""

            scp_file_name = "fluent.scp"
            self._solver.settings.setup.models.system_coupling.write_scp_file(
                file_name=scp_file_name
            )

            if self._solver._fluent_connection._remote_instance is not None:
                # download the file locally in case Fluent is remote
                # assume file transfer service is configured - download the file
                self._solver.download(scp_file_name)
            elif self._solver.connection_properties.inside_container:
                # Right now, the way that PyFluent containers and tests are set up,
                # the local Fluent container working directory will correspond to
                # pyfluent.EXAMPLES_PATH in the host, so that is where the SCP file
                # will be written.
                examples_path_scp = os.path.join(pyfluent.EXAMPLES_PATH, scp_file_name)
                if os.path.exists(examples_path_scp):
                    scp_file_name = examples_path_scp

            assert os.path.exists(
                scp_file_name
            ), f"ERROR: could not create System Coupling SCP file: {scp_file_name}"

            with open(scp_file_name, "r") as f:
                xml_string = f.read()

            os.remove(scp_file_name)
            return xml_string

        def get_name(xml_element) -> str:
            return xml_element.find("Name").text

        def get_display_name(xml_element) -> str:
            display_name_elem = xml_element.find("DisplayName")
            if display_name_elem is not None:
                return display_name_elem.text
            else:
                return get_name(xml_element)

        def get_tensor_type(variable) -> str:
            tensor_type_elem = variable.find("TensorType")
            if tensor_type_elem is not None:
                return tensor_type_elem.text

            if get_name(variable) in {"displacement", "force", "lorentz-force"}:
                return "Vector"
            else:
                return "Scalar"

        def get_is_extensive(variable) -> bool:
            is_extensive_elem = variable.find("IsExtensive")
            if is_extensive_elem is not None:
                is_ext_map = {"True": True, "False": False}
                return is_ext_map[is_extensive_elem.text]

            ext_vars = {
                "force",
                "lorentz-force",
                "heatrate",
                "heatflow",
                "mass-flow-rate",
            }
            if get_name(variable) in ext_vars:
                return True
            else:
                return False

        def get_location(variable) -> str:
            # SCP file contents for location are not always correct,
            # so do not rely on that.
            # This has to do with old vs. new APIs. Here, assume
            # only new APIs are used, so all variables are on elements,
            # except displacements.
            if get_name(variable) == "displacement":
                return "Node"
            else:
                return "Element"

        def get_quantity_type(variable) -> str:
            quantity_type_elem = variable.find("QuantityType")
            if quantity_type_elem is not None:
                return quantity_type_elem.text
            else:
                return "Unspecified"

        setup_info = dict()

        xml_root = XmlET.ElementTree(XmlET.fromstring(get_scp_string()))
        cosim_control = xml_root.find("./CosimulationControl")

        setup_info["analysis-type"] = cosim_control.find("AnalysisType").text

        setup_info["variables"] = list()
        for variable in cosim_control.find("Variables").findall("Variable"):
            setup_info["variables"].append(
                Variable(
                    name=get_name(variable),
                    display_name=get_display_name(variable),
                    tensor_type=get_tensor_type(variable),
                    is_extensive=get_is_extensive(variable),
                    location=get_location(variable),
                    quantity_type=get_quantity_type(variable),
                )
            )

        regions = cosim_control.find("Regions").findall("Region")
        setup_info["regions"] = [
            Region(
                name=get_name(region),
                display_name=get_display_name(region),
                topology=region.find("Topology").text,
                input_variables=[var.text for var in region.find("InputVariables")],
                output_variables=[var.text for var in region.find("OutputVariables")],
            )
            for region in regions
        ]

        return setup_info
