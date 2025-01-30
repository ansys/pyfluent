# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os.path
from pathlib import Path
import shutil

import pytest

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples


@pytest.mark.fluent_version(">=24.2")
def test_icing_session():
    aero_session = pyfluent.launch_fluent(mode=pyfluent.FluentMode.SOLVER_AERO)
    assert "aero" in dir(aero_session)


@pytest.mark.skip("Run this locally only as of now.")
@pytest.mark.fluent_version(">=24.2")
def test_sample_setup():
    mesh_filepath = examples.download_file(
        "wing.msh.h5",
        "pyfluent/aero",
        return_without_path=False,
    )
    solver_aero_path = str(Path(pyfluent.EXAMPLES_PATH) / "solver_aero")
    if os.path.exists(solver_aero_path + ".cffdb"):
        shutil.rmtree(solver_aero_path + ".cffdb")
    solver = pyfluent.launch_fluent(mode="solver_aero")
    solver.new_project(project_name=solver_aero_path)
    solver.new_simulation(case_file_name=mesh_filepath)

    # Geometric Properties
    solver.aero.AeroWorkflow.Setup.GeometricProperties.MomentCenterX = 0.2
    solver.aero.AeroWorkflow.Setup.GeometricProperties.MomentCenterY = 0
    solver.aero.AeroWorkflow.Setup.GeometricProperties.MomentCenterZ = 0
    solver.aero.AeroWorkflow.Setup.GeometricProperties.RefLength = 0.5334
    solver.aero.AeroWorkflow.Setup.GeometricProperties.RefArea = 0.05334

    # Simulation Conditions
    solver.aero.AeroWorkflow.Setup.SimulationConditions.FlightConditions.FlowSpeed.Parameter = (
        "Mach"
    )
    solver.aero.AeroWorkflow.Setup.SimulationConditions.FlightConditions.FlowSpeed.Distribution = (
        "Constant"
    )
    solver.aero.AeroWorkflow.Setup.SimulationConditions.FlightConditions.FlowSpeed.Mach = (
        0.3
    )
    solver.aero.AeroWorkflow.Setup.SimulationConditions.FlightConditions.FlowDirection.Parameter = (
        "AoA"
    )
    solver.aero.AeroWorkflow.Setup.SimulationConditions.FlightConditions.FlowDirection.DistributionAoa = (
        "Uniform"
    )
    solver.aero.AeroWorkflow.Setup.SimulationConditions.FlightConditions.FlowDirection.AoaMin = (
        3
    )
    solver.aero.AeroWorkflow.Setup.SimulationConditions.FlightConditions.FlowDirection.AoaMax = (
        5
    )
    solver.aero.AeroWorkflow.Setup.SimulationConditions.FlightConditions.FlowDirection.AoaNum = (
        2
    )
    solver.aero.AeroWorkflow.Setup.SimulationConditions.FlightConditions.PresTempInput.Parameter = (
        "Static"
    )
    solver.aero.AeroWorkflow.Setup.SimulationConditions.FlightConditions.PresTempInput.DistributionPressure = (
        "Constant"
    )
    solver.aero.AeroWorkflow.Setup.SimulationConditions.FlightConditions.PresTempInput.DistributionTemperature = (
        "Constant"
    )
    solver.aero.AeroWorkflow.Setup.SimulationConditions.FlightConditions.PresTempInput.Pressure = (
        101325
    )
    solver.aero.AeroWorkflow.Setup.SimulationConditions.FlightConditions.PresTempInput.Temperature = (
        300
    )

    # Solve
    solver.aero.AeroWorkflow.Solution.Solve.Iterations = 10
    solver.aero.AeroWorkflow.Solution.Solve.ShowAdvanced = True
    solver.aero.AeroWorkflow.Setup.AirflowPhysics.Solver.Type = "Pressure based"

    # Calculate, Disconnect, Exit
    solver.aero.AeroWorkflow.Solution.Solve.AeroCalculate()

    solver.exit()
