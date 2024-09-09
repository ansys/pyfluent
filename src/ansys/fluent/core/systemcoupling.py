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
    __getattr__
    get_variables
    get_regions
    get_analysis_type
    connect
    solve
    """

    def __init__(self, solver):
        self._solver = solver
        # version check - this requires Fluent 2024 R1 or newer.
        if self._solver.get_fluent_version() < FluentVersion.v241:
            raise RuntimeError(
                f"Using {str(self._solver.get_fluent_version())}. PySystemCoupling integration requires {str(FluentVersion.v241)} or later."
            )

    @property
    def participant_type(self) -> str:
        """Get participant type."""
        return "FLUENT"

    def get_variables(self) -> List[Variable]:
        """Get variables."""
        return self.__get_syc_setup()["variables"]

    def get_regions(self) -> List[Region]:
        """Get regions."""
        return self.__get_syc_setup()["regions"]

    def get_analysis_type(self) -> str:
        """Get analysis type."""
        return self.__get_syc_setup()["analysis-type"]

    def connect(self, host: str, port: int, name: str) -> None:
        """Connect parallelly."""
        self._solver.setup.models.system_coupling.connect_parallel(
            schost=host, scport=port, scname=name
        )

    def solve(self) -> None:
        """Initialize and solve."""
        self._solver.setup.models.system_coupling.init_and_solve()

    def __get_syc_setup(self) -> dict:
        def get_scp_string() -> str:
            """Get the SCP file contents in the form of an XML string."""

            scp_file_name = "fluent.scp"
            self._solver.setup.models.system_coupling.write_scp_file(
                file_name=scp_file_name
            )

            if self._solver._fluent_connection._remote_instance != None:
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
