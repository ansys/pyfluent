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
