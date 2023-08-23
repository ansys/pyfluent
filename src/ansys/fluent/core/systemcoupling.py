"""Module containing System Coupling-related functionality."""

from dataclasses import dataclass
import os
from typing import List
import xml.etree.ElementTree as XmlET


@dataclass
class Variable:
    name: str
    display_name: str
    tensor_type: str
    is_extensive: bool
    location: str
    quantity_type: str


@dataclass
class Region:
    name: str
    display_name: str
    topology: str
    input_variables: List[str]
    output_variables: List[str]


class SystemCoupling:
    """Wrap a System Coupling object, adding methods to discover more about the
    System Coupling related setup and to help solving a System Coupling analysis.

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
        fluent_version = self._solver.get_fluent_version()
        if float(fluent_version[:-2]) < 24.1:
            raise RuntimeError(
                f"Fluent version is {fluent_version}. PySystemCoupling integration requires Fluent 24.1.0 or later."
            )

    @property
    def participant_type(self) -> str:
        return "FLUENT"

    def get_variables(self) -> List[Variable]:
        return self.__get_syc_setup()["variables"]

    def get_regions(self) -> List[Region]:
        return self.__get_syc_setup()["regions"]

    def get_analysis_type(self) -> str:
        return self.__get_syc_setup()["analysis-type"]

    def connect(self, host: str, port: int, name: str) -> None:
        self._solver.setup.models.system_coupling.connect_parallel(
            schost=host, scport=port, scname=name
        )

    def solve(self) -> None:
        self._solver.setup.models.system_coupling.init_and_solve()

    def __get_syc_setup(self) -> dict:
        def get_scp_string() -> str:
            """Get SCP file contents in the form of the XML string."""
            scp_file_name = "fluent.scp"
            self._solver.setup.models.system_coupling.write_scp_file(
                file_name=scp_file_name
            )
            assert os.path.exists(
                scp_file_name
            ), "ERROR: could not create System Coupling .scp file"

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

            if get_name(variable) in {"force", "lorentz-force"}:
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
                "lortentz-force",
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
