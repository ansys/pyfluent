"""Module containing System Coupling-related functionality."""

import os
from dataclasses import dataclass
from typing import List
import xml.etree.ElementTree

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

    @dataclass
    class Variable:
        name: str
        display_name: str
        tensor_type: str
        is_extensive: bool
        location: str
        quantity_type: str

    @dataclass
    class Region(object):
        name: str
        display_name: str
        topology: str
        input_variables: List[str]
        output_variables: List[str]

    def __init__(self, solver):
        self._solver = solver
        self.participant_type = "FLUENT"

    def get_variables(self):
        return self.__get_syc_setup()["variables"]

    def get_regions(self):
        return self.__get_syc_setup()["regions"]

    def get_analysis_type(self):
        return self.__get_syc_setup()["analysis-type"]

    def connect(self, host : str, port : int, name : str):
        self._solver.setup.models.system_coupling.connect_parallel(host = host, port = port, name = name)

    def solve(self):
        self._solver.setup.models.system_coupling.init_and_solve()

    def __get_syc_setup(self):
        setup_info = dict()

        scp_file_name = "fluent.scp"

        self._solver.setup.models.system_coupling.write_scp_file(file_name = scp_file_name)

        assert os.path.exists(scp_file_name), "ERROR: could not create System Coupling .scp file"
        xmlRoot = xml.etree.ElementTree.parse(scp_file_name)
        coSimControl = xmlRoot.find("./CosimulationControl")
        setup_info["analysis-type"] = coSimControl.find("AnalysisType").text
        setup_info["variables"] = list()
        for variable in coSimControl.find("Variables").findall("Variable"):
            name = variable.find("Name").text
            setup_info["variables"].append(
                SystemCoupling.Variable(
                    name = name,
                    display_name = variable.find("DisplayName").text,
                    tensor_type = "Vector" if name in {"force", "lorentz-force"} else "Scalar",
                    is_extensive = name in {"force", "lortentz-force", "heatrate", "heatflow"},
                    location = "Node" if name in {"displacement"} else "Element",
                    quantity_type = variable.find("QuantityType").text
                )
            )
        regions = coSimControl.find("Regions").findall("Region")
        setup_info["regions"] = [
            SystemCoupling.Region(
                name = region.find("Name").text,
                display_name = region.find("DisplayName").text,
                topology = region.find("Topology").text,
                input_variables = [var.text for var in region.find("InputVariables")],
                output_variables = [var.text for var in region.find("OutputVariables")]
            )
            for region in regions
        ]

        # remove the generated scp file
        os.remove(scp_file_name)

        return setup_info
