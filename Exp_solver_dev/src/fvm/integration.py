"""Adapter between setup-software case documents and the Python FVM backend."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

import numpy as np

from .boundary_conditions import BoundaryConditions, MovingWall, NoSlipWall
from .case_definition import CaseDefinition, CaseDocument, load_case_file, parse_case_definition
from .fields import ScalarField, VectorField
from .mesh import BOUNDARY_NAMES, CartesianMesh
from .postprocessing import velocity_extrema
from .simulation import SimulationResult, StepObserver, TransientSolver


@dataclass(frozen=True, slots=True)
class PreparedCase:
    """Solver-owned objects translated from a framework-neutral definition."""

    definition: CaseDefinition
    mesh: CartesianMesh
    initial_velocity: VectorField
    initial_pressure: ScalarField
    boundary_conditions: BoundaryConditions
    solver: TransientSolver


@dataclass(frozen=True, slots=True)
class BackendRun:
    """Simulation output returned to a caller, with a JSON-compatible summary."""

    case_id: str
    simulation: SimulationResult
    summary: dict[str, object]
    artifact_directory: Path | None


class PythonFVMBackend:
    """Prepare and execute the capabilities described by a v1 case document.

    The setup framework only needs to emit the documented JSON contract (or a
    mapping with the same keys). This adapter performs no framework imports;
    unsupported models and boundary types are rejected by the case validator.
    """

    backend_id = "independent-fvm-python"
    supported_schema_version = "1.0"

    def prepare(self, case: CaseDefinition | CaseDocument) -> PreparedCase:
        """Translate validated case data to mesh, fields, BCs, and solver."""
        definition = case if isinstance(case, CaseDefinition) else parse_case_definition(case)
        if definition.schema_version != self.supported_schema_version:
            raise ValueError(f"unsupported schema version: {definition.schema_version}")

        mesh = CartesianMesh(
            nx=definition.nx,
            ny=definition.ny,
            width=definition.width,
            height=definition.height,
        )
        velocity = VectorField(
            mesh,
            name="velocity",
            initial_value=(definition.initial_u, definition.initial_v),
        )
        pressure = ScalarField(
            mesh,
            name="pressure",
            initial_value=definition.initial_pressure,
        )
        boundaries = BoundaryConditions()
        for side in BOUNDARY_NAMES:
            wall = definition.boundary_for(side)
            if wall.boundary_type == "moving_wall":
                boundaries.set("velocity", side, MovingWall(wall.velocity))
            else:
                boundaries.set("velocity", side, NoSlipWall())
        solver = TransientSolver(
            density=definition.density,
            viscosity=definition.dynamic_viscosity,
            **definition.solver.to_solver_kwargs(),
        )
        return PreparedCase(definition, mesh, velocity, pressure, boundaries, solver)

    def run(
        self,
        case: CaseDefinition | CaseDocument,
        output_directory: str | Path | None = None,
        *,
        step_observer: StepObserver | None = None,
    ) -> BackendRun:
        """Run a case mapping and optionally write the stable result artifacts."""
        prepared = self.prepare(case)
        simulation = prepared.solver.run(
            prepared.initial_velocity,
            prepared.initial_pressure,
            prepared.boundary_conditions,
            step_observer=step_observer,
        )
        summary = self._result_summary(prepared.definition, simulation)
        artifact_path: Path | None = None
        if output_directory is not None:
            from .postprocessing import export_simulation_result

            artifact_path = export_simulation_result(simulation, output_directory)
            with (artifact_path / "case.json").open("w", encoding="utf-8") as case_file:
                json.dump(prepared.definition.to_mapping(), case_file, indent=2)
            with (artifact_path / "summary.json").open("w", encoding="utf-8") as summary_file:
                json.dump(summary, summary_file, indent=2)
        return BackendRun(
            case_id=prepared.definition.case_id,
            simulation=simulation,
            summary=summary,
            artifact_directory=artifact_path,
        )

    def run_file(
        self,
        path: str | Path,
        output_directory: str | Path | None = None,
        *,
        step_observer: StepObserver | None = None,
    ) -> BackendRun:
        """Load a JSON case file, execute it, and optionally export artifacts."""
        return self.run(
            load_case_file(path),
            output_directory,
            step_observer=step_observer,
        )

    def _result_summary(
        self, definition: CaseDefinition, simulation: SimulationResult
    ) -> dict[str, object]:
        """Create a unit-labeled, stable summary suitable for setup software."""
        extrema = velocity_extrema(simulation.velocity)
        lid_speed = max(
            float(np.hypot(*definition.boundary_for(side).velocity))
            for side in BOUNDARY_NAMES
        )
        reynolds_number = (
            definition.density * lid_speed * definition.width / definition.dynamic_viscosity
        )
        summary: dict[str, object] = {
            "result_format_version": "1.0",
            "backend": self.backend_id,
            "case_id": definition.case_id,
            "schema_version": definition.schema_version,
            "status": "converged" if simulation.converged else "not_converged",
            "converged": simulation.converged,
            "termination_reason": simulation.termination_reason,
            "steps": simulation.steps,
            "final_time_s": simulation.final_time,
            "mesh": {
                "nx": definition.nx,
                "ny": definition.ny,
                "width_m": definition.width,
                "height_m": definition.height,
            },
            "reynolds_number": reynolds_number,
            "velocity_extrema": {
                "u_min_m_s": extrema.u.minimum,
                "u_min_location_m": list(extrema.u.minimum_location),
                "u_max_m_s": extrema.u.maximum,
                "u_max_location_m": list(extrema.u.maximum_location),
                "v_min_m_s": extrema.v.minimum,
                "v_min_location_m": list(extrema.v.minimum_location),
                "v_max_m_s": extrema.v.maximum,
                "v_max_location_m": list(extrema.v.maximum_location),
                "speed_max_m_s": extrema.maximum_speed,
                "speed_max_location_m": list(extrema.maximum_speed_location),
            },
        }
        if simulation.history:
            last_step = simulation.history[-1]
            summary["conservation"] = {
                "max_divergence_s_inv": last_step.max_divergence_after,
                "global_mass_imbalance_m2_s": last_step.global_mass_imbalance,
            }
            summary["residuals"] = {
                "u_momentum": last_step.u_momentum_residual,
                "v_momentum": last_step.v_momentum_residual,
                "pressure": last_step.pressure_residual,
            }
        return summary